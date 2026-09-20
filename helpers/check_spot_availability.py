#!/usr/bin/env python3
"""
helpers/check_spot_availability.py

Pre-flight check: verify that g4dn.xlarge (NVIDIA T4 — the most widely
available GPU instance) capacity is available in the target
VPC/subnet/security-group before provisioning AWS Batch infrastructure.

Supports checking Spot capacity, On-Demand capacity, or both:
  1. Instance type offering — is the instance type offered in this AZ at all
  2. Spot price history      — current price vs on-demand, % savings (Spot only)
  3. Spot placement score    — AWS's 1–10 capacity confidence score (Spot only)
  4. Dry-run request         — confirms the subnet/SG combo + IAM allow the launch
                                (RequestSpotInstances for Spot, RunInstances for On-Demand)

Usage:
    python helpers/check_spot_availability.py
    python helpers/check_spot_availability.py --capacity-type on-demand
    python helpers/check_spot_availability.py --capacity-type both

    # Override the course network values if needed:
    python helpers/check_spot_availability.py \\
        --vpc-id        vpc-xxxxxxxxxxxxxxxxx \\
        --subnet-id     subnet-xxxxxxxxxxxxxxxxx \\
        --security-group-id sg-xxxxxxxxxxxxxxxxx \\
    [--instance-type g4dn.xlarge] \\
    [--capacity-type spot|on-demand|both] \\
    [--region       ap-northeast-1]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# ── colour helpers ────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg: str)   -> str: return f"{GREEN}✅ {msg}{RESET}"
def warn(msg: str) -> str: return f"{YELLOW}⚠️  {msg}{RESET}"
def err(msg: str)  -> str: return f"{RED}❌ {msg}{RESET}"
def hdr(msg: str)  -> str: return f"\n{BOLD}{msg}{RESET}"


# ── check 0: instance type offered in this AZ/region ──────────────────────────
def check_instance_offering(ec2, instance_type: str, az: str) -> tuple[bool, str]:
    """Return (offered, verdict) — confirms the instance type exists in this AZ."""
    print(hdr(f"[0] Instance type offering — {instance_type} in {az}"))

    resp = ec2.describe_instance_type_offerings(
        LocationType="availability-zone",
        Filters=[
            {"Name": "instance-type", "Values": [instance_type]},
            {"Name": "location", "Values": [az]},
        ],
    )
    offered = bool(resp.get("InstanceTypeOfferings"))
    if offered:
        print(ok(f"{instance_type} is offered in {az}"))
        return True, "GOOD"
    print(err(f"{instance_type} is NOT offered in {az} — pick a different AZ or instance type"))
    return False, "FAILED"


# ── check: spot price history ─────────────────────────────────────────────────
def check_spot_price(ec2, instance_type: str, az: str) -> tuple[float, str]:
    """
    Return (current_spot_price, verdict_string).
    Also fetches on-demand price from the Pricing API for comparison.
    """
    print(hdr(f"[Spot 1/3] Spot price history — {instance_type} in {az}"))

    resp = ec2.describe_spot_price_history(
        InstanceTypes=[instance_type],
        ProductDescriptions=["Linux/UNIX"],
        AvailabilityZone=az,
        MaxResults=1,
    )

    history = resp.get("SpotPriceHistory", [])
    if not history:
        print(warn(f"No spot price history found for {instance_type} in {az}"))
        return 0.0, "UNKNOWN"

    entry      = history[0]
    spot_price = float(entry["SpotPrice"])
    timestamp  = entry["Timestamp"].strftime("%Y-%m-%d %H:%M UTC")

    print(f"  Spot price : ${spot_price:.4f}/hr  (as of {timestamp})")

    # Fetch on-demand price from AWS Pricing API (us-east-1 only endpoint)
    on_demand = _get_on_demand_price(instance_type, ec2._endpoint.host)
    if on_demand:
        savings = (1 - spot_price / on_demand) * 100
        print(f"  On-demand  : ${on_demand:.4f}/hr")
        print(f"  Savings    : {savings:.0f}% cheaper than on-demand")

    verdict = "GOOD" if spot_price > 0 else "UNKNOWN"
    print(ok(f"Spot price data available — ${spot_price:.4f}/hr") if spot_price > 0
          else warn("Could not determine spot price"))

    return spot_price, verdict


def _get_on_demand_price(instance_type: str, region_endpoint: str) -> float | None:
    """Fetch on-demand price from the AWS Pricing API. Returns None on any error."""
    # Region-to-location-name mapping (subset — add more if needed)
    location_map = {
        "ap-northeast-1": "Asia Pacific (Tokyo)",
        "us-east-1":      "US East (N. Virginia)",
        "us-west-2":      "US West (Oregon)",
        "eu-west-1":      "EU (Ireland)",
    }

    # Derive region from the EC2 endpoint URL
    # e.g. "https://ec2.ap-northeast-1.amazonaws.com" → "ap-northeast-1"
    region = "ap-northeast-1"
    for r in location_map:
        if r in region_endpoint:
            region = r
            break

    location = location_map.get(region)
    if not location:
        return None

    try:
        pricing = boto3.client("pricing", region_name="us-east-1")
        resp = pricing.get_products(
            ServiceCode="AmazonEC2",
            Filters=[
                {"Type": "TERM_MATCH", "Field": "instanceType",    "Value": instance_type},
                {"Type": "TERM_MATCH", "Field": "location",        "Value": location},
                {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Linux"},
                {"Type": "TERM_MATCH", "Field": "tenancy",         "Value": "Shared"},
                {"Type": "TERM_MATCH", "Field": "capacityStatus",  "Value": "Used"},
                {"Type": "TERM_MATCH", "Field": "preInstalledSw",  "Value": "NA"},
            ],
            MaxResults=1,
        )
        if not resp["PriceList"]:
            return None
        product = json.loads(resp["PriceList"][0])
        terms   = product["terms"]["OnDemand"]
        # Traverse the nested pricing structure
        for term in terms.values():
            for dim in term["priceDimensions"].values():
                price_str = dim["pricePerUnit"].get("USD", "0")
                price = float(price_str)
                if price > 0:
                    return price
    except Exception:
        pass
    return None


# ── check: spot placement score ───────────────────────────────────────────────
def check_placement_score(ec2, instance_type: str, subnet_id: str) -> tuple[int, str]:
    """
    Return (score, verdict).  Score is 1–10; ≥ 7 is considered healthy.
    """
    print(hdr(f"[Spot 2/3] Spot placement score — {instance_type}"))

    try:
        resp = ec2.get_spot_placement_scores(
            InstanceTypes=[instance_type],
            TargetCapacity=1,
            TargetCapacityUnitType="units",
            SingleAvailabilityZone=False,
        )
    except ClientError as e:
        # This API requires opt-in; some accounts/regions may not support it.
        print(warn(f"Placement score API unavailable: {e.response['Error']['Message']}"))
        return 0, "SKIPPED"

    scores = resp.get("SpotPlacementScores", [])
    if not scores:
        print(warn("No placement score data returned"))
        return 0, "UNKNOWN"

    # Take the highest score across all AZs in the region
    best = max(scores, key=lambda s: s["Score"])
    score = best["Score"]
    az    = best.get("AvailabilityZoneId", "unknown AZ")

    print(f"  Best score : {score}/10  (AZ: {az})")
    print(f"  All scores : {[s['Score'] for s in scores]}")

    if score >= 7:
        verdict = "GOOD"
        print(ok(f"Placement score {score}/10 — healthy spot capacity"))
    elif score >= 4:
        verdict = "MARGINAL"
        print(warn(f"Placement score {score}/10 — capacity exists but may be constrained"))
    else:
        verdict = "POOR"
        print(err(f"Placement score {score}/10 — low spot capacity in this region"))

    return score, verdict


# ── check: dry-run spot request ───────────────────────────────────────────────
def check_dry_run_spot(ec2, instance_type: str, subnet_id: str, sg_id: str) -> tuple[bool, str]:
    """
    Submit a DryRun spot request to confirm the subnet/SG combination is valid
    and IAM permissions allow spot requests.

    A DryRunOperation error from AWS means the request *would* succeed.
    """
    print(hdr(f"[Spot 3/3] Dry-run spot request — subnet {subnet_id}"))

    # We need a minimal AMI to satisfy the API; use the Amazon Linux 2 parameter
    # to avoid hardcoding an AMI ID.  On DryRun=True the AMI is never actually used.
    try:
        ssm = boto3.client("ssm", region_name=_region_from_ec2(ec2))
        ami_resp = ssm.get_parameter(
            Name="/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"
        )
        ami_id = ami_resp["Parameter"]["Value"]
        print(f"  Using AMI  : {ami_id} (Amazon Linux 2, fetched from SSM — DryRun only)")
    except Exception:
        ami_id = "ami-00000000000000000"  # placeholder; DryRun never launches
        print(f"  Using AMI  : {ami_id} (placeholder — only needed for DryRun API call)")

    try:
        ec2.request_spot_instances(
            DryRun=True,
            InstanceCount=1,
            Type="one-time",
            LaunchSpecification={
                "ImageId":          ami_id,
                "InstanceType":     instance_type,
                "SubnetId":         subnet_id,
                "SecurityGroupIds": [sg_id],
            },
        )
        # Should never reach here on DryRun
        print(ok("Dry-run passed (unexpected non-error — request would succeed)"))
        return True, "GOOD"

    except ClientError as e:
        code = e.response["Error"]["Code"]
        msg  = e.response["Error"]["Message"]

        if code == "DryRunOperation":
            # This is the expected success response for DryRun=True
            print(ok("Dry-run passed — subnet/SG config is valid, IAM allows spot requests"))
            return True, "GOOD"
        elif code == "UnauthorizedOperation":
            print(err(f"IAM permission denied: {msg}"))
            print("   → Ensure your IAM user/role has ec2:RequestSpotInstances permission")
            return False, "FAILED"
        elif code in ("InvalidSubnetID.NotFound", "InvalidGroup.NotFound"):
            print(err(f"Network config error: {msg}"))
            return False, "FAILED"
        else:
            print(warn(f"Unexpected error ({code}): {msg}"))
            return False, "UNKNOWN"


# ── check: dry-run on-demand launch ───────────────────────────────────────────
def check_dry_run_on_demand(ec2, instance_type: str, subnet_id: str, sg_id: str) -> tuple[bool, str]:
    """
    Submit a DryRun RunInstances request to confirm the subnet/SG combination
    is valid and IAM permissions allow an on-demand launch of this instance type.

    A DryRunOperation error from AWS means the request *would* succeed.
    """
    print(hdr(f"[On-Demand] Dry-run launch — subnet {subnet_id}"))

    try:
        ssm = boto3.client("ssm", region_name=_region_from_ec2(ec2))
        ami_resp = ssm.get_parameter(
            Name="/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"
        )
        ami_id = ami_resp["Parameter"]["Value"]
        print(f"  Using AMI  : {ami_id} (Amazon Linux 2, fetched from SSM — DryRun only)")
    except Exception:
        ami_id = "ami-00000000000000000"  # placeholder; DryRun never launches
        print(f"  Using AMI  : {ami_id} (placeholder — only needed for DryRun API call)")

    try:
        ec2.run_instances(
            DryRun=True,
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            SubnetId=subnet_id,
            SecurityGroupIds=[sg_id],
        )
        # Should never reach here on DryRun
        print(ok("Dry-run passed (unexpected non-error — launch would succeed)"))
        return True, "GOOD"

    except ClientError as e:
        code = e.response["Error"]["Code"]
        msg  = e.response["Error"]["Message"]

        if code == "DryRunOperation":
            # This is the expected success response for DryRun=True
            print(ok("Dry-run passed — subnet/SG config is valid, IAM allows on-demand launch"))
            return True, "GOOD"
        elif code == "UnauthorizedOperation":
            print(err(f"IAM permission denied: {msg}"))
            print("   → Ensure your IAM user/role has ec2:RunInstances permission")
            return False, "FAILED"
        elif code == "InsufficientInstanceCapacity":
            print(err(f"No on-demand capacity right now: {msg}"))
            return False, "FAILED"
        elif code in ("InvalidSubnetID.NotFound", "InvalidGroup.NotFound"):
            print(err(f"Network config error: {msg}"))
            return False, "FAILED"
        else:
            print(warn(f"Unexpected error ({code}): {msg}"))
            return False, "UNKNOWN"


def _region_from_ec2(ec2) -> str:
    """Extract the region string from a boto3 EC2 client."""
    return ec2.meta.region_name


# ── subnet → AZ lookup ────────────────────────────────────────────────────────
def get_az_for_subnet(ec2, subnet_id: str) -> str:
    resp = ec2.describe_subnets(SubnetIds=[subnet_id])
    return resp["Subnets"][0]["AvailabilityZone"]


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    # Load .env from repo root (two levels up from helpers/)
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)

    parser = argparse.ArgumentParser(
        description="Check GPU spot instance availability before provisioning Batch infra.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--vpc-id",             default="vpc-3f0b1a58", help="VPC ID (default: course VPC)")
    parser.add_argument("--subnet-id",           default="subnet-b560b3fd", help="Subnet ID (default: course subnet)")
    parser.add_argument("--security-group-id",   default="sg-bd00e4f5", help="Security group ID (default: course security group)")
    parser.add_argument("--instance-type",       default="g4dn.xlarge", help="EC2 instance type — NVIDIA T4 (default: g4dn.xlarge)")
    parser.add_argument("--capacity-type",       choices=["spot", "on-demand", "both"], default="both",
                        help="Which purchasing option(s) to check (default: both)")
    parser.add_argument("--region",              default=os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1"),
                        help="AWS region (default: ap-northeast-1 or AWS_DEFAULT_REGION from .env)")
    args = parser.parse_args()

    print(f"\n{BOLD}=== GPU Availability Check ({args.capacity_type}) ==={RESET}")
    print(f"  Instance type : {args.instance_type}")
    print(f"  Capacity type : {args.capacity_type}")
    print(f"  Region        : {args.region}")
    print(f"  VPC           : {args.vpc_id}")
    print(f"  Subnet        : {args.subnet_id}")
    print(f"  Security group: {args.security_group_id}")

    ec2 = boto3.client("ec2", region_name=args.region)

    # Resolve subnet → AZ for spot price lookup
    try:
        az = get_az_for_subnet(ec2, args.subnet_id)
        print(f"  AZ (from subnet): {az}")
    except ClientError as e:
        print(err(f"Could not resolve subnet {args.subnet_id}: {e.response['Error']['Message']}"))
        sys.exit(1)

    check_spot = args.capacity_type in ("spot", "both")
    check_on_demand = args.capacity_type in ("on-demand", "both")
    bad_verdicts = {"UNKNOWN", "POOR", "FAILED"}

    # ── Check 0: instance type offered in this AZ (always) ───────────────────
    offered, offering_verdict = check_instance_offering(ec2, args.instance_type, az)

    price_verdict = score_verdict = spot_dry_verdict = None
    score = 0
    if check_spot:
        _, price_verdict     = check_spot_price(ec2, args.instance_type, az)
        score, score_verdict = check_placement_score(ec2, args.instance_type, args.subnet_id)
        _, spot_dry_verdict  = check_dry_run_spot(ec2, args.instance_type, args.subnet_id, args.security_group_id)

    on_demand_verdict = None
    if check_on_demand:
        _, on_demand_verdict = check_dry_run_on_demand(ec2, args.instance_type, args.subnet_id, args.security_group_id)

    # ── Final summary ─────────────────────────────────────────────────────────
    print(hdr("=== Summary ==="))
    print(f"  [0] Instance offering : {offering_verdict}")
    if check_spot:
        print(f"  [Spot] Price          : {price_verdict}")
        print(f"  [Spot] Placement score: {score_verdict}  (score: {score}/10)")
        print(f"  [Spot] Dry-run request: {spot_dry_verdict}")
    if check_on_demand:
        print(f"  [On-Demand] Dry-run   : {on_demand_verdict}")

    verdicts = [offering_verdict]
    if check_spot:
        verdicts += [price_verdict, score_verdict, spot_dry_verdict]
    if check_on_demand:
        verdicts += [on_demand_verdict]

    # Placement score is informational — a POOR score with a passing dry-run
    # means capacity is tight but the launch would succeed. Treat POOR as a
    # warning only when the dry-run confirms the request is valid.
    if offering_verdict == "FAILED" or (check_spot and spot_dry_verdict == "FAILED") \
            or (check_on_demand and on_demand_verdict == "FAILED"):
        print(f"\n{err('RESULT: ❌ UNAVAILABLE — request would be rejected (check IAM, network, or capacity)')}")
        sys.exit(1)
    elif any(v in bad_verdicts for v in verdicts if v != "POOR"):
        print(f"\n{warn('RESULT: ⚠️  MARGINAL — capacity may be limited, consider another AZ or instance type')}")
        sys.exit(2)
    else:
        if score_verdict == "POOR":
            print(f"\n{warn('RESULT: ✅ GOOD (with warning) — dry-run passed but spot placement score is low; on-demand is recommended')}")
        else:
            print(f"\n{ok('RESULT: ✅ GOOD — capacity looks healthy, safe to provision Batch infra')}")
        sys.exit(0)


if __name__ == "__main__":
    main()

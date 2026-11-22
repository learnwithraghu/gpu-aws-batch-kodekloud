# 01 — Region, role, and network

Confirm three things before you create anything. Batch launches real machines, so the region, the instance role, and the network have to be right on the first click.

## Open the console

1. Sign in to the AWS console.
2. In the top bar, set the region to **Asia Pacific (Tokyo) `ap-northeast-1`**.
3. Open **AWS Batch**. If a first-run wizard appears, close it. This course creates each piece from the left navigation so you can see it on its own.

## Instance role

The machines Batch starts need a role that can join ECS and write logs.

1. Open **IAM** → **Roles**.
2. Search for **`ecsInstanceRole`**.
3. Open it and confirm the attached policy includes **`AmazonEC2ContainerServiceforEC2Role`**.

If the role is missing, you do not create it by hand in this step. In step 02 (**Step 1: Compute environment configuration**), the **Instance role** field offers **Create a new instance profile**. Use that, and AWS creates and names the role `ecsInstanceRole`.

The Batch service role is separate. On the same page, **Service role** offers **`AWSServiceRoleForBatch`**. Pick that. If it does not exist yet, the form creates it the first time.

## Network

Use the network already used by the teaching compute environments:

| Field | Value |
|-------|--------|
| VPC | `vpc-3f0b1a58` |
| Subnet | `subnet-b560b3fd` (`ap-northeast-1a`) |
| Security group | `sg-bd00e4f5` |

1. Open **VPC** → **Your VPCs** and confirm `vpc-3f0b1a58` is in Tokyo.
2. Open **Subnets**, confirm `subnet-b560b3fd`, and verify **Auto-assign public IPv4 address** is **`Yes`**. EC2 compute environments rely on the subnet setting to assign public IPs rather than a toggle in the Batch console.
3. Open **Security groups** and confirm `sg-bd00e4f5`. Outbound traffic must be allowed so the machine can pull a container image.

## Log group

1. Open **CloudWatch** → **Log groups**.
2. If **`/aws/batch/job`** is missing, choose **Create log group** and name it `/aws/batch/job`.

## You are done when

You are in Tokyo, you know whether `ecsInstanceRole` already exists, and you have the VPC, subnet, and security group written down.

Next: [02 — Create the compute environment](../02-create-the-compute-environment/GUIDE.md).

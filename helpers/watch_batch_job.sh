#!/usr/bin/env bash
# Watch one AWS Batch job until it finishes. Prints statusReason and explains
# RUNNABLE (no container logs yet) vs STARTING/RUNNING (CloudWatch logs).
#
# Usage:
#   helpers/watch_batch_job.sh <job-id>
#   helpers/watch_batch_job.sh <job-id> --region ap-northeast-1
#
# Exit 0 on SUCCEEDED, 1 on FAILED or usage error.
set -u

JOB_ID=""
REGION=""
INTERVAL=15
RUNNABLE_HINT_AFTER=120

while [ $# -gt 0 ]; do
  case "$1" in
    --region)
      [ $# -ge 2 ] || { echo "Error: --region needs a value" >&2; exit 2; }
      REGION="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: helpers/watch_batch_job.sh <job-id> [--region <region>]"
      exit 0 ;;
    -*)
      echo "Unknown option: $1" >&2
      exit 2 ;;
    *)
      if [ -z "$JOB_ID" ]; then JOB_ID="$1"; shift
      else echo "Unexpected argument: $1" >&2; exit 2
      fi ;;
  esac
done

if [ -z "$JOB_ID" ]; then
  echo "Usage: helpers/watch_batch_job.sh <job-id> [--region <region>]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$(dirname "$SCRIPT_DIR")/.env"
REGION="${REGION:-$(grep -E '^AWS_DEFAULT_REGION=' "$ENV_FILE" 2>/dev/null | cut -d= -f2)}"
REGION="${REGION:-$(aws configure get region 2>/dev/null || true)}"
REGION="${REGION:-ap-northeast-1}"
export AWS_DEFAULT_REGION="$REGION"

peek_compute_environment() {
  local queue_arn ce_arn ce_name
  queue_arn="$(aws batch describe-jobs --jobs "$JOB_ID" \
    --query 'jobs[0].jobQueue' --output text 2>/dev/null)" || return 0
  [ -n "$queue_arn" ] && [ "$queue_arn" != "None" ] || return 0
  ce_arn="$(aws batch describe-job-queues --job-queues "$queue_arn" \
    --query 'jobQueues[0].computeEnvironmentOrder[0].computeEnvironment' \
    --output text 2>/dev/null)" || return 0
  [ -n "$ce_arn" ] && [ "$ce_arn" != "None" ] || return 0
  ce_name="${ce_arn##*/}"
  aws batch describe-compute-environments --compute-environments "$ce_name" \
    --query 'computeEnvironments[0].{ce:computeEnvironmentName,status:status,state:state,desired:computeResources.desiredvCpus,max:computeResources.maxvCpus,type:computeResources.type}' \
    --output json 2>/dev/null || true
}

START_EPOCH="$(date +%s)"
RUNNABLE_HINT_SHOWN=0
STARTED_HINT_SHOWN=0

echo "Watching job $JOB_ID (region $REGION), every ${INTERVAL}s"
echo "CloudWatch logs appear only after STARTING/RUNNING — not while RUNNABLE."
echo

while true; do
  RAW="$(aws batch describe-jobs --jobs "$JOB_ID" --output json)" || {
    echo "Error: describe-jobs failed" >&2
    exit 1
  }

  eval "$(python3 -c '
import json, os, shlex, sys
j = json.load(sys.stdin)["jobs"][0]
c = (j.get("attempts") or [{}])[-1].get("container") or j.get("container") or {}
vals = {
    "STATUS": j.get("status") or "",
    "REASON": j.get("statusReason") or "",
    "EXIT": "" if c.get("exitCode") is None else str(c.get("exitCode")),
    "LOG": c.get("logStreamName") or "",
    "QUEUE": (j.get("jobQueue") or "").rsplit("/", 1)[-1],
}
for k, v in vals.items():
    print(f"{k}={shlex.quote(v)}")
' <<<"$RAW")"

  NOW="$(date +%H:%M:%S)"
  LINE="$NOW  status=$STATUS"
  [ -n "$REASON" ] && LINE="$LINE  reason=$REASON"
  [ -n "$EXIT" ] && LINE="$LINE  exit=$EXIT"
  [ -n "$LOG" ] && LINE="$LINE  log=$LOG"
  echo "$LINE"

  case "$STATUS" in
    RUNNABLE)
      ELAPSED=$(( $(date +%s) - START_EPOCH ))
      if [ "$ELAPSED" -ge "$RUNNABLE_HINT_AFTER" ] && [ "$RUNNABLE_HINT_SHOWN" -eq 0 ]; then
        RUNNABLE_HINT_SHOWN=1
        echo
        echo "Still RUNNABLE after ${RUNNABLE_HINT_AFTER}s."
        echo "  No container has started → no /aws/batch/job logs yet."
        echo "  This is usually Spot capacity, quota, or CE placement — not describe_items.py."
        echo "  Queue: $QUEUE"
        echo "  Check CE scale attempt:"
        peek_compute_environment
        echo "  Escape hatch: cancel this job, set BATCH_JOB_QUEUE to the on-demand queue, resubmit."
        echo
      fi
      ;;
    STARTING|RUNNING)
      if [ "$STARTED_HINT_SHOWN" -eq 0 ]; then
        STARTED_HINT_SHOWN=1
        echo "  Container is starting/running. Logs: /aws/batch/job"
        [ -n "$LOG" ] && echo "  Stream: $LOG"
      fi
      ;;
    SUCCEEDED)
      echo
      echo "SUCCEEDED"
      exit 0
      ;;
    FAILED)
      echo
      echo "FAILED"
      [ -n "$LOG" ] && echo "Read logs: aws logs get-log-events --log-group-name /aws/batch/job --log-stream-name $(printf %q "$LOG") --region $REGION"
      exit 1
      ;;
  esac

  sleep "$INTERVAL"
done

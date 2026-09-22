#!/usr/bin/env bash
# Run the AWS Batch smoke tests in order:
#   [1/4] Spot pre-flight   (helpers/check_spot_availability.py --capacity-type spot)
#   [2/4] GPU spot          (helpers/test_gpu_batch.py --capacity-type spot)
#   [3/4] GPU on-demand     (helpers/test_gpu_batch.py --capacity-type on-demand)
#   [4/4] CPU               (helpers/test_cpu_batch.py)
#
# The tests reuse persistent Batch resources (create-if-missing, never delete),
# so repeat runs skip the create/wait/delete cycle. Run helpers/teardown.py to
# remove everything when you are done with the course.
#
# Usage:
#   helpers/run_smoke_tests.sh [--skip-preflight] [--continue-on-failure]
#
#   --skip-preflight       Skip the spot availability pre-flight check
#   --continue-on-failure  Run every stage even if an earlier one fails
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

SKIP_PREFLIGHT=false
CONTINUE_ON_FAILURE=false
for arg in "$@"; do
  case "$arg" in
    --skip-preflight)      SKIP_PREFLIGHT=true ;;
    --continue-on-failure) CONTINUE_ON_FAILURE=true ;;
    -h|--help)
      echo "Usage: helpers/run_smoke_tests.sh [--skip-preflight] [--continue-on-failure]"
      echo ""
      echo "Runs the smoke tests in order: spot pre-flight, GPU spot, GPU on-demand, CPU."
      echo "  --skip-preflight       Skip the spot availability pre-flight check"
      echo "  --continue-on-failure  Run every stage even if an earlier one fails"
      exit 0 ;;
    *)
      echo "Unknown option: $arg" >&2
      echo "Usage: helpers/run_smoke_tests.sh [--skip-preflight] [--continue-on-failure]" >&2
      exit 2 ;;
  esac
done

UV=(uv run --with boto3 --with python-dotenv python)

run_stage() {
  local index="$1" total="$2" label="$3"; shift 3
  echo
  echo "━━ [$index/$total] $label ━━"
  if "${UV[@]}" "$@"; then
    echo "[$index/$total] $label — PASSED"
    return 0
  fi
  echo "[$index/$total] $label — FAILED" >&2
  return 1
}

TOTAL=4
STAGE=0
FAILED_STAGES=()

STAGE=$((STAGE + 1))
if [ "$SKIP_PREFLIGHT" = "true" ]; then
  echo "[$STAGE/$TOTAL] Spot pre-flight — SKIPPED"
elif ! run_stage "$STAGE" "$TOTAL" "Spot pre-flight (check_spot_availability.py)" \
      helpers/check_spot_availability.py --capacity-type spot; then
  FAILED_STAGES+=("spot pre-flight")
  if [ "$CONTINUE_ON_FAILURE" != "true" ]; then
    echo
    echo "Stopped at stage $STAGE/$TOTAL."
    exit 1
  fi
fi

STAGE=$((STAGE + 1))
if ! run_stage "$STAGE" "$TOTAL" "GPU spot smoke test (test_gpu_batch.py)" \
      helpers/test_gpu_batch.py --capacity-type spot; then
  FAILED_STAGES+=("GPU spot")
  if [ "$CONTINUE_ON_FAILURE" != "true" ]; then
    echo
    echo "Stopped at stage $STAGE/$TOTAL."
    exit 1
  fi
fi

STAGE=$((STAGE + 1))
if ! run_stage "$STAGE" "$TOTAL" "GPU on-demand smoke test (test_gpu_batch.py)" \
      helpers/test_gpu_batch.py --capacity-type on-demand; then
  FAILED_STAGES+=("GPU on-demand")
  if [ "$CONTINUE_ON_FAILURE" != "true" ]; then
    echo
    echo "Stopped at stage $STAGE/$TOTAL."
    exit 1
  fi
fi

STAGE=$((STAGE + 1))
if ! run_stage "$STAGE" "$TOTAL" "CPU smoke test (test_cpu_batch.py)" \
      helpers/test_cpu_batch.py; then
  FAILED_STAGES+=("CPU")
  if [ "$CONTINUE_ON_FAILURE" != "true" ]; then
    echo
    echo "Stopped at stage $STAGE/$TOTAL."
    exit 1
  fi
fi

echo
if [ "${#FAILED_STAGES[@]}" -gt 0 ]; then
  echo "Completed with failures: ${FAILED_STAGES[*]}"
  exit 1
fi
echo "All $TOTAL stages passed."

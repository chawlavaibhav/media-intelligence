#!/usr/bin/env bash
# RES-001 budget guard. Sourced by every acquisition script.
# Amendment 01 + RES-001 RESOURCE BUDGET: target 4-6 GB retained, hard stop 8 GB,
# maintain >= 12 GB free disk at all times. Never start work that could breach either.
set -euo pipefail

RAW_DIR="${RAW_DIR:-resources/corpus/raw}"
HARD_STOP_GB=8
FREE_FLOOR_GB=12

gb() { echo "scale=2; $1/1073741824" | bc; }

free_gb()    { df -k . | awk 'NR==2{printf "%.2f", $4/1048576}'; }
retained_gb(){ [ -d "$RAW_DIR" ] && du -sk "$RAW_DIR" 2>/dev/null | awk '{printf "%.2f", $1/1048576}' || echo "0.00"; }

# check_budget <bytes_to_download> <bytes_after_extraction>
check_budget() {
  local dl_b="$1" ext_b="$2"
  local dl ext free retained after peak_need
  dl=$(gb "$dl_b"); ext=$(gb "$ext_b")
  free=$(free_gb); retained=$(retained_gb)
  after=$(echo "scale=2; $retained + $ext" | bc)
  peak_need=$(echo "scale=2; $dl + $ext" | bc)
  local free_after_peak
  free_after_peak=$(echo "scale=2; $free - $peak_need" | bc)

  echo "  budget check:"
  echo "    free now            : ${free} GB"
  echo "    retained now        : ${retained} GB"
  echo "    this download       : ${dl} GB"
  echo "    after extraction    : ${ext} GB  -> retained would be ${after} GB"
  echo "    peak transient need : ${peak_need} GB -> free at peak ${free_after_peak} GB"

  if (( $(echo "$after > $HARD_STOP_GB" | bc -l) )); then
    echo "    STOP: retained ${after} GB would exceed the ${HARD_STOP_GB} GB hard stop." >&2; return 1
  fi
  if (( $(echo "$free_after_peak < $FREE_FLOOR_GB" | bc -l) )); then
    echo "    STOP: free space at peak ${free_after_peak} GB would breach the ${FREE_FLOOR_GB} GB floor." >&2; return 1
  fi
  echo "    OK (under ${HARD_STOP_GB} GB retained, above ${FREE_FLOOR_GB} GB free)"
  return 0
}

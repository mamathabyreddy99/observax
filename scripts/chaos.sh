#!/usr/bin/env bash
# Usage:
#   ./scripts/chaos.sh <gateway|orders|payments> latency <ms>
#   ./scripts/chaos.sh <gateway|orders|payments> errors <0.0-1.0>
#   ./scripts/chaos.sh <gateway|orders|payments> reset
set -euo pipefail
svc=${1:?service}; mode=${2:?mode}; val=${3:-0}
case "$svc" in
  gateway)  port=8001 ;;
  orders)   port=8002 ;;
  payments) port=8003 ;;
  *) echo "unknown service: $svc"; exit 1 ;;
esac
case "$mode" in
  latency) body="{\"latency_ms\": $val}" ;;
  errors)  body="{\"error_rate\": $val}" ;;
  reset)   body='{"latency_ms": 0, "error_rate": 0}' ;;
  *) echo "unknown mode: $mode"; exit 1 ;;
esac
curl -s -X POST "localhost:$port/chaos" -H 'Content-Type: application/json' -d "$body"; echo

#!/usr/bin/env bash
# provider-health-check.sh — probe OpenAI-compatible providers in bulk
# Usage: ./provider-health-check.sh
# Reads API keys from ~/.hermes/.env (does not print key values).
# Output: per-provider status (OK/FAIL/DEAD + model counts + latency samples).

set -uo pipefail
ENV_FILE="$HOME/.hermes/.env"
MAX_TOKENS=10
PROBE_MSG='{"role":"user","content":"h"}'

get_key() {
  local name="$1"
  grep "^${name}=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'"
}

probe_provider() {
  local label="$1" key="$2" base="$3"
  local -a models=()
  local code ms
  # Fetch model list
  code=$(curl -sS -m 15 -o /tmp/pv_models.json -w '%{http_code}' \
    "${base}/models" -H "Authorization: Bearer ${key}" 2>/dev/null)
  if [[ "$code" == "200" ]]; then
    models=($(python3 -c 'import json,sys; d=json.load(open("/tmp/pv_models.json")); [print(m["id"]) for m in d.get("data",[])]' 2>/dev/null))
  else
    echo "  ⚠️  ${label}: /v1/models HTTP ${code}"
    return
  fi
  echo "  ✅  ${label}: ${#models[@]} models at ${base}"
  # Probe up to 4 models for latency
  local probed=0
  for m in "${models[@]:0:4}"; do
    [[ -z "$m" ]] && continue
    local body=$(python3 -c "import json; print(json.dumps({'model':'${m}','messages':[{'role':'user','content':'h'}],'max_tokens':${MAX_TOKENS}}))")
    local start end elapsed
    start=$(date +%s%N)
    code=$(curl -sS -m 20 -o /dev/null -w '%{http_code}' \
      -X POST "${base}/chat/completions" \
      -H "Authorization: Bearer ${key}" \
      -H "Content-Type: application/json" \
      -d "$body" 2>/dev/null)
    end=$(date +%s%N)
    elapsed=$(( (end - start) / 1000000 ))
    if [[ "$code" == "200" ]]; then
      echo "      ${m}: OK (${elapsed}ms)"
      probed=$((probed + 1))
    elif [[ "$code" == "429" ]]; then
      echo "      ${m}: 429 rate-limited"
    elif [[ "$code" == "503" || "$code" == "500" ]]; then
      echo "      ${m}: HTTP ${code} — possibly backend down"
    else
      echo "      ${m}: HTTP ${code}"
    fi
  done
  if [[ $probed -eq 0 ]]; then
    echo "      ⚠️  0/${#models[@]} models returned OK — provider may be degraded"
  fi
}

echo "=== Provider Health Check — $(date '+%H:%M:%S') ==="
echo ""

# 9router (local)
NINE_KEY=$(get_key NINE_ROUTER_API_KEY)
if [[ -n "$NINE_KEY" ]]; then
  probe_provider "9router" "$NINE_KEY" "http://localhost:20128/v1"
else
  echo "  ⚠️  9router: NINE_ROUTER_API_KEY not found"
fi

# OpenRouter
OPENROUTER_KEY=$(get_key OPENROUTER_API_KEY)
if [[ -n "$OPENROUTER_KEY" ]]; then
  probe_provider "OpenRouter" "$OPENROUTER_KEY" "https://openrouter.ai/api/v1"
else
  echo "  ⚠️  OpenRouter: OPENROUTER_API_KEY not found"
fi

# Huancheng
HUANCHENG_KEY=$(get_key HUANCHENG_API_KEY)
if [[ -n "$HUANCHENG_KEY" ]]; then
  probe_provider "Huancheng" "$HUANCHENG_KEY" "https://api.hcnsec.cn/v1"
else
  echo "  ⚠️  Huancheng: HUANCHENG_API_KEY not found"
fi

echo ""
echo "=== Done ==="

#!/bin/sh
# keys.sh — Niumination central credential broker (macOS)
#
# Ponytail design:
#   - ONE control plane for every direct AI-API key used by jcode/opencode/hermes.
#   - Backed by macOS Keychain (no sudo, encrypted at rest, survives reboot).
#   - Plaintext fallback only if `security` is missing (non-macOS / CI).
#   - NEVER stores values in this file or in git. Only key NAMES live here.
#
# Usage:
#   keys get <canonical>          # print raw value (for scripts/debug)
#   keys set <canonical> <value>  # store (upsert)
#   keys del <canonical>          # remove
#   keys list                     # canonical names present
#   keys env                      # emit `export ALIAS=value` for every alias
#   keys env <canonical>          # emit exports for one credential's aliases
#
# Canonical name  ->  env-var aliases consumed by the ecosystem
# (9router keeps its OWN aggregator store; it is not part of this broker —
#  it is reached via the single `nine_router` key only.)
SERVICE="niumination"

# canonical -> space-separated alias env vars
REGISTRY='
opencode_zen   OPENCODE_ZEN_API_KEY OPENCODE_API_KEY OPENCODE_GO_API_KEY
openrouter     OPENROUTER_API_KEY
gemini         GEMINI_API_KEY GOOGLE_API_KEY
github         GITHUB_TOKEN
fal            FAL_KEY
telegram       TELEGRAM_BOT_TOKEN
agentrouter    AGENTROUTER_API_KEY JCODE_PROVIDER_AGENTROUTER_API_KEY
juan           JUAN_ROUTER_API_KEY
nine_router    NINE_ROUTER_API_KEY
huancheng      HUANCHENG_API_KEY AUXILIARY_VISION_API_KEY JCODE_PROVIDER_HUANCHENG_API_KEY
aerolink       AEROLINK_API_KEY
tavily         TAVILY_API_KEY
anthropic      ANTHROPIC_API_KEY
vercel         VERCEL_TOKEN
discord        DISCORD_BOT_TOKEN
bing           BING_API_KEY JCODE_BING_API_KEY
nvidia_nim     NVIDIA_NIM_API_KEY
'

FALLBACK="${XDG_CONFIG_HOME:-$HOME/.config}/niumination/keys.fallback"

set -u

canon_exists(){ echo "$REGISTRY" | awk -v c="$1" 'NF>=1 && $1==c {found=1} END{exit !found}'; }

aliases_of(){
  echo "$REGISTRY" | while read -r c rest; do
    [ "$c" = "$1" ] && { echo "$rest"; break; }
  done
}

kc_get(){ security find-generic-password -a "$1" -s "$SERVICE" -w 2>/dev/null; }
kc_set(){
  security add-generic-password -a "$1" -s "$SERVICE" -w "$2" -U 2>/dev/null \
    || printf '%s\t%s\n' "$1" "$2" >>"$FALLBACK"
}
kc_del(){ security delete-generic-password -a "$1" -s "$SERVICE" 2>/dev/null >/dev/null; }
kc_list(){
  echo "$REGISTRY" | while read -r c rest; do
    [ -n "$c" ] && { v=$(kc_get "$c"); [ -n "$v" ] && echo "$c"; }
  done
}

cmd="${1:-help}"; shift 2>/dev/null || true
case "$cmd" in
  get)
    [ $# -ge 1 ] && canon_exists "$1" && kc_get "$1"
    ;;
  set)
    [ $# -ge 2 ] || { echo "usage: keys set <canonical> <value>" >&2; exit 1; }
    canon_exists "$1" || { echo "unknown canonical: $1 (add to REGISTRY)" >&2; exit 1; }
    kc_set "$1" "$2" && echo "stored: $1"
    ;;
  del)
    [ $# -ge 1 ] && canon_exists "$1" && kc_del "$1" && echo "deleted: $1"
    ;;
  list)
    kc_list
    ;;
  env)
    if [ $# -ge 1 ]; then
      c="$1"; canon_exists "$c" || { echo "unknown canonical: $c" >&2; exit 1; }
      set -- "$c"
    fi
    echo "$REGISTRY" | while read -r c rest; do
      [ -n "$c" ] || continue
      [ $# -ge 1 ] && [ "$c" != "$1" ] && continue
      v=$(kc_get "$c"); [ -n "$v" ] || continue
      for a in $rest; do printf 'export %s=%s\n' "$a" "$v"; done
    done
    ;;
  help|*)
    cat <<USAGE
keys.sh — Niumination credential broker (macOS Keychain)

  keys get <canonical>          raw value
  keys set <canonical> <value>  store/upsert
  keys del <canonical>          remove
  keys list                     canonical names present
  keys env [<canonical>]        emit export lines for shell/tool consumption

Canonical names:
$(echo "$REGISTRY" | awk 'NF>=1{print "  "$1}')
USAGE
    ;;
esac

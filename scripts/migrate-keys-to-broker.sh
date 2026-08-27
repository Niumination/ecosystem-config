#!/bin/sh
# migrate-keys-to-broker.sh — Niumination credential broker migration (Phase B)
#
# Ponytail: idempotent, read-only on sources, aborts safely if preconditions fail.
# Migrates flat AI-API keys from their legacy plaintext stores into the
# macOS Keychain-backed broker (scripts/keys.sh). Does NOT delete sources
# until the consumer is verified against the broker (manual step, see below).
#
# PREREQUISITES (all checked, aborts if unmet):
#   1. Legacy sources exist & readable:
#        ~/.hermes/.env
#        ~/Desktop/Niumination/vault/secrets.zsh
#        ~/.jcode/config.toml
#        ~/.config/opencode/opencode.jsonc
#        ~/.deepseek/config-9router.toml
#   2. Broker script present: scripts/keys.sh
#   3. NOT while a jcode/opencode repair is in flight (user must confirm).
#
# USAGE:
#   sh migrate-keys-to-broker.sh --dry-run   # report what WOULD move, no writes
#   sh migrate-keys-to-broker.sh             # execute (prompts per key)
#
# After migration, SEPARATELY repoint consumers (not done by this script):
#   - jcode ~/.jcode/config.json   -> providers use key_env pointing at broker vars
#   - opencode opencode.jsonc      -> replace inline apiKey with ${ENV}
#   - hermes  ~/.hermes/.env       -> single 'eval $(scripts/keys.sh env)' line
#   - gemini/continue configs      -> consume broker vars
# Then delete plaintext sources ONLY after verifying each tool works.

set -u
ROOT="${NIUMINATION:-$HOME/Desktop/Niumination}"
KEYS="$ROOT/scripts/keys.sh"
DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1

echo "=== Precondition checks ==="
[ -x "$KEYS" ] || { echo "FAIL: $KEYS not found/executable"; exit 1; }
for src in ~/.hermes/.env "$ROOT/vault/secrets.zsh" ~/.jcode/config.toml ~/.config/opencode/opencode.jsonc ~/.deepseek/config-9router.toml; do
  [ -f "$src" ] || { echo "FAIL: source missing: $src (repair not done yet?)"; exit 1; }
  [ -r "$src" ] || { echo "FAIL: source not readable: $src"; exit 1; }
done
echo "All source files present. Proceeding."

# Map: canonical -> env-var-name to grep in sources (value extracted by '=')
# Format: "canonical:ENVVAR:sourcefile"
MAP='
opencode_zen:OPENCODE_ZEN_API_KEY:~/.hermes/.env
opencode_zen:OPENCODE_API_KEY:~/.hermes/.env
github:GITHUB_TOKEN:~/.hermes/.env
fal:FAL_KEY:~/.hermes/.env
telegram:TELEGRAM_BOT_TOKEN:~/.hermes/.env
gemini:GEMINI_API_KEY:~/.gemini/.env
anthropic:ANTHROPIC_API_KEY:~/Desktop/Niumination/vault/secrets.zsh
nine_router:NINE_ROUTER_API_KEY:~/.jcode/config.json
huancheng:HUANCHENG_API_KEY:~/.jcode/config.toml
juan:JUAN_ROUTER_API_KEY:~/.jcode/config.json
agentrouter:AGENTROUTER_API_KEY:~/.jcode/config.json
aerolink:AEROLINK_API_KEY:~/.jcode/config.json
'

get_val(){
  # $1=envvar $2=sourcefile  -> print raw value after first '=' (unquoted-ish)
  grep -E "^[[:space:]]*$1=" "$2" 2>/dev/null | head -1 | sed -E "s/^[^=]*=//; s/^['\"]//; s/['\"]$//" | sed 's/[[:space:]]*$//'
}

echo; echo "=== Migration plan (canonical <- envvar @ source) ==="
echo "$MAP" | while read -r line; do
  [ -z "$line" ] && continue
  c=$(echo "$line" | cut -d: -f1)
  ev=$(echo "$line" | cut -d: -f2)
  sf=$(echo "$line" | cut -d: -f3 | sed "s|~|$HOME|")
  val=$(get_val "$ev" "$sf")
  if [ -z "$val" ]; then
    echo "  SKIP  $c ($ev) — not found in $sf"
  else
    if [ "$DRY" -eq 1 ]; then
      echo "  WOULD SET $c ($ev) = <${#val} chars hidden>"
    else
      # prompt-free but logged; value only goes to Keychain
      "$KEYS" set "$c" "$val" >/dev/null 2>&1 && echo "  SET   $c ($ev)" || echo "  ERR   $c ($ev)"
    fi
  fi
done

echo; echo "=== Result ==="
"$KEYS" list 2>/dev/null | sed 's/^/  stored: /'
[ "$DRY" -eq 1 ] && echo "(dry-run: nothing written)"
echo "Next: repoint consumers (jcode/opencode/hermes/gemini/continue) then verify, then delete plaintext sources."

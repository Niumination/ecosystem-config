#!/bin/sh
# thermal-guardian.sh — Niumination ecosystem (Intel Mac, 15W TDP)
#
# Keeps the Mac cool under heavy AI-agent load by dynamically renicing CPU hogs
# by NAME (survives PID churn from respawning agent sub-processes).
#
# Design (Ponytail): no sudo, no external deps beyond osx-cpu-temp (brew),
# never kills an agent session, reversible (restores priority when cool).
#
# Triggers:
#   temp >= CRIT  -> SIGSTOP delegated batch jobs + heavy renice
#   temp >= HOT   -> renice batch/proxy/agents down by name
#   temp <  COOL  -> restore interactive agents to normal, resume paused batch
#
# Run:  INTERVAL=15 HOT=82 CRIT=92 COOL=72 sh thermal-guardian.sh
#       (or launch via com.niumination.thermal-guardian.plist)

set -u
INTERVAL="${INTERVAL:-15}"
HOT="${HOT:-82}"      # start throttling
CRIT="${CRIT:-92}"    # emergency: pause batch jobs
COOL="${COOL:-72}"    # restore normal priority
LOG="${LOG:-$HOME/Desktop/Niumination/scripts/.thermal-guardian.log}"
TEMP_BIN="$(command -v osx-cpu-temp || echo /usr/local/bin/osx-cpu-temp)"

[ -x "$TEMP_BIN" ] || { echo "osx-cpu-temp missing: brew install osx-cpu-temp" >&2; exit 1; }

log(){ printf '%s  %s\n' "$(date '+%H:%M:%S')" "$*" >>"$LOG"; }
temp_num(){ "$TEMP_BIN" 2>/dev/null | grep -oE '[0-9]+(\.[0-9]+)?' | head -1; }

# pattern:niceness  (higher niceness = lower priority = cooler)
RULES="extract_:15
\.py$:12
custom-server\.js:8
9router:8
mcp-server:6
opencode:4
_jcode-bin:2"

renice_name(){
  pat="$1"; lvl="$2"
  for pid in $(pgrep -f "$pat" 2>/dev/null); do
    cur=$(ps -o nice= -p "$pid" 2>/dev/null | tr -d ' ')
    [ -n "$cur" ] || continue
    # only lower priority (raise nice) when it is currently higher priority
    if [ "$cur" -lt "$lvl" ] 2>/dev/null; then
      renice "$lvl" -p "$pid" >/dev/null 2>&1 && log "renice $pid ($pat) -> $lvl"
    fi
  done
}

apply_rules(){
  echo "$RULES" | while IFS= read -r line; do
    [ -z "$line" ] && continue
    p=$(printf '%s' "$line" | cut -d: -f1)
    n=$(printf '%s' "$line" | cut -d: -f2)
    renice_name "$p" "$n"
  done
}

stop_batch(){
  for pid in $(pgrep -f "extract_.*\.py" 2>/dev/null); do
    ps -o state= -p "$pid" 2>/dev/null | grep -q 'T' || { kill -STOP "$pid" 2>/dev/null && log "STOP batch $pid"; }
  done
}
cont_batch(){
  for pid in $(pgrep -f "extract_.*\.py" 2>/dev/null); do
    ps -o state= -p "$pid" 2>/dev/null | grep -q 'T' && { kill -CONT "$pid" 2>/dev/null && log "CONT batch $pid"; }
  done
}

echo "thermal-guardian started pid $$ (HOT=$HOT CRIT=$CRIT COOL=$COOL interval=${INTERVAL}s)"
log "START pid $$"
while :; do
  t=$(temp_num)
  [ -z "$t" ] && { sleep "$INTERVAL"; continue; }
  if awk "BEGIN{exit !($t>=$CRIT)}"; then
    log "CRIT ${t}C"; stop_batch; apply_rules
  elif awk "BEGIN{exit !($t>=$HOT)}"; then
    log "HOT ${t}C"; apply_rules
  else
    cont_batch
    for pid in $(pgrep -f "opencode|_jcode-bin" 2>/dev/null); do
      cur=$(ps -o nice= -p "$pid" 2>/dev/null | tr -d ' ')
      [ -n "$cur" ] && [ "$cur" -gt 0 ] 2>/dev/null && renice 0 -p "$pid" >/dev/null 2>&1
    done
  fi
  sleep "$INTERVAL"
done

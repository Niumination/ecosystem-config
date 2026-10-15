#!/bin/bash
# =============================================================================
# Template — wrapper for a Hermes cron job created with no_agent=true
# =============================================================================
# Copy to ~/.hermes/scripts/<job-name>.sh and replace REAL_SCRIPT below.
# The scheduler runs THIS file as the job and delivers its stdout verbatim to
# the target, with no LLM involved: no token cost, and no dependency on any
# model provider being reachable or funded.
#
# Fill in:
#   REAL_SCRIPT  absolute path to the real work (build/sync/probe script)
#   JOB_NAME     short label used for the log file name and the message header
#   TOOLS        binaries the real script needs (checked before starting)
#
# Properties this template exists to guarantee:
#   * PATH is PREPENDED, never assigned — a scheduler inherits a minimal PATH,
#     and a hand-written list silently drops binaries you did not think about.
#   * every required binary is asserted up front, so a missing one fails in
#     milliseconds instead of minutes into the run.
#   * stdout stays short (it is delivered verbatim) while the full log is kept.
#   * failure exits non-zero and prints the failing step + log tail, because
#     empty stdout would look identical to success.
# =============================================================================

REAL_SCRIPT="$HOME/Desktop/<ecosystem>/scripts/<real-script>.sh"
JOB_NAME="<job-name>"
TOOLS="hermes gh git openssl"          # binaries the real script depends on
KEEP_LOGS=10
LOGDIR="$HOME/.hermes/logs"

# 1. PATH: prepend, never assign
for d in "$HOME/.local/bin" "$HOME/src/hermes-agent/.venv/bin" /usr/local/bin /opt/homebrew/bin; do
  [[ -d "$d" ]] && case ":$PATH:" in *":$d:"*) ;; *) PATH="$d:$PATH" ;; esac
done
export PATH

# 2. assert prerequisites before doing any work
missing=""
for t in $TOOLS; do command -v "$t" >/dev/null 2>&1 || missing="$missing $t"; done
if [[ -n "$missing" ]]; then
  echo "❌ ${JOB_NAME}: command not found:$missing"
  echo "   PATH=$PATH"
  exit 1
fi
if [[ ! -f "$REAL_SCRIPT" ]]; then
  echo "❌ ${JOB_NAME}: script not found: $REAL_SCRIPT"
  exit 1
fi

mkdir -p "$LOGDIR"
LOG="$LOGDIR/${JOB_NAME}-$(date +%Y%m%d-%H%M%S).log"
START=$(date +%s)
STAMP=$(date '+%Y-%m-%d %H:%M')

# 3. run the real work, capture everything, keep the exit code
bash "$REAL_SCRIPT" "$@" >"$LOG" 2>&1
RC=$?
DUR=$(( $(date +%s) - START ))
DURASI="$((DUR/60))m $((DUR%60))s"

rotate_logs() {
  ls -1t "$LOGDIR"/${JOB_NAME}-*.log 2>/dev/null | tail -n +$((KEEP_LOGS+1)) \
    | while read -r f; do rm -f "$f"; done
}

# 4a. failure: loud, with the cause visible, non-zero exit
if [[ $RC -ne 0 ]]; then
  echo "❌ ${JOB_NAME} GAGAL (exit $RC) — $STAMP · $DURASI"
  echo
  last=$(grep -E '^\[' "$LOG" | tail -1)
  [[ -n "$last" ]] && echo "Langkah terakhir: ${last#*] }"
  echo
  echo "--- 15 baris terakhir ---"
  tail -15 "$LOG"
  echo
  echo "Tidak ada yang diperbarui. Jalankan manual: bash $REAL_SCRIPT"
  rotate_logs
  exit 1
fi

# 4b. success: short summary only (this is what gets delivered)
echo "✅ ${JOB_NAME} — $STAMP · selesai dalam $DURASI"
echo
# replace with the markers your real script prints
grep -E '^\[|✓|pushed|commit' "$LOG" | tail -12 | sed 's/^/• /'
echo
rotate_logs
exit 0

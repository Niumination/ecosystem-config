#!/bin/bash
# reload-gateway.sh — restart Hermes gateway via launchd, drain-safe.
#
# Kenapa file ini ada (bukan `launchctl bootout && launchctl bootstrap`):
#   bootout hanya mengirim SIGTERM lalu LANGSUNG return. Gateway punya 2 proses
#   (supervisor + worker A2A). bootstrap yang dipanggil sekejap setelah bootout
#   => label masih terdaftar => "Bootstrap failed: 5: Input/output error".
#   Sumber: hermes_cli/gateway.py:3831 "bootout only SIGTERMs and every
#   bootstrap during the drain fails EIO".
#
# Urutan wajib: bootout -> tunggu PID lama mati -> bootstrap -> retry sampai
# label terdaftar DAN punya PID positif.
#
# JANGAN jalankan dari sesi Telegram/Hermes: bootout membunuh process coalition
# gateway = bunuh diri sendiri. Jalankan dari shell terpisah (Terminal.app).
#
# Exit: 0 = OK, 1 = drain timeout, 2 = bootstrap gagal sampai budget, 3 = self-kill ditolak.

set -uo pipefail

LABEL="ai.hermes.gateway"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/.hermes/logs/gateway-reload.log"
DOMAIN="gui/$(id -u)"
BUDGET=180   # detik, sama dengan default _launchd_reload_budget Hermes

log() { printf '[%s] %s\n' "$(date '+%F %T')" "$*" >>"$LOG"; }
say() { printf '%s\n' "$*"; }

# --- guard: jangan bunuh diri sendiri ---------------------------------------
for p in $$ $(ps -o ppid= -p $$) ; do
  if ps -o command= -p "$p" 2>/dev/null | grep -q "hermes_cli.main gateway"; then
    say "DITOLAK: script dijalankan dari dalam proses gateway (ancestor PID $p)."
    say "Jalankan dari shell terpisah — bootout akan mematikan sesi ini."
    exit 3
  fi
  p=$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')
  [ -z "$p" ] || [ "$p" = "1" ] && break
done

# --- preflight ---------------------------------------------------------------
[ -f "$PLIST" ] || { say "GAGAL: plist tidak ada: $PLIST"; exit 2; }
plutil -lint "$PLIST" >/dev/null 2>&1 || { say "GAGAL: plist tidak valid"; exit 2; }

# PID dari launchctl bisa "0"/"-1" (crashed) — bukan proses nyata.
# Parse ke integer dulu supaya aritmetika di bawah tidak salah.
OLD_PID=$(launchctl list "$LABEL" 2>/dev/null \
  | awk -F'= ' '/"PID"/{gsub(/;/,"");print $2; exit}')
case "$OLD_PID" in ''|*[!0-9]*) OLD_PID="" ;; esac

log "reload start old_pid=${OLD_PID:-none}"
say "reload start  old_pid=${OLD_PID:-none}"

# --- bootout ----------------------------------------------------------------
launchctl bootout "$DOMAIN/$LABEL" 2>>"$LOG"
log "bootout issued rc=$?"

# --- drain wait: tunggu proses lama benar-benar mati ------------------------
if [ -n "$OLD_PID" ] && [ "$OLD_PID" -gt 0 ]; then
  deadline=$(( $(date +%s) + BUDGET ))
  while kill -0 "$OLD_PID" 2>/dev/null; do
    if [ "$(date +%s)" -ge "$deadline" ]; then
      log "drain timeout ${BUDGET}s pid=$OLD_PID, bootstrap dipaksa"
      say "drain timeout ${BUDGET}s — bootstrap dipaksa"
      break
    fi
    sleep 1
  done
  log "drain selesai (pid=$OLD_PID masih hidup: $(kill -0 "$OLD_PID" 2>/dev/null && echo yes || echo no))"
fi
sleep 1

# --- bootstrap dengan retry --------------------------------------------------
deadline=$(( $(date +%s) + BUDGET ))
NEW_PID=""
while :; do
  if launchctl bootstrap "$DOMAIN" "$PLIST" 2>>"$LOG"; then
    sleep 1
    NEW_PID=$(launchctl list "$LABEL" 2>/dev/null \
      | awk -F'= ' '/"PID"/{gsub(/;/,"");print $2; exit}')
    case "$NEW_PID" in ''|*[!0-9]*) NEW_PID="" ;; esac
    [ -n "$NEW_PID" ] && [ "$NEW_PID" -gt 0 ] && { log "OK new_pid=$NEW_PID"; break; }
  fi
  if [ "$(date +%s)" -ge "$deadline" ]; then
    log "GAGAL bootstrap setelah ${BUDGET}s"
    say "GAGAL: bootstrap tidak berhasil setelah ${BUDGET}s — cek $LOG"
    exit 2
  fi
  sleep 2
done

say "OK  new_pid=$NEW_PID"

# --- verifikasi --------------------------------------------------------------
STATE=$(launchctl print "$DOMAIN/$LABEL" 2>/dev/null | awk -F'= ' '/state =/{print $2; exit}')
log "state=$STATE pid=$NEW_PID"
say "state=$STATE"
launchctl list | grep "$LABEL"
exit 0
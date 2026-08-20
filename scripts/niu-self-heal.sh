#!/usr/bin/env bash
# niu-self-heal.sh — Tindakan 1 dari matriks self-healing (laporan §3.2)
# Dipanggil probe, launchd, atau manusia. Idempotent. Tidak mematikan drift guard.
# Tidak auto-commit ecosystem-config. Tidak echo secret.
set -euo pipefail

NIU="${NIU:-/Users/zaryu/Desktop/Niumination}"
MC="${MC:-$NIU/services/niu-mission-control}"
JOB="${JOB:-c6ec80ed633f}"
MC_PORT="${NIU_MC_PORT:-5200}"
NINE_PORT="${NINE_PORT:-20128}"
OPS="$NIU/brain/ops"
ACTION="${1:-auto}"

mkdir -p "$OPS"
log() { printf '%s %s\n' "$(date '+%F %T')" "$*" | tee -a "$OPS/heal.log"; }

http_code() {
  curl -sS -o /dev/null -w '%{http_code}' -m "${2:-4}" "$1" 2>/dev/null || echo '000'
}

kick() {
  local label="$1"
  if launchctl kickstart -k "gui/${UID}/${label}" 2>/dev/null; then
    log "kickstart ${label}"
    return 0
  fi
  return 1
}

heal_mc() {
  local code
  code="$(http_code "http://127.0.0.1:${MC_PORT}/" 3)"
  if [[ "$code" != "000" ]]; then
    log "MC sudah hidup HTTP $code"
    return 0
  fi
  log "MC DOWN — heal"
  kick niu.missioncontrol || true
  sleep 2
  code="$(http_code "http://127.0.0.1:${MC_PORT}/" 3)"
  if [[ "$code" != "000" ]]; then
    log "MC pulih via launchd HTTP $code"
    return 0
  fi
  if [[ -f "$MC/server.py" ]] && ! pgrep -f 'niu-mission-control/server.py' >/dev/null 2>&1; then
    ( cd "$MC" && nohup python3 server.py >>"$OPS/mc.stdout.log" 2>>"$OPS/mc.stderr.log" & echo $! >"$OPS/mc.pid" )
    sleep 2
    code="$(http_code "http://127.0.0.1:${MC_PORT}/" 3)"
    log "MC start langsung HTTP $code pid=$(cat "$OPS/mc.pid" 2>/dev/null || echo '?')"
  fi
}

heal_nine() {
  local code
  code="$(http_code "http://127.0.0.1:${NINE_PORT}/v1/models" 3)"
  if [[ "$code" != "000" ]]; then
    log "9router sudah hidup HTTP $code"
    return 0
  fi
  log "9router DOWN — kickstart niu.ninerouter (jika plist terpasang)"
  kick niu.ninerouter || log "9router launchd belum terpasang — intervensi manusia"
}

heal_gateway() {
  if pgrep -f '[h]ermes' >/dev/null 2>&1; then
    log "gateway/hermes process terlihat"
    return 0
  fi
  log "gateway DOWN — kickstart"
  kick ai.hermes.gateway || kick hermes.gateway || log "gateway launchd belum diketahui — jalankan hermes gateway"
}

heal_jcode() {
  if [[ ! -d /Volumes/HermesAgent ]]; then
    log "USB tidak mounted — Jcode optional, skip"
    return 0
  fi
  mkdir -p /Volumes/HermesAgent/.cache/unix-home/.jcode/skills
  log "Jcode dir dipastikan"
}

heal_cron_pin() {
  if ! command -v hermes >/dev/null 2>&1; then
    log "hermes tidak di PATH — tidak bisa pin $JOB"
    return 0
  fi
  if hermes cron edit "$JOB" --provider opencode-zen --model nemotron-3-ultra-free; then
    log "pinned $JOB opencode-zen/nemotron-3-ultra-free"
  else
    log "gagal pin $JOB — lakukan manual"
  fi
  hermes config set cron.model nemotron-3-ultra-free >/dev/null 2>&1 || true
  hermes config set cron.model_provider opencode-zen >/dev/null 2>&1 || true
}

heal_ram() {
  # tidak membunuh Gateway/MC/9router — hanya noise
  log "RAM heal: tidak ada kill otomatis proses produksi. Tutup sandbox secara sadar."
}

case "$ACTION" in
  auto)
    heal_mc
    heal_nine
    heal_gateway
    heal_jcode
    ;;
  mc)       heal_mc ;;
  nine)     heal_nine ;;
  gateway)  heal_gateway ;;
  jcode)    heal_jcode ;;
  cron)     heal_cron_pin ;;
  ram)      heal_ram ;;
  *)
    echo "usage: $0 [auto|mc|nine|gateway|jcode|cron|ram]" >&2
    exit 2
    ;;
esac

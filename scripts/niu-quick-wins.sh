#!/usr/bin/env bash
# niu-quick-wins.sh — Langkah taktis < 1 jam untuk Niumination/Hermes
# Idempotent. Tidak mencetak nilai secret. Tidak menonaktifkan cron.model_drift_guard.
# Jalankan di MacBook zaryu:  bash scripts/niu-quick-wins.sh
set -euo pipefail

NIU="${NIU:-/Users/zaryu/Desktop/Niumination}"
MC="${MC:-$NIU/services/niu-mission-control}"
JOB="${JOB:-c6ec80ed633f}"
MC_PORT="${NIU_MC_PORT:-5200}"
NINE_PORT="${NINE_PORT:-20128}"

ok()   { printf '  [OK]  %s\n' "$*"; }
warn() { printf '  [!!]  %s\n' "$*" >&2; }
info() { printf '  [--]  %s\n' "$*"; }

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    warn "perintah '$1' tidak ada di PATH — langkah terkait dilewati"
    return 1
  fi
}

http_code() {
  local url="$1" timeout="${2:-5}"
  curl -sS -o /dev/null -w '%{http_code}' -m "$timeout" "$url" 2>/dev/null || echo '000'
}

echo "=== Niumination quick wins $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
echo "    NIU=$NIU"
echo

# ---------------------------------------------------------------------------
# 0. Preflight path
# ---------------------------------------------------------------------------
echo "== 0. Preflight =="
if [[ ! -d "$NIU" ]]; then
  warn "root ekosistem tidak ada: $NIU"
  warn "jalankan hanya di mesin zaryu, atau set NIU=..."
  exit 2
fi
ok "root ekosistem ada"

if [[ -d /Volumes/Niumination ]]; then
  warn "mount NTFS /Volumes/Niumination terdeteksi (READ-ONLY, nama jebakan)"
  warn "JANGAN tulis ke sini. Root sah: $NIU"
fi
if [[ -d /Volumes/HermesAgent ]]; then
  ok "USB HermesAgent mounted (cache opsional)"
else
  info "USB HermesAgent tidak mounted — Jcode/USB sync akan di-skip"
fi
echo

# ---------------------------------------------------------------------------
# 1. Mission Control :5200
# ---------------------------------------------------------------------------
echo "== 1. Mission Control :$MC_PORT =="
code="$(http_code "http://127.0.0.1:${MC_PORT}/" 3)"
if [[ "$code" != "000" && "$code" != "" ]]; then
  ok "sudah merespons HTTP $code"
else
  if [[ -f "$MC/server.py" ]]; then
    info "DOWN — mencoba start python3 server.py (foreground tidak, background)"
    if [[ ! -d "$NIU/brain/ops" ]]; then mkdir -p "$NIU/brain/ops"; fi
    if command -v python3 >/dev/null 2>&1; then
      ( cd "$MC" && nohup python3 server.py >>"$NIU/brain/ops/mc.stdout.log" 2>>"$NIU/brain/ops/mc.stderr.log" & echo $! >"$NIU/brain/ops/mc.pid" )
      sleep 2
      code="$(http_code "http://127.0.0.1:${MC_PORT}/" 3)"
      if [[ "$code" != "000" ]]; then
        ok "MC hidup setelah start, HTTP $code (pid $(cat "$NIU/brain/ops/mc.pid" 2>/dev/null || echo '?'))"
        info "ini NON-persistent. Pasang launchd: scripts/launchd/niu.missioncontrol.plist"
      else
        warn "MC masih DOWN setelah start. Cek $NIU/brain/ops/mc.stderr.log"
      fi
    else
      warn "python3 tidak ada"
    fi
  else
    warn "server.py tidak ditemukan di $MC"
  fi
fi
echo

# ---------------------------------------------------------------------------
# 2. Pin cron agent-reach-watch
# ---------------------------------------------------------------------------
echo "== 2. Pin cron $JOB =="
if need_cmd hermes; then
  info "edit pin provider=opencode-zen model=nemotron-3-ultra-free"
  if hermes cron edit "$JOB" --provider opencode-zen --model nemotron-3-ultra-free; then
    ok "cron $JOB di-pin"
  else
    warn "hermes cron edit gagal — coba dari dashboard atau cek job_id"
  fi
  hermes config set cron.model nemotron-3-ultra-free || warn "gagal set cron.model"
  hermes config set cron.model_provider opencode-zen || warn "gagal set cron.model_provider"
  info "drift guard HARUS tetap true (tidak disentuh)"
  info "trigger sadar:  hermes cron trigger $JOB"
else
  warn "lewati pin cron"
fi
echo

# ---------------------------------------------------------------------------
# 3. Fallback order (informational + perintah yang aman)
# ---------------------------------------------------------------------------
echo "== 3. Fallback chain =="
if need_cmd hermes; then
  info "daftar saat ini:"
  hermes fallback ls || true
  echo
  info "TARGET v2 — SATU kaki, keluarga yang sama:"
  info "  opencode-zen / hy3-free"
  info "HAPUS dari chain: juan-router, 9router/*, huancheng, gratislonggar"
  info "Hop lintas keluarga = merusak core. Setelah kaki Zen gagal: HALT + HANDOFF."
else
  warn "lewati fallback"
fi

nine_code="$(http_code "http://127.0.0.1:${NINE_PORT}/v1/models" 3)"
if [[ "$nine_code" == "200" || "$nine_code" == "401" ]]; then
  ok "9router :$NINE_PORT merespons HTTP $nine_code"
else
  warn "9router :$NINE_PORT tidak merespons ($nine_code) — SPOF thread Telegram"
fi
echo

# ---------------------------------------------------------------------------
# 4. Git hygiene (tidak auto-commit)
# ---------------------------------------------------------------------------
echo "== 4. Git hygiene (report only) =="
if [[ -d "$NIU/.git" ]]; then
  dirty="$(git -C "$NIU" status --porcelain || true)"
  if [[ -z "$dirty" ]]; then
    ok "ecosystem root clean"
  else
    warn "file dirty (TIDAK di-commit otomatis):"
    printf '%s\n' "$dirty" | sed 's/^/       /'
    info "jika bukan secret: git add -p && git commit -m 'chore(eco): snapshot hygiene 2026-08-18'"
    info "jika secret: pindahkan ke vault/ — jangan commit"
  fi
else
  info "$NIU bukan git root (mungkin ecosystem-config di subfolder) — cek manual"
fi
echo

# ---------------------------------------------------------------------------
# 5. Jcode target
# ---------------------------------------------------------------------------
echo "== 5. Jcode skill dir =="
JCODE="/Volumes/HermesAgent/.cache/unix-home/.jcode/skills"
if [[ -d /Volumes/HermesAgent ]]; then
  mkdir -p "$JCODE"
  ok "dipastikan ada: $JCODE"
else
  info "USB tidak mounted — Jcode bersifat optional, tidak dianggap P0"
fi
echo

# ---------------------------------------------------------------------------
# 6. Plugin policy (tidak mengubah config)
# ---------------------------------------------------------------------------
echo "== 6. Plugin policy =="
ok "rtk-rewrite        : TETAP enabled"
ok "niu-core-fence     : WAJIB enabled (pagar file beku + ganti model)"
ok "telegram_router    : JANGAN enable (Gateway Telegram sudah connected)"
ok "hermes-achievements: JANGAN enable"
ok "orca-status        : tunda"
echo

# ---------------------------------------------------------------------------
# 7. Deploy canary
# ---------------------------------------------------------------------------
echo "== 7. Deploy canary =="
canary() {
  local name="$1" url="$2"
  local out
  out="$(curl -sS -o /dev/null -w '%{http_code} %{time_total} %{redirect_url}' -m 10 "$url" 2>/dev/null || echo '000 10 TIMEOUT')"
  printf '  %-18s %s  %s\n' "$name" "$out" "$url"
}
canary "kune-ya"          "https://kune-ya.com"
canary "PemdiAcehTengah"  "https://pemdi-aceh-tengah.vercel.app"
canary "niu-dash"         "https://niumination.github.io/niu-dash/"
echo
info "kune-ya timeout / vermilion 307 = keputusan manusia, bukan auto-redeploy"
echo

echo "=== selesai. Lanjut: pasang launchd + niu-health-probe.py --loop ==="
echo "    JANGAN: hermes config set cron.model_drift_guard false"
echo "    JANGAN: docker compose up untuk MC di laptop 16 GB"

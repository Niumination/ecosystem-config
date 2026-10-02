#!/usr/bin/env bash
# =============================================================================
# build-services.sh — bekukan plist launchd sebagai template ke repo restore
# =============================================================================
# SISI BUILD. Plist nyata memuat /Users/zaryu; diganti {{HOME}} agar device
# dengan username berbeda tetap benar. Disimpan sebagai .template supaya jelas
# bahwa isinya belum siap-pakai (harus lewat install-macos.sh).
#
# Pemakaian: bash build-services.sh
# =============================================================================
set -Eeuo pipefail

# Nama env bertipe rahasia. Dipakai redact_plist di bawah.
SENSITIVE_NAME='^(CAMOFOX_[A-Z_]*KEY|[A-Z0-9_]*_API_KEY|[A-Z0-9_]*_ACCESS_KEY|[A-Z0-9_]*_ADMIN_KEY|[A-Z0-9_]*_TOKEN|[A-Z0-9_]*_SECRET|[A-Z0-9_]*_PASSWORD|[A-Z0-9_]*_PASSPHRASE)$'

# Tandai <key> yang sensitif, lalu ganti baris <string> berikutnya dengan
# __REDACTED__. Pakai awk, bukan sed: BRE tidak punya operator non-capturing,
# dan pola "key lalu值为 Sensitive" jadi kabur tanpa itu.
redact_plist() {
  awk -v pat="$SENSITIVE_NAME" '
    /<key>[^<]+<\/key>/ {
      name = $0
      sub(/^.*<key>/, "", name)
      sub(/<\/key>.*$/, "", name)
      sensitive = (name ~ pat)
      print
      next
    }
    sensitive && /<string>/ {
      print "        <string>__REDACTED__</string>"
      sensitive = 0
      next
    }
    { print }
  ' "$1"
}

REPO="$HOME/Desktop/Niumination/apps/niumination-restore"
OUT="$REPO/scripts/services/launchd"
mkdir -p "$OUT"

# Milik ekosistem/Hermes. Agen pihak ketiga (Google keystone) TIDAK diikutkan —
# itu dipasang ulang oleh aplikasinya sendiri.
AGENTS=(
  ai.hermes.gateway
  ai.hermes.gateway-marker
  ai.hermes.camofox
  com.9router.autostart
  com.niumination.9router-sync
  com.niu.missioncontrol
  com.niumination.missioncontrol
  com.niumination.nosleep
)

echo "== bekukan $(( ${#AGENTS[@]} )) plist → $OUT"
OK=0; MISS=0
: > "$OUT/../MANIFEST-services.txt"
for a in "${AGENTS[@]}"; do
  src="$HOME/Library/LaunchAgents/$a.plist"
  if [[ ! -f "$src" ]]; then
    echo "  ✗ tidak ada: $a.plist" >&2; MISS=$((MISS+1)); continue
  fi
  # SISI KREDENSIAL (2026-10-02): versi lama hanya `sed -e "s|$HOME|{{HOME}}|g"`,
  # yang menyalin plist apa adanya. ai.hermes.camofox.plist memuat
  # CAMOFOX_API_KEY / ACCESS_KEY / ADMIN_KEY, jadi tiap `sync-all.sh` menulis ulang
  # secret plaintext ke riwayat git repo niumination-restore. Aturan 1 repo DR
  # melarang plaintext; visibilitas private bukan alasan.
  # Nilai environment yang sensitif diganti `__REDACTED__`. Nama variabel, urutan,
  # dan nilai non-rahasia (port, PATH, flag) tetap utuh agar template berguna
  # sebagai dokumentasi. restore.sh belum memasang LaunchAgent sama sekali, jadi
  # placeholder ini belum diisi apa pun.
  redact_plist "$src" \
    | sed -e "s|$HOME|{{HOME}}|g" > "$OUT/$a.plist.template"
  if grep -qE '^[^<]*(KEY|TOKEN|SECRET|PASSWORD|PASSPHRASE)=[^<]{16,}' "$OUT/$a.plist.template" 2>/dev/null; then
    echo "  ✗ REDAKSI GAGAL untuk $a.plist — secret akan bocor ke repo" >&2
    exit 1
  fi
  net=""; grep -q 'NetworkState' "$src" && net=" [WaitNetwork]"
  printf "  ✓ %-36s %5s B%s\n" "$a.plist" "$(wc -c < "$OUT/$a.plist.template" | tr -d ' ')" "$net"
  printf "%s|%s|%s\n" "$a" "$(wc -c < "$OUT/$a.plist.template" | tr -d ' ')" "${net:-network-optional}" >> "$OUT/../MANIFEST-services.txt"
  OK=$((OK+1))
done
echo
echo "  dibekukan: $OK | tidak ditemukan: $MISS"
if [[ $MISS -gt 0 ]]; then
  echo "  PERINGATAN: agen yang tidak ada di mesin ini tidak ikut dipulihkan" >&2
fi
grep -c 'WaitNetwork' "$OUT/../MANIFEST-services.txt" | sed 's/^/  agen butuh jaringan (WaitNetwork): /'
echo "Catatan: agen pihak ketiga (Google keystone/updater) tidak diikutkan."

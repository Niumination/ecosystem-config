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
  sed -e "s|$HOME|{{HOME}}|g" "$src" > "$OUT/$a.plist.template"
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

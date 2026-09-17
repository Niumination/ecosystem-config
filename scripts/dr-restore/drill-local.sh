#!/usr/bin/env bash
# =============================================================================
# drill-local.sh — uji penuh TANPA jaringan (dipakai saat token/Release belum siap)
# =============================================================================
# Membuktikan: build L1 terenkripsi → klon repo → gabung+verifikasi+dekripsi →
# restore ke HOME KOSONG → verifikasi. Yang tidak diuji hanyalah pengunduhan dari
# GitHub (butuh token) — sisanya identik dengan drill.sh.
#
# Pemakaian: bash drill-local.sh
# =============================================================================
set -Eeuo pipefail

E="$HOME/Desktop/Niumination"
REPO="$E/apps/niumination-restore"
WORK="${WORK:-/tmp/dr-local-$(date +%H%M%S)}"
KEEP="$WORK/l1"
mkdir -p "$WORK/home" "$KEEP"
LOG="$WORK/drill-local.log"

PASS=$(security find-generic-password -s niumination-restore-dr -w) \
  || { echo "GAGAL: passphrase tidak ada di Keychain" >&2; exit 1; }
export PASS

# GH_TOKEN dibutuhkan restore.sh untuk mengklon repo ekosistem + dotfiles.
# Ambil dari .env (menimpa nilai warisan yang mungkin basi).
if [[ -f "$HOME/.hermes/.env" ]]; then set -a; . "$HOME/.hermes/.env"; set +a; fi
[[ -n "${GH_TOKEN:-}" ]] || { echo "GAGAL: GH_TOKEN tidak ada di ~/.hermes/.env" >&2; exit 1; }
export GH_TOKEN

{
echo "=========== DRILL LOKAL $(date '+%Y-%m-%d %H:%M:%S') ==========="
echo "work: $WORK"

echo "== 1. build L1 TERENKRIPSI (tanpa unggah) → $KEEP"
bash "$E/scripts/dr-restore/build-l1-release.sh" --no-upload --keep "$KEEP"
ls -1 "$KEEP" | sed 's/^/   /'

echo "== 2. klon repo restore (klon nyata dari working copy)"
git clone --quiet "$REPO" "$WORK/src"
echo "   HEAD: $(git -C "$WORK/src" rev-parse --short HEAD)"

echo "== 3. gabung pecahan + verifikasi SHA256 + dekripsi"
OUT="$WORK/src/l1-hermes"; mkdir -p "$OUT"
SORTED=$(printf '%s\n' "$KEEP"/hermes-backup.zip.enc.part-* | sort -t- -k2 -n)
: > "$OUT/hermes-backup.zip.enc"
while IFS= read -r p; do echo "   + $(basename "$p")"; cat "$p" >> "$OUT/hermes-backup.zip.enc"; done <<< "$SORTED"
# checksum diverifikasi pada BERKAS HASIL GABUNGAN (bukan di dir pecahan —
# SHA256SUMS menyebut hermes-backup.zip.enc yang hanya ada setelah digabung)
cp -f "$KEEP/SHA256SUMS" "$OUT/SHA256SUMS"
( cd "$OUT" && shasum -a 256 -c SHA256SUMS ) || { echo "GAGAL: checksum" >&2; exit 1; }
echo "   ✓ checksum cocok (hasil gabungan)"
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$OUT/hermes-backup.zip.enc" \
  -out "$OUT/hermes-backup.zip" -pass env:PASS || { echo "GAGAL: dekripsi" >&2; exit 1; }
unzip -l "$OUT/hermes-backup.zip" >/dev/null 2>&1 || { echo "GAGAL: bukan zip valid" >&2; exit 1; }
echo "   ✓ dekripsi → zip valid ($(du -h "$OUT/hermes-backup.zip" | cut -f1))"
rm -f "$OUT/hermes-backup.zip.enc"

echo "== 4. restore ke HOME KOSONG: $WORK/home"
( cd "$WORK/src" && bash restore.sh --source "$WORK/src" --target-home "$WORK/home" --apply )

echo "== 5. verifikasi ulang (independen dari restore.sh)"
( cd "$WORK/src" && HOME="$WORK/home" HERMES_HOME="$WORK/home/.hermes" \
    bash verify.sh --root "$WORK/home/Desktop/Niumination" )
} 2>&1 | tee "$LOG"

echo
echo "log: $LOG"

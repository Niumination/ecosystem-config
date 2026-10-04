#!/usr/bin/env bash
# Arsipkan ~/.hermes/.env + seluruh .env.bak-* ke vault terenkripsi.
#
# Latar (3 Okt 2026): 7 salinan plaintext ~/.hermes/.env/.env.bak-*ettle di
# ~/.hermes/ berisi seluruh kredensial ekosistem (Telegram, Vercel, 9router,
# Google, OpenCode, Composio, CamoFox, GH token). Izin file 600 melindungi dari
# user lain, tapi tidak dari seizure mesin, backup tak terenkripsi, atau sync
# awan yang salah konfigurasi. Kredensial yang hilang tanpa jejak juga jauh lebih
# sulit dipulihkan daripada yang bocor -- insiden 2 Okt membuktikan itu (butuh
# backup 28 Sep untuk mengembalikan 23 kunci).
#
# SKEMA SAMA dengan repo niumination-restore (restore.sh:248):
#   openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -pass env:PASS
# Passphrase dari Keychain `niumination-restore-dr`; tidak pernah dicetak.
#
# Dipakai:  bash scripts/archive-hermes-env.sh [--dry-run]
set -euo pipefail

H="$HOME/.hermes"
VAULT="$HOME/Desktop/Niumination/vault/_backup-credentials"
KCHAIN="niumination-restore-dr"
STAMP="$(date '+%Y%m%d-%H%M%S')"
OUT="$VAULT/hermes-env-archive-$STAMP.tar.gz.enc"
DRY=0
[[ "${1:-}" == "--dry-run" ]] && DRY=1

[[ -d "$VAULT" ]] || { echo "GAGAL: vault tidak ada: $VAULT" >&2; exit 1; }

# ── kumpulkan ────────────────────────────────────────────────────────────────
# Tanpa mapfile: macOS masih bash 3.2 (aturan 7 repo niumination-restore), dan
# skrip ini dijalankan dari cron non-interaktif di sana juga.
FILES=""
add() { case " $FILES " in *" $1 "*) ;; *) FILES="$FILES $1" ;; esac; }
[[ -f "$H/.env" ]] && add ".env"
for f in "$H"/.env.bak-*; do
  [[ -f "$f" ]] && add "$(basename "$f")"
done
[[ -n "$FILES" ]] || { echo "GAGAL: tidak ada .env / .env.bak-* untuk diarsipkan" >&2; exit 1; }
COUNT=$(printf '%s\n' $FILES | wc -l | tr -d ' ')

echo "Kandidat arsip ($COUNT berkas):"
printf '%s\n' $FILES | while read -r b; do
  f="$H/$b"
  printf '  %-46s %6s bytes  mode=%s  keys=%s\n' \
    "$b" "$(stat -f%z "$f")" "$(stat -f%Lp "$f")" \
    "$(grep -cE '^[A-Za-z_][A-Za-z0-9_]*=' "$f" || echo 0)"
done

if [[ $DRY -eq 1 ]]; then
  echo
  echo "DRY-RUN: tidak ada yang ditulis."
  echo "Akan menulis: $OUT"
  exit 0
fi

# ── passphrase dari Keychain ──────────────────────────────────────────────────
if ! command -v security >/dev/null; then
  echo "GAGAL: 'security' (Keychain CLI) tidak ada. Isi PASS secara manual." >&2
  exit 1
fi
if [[ -z "${PASS:-}" ]]; then
  PASS="$(security find-generic-password -s "$KCHAIN" -w 2>/dev/null)" \
    || { echo "GAGAL: passphrase tidak ada di Keychain (service=$KCHAIN)" >&2; exit 1; }
fi
[[ -n "$PASS" ]] || { echo "GAGAL: passphrase kosong" >&2; exit 1; }
export PASS

# ── tar → encrypt → verify → hapus salinan ───────────────────────────────────
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

tar -czf "$TMP/env.tar.gz" -C "$H" $(printf './%s ' $FILES)

openssl enc -aes-256-cbc -pbkdf2 -iter 200000 \
  -in "$TMP/env.tar.gz" -out "$OUT" -pass env:PASS 2>/dev/null \
  || { echo "GAGAL: enkripsi gagal" >&2; exit 1; }

# BUKTI: dekripsi ulang lalu bandingkan isi. "Berkas ada" != "berkas benar"
# (aturan 4 repo niumination-restore).
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 \
  -in "$OUT" -pass env:PASS -out "$TMP/verify.tar.gz" 2>/dev/null \
  || { echo "GAGAL: dekripsi ulang gagal (passphrase salah?)" >&2; exit 1; }

diff -q "$TMP/env.tar.gz" "$TMP/verify.tar.gz" >/dev/null \
  || { echo "GAGAL: hasil dekripsi tidak identik" >&2; exit 1; }

tar -tzf "$TMP/verify.tar.gz" | grep -q '^\./\.env$' \
  || { echo "GAGAL: .env tidak ada di dalam arsip" >&2; exit 1; }

chmod 600 "$OUT"
echo
echo "TERVERIFIKASI: dekripsi ulang cocok byte-per-byte."
echo "  arsip : $OUT ($(stat -f%z "$OUT") bytes, mode 600)"
echo "  isi   : $(tar -tzf "$TMP/verify.tar.gz" | tr '\n' ' ')"

# ── hapus salinan plaintext ──────────────────────────────────────────────────
# Hanya setelah verifikasi ciphertext. Salinan vault lama tetap dibiarkan --
#_until__-> ownershiptransfer selesai; lihat catatan di laporan.
echo
echo "Salinan plaintext di ~/.hermes TETAP dipertahankan (owner memutuskan berikut)."
echo "Hapus manual bila sudah yakin arsip + vault cukup."

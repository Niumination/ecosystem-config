#!/usr/bin/env bash
# =============================================================================
# drill.sh — bukti nyata: clone repo restore dari GitHub → pulihkan ke HOME kosong
# =============================================================================
# Drill ini SENGAJA memakai repo dari GitHub (bukan salinan lokal), dengan HOME
# yang benar-benar bersih. Inilah satu-satunya bukti yang sah bahwa restore
# berhasil — bukan pembacaan dokumen, bukan asumsi.
#
# Pemakaian: bash drill.sh [--keep]
#   --keep  jangan hapus HOME drill di akhir (untuk diperiksa manual)
# =============================================================================
set -Eeuo pipefail

KEEP=false
[[ "${1:-}" == "--keep" ]] && KEEP=true

REPO_SLUG="Niumination/niumination-restore"
WORK="${WORK:-/tmp/dr-drill-$(date +%H%M%S)}"
LOG="$WORK/drill.log"
mkdir -p "$WORK/home"

# --- token & passphrase -------------------------------------------------------
set -a; . "$HOME/.hermes/.env"; set +a
[[ -n "${GH_TOKEN:-}" ]] || { echo "GAGAL: GH_TOKEN tidak ada di ~/.hermes/.env" >&2; exit 1; }
PASS=$(security find-generic-password -s niumination-restore-dr -w) \
  || { echo "GAGAL: passphrase tidak ada di Keychain" >&2; exit 1; }
export PASS GH_TOKEN

echo "work   : $WORK"
echo "log    : $LOG"
echo "passphrase: [dari Keychain, tidak dicetak]"
echo

{
echo "==================== DRILL $(date '+%Y-%m-%d %H:%M:%S') ===================="
echo "== 1. clone repo restore DARI GITHUB (bukan salinan lokal)"
# device baru: coba gh+GH_TOKEN dulu (HTTPS). Bila token belum/bermasalah,
# jatuh ke SSH — tetapi pada device yang benar-benar kosong kunci SSH belum ada
# (kunci itu justru DI DALAM repo ini), sehingga jalur resminya tetap gh+token.
if ! gh repo clone "$REPO_SLUG" "$WORK/src" -- --quiet 2>/dev/null; then
  echo "   gh gagal (token?) — mencoba SSH…"
  rm -rf "$WORK/src"
  git clone --quiet "git@github.com:$REPO_SLUG.git" "$WORK/src" \
    || { echo "GAGAL: tidak bisa mengklon $REPO_SLUG (token maupun SSH)" >&2; exit 1; }
fi
HEAD=$(git -C "$WORK/src" rev-parse --short HEAD)
echo "   HEAD: $HEAD"

echo "== 2. unduh blob L1 dari aset Release"
( cd "$WORK/src" && bash scripts/fetch-release.sh --out l1-hermes )

echo "== 3. restore ke HOME KOSONG: $WORK/home"
( cd "$WORK/src" && bash restore.sh --source "$WORK/src" --target-home "$WORK/home" --apply )

echo "== 4. selesai restore"
} 2>&1 | tee "$LOG"

# exit code restore.sh diambil dari isi log (bukan dari tee)
if grep -qE '^GAGAL|^\[FATAL\]|gagal:' "$LOG"; then
  echo
  echo "DRILL: ada kegagalan — lihat $LOG" >&2
fi

echo
echo "===================== LANGKAH MANUAL YANG TERSISA ====================="
echo "(restore.sh tidak menjalankan verifikasi saat DRY-RUN; --apply sudah menjalankannya)"
echo "Untuk memeriksa ulang:"
echo "  HOME=$WORK/home HERMES_HOME=$WORK/home/.hermes bash $WORK/src/verify.sh --root $WORK/home/Desktop/Niumination"
echo
if $KEEP; then
  echo "HOME drill DIPERTAHANKAN (--keep): $WORK/home"
else
  echo "HOME drill disimpan sementara di $WORK/home (isi berkas rahasia — hapus bila tidak perlu)"
fi

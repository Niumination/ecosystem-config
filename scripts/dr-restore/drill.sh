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
# Klon WAJIB berbatas waktu: git di jaringan ini bisa MENGGANTUNG tanpa error
# (terukur 0 KB dalam 30 detik sementara prosesnya masih hidup).
CLONE_LOG="$WORK/clone.log"
to() { local l="$1"; shift
  if command -v timeout >/dev/null 2>&1; then timeout "$l" "$@"; return $?; fi
  "$@" & local p=$!
  ( sleep "$l"; kill -TERM "$p" 2>/dev/null; sleep 5; kill -9 "$p" 2>/dev/null ) >/dev/null 2>&1 &
  local w=$!; wait "$p"; local r=$?; kill "$w" 2>/dev/null; return $r
}
clone_ok=0
for coba in 1 2; do
  rm -rf "$WORK/src"
  if to 180 gh repo clone "$REPO_SLUG" "$WORK/src" -- --depth 1 >>"$CLONE_LOG" 2>&1; then clone_ok=1; break; fi
  echo "   percobaan $coba gagal/timeout (180s) — ulangi"
done
if [ "$clone_ok" -ne 1 ]; then
  echo "   jalur gh gagal — mencoba SSH…"
  rm -rf "$WORK/src"
  if to 180 git clone --depth 1 "git@github.com:$REPO_SLUG.git" "$WORK/src" >>"$CLONE_LOG" 2>&1; then clone_ok=1; fi
fi
if [ "$clone_ok" -ne 1 ]; then
  rm -rf "$WORK/src"
  echo "   semua jalur git gagal — fallback tarball API (tanpa git)"
  if to 300 gh api "repos/$REPO_SLUG/tarball/main" >"$WORK/src.tar.gz" 2>>"$CLONE_LOG" \
     && [ -s "$WORK/src.tar.gz" ] \
     && mkdir -p "$WORK/src" \
     && tar -xzf "$WORK/src.tar.gz" -C "$WORK/src" --strip-components=1 >>"$CLONE_LOG" 2>&1; then
    rm -f "$WORK/src.tar.gz"; clone_ok=1
  fi
fi
if [ "$clone_ok" -ne 1 ]; then
  echo "   --- 3 baris terakhir log klon ---" >&2
  tail -3 "$CLONE_LOG" 2>/dev/null | sed 's/^/      /' >&2
  echo "GAGAL: tidak bisa mengklon $REPO_SLUG (gh, HTTPS, SSH, tarball)" >&2; exit 1
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

#!/usr/bin/env bash
# =============================================================================
# build-l1-release.sh — bekukan Hermes home (L1) & unggah sebagai aset Release
# =============================================================================
# SISI BUILD. `hermes backup` menghasilkan ~203 MB; setelah membuang berkas yang
# bisa dibangun ulang (bin/lsp/cache/logs/...) menjadi ~116 MB. Itu di atas batas
# 100 MB/berkas GitHub, jadi dipecah dan diunggah sebagai aset Release.
#
# PELAJARAN WAJIB (pernah terjadi): `gh release create` TANPA `--repo` jatuh ke
# repo dari cwd → release uji nyasar ke repo PUBLIK. Semua perintah gh di sini
# memakai --repo EKSPLISIT.
#
# Pemakaian: bash build-l1-release.sh [--no-upload]
# =============================================================================
set -Eeuo pipefail

REPO="Niumination/niumination-restore"
TAG="l1-$(date +%Y-%m-%d)"
SIZE="45m"          # di bawah batas 100 MB/berkas, menyisakan ruang aman
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
UPLOAD=true
[[ "${1:-}" == "--no-upload" ]] && UPLOAD=false

# GH_TOKEN: proses non-interaktif TIDAK bisa membaca Keychain macOS, dan
# lingkungan bisa membawa GH_TOKEN warisan yang sudah basi. Karena itu SELALU
# ambil dari ~/.hermes/.env (menimpanya), bukan "hanya bila kosong".
if [[ -f "$HOME/.hermes/.env" ]]; then
  set -a; . "$HOME/.hermes/.env"; set +a
  echo "== GH_TOKEN diambil dari ~/.hermes/.env (menimpa nilai warisan)"
fi
[[ -n "${GH_TOKEN:-}" ]] || { echo "GAGAL: GH_TOKEN tidak tersedia" >&2; exit 1; }
if ! _err=$(gh api user 2>&1 >/dev/null); then
  echo "GAGAL: GH_TOKEN tidak valid — pesan gh: $(printf '%s' "$_err" | head -2 | tr '\n' ' ')" >&2
  exit 1
fi

echo "== 1. hermes backup"
command -v hermes >/dev/null || { echo "GAGAL: hermes tidak ada di PATH" >&2; exit 1; }
hermes backup -o "$TMP/hermes-backup.zip" >/dev/null 2>&1 || { echo "GAGAL: hermes backup gagal" >&2; exit 1; }
echo "   mentah: $(du -h "$TMP/hermes-backup.zip" | cut -f1)"

echo "== 2. buang berkas yang BISA dibangun ulang (bukan data hilang)"
BEFORE=$(du -k "$TMP/hermes-backup.zip" | cut -f1)
# catatan: pola disengaja menyasar direktori tingkat-atas di dalam zip
zip -q -d "$TMP/hermes-backup.zip" \
  'bin/*' 'lsp/*' 'cache/*' 'logs/*' 'checkpoints/*' 'firefox-profile-backup/*' \
  'models_dev_cache.json' '*/models_dev_cache.json' '.DS_Store' '*/.DS_Store' \
  >/dev/null 2>&1 || true
AFTER=$(du -k "$TMP/hermes-backup.zip" | cut -f1)
echo "   $((BEFORE/1024)) MB → $((AFTER/1024)) MB (dibuang $(( (BEFORE-AFTER)/1024 )) MB regenerable)"

echo "== 3. periksa isi penting masih ada"
# Catatan: JANGAN `unzip -l | grep -q` — grep -q keluar pada kecocokan pertama,
# unzip kena SIGPIPE, dan `pipefail` membuat pipeline dianggap GAGAL padahal
# cocok (menghasilkan laporan "HILANG" palsu). Simpan daftar isi dulu.
ZLIST=$(mktemp)
unzip -l "$TMP/hermes-backup.zip" > "$ZLIST" 2>/dev/null || { echo "GAGAL: tidak bisa membaca zip" >&2; exit 1; }
for must in 'config.yaml' '.env' 'auth.json' 'state.db' 'sessions/' 'skills/' 'memories/'; do
  if grep -qF "$must" "$ZLIST"; then
    echo "   ✓ $must"
  else
    echo "   ✗ $must HILANG — batal unggah" >&2; rm -f "$ZLIST"; exit 1
  fi
done
echo "   jumlah entri: $(grep -cE ' +[0-9]+ +[0-9-]+' "$ZLIST" || true)"
rm -f "$ZLIST"

echo "== 4. pecah & checksum"
( cd "$TMP" && split -b "$SIZE" -d -a 2 hermes-backup.zip hermes-backup.zip.part- )
( cd "$TMP" && shasum -a 256 hermes-backup.zip > SHA256SUMS )
ls -1 "$TMP" | grep -c 'part-' | sed 's/^/   bagian: /'
echo "   sha256(zip gabungan): $(cut -c1-16 < "$TMP/SHA256SUMS")…"

if ! $UPLOAD; then
  echo; echo "(--no-upload) berkas siap di: $TMP"; ls -lh "$TMP" | tail -n +2; exit 0
fi

echo "== 5. unggah ke Release (target EKSPLISIT: $REPO@$TAG)"
if gh release view "$TAG" --repo "$REPO" >/dev/null 2>&1; then
  echo "   Release $TAG sudah ada — aset ditimpa (--clobber)"
  gh release upload "$TAG" --repo "$REPO" --clobber "$TMP"/hermes-backup.zip.part-* "$TMP/SHA256SUMS" >/dev/null
else
  gh release create "$TAG" --repo "$REPO" \
    --title "L1 — Hermes home + sesi ($TAG)" \
    --notes "Snapshot Hermes home tanpa berkas yang bisa dibangun ulang.

Isi: config.yaml, .env, auth.json, state.db + seluruh sesi, skills/, cron/, memories/, kanban.db, plugins/.
Dibuang: bin/, lsp/, cache/, logs/, checkpoints/, firefox-profile-backup/ (regenerable).

Unduh + gabung: bash scripts/fetch-release.sh --out l1-hermes --tag $TAG" \
    "$TMP"/hermes-backup.zip.part-* "$TMP/SHA256SUMS" >/dev/null
fi

echo "== 6. verifikasi aset benar-benar ada di GitHub"
gh release view "$TAG" --repo "$REPO" --json assets \
  --jq '.assets[] | "   \(.name)  \(.size) B"' | sort

echo
echo "Selesai: $REPO@$TAG"

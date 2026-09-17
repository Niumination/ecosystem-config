#!/usr/bin/env bash
# =============================================================================
# make-integrity.sh — bangun integrity.sha256 untuk repo niumination-restore
# =============================================================================
# Sisi BUILD dari pola autoskills #1.
#
# Format tiap baris:  <blob_sha256>  <norm_sha256>  <path>
#   blob : sha256 isi berkas DI DALAM GIT (git cat-file blob HEAD:path)
#   norm : sha256 berkas di disk dengan CR dibuang (fallback bila tidak ada git)
#
# KENAPA blob, bukan berkas di disk: `.gitattributes` (mis. `*.ps1 text
# eol=crlf`) membuat checkout memakai baris akhir berbeda dari blob-nya, jadi
# hash berkas-di-disk TIDAK sama antara mesin build dan hasil clone bersih —
# manifest seperti itu akan menuduh salinan yang sehat sebagai rusak. Hash blob
# tidak terpengaruh atribut/EOL/platform.
# =============================================================================
set -Eeuo pipefail

R="${1:-$HOME/Desktop/Niumination/apps/niumination-restore}"
cd "$R" || { echo "GAGAL: tidak bisa masuk $R" >&2; exit 1; }
git rev-parse --git-dir >/dev/null 2>&1 || { echo "GAGAL: $R bukan repo git" >&2; exit 1; }

if command -v shasum >/dev/null 2>&1; then
  h_stdin() { shasum -a 256 | cut -d' ' -f1; }
elif command -v sha256sum >/dev/null 2>&1; then
  h_stdin() { sha256sum | cut -d' ' -f1; }
else
  echo "GAGAL: butuh shasum atau sha256sum" >&2; exit 1
fi

tmp="$(mktemp)"
git ls-files -z | while IFS= read -r -d '' f; do
  [ "$f" = "integrity.sha256" ] && continue

  # Ambil dari INDEX (`:path`) dulu — saat sync-all.sh memanggil ini, berkas
  # sudah di-`git add` tapi belum ter-commit; index = isi yang akan dikirim.
  bh="-"
  if git rev-parse --verify --quiet ":$f" >/dev/null 2>&1; then
    bh="$(git cat-file blob ":$f" | h_stdin)"
  elif git rev-parse --verify --quiet "HEAD:$f" >/dev/null 2>&1; then
    bh="$(git cat-file blob "HEAD:$f" | h_stdin)"
  fi

  if [ -f "$f" ]; then
    nh="$(tr -d '\r' < "$f" | h_stdin)"
  else
    nh="-"
  fi

  printf '%s  %s  %s\n' "$bh" "$nh" "$f"
done | LC_ALL=C sort -k3 > "$tmp"

mv "$tmp" integrity.sha256
echo "   integrity.sha256: $(wc -l < integrity.sha256 | tr -d ' ') berkas (hash blob + norm)"

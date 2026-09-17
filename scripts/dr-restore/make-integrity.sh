#!/usr/bin/env bash
# =============================================================================
# make-integrity.sh — bangun integrity.sha256 untuk repo niumination-restore
# =============================================================================
# Sisi BUILD dari pola autoskills #1: menghasilkan manifest SHA-256 semua berkas
# TERLACAK di repo restore (kecuali manifest itu sendiri), memakai format
# `shasum`/`sha256sum` standar sehingga bisa diverifikasi di OS mana pun.
#
# Dijalankan otomatis oleh sync-all.sh sebelum commit, jadi manifest selalu
# sejalan dengan berkas yang benar-benar di-push.
# =============================================================================
set -Eeuo pipefail

R="${1:-$HOME/Desktop/Niumination/apps/niumination-restore}"
cd "$R" || { echo "GAGAL: tidak bisa masuk $R" >&2; exit 1; }
git rev-parse --git-dir >/dev/null 2>&1 || { echo "GAGAL: $R bukan repo git" >&2; exit 1; }

if command -v shasum >/dev/null 2>&1; then
  hash_of() { shasum -a 256 "$1" | cut -d' ' -f1; }
elif command -v sha256sum >/dev/null 2>&1; then
  hash_of() { sha256sum "$1" | cut -d' ' -f1; }
else
  echo "GAGAL: butuh shasum atau sha256sum" >&2; exit 1
fi

tmp="$(mktemp)"
git ls-files -z | while IFS= read -r -d '' f; do
  [ "$f" = "integrity.sha256" ] && continue
  [ -f "$f" ] || continue
  printf '%s  %s\n' "$(hash_of "$f")" "$f"
done | LC_ALL=C sort -k2 > "$tmp"

mv "$tmp" integrity.sha256
echo "   integrity.sha256: $(wc -l < integrity.sha256 | tr -d ' ') berkas ter-hash"

#!/usr/bin/env bash
# =============================================================================
# build-l2.sh — bekukan berkas ekosistem yang TIDAK ada di git (L2) ke repo restore
# =============================================================================
# SISI BUILD. Berkas-berkas ini tidak bisa dibangun ulang (kunci signing, dataset,
# kredensial proyek) dan tidak ada di GitHub — kalau hilang, hilang permanen.
#
# Alur:
#   1. kumpulkan kandidat (pola eksplisit) dari ekosistem
#   2. staging: /Users/zaryu → {{HOME}}  (agar device dengan username beda tetap benar)
#   3. tar + kompresi + enkripsi (passphrase dari Keychain)
#   4. GENERATE allowlist substitusi: berkas L2 ber-placeholder + berkas git
#      ekosistem yang memuat path absolut
#
# Pemakaian: bash build-l2.sh [--no-encrypt]
# =============================================================================
set -Eeuo pipefail

E="$HOME/Desktop/Niumination"
REPO="$E/apps/niumination-restore"
KC_SERVICE="niumination-restore-dr"
OLD_HOME="$HOME"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
NO_ENC=false
[[ "${1:-}" == "--no-encrypt" ]] && NO_ENC=true

command -v zstd >/dev/null || { echo "GAGAL: zstd tidak ada" >&2; exit 1; }
[[ -d "$REPO" ]] || { echo "GAGAL: repo tidak ada: $REPO" >&2; exit 1; }

echo "== 1. kumpulkan kandidat L2"
STAGE="$TMP/stage"; mkdir -p "$STAGE"
LIST="$TMP/kandidat.txt"; : > "$LIST"

# pola: kunci signing, .env proyek, .vercel, DB state, dataset mentah, vault
find "$E" \
  \( -path '*/node_modules/*' -o -path '*/.git/*' -o -path '*/.next/*' \
     -o -path '*/dist/*' -o -path '*/build/*' -o -path '*/.venv/*' -o -path '*/venv/*' \
     -o -path '*/vendor/*' -o -path '*/Pods/*' -o -path '*/coverage/*' \
     -o -path '*/__pycache__/*' -o -path "$REPO/*" -o -path '*/sandbox/*' \
     -o -path '*/archive/*' -o -path '*/inactive-2026-09/*' \) -prune -o \
  -type f \
  \( -path '*/play-store/signing/*' \
     -o -name '.env' -o -name '.env.local' -o -name '.env.production' \
     -o -name '.env.development' -o -name '.env.prod' \
     -o -path '*/.vercel/*' \
     -o -path '*/dtsen-raw/*' \
     -o -path "$E/vault/*" \
     -o -path '*/niu-mission-control/data/*' \
     -o -path '*/niu-dash-fullstack/data/projects.json' \
     -o -path '*/mata/config.json' \
     -o -name 'swarm_state.db' -o -name 'dev.db' \
  \) -print 2>/dev/null \
  | grep -v -e '\.DS_Store$' -e '\.env\.example$' -e '\.log$' -e '\.pyc$' \
  > "$LIST" || true

N=$(wc -l < "$LIST" | tr -d ' ')
[[ "$N" -gt 0 ]] || { echo "GAGAL: tidak ada kandidat — pola perlu diperiksa" >&2; exit 1; }
echo "   kandidat: $N berkas"

echo "== 2. staging + ubah /Users/$USER → {{HOME}} (berkas teks saja)"
L2ALLOW="$TMP/l2-allow.txt"; : > "$L2ALLOW"
BIN=0; TXT=0; REW=0
while IFS= read -r src; do
  rel="${src#$E/}"
  dst="$STAGE/$rel"
  mkdir -p "$(dirname "$dst")"
  cp -p "$src" "$dst"
  mt=$(file -b --mime-type "$src" 2>/dev/null || echo application/octet-stream)
  case "$mt" in
    text/*|application/json|application/xml|application/javascript)
      TXT=$((TXT+1))
      if grep -q -F "$OLD_HOME" "$dst" 2>/dev/null; then
        sed -e "s|$OLD_HOME|{{HOME}}|g" "$dst" > "$dst.rw" && cat "$dst.rw" > "$dst" && rm -f "$dst.rw"
        REW=$((REW+1)); echo "$rel" >> "$L2ALLOW"
      fi ;;
    *) BIN=$((BIN+1)) ;;
  esac
done < "$LIST"
echo "   teks: $TXT (diubah: $REW) | biner: $BIN"

echo "== 3. tar + zstd"
RAW="$TMP/ecosystem-ignored.tar"
tar -cf "$RAW" -C "$STAGE" . 2>/dev/null
zstd -19 -q -f "$RAW" -o "$RAW.zst"
echo "   tar: $(du -h "$RAW" | cut -f1) → zst: $(du -h "$RAW.zst" | cut -f1)"

echo "== 4. enkripsi + simpan ke repo"
OUT="$REPO/l2-data"; mkdir -p "$OUT"
if $NO_ENC; then
  cp "$RAW.zst" "$OUT/ecosystem-ignored.tar.zst"
  echo "   (tanpa enkripsi — HANYA untuk uji, JANGAN commit)"
else
  DR_PASS=$(security find-generic-password -s "$KC_SERVICE" -w)
  export DR_PASS
  openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt \
    -in "$RAW.zst" -out "$OUT/ecosystem-ignored.tar.zst.enc" -pass env:DR_PASS
  # bukti: dekripsi balik dan bandingkan hash
  h1=$(shasum -a 256 "$RAW.zst" | cut -d' ' -f1)
  h2=$(openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$OUT/ecosystem-ignored.tar.zst.enc" \
        -pass env:DR_PASS 2>/dev/null | shasum -a 256 | cut -d' ' -f1)
  [[ "$h1" == "$h2" ]] || { echo "GAGAL: hash dekripsi tidak cocok" >&2; exit 1; }
  echo "   ✓ $(du -h "$OUT/ecosystem-ignored.tar.zst.enc" | cut -f1) terenkripsi, hash roundtrip cocok"
fi

echo "== 5. generate allowlist (L2 + berkas git yang memuat path absolut)"
ECOLIST="$TMP/eco-allow.txt"; : > "$ECOLIST"
for repo in "$E" "$E/dotfiles/zaryu-terminal-dotfiles"; do
  [[ -d "$repo/.git" ]] || continue
  git -C "$repo" ls-files -z 2>/dev/null | while IFS= read -r -d '' f; do
    full="$repo/$f"; [[ -f "$full" ]] || continue
    case "$f" in *node_modules/*|*.lock|package-lock.json) continue ;; esac
    mt=$(file -b --mime-type "$full" 2>/dev/null || echo application/octet-stream)
    case "$mt" in text/*|application/json|application/javascript|application/xml) ;; *) continue ;; esac
    if grep -q -F "$OLD_HOME" "$full" 2>/dev/null; then
      if [[ "$repo" == "$E" ]]; then echo "$f" >> "$ECOLIST"; else echo "dotfiles/zaryu-terminal-dotfiles/$f" >> "$ECOLIST"; fi
    fi
  done
done
cat "$L2ALLOW" "$ECOLIST" | sort -u | grep -v '^$' > "$REPO/scripts/allowlist-paths.txt"
echo "$OLD_HOME" > "$REPO/scripts/old-home.txt"
echo "   allowlist: $(wc -l < "$REPO/scripts/allowlist-paths.txt" | tr -d ' ') entri (L2: $(wc -l < "$L2ALLOW" | tr -d ' '), git: $(wc -l < "$ECOLIST" | tr -d ' '))"
echo "   old-home : $(cat "$REPO/scripts/old-home.txt")"

echo
echo "Selesai. Blob L2: $OUT/ecosystem-ignored.tar.zst.enc"

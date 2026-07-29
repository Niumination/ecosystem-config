#!/usr/bin/env bash
# =============================================================================
# cleanup-modul-images.sh — Bersihkan duplikasi gambar modul indikator
# =============================================================================
# Masalah: Hermes membuat duplikasi ~500MB gambar PNG ke public/docs/ dan
# docs/modul-indikator-clean/. Gambar asli ada di docs/modul-indikator/.
#
# Yang dilakukan script ini:
# 1. Hapus public/docs/ (500MB — duplikasi di folder publik, bikin Vercel berat)
# 2. Hapus docs/modul-indikator-clean/ (500MB — duplikasi)
# 3. Opsional: kompres gambar PNG di docs/modul-indikator/ ke WebP
# =============================================================================

set -euo pipefail

BASE="/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo ""
echo "🧹 Pembersihan Duplikasi Gambar Modul Indikator"
echo "════════════════════════════════════════════════"
echo ""

# ── Step 1: Hapus public/docs (500MB — Hermes' duplicate) ──
if [ -d "$BASE/public/docs" ]; then
  SIZE=$(du -sh "$BASE/public/docs" 2>/dev/null | cut -f1)
  echo -e "${YELLOW}⚠️  public/docs/ ($SIZE) — duplikasi di folder publik${NC}"
  echo -n "Hapus? [y/N] "
  read -r confirm
  if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    rm -rf "$BASE/public/docs"
    echo -e "${GREEN}✅ public/docs/ dihapus${NC}"
  else
    echo "⏭️  Dilewati"
  fi
else
  echo -e "${GREEN}✅ public/docs/ sudah tidak ada${NC}"
fi

# ── Step 2: Hapus docs/modul-indikator-clean (500MB — Hermes' duplicate) ──
if [ -d "$BASE/docs/modul-indikator-clean" ]; then
  SIZE=$(du -sh "$BASE/docs/modul-indikator-clean" 2>/dev/null | cut -f1)
  echo -e "${YELLOW}⚠️  docs/modul-indikator-clean/ ($SIZE) — duplikasi${NC}"
  echo -n "Hapus? [y/N] "
  read -r confirm
  if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    rm -rf "$BASE/docs/modul-indikator-clean"
    echo -e "${GREEN}✅ docs/modul-indikator-clean/ dihapus${NC}"
  else
    echo "⏭️  Dilewati"
  fi
else
  echo -e "${GREEN}✅ docs/modul-indikator-clean/ sudah tidak ada${NC}"
fi

# ── Step 3: Kompres gambar di docs/modul-indikator ke WebP ──
if [ -d "$BASE/docs/modul-indikator" ]; then
  PNG_COUNT=$(find "$BASE/docs/modul-indikator" -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
  echo -e "\n${YELLOW}📷 $PNG_COUNT file PNG di docs/modul-indikator/ — kompres ke WebP?${NC}"
  echo "Catatan: halaman modul-indikator sudah tidak pakai gambar."
  echo "         File ini sebagai referensi offline saja."
  echo -n "Kompres PNG → WebP (lossy 80%)? [y/N] "
  read -r compress
  if [ "$compress" = "y" ] || [ "$compress" = "Y" ]; then
    which cwebp >/dev/null 2>&1 || {
      echo "❌ cwebp tidak terinstall. Install: brew install webp"
      exit 1
    }
    echo "⏳ Mengompres gambar..."
    TOTAL_SAVED=0
    find "$BASE/docs/modul-indikator" -name "*.png" -print0 | while IFS= read -r -d '' png; do
      webp="${png%.png}.webp"
      if [ ! -f "$webp" ]; then
        ORIG_SIZE=$(stat -f%z "$png" 2>/dev/null || stat -c%s "$png" 2>/dev/null)
        cwebp -quiet -q 80 "$png" -o "$webp" 2>/dev/null || true
        if [ -f "$webp" ]; then
          NEW_SIZE=$(stat -f%z "$webp" 2>/dev/null || stat -c%s "$webp" 2>/dev/null)
          SAVED=$((ORIG_SIZE - NEW_SIZE))
          TOTAL_SAVED=$((TOTAL_SAVED + SAVED))
        fi
      fi
    done
    echo -e "${GREEN}✅ Kompresi selesai. Hemat ~${TOTAL_SAVED} bytes${NC}"
    echo "   Hapus PNG asli setelah verifikasi?"
    echo -n "   Hapus PNG asli? [y/N] "
    read -r delete_png
    if [ "$delete_png" = "y" ] || [ "$delete_png" = "Y" ]; then
      find "$BASE/docs/modul-indikator" -name "*.png" -delete
      echo -e "${GREEN}✅ PNG asli dihapus${NC}"
    fi
  else
    echo "⏭️  Kompresi dilewati"
  fi
fi

echo ""
echo -e "${GREEN}✅ Selesai!${NC}"
echo "   Jalankan 'git status' untuk lihat perubahan."
echo "   Pastikan halaman modul-indikator tetap berfungsi."

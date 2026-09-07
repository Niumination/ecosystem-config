# Free-Tier Reels Workflow — Condensed Guide

> Condensed knowledge bank for the `free-tier-reels` skill class.
> Session-specific detail, verification steps, and provider quirks.

## 📋 Quick Export Checklist

- [ ] HTML scaffold di `~/Downloads/ide-reels-html/index.html`
- [ ] `npm install hyperframes@latest` sukses
- [ ] `npx hyperframes render` selesai tanpa error
- [ ] File `ide5-reels-final.mp4` ada di `~/Downloads/ide-reels-html/`
- [ ] Aspect ratio 9:16 (1080×1920) terverifikasi
- [ ] Durasi 15-60 detik terverifikasi
- [ ] Watermark "Built with Niumination" ada di video
- [ ] Caption siap-copy dari guide ini
- [ ] Hashtag `#Niumination #AITools #Gratis #Reels #contentcreator` ditambahkan
- [ ] Tracking di `BACKLOG.md` dan `docs/reports/` setelah posting

## ⚠️ PITFALL: Common Failures & Fixes

| Masalah | Penyebab | Solusi |
|---------|----------|--------|
| `npm: command not found` | Node.js belum terinstall | `brew install node` lalu coba lagi |
| `ffmpeg: command not found` | FFmpeg belum terinstall | `brew install ffmpeg` lalu coba lagi |
| `npx: not found` | HyperFrames belum terinstall | `npm install hyperframes@latest` lalu coba lagi |
| Video terlalu pendek (5 detik) | `--duration` salah di command | Ganti dengan `--duration 60` (untuk 60 detik total) |
| Video resolusi salah | `--width`/`--height` salah | Gunakan `--width 1080 --height 1920` (9:16) |
| Watermark tidak muncul | HTML tidak mengandung element `.watermark` | Pastikan HTML mengandalkan CSS `.watermark` class |
| MP4 tidak bisa di-upload Instagram | Format tidak didukung | Pastikan output MP4, bukan WebM atau format lain |
| Caption terpotong di Instagram | Terlalu panjang | Potong manual di Instagram setelah upload, atau kurangi panjang |

## ✅ VERIFIKASI SETELAH RENDER

Setelah `npx hyperframes render` selesai, jalankan:

```bash
# 1. Cek file ada tidak
ls -la ~/Downloads/ide-reels-html/ide5-reels-final.mp4

# 2. Cek durasi & resolusi (butuh ffprobe)
ffprobe -v quiet -show_format -show_streams ~/Downloads/ide-reels-html/ide5-reels-final.mp4 2>/dev/null | grep -E "duration|width|height"

# 3. Cek aspect ratio manual
# Jika width < height → 9:16 ✅
# Jika width > height → 16:9 ❌ (ubah command)

# 4. Cek watermark visual (lihat video)
# - Cari teks "Built with Niumination" di video
# - Harus muncul di pojok kanan bawah (3 detik terakhir)

# 5. Upload test ke Instagram (draft saja)
# - Pastikan 9:16 ratio diterima
# - Cek preview sebelum publish
```

## 📞 TROUBLESHOOTING LANJUT

**Jika `npx hyperframes render` error:**

1. **Pastikan di folder yang benar:**
   ```bash
   cd ~/Downloads/ide-reels-html
   ```

2. **Cek versi Node.js:**
   ```bash
   node --version  # Harus ≥22
   npm --version
   ```

3. **Cek FFmpeg:**
   ```bash
   ffmpeg -version 2>&1 | head -1
   # Jika error, install: brew install ffmpeg
   ```

4. **Cek permission write:**
   ```bash
   ls -la ~/Downloads/ide-reels-html/
   # Harus punya write permission di folder tujuan
   ```

5. **Alternatif jika terus error:**
   - Pakai CapCut di handphone (user preference Afrizal)
   - Manual record screen Reels dari desktop
   - Gunakan FLUX 3 text-to-video via Nous subscription (jika ada API key)

## 📝 CATATAN PER-TOOL

### Ghost Humanizer
- **Input:** Teks AI robot
- **Output:** Teks jadi alami
- **Verifikasi:** Baca output di voice-over, pastikan nada bahasa Indonesia alami

### HyperFrames
- **Input:** `index.html` di folder kerja
- **Output:** `ide5-reels-final.mp4`
- **Verifikasi:** Lihat checklist di atas

### Baoyu Infographic
- **Input:** Data CSV/JSON tentang 68 skill Niumination
- **Output:** Desain carousel untuk Reels karousel
- **Verifikasi:** Desain keren, informasi lengkap 68 skill

### Manim Video
- **Input:** Scene Python dengan teks animasi
- **Output:** File video animasi
- **Verifikasi:** Animasi smooth, teks terbaca, durasi 10-15 detik

---

*File ini tergenerate otomatis dari skill `free-tier-reels` class di Niumination skill bank. Diperbarui setiap bulan untuk mencerminkan perubahan tooling & free-tier limits.*
---
name: free-tier-reels
description: "Free-tier Reels creation workflow."
version: 1.0.0
author: Afrizal Munthe (Niumination)
tags: [creative, video, reels, instagram, free-tier]
platforms: [macos, linux, mobile]
---
# Free-Tier Reels Creation Workflow

**Trigger:** Create Instagram Reels using entirely free tools from Niumination ecosystem.

**Purpose:** Provide complete workflow for Instagram Reels (9:16, 15-60s) using only free tools. No paid subscriptions.

## 🛠 Available Free Tools (Class Overview)

This skill class covers these free-tier tools from the Niumination ecosystem:

1. **Ghost** - AI text humanizer for scripts
2. **HyperFrames** - HTML to MP4 video renderer
3. **Baoyu Infographic** - Carousel/infographic generator
4. **Manim Video** - Animation/explainer video generator
5. **Canva** (free tier) - Design and video editing
6. **Meta Business Suite** - Free social media management
7. **Buffer** (free: 3 accounts, 10 posts/profil) - Post scheduling
8. **Pallyy** (free forever, 1 profile) - Instagram scheduling
9. **Postiz** (self-hosted, total GRATIS) - Full-featured free social media tool
10. **Make.com** (free: 1,000 ops/bulan) - Workflow automation

## 📊 30-Hari Content Calendar Integration

| Minggu | Fokus Konten | Tool Utama |
|--------|-------------|------------|
| Mg 1-3 | Behind the Build | Screen record niu-dash + HyperFrames |
| Mg 4-6 | AI Tools Gratis | 4 tools demo (Ghost, HyperFrames, Baoyu, Manim) |
| Mg 7-9 | GovTech/Pemdi | Canva infographic + Carousel |
| Mg 10-12 | AI Agent & Local AI | Manim explainer demo |
| Mg 13-15 | Aceh Pride | Didong-code storytelling |
| Mg 16-18 | Evaluasi Minggu 1 | Insights dari Meta Suite/Buffer |
| Mg 19-21 | Optimasi Naskah | Ghost humanizer + data input |
| Mg 22-24 | Produk Digital | Template & prompt-pack dari 68 skill |
| Mg 25-28 | AI Command Center | cc-acehtengah demo di Cloud Run |
| Mg 29-30 | Laporan Bulanan | Semua output di atas |

## 🚀 Workflow Ketika Jauh dari Mac

Ketika user (Afrizal Munthe) tidak berada di sekitar machine-nya, seluruh workflow di-generate otomatis berupa:

1. **HTML scaffold** untuk HyperFrames composition (9:16 aspect ratio)
2. **Terminal commands** untuk rendering MP4 (butuh Node.js + FFmpeg di machine user)
3. **Caption & hashtag** siap-copy untuk Instagram
4. **Full guide** di dokumen referensi ekosistem

**User hanya perlu:**

- Copy file HTML ke `~/Downloads/ide-reels-html/`
- Jalankan `npm install hyperframes` + `npx hyperframes render`
- Upload hasil MP4 ke Instagram Reels

## 📁 Struktur File Skill

```
skills/creative/free-tier-reels/
├── SKILL.md              <-- skill ini
├── references/
│   └── ide5-reels-workflow.md     <!-- Condensed workflow guide -->
├── templates/
│   └── reels-html-scaffold.html  <!-- HTML scaffold untuk 9:16 Reels -->
└── scripts/
    └── generate-html.sh          <!-- Script generate HTML scaffold -->
```

## ⚠️ PITFALL: User Workflow When Distant from Machine

- Ketika user jauh dari Mac/terminal, **semua output berupa script/file yang dieksekusi user kembali**.
- **Bukan** file video MP4 langsung (karena rendering butuh Node.js + FFmpeg di machine user).
- **Verifikasi** kualitas MP4 (aspect ratio 9:16, durasi 15-60 detik) sebelum upload ke Instagram Reels.
- **Watermark** "Built with Niumination" harus ada di tiap reel.
- **Tracking** di `BACKLOG.md` dan `docs/reports/` wajib setelah posting.

## ✅ CHECKLIST SEPULUH MENIT (Setup Awal di Machine User)

```bash
# 1. Pindah ke folder skills Niumination
cd ~/Desktop/Niumination/skills

# 2. Cek tools yang ada di repo
ls -la | grep -E "ghost|hyperframes|baoyu|manim"

# 3. Install hyperframes dependencies (di machine user)
npm install hyperframes@latest

# 4. Atau pakai CapCut/Canva manual kalau butuh alternatif (preference user)
#    User punya CapCut di handphone: rekam manual lebih sederhana
```

## 📋 LANGKAH-LANGKAH EKSEKUSI (KETIKA PULANG KE MAC)

1. **Buat folder:** `mkdir -p ~/Downloads/ide-reels-html && cd ~/Downloads/ide-reels-html`
2. **Copy HTML scaffold** dari `templates/reels-html-scaffold.html` ke `index.html`
3. **Install dependencies:** `npm install hyperframes@latest`
4. **Render video:** `npx hyperframes render --composition index.html --output ide5-reels-final.mp4 --width 1080 --height 1920 --duration 60 --fps 24 --audio none`
5. **Cek hasil:** `ls -la ~/Downloads/ide-reels-html/ide5-reels-final.mp4`
6. **Upload ke Instagram:** Reels > Upload MP4 > Tambah caption & hashtag

## 📝 SCRIPT & CAPTION READY-TO-COPY

### 4 Script Tool per Reels (15 detik per clip):

**Tool 1: Ghost** (Humanizer AI)

- Script: "Sudah bayar ribuan buat naskah AI yang terasa buatan? Ghost AI bikin jadi alami 1 klik. Gratis di Niumination. Built with Niumination."
- Voice-over: "Tool ke-1: Ghost AI. Naskah jadi alami 1 klik. Gratis di Niumination."

**Tool 2: HyperFrames**

- Script: "Gak butuh potongan ribuan buat bikin Reels viral? HyperFrames bikin video 9:16 viral dalam menit. 0 cost, 100% result. Cek repo Niumination. Built with Niumination."
- Voice-over: "Tool ke-2: HyperFrames. Video 9:16 jadi viral dalam menit."

**Tool 3: Baoyu Infographic**

- Script: "Karousel Infografis jual Rp50.000, sekarang gratis! Hanya di Niumination. Daftar 68 skill, ambil Link Bio. Built with Niumination."
- Voice-over: "Tool ke-3: Baoyu Infografis. Karousel keren tanpa desain."

**Tool 4: Manim Video**

- Script: "Explainer animasi jual Rp100.000+, tapi di Niumination gratis! Skill Manim Video bikin animasi keren 1 menit. Coba repo. Gratis buat educator & creator. Built with Niumination."
- Voice-over: "Tool ke-4: Manim Video. Explainer animasi jual ribuan, tapi gratis di Niumination."

### Caption Siap-Copy:

```
4 Tools AI Gratis yang Bisa Ganti Jutaan Rupiah 💸

👉 Dapet di Niumination, 100% free.
🔗 Link di bio buat gabung!

#Niumination #AITools #ContentCreator #Gratis #ReelsID #PranataKomputer
#niumination #ai #contentcreator #gratis #reels #aceh #tech #prodigital
```

### Hashtag Wajib:

`#Niumination #AITools #Gratis #Reels #contentcreator`

## 🔗 Referensi Lain di Ekosistem

- `docs/registry/composio-integration-plan.md` - Integrasi toolkit ke ekosistem
- `docs/registry/composio-free-tier-tools.md` - Daftar toolkit gratis luar composio
- `skills/creative/free-tier-reels/references/ide5-reels-workflow.md` - Guide workflow IDE-5 (rumah asli; hash terdaftar di `skills/manifest.json`)
- `BACKLOG.md` - Prioritas master proyek
- `AGENTS.md` - Global rules Niumination

## 📞 TROUBLESHOOTING

- **Jika `npm install hyperframes` error:** pastikan Node.js ≥22 terinstall (`brew install node` di macOS)
- **Jika `ffmpeg` not found:** `brew install ffmpeg`
- **Kalau user punya CapCut di handphone:** rekam manual, lebih sederhana (user preference)
- **Untuk detail per-tool:** lihat SKILL.md masing-masing di `skills/creative/`
- **Jika Node.js belum ada:** install terlebih dahulu sebelum `npm install hyperframes`

---

*Skill ini dibuat berdasarkan observasi penggunaan di sesi Afrizal Munthe, Niumination Pranata Komputer Diskominfo Aceh Tengah. Skill ini bagian dari kelas "creative" di skill bank Niumination. Setiap bulan direview untuk mencerminkan perubahan tooling & free-tier limits.*

**Catatan Pentar:** Skill ini dirancang untuk workflew di saat user JAUH dari Mac/terminal. Semua output adalah script, commands, dan guide yang bisa dieksekusi user kembali saat pulang. Bukan file video MP4 langsung (karena rendering butuh environment di machine user).
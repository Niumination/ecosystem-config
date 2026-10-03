---
name: hyperframes
description: "HyperFrames — open-source framework dari HeyGen untuk mengubah HTML + CSS + animasi menjadi video MP4. 'Write HTML. Render video. Built for agents.'"
version: 1.0.0
author: Niumination
source: heygen-com/hyperframes
tags: [creative, video, animation, html-to-video, hyperframes, heygen]
platforms: [macos, linux]
---

# HyperFrames — HTML to Video Framework

**Repo:** `github.com/heygen-com/hyperframes` (38.7k ⭐ — Apache 2.0)

## Prasyarat

- Node.js ≥22
- FFmpeg (untuk render MP4 lokal)
- Chromium (Puppeteer bundled, tidak perlu install manual)
- npm package: `npm install hyperframes` (already in root Niumination)

## ⚠️ PITFALL: JANGAN init project di dalam ekosistem Niumination

Proyek video HyperFrames adalah **artefak kerja sementara** — jangan pernah `npx hyperframes init` di dalam `~/Desktop/Niumination/` (root ekosistem) atau folder proyek lain. Folder `cc-ai-video/` di root ekosistem = **polusi struktur** (user menegur: "ini bakal ngerusak struktur ekosistem"). Video jadi & file render bersih, lalu HAPUS folder kerja atau simpan di luar ekosistem.

**Lokasi kerja yang benar:** `~/Downloads/` atau `~/Desktop/` (luar Niumination), contoh:
```bash
cd ~/Downloads
npx hyperframes init cc-ai-video --example blank
cd cc-ai-video
# ... tulis index.html ...
npx hyperframes render   # → renders/cc-ai-video_*.mp4
```
Hasil akhir MP4 bisa di-copy ke mana saja (kirim ke user), folder kerja bisa dihapus setelahnya. Verifikasi ekosistem bersih setelah selesai: `ls -d ~/Desktop/Niumination/*/` harus berisi 15 folder standar (agents apps archive brain desktop docs dotfiles labs sandbox scripts services sites skills tools vault) — tidak ada folder video asing.

## Quick Start

```bash
cd ~/Desktop/Niumination

# Init project baru
npx hyperframes init video-ku --example blank
cd video-ku

# Dev loop
npx hyperframes preview   # browser live reload (1920×1080)
npx hyperframes render    # → MP4 via Puppeteer + FFmpeg
```

## Cara Kerja

```
HTML/CSS/JS (index.html) → Puppeteer (capture frame) → FFmpeg (encode) → MP4
```

- **Input:** File HTML standar — **tanpa build step** (beda dengan Remotion)
- **Output:** MP4 deterministik, frame-accurate
- **Animasi:** Seekable via adapters (GSAP, CSS Keyframes, Anime.js, WAAPI, Three.js)
- **Durasi:** Dikontrol via `data-start` / `data-duration` di HTML

## Kapan pilih Remotion vs HyperFrames

| Kriteria | HyperFrames | Remotion |
|----------|-------------|----------|
| Authoring | HTML/CSS/JS (tanpa build) | React + TypeScript (JIT bundler) |
| Lisensi | Apache 2.0, gratis tanpa batas tim | Free tier ≤3 org; $25/bulan di atasnya |
| Agent Skills | adapters (GSAP, CSS, WAAPI) | resmi (`npx remotion skills add`) |
| Render CPU | Ringan | Berat (5–15 menit/video di CPU lemah) |
| Pilih | Konten pendek, template cepat, tim >3 orang | Agent-prompt-driven, React developer, ≤3 org |

**Aturan:** untuk thread Konten Kreator (i5-10310U, tanpa GPU), Remotion **hanya bila lisensi Free tier mencukupi** (≤3 org) dan durasi ≤30 detik. Bila render >5 menit → fallback HyperFrames. Lihat skill `remotion-video` untuk prosedur lengkap.

## Agent Workflows

### Router (baca pertama)
- `/hyperframes` — entry skill, capability map + intent router

### Creation Workflows
| Skill | Untuk |
|-------|-------|
| `/product-launch-video` | Video promosi produk dari URL |
| `/faceless-explainer` | Video explainer tanpa wajah |
| `/pr-to-video` | PR GitHub → changelog video |
| `/motion-graphics` | Motion graphic pendek (<10s), overlay, logo sting |
| `/music-to-video` | Audio → beat-synced lyric/slideshow video |
| `/slideshow` | Deck presentasi interaktif (bukan video, navigable) |
| `/general-video` | Fallback untuk semua jenis video |
| `/talking-head-recut` | Overlay grafis di video talking-head |
| `/embedded-captions` | Caption/subtitle ke video existing |

## Production Loop

1. **Plan** — tentukan workflow sesuai request (promo/explainer/caption dll)
2. **Write** — HTML + CSS + GSAP timeline (seekable, frame-accurate)
3. **Media** — resolve BGM/SFX/images/voice via `media-use` skill
4. **Lint** — `npx hyperframes lint`
5. **Preview** — `npx hyperframes preview` (lihat di browser)
6. **Render** — `npx hyperframes render` → MP4

## Rendering Options

| Method | Command |
|--------|---------|
| Local (Puppeteer + FFmpeg) | `npx --yes hyperframes@0.8.30 render . --format mp4 -f 30 --workers 1 --low-memory-mode --no-browser-gpu` |
| Cloud (HeyGen hosted) | `npx hyperframes cloud render` |
| AWS Lambda (distributed) | `npx hyperframes lambda deploy` + `lambda render` |
| Embed web component | `<hf-player src="...">` |

## ⚠️ Pin versi + flag wajib di mesin tanpa GPU

Tanpa pin, `npx hyperframes` mengambil versi terbaru apa pun — dan itu sudah
membuktikan dirinya berbahaya di mesin ini (i5-10310U, 16 GB RAM, VRAM 2 GB):

| Flag | Mengapa wajib | Bukti ukur |
|------|---------------|------------|
| `hyperframes@0.8.30` | **WAJIB.** Lint dengan CLI 0.8.62 tanpa pin = **6 warning** (`text_not_painted`, contrast 1.08:1 pada `.wnum`). Dengan pin 0.8.30 = **0 errors, 0 warnings.** | `project/reels-003-*/web/` |
| `--low-memory-mode` | **WAJIB untuk komposisi >50 detik.** Render pertama reels-003 (1628 frame) **ditolak otomatis** tanpa flag ini — butuh 13,5 GB sementara margin disk terlalu tipis untuk dipakai. Dengan flag: sukses, 262 detik. | `project/reels-003-*/render-v4.sh` |
| `--workers 1` | Dipakai di `render-v4.sh` sebagai konfigurasi aman untuk 16 GB RAM + VRAM 2 GB. **MOTIFNYA BELUM DIUKUR** — saya tidak pernah membandingkan `--workers 1` vs `--workers 2` di mesin ini, jadi bukan saya yang tahu apakah ia memang penyebabnya. Jaga di 1 sampai ada ukurannya. | nilai dari `render-v4.sh`; alasan teknis **UNCHECKED** |

Perintah lengkap terbukti (render reels-003 v4.1 final):
```bash
npx --yes hyperframes@0.8.30 render . -o output/x.mp4 --format mp4 -f 30 \
  --workers 1 --low-memory-mode --no-browser-gpu
```
Lalu mux VO dengan FFmpeg (render HyperFrames menghasilkan video bisu).

## Struktur Project

```
video-ku/
├── index.html          # Composition utama (1920×1080, data-* attributes)
├── hyperframes.json    # Config (registry, paths, media proxy)
├── AGENTS.md           # Agent guidance
├── CLAUDE.md           # Claude Code guidance
├── meta.json           # Metadata
└── package.json        # Dependencies
```

## Contoh Minimal

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="10"
     data-width="1920" data-height="1080">
  <div id="title" class="clip" data-start="0" data-duration="5" data-track-index="1"
       style="font-size:64px; color:#fff; padding:40px">
    Hello World
  </div>
</div>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  tl.from("#title", { opacity: 0, y: -50, duration: 1 }, 0);
  window.__timelines["main"] = tl;
</script>
```

## Links Penting

- Docs: https://hyperframes.heygen.com/introduction
- Showcase: https://hyperframes.heygen.com/showcase
- Playground: https://www.hyperframes.dev/
- Catalog (1,000+ blocks): https://hyperframes.heygen.com/catalog/blocks/data-chart
- Discord: https://discord.gg/EbK98HBPdk

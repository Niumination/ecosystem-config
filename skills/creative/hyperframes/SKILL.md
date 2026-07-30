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
| Local (Puppeteer + FFmpeg) | `npx hyperframes render` |
| Cloud (HeyGen hosted) | `npx hyperframes cloud render` |
| AWS Lambda (distributed) | `npx hyperframes lambda deploy` + `lambda render` |
| Embed web component | `<hf-player src="...">` |

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

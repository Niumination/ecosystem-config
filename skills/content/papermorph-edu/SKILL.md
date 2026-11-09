---
name: papermorph-edu
description: Make or edit animated, narrated, interactive web books from reference PDFs (Niumination Edu Content adaptation). Use for book planning, storyboards, chapter animation and exercises, narration, and cover and contents pages, including "make the next chapter" or "fix this animation". Deliver runnable static book files.
---

# Papermorph Edu — Niumination Adaptation

Adaptasi pipeline Papermorph (MIT, DozenTwelve/Papermorph) untuk ekosistem Niumination. Mengubah PDF buku/modul menjadi web book interaktif bernarasi.

**Perbedaan dari Papermorph asli:**
- TTS: **Piper TTS lokal** (bukan Edge TTS) — gratis, tanpa network quota
- PDF parse: **markitdown + ODL-PDF skill** (bukan pymupdf custom)
- Model: multi-model routing via 9router (bukan Opus 5.5 single model)
- Bahasa: **Bahasa Indonesia** primary (voice: `id_ID-news_tts-medium`)
- Thread binding: **12707 (Edu Content)** — terpisah dari thread 1172 (Kreator)

## Pipeline

```
PDF → Book plan → Storyboards → Narration → Animation & quizzes → Web book
```

### Stage routing (model 9router)

| Stage | Model | Provider | Status |
|-------|-------|----------|--------|
| PDF Parse | `gemini/gemini-3.8-flash` | 9router | ✅ HTTP 200 |
| Book Plan | `ag/claude-opus-4-6-thinking` | 9router | ✅ HTTP 200 |
| Storyboards | `ag/claude-sonnet-4-6` | 9router | ✅ HTTP 200 |
| Narration | Piper TTS (lokal) | — | ✅ tested |
| Quiz | `agnes/agnes-3.0-flash` | 9router | ✅ HTTP 200 |
| Web Book | Astro SSG | — | static |

**Fallback parse:** `cf/@cf/zai-org/glm-4.7-flash`, `gh/gpt-4o-mini`, `kr/glm-5-thinking` (semua HTTP 200).

## Project layout

```
~/Desktop/Niumination/labs/edu-content/<book>/
  book.pdf, sections.json      source and page map (private)
  pages/chNN/text.md           extracted reference material (private)
  BOOK.md                      current scope, conventions, helper index
  chapters.md                  chapter map and status
  chapters/chNN.md             brief storyboard, relevant errata and feedback
content/<book>/chNN/           narration.<lang>.json and TTS cache
site/                          static output; private sources stay outside
  <book>/index.html            cover + contents
  <book>/chNN/index.html       a lesson
  <book>/chNN/audio/id/        beat WAV/MP3 + timings.js
```

**Aturan ekosistem (WAJIB):**
- Source PDF, page images, extracted text → **di luar `site/`** dan di-gitignore (`*.pdf`, `*/pages/`)
- Output static → `site/` (deploy ke Vercel; CF Pages blocked — token invalid)
- Penamaan folder mengikuti DOX: `labs/edu-content/` (experimental)

## Narration — Piper TTS

```bash
# Voice model (62 MB, sekali download)
# https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx

PIPER=/Users/zaryu/src/hermes-agent/.venv/bin/piper
VOICE=/path/to/id_ID-news_tts-medium.onnx
VOICE_CFG=/path/to/id_ID-news_tts-medium.onnx.json

echo "Teks narasi bab..." > /tmp/ch01.txt
$PIPER -m $VOICE -c $VOICE_CFG -i /tmp/ch01.txt -f site/<book>/ch01/audio/id/ch01.wav
```

**Verifikasi (dari test 6 Okt 2026):**
- Voice: `id_ID-news_tts-medium` — natural, bersih
- Durasi: 6.19 detik dari 15 kata (~0.41 dtk/kata)
- Rate: 22050 Hz mono, 16-bit
- Clipping: 5/136448 sample (0.004%) — bersih
- Leading silence: 0.11 dtk, trailing: 0.03 dtk

## Chapter loop

1. **Read** — parse chapter text via markitdown/ODL-PDF. Select ideas to teach.
2. **Storyboard** — beat list, visual changes, narration triggers, quiz questions. Model: `ag/claude-sonnet-4-6`.
3. **Narration** — write `content/<book>/chNN/narration.id.json`, run Piper TTS.
4. **Beats** — implement storyboard in `site/<book>/chNN/index.html` (SVG 1600×900 + JS controls).
5. **Quiz** — Custom HTML/JS quiz (lihat `references/quiz-component.md`). Model: `agnes/agnes-3.0-flash`. Minimal 3 soal per chapter, threshold lulus 70%.
6. **Delivery pass** — check loading, blanks, cropping, text density, color consistency.
7. **Register** — update `chapters.md`, BOOK.md, chapter notes.

## Context

- Satu chapter per sesi (CPU-only render, i5-10310U)
- Durasi video ringkas ≤30 detik jika diperlukan (Remotion, thread 1172)
- Disk tight (17 GB free) — compress assets, cleanup temp
- Skill terkait: `document-content-pipeline`, `markitdown`, `remotion-video`, `ghost`, `humanizer`
- Rencana: `docs/reports/PLAN-PAPERMORPH-ADAPTASI-EDU-2026-10-05.md`
- Thread doc: `docs/reports/THREAD-12707-EDU-CONTENT-2026-10-06.md`

## Design System — Niumination Brand (WAJIB)

Semua output `site/` (index + chapter pages) **harus** menggunakan design system Niumination agar konsisten dengan niumination.web.id. Jangan gunakan tema light/cream sendiri.

**Design tokens (CSS variables):**
```css
:root {
  --ink: #14110d;          /* background utama */
  --ink-2: #1b1712;        /* background hero/card */
  --cream: #f2ecdf;        /* text utama */
  --cream-55: rgba(242,236,223,0.55);  /* text body */
  --cream-40: rgba(242,236,223,0.40);  /* text muted */
  --cream-07: rgba(242,236,223,0.07);  /* background subtle */
  --ember: #e05a1e;        /* accent primary (CTA, links, borders) */
  --ember-soft: #f07a40;   /* accent hover */
  --spotlight: #00e5ff;    /* accent secondary (glow) */
  --card-bg: rgba(242,236,223,0.03);
  --border: rgba(242,236,223,0.08);
  --border-hover: rgba(224,90,30,0.35);
}
```

**Font:**
- Display/heading: `Space Grotesk` (400-700)
- Body: `Space Grotesk` (400-500)
- Labels/micro/mono: `JetBrains Mono` (400-600)

**Pola wajib:**
- Dark theme (#14110d background), bukan light
- Topbar sticky dengan logo Niumination (hexagon + cyan dot) + nav links
- Hero section: glow orbs (ember + spotlight) + dotgrid pattern (opacity 0.05)
- Cards: border-radius 20-24px, border 1px solid var(--border), background var(--card-bg)
- Hover: border-color → var(--border-hover), translateY(-2px)
- Buttons: border-radius 999px, background var(--ember), color var(--ink)
- Status badges: rounded-full, background rgba(224,90,30,0.10), color var(--ember)
- Font labels: uppercase, letter-spacing 0.08-0.24em, JetBrains Mono

**Cara ekstrak dari reference (jika perlu update):**
1. `curl -s https://niumination.web.id/` → cari class CSS (tailwind) dan inline styles
2. Ambil hex values dari computed styles
3. Map ke CSS variables di atas
4. Terapkan ke semua pages secara konsisten

**Anti-pattern (JANGAN):**
- Tema light/cream (legacy — sudah di-replace)
- Font Plus Jakarta Sans atau Inter
- Accent gold (#C6A75E) — sudah diganti ember
- Cards putih dengan shadow — gunakan glassmorphism dark

## References

- `references/quiz-component.md` — Reusable HTML/JS quiz pattern (CSS + JS, no dependencies)

## Source

- Original: https://github.com/DozenTwelve/Papermorph (MIT)
- SKILL.md asli: `.claude/skills/papermorph/SKILL.md` (6.8 KB, 68 baris pipeline)
- Adaptasi ini mengikuti struktur asli dengan substitusi tool ekosistem

# Rencana Adaptasi Papermorph — Edu Content Thread

**Tanggal:** 2026-10-05
**Status:** Rencana (belum dieksekusi)
**Scope:** Thread Edu Content baru — PDF buku → web book interaktif

---

## 1. Ringkasan

Adaptasi pipeline Papermorph (`PDF → Book plan → Storyboards → Narration → Animation & quizzes → Web book`) ke ekosistem Niumination, dibind ke thread **Edu Content** baru, terpisah dari thread konten kreator (1172).

## 2. Pipeline Adaptasi (Revisi — Ekosistem Maksimal)

| Stage | Papermorph (asli) | Adaptasi Niumination | Model 9router |
|-------|-------------------|----------------------|---------------|
| PDF Parse | Opus 5.5 | `markitdown` + ODL-PDF skill | **kimi-k2.6** (cloudflare edge, fast) |
| Book Plan | Opus 5.5 | Structured prompt + Hermes skill | **claude-opus-4-6-thinking** (terdekat Opus 5.5) |
| Storyboards | Opus 5.5 | Creative generation | **claude-sonnet-4-6** (kreativitas tinggi) |
| Narration | TTS bawaan | **Piper TTS** (local, gratis) | — (offline, tanpa quota) |
| Animation | CSS/JS | Remotion (thread 1172 reuse) | CPU-only ≤30dtk |
| Quiz | JS interaktif | SurveyJS embed | agnes-3.0-flash |
| Web Book | Custom | Astro SSG (ringan) | Static |
| Deploy | Vercel/Cloudflare | **Cloudflare Pages** (gratis, CDN) | — |

**Kenapa model ini:**
- **claude-opus-4-6-thinking** — scored setara Opus 5.5 di benchmark independent, available di 9router
- **claude-sonnet-4-6** — upgrade signifikan dari Sonnet 4, creativity lebih baik
- **kimi-k2.6** — Cloudflare edge, fast parsing, murah
- **Piper TTS** — sudah terinstal di `.venv`, lokal, tanpa API quota
- **agnes-3.0-flash** — fast quiz generation

## 3. Thread Binding

- **Thread baru:** "Edu Content" — khusus PDF → web book
- **Pisah dari 1172:** format beda (web book vs video), audience beda
- **Model routing:** beda pipeline, jangan campur quota
- **Scope:** Afrizal only, 1 seat Free tier

## 4. Ecosystem Tools Integration

| Tool | Sumber | Status | Integrasi |
|------|--------|--------|-----------|
| **Piper TTS** | `~/.hermes/.venv/bin/piper` | ✅ Terinstal | Narration lokal |
| **Astro** | npm | ✅ Node 24 support | Static site generator |
| **Cloudflare Pages** | cloudflare.com | ✅ Gratis | Deploy web book |
| **SurveyJS** | GitHub open source | ✅ MIT | Quiz embed |
| **markitdown** | uv tool | ✅ Terinstal | PDF parse |
| **ODL-PDF** | skill bank | ✅ Ada | PDF kompleks |
| **Remotion** | sandbox | ✅ Terinstal | Animation |
| **gemini-vo-narration** | skill bank | ✅ Ada | Fallback narration |

## 5. Skill Adaptation

- Buat skill `papermorph` di bank skill (Hermes-compatible, bukan Claude Code only)
- Adaptasi `.claude/skills/papermorph/SKILL.md` → format SKILL.md Niumination
- Integrasikan existing skills: `markitdown`, `document-content-pipeline`, `remotion-video`
- Tambahkan `piper-tts` local narration workflow

## 6. Output Format

| Format | Platform | Deploy |
|--------|----------|--------|
| Web book (HTML/CSS/JS) | Static site | Cloudflare Pages |
| Video ringkas | Remotion → MP4 | Thread 1172 (jika diperlukan) |
| Quiz interaktif | SurveyJS embed | Web book |
| Narration audio | Piper Ogg/MP3 | Embedded web book |

## 7. Resource Estimate

| Resource | Estimasi | Catatan |
|----------|----------|---------|
| RAM | ≤8 GB | PDF parse + render |
| CPU | i5-10310U UHD 620 | CPU-only, ≤30dtk per clip |
| Disk | 17 GB free | Tight — compress assets, lazy load |
| Storage | SQLite + temp PDF + output static | Web book statis ringan |
| Quota | Kimi (free), Sonnet 4 (berbayar) | Piper gratis, tanpa API |

## 8. Risiko & Mitigasi

| Risiko | Mitigasi |
|--------|----------|
| Opus 5.5 tidak ada di 9router | claude-opus-4-6-thinking (setara) |
| Sonnet 4 creativity terbatas | claude-sonnet-4-6 (upgrade signifikan) |
| Disk 17GB tight | Compress assets, lazy load, cleanup temp |
| Papermorph skill Claude-only | Rewrite ke Hermes skill format |
| Web book output besar | Astro SSG (ringan), Cloudflare CDN |
| Model availability berubah | Probe HTTP-200 sebelum catat mapping |
| Piper TTS voice quality | Test dulu, fallback gemini-vo-narration |

## 9. Langkah Selanjutnya (sesuai approval)

1. ✅ Rencana ditulis (dokumen ini)
2. ⏳ Buat thread Edu Content di Telegram
3. ⏳ Probe model: verifikasi `claude-opus-4-6-thinking`, `claude-sonnet-4-6`, `kimi-k2.6` HTTP-200
4. ⏳ Test Piper TTS lokal — kualitas voice, format output
5. ⏳ Adaptasi skill Papermorph ke Hermes format
6. ⏳ Test pipeline: 1 PDF → web book (scope kecil)
7. ⏳ Ukur quota & performa
8. ⏳ Evaluasi: adopt / parsial / drop

## 10. Catatan

- Papermorph masih beta (309 ⭐, 57 commits)
- MIT license — aman legal
- Opus 5.5 hanya untuk demo, pipeline pakai model available
- Tidak ada integrasi Hermes bawaan — perlu adaptasi
- Model mapping harus lolos probe HTTP-200 sebelum dicatat (DOX rule)
- Disk 17GB tight — monitoring diperlukan

---

*Dokumen ini rencana studi, belum dieksekusi. Tunggu approval sebelum tahap 2.*

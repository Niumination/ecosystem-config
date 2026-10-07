# Thread 12707 — Edu Content

**Dibuat:** 6 Okt 2026
**Group:** `Niu-MissionControl` (`-1004204696417`)
**Link:** https://t.me/c/4204696417/12707

---

## Tujuan

Thread khusus konten edukasi — mengubah PDF buku/modul menjadi **web book interaktif bernarasi**. Ini adalah adaptasi pipeline [Papermorph](https://github.com/DozenTwelve/Papermorph) (MIT) ke ekosistem Niumination.

**Mengapa terpisah dari thread 1172 (Kreator):**
- Format beda: web book interaktif vs video vertikal/Reels
- Audience beda: pembaca (edukasi mendalam) vs penonton (konten singkat)
- Pipeline beda: PDF-heavy vs video-render-heavy
- Model routing beda: multi-stage document pipeline vs creative video pipeline

## Pipeline (adaptasi Papermorph)

```
PDF → Book plan → Storyboards → Narration → Animation & quizzes → Web book
```

| Stage | Tool | Model 9router |
|-------|------|---------------|
| PDF Parse | markitdown + ODL-PDF skill | kimi-k2.6 (cloudflare edge, fast) |
| Book Plan | Structured prompt + Hermes skill | claude-opus-4-6-thinking (terdekat Opus 5.5) |
| Storyboards | Creative generation | claude-sonnet-4-6 (kreativitas tinggi) |
| Narration | Piper TTS (lokal, gratis) | — (offline, tanpa quota) |
| Animation | Remotion (reuse dari thread 1172) | CPU-only ≤30dtk |
| Quiz | SurveyJS embed | agnes-3.0-flash |
| Web Book | Astro SSG (ringan) | Static |
| Deploy | Cloudflare Pages (gratis, CDN) | — |

Rencana lengkap: `docs/reports/PLAN-PAPERMORPH-ADAPTASI-EDU-2026-10-05.md`

## Konfigurasi

- **Model:** `inclusionai/ling-3.0-flash-fin:free` — nous (sementara, sesuai thread lain di ekosistem)
- **Provider:** nous
- **Prompt:** persona 3 blok (persona + ATURAN DOKUMEN + KREDENSIAL), 1.367 char
- **Skills binding:** `document-content-pipeline`, `markitdown`, `remotion-video`, `ghost`, `humanizer`
- **Config:** `~/.hermes/config.yaml` → `platforms.telegram.channel_overrides.12707` + `extra.channel_prompts.12707` + `extra.channel_skill_bindings`
- **Backup config:** `~/.hermes/config.yaml.bak-edu-12707-20261006-100817`

## Catatan teknis

- **YAML escaping bug ditemukan & diperbaiki:** `hermes config set` dengan key numerik di-quote shell menghasilkan literal `'''12707'''` (triple-quote) di config.yaml — key tidak terbaca sebagai `12707`. Diperbaiki via Python yaml round-trip. **Pelajaran:** untuk key numerik di `channel_overrides`, edit langsung via Python yaml (dengan backup + verifikasi parse), bukan `hermes config set` dengan shell quoting.
- Thread dibuat oleh human via `/newtopic` di Telegram (bot API tidak bisa createForumTopic tanpa akses token yang tidak diberikan ke agent).
- Routing row terdaftar di gateway setelah 1 pesan masuk ke thread.

## Status

- ✅ Thread dibuat (6 Okt 2026)
- ✅ Config terpasang (model + prompt + skill bindings)
- ✅ Registry diupdate (`docs/registry/telegram-threads.md`)
- ✅ Backup config dibuat
- ✅ Probe model pipeline — claude-opus-4-6-thinking ✅, claude-sonnet-4-6 ✅, agnes-3.0-flash ✅, gemini-3.8-flash ✅. kimi-k2.6 ❌ 503 (fallback tersedia)
- ✅ Test Piper TTS lokal — voice id_ID-news_tts-medium, bersih (clipping 0.004%)
- ✅ Adaptasi skill Papermorph → `skills/content/papermorph-edu/SKILL.md`
- ✅ Voice model disimpan di `labs/edu-content/.piper-voices/`
- ✅ Test pipeline: 1 PDF → web book — `labs/edu-content/pemdi-dasar/` (cover + ch01 + narasi MP3, HTTP 200)
- ✅ Bab 2-4 selesai (7 Okt 2026) — ch02 (52.3 dtk), ch03 (22.2 dtk), ch04 (31.8 dtk), total site 1.5 MB
- ⏳ Deploy Cloudflare Pages — pending
- ⏳ SurveyJS quiz — pending (manual HTML beat layout sebagai ganti sementara)

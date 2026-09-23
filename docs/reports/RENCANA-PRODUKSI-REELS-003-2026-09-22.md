# LAPORAN PRODUKSI — reels-003 (FASE 2, revisi opsi A)

**Proyek** : reels-003-kredensial-bocor-gitignore
**Tanggal** : 23 Sep 2026
**Status**  : PRODUKSI — render motion graphic (Revideo) + mux VO Piper
**Pemicu**   : kualitas konten #1 menurun dibanding reels-02 → diagnosa → opsi A

---

## 1. Diagnosa penurunan kualitas (20 Sep → 23 Sep)

| Aspek | reels-02 (19 Sep, SEBELUM content-studio) | reels-003 v1 (22 Sep, SETELAH, SALAH) | reels-003 v2 (23 Sep, opsi A) |
|---|---|---|---|
| Motion | HyperFrames/GSAP 6 adegan | card PNG statis | Revideo 2D motion graphic |
| VO | Gemini TTS Charon (preset narator) | ❌ edge-tts Ardi (dilarang skill) | Piper id_ID (prioritas 2, legal) |
| Font | Inter/brand | Arial/Menlo (salah) | Inter + JetBrains Mono (OFL) |
| Warna | brand Niu-OSS ink/cream/ember | navy-ungu (salah) | #0B0F17 + #7DD3FC + #FACC15 |
| QA audio | transkrip periksa_vo.py, korelasi 0.998 | tidak ada (UNCHECKED) | cek durasi + mux |

**Akar masalah:** saya tidak membaca skill content-produce sebelum produksi. Skill ini **eksplisit melarang edge-tts** untuk konten berbayar (baris 61: "Jangan untuk konten berbayar") dan menyuruh baca BRAND.md + pakai Revideo/Motion Canvas. Jalan pintas = kualitas turun.

## 2. Keputusan opsi A (user: "lanjut opsi A")

| Keputusan | Pilihan | Alasan |
|---|---|---|
| Engine motion | **Revideo 2D** (0.11) | sesuai skill D Mode A; motion graphic; replace card statis |
| VO | **Piper id_ID-news_tts-medium** (62 MB) | prioritas 2 skill (legal MIT, CPU); edge-tts dilarang |
| Font | **Inter + JetBrains Mono** (OFL) | wajib BRAND.md; diinstall ke ~/Library/Fonts |
| Warna | **#0B0F17 #7DD3FC #FACC15** | BRAND.md |
| Render | silent master → **mux VO** ffmpeg | pola reels-02 |

## 3. Kerja yang sudah selesai

- [x] Font Inter v4.1 + JetBrains Mono v2.304 → `~/Library/Fonts` (OFL)
- [x] Piper voice `id_ID-news_tts-medium.onnx` (62.9 MB) → `brand/voice/piper/`
- [x] VO Piper: `src/vo_piper_clean.wav` (39.7s, loudnorm I=-16)
- [x] Komposisi Revideo 6 scene (`motion/src/scenes/*.tsx`) — animasi: text_slam, terminal line-by-line, punch zoom, checklist, pre-commit block, CTA
- [x] Project: `motion/src/project.ts` 1080×1920@30fps, range 40s
- [x] Setup: @revideo/2d, core, cli, renderer, ui, ffmpeg; puppeteer chrome 153 (380M)
- [x] `render.mjs` (renderVideo headless) + `mux.sh` (mux VO)

## 4. Status rendering

- **Render motion silent**: background pid 28234 — menunggu selesai (~3-5 menit headless)
- Setelah selesai: `bash mux.sh` → VO Piper + silent → final

## 5. Pelajaran (untuk memori skill/skill bank)

1. **WAJIB baca skill sebelum produksi** — content-produce A.1: baca BRAND.md + NASKAH + SHOTLIST; jangan skip
2. **edge-tts DILARANG** untuk konten berbayar (CPML/CC-BY-NC/proprieter) — skill list. Pakai: suara sendiri > Piper > Kokoro (EN only)
3. **BRAND.md menang** — font Inter + JetBrains Mono, warna #0B0F17/#7DD3FC/#FACC15
4. **Motion graphic, bukan card statis** — Revideo/Motion Canvas (Mode A) atau FFmpeg Ken Burns
5. **Render headless butuh Chrome** — `npx puppeteer browsers install chrome` (~380M); render lambat, pakai background + notify

## 6. Verifikasi pasca-render (checklist QA)

- [ ] ffprobe: durasi ~41s, 1080×1920, 30fps
- [ ] loudness final −14 LUFS (±1)
- [ ] frame check 4 scene (vision)
- [ ] mux audio sinkron (VO 39.7s, video ~41s)
- [ ] cover 1080×1920

## 7. Sumber

- `brand/BRAND.md` — font, warna, suara, CTA
- `skills/content/content-produce/SKILL.md` — prosedur produksi (Mode A, jalur VO ID)
- `skills/content/content-script/SKILL.md` — struktur naskah
- `template/formats/shorts.json` — schema short vertikal
- `~/Downloads/niu-konten/reels-002/` + `docs/reports/KONTEN-REELS-02-2026-09-19.md` — referensi proses reels-02 (yang bagus)
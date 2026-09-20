# Rencana Adopsi — Hermes Content Studio (thread Kreator #1172)

**Disusun:** 20 Sep 2026 · **Status: RENJA — eksekusi TERTAHAN** (menunggu approval)
**Sumber:** `~/Downloads/hermes-content-studio.zip` (paket utama) + `~/Downloads/riset-eco-hermes.zip` (paket pendukung)
**Lingkup:** thread "Konten Kreator" (Niu-MissionControl #1172) — fokus **100% gratis / free tier**

---

## 1. Ringkasan Paket

`hermes-content-studio` adalah **bukan skill tunggal**, melainkan **studio konten lengkap** hasil perakit
berbasis riset internet September 2026, dirancang untuk niche "Vibe Coding → Production" dan **mode A
(tanpa GPU)**. Komposisinya:

| Bagian | Isi | Yang sudah terisi di paket |
|---|---|---|
| `docs/01-BLUEPRINT` | Arsitektur topic, state machine 7 tahap, 7 gerbang QA, 9 topic Telegram | 8 blueprint + 7 cron di snippet |
| `docs/02-TOOLSTACK` | ~90 tool open source per kategori + audit lisensi + jalur tanpa GPU | 10 kategori A–K, semua berlabel lisensi |
| `docs/03-MONETISASI` | 9 jalur cuan, rate card global + Indonesia, syarat platform | 9 jalur + rate card |
| `docs/04-PLAYBOOK-KONTEN` | Hook, retensi, format matrix, spesifikasi teknis | playbook lengkap |
| `docs/05-LISENSI-LEGAL` | Whitelist/blacklist lisensi, AI disclosure, kontrak | aturan legal |
| `docs/06-RADAR` | Agar konten tidak basi (cron + kurator) | mekanisme |
| `docs/07-NICHE` | 5 pilar niche + resep mode A | pilar + resep |
| `hermes/skills` | **8 skill Hermes** (format SKILL.md resmi) | siap salin, format sudah benar |
| `hermes/skill-bundles` | 5 bundle: `/content-studio`, `/audit-klien`, `/client-kit`, `/ugc-produksi`, `/repurpose` | siap salin |
| `hermes/config/config-snippet.yaml` | 9 topic + 7 cron (radar, QA, repurpose, cuan, legal, rules, riset-rate) | snippet terisi |
| `scripts/` | `trend_radar.py`, `license_audit.py`, `ratecard.py`, `ledger.py`, `vertical_clip.sh` | 5 script jalan |
| `templates/` | 19 template + 6 schema format + Rules Pack (AGENTS/CLAUDE/cursor + 3 stack + checklist audit 27 titik) | siap edit |
| `workspace/` | `BRAND.md` ter-seed + 11 CSV + kalender 30 hari + **1 proyek contoh jadi** (`audit-60-detik-rls-bocor`) | seed siap pakai |

### Paket pendukung: `riset-eco-hermes`
- **PENGATURAN-GRATIS-FREE-TIER-HERMES** — daftar free tier terverifikasi (OrcaRouter `orcarouter/auto`,
  OpenRouter `:free`, Netlify, Cloud Run, WeatherNext, LibreChat, WebLLM+Whisper lokal). Relevan untuk
  jalur monetisasi/publish yang tetap gratis.
- **DOKUMEN-PEMBELAJARAN-HERMES** + RINGKASAN-FUNGSI — konteks adopsi Hermes.

**Catatan:** niche default paket = "Vibe Coding → Production". Thread #1172 adalah **Konten Kreator
ekosistem Niumination** — niche lokal (Diskominfo Aceh Tengah, proyek OSS, layanan publik). Maka adopsi
ini = **ambil kerangka & tooling-nya, ganti niche + bukti + brand-nya** sesuai `workspace/BRAND.md` thread ini.

---

## 2. Audit Kondisi Lokal (yang sudah ada vs yang kurang)

**Sudah tersedia di mesin ini (tidak perlu diinstal ulang):**

- `ffmpeg`, `ImageMagick (magick)`, `node` — ✅ inti pipeline ada.
- Skill produksi **sudah terbukti jalan** di thread ini: HyperFrames (`npx hyperframes render`, lint 0),
  Gemini TTS `gemini-vo-narration` (3 suara + 4 preset + alat verifikasi), `periksa_vo.py`, pipeline
  `free-tier-reels` (Reels 01 & 02 sudah siap posting).
- Bank skill pusat: `~/Desktop/Niumination/skills` (145 skill) — **sumber kebenaran skill**; target
  `~/.hermes/skills` hanya hasil `sync-to-agents.sh`.
- `hermes bundles` didukung penuh (`No bundles installed yet` — siap di-install).

**Yang BELUM ada (gap):**

- `faster-whisper`, `piper-tts` — ❌ belum terpasang.
- `docker` — ❌ tidak ada → semua jalur berbasis container (ComfyUI, Coolify, Remotion headless,
  Postiz self-host, n8n) **tidak bisa jalan di mesin ini** (lihat §5 Batasan).
- GPU — tidak ada → semua model video/gambar/generatif GPU (Wan, FLUX, SVD, Orpheus, dia, Chatterbox)
  **di luar jangkauan**; dipakai hanya jalur `[tanpa GPU]`.

**Gap ini menentukan scope.** Rencana di bawah hanya mengadopsi yang **gratis, tanpa GPU, dan tanpa
Docker** di mesin ini — persis permintaan Anda ("terutama yang gratis dan free tier").

---

## 3. Rencana Adopsi — 4 Fase (semua TERTAHAN)

### FASE 1 · Kerangka (tanpa install berat) — nilai tertinggi, risiko terkecil
Adopsi **arsitektur + gerbang + template**, bukan tooling GPU:

1. **Salin 8 skill** `hermes/skills/*` → bank pusat `~/Desktop/Niumination/skills/content/`
   (bukan langsung ke `~/.hermes/skills`, supaya patuh one-home rule + sync resmi). Format SKILL.md
   sudah valid; hanya perlu cek frontmatter + register di manifest.
2. **Adaptasi niche**: edit `workspace/BRAND.md` dari niche "Vibe Coding" → **Konten Kreator
   Niumination** (bukti: 91 repo OSS, 41 tes, layanan publik Diskominfo, proyek MATA/OSS Dashboard).
   Isi placeholder 14 field.
3. **7 gerbang QA** dari blueprint → jadikan skill/checklist wajib di thread ini. Ini inti nilai paket
   (mengubah "isi" jadi "standar" — bukan sekadar tool).
4. **State machine 7 tahap** + `LEDGER.csv` + `CONTENT_INDEX.csv` → tempatkan di `workspace/` thread.
5. **Templat siap pakai**: salin `templates/formats/*.json` (6 format) + `templates/rules/*`
   (Rules Pack = lead magnet) → ke bank skill atau `workspace/templates-local/`.
6. **Rekomendasi 9 topic** (atau **minimum 1 topic** = Konten Kreator dengan `content-studio`) →
   tambahkan ke `group_topics` di `~/.hermes/config.yaml`.

**Output fase 1:** thread ini jadi punya pipeline & QA gate terstandarisasi. **Biaya: $0, tanpa GPU,
tanpa Docker.** (Ini fase yang paling saya rekomendasikan untuk disetujui dulu.)

### FASE 2 · Script gratis & ringan (yang jalan tanpa GPU/Docker)
Aktifkan script yang memang CPU-only & open source:
- `trend_radar.py` — HN + GitHub trending + Lobsters, **tanpa API key** → feed ide konten.
- `license_audit.py` — audit lisensi aset vs whitelist komersial.
- `ratecard.py` + `ledger.py` — monetisasi & buku kas (gratis, lokal).
- `vertical_clip.sh` — FFmpeg 9:16 + caption burn-in + loudnorm + safe zone (FFmpeg sudah ada ✅).

**TTS bahasa Indonesia (gratis, CPU):** paket merekomendasikan **Piper `id_ID-news_tts-medium`**
(gaya berita, agak datar) sebagai default. **Tapi kita sudah punya jalur lebih baik** — Gemini TTS
(`gemini-vo-narration`) yang terbukti di thread ini. Keputusan: **pertahankan Gemini sebagai VO utama**
(keputusan sudah dikunci sebelumnya), Piper hanya sebagai **cadangan CPU** kalau kuota Gemini habis.
Isi `workspace/brand/voice/pronunciation-id.csv` (33 istilah teknis → ejaan fonetik) untuk Piper.

**Kunci free tier untuk publish (dari paket pendukung):** OrcaRouter `orcarouter/auto` + OpenRouter
`:free` (50 req/hari tanpa kartu kredit) → untuk jalur **analitik/otomasi** tanpa biaya. Netlify
(300 credit) / Cloud Run free tier untuk **hosting Ghost/Postiz** kalau nanti butuh kanal milik sendiri.

### FASE 3 · (Opsional, butuh persetujuan per item) — hanya yang relevan & feasible
- **Postiz self-host** (scheduler 20+ platform + API/MCP) — **butuh Docker/Cloud Run**. Di mesin ini
  tanpa Docker → hanya bisa via Cloud Run free (biaya $0, perlu setup). Tunda sampai fase 2 berjalan.
- **Ghost self-host** (blog + membership berbayar, 0% potongan) — jalur "punya audiens milik sendiri".
  Butuh hosting (Cloud Run/Netlify free). Tunda.
- **code-audit ("AI Code Doctor")** — pilar paling cepat menghasilkan uang, **CPU-only**. Bisa langsung
  jalan di fase 1 (pakai tool yang ada). **Ini rekomendasi utama monetisasi.**

### FASE 4 · Yang TIDAK bisa / TIDAK disarankan di mesin ini
- Semua tool **GPU** (video generatif, FLUX, Orpheus, clone suara) — tidak ada GPU. Lewati.
- Semua tool **berbasis Docker** tanpa Docker. Lewati kecuali via Cloud Run.
- Tool **non-komersial** untuk konten berbayar (XTTS v2, F5-TTS, FLUX dev, SVD) — **jangan pernah**
  pakai, sesuai aturan emas paket: *lisensi model ≠ lisensi output*.

---

## 4. Yang Gratis & Free Tier — RINGKASAN (permintaan utama)

**Sudah terbukti & dipakai thread ini (gratis):**
`ffmpeg` · `ImageMagick` · `HyperFrames` (npx) · `Gemini TTS gemini-vo-narration` · `periksa_vo.py` ·
OpenRouter `:free` · OrcaRouter `orcarouter/auto` · GitHub Models / Kimi free tier · `Pexels/Pixabay/
Unsplash/Poly Haven` (aset CC0/permisif) · `Inkscape/Excalidraw` (desain CPU) · `Kdenlive/Shotcut/
LosslessCut/Auto-Editor` (edit CPU) · `Motion Canvas/Revideo` (animasi kode, CPU) · `Kokoro-82M`
(TTS CPU, untuk segmen bahasa Inggris).

**Dari paket, gratis & CPU-only yang belum terpasang (layak di-add fase 2):**
`faster-whisper` (transkrip/caption CPU) · `Piper id_ID` (VO cadangan CPU) · `WhisperX` (caption
word-level) · `trend_radar.py` · `license_audit.py` · `ratecard.py` · `ledger.py` · `vertical_clip.sh`.

**Free tier (gratis, butuh setup hosting):**
OrcaRouter (0 markup, no CC) · OpenRouter :free (50 req/hari) · Netlify 300 credit · Cloud Run free ·
WeatherNext free · Postiz self-host (via Cloud Run).

**Yang harus Dihindari (biaya bersembunyi):** tool GPU, tool Docker tanpa Docker, aset non-komersial,
`Remotion` untuk tim ≥4 (lisensi komersial), CapCut (cek kebijakan komersial).

---

## 5. Batasan & Risiko (perlu Anda tahu sebelum eksekusi)

1. **Tidak ada Docker** → 3 dari 7 jalur "kanal milik sendiri" (Postiz, n8n, ComfyUI) tunda sampai
   bisa via Cloud Run. Ini memotong jalur otomasi publish otomatis; publish tetap manual untuk saat ini.
2. **Tidak ada GPU** → tidak ada video/gambar generatif. Semua produksi = rekaman layar, animasi kode
   (Motion Canvas/HyperFrames), slideshow, aset CC0, TTS Gemini/Piper. Ini **cukup** untuk konten
   edukasi/teknis, tapi membatasi "B-roll sinematik".
3. **Format grup #1172**: thread ini adalah **Telegram topic** (thread_id 1172). Binding
   `group_topics` butuh **chat_id supergrup + thread_id**. Thread #1172 milik Niu-MissionControl —
   perlu Anda konfirmasi apakah mau di-bind ke skill `content-studio` (hot-reload, tanpa restart).
4. **Niche berbeda** — paket default = Vibe Coding. Adopsi wajib ganti `BRAND.md`. Saya sudah menyiapkan
   mapping buktinya (§3.2). Tanpa ini, template-nya tidak akan "klik" dengan audiens thread ini.
5. **Skill bank** — `hermes/skills/*` (8 skill) harus masuk ke **bank pusat** lalu via sync resmi
   (one-home rule). Dilarang copy-paste manual ke target. **Ini butuh approval Anda** (hard rule
   self-change guard untuk skill bank).
6. **Secret** — `POSTIZ_API_KEY`, `HF_TOKEN`, `GITHUB_TOKEN` dsb. hanya di `~/.hermes/.env`; jangan
   pernah masuk workspace proyek. Follow aturan kredensial DOX.

---

## 6. Urutan Rekomendasi & Keputusan yang Butuh Anda

**Rekomendasi eksekusi bertahap (tiap tahap berhenti minta approval):**
1. **FASE 1** (kerangka + QA gate + state machine + adaptasi BRAND.md + 8 skill ke bank pusat) —
   **nilainya terbesar, risk-nya terkecil, $0.**
2. **FASE 2** (script CPU + Piper cadangan + free-tier publish OrcaRouter/OpenRouter/Netlify/Cloud Run).
3. **code-audit (pilar monetisasi cepat)** — bisa langsung di fase 1 karena CPU-only.
4. FASE 3 (Postiz/Ghost via Cloud Run) — **tunda** sampai fase 1–2 terbukti.

**Pertanyaan approval (menahan eksekusi):**

- (a) **Setujui FASE 1** (8 skill → bank pusat `~/Desktop/Niumination/skills/content/` + adaptasi
  BRAND.md + QA gate + state machine)? Ini menyentuh **skill bank** → wajib izin eksplisit Anda.
- (b) Mau **bind thread #1172 ke skill `content-studio`** di config (hot-reload, tanpa restart)?
- (c) TTS utama: **pertahankan Gemini** (sudah dikunci) + Piper hanya cadangan — setuju?
- (d) Monetisasi cepat: mau saya aktifkan jalur **`code-audit` (AI Code Doctor, CPU-only)** sebagai
  pilarnya?

> Saya belum menyentuh apa pun: belum menyalin skill, belum menambah config, belum menginstal tool.
> Semua di atas hanya **rencana**. Setelah Anda memilih (a)–(d), saya eksekusi bertahap dengan bukti
> per tahap (command + exit code + daftar file).

---

## 7. Bukti (pelajari paket, tanpa eksekusi)

- Paket ter-ekstrak ke `/tmp/hermes-content-studio/` & `/tmp/riset-eco/` (32 + 7 file).
- `hermes bundles list` → "No bundles installed yet" (fitur tersedia, belum dipakai).
- Audit tool lokal: `ffmpeg` ✅ `magick` ✅ `node` ✅ `docker` ❌ `faster-whisper` ❌ `piper-tts` ❌.
- `config-snippet.yaml` berisi 9 topic + 7 cron — sudah saya baca penuh.
- Skill produksi yang sudah teruji di thread ini: HyperFrames (Reels 02 render 56.6 s, lint 0),
  Gemini TTS (`gemini-vo-narration`), `periksa_vo.py`.

# Rencana Adopsi — Hermes Content Studio (thread Kreator #1172) — v2 DISEMPURNAKAN

**Disusun:** 20 Sep 2026 · **Status: RENJA — eksekusi TERTAHAN** (menunggu approval)
**Sumber:** `~/Downloads/hermes-content-studio.zip` + `~/Downloads/riset-eco-hermes.zip`
**Fokus:** 100% gratis / free tier · **disesuaikan ke profil mesin & ekosistem yang sebenarnya**

> **Kenapa versi v2:** versi v1 mengasumsikan "mesin tanpa GPU/Docker" secara umum.
> Setelah inspeksi menyeluruh (mesin = **Intel Core i5-10310U x86_64, RAM 16GB, GPU Intel
> UHD 620, macOS 26.5**, ekosistem 108 model live via 9router, skill bank 145, beberapa repo
> dirty), banyak asumsi harus dikoreksi. Mitigasi & dampak di bawah berbasis data nyata ini.

---

## 0. Profil Perangkat & Ekosistem — DANGKALNYA (fakta terverifikasi)

| Aspek | Fakta terukur | Dampak pada rencana |
|---|---|---|
| CPU | Intel Core i5-10310U, 8 thread, x86_64 (Intel, **bukan** Apple Silicon) | Model AI biner harus varian **x86**; CPU lambat → TTS lokal lambat |
| RAM | 16 GB, saat ini **~0 tersedia** (16G used, 244M unused) | Beban tinggi; **jangan** jalankan model lokal besar bersamaan dengan gateway |
| GPU | Intel UHD 620, VRAM **2 GB dinamis**, Metal 3 | `VRAM < 8GB` → **semua** model video/generatif/GPU di paket **tidak bisa jalan** |
| Disk | 128 GB, **~21 GB free** | Cukup untuk tool CPU; **tidak cukup** untuk model GPU (5–12 GB + dataset) |
| Docker | **TIDAK ADA** (docker/podman tidak ada) | Semua jalur container (ComfyUI, n8n, Remotion headless, Postiz lokal) **mati** |
| ffmpeg/magick/node/npx/obs/gh/uv | ✅ ada di `/usr/local/bin` | Tulang punggung pipeline **sudah siap** |
| piper | ✅ **ADA** di venv `~/src/hermes-agent/.venv/bin/piper` | TTS cadangan CPU **sudah terpasang** — tinggal unduh voice |
| voice Piper `id_ID` | ❌ belum diunduh | Perlu unduh ~63 MB ONNX (sangat murah, ~1 menit) |
| 9router | `localhost:20128` **live**, 108 model, provider aktif: antigravity, cloudflare-ai, elevenlabs, firecrawl, gemini(×2), github, kiro | **Sumber model gratis** sudah stabil — bisa jadi "fallback LLM" tanpa GPU |
| Skill bank | 145 skill di `~/Desktop/Niumination/skills` (sumber kebenaran), sync ke `~/.hermes/skills` | 8 skill paket **wajib** masuk bank pusat → sync resmi (one-home rule) |
| Repo dirty | Root (1 file: `scripts/provider-health-check.sh`), `apps/PemdiAcehTengah`, `apps/niu-dash` | **Jangan** commit blind; commit selektif sesuai DOX |
| Load | Load avg ~5,7 (tinggi) | Tunggu mesin idle untuk uji TTS lokal; jangan saingi gateway |

---

## 1. Ringkasan Paket (dari inspeksi penuh)

Bukan 1 skill, melainkan **studio konten lengkap** hasil riset Sep 2026 untuk niche
"Vibe Coding → Production", Mode A (tanpa GPU):

- **`hermes/skills/`** — 8 skill format SKILL.md valid: `content-studio` (orchestrator + pipeline +
  QA gate), `content-research`, `content-script`, `content-produce`, `content-publish`,
  `content-monetize`, `content-legal`, `code-audit`.
- **`hermes/skill-bundles/`** — 5 bundle: `/content-studio`, `/audit-klien`, `/client-kit`,
  `/ugc-produksi`, `/repurpose`.
- **`hermes/config/config-snippet.yaml`** — 9 topic binding + 7 cron job (radar pagi, QA siang,
  repurpose sore, cuan Jumat, legal mingguan, rules bulanan, riset rate).
- **`docs/02-TOOLSTACK`** — ~90 tool per kategori **semua berlabel lisensi & jalur [tanpa GPU]**.
- **`docs/04-PLAYBOOK-KONTEN`** — bank 40 hook, struktur retensi, spesifikasi teknis per platform,
  FFmpeg siap pakai, format matrix 14, repurposing matrix, SEO, kalender, protokol A/B, metrik.
- **`scripts/`** — 5 script CPU-only & free: `trend_radar.py` (HN+GitHub+Lobsters, **tanpa API key**),
  `license_audit.py`, `ratecard.py`, `ledger.py`, `vertical_clip.sh` (FFmpeg 9:16+caption+loudnorm).
- **`templates/`** — 19 template + 6 schema format + Rules Pack (AGENTS/CLAUDE/cursor + 3 stack +
  checklist audit 27 titik = lead magnet).
- **`workspace/`** — `BRAND.md` ter-seed + 11 CSV + kalender 30 hari + **1 proyek contoh jadi**
  (`audit-60-detik-rls-bocor`).

**Paket pendukung** `riset-eco-hermes`: daftar free-tier terverifikasi (OrcaRouter `orcarouter/auto`,
OpenRouter `:free` 50 req/hari no-CC, Netlify 300 credit, Cloud Run free, LibreChat, WebLLM+Whisper
lokal) + konteks adopsi Hermes.

**Penting:** niche default = Vibe Coding. Thread #1172 = **Konten Kreator Niumination**
(layanan publik Diskominfo, OSS 91 repo, proyek MATA/OSS-Dashboard). → adopsi = **ambil
kerangka & tooling, ganti niche + bukti + brand** via `BRAND.md`.

---

## 2. Gap Mesin vs Paket (apa yang bisa / tidak bisa di perangkat INI)

**Bisa langsung dipakai (sudah ada):**
`ffmpeg` · `ImageMagick` · `node`/`npx` · `obs` · `gh` · `uv` · `piper` (venv) ·
`HyperFrames` (npx, teruji di Reels 01/02) · `Gemini TTS` (`gemini-vo-narration`, terkurasi 3 suara)
· `periksa_vo.py` · `trend_radar.py` · `license_audit.py` · `ratecard.py` · `ledger.py` ·
`vertical_clip.sh` · 9router (108 model live, gratis).

**Perlu unduh ringan (gratis, <200 MB, ~1–5 menit):**
- Voice Piper `id_ID-news_tts-medium` (~63 MB ONNX) → cadangan VO CPU.
- `faster-whisper` model `small`/`base` (~150–500 MB) → caption/transkrip CPU (opsional;
  `periksa_vo.py`/Gemini ASR sudah menutup sebagian).

**TIDAK bisa (kondisi perangkat) — di-eliminasi, bukan ditunda:**
- **Segala model GPU** (Wan, FLUX, SVD, Orpheus, Chatterbox, Qwen-Image, LatentSync) — VRAM 2 GB +
  disk 21 GB tidak memadai. Paket sendiri menandai semuanya bukan `[tanpa GPU]`.
- **Semua jalur Docker** (ComfyUI, n8n, Remotion headless, Postiz lokal, Coolify) — tidak ada Docker.
  Mitigasi: jalur self-host via **Cloud Run / Netlify free tier** (fasilitas di paket pendukung).
- **Kokoro** (untuk segmen EN) — CPU-only tapi **belum terpasang**; opsional, bukan urgent.

---

## 3. Rencana 4 Fase (masing-masing TERTAHAN, bukti per tahap)

### FASE 1 · Kerangka ($0, tanpa GPU, tanpa Docker) — nilai tertinggi
1. **Salin 8 skill** `hermes/skills/*` → bank pusat `~/Desktop/Niumination/skills/content/`
   (BUKAN langsung ke `~/.hermes/skills`). Cek frontmatter + register di manifest.
   - *Dampak:* menambah 8 entri ke skill bank → wajib lewat `sync-to-agents.sh` resmi (one-home rule).
   - *Mitigasi:* **ini menyentuh skill bank → wajib approval eksplisit Anda** (hard rule self-change guard).
   - *Rollback:* `git revert` 1 commit + sync ulang; tidak ada efek ke config.
2. **Adaptasi `BRAND.md`**: niche Vibe Coding → Konten Kreator Niumination; isi 14 field
   (bukti: 91 repo OSS, 41 tes, layanan publik 52 OPD, MATA, OSS-Dashboard).
3. **7 gerbang QA** + **state machine 7 tahap** + `LEDGER.csv` + `CONTENT_INDEX.csv` →
   `workspace/` thread. Ini inti nilai paket (standarisasi, bukan sekadar tool).
4. **Template siap pakai**: `formats/*.json` (6) + `rules/*` (Rules Pack = lead magnet) →
   bank skill / `workspace/templates-local/`.
5. **Bind 9 topic (atau minimum 1)** ke `group_topics` di `~/.hermes/config.yaml` — hot-reload,
   tanpa restart.

   *Dampak:* config.yaml bertambah → per **DOX "Jangan edit config saat repair berjalan"**
   (insiden 27 Agu) — cek `docs/reports/ECOSYSTEM-STATUS-*` dulu sebelum sentuh config.
   *Mitigasi:* backup `config.yaml.bak-YYYYMMDD` sebelum edit; hanya tambah blok, jangan ubah yang ada.
   *Rollback:* `cp config.yaml.bak-* config.yaml` lalu restart gateway.

### FASE 2 · Script CPU + Free-Tier (gratis, ringan)
- Aktifkan `trend_radar.py`, `license_audit.py`, `ratecard.py`, `ledger.py`, `vertical_clip.sh`.
- **Unduh voice Piper `id_ID`** (63 MB) → VO cadangan CPU.
- **TTS: pertahankan Gemini** (sudah dikunci, terkurasi) sebagai VO utama; **Piper = cadangan**
  kalau kuota Gemini habis. Isi `pronunciation-id.csv` (33 istilah teknis → ejaan fonetik) untuk Piper.
- **Free-tier publish**: OrcaRouter `orcarouter/auto` (0 markup, no CC) + OpenRouter `:free`
  (50 req/hari) → analitik/otomasi tanpa biaya; Netlify (300 credit) / Cloud Run free →
  hosting Ghost/Postiz bila mau kanal milik sendiri.

  *Dampak:* unduhan ~200 MB ke disk (21 GB free) — aman. Load CPU: Piper CPU ~realtime, ringan.
  *Mitigasi:* unduh saat load avg < 3 (sekarang ~5,7, tinggi) — **atur jadwal, jangan saingi gateway**.
  *Kredensial:* `ORCAROUTER_API_KEY`, `POSTIZ_*` hanya di `~/.hermes/.env` — jangan masuk workspace.

### FASE 3 · Monetisasi Cepat (CPU-only) — `code-audit` ("AI Code Doctor")
- 1 audit repo → **2 output**: laporan klien (dibayar) + 3–5 konten (dianonimkan). CPU-only, langsung
  jalan di Fase 1. Ini jalur uang tercepat dari paket.
- *Mitigasi:* hasil audit klien **wajib dianonimkan** (tanpa path/email/token/data klien) sebelum jadi
  konten — sesuai gerbang QA #6 (privasi).

### FASE 4 · Self-Host via Free-Tier Hosting (OPSIONAL, butuh keputusan)
- Postiz / Ghost di **Cloud Run / Netlify free tier** (bukan Docker lokal).
- *Dampak:* menambah biaya $0, tapi perlu account + domain. *Mitigasi:* tunda sampai Fase 1–2 terbukti.

---

## 4. Matriks Mitigasi & Dampak (inti permintaan Anda)

| Risiko | Dampak jika terjadi | Mitigasi | Mitigasi aktif |
|---|---|---|---|
| Skill bank tersentuh tanpa sync resmi | 8 skill "tenggelam", divergensi with target | Salin ke bank pusat + `sync-to-gates.sh` + manifest | Menunggu approval Anda (a) |
| Config di-edit saat ada repair | Gateway rusak (insiden 27 Agu) | Cek `ECOSYSTEM-STATUS-*` + backup + restart terpisahkan | Cek status sebelum Fase 1.5 |
| Repo dirty di-commit blind | Insiden kredensial (16 Sep) / merge error | `git add` selektif, gate `secret-scan-staged.py` | Commit 1 file `scripts/provider-health-check.sh` dulu (approval b) |
| Voice Piper tidak didukung / pelafalan teknis rusak | VO cadangan tidak bisa dipakai | Kamus `pronunciation-id.csv`; uji `uji.wav` SEBELUM render | Isi kamus + uji saat FASE 2 |
| Load mesin tinggi (~5,7) saat unduh/jalan model | Gateway Telegram melambat | Jadwalkan unduhan saat idle (<3) | Aturan eksplisit di FASE 2 |
| Gemini free tier habis / berubah | VO utama hilang | Piper cadangan CPU sudah siap | Fallback teruji |
| 9router provider mati | Model gratis hilang | 108 model dari 8 provider; ada redundansi | `audit_models.py` bila ada yang 0 OK |
| Konten berbayar pakai aset non-komersial | Monetisasi mati + DMCA | `license_audit.py` + `ASSETS_LICENSE.csv` tiap unduhan | FASE 2 + gerbang QA #6 |
| Niche default salah (Vibe Coding) | Template tidak "klik" | Adaptasi `BRAND.md` | FASE 1.2 |
| VRAM 2 GB / disk 21 GB dipaksakan | Crash/OOM | **Eliminasi semua jalur GPU & Docker** (Fase 4 via hosting) | Sudah di FASE 4 |

---

## 5. Keputusan yang Butuh Anda (eksekusi TERTAHAN)

- **(a)** Setujui **FASE 1** — salin 8 skill ke bank pusat `~/Desktop/Niumination/skills/content/`
  + adaptasi `BRAND.md` + QA gate + state machine. **Menyentuh skill bank → wajib izin eksplisit.**
- **(b)** Setujui **commit 1 file dirty** `scripts/provider-health-check.sh` (sebelum commit, jalankan
  gate `secret-scan-staged.py`)? Ini memblokir `up-eco` sampai bersih.
- **(c)** **Bind thread #1172** ke skill `content-studio` di config (hot-reload, backup config dulu)?
- **(d)** TTS: **pertahankan Gemini** sebagai VO utama + **Piper `id_ID`** (unduh 63 MB) sebagai
  cadangan CPU — setuju?
- **(e)** Jalur monetisasi: aktifkan **`code-audit` (AI Code Doctor, CPU-only)** sebagai pilar?
- **(f)** FASE 4 (self-host via Cloud Run/Netlify): **tunda** sampai FASE 1–2 terbukti — setuju?

---

## 6. Bukti (inspeksi menyeluruh, tanpa eksekusi)

- **Mesin:** `i5-10310U x86_64 · 8 thread · 16GB RAM (used, ~0 avail) · GPU UHD 620 (VRAM 2GB) ·
  disk 21GB free · load 5,7`.
- **Tool:** `ffmpeg magick node npx obs gh uv` ✅; `piper` ✅ di venv; `docker/kdenlive/auto-editor/
  kokoro` ❌; voice Piper `id_ID` ❌ belum.
- **Ekosistem:** `up-eco` → HEAD `310820a`, 3 repo dirty (root/PemdiAcehTengah/niu-dash). 9router
  `:20128` live, 108 model, 8 provider aktif.
- **Paket:** ter-ekstrak `/tmp/hermes-content-studio/` (32 file) & `/tmp/riset-eco/` (7 file);
  playbook, toolstack, 8 skill, 5 script, config-snippet 9-topic + 7-cron dibaca penuh.
- **Belum disentuh:** tidak ada skill, config, tool, atau commit. Hanya inspeksi + 2 dokumen rencana
  di `docs/reports/`.

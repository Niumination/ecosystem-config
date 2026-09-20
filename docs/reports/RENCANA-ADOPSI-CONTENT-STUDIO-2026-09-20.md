# Rencana Adopsi — Hermes Content Studio (thread Kreator #1172) — v3 SPEK-ADAPTASI PENUH

**Disusun:** 20 Sep 2026 · **Status: RENJA — eksekusi TERTAHAN** (menunggu approval)
**Sumber:** `~/Downloads/hermes-content-studio.zip` (28 item) + `~/Downloads/riset-eco-hermes.zip` (6 item, v4.1 Free Tier Edition)
**Perubahan dari v2:** seluruh isi kedua paket **disedangkan per-baris** ke spesifikasi Mac ini — setiap rekomendasi tool kini punya status *ada / perlu unduh / TIDAK BISA di mesin ini*, plus jalur penggantinya.

---

## 0. Spesifikasi Target (satu-satunya tempat rencana ini bisa jalan)

| Aset | Nilai terukur | Konsekuensi desain |
|---|---|---|
| CPU | Intel Core i5-10310U · x86_64 · 8 thread (bukan Apple Silicon) | Semua binary/whisker harus varian **x86** (whisper.cpp `ggml-*.bin` = versi x86) |
| RAM | 16 GB (saat diukur terpakai ~16G, sisanya ~0) | **Aturan beban:** model CPU berjalan **satu-satu, berurutan**, tidak bersamaan; unduhan dijadwalkan saat load < 3 |
| GPU | Intel UHD 620 · VRAM 2 GB dinamis | **VRAM < 8 GB = SELURUH model GPU di paket tidak bisa jalan** |
| Disk | 128 GB · ~21 GB free | Cukup untuk tool CPU (whisper small ~250 MB, revideo npx, dll); **tidak cukup** model GPU 5–12 GB + dataset |
| Docker | **tidak ada** (docker & podman tak terpasang) | Semua jalur container di paket (ComfyUI, n8n, Remotion headless, LibreChat, `docker-compose.free-tier.yml`) **dibuang dari rencana** |
| OS | macOS 26.5 (Intel) | Homebrew `/usr/local` · `uv` tersedia → unduhan tool lewat `brew` / `uv pip` |

**Yang sudah ada & siap (verifikasi per-tool, bukan asumsi):**

| Tool | Status | Lokasi |
|---|---|---|
| ffmpeg (loudnorm/subtitles/scale/crop/zoompan filter ✅) | ADA | `/usr/local/bin/ffmpeg` |
| ImageMagick (magick) | ADA | `/usr/local/bin/magick` |
| node + npx (v26.7.0) | ADA | `/usr/local/bin` |
| OBS Studio (rekaman layar — inti Mode A) | ADA | `/usr/local/bin/obs` |
| gh CLI | ADA | `/usr/local/bin/gh` |
| gitleaks (jantung code-audit) | ADA | `/usr/local/bin/gitleaks` |
| **Piper TTS** | **ADA** di venv `~/src/hermes-agent/.venv/bin/piper` | onnxruntime 1.23.2 terpasang |
| **edge-tts** | **ADA** di venv yang sama | pengganti cadangan Gemini |
| 9router `:20128` | LIVE, 108 model (namespace `ag/cf/gemini/gh/kr`; label "*-free*" cuma `gh/gpt-5.4-mini-free-auto` & `gh/gpt-5.6-luna-free-auto`) | sumber LLM bebas GPU |

---

## 1. Peta Paket Studi → Spek Mesin (inti permintaan: "seluruh isi zip sesuai spek")

### 1.1 Skill Hermes (8) — `hermes/skills/*`

| Skill | Bergantung ke tool | Kesiapan di Mac ini | Tindakan adaptasi |
|---|---|---|---|
| `content-studio` (orchestrator + 7 QA gate) | teks + filesystem | **Siap 100%** | Salin ke bank pusat `skills/content/` + sync resmi |
| `content-research` | `web_search`, `trend_radar.py` (stdlib, tanpa key) | **Siap 100%** | Salin + aktifkan |
| `content-script` (hook bank, naskah, storyboard, caption) | teks | **Siap 100%** | Salin |
| `content-produce` | ffmpeg ✅, magick ✅, piper ✅ (voice belum), whisperX ❌, ComfyUI ❌, Revideo ❌(npx bisa), OBS ✅ | **~70% siap** | Patch SKILL.md: tandai jalur GPU/Docker sebagai *tidak tersedia di host ini*; VO utama = Gemini, cadangan = Piper/edge-tts |
| `content-publish` | scheduler `POSTIZ_URL` (butuh self-host) | **Tidak ada** (Postiz = Docker/self-host) | **Modus manual**: paket hasil render dikirim "siap posting" ke thread (persis kondisi sekarang); self-host hanya bila Cloud Run |
| `content-monetize` | ratecard.py, ledger.py (CPU) | **Siap 100%** | Salin |
| `content-legal` | license_audit.py (CPU) | **Siap 100%** | Salin |
| `code-audit` | gitleaks ✅; **trivy/semgrep/pip-audit/bandit/osv-scanner/lizard ❌** | **~50% siap** | **Unduh ringan**: `brew install trivy semgrep osv-scanner bandit lizard` + `uv tool install pip-audit` (~100–300 MB, CPU-only, gratis) → lalu 100% siap |

### 1.2 Bundle (5) & config-snippet (9 topic + 7 cron)

| Item | Kesiapan | Tindakan |
|---|---|---|
| `/content-studio`, `/audit-klien`, `/client-kit`, `/ugc-produksi`, `/repurpose` (5 bundle) | `hermes bundles` tersedia (belum ada) | Pasang 5 YAML ke `~/.hermes/skill-bundles/` + `hermes bundles reload` |
| Binding 9 topic | Thread #1172 sudah ada di `channel_skill_bindings` (`[ghost, humanizer]`) | Tambah skill `content-studio` ke binding 1172; **9 topic penuh = opsional** (minimum viable = 1 topic, sesuai blueprint) |
| Cron `radar-tren-pagi` 07:00 | `trend_radar.py` jalan tanpa key | **Aktifkan** — hasil dikirim ke thread |
| Cron `qa-siang` 13:00 | baca `STATUS.md` + ffprobe (CPU ringan) | **Aktifkan** |
| Cron `repurpose-sore` 16:00 | butuh konten terbaik di CONTENT_INDEX | Aktifkan setelah 2+ konten diarsip |
| Cron `laporan-cuan` Jumat 20:00 | `ledger.py summary` | Aktifkan (ringan) |
| Cron `audit-lisensi` Senin 09:00 | `license_audit.py` | Aktifkan (ringan) |
| Cron `kuras-rules-pack` Sabtu 11:00 | pembacaan CSV | Aktifkan (ringan) |
| Cron `riset-rate-bulanan` | web_search | Aktifkan (ringan) |
| `security: approval_mode: ask` (disarankan snippet) | sudah sesuai aturan DOX | Biarkan default Hermes |

### 1.3 Toolstack (90 tool) — per kelas, keputusan "yang bisa di Mac ini"

| Kelas | Di Mac ini | Alasan |
|---|---|---|
| A Mesin inti | **FFmpeg ✅ · Whisper (faster-whisper kecil) ✅ (unduh) · whisper.cpp ✅ (sudah di `/tmp/ggml-medium.bin` 1.4 GB dari sesi sebelumnya — **kalikan & tempatkan resmi**) · OBS ✅ · Git ✅ · ComfyUI ❌ (Docker) · Ollama/vLLM ❌ (GPU)** | GPU 2 GB & tanpa Docker |
| B TTS | **Piper `id_ID` ✅ (venv ada; voice unduh 63 MB) · edge-tts ✅ (venv; gratis, online) · Gemini TTS ✅ (provider 9router/nous, sudah dikunci) · Kokoro ⚠️ (CPU lambat, opsional) · Chatterbox/Orpheus/XTTS/F5/SVD ❌ (GPU/non-komersial)** | Urutan: Gemini > Piper/edge > Cocokro (EN) |
| C Gambar | **Inkscape/Excalidraw/Blender (CPU) ✅ · ImageMagick ✅ · Qwen-Image/FLUX/SDXL/Z-Image ❌ (GPU)** | Thumbnail/carousel = HTML+magick (alur Reels 01/02 sudah membuktikan) |
| D Video generatif/avatar | **FramePack 6 GB ⚠️ (teori saja, VRAM 2 GB → praktis tidak bisa) · sisanya ❌** | Semua B-roll = rekaman OBS + aset CC0 |
| E Editor & motion | **Motion Canvas / Revideo ✅ via `npx` (CPU, gratis, batch render API) · Auto-Editor ✅ (npm/`npx`) · LosslessCut ✅ (App, gratis) · Kdenlive/Shotcut/OpenCut ⚠️ (App, opsional) · Remotion ⚠️ (JIT, lisensi individu OK)** | Revideo + Auto-Editor = mesin template tanpa GPU |
| F Audio/musik | **Audacity ✅ · DeepFilterNet ✅ (`uv tool install`) · ACE-Step ⚠️ (CPU lambat; musik latar pakai aset CC0: Free Music Archive/Mixkit) · Demucs ⚠️** | Prioritas CC0 (gratis, tanpa unduh besar) |
| G Distribusi | **Postiz ❌ (Docker) → manual posting + n8n ❌ → `Huginn` ⚠️ (Ruby, opsional) · Plausible/Umami ✅ (server opsional)** | Jalur publish = **manual** (sesuai status thread hari ini) |
| H Kanal milik sendiri | **Ghost ⚠️ (via Cloud Run/Netlify free — FASE hosting) · Matrix/Discourse/Supabase ⚠️ (hanya bila FASE hosting)** | Tunda — lihat §4 |
| I Aset gratis | **Pexels/Pixabay/Unsplash/Mixkit/Poly Haven/ISO Republic ✅ (CC0) · Freesound CC0 · Google Fonts OFL ✅** | Setiap unduhan tercatat `ASSETS_LICENSE.csv` (skill `content-legal`) |
| J Riset | **trend_radar.py ✅ (tanpa key) · HN/GitHub/Lobsters ✅ · GitHub Search API ⚠️ (rate limit 60/jam tanpa token — pakai `gh` + token GitHub yang ada) · pytrends ✅ (BSD)** | Radar harian = CPU ringan |
| K DevOps | **Uptime Kuma ⚠️ (server) · Restic ✅ (backup arsip konten — penting, aset=modal) · MinIO/Vaultwarden/Immich ❌ (Docker/berat)** | Fokus: `Restic` untuk arsip `workspace/output/` |

### 1.4 Script (5) — semuanya CPU-only & stdlib, **bisa 100% di Mac ini**

| Script | Verifikasi | Catatan |
|---|---|---|
| `trend_radar.py` | stdlib urllib, tanpa API key ✅ | GitHub Search API pakai token `gh` bila tersedia |
| `license_audit.py` | stdlib + `package.json`/`requirements.txt` parsing ✅ | aman CPU |
| `ratecard.py`, `ledger.py` | stdlib CSV/MD ✅ | |
| `vertical_clip.sh` | FFmpeg filter loudnorm/scale/subtitles ✅ tersedia | siap pakai |

### 1.5 Template (19 + 6 format + Rules Pack) — teks murni

**Bisa 100% di Mac ini** (Markdown/JSON). Yang langsung berguna untuk thread ini:
`naskah-short-vertical`, `formats/shorts.json`, `kalender-konten-30hari`, `konten-brief`,
`rules/audit-checklist.md` (lead magnet "27 titik"), `rules/stacks/public-service.md`
(**cocok untuk PemdiAcehTengah — layanan publik, bukan vibe coding**).

### 1.6 `workspace/` seed — `BRAND.md` (niche Vibe Coding) harus ditulis ulang untuk **Konten Kreator Niumination**

- BUKTI diisi dari ekosistem nyata: 91 repo OSS, 41 tes lulus, 101 berkas JSON API, 52 OPD,
  proyek MATA/OSS-Dashboard (data yang sudah Anda punya — bukan placeholder).
- `AUDIT_PATTERNS.csv`, `CALENDAR.csv` (30 baris), `HOOKS_PROVEN.csv`, dll — dipakai apa adanya.
- **Proyek contoh `audit-60-detik-rls-bocor`** = template alur kerja code-audit → konten (anonim).

### 1.7 dari paket `riset-eco` (v4.1 Free Tier) — yang masuk rencana thread ini

| Item paket | Status di Mac ini | Keputusan |
|---|---|---|
| OrcaRouter `orcarouter/auto` (0 markup, no CC) | LLM cloud, jalan dari Mac | **SALIN** ke rencana free-tier (fallback bila 9router/Gemini gagal) |
| OpenRouter `:free` (50 req/hari, no CC) | sama | **SALIN** |
| TokenRouter $5 free / ZenMux | sama | **SALIN** sebagai cadangan ke-3 |
| Fugu TRINITY / Teamwork / CRDT (multi-agent OSS) | luar thread konten (untuk cc-acehtengah) | **DILOKASIKAN** ke proyek induk, bukan thread ini |
| LibreChat + docker-compose.free-tier (4 GB RAM) | butuh Docker | **DILOKASIKAN** (tidak di Mac ini; hanya bila Docker diinstalnya nanti) |
| Netlify 300 credit / Cloud Run free | hosting | → FASE 4 (Fase hosting opsional) |
| WeatherNext free / GitDiagram / GitReverse / Mermaid | pendukung | **PILIH** sesuai kebutuhan konten (mis. konten Pemdi) |
| WAHA (WA gateway self-host) | Docker | DILOKASIKAN |
| WebLLM (in-browser LLM) | jalan di browser Mac (CPU 16 GB) | **BOLEH** untuk demo/isi konten (bukan untuk agen) |

---

## 2. Daftar Unduhan Wajib (semua gratis, CPU-only, sesuai spek)

| # | Item | Cara | Ukuran | Kapan |
|---|---|---|---|---|
| U1 | Voice Piper `id_ID-news_tts-medium` | `~/src/hermes-agent/.venv/bin/python3 -m piper.download_voices id_ID-news_tts-medium` | ~63 MB | FASE 2, saat load < 3 |
| U2 | faster-whisper (model `small` ID) | `uv tool install faster-whisper` | ~150–500 MB | FASE 2, saat load < 3 |
| U3 | relokasi `ggml-medium.bin` (whisper.cpp, sudah diunduh 1.4 GB di `/tmp`) | `mv /tmp/ggml-medium.bin ~/models/whisper/` | 0 (reklo) | FASE 2 |
| U4 | trivy, semgrep, osv-scanner, bandit, lizard | `brew install trivy semgrep osv-scanner; uv tool install bandit lizard` | ~100–300 MB | FASE 3 (code-audit) |
| U5 | Auto-Editor | `npx auto-editor` (JIT, npm) | kecil | FASE 2 |
| U6 | DeepFilterNet (denoise) | `uv tool install deepfilternet` | ~50 MB | opsional FASE 2 |

**Total unduhan baru: ±0,5–1 GB** → aman untuk disk 21 GB free. **Aturan beban:** semua unduhan
diserukan **berurutan, satu-satu, saat load avg < 3** (load sekarang 5,7 → jangan langsung).

---

## 3. Mitigasi & Dampak (per risiko nyata di Mac ini)

| Risiko | Dampak | Mitigasi (spesifik) |
|---|---|---|
| RAM 16 GB tanpa headroom → model CPU + gateway bersamaan = swap/lumpuh | Telegram gateway melambat / crash | **Aturan beban**: proses CPU berat (whisper/piper/semgrep) hanya saat load < 3 & **satu-satu**. Cron dijadwalkan malam (radar 07:00 sudah pagi-pagi; QA 13:00 ringan; unduhan = manual, pagi kerja) |
| VRAM 2 GB → model GPU di paket di-"install" juga tidak bisa jalan | frustrasi: unduh, tidak jalan | **Eliminasi dari rencana** (bukan tunda): semua entri GPU di §1.3 C/D ditandai ❌ sejak awal. Dokumen ini = satu-satunya sumber |
| Tanpa Docker → Postiz/n8n/ComfyUI/LibreChat dari paket tak bisa lokal | jalur "publish otomatis" tidak ada | **Modus manual** (status thread hari ini = konten "siap posting", unggah manual). Opsi Cloud Run (FASE 4) baru bila disetujui |
| Piper voice belum ada → cadangan TTS kosong | Gemini habis = tidak ada VO | U1 (63 MB) wajib di-FASE 2; edge-tts (sudah di venv) = cadangan online; Gemini = utama |
| code-audit tanpa trivy/semgrep → laporan 50% SKIPPED | laporan klien tak lengkap → harga rendah | U4 (brew, CPU, gratis) di FASE 3 |
| Skill bank disentuh langsung → divergensi target `~/.hermes/skills` | skill "hilang" pasca sync | Salin **hanya** ke bank pusat `~/Desktop/Niumination/skills/content/` → `sync-to-agents.sh` + `skill-manifest.py --check` (one-home rule, sesuai memori) |
| Config di-edit saat ada repair (insiden 27 Agu) | gateway rusak | Cek `docs/reports/ECOSYSTEM-STATUS-*` sebelum sentuh config; backup `config.yaml.bak-*`; restart gateway dari shell terpisah |
| Repo dirty di-commit blind (insiden 16 Sep) | kredensial bocor | commit selektif + gate `secret-scan-staged.py` (`.githooks/pre-commit`) — hanya `docs/reports/` + `scripts/` yang di-add |
| Beban & unduhan saingi proses yang sedang berjalan (Mac "kerja berat") | hasil korup / timeout | Semua FASE 2/3 dikerjakan saat load < 3; unduhan dijadwalkan di jam kerja Anda, bukan cron |
| Niche paket = Vibe Coding, thread = Kreator Niumination | template tak "klik" | Tulis ulang `BRAND.md` (BUKTI = data ekosistem Anda), fokus niche = layanan publik/OSS/lokal; Rules Pack tetap bisa dipakai untuk klien OSS Pemdi |
| Free-tier Gemini / 9router berubah/mati | VO & LLM utama hilang | Cadangan berjenjang: Gemini → edge-tts/Piper (CPU) · 9router → OpenRouter :free / OrcaRouter / TokenRouter (dari paket riset-eco, semua no-CC) |

---

## 4. Urutan Fase (TERTAHAN, bukti per tahap)

**FASE 1 — Kerangka ($0, tanpa unduh)**
1. 8 skill → bank pusat `skills/content/` + register manifest + `sync-to-agents.sh`
2. 5 bundle → `~/.hermes/skill-bundles/` + `hermes bundles reload`
3. Tulis ulang `BRAND.md` (niche = Konten Kreator Niumination, BUKTI dari data ekosistem)
4. 7 QA gate + state machine + `LEDGER/CONTENT_INDEX` → `workspace/` thread
5. Template (19+6) + Rules Pack → `workspace/templates-local/`
6. Tambah skill `content-studio` ke `channel_skill_bindings` thread 1172 (config, backup dulu)
- **Bukti:** manifest SHA-256 8 skill baru, `bundles list` menunjukkan 5, `workspace/BRAND.md` tanpa `{{}}`

**FASE 2 — Voice & Caption (CPU, saat load < 3)**
- U1 (Piper 63 MB) + U2 (faster-whisper) + U3 (relokasi ggml-medium) + U5 (Auto-Editor JIT)
- Uji wajib: `uji.wav` Piper vs `periksa_vo.py` sebelum render penuh
- **Bukti:** file terunduh + keluaran `uji.wav` + transkrip kontrol

**FASE 3 — code-audit 100%**
- U4 (brew: trivy/semgrep/osv-scanner + uv: bandit/lizard/pip-audit)
- **Bukti:** 1 audit repo contoh (mis. `apps/niu-dash`) menghasilkan `AUDIT_REPORT.md` 7 bagian + skor kesehatan + 3 temuan dianonim

**FASE 4 — Hosting free (opsional, TUNDA)**
- Postiz/Ghost di Cloud Run/Netlify (dari paket riset-eco) → baru bila FASE 1–3 terbukti

---

## 5. Keputusan Approval (eksekusi TERTAHAN)

- **(a)** FASE 1 — salin 8 skill + 5 bundle + BRAND.md + QA gate + binding 1172? *(menyentuh skill bank & config → wajib eksplisit)*
- **(b)** FASE 2 — unduh U1–U3, U5 (total ±0,5–1 GB, CPU, gratis) saat Mac idle?
- **(c)** FASE 3 — unduh U4 (brew/uv, ±100–300 MB) untuk code-audit 100%?
- **(d)** FASE 4 — hosting free (Cloud Run/Netlify)? Tunda / langsung?
- **(e)** commit 1 file dirty `scripts/provider-health-check.sh` di root (menghambat `up-eco`)?

---

## 6. Bukti Inspeksi (tanpa eksekusi, tanpa mengubah apa pun)

- **Mesin:** i5-10310U x86_64 · 16 GB RAM · UHD 620 (VRAM 2 GB) · disk 21 GB free · load 5,7 · **tanpa Docker**
- **Siap:** ffmpeg (9 filter yang dibutuhkan ✅) · magick · node 26 · OBS · gh · gitleaks · **piper & edge-tts & onnxruntime di venv hermes** · 9router 108 model (2 label free: `gh/gpt-5.4-mini-free-auto`, `gh/gpt-5.6-luna-free-auto`)
- **Paket:** 28 item (studio) + 6 item (riset-eco) dibaca penuh — skill, bundle, config-snippet, 7 docs, 5 script, template, BRAND.md seed, proyek contoh
- **Belum disentuh:** tidak ada skill/config/tool/commit. Hanya inspeksi + dokumen rencana ini (`69d3488` → versi v3)

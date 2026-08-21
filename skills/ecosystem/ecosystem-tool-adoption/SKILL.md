---
name: ecosystem-tool-adoption
description: Workflow studi & adopsi tool/proyek pihak ketiga ke ekosistem Niumination — deep study (clone + baca source), gap analysis terukur, rencana bertahap di docs/architecture/, persetujuan user via clarify, eksekusi non-destruktif. Trigger saat user kirim URL repo/tool + "pelajari ini".
tags: [ecosystem, research, adoption, planning, niumination]
last_updated: "2026-08-17"
version: 1.1.0
changes:
  - v1.1: Added explicit autoskills adoption workflow (license check, review status, flag patterns)
  - Added: MC redesign v3 status update (Phase 0+1 complete)
  - Noted: 6 overlapping skill-bank-* skills need curator consolidation
---

# 🧰 Ecosystem Tool Adoption — Studi & Adopsi Tool Pihak Ketiga

## Trigger
User kirim URL repo/tool + **"pelajari ini"** / **"pelajari dulu untuk diterapkan di ekosistem"** (contoh nyata: autoskills, 9drive, OpenRouter, Motion.so, UACC, Munder Difflin). **Varian dokumen (18-Ags-2026):** user kirim file .md hasil kajian eksternal (analisis + research report) + "pelajari ini" — perlakukan sama: pelajari, verifikasi klaim terhadap kondisi aktual, lalu LAPORKAN + tunggu instruksi. **Varian paket zip (18-Ags-2026):** user kirim `Downloads/<name>.zip` berisi paket rebuild/optimisasi + "pelajari ini" — extract ke `/tmp/<name>-study/`, baca urutan: README → dokumen audit utama → semua script/config/prompt (jangan lewat file pendukung), lalu verifikasi klaim terhadap sistem aktual (config.yaml, proses, port, path) dan laporkan isi + delta antar versi.

## Aturan keras (user preference, berlaku semua task)
- **"pelajari ini" = study + lapor + tunggu instruksi. JANGAN eksekusi apa pun** (fix, config, install, restart) sampai user bilang "gas/kerjakan/fix". User marah keras saat agent langsung mengerjakan yang tidak diminta: "kamu gak perlu kerjain apapun kalau aku gak minta".
- **"periksa/cek/pastikan X" = probe langsung + laporan ringkas.** Bukan rekap sejarah, bukan wall-of-text, bukan dokumen baru. Tawarkan fix satu baris ("mau saya fix?"), jangan eksekusi.
- **Data valid dari filesystem** (config.yaml.bak.*, changelog, git log, output tool), bukan rekonstruksi memory/session. User: "aku selalu menginginkan data valid bukan rekayasa/kebodohan kamu".
- **Paket versi berlapis: SELALU cek ERRATA/dokumen supersede dulu.** Paket v2 bisa **menarik rekomendasi v1 secara eksplisit** (contoh nyata `niumination-rebuild-v2.zip` → `ERRATA-AUDIT-V1.md` menarik fallback 9router/juan/huancheng + multi-agen dari rekomendasi v1). Saat user kirim v2 setelah v1: baca README + errata PERTAMA, laporkan "yang ditarik vs yang tetap", dan JANGAN pernah menerapkan rekomendasi yang sudah ditarik (mis. jangan re-add 9router ke fallback_providers padahal kebijakan v2 bilang otak hanya keluarga opencode-zen).
- **"simpan dulu jadi referensi" = copy ke `docs/references/<nama-bermakna>-<YYYY-MM-DD>/`** (untuk paket multi-file: extract folder penuh; untuk dokumen tunggal: file .md), lalu commit+push bersama snapshot hari itu. Jangan ubah isi.

## Workflow

### Step 1: Deep study (bukan skimming)
1. `web_extract` halaman utama + README GitHub (fitur, arsitektur, lisensi)
2. **Clone repo** ke /tmp (`git clone --depth 1`) — baca kode inti, bukan cuma README:
   - `wc -l` file untuk tahu mana yang penting; baca entry/main file + logika inti + security model
3. Catat: stack, lisensi (⚠️ CC BY-NC / non-komersial = pola boleh diadopsi, kode jangan disalin untuk produk komersial), model keamanan, pola yang belum dimiliki ekosistem

### Step 2: Gap analysis terukur
- Bandingkan dengan kondisi ekosistem SEKARANG — ukur: jumlah file, baris script, struktur (contoh: `find skills -name SKILL.md | wc -l`, `du -sh`)
- Tiap gap: bukti konkret (path file, nomor baris, angka) — bukan asumsi
- Tandai gap "paling berharga" = yang menyelesaikan masalah nyata yang ADA (bukan potensial)

### Step 3: Rencana detail → dokumen dulu (preferensi user!)
User memilih **"Buat rencana detail dulu sebagai dokumen"** (16-Ags-2026) untuk kerja multi-fase — JANGAN langsung eksekusi.
- Lokasi: `~/Desktop/Niumination/docs/architecture/<tool>-adoption.md` (repo ecosystem-config)
- Struktur dokumen: ringkasan eksekutif → latar belakang → gap analysis (tabel) → fase (spesifikasi teknis + kriteria sukses per fase) → prioritas/timeline → risiko & mitigasi → Definition of Done → lampiran
- **Commit dokumen dulu** (`git add` + commit) sebelum menawarkan eksekusi

### Step 4: Persetujuan (clarify)
Tawarkan opsi: gas semua / fase prioritas / buat dokumen dulu. Hormati pilihan user — jangan eksekusi tanpa persetujuan.

### Step 5: Eksekusi
- Non-destruktif, reversible, verifikasi nyata sebelum klaim selesai (diff -r, exit code, output command — bukan narasi)
- DoD harus bisa dibuktikan; audit = saran saja, bukan mutasi data (aturan user)

## Konteks aktif (2026-08-16)

### Rekonstruksi ekosistem v2 (18-Ags-2026) — kebijakan model BERUBAH, jangan pakai rekomendasi v1
User sedang merekonstruksi ekosistem (kinerja model lemah merusak state). Paket `niumination-rebuild-v2.zip` = kebijakan SAAT INI; `AUDIT-REKONSTRUKSI-...md` (v1) = observasi snapshot saja, rekomendasi arsitekturnya **ditarik oleh `ERRATA-AUDIT-V1.md`**. Poin yang ditarik dan TIDAK boleh diterapkan:
- ❌ Fallback ke 9router/juan/huancheng/gemini/gratislonggar — **mesin cacat** (model beda keluarga lanjut tugas = state kacau)
- ❌ Multi-agen runtime (4 karakter + orchestrator + Ultra) — dormant/arsip sampai core hijau 14 hari
- ❌ Bind 5 thread Telegram ke 5 model beda — semua thread harus `opencode-zen/nemotron-3-ultra-free` (cadangan se-keluarga: `hy3-free` / `nemotron-3.5-lightning-free`), via `/model` manual bukan silent hop
- ❌ Auxiliary compression ke model asing — compression harus keluarga Zen

Yang TETAP berlaku: pin cron `c6ec80ed633f` ke opencode-zen/nemotron-3-ultra-free, `model_drift_guard: true` (JANGAN false), no-Docker MC di 16 GB, no `telegram_router`, RTK tetap enabled, vault tertutup, NTFS `/Volumes/Niumination` jebakan, Jcode optional.

Arsitektur v2: `core/` (CONSTITUTION 12 hukum, MODEL.policy, FREEZE.list, STATE.yaml, ledger) + plugin/hook `niu-core-fence` (pre_tool_call block file beku, pre_llm_call deteksi model asing, on_session_end ledger) + scripts `niu_corelib.py`/`niu-handoff.py`/`niu-doc-capture.py`/`niu-seal-core.sh` + `AGENTS.md` slim ≤2 KB. Semua tersimpan di `docs/references/niumination-rebuild-2026-08-18/` (v1; v2 masih di Downloads, belum di-commit ke referensi).

### autoskills (midudev, 6.8k⭐, CC BY-NC) — 7/11 skill diadopsi
Dokumen: `docs/architecture/autoskills-pattern-adoption.md` (committed 37e0c58).

**Adopsi skill dari autoskills registry — workflow:**
1. Baca `skills-registry/index.json` → cek per skill: `review.status` (approved/flagged) + `flags[]` + `license` di SKILL.md
2. **SKIP jika**: flagged (python-executor: broad exec, raw install link), NO-LICENSE (python-patterns), tidak relevan
3. **Copy** folder ke `skills/<domain>/<skill>/` (ikutkan references/ jika ada)
4. **Frontmatter**: tambah `license:` + `source: autoskills registry — <repo>` + `metadata.version:`
5. **Update** INDEX.md (baris tabel + counter "Status: N ✅ Aktif")
6. Regenerate manifest + sync + verify 3 target + commit+push

**Yang sudah diadopsi (7):**
- ✅ accessibility (MIT, addyosmani) — WCAG 2.2
- ✅ frontend-design (Apache-2.0, anthropics) — anti-AI-slop
- ✅ seo (MIT, addyosmani) — technical SEO
- ✅ python-testing-patterns (MIT, wshobson)
- ✅ fastapi-templates (MIT, wshobson)
- ✅ fastapi-python (Apache-2.0, mindrally)
- ✅ flask-api-development (MIT, aj-geddes)

**Yang di-skip (4):**
- 🚫 python-patterns — NO-LICENSE (affaan-m repo)
- 🚫 python-executor — flagged: broad exec + raw GitHub install link
- 🔻 machine-learning, pandas-data-analysis — tidak relevan MC/Pemdi

**Bug kritis ditemukan & diperbaiki:** `sync-to-agents.sh` hanya copy SKILL.md → 8 skill terpotong. Fix: rsync -a -u SELURUH folder + verify hash + lockfile. Skill-bank-management skill punya prosedur lengkap.

**MC Redesign v3**: Backend Phase 0-4,6-8 SELESAI + Phase 5A (migrate backend logic → v3 routers: tasks, agents, cost, ecosystem). **Phase 5B-5C (frontend visual + L3 Inspector) BELUM** — L0-L3 views belum dikerjakan, tampilan masih dashboard lama. ⌘K palette + WCAG fixes ditambah ke dashboard LAMA, bukan redesign visual. Lesson penting: **jangan klaim "X/X items complete" tanpa verifikasi visual actual** — backend selesai ≠ frontend selesai. Detail: `docs/REDESIGN_V3_BREAKDOWN.md` + `docs/PHASE5_PLAN.md` + skill `niu-mission-control-ui`

### Camoufox (daijro, MIT) — terinstall & terintegrasi
Anti-detect Firefox built untuk AI agents. Playwright-based, auto-fingerprint (OS, CPU, fonts, WebGL, navigator).
- **Install global:** `pip3 install --break-system-packages camoufox && python3 -m camoufox fetch`
- **Install Hermes venv:** `/Users/zaryu/.hermes-portable/venv/bin/pip install camoufox` (shared cache ~/.cache/camoufox)
- **Config Hermes:** `config.yaml` → `browser.engine: local` + `browser.camofox.managed_persistence: true`
- **Verifikasi:** `navigator.webdriver = false` (anti-detect), `AsyncCamoufox(headless=True)` berhasil launch
- **Use case:** anti-detect scraping, comp research, login flows butuh fingerprint real
- **Bukan** pengganti cua-driver (desktop automation); ini untuk browser automation
- **Browser binary:** v152.0.4-beta.28 (official/stable), ~1.2GB, shared cache

### 9drive (zenhosta, 1.7k⭐) — studi selesai, belum ada keputusan
Storage gateway multi Google Drive + S3 (Express+TS, React+Vite, MySQL+Prisma).
- File upload di-stream LANGSUNG ke provider — 0 byte di server; lokal hanya metadata (MySQL) + source (~700KB + node_modules)
- Routing: `most_available` (sort availableBytes desc, S3 diutamakan saat quota null), `round_robin` (cursor di DB), `priority` (list id); quota sync LAZY (hanya stale >5 menit, Promise.allSettled); reservedBytes anti-overcommit batch upload
- Bisa deploy remote total (VPS + Docker). Alternatif lebih ringan untuk backup biasa: `rclone` (tanpa server/MySQL/DB)
- Insight: pola `most_available` + lazy quota sync bisa diterapkan di dispatch Mission Control (routing multi-provider)

### OpenRouter (free tier)
Key tersimpan `~/.config/openrouter/env` (chmod 600). Detail lengkap: skill `hermes-provider-config` → `references/openrouter-free-tier.md` (sudah ter-capture 16-Ags-2026).

### SerpApi / barehands / ai-memory-vault (18-Ags-2026) — studi selesai, disimpan referensi
- **SerpApi** (serpapi.com, berbayar) — 80+ API search engine + MCP integration. **Defer**: Hermes sudah punya `web_search` + `TAVILY_API_KEY` di .env (gratis). Tidak ada key SerpApi.
- **barehands** (jaredrhod, 214⭐, **AGPL-3.0-or-later**) — webcam hand-tracked board utk AI (localhost:8794, Python stdlib-only, MediaPipe+three.js CDN, `bin/board.sh`=tangan AI, `bin/board-state.sh`=mata AI, Obsidian vault bisa jadi orbs). **Defer** (satelit/eksperimen setelah core hijau). AGPL: jangan vendor ke produk closed-source; jalankan sebagai proses terpisah.
- **ai-memory-vault** (jaredrhod, 525⭐, **CC BY-SA 4.0**) — Obsidian jadi working memory AI tanpa vector DB. 4 template: CLAUDE.md (boot config/identity, survive compaction), VAULT-INDEX.md (operating manual), DAILY-NOTE.md, MEMORY.md (redirect native memory). Konsep kunci: **AI Priming** (agent baca notes relevan SEBELUM output) + master note per recurring job. **Adopsi konsep**: pola sama dgn `brain/` + `~/.hermes/memories/` + rebuild v2 (SOUL/USER/STATE); AI Priming = upgrade berikutnya setelah core hijau.
- Referensi: `docs/references/serpapi-barehands-memoryvault-2026-08-18.md` + `docs/references/audit-model-provider-2026-08-18.md` (rekomendasi fallback saat Zen 429 — BELUM diterapkan, tunggu instruksi).

## Catatan curation
- `up-eco` skill = manually authored (created_by=None) — curator REFUSE patch langsung. Backport perubahan ke sumber Bank Pusat: `~/Desktop/Niumination/skills/ecosystem/up-eco/SKILL.md`, lalu tunggu sync 6h (atau jalankan `sync-to-agents.sh`).
- **6 overlapping skill-bank-* skills** terdeteksi: skill-bank-integrity, skill-bank-maintenance, skill-bank-management, skill-bank-operations, skill-bank-ops, skill-bank-sync. Semua menangani topik serupa (manifest SHA-256 + sync + drift). Perlu konsolidasi oleh curator ke 1 umbrella skill. `skill-bank-management` memiliki coverage terlengkap (adopt + verify + drift).

## Related
- `up-eco` — status & sync ekosistem (baca status, jangan patch langsung)
- `hermes-provider-config` — provider config & OpenRouter free tier
- `project-foundation` — standar dokumen proyek (PRD/Tech Spec)

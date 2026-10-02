# Riset Remotion — Adaptasi ke Ekosistem Niumination

**Tanggal:** 2 Oktober 2026 · **Status:** STUDY — menunggu keputusan pemilik
**Sumber utama:** remotion.dev/docs, github.com/remotion-dev/remotion, hyperframes.heygen.com/guides/hyperframes-vs-remotion, getmasset.com/resources/blog/hyperframes-vs-remotion-review

---

## 1. Apa itu Remotion

Framework video berbasis React + TypeScript. Membuat video via kode: komponen React yang merender per frame, di-compile JIT, dirender headless Chrome + FFmpeg menjadi MP4. Ekosistemnya punya:

- **Agent Skills** (`npx remotion skills add`) — integrasi Claude Code / Codex / Kimi / OpenCode, prompt langsung jadi video
- **Templates** (Hello World, Prompt-to-Video, AI SaaS)
- **Remotion Studio** (preview browser)
- **Cloud Lambda rendering**
- **Bolt.new / ChatGPT plugin** integration

---

## 2. Lisensi — titik keputusan krusial

| Tier | Harga | Coverage |
|------|-------|----------|
| Free | $0 | Individu, ≤ 3 orang, semua fitur |
| Individual | **$25/bulan/orang** | Agentic coding (AI buat video) |
| Company | **$100/bulan** | 3–10 orang |

**Implikasi Niumination:** organisasi >3 orang (Afrizal + tim cc-acehtengah + potensi klien) → harus bayar. Harga berbeda dari HyperFrames (Apache 2.0, gratis tanpa batas tim) dan Revideo (MIT).

---

## 3. Perbandingan dengan stack kita saat ini

| Aspek | Remotion | HyperFrames (ADA di bank skill) | Revideo (ada di content-produce) |
|-------|----------|--------------------------------|----------------------------------|
| Bahan tulis | React + TypeScript | HTML + CSS + JS | TypeScript (Motion Canvas) |
| Build step | Wajib (bundler) | **Tidak ada** | JIT via npx |
| Lisensi | Free ≤3 org, berbayar di atasnya | **Apache 2.0 gratis** | MIT |
| Built for | React developer | **AI agents** | Motion graphic |
| Render | Headless Chrome + FFmpeg | Headless Chrome + FFmpeg | npx revideo render |
| Kebutuhan mesin | macOS 15+, Node 16+, JIT CPU berat | Node ≥22, FFmpeg, Chromium | npx, CPU ringan |
| Agent Skills | ✅ resmi | ✅ adapters (GSAP, CSS, WAAPI) | ❌ (manual template) |

---

## 4. Kesesuaian dengan spesifikasi Mac ini (i5-10310U · 16 GB · UHD 620 · tanpa Docker)

| Faktor | Evaluasi |
|--------|----------|
| macOS 15+ | ✅ macOS 26.5 terpasang |
| JIT compilation CPU | ⚠️ berat — render video bisa capai 5–15 menit per video |
| RAM 16 GB | ⚠️ Chromium + FFmpeg + Node = aman hanya 1 render sekaligus |
| Tanpa GPU | ✅ headless Chrome jalan di CPU (lambat tapi jalan) |
| Tanpa Docker | ✅ Remotion install npm biasa |
| Lisensi tim | ❌ $25/bulan/orang × 3+ = $75+/bulan — tidak gratis |
| Agent Skills | ✅ klaim utama — prompt coding agent → video |

---

## 5. Rekomendasi adaptasi

**Opsi A — Pakai Remotion Agent Skills (jika pemilik mau bayar lisensi):**
- `npx create-video@latest --blank my-video && cd my-video && npx remotion skills add`
- Agent (Claude Code / OpenCode) tulis komponen React + prompt deskripsi video
- Cocok untuk: prompt-to-video, motion graphics kompleks, template reusable
- Risiko: JIT render lambat di CPU, lisensi berlanjut

**Opsi B — Tetap HyperFrames + Revideo (REKOMENDASI — hemat, gratis, sesuai spek):**
- HyperFrames untuk HTML-based video (sesuai skill `content-produce` existing)
- Revideo untuk motion graphic template (sudah direncanana FASE 2)
- Agent Skills adapter custom di `skills/content/content-produce/` — prompt "buat HTML-nya dulu, lalu render via HyperFrames"
- Nol biaya lisensi, zero build step, Apache 2.0/MIT

**Opsi C — Hybrid (bila pemilik ingin eksperimen):**
- Remotion install di `sandbox/` (luar ekosistem utama, sesuai aturan HyperFrames pitfall)
- Render test per proyek, ukur waktu + kualitas vs HyperFrames
- Keputusan final setelah 3× uji banding

---

## 6. Yang perlu diputuskan pemilik

1. **Lisensi:** mau bayar $25+/bulan untuk Agent Skills Remotion, atau tetap gratis?
2. **Prioritas:** Agent Skills (prompt→video otomatis) lebih penting daripada template React?
3. **Volume render:** render jarang (1–2/bulan) → HyperFrames cukup; render rutin → perlu Optimasi (Revideo batch)
4. **Opsi C hybrid:** izin install di `sandbox/` untuk uji banding?

---

## Bukti

- `web_search` remotion.dev/docs → lisensi FAQ page terdeteksi: "$25/month per person who writes Remotion code themselves or using agentic coding tools"
- `web_search` hyperframes-vs-remotion → tabel perbandingan Masset: HyperFrames Apache 2.0 gratis tanpa batas tim vs Remotion free ≤3 org
- `web_extract` remotion.dev/docs/ai → Agent Skills docs: `npx remotion skills add`, supported agents Claude/Codex/Kimi/OpenCode
- `read_file` skills/creative/hyperframes/SKILL.md → verified pitfall "JANGAN init project di dalam ekosistem Niumination"
- `read_file` skills/content/content-produce/SKILL.md → jalur Revideo/Motion Canvas sudah terdaftar sebagai opsi Mode A (tanpa GPU)
- `read_file` docs/reports/RENCANA-ADOPSI-CONTENT-STUDIO-2026-09-20.md → spesifikasi Mac: i5-10310U, 16 GB, UHD 620, tanpa Docker
- `search_files` pattern=remotion di ~/Desktop/Niumination → 0 file Remotion di ekosistem (hanya 5 referensi kasus-insensitive di docs/references dan skills/creative/hyperframes)

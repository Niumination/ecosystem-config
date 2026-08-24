# Third-Party Tool Integration Assessment

Ketika user bertanya **"pelajari repo/tool X ini — bisa diintegrasi ke ekosistem?"**, gunakan framework ini untuk riset + evaluasi.

## Workflow

### 1. Ekstrak Repo Info

```bash
web_extract(urls=["https://github.com/<owner>/<repo>"])
```

Baca README lengkap — fokus ke:
- **Tagline & purpose** — apa yang tool ini lakukan
- **Architecture** — sensors → models → tools (atau pattern serupa)
- **Stack** — bahasa, framework, runtime dependencies
- **License** — GPL/AGPL punya implikasi linking
- **Current release** — versi + tanggal, maturity signal
- **Stars/forks/commits** — community adoption signal

### 2. Petakan ke Ekosistem Saat Ini

Buat tabel integrasi potensial vs hambatan:

| Area | Bisa? | Cara |
|------|-------|------|
| **Notifikasi** | ✅/⚠️/❌ | Spesifik mekanisme |
| **Monitoring** | ✅/⚠️/❌ | Spesifik mekanisme |
| **Data source** | ✅/⚠️/❌ | Spesifik mekanisme |
| **Orkestrasi** | ✅/⚠️/❌ | Spesifik mekanisme |
| **Overlap** | — | Apakah fungsinya sudah ada di ekosistem? |

### 3. Identifikasi Kendala

| Aspek | Catatan |
|-------|---------|
| **License** | AGPL/GPL = hati-hati linking. Komunikasi API/proses terpisah aman |
| **Stack compatibility** | TypeScript/Rust cocok dgn Next.js. Python perlu bridge |
| **Deployment model** | Desktop app vs web service vs library |
| **Overlap dgn existing** | Hermes Agent, herdr, atau tool lain yang sudah ada |

### 4. Rekomendasi Akhir

Tiga kemungkinan:
- **✅ Bisa diintegrasi sebagai X** — spesifik peran dalam ekosistem
- **⚠️ Bisa tapi terbatas** — perlu bridging atau workaround
- **❌ Tidak cocok untuk di-merge** — alasan jelas (stack, license, overlap)

State kapan tool dipakai sebagai **lapisan terpisah** (komunikasi via API/webhook) vs **library langsung** (import kode).

## Contoh: Observer AI Assessment

### Hasil Riset
- TypeScript + Rust + Python stack
- Desktop/local agent runner: screen → LLM → tools
- AGPL-3.0 license
- Tools: Telegram, Email, SMS, WhatsApp, Discord, notifikasi

### Peta Integrasi

| Area | Kemungkinan |
|------|-------------|
| **Notifikasi build** | ✅ Observer pantau terminal → kirim Telegram kalau build fail |
| **Monitor dev server** | ✅ Observer ping localhost:3000 — alert kalau down |
| **Timeline data source** | ✅ Observer log aktivitas coding → API pull ke dashboard |
| **Trigger herdr agents** | ✅ Observer detect event → API call ke herdr agent |

### Kendala
- ⚠️ **AGPL-3.0** — kalau di-link langsung ke kode, seluruh proyek harus AGPL. Tapi API-based aman.
- ⚠️ **Desktop app** — bukan web service, jalan di background Mac/Windows/Linux — perlu instalasi terpisah
- ⚠️ **Overlap** — Observer dan Hermes Agent sama-sama local AI agent. Perlu batasi peran: Observer = sensor layer, Hermes = reasoning layer.

### Rekomendasi
✅ **Bisa sebagai "sensor layer" terpisah** — bukan di-merge ke kode niu-dash-fullstack. Install Observer Desktop App, buat agent yang monitor terminal/build. Komunikasi via webhook/API, bukan linking langsung.

## Blueprint Documentation Workflow

Setelah assessment selesai dan user setuju untuk lanjut, **jangan hanya simpan assessment** — buat blueprint dokumentasi lengkap dengan format terstruktur seperti migration docs:

### Blueprint Document Structure

```
docs/<tool-name>-ecosystem-integration/
├── README.md               — Gambaran besar, tujuan, risiko, struktur dokumen
├── 01-overview.md          — Arsitektur tool, cara kerja, fitur utama
├── 02-integration-points.md — Titik integrasi dengan ekosistem (dengan tabel matriks)
├── 03-agent-blueprints.md  — Blueprint agent/workflow siap pakai (contoh system prompt, code)
├── 04-roadmap.md           — Tahapan implementasi (P0-P4/🔴🟡🟢)
└── 05-risks-notes.md       — Lisensi, alternatif, arsitektur, perbandingan
```

### Rules per Section

| Section | Key Content |
|---------|-------------|
| **README.md** | One-paragraph summary, why-this-tool-over-existing, risk table (🔴/🟡/🟢), document index, status line (BELUM dieksekusi) |
| **01-overview.md** | Architecture diagram (ASCII), sensor→model→tools pipeline, all system prompt variables, all tools/functions, deployment options table, recommended option |
| **02-integration-points.md** | Matrix table (every integration with priority), detailed diagram for each integration (ASCII), data flow diagram showing observer↔ekosistem↔dashboard |
| **03-agent-blueprints.md** | Per-agent: Tujuan, System Prompt lengkap (copy-paste ready), Code Tab lengkap (JavaScript), Trigger config (sensor + interval), Priority order for implementation |
| **04-roadmap.md** | Phased timeline (P0 prerequisites, Pn implementation phases), concrete step-by-step per phase, verification steps per phase, timeline estimate |
| **05-risks-notes.md** | License analysis table (skenario + risiko level), alternative tools comparison, technical risks (permissions, performance, false positives, resources), ecosystem role table (Hermes vs Observer vs Herdr vs Dashboard), communication architecture (recommended + future options) |

### Implementation Notes

- **Ikuti format migration-portable-to-native docs** — konsistensi dokumentasi lebih penting dari kreativitas format
- **Doc path:** `docs/<tool-name>-ecosystem-integration/` di root Niumination
- **Sections are numbered** (01-, 02-, etc.) untuk urutan baca yang jelas
- **Status line** di README: `🔄 **Status:** Blueprint — BELUM dieksekusi`
- **Priority order implementation** di 03-agent-blueprints.md — selalu grouping 🔴 → 🟡 → 🟢
- **Jangan merge blueprint ke kanban** — simpan sebagai dokumentasi. User akan minta di-kanban-kan nanti jika perlu.

### When to Use

Flow lengkap: User bilang "pelajari tool X ini" → lakukan assessment (step 1-4 di atas) → presentasi ke user → jika user bilang "buat dokumentasi dan simpan untuk dikerjakan nanti" → bikin blueprint docs dengan struktur di atas.

## Checklist Setiap Evaluasi

- [ ] Read full README
- [ ] Check license compatibility
- [ ] Identify stack overlap
- [ ] Map integration points
- [ ] Check for existing ecosystem overlap
- [ ] Recommend merge/API-bridge/skip
- [ ] Save findings as reference (file ini) + update memory
- [ ] If user says "buat dokumentasi": create blueprint docs (Blueprint Documentation Workflow above)

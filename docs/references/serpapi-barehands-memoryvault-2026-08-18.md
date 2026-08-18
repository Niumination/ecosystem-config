# Analisis — SerpApi + barehands + ai-memory-vault

| Field | Nilai |
|---|---|
| **Tanggal** | 18 Agustus 2026 |
| **Sumber** | https://serpapi.com/ · https://github.com/jaredrhod/barehands · https://github.com/jaredrhod/ai-memory-vault |
| **Status** | Referensi — belum diterapkan |

---

## 1. SerpApi — Google Search API

**Jenis:** Layanan komersial (API berbayar) — scrape Google + 80+ search engine.

### Kapabilitas
- **Google Search API** (utama): query → JSON terstruktur (organic results, ads, knowledge graph, related questions)
- 80+ API: Google Images, Maps, Flights, Hotels, Jobs, News, Trends, Scholar, Shopping, YouTube, Amazon, eBay, Bing, DuckDuckGo, Baidu, Yandex, dll.
- Fitur: X-Ray, ZeroTrace Mode, U.S. Legal Shield, Markdown Output, Pixel Position
- Integrasi: Python, JS, Go, PHP, Java, Rust, .NET, **MCP**, CLI

### Harga (perlu cek plan)
- Developer Plan: 5,000 searches/bulan, throughput 1,000/jam
- 99.95% SLA, refund 7 hari
- U.S. Legal Shield (Production+): $2M coverage

### Relevansi ke Niumination
- ✅ **MCP integration tersedia** — bisa dipasang via `hermes mcp add`
- ⚠️ **Berbayar** — user prefer free/open-source. Perlu pertimbangan budget
- ⚠️ **Tidak ada key di .env** — belum ada kredensial
- 💡 Alternatif gratis: `web_search` bawaan Hermes (sudah ada) atau Tavily (`TAVILY_API_KEY` sudah di .env!)

### Keputusan: **Opsional/defer** — Hermes sudah punya web_search + Tavily key. SerpApi hanya jika butuh data search engine terstruktur (SEO, riset pasar).

---

## 2. barehands — Hand-tracked Interface untuk AI

**Repo:** jaredrhod/barehands (214⭐, 37 fork) · **Lisensi: AGPL-3.0-or-later**
**Konsep:** Webcam → tangan → interface "glass board". Pinch, throw, stretch, force-pull kartu catatan/3D di layar. **Tubuh untuk AI** — AI bisa di-wire sebagai "otak" (ring = wajah, scripts = tangan/mata).

### Teknis
- `server.py` — Python stdlib-only (tidak ada dependency), port 8794
- `stage.html` — UI board (MediaPipe hand tracking + three.js, dari CDN)
- `bin/board.sh` — "hands" AI: POST JSON ke `/cmd` channel (localhost)
- `bin/board-state.sh` — "eyes" AI: baca state board
- `barehands.json` — config (nama, port, orbs/notes folders)
- `barehands.md` — system builder file (untuk Claude Code / agent setup)
- Obsidian vault **bisa langsung jadi orbs** (folder .md works as-is)

### Lisensi
- AGPL-3.0-or-later — boleh komersial gratis, tapi kalau di-host sebagai service/modifikasi, source harus terbuka
- **Konsekuensi:** jangan vendor code-nya ke produk closed-source; jalankan sebagai proses terpisah (service boundary) kalau dipakai

### Relevansi ke Niumination
- 🖥️ MacBookPro16,2 **punya webcam** — bisa jalan
- 💡 Cocok sebagai **visual interface eksperimen** untuk Niu-MissionControl dashboard / agent face
- ⚠️ Bukan prioritas — core sedang direkonstruksi (konstitusi v2: jangan hidupkan satelit dulu)
- ⚠️ Server localhost:8794 butuh Chrome + camera

### Keputusan: **Defer** (satelit/eksperimen). Bisa jadi demo keren setelah core hijau.

---

## 3. ai-memory-vault — Obsidian sebagai Memory AI

**Repo:** jaredrhod/ai-memory-vault (525⭐, 116 fork) · **Lisensi: CC BY-SA 4.0**
**Konsep:** Obsidian vault → **working memory** AI. Tanpa vector database, murni markdown. "Memori di luar model, tanpa batas ukuran, load on demand."

### Arsitektur (4 template)
| Template | Lokasi | Fungsi |
|---|---|---|
| `CLAUDE.md` | working directory (luar vault) | **Boot config** — identitas agent + rules yang tidak boleh lapse. Survive compaction |
| `VAULT-INDEX.md` | dalam vault | **Operating manual** — profile user + peta vault |
| `DAILY-NOTE.md` | dalam vault `01 - Daily Notes/` | Template catatan harian |
| `MEMORY.md` | `~/.claude/projects/` | Redirect memory native Claude Code → vault (hindari 2 layer drift) |

### Konsep kunci
1. **AI Priming** — agent baca catatan spesifik SEBELUM output (mis. baca copywriting notes sebelum tulis email marketing)
2. **Memori tanpa ceiling** — luar model, load per job
3. **Satu master note per recurring job** → pointer ke notes yang dibutuhkan
4. **Identity di boot file** (survive compaction), operasional di VAULT-INDEX

### Relevansi ke Niumination — SANGAT TINGGI
Ekosistem Niumination **sudah punya pola serupa**:
- `brain/` = Obsidian vault (27 MB) ✅ sudah ada
- `~/.hermes/memories/` = MEMORY.md + USER.md ✅ sudah ada
- `brain/ops/` + ledger = konsep sama dengan daily notes

**Yang bisa diadopsi:**
1. **Boot config pattern** → persis yang dilakukan paket `niumination-rebuild-v2` (SOUL.md + USER.md + STATE.yaml) — v2 sudah menerapkan konsep ini
2. **AI Priming per job** → belum ada di Niumination! Bisa: tiap task baca notes relevan dulu
3. **Master note per recurring job** → cocok untuk brain/projects/
4. **Daily note template konsisten** → brain/templates/ sudah ada, bisa disempurnakan

### Keputusan: **Adopsi konsep** — sejalan dengan rebuild v2 (SOUL/USER/STATE). Pola AI Priming + master note per job = upgrade berikutnya setelah core hijau.

---

## Ringkasan Keputusan

| Sumber | Keputusan | Prioritas |
|---|---|---|
| SerpApi | Opsional/defer — Hermes sudah punya web_search + Tavily | Rendah |
| barehands | Defer — eksperimen visual setelah core hijau (AGPL) | Rendah |
| ai-memory-vault | **Adopsi konsep** — sejalan dengan rebuild v2; AI Priming = upgrade berikutnya | Tinggi |

---

*Referensi disimpan 2026-08-18. Source clone: /tmp/barehands, /tmp/ai-memory-vault (untuk studi; tidak disalin ke repo karena lisensi AGPL/CC BY-SA perlu pertimbangan).*
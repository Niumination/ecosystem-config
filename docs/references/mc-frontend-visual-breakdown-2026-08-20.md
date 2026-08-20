# Breakdown Frontend Visual — Niu-MissionControl Dashboard

| Field | Nilai |
|---|---|
| **Tanggal** | 20 Agustus 2026 |
| **Metode** | Browser live (localhost:5200/dashboard) + DOM count + fetch route audit |
| **Status** | BACKEND ROUTERS ✅ SELESAI · FRONTEND SEBAGIAN TERISI |

---

## Ringkasan

Frontend **SUDAH punya 12 halaman + ORB overlay** dan **fetch ke semua backend router**.
Yang belum = beberapa halaman masih tipis/kosong data visual, dan satu blocker eksternal (vision model down).

---

## 1. Status Per-Halaman (verifikasi DOM 20 Ags)

| Halaman | Konten | Elemen data | Status |
|---|---|---|---|
| **DASHBOARD** | 9.3K chars | health excel 100%, cards | ✅ TERISI |
| **ECOSYSTEM** | 22.3K chars | **326 cards** (projects/git/cron) | ✅ TERISI PENUH |
| **TASK QUEUE** | 6.4K chars | **243 task cards** (kanban) | ✅ TERISI |
| **SKILL BANK** | 1.5K-19K chars | rows berubah (fetch async) | 🟡 Async — setelah refresh berisi |
| **SWARM** | 1.2K chars | 19 node/agent elemen | 🟡 Layout ada, data tipis |
| **STORAGE** | 1.2K chars | 8 elemen (disk/usb/wal) | 🟡 Ringkas |
| **TELEGRAM** | 9 pesan ter-render | ✅ TERISI (parser chat_id dari env) |
| **COST** | KPI + 12 agent + 12 model | ✅ TERISI (fallback state.db + loadCostData baru) |
| **SYSTEM** | 957 chars | 5 input/select | 🟡 Form ada, data tipis |
| **DEPLOY** | **2 cards dinamis** (Niu-Vermilion, Pemdi) | ✅ TERISI (loadDeployStatus render grid) |
| **SKILL MARKET** | 994 chars | minimal | 🟡 Ringkas |
| **TERMINAL** | 836 chars | 1 output (welcome) | 🟡 Ada, belum interactive test |

## 2. Blocker Ditemukan

~~Vision model auxiliary DOWN~~ **FIXED (20 Ags 11:54):** model `Qwen3.5-397B-A17B` (9router) 503 model_not_found.
- **Root cause:** mismatch 3 arah — provider=9router tapi base_url=api.hcnsec.cn (huancheng) + key huancheng.
- **Fix:** model → `gemini/gemini-3.7-flash`, base_url → `http://localhost:20128/v1`, key → `${NINE_ROUTER_API_KEY}` (via hermes config set + restart gateway).
- **Terverifikasi:** browser_vision sukses (41.46s, 2226 chars) — dark sci-fi dashboard, ORB 3D, 13 modul, widget SYSTEM/ROUTINES/AGENTS. Log: `using custom (gemini/gemini-3.7-flash)`.

## 3. Data Flow (sudah benar)

```
app.js fetch → /api/mc/{system, tasks, agents, config, hermes, ecosystem, skills, deploy, ws}
              ↓
            render ke 12 page sections (index.html)
```

Semua route yang dipanggil frontend SUDAH ada di server.py (terverifikasi openapi: 48 routes).

## 4. Prioritas Kerja Visual Berikutnya

| # | Prioritas | Aksi | Effort |
|---|---|---|---|
| P1 | Cost page | fix fetch/render cost data (kosong padahal backend `/api/mc/cost/agents` ada) | S |
| P2 | Telegram feed | fix render message feed (0 elemen padahal `/api/mc/telegram-feed` ada) | S |
| P3 | Vision auxiliary | ganti model vision 9router → zen/aktif (unblock browser_vision) | S |
| P4 | Deploy page | isi status deploy dari `/api/mc/deploy/status` | M |
| P5 | Swarm | render topology lebih detail | M |
| P6 | Skill market | render marketplace dari Bank Pusat | M |

## 5. Tidak Perlu Diubah

- Layout ORB overlay, taskbar, 12 page scaffold — sudah rapi & lengkap
- `build_unified.py` (30KB) — mekanisme build tunggal sudah ada
- Data fetch architecture — sudah benar (semua route ada)

---

*Dokumen ini breakdown, bukan klaim selesai. Verifikasi visual penuh butuh model vision hidup.*
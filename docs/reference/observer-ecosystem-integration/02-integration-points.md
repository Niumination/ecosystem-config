# 02 — Titik Integrasi dengan Ekosistem Niumination

> **Ekosistem saat ini:**
> - `niu-dash-fullstack` — Dashboard Next.js (112 projects, data pipeline)
> - `herdr` — 4 karakter AI agent (Pembangun, Pengawas, Arsitek, Penjaga)
> - `Hermes Agent` — AI assistant utama (Telegram gateway)
> - `Production/niu-dash/` — Source data master

---

## Matriks Integrasi

| # | Integrasi | Observer → Ekosistem | Ekosistem → Observer | Prioritas |
|---|-----------|---------------------|---------------------|:---------:|
| 1 | **Build Monitor** | Deteksi error build → notif Telegram | — | 🔴 Tinggi |
| 2 | **Dev Server Watchdog** | Deteksi dev server down → restart/notif | — | 🔴 Tinggi |
| 3 | **Git Activity Logger** | Deteksi git commit/push → log ke memory | — | 🟡 Sedang |
| 4 | **Timeline Data Source** | Log activity → API endpoint dibaca dashboard | Dashboard tampilkan timeline | 🟡 Sedang |
| 5 | **Herdr Agent Trigger** | Deteksi event → trigger herdr agent | Herdr kirim status ke Observer | 🟢 Rendah |
| 6 | **Screen Capture Log** | Screenshot berkala → simpan sebagai evidence | — | 🟢 Rendah |

---

## 1. 🔴 Build Monitor

**Cara Kerja:**
```
Observer screen-moniitor terminal
  → Detect "build failed" / "ERROR" di layar
  → sendTelegram(chat_id, "❌ Build failed: ...")
  → Simpan ke memory untuk konteks
```

**Sensor:** `$SCREEN_OCR` atau `$SCREEN` (multimodal)
**Trigger:** Regex error pattern di OCR output
**Output:** Telegram notifikasi + memory log

**Contoh Agent Prompt:**
```
Kamu adalah build monitor. Pantau terminal di layar.
Jika melihat "build failed" atau "ERROR" atau "Module not found",
kirim notifikasi Telegram dengan isi error.
Jika tidak ada, cukup tulis "OK" dan timestamp.
$SCREEN_OCR
```

## 2. 🔴 Dev Server Watchdog

**Cara Kerja:**
```
Observer cek localhost:3000 tiap 30 detik
  → Jika response bukan 200
  → Bunuh proses lama
  → Jalankan ulang `npm run dev`
  → Notifikasi "✅ Dev server restarted"
```

**Tools:** `fetch` via code execution di JS, `sendTelegram`
**Trigger:** HTTP status code !== 200

**Contoh Kode:**
```javascript
const status = await fetch('http://localhost:3000').then(r => r.status).catch(() => 0);
if(status !== 200) {
  sendTelegram(CHAT_ID, `🔴 Dev server down (HTTP ${status}). Restarting...`);
  // Observer bisa trigger shell command via agent
} else {
  // silent — semuanya baik
}
```

## 3. 🟡 Git Activity Logger

**Cara Kerja:**
```
Observer pantau terminal untuk pola git push/commit
  → Deteksi "git push" atau "To github.com:"
  → Catat ke memory dengan timestamp
  → Notifikasi ringan
```

**Sensor:** `$SCREEN_OCR`
**Output:** Memory entry + notif Telegram (optional)

## 4. 🟡 Timeline Data Source untuk Dashboard

**Arsitektur:**

```
┌──────────┐     ┌──────────────┐     ┌──────────────────┐
│ Observer  │────▶│ Memory/Log   │────▶│ niu-dash API     │
│ Agent     │     │ (JSON file)  │     │ (read-only)      │
└──────────┘     └──────────────┘     └──────────────────┘
                      │
                      ▼
              ┌──────────────────┐
              │ Dashboard Widget │
              │ Timeline Card    │
              └──────────────────┘
```

Observer menyimpan activity log ke file JSON di `data/observer-logs/`.
Niu-dash membaca file tersebut via API endpoint atau server-side import.

**Format Data:**
```json
{
  "timestamp": "2026-07-13T10:30:00+07:00",
  "type": "build" | "git" | "server" | "note",
  "status": "success" | "error" | "info",
  "message": "Build selesai — 0 errors",
  "project": "niu-dash-fullstack"
}
```

## 5. 🟢 Herdr Agent Trigger

**Konsep:**
```
Observer detect "ERROR" di terminal
  → Panggil API herdr untuk trigger 🏗️ Si Pembangun
  → Herdr jalankan agent untuk fix error
  → Observer monitor hasilnya
```

Ini butuh:
- Observer punya akses ke herdr API/socket
- Agent herdr punya mode "fix error" yang bisa dipanggil dari luar

**Kompleksitas:** Tinggi — butuh koordinasi antar system.

## 6. 🟢 Screen Capture Log

Observer bisa screenshot berkala layar coding (setiap 5-10 menit) dan simpan sebagai image memory. Berguna untuk:
- Daily standup summary / evidence
- Visual timeline aktivitas
- Debug sesi panjang

---

## Diagram Alur Data

```
                    ┌─────────────────────┐
                    │    OBSERVER AI       │
                    │  (Desktop App)       │
                    │                      │
  ┌────────┐        │  ┌──────────────┐   │       ┌──────────────┐
  │Terminal│───────▶│  │ Build Monitor │───┼──────▶│  Telegram     │
  │ VS Code│        │  │ Agent         │   │       │  Notification │
  │ Browser│        │  └──────────────┘   │       └──────────────┘
  └────────┘        │                      │
       │            │  ┌──────────────┐   │       ┌──────────────┐
       │            │  │ Git Logger   │───┼──────▶│  Memory/Log  │
       └────────────│  │ Agent        │   │       │  File        │
                    │  └──────────────┘   │       └──────┬───────┘
                    │                      │              │
                    │  ┌──────────────┐   │              ▼
                    │  │ Server       │   │       ┌──────────────┐
                    │  │ Watchdog     │───┼──────▶│  niu-dash    │
                    │  └──────────────┘   │       │  Dashboard   │
                    └─────────────────────┘       └──────────────┘
```

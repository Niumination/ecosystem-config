# 04 — Roadmap Implementasi Observer

> **Kondisi awal:** Observer belum di-install. Ekosistem berjalan dengan Hermes + herdr.
> **Target:** Observer sebagai sensor layer yang bekerja di background.

---

## Phase 0: Prasyarat ✅ (Done)

- [x] Ekosistem niu-dash-fullstack berjalan (build OK, data pipeline OK)
- [x] GitHub repo ter-push
- [x] Deploy platform siap (Vercel/Cloudflare — by user later)

---

## Phase 1: Foundation 🔴

### 1.1 Install Observer Desktop App

**Langkah:**
1. Download release v2.4.2 dari [GitHub Releases](https://github.com/Roy3838/Observer/releases/latest/)
2. Install di `/Applications/Observer.app`
3. Jalankan dan grant permissions (screen recording, accessibility)
4. Login/create account (untuk notification bot)

**Verifikasi:**
- App bisa jalan di background
- Screen capture berfungsi
- Telegram notif bot terdaftar

### 1.2 Setup Telegram Notification

**Langkah:**
1. Buka Observer dashboard → Settings → Notifications
2. Konek ke bot `@observer_notification_bot`
3. Dapatkan chat_id untuk channel/group Telegram

### 1.3 Setup Local LLM

**Opsi A — Transformers.js (tanpa install tambahan):**
- Langsung bisa dari WebApp/Desktop App
- Model: Gemma 4 e2b/e4b (built-in)
- Catatan: Kurang stabil di mobile

**Opsi B — Ollama (rekomendasi):**
```bash
# Jika belum install Ollama
brew install ollama
ollama pull gemma:2b  # atau mistral, llama3.2

# Jalankan Ollama di background
ollama serve
```
- Observer Desktop → Settings → Model → Ollama
- Endpoint: `http://localhost:11434`

---

## Phase 2: Agent Deployment 🔴

### 2.1 Build Sentry (Agent A)

**Langkah:**
1. Observer dashboard → Create Agent
2. Copas system prompt dari `03-agent-blueprints.md`
3. Copas code dari `03-agent-blueprints.md`
4. Set sensor: `$SCREEN_OCR` — interval 5 detik
5. Ganti `CHAT_ID_HERE` dengan chat_id Telegram
6. Test: jalankan build yang gagal → harus dapat notif

**Verifikasi:**
- ✅ Build sukses → tidak ada notif (atau notif ✅ ringan)
- ✅ Build gagal → Telegram notif dalam <10 detik
- ✅ Error log tersimpan di memory

### 2.2 Server Watchdog (Agent B)

**Langkah:**
1. Create agent baru
2. Copas system prompt + code server watchdog
3. Sensor: `$SCREEN_OCR` — interval 30 detik
4. Test: matikan dev server → harus dapat notif

**Verifikasi:**
- ✅ Server mati → notif dalam <30 detik
- ✅ Server hidup → silent (no false positive)
- ✅ Memory log tercatat

---

## Phase 3: Data Integration 🟡

### 3.1 Shared Log File

**Langkah:**
1. Buat direktori `data/observer-logs/` di ekosistem
2. Observer code tab write ke JSON file
3. Niu-dash baca file via API route

**Observer Code tambahan (di tiap agent):**
```javascript
// Append ke shared log
const logEntry = JSON.stringify({
  timestamp: time(),
  type: 'build', // atau 'git', 'server'
  status: response.includes('🔴') ? 'error' : 'success',
  message: response
});
// Write to file (via fetch ke local API atau append ke file)
```

### 3.2 API Route di Niu-Dash

**File baru:** `app/api/observer-logs/route.ts`
```typescript
import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET() {
  const logPath = path.join(process.cwd(), 'data', 'observer-logs', 'activity.json')
  if (!fs.existsSync(logPath)) {
    return NextResponse.json({ logs: [] })
  }
  const data = fs.readFileSync(logPath, 'utf-8')
  const logs = data.trim().split('\n').map(JSON.parse).reverse().slice(0, 50)
  return NextResponse.json({ logs })
}
```

### 3.3 Dashboard Widget

**Komponen baru:** `components/ObserverTimeline.tsx`
- Baca dari `/api/observer-logs`
- Tampilkan timeline aktivitas development
- Filter: build | git | server | all
- Limit: 20 entri terbaru

---

## Phase 4: Advanced 🟢

### 4.1 Herdr Integration

- Observer detect critical error → trigger herdr agent untuk fix
- Butuh: herdr API endpoint atau socket command

### 4.2 Daily Report

- Agent D (Daily Logger) generate ringkasan harian
- Kirim ke Telegram jam 18:00
- Format: "Today: 3 builds, 2 errors, 5 commits in niu-dash-fullstack"

### 4.3 Multi-Project Support

- Expand monitoring ke project lain (TEDEO, kune-ya.com, dll)
- Per-agent per-project

---

## Timeline Estimasi

| Phase | Estimasi | Dependensi |
|-------|:--------:|------------|
| P1 Foundation | 1-2 jam | Download + install + setup |
| P2 Build Sentry | 1 jam | Test + tuning |
| P2 Watchdog | 30 menit | Copy from P2.1 |
| P3 Data Integration | 2-3 jam | File write + API + widget |
| P4 Advanced | TBD | Tergantung kebutuhan |
| **Total** | **~5-7 jam** | |

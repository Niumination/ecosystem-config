# 03 — Blueprint Agent Observer untuk Development Workflow

> Agent Observer ditulis dalam sistem Observer AI — terdiri dari **System Prompt** (instructions for local LLM) + **Code Tab** (JavaScript callback).

---

## Agent A: Build Sentry 🔴

**Tujuan:** Monitor build process dan kirim notif realtime saat error.

### System Prompt
```
Kamu adalah Build Sentry — asisten yang memantau terminal
build process. Tugasmu hanya melihat output terminal dan
mendeteksi error.

Jika kamu melihat:
- "build failed" → RESPON: BUILD_FAIL + cuplikan error
- "ERROR" atau "Error:" → RESPON: ERROR_LINE + baris error
- "Module not found" → RESPON: MODULE_MISSING + nama modul
- "successfully" + "compiled" → RESPON: BUILD_OK + durasi
- "0 errors" → RESPON: BUILD_OK
- Selain itu → RESPON: OK

Format RESPON: [STATUS] pesan singkat

$SCREEN_OCR
```

### Code Tab
```javascript
const statusMap = {
  BUILD_FAIL: '🔴',
  ERROR_LINE: '⚠️',
  MODULE_MISSING: '📦',
  BUILD_OK: '✅',
  OK: ''
};

const emoji = statusMap[response.split(' ')[0]] || '❓';
if(emoji && emoji !== '') {
  const msg = `${emoji} ${response}`;
  const now = time();
  sendTelegram("CHAT_ID_HERE", `${msg}\n🕐 ${now}`);
  appendMemory(`[${now}] ${msg}`);
}
```

### Trigger
- Interval: 5 detik
- Sensor: `$SCREEN_OCR`
- Model: Small/Local (transformers.js atau Ollama)

---

## Agent B: Server Watchdog 🛡️

**Tujuan:** Pastikan dev server selalu hidup.

### System Prompt
```
Kamu adalah server watchdog. Pantau output curl atau browser
untuk status server development.

Jika melihat:
- "200" atau halaman dashboard → RESPON: OK
- "Connection refused" atau "ERR_CONNECTION_REFUSED"
  → RESPON: DOWN
- "502" atau "503" atau "504" → RESPON: DEGRADED + kode

$SCREEN_OCR
```

### Code Tab
```javascript
if(response.includes('DOWN')) {
  sendTelegram("CHAT_ID_HERE", `🔴 Dev server DOWN! ${time()}`);
  appendMemory(`[${time()}] SERVER_DOWN`);
  // Opsional: trigger restart via shell
  // exec('cd ~/Desktop/Niumination/projects/niu-dash-fullstack && npm run dev &');
} else if(response.includes('DEGRADED')) {
  sendTelegram("CHAT_ID_HERE", `🟡 Server degraded: ${response}`);
}
```

### Trigger
- Interval: 30 detik
- Sensor: Browser atau curl manual di terminal

---

## Agent C: Git Activity Tracker 📝

**Tujuan:** Catat aktivitas git (commit, push) ke memory log.

### System Prompt
```
Kamu adalah git tracker. Pantau terminal untuk aktivitas git.

Jika melihat:
- "git commit" → RESPON: COMMIT + message
- "git push" → RESPON: PUSH
- "To github.com:Niumination/" → RESPON: PUSH_SUCCESS + repo
- "main -> main" → RESPON: PUSH_DONE
- Selain itu → RESPON: OK

$SCREEN_OCR
```

### Code Tab
```javascript
if(response !== 'OK') {
  const log = `[${time()}] 📝 ${response}`;
  appendMemory(log);
}
```

### Trigger
- Interval: 10 detik
- Sensor: `$SCREEN_OCR`

---

## Agent D: Daily Activity Logger 📊

**Tujuan:** Buat ringkasan aktivitas coding harian.

### System Prompt
```
Kamu adalah daily logger. Setiap 30 menit, lihat screenshot
layar dan catat aktivitas yang terlihat.

Identifikasi:
- Apakah VS Code/IDE terbuka? → project apa?
- Apakah terminal terbuka? → command apa?
- Apakah browser dengan dashboard? → localhost berapa?

RESPON dengan format:
[YYYY-MM-DD HH:MM] ACTIVITY: deskripsi singkat

$SCREEN
```

### Code Tab
```javascript
if(response.includes('ACTIVITY:')) {
  appendMemory(response);
}
```

### Trigger
- Interval: 30 menit
- Sensor: `$SCREEN` (multimodal, butuh model dengan vision)

---

## Priority Order Implementasi

```
Phase 1 (🔴 High)
├── Agent A: Build Sentry
└── Agent B: Server Watchdog

Phase 2 (🟡 Medium)
├── Agent C: Git Activity Tracker
└── Setup shared memory/file logging

Phase 3 (🟢 Nice-to-have)
├── Agent D: Daily Activity Logger
└── Integrasi timeline ke dashboard
```

# 01 — Apa Itu Observer AI

> **Source:** [Roy3838/Observer](https://github.com/Roy3838/Observer)
> **Version:** v2.4.2 (29 Jun 2026)
> **License:** AGPL-3.0
> **Stars:** 1.4k | **Forks:** 117

---

## Arsitektur Inti

```
┌─────────────────────────────────────────────────────┐
│                   OBSERVER AI                         │
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │ SENSORS  │───▶│  MODELS  │───▶│  TOOLS    │        │
│  │          │    │ (Local)  │    │           │        │
│  │ Screen   │    │ Transform│    │ Telegram  │        │
│  │ Camera   │    │  ers.js  │    │ WhatsApp  │        │
│  │ Mic      │    │ llama.cpp│    │ Discord   │        │
│  │ Audio    │    │ Ollama   │    │ SMS/Email │        │
│  │ Clipboard│    │          │    │ Memory    │        │
│  │ Memory   │    │          │    │ Code Exec │        │
│  └──────────┘    └──────────┘    └──────────┘        │
└─────────────────────────────────────────────────────┘
```

## Cara Kerja per Loop

1. **Sensor membaca input** — screen capture, OCR, clipboard, mic, audio, memory
2. **Local LLM memproses** — dengan system prompt + sensor data sebagai variabel (`$SCREEN`, `$MEMORY`, dll)
3. **JavaScript callback dijalankan** — berdasarkan respons model, bisa kirim notif, simpan memory, panggil API, dll

## Sensor Variables (System Prompt)

| Variable | Deskripsi | Use Case untuk Ekosistem |
|----------|-----------|--------------------------|
| `$SCREEN` | Screenshot layar (multimodal) | Monitor terminal/IDE saat build |
| `$SCREEN_OCR` | Teks dari layar | Baca log error di terminal |
| `$CLIPBOARD` | Isi clipboard | Snapshot command yang di-copy |
| `$MEMORY` | Text memory agent | Simpan log aktivitas development |
| `$MICROPHONE` | Transkripsi mic | Voice note untuk daily log |
| `$SCREEN_AUDIO` | Audio dari screen | Capture meeting/screencast |

## Tools (JavaScript Functions)

### Notifikasi — Relevan untuk Ekosistem

| Function | Platform | Catatan |
|----------|----------|---------|
| `sendTelegram(chat_id, msg, images?)` | Telegram ✅ | Bot: `@observer_notification_bot` |
| `sendDiscord(webhook, msg, images?)` | Discord ✅ | Webhook-based |
| `sendEmail(email, msg, images?)` | Email ✅ | Via signed-in email |
| `sendWhatsapp(phone, msg, images?)` | WhatsApp ⚠️ | Whitelisting required |
| `sendSms(phone, msg)` | SMS ⚠️ | Whitelisting required |
| `sendPushover(token, msg)` | Pushover ✅ | |

### Memory — State Persistence

| Function | Deskripsi |
|----------|-----------|
| `setMemory(id?, content)` | Simpan text memory |
| `getMemory(id?)` | Baca text memory |
| `appendMemory(id?, content)` | Append ke memory |
| `getImageMemory(id?)` | Baca image memory |

### Control & Utility

| Function | Deskripsi |
|----------|-----------|
| `startAgent(id?)` | Start agent lain |
| `stopAgent(id?)` | Stop agent |
| `time()` | Current timestamp |
| `sleep(ms)` | Delay |

## Deployment Options

| Opsi | Metode | Cocok untuk |
|------|--------|-------------|
| **1. Web App** | Transformers.js di browser | Testing, tanpa install |
| **2. Desktop App** | Bundled llama.cpp | Production — jalan di background Mac/Windows |
| **3. Desktop + Ollama** | Ollama API via localhost:3838 | Pakai model existing (Mistral, LLaMA, dll) |
| **4. Docker/Jupyter** | Container | Development/eksperimen |

> **Rekomendasi untuk ekosistem:** Opsi 2 atau 3 — Desktop App + Ollama, karena sudah punya model lokal.

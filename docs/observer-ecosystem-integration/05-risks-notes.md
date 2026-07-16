# 05 — Risiko, Lisensi & Catatan Arsitektur

---

## 1. Lisensi AGPL-3.0 ⚠️

**Status:** Observer AI menggunakan lisensi AGPL-3.0.

**Apa artinya untuk ekosistem Niumination:**
| Skenario | Risiko | Aman? |
|----------|:------:|:-----:|
| Observer sebagai desktop app terpisah | 🟢 Rendah | ✅ Aman — proses independen |
| Observer komunikasi via HTTP/API | 🟢 Rendah | ✅ Aman — network communication |
| Observer dan niu-dash berbagi file JSON | 🟢 Rendah | ✅ Aman — data interchange |
| Copy-paste kode Observer ke niu-dash | 🔴 Tinggi | ❌ Tidak boleh — derivatif work |
| Modifikasi kode Observer sendiri | 🟡 Sedang | ⚠️ Harus tetap AGPL jika didistribusi |

**Kesimpulan:** Selama Observer berjalan sebagai **proses terpisah** dan komunikasinya via **file/API**, lisensi aman. Jangan meng-copy kode Observer langsung ke proyek Niumination.

---

## 2. Alternatif Open Source

Jika lisensi AGPL jadi masalah di masa depan, ada alternatif:

| Alternatif | Lisensi | Fitur Screen Monitor | Fitur Notifikasi | Status |
|------------|:-------:|:--------------------:|:----------------:|:------:|
| **Observer AI** | AGPL-3.0 | ✅ Lengkap | ✅ Telegram, WA, Discord | ⭐ Pilihan utama |
| **Screenotate** | MIT | ✅ Screenshot | ❌ No notif | Parsial |
| **Tesseract OCR** | Apache 2.0 | ✅ OCR only | ❌ | Parsial |
| **n8n + Tesseract** | Sustainable | ⚠️ Custom build | ✅ | Butuh setup |
| **Build sendiri** | — | ⚠️ Butuh waktu | ✅ | Opsi jangka panjang |

---

## 3. Risiko Teknis

### 3.1 Screen Recording Permission

Observer butuh **Screen Recording** akses di macOS (System Settings → Privacy & Security → Screen Recording). Ini wajar untuk screen capture tool, tapi:
- Beberapa enterprise VPN/security software bisa block
- Perlu di-allow manual sekali setup
- Jika Mac restart dengan FileVault penuh, grant mungkin perlu diulang

### 3.2 Local LLM Performance

| Model | RAM | CPU/GPU | Kelancaran |
|-------|:---:|:-------:|:----------:|
| Transformers.js (Gemma 4 e2b) | ~2GB | CPU | ⚡ Cepat, kurang akurat |
| Ollama + Gemma 2B | ~2GB | CPU/GPU | ⚡ Cepat |
| Ollama + Mistral 7B | ~6GB | CPU/GPU | 🐢 Lebih lambat |
| llama.cpp (bundled in Desktop App) | ~4GB | GPU ideal | ⚡ Stabil |

**Rekomendasi:** Mulai dengan Transformers.js (bawaan) untuk testing, upgrade ke Ollama jika butuh akurasi lebih.

### 3.3 False Positive / Noise

- Screen OCR bisa salah baca teks (font, ukuran, warna)
- Build output yang mengandung kata "ERROR" di log lama bisa trigger false positive
- Perlu tuning regex dan cooling period

**Mitigasi:**
- Gunakan pattern spesifik ("build failed", "error:", bukan "ERROR" saja)
- Tambah cooldown: jangan kirim notif untuk error yang sama dalam 5 menit
- Mode "silent" untuk status OK — hanya notif kalau ada masalah

### 3.4 Resource Usage

Observer Desktop + local LLM:
- CPU: ~10-20% saat aktif (tergantung model)
- RAM: 2-6GB (tergantung model)
- Battery: Drain lebih cepat di MacBook

**Mitigasi:**
- Turunkan interval scan (15-30 detik untuk watchdog, bukan 5 detik)
- Gunakan model kecil (Gemma 2B dibanding 7B+)
- Matikan agent saat tidak coding

---

## 4. Perbandingan: Hermes vs Observer vs Herdr

```
┌──────────────────────────────────────────────────────────┐
│                    ECOSYSTEM NIUMINATION                   │
│                                                           │
│  ┌──────────────────┐   ┌──────────────────┐             │
│  │   HERMES AGENT   │   │  OBSERVER AI     │             │
│  │                  │   │  (BARU)          │             │
│  │ • Reasoning      │   │ • Screen monitor │             │
│  │ • Planning       │   │ • Event trigger  │             │
│  │ • Code writing   │   │ • Notifications  │             │
│  │ • Telegram bot   │   │ • Build watchdog │             │
│  │ • Data pipeline  │   │ • OCR/clipboard  │             │
│  │ • Skill mgmt     │   │ • Daily logging  │             │
│  └──────┬───────────┘   └────────┬─────────┘             │
│         │                        │                        │
│         ▼                        ▼                        │
│  ┌─────────────────────────────────────────┐              │
│  │          HERDR MULTI-AGENT               │              │
│  │  🏗️ 🔍 📐 🛡️                           │              │
│  │  • Parallel task execution               │              │
│  │  • Code generation via opencode          │              │
│  │  • Character-based agent roles           │              │
│  └─────────────────────────────────────────┘              │
│                                                           │
│  ┌─────────────────────────────────────────┐              │
│  │       NIU-DASH DASHBOARD                 │              │
│  │  • 112 projects visualized               │              │
│  │  • Team status cards                     │              │
│  │  • 3D zen UI 🧘                          │              │
│  │  • (Future: Observer timeline widget)    │              │
│  └─────────────────────────────────────────┘              │
└──────────────────────────────────────────────────────────┘
```

### Kapan pakai yang mana:

| Saya butuh... | Pakai... |
|---------------|----------|
| Nulis kode, planning, reasoning | Hermes Agent + herdr multi-agent |
| Monitor build error realtime | Observer AI |
| Notifikasi Telegram pas build gagal | Observer AI (lebih cepat dari cron) |
| Ngerjain task paralel (4 agent) | herdr (🏗️🔍📐🛡️) |
| Extract data & sync pipeline | Hermes Agent |
| Dashboard visualisasi | niu-dash-fullstack |
| Daily report aktivitas coding | Observer AI |

---

## 5. Catatan Arsitektur

### 5.1 File-Based Communication (Recommended)

Observer tulis activity log ke file → niu-dash baca file.

```
Observer → writes to data/observer-logs/activity.log
Niu-Dash → reads via API route at /api/observer-logs
```

**Keuntungan:**
- Decoupled — Observer bisa mati, dashboard tetap jalan
- No API key sharing
- Simple, reliable

### 5.2 HTTP-Based Communication (Future)

Observer panggil endpoint di niu-dash langsung:
```
Observer → POST /api/observer-logs { type, status, message }
```

**Butuh:**
- Niu-dash jalan (tidak selalu di lokal)
- API key untuk autentikasi Observer
- CORS handling

### 5.3 No Direct Code Sharing

**Prinsip penting:** Observer dan Niumination adalah dua proyek terpisah:
- `github.com/Roy3838/Observer` — punya Roy Medina
- `github.com/Niumination/*` — punya Niumination

Jangan:
- ❌ Fork Observer ke Niumination tanpa keputusan lisensi
- ❌ Copy-paste kode Observer ke dashboard
- ❌ Modifikasi Observer dan distribusikan ulang (tanpa nerbitin source)

Lakukan:
- ✅ Observer sebagai tool yang di-install dan dikonfigurasi
- ✅ Agent blueprint disimpan sebagai dokumentasi, bukan kode yang di-merge
- ✅ Data interchange via file/API yang terdefinisi

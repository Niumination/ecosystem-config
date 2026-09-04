# 🛠 Integrasi Toolkits ke Hermes Agent — Niumination Content Creator

> Tujuan: Otomatisasi pipeline naskah → video → posting ke social media pakai toolkits gratis.

## A. Klasifikasi Toolkit: Luar vs Dalam Composio

### 𝟭. KELAS A: TOOLKIT GRATIS LUAR (Free Tier, Bukan Composio)

| Tool | Free Tier | Platform | Cocok Buat Pilar |
|---|---|---|---|
| **Meta Business Suite** | Unlimited | FB & IG | `Behind the Build`, `Aceh Pride` |
| **Buffer (free)** | 3 akun, 10 post/profil | IG, FB, TT, LI, YT, Pinterest, X | Kalender 30-hari posting |
| **Pallyy** | Free forever, 1 profile | IG | `AI Tools Gratis` demo, reels distribution |
| **Postiz (self-hosted)** | Total GRATIS | Semua platform | Semua pilar, deploy VM Cloud |
| **Make.com** | 1,000 ops/bln | Visual workflow | Otomatisasi pipa produksi |
| **Canva (free)** | Desain & video edit | 9:16 video, infografis | `baoyu-infographic`, `impeccable` |
| **Ocoya** | AI caption + scheduling | Basic analytics | Copy hook & naskah cepat |
| **Zernio** | Unified API 15 platforms | Posting, comments, DMs, analytics | API layer untuk multi-platform |
| **Meta Ads Manager** | Free (native) | Campaign boosting reels | Promo paid jika butuh |

### 𝟮. KELAS B: TOOLKIT DALAM COMPOSIO.dev (MCP/API Integrations)

| Tool | Fitur Kunci | Persyaratan |
|---|---|---|
| **Instagram** | Posting, media, insights via MCP | Daftar composio + IG developer |
| **TikTok** | Upload video, oEmbed, analytics | Daftar + TikTok API key |
| **Facebook** | Graph API, post scheduling, insights | Daftar + FB developer |
| **Twitter/X** | Post, reply, trends | Daftar + X API key |
| **LinkedIn** | Post articles, engagement | Daftar + LinkedIn API |
| **Ayrshare** | Multi-platform posting (IG+FB+TT+LI sekaligus) | Free tier ada |
| **Buffer (di composio)** | Scheduling, analytics via MCP | Butuh akun Buffer |
| **ContentStudio** | Content curation + scheduling | Free trial/limited |
| **ActiveCampaign** | Email marketing automation | Paid, tapi free trial |
| **Google Sheets, Docs, Airtable** | Data storage & workflow | Biasa di Hermes |

---

## B. Rencana Integrasi ke Hermes Thread (8 Langkah)

### ✅ Langkah 1: Daftarkan Akun Gratis (One-time)
- Buat akun **Meta Business Suite** (gratis total)
- Daftar **Buffer** (free plan: 3 akun)
- Daftar **Make.com** (free: 1,000 ops/bulan)
- (Opsional) Daftar **composio.dev** kalau butuh MCP integrations advanced

### ✅ Langkah 2: Buat File Integrasi di Docs Ekosistem
*(Sudah kamu baca di atas — file ini)*

### ✅ Langkah 3: Setup Workflow Teknis per Toolkits

**1. Meta Business Suite → Hermes**
- Aksi: Export list reels/karousel ke CSV → Hermes cronjob import
- Cron schedule: Setiap Mg 1, Mg 5, Mg 9 (per kalender 30-hari)
- Output: Link post + insights (reach, engagement) → input ke BACKLOG.md

**2. Buffer → Hermes**
- Aksi: Isi caption naskah → Buffer API posting
- MCP composio option: Jika butuh automasi cross-platform
- Cron: Setiap selesai generate 1 reel, otomatis push ke Buffer draft

**3. Make.com → Hermes (Workflow Builder)**
- Workflow 1: Google Sheet (kalender 30-hari) → Trigger → Buffer/Meta Suite posting
- Workflow 2: Naskah dari `ghost` skill → hyperframes generate → post otomatis
- Trigger: Setiap akhir Semana, Make.com cek Google Sheet ada yang belum diposting?

**4. Postiz (self-hosted) → Hermes**
- Deploy: VM Google Cloud Compute Engine free (e2-micro)
- Integrasi: `~/Desktop/Niumination/` → Postiz dashboard → posting sekaligus IG+FB+TT
- Benefit: Total gratis, tanpa batas akun sosial

**5. Canva → Hermes (Design)**
- Aksi: Desain infografis carousel → Export MP4/video reels
- Cara kerja: `image_generate` skill → Canva edit → simpan ke `~/Downloads`
- Posting: Manual ke Meta Suite / Buffer

**6. Pallyy → Hermes (Scheduling IG)**
- Aksi: Schedule reels ke IG gratis forever
- Integrasi: Buka pallyy.com → hubungkan 1 IG proyek Niumination → setting kalender

**7. Zernio API → Hermes (Layer API)**
- Fungsi: Unified API buat posting ke 15 platform sekaligus
- Integrasi: Hermes terminal → curl ke Zernio endpoint → post sama sekali
- Free tier: 2 akun awal, lalu $6→$1/account/bln (graduated)

**8. Google Cloud + BigQuery → Hermes (Analitik)**
- Simpan data: Performansi reels/karousel ke Cloud Storage → BigQuery free 1TB/bln
- Query: SQL buat laporan progress 30-hari, engagement trend, best posting time
- Input ke: `docs/reports/` & `BACKLOG.md` buat evaluasi

### ✅ Langkah 4: Kalender Integrasi Teknis (30 Hari)

| Minggu | Aksi Integrasi | Tool Utama |
|---|---|---|
| Mg 1-3 | Generate 3 reels + setup Meta Business Suite account | Meta Suite, Canva, hyperframes |
| Mg 4-6 | Setup Buffer account + schedule 3 reel pertama | Buffer, Make.com workflow |
| Mg 7-9 | Deploy Postiz di VM Cloud + test posting cross-platform | Postiz, Zernio API |
| Mg 10-12 | Buat Make.com workflow: Sheet → posting otomatis | Make.com, Google Sheets |
| Mg 13-15 | Integrasi analytics: input BigQuery insights ke Hermes | BigQuery, Google Sheets |
| Mg 16-18 | Test Pallyy scheduling + cek performa minggu 1 | Pallyy, Meta Suite insights |
| Mg 19-21 | Optimasi naskah berdasarkan data (ghost + data input) | ghost, Make.com |
| Mg 22-24 | Bulan eval: apa yang work, budget upgrade apa needed | Semua tool, docs/reports |
| Mg 25-28 | Produk digital: template dari 68 skill → export ke Google Drive | Airtable free, Google Drive |
| Mg 29-30 | Laporan bulanan + rencana bulan selanjutnya | Semua output di atas |

### ✅ Langkah 5: Catatan Penting

1. **Semua tool free tier bisa jalan tanpa kartu kredit** kecuali kalau butuh upgrade buat volume tinggi.
2. **Composio.dev** butuh signup dan API key, tapi kadang free tier ada buat tool tertentu (Buffer, Instagram, TikTok MCP).
3. **Prioritas awalan:** Mulai dari Meta Business Suite (gratis total) → Buffer (free plan) → Make.com workflow → Postiz self-hosted.
4. **Tracking wajib:** Semua link post + insights simpan di `docs/reports/` + catat di `BACKLOG.md` per minggu.
5. **Backup:** Jika salah satu tool mati, tools lain masih bisa jalan karena terpisah (modular).

---

## C. Struktur File di Ecosistem Niumination

File ini disimpan di:
```
/Users/zaryu/Desktop/Niumination/docs/reference/composio-integration-plan.md
```

File lengkap ini sekarang adalah bagian dari dokumentasi referensi ekosistem, dapat diakses bersama:
- `BACKLOG.md` (prioritas projek)
- `AGENTS.md` (global rules)
- `skills/manifest.json` (skill bank)
- `docs/reports/` (laporan status & insiden)

---
> *File ini dibuat dari integrasi rekomendasi toolkits gratis (kelas A) dan toolkits composio.dev (kelas B) untuk thread konten kreator Niumination. Setiap minggu berikut progress sesuai kalender 30-hari di rencana konten reels.*
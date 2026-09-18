# 🛠 Integrasi Toolkits ke Hermes Agent — Niumination Content Creator

> Tujuan: Otomatisasi pipeline naskah → video → posting ke social media pakai toolkits gratis.

## A. Klasifikasi Toolkit: Luar vs Dalam Composio

### 𝟭. KELAS A: TOOLKIT GRATIS LUAR (Free Tier, Bukan Composio) — DIPINDAH

> Katalog lengkap (**10 tool + 1 koreksi**, angka diverifikasi ulang langsung ke halaman resmi 18 Sep 2026): `docs/registry/composio-free-tier-tools.md`
> Dipindah 2026-09-16 ke satu rumah (One-home rule) — jangan salin tabelnya kembali ke sini.
> Fakta yang mengubah rencana: Postiz Cloud **tanpa** free plan (self-hosted gratis), Canva Free **tidak** menjadwalkan ke sosial, Pallyy Free **gambar saja** (reels tidak bisa), Ocoya **tidak gratis**.

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
- Buat akun **Meta Business Suite** (gratis total; jendela jadwal FB 20 menit–29 hari)
- Daftar **Buffer** (free plan: 3 kanal × 10 post terjadwal per kanal)
- Daftar **Make.com** (free: 1.000 credit/bulan, **maksimum 2 skenario aktif**)
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
- Aksi: Schedule **gambar/carousel** ke IG
- ⚠️ Free tier **tidak** bisa publikasi video: 1 social set, **15 post terjadwal/bulan, hanya gambar** (diverifikasi 18 Sep 2026). Untuk reels pakai penjadwal native IG, Buffer, atau Postiz self-hosted
- Integrasi: Buka pallyy.com → hubungkan 1 IG proyek Niumination → setting kalender

**7. Zernio API → Hermes (Layer API)**
- Fungsi: API terpadu untuk social + blogs + ads + messaging (angka "15 platform" lama tidak ditemukan di halaman resmi — jangan dipakai sebagai klaim)
- Integrasi: Hermes terminal → curl ke Zernio endpoint → post sama sekali
- Free tier (diverifikasi 18 Sep 2026): **2 akun pertama gratis tanpa kartu kredit**, lalu $6/akun/bln untuk akun ke-3–10 dan $3/akun untuk 11–100

**8. Google Cloud + BigQuery → Hermes (Analitik)**
- Simpan data: Performansi reels/karousel ke Cloud Storage → BigQuery free tier **1 TiB query + 10 GiB penyimpanan per bulan** (terverifikasi 18 Sep 2026, `cloud.google.com/bigquery`)
- Query: SQL buat laporan progress 30-hari, engagement trend, best posting time
- Input ke: `docs/reports/` & `BACKLOG.md` buat evaluasi

### ✅ Langkah 4: Kalender Integrasi Teknis (30 Hari)

| Minggu | Aksi Integrasi | Tool Utama |
|---|---|---|
| Mg 1-3 | Generate 3 reels + setup Meta Business Suite account | Meta Suite, Canva, hyperframes |
| Mg 4-6 | Setup Buffer account + schedule 3 reel pertama | Buffer, Make.com workflow |
| Mg 7-9 | Deploy **Postiz self-hosted** di VM Cloud (cloud Postiz tidak punya free plan) + test posting cross-platform | Postiz, Zernio API |
| Mg 10-12 | Buat Make.com workflow: Sheet → posting otomatis | Make.com, Google Sheets |
| Mg 13-15 | Integrasi analytics: input BigQuery insights ke Hermes | BigQuery, Google Sheets |
| Mg 16-18 | Test Pallyy scheduling + cek performa minggu 1 | Pallyy, Meta Suite insights |
| Mg 19-21 | Optimasi naskah berdasarkan data (ghost + data input) | ghost, Make.com |
| Mg 22-24 | Bulan eval: apa yang work, budget upgrade apa needed | Semua tool, docs/reports |
| Mg 25-28 | Produk digital: template dari 68 skill → export ke Google Drive | Airtable free, Google Drive |
| Mg 29-30 | Laporan bulanan + rencana bulan selanjutnya | Semua output di atas |

### ✅ Langkah 5: Catatan Penting

1. **Free tier yang diklaim sudah diverifikasi 18 Sep 2026** (kecuali disebut lain). Yang berubah dari asumsi lama: **Ocoya tidak gratis**, **Postiz Cloud tanpa free plan**, **Canva Free tidak menjadwalkan ke sosial**, **Pallyy Free hanya gambar (bukan reels)**, dan **jendela jadwal Meta FB hanya 29 hari**.
2. **Composio.dev** butuh signup dan API key, tapi kadang free tier ada buat tool tertentu (Buffer, Instagram, TikTok MCP).
3. **Prioritas awalan:** Mulai dari Meta Business Suite (gratis total) → Buffer (free plan) → Make.com workflow → Postiz self-hosted.
4. **Tracking wajib:** Semua link post + insights simpan di `docs/reports/` + catat di `BACKLOG.md` per minggu.
5. **Backup:** Jika salah satu tool mati, tools lain masih bisa jalan karena terpisah (modular).

---

## C. Struktur File di Ecosistem Niumination

File ini disimpan di:
```
/Users/zaryu/Desktop/Niumination/docs/registry/composio-integration-plan.md
```

File lengkap ini sekarang adalah bagian dari dokumentasi referensi ekosistem, dapat diakses bersama:
- `BACKLOG.md` (prioritas projek)
- `AGENTS.md` (global rules)
- `skills/manifest.json` (skill bank)
- `docs/reports/` (laporan status & insiden)

---
> *File ini dibuat dari integrasi rekomendasi toolkits gratis (kelas A) dan toolkits composio.dev (kelas B) untuk thread konten kreator Niumination. Setiap minggu berikut progress sesuai kalender 30-hari di rencana konten reels.*
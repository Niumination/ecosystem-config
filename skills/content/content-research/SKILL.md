---
name: content-research
description: "Riset tren, keyword, audiens, dan bedah kompetitor"
version: 1.0.0
author: Hermes Content Studio Pack
license: MIT
metadata:
  hermes:
    tags: [Content, Research, Trends, SEO, Keyword]
    related_skills: [content-studio, content-script]
    requires_tools: [web_search]
    blueprint:
      schedule: "0 7 * * *"
      deliver: origin
      prompt: "Radar tren harian: jalankan scripts/trend_radar.py, pilih 3 sinyal terkuat untuk niche kita, usulkan 5 ide konten dengan skor nilai jual, simpan ke TREND_LOG.csv."
---

# Content Research

Ubah informasi mentah di internet menjadi **ide konten bernilai jual** dan **bukti** yang bisa dikutip.

## When to Use

- "cari tren", "apa yang lagi ramai", "radar", "ide konten"
- "riset keyword/SEO untuk topik X"
- "bedah akun/kompetitor X" (competitor teardown)
- "cari data/angka untuk mendukung klaim X"
- "cek rate pasar / kebijakan platform terbaru"
- sebelum menulis naskah apa pun yang memuat klaim atau angka

## Quick Reference

| Tugas | Perintah/alat |
|---|---|
| Radar harian | `python3 scripts/trend_radar.py --niche "ai,automation,video" --days 2 --limit 15 --csv workspace/data/TREND_LOG.csv` |
| Minat pencarian | `pytrends` (Google Trends) — `interest_over_time`, `related_queries`, `geo_id=ID` |
| Berita/discussion | `web_search` + Hacker News Algolia API (gratis, tanpa key) |
| Repo/tool baru | GitHub Trending + Search API (`created:>YYYY-MM-DD stars:>100 topic:video`) |
| Video/short trend | TikTok Creative Center (gratis), YouTube autocomplete, `web_extract` halaman trending |
| Iklan kompetitor | Meta Ad Library (gratis), TikTok Creative Center → Top Ads |
| Bedah kanal publik | halaman About + 20 video teratas (views, durasi, judul, tanggal) via `web_extract` |
| Fakta untuk naskah | `web_search` → `web_extract` sumber primer → catat di `SOURCES.md` |

## Procedure

### A. Radar tren (harian / on-demand)
1. Jalankan `scripts/trend_radar.py` dengan niche dari `workspace/BRAND.md`.
2. Saring: buang yang tidak relevan audiens; tandai yang **bisa diproduksi < 4 jam**.
3. Untuk 3 sinyal terkuat tulis blok wajib:
   `SINYAL` → `KENAPA PENTING UNTUK AUDIENS` → `IDE KONTEN (judul kerja)` → `FORMAT` → `SUDUT EKSKLUSIF (data/pengalaman apa yang hanya kita punya)` → `SKOR NILAI JUAL 1–10`.
4. Skor: (relevansi audiens ×0,3) + (bukti tersedia ×0,25) + (first-mover ×0,2) + (jalur cuan jelas ×0,25).
5. Append ke `workspace/data/TREND_LOG.csv`, usulkan 5 ide teratas ke pengguna.

### B. Riset keyword & SEO
1. Kumpulkan 20–30 kandidat: autocomplete YouTube/Google, `pytrends` related queries, pertanyaan forum (Reddit/StackOverflow/Kaskus), komentar di video sejenis.
2. Kelompokkan: **informasional** (cara/apa/kenapa), **komersial** (terbaik/vs/harga/review), **transaksional** (beli/unduh/jasa).
3. Untuk tiap kelompok tentukan: intent, format terbaik, dan satu sudut yang belum dipakai pesaing.
4. Output: `workspace/project/<slug>/KEYWORDS.csv` (`keyword,intent,volume_proxy,pesaing,format,sudut`).

### C. Competitor teardown (bedah kompetitor)
1. Pilih 3 akun sejenis (1 besar, 1 setara, 1 di luar niche tapi formatnya bagus).
2. Ambil 20 konten teratas masing-masing → catat: hook, format, durasi, struktur, CTA, views/engagement, tanggal.
3. Cari pola: hook yang berulang, celah topik yang tidak mereka bahas, format yang engagement-nya tinggi tapi produksinya murah.
4. Output `TEARDOWN.md`: 5 hal yang kita tiru (bukan salin), 3 celah yang kita isi, 1 format baru yang kita ciptakan.
5. **Etika & hukum:** hanya ambil insight struktural. Jangan menyalin naskah, visual, atau audio.

### D. Riset bukti untuk naskah (wajib sebelum klaim dipublikasikan)
1. Untuk setiap angka/klaim: cari **sumber primer** (laporan resmi, dokumentasi, paper, halaman kebijakan platform).
2. Catat di `SOURCES.md`: `klaim | sumber (URL) | penerbit | tanggal publikasi | tanggal akses | kutipan pendek`.
3. Bila sumbernya sekunder/blog, tandai `kepercayaan: sedang` dan cari pembanding.
4. Bila data tidak ada → ubah klaim jadi hipotesis atau jadikan **data proprietary**: ukur sendiri (uji tool, survei 20 orang, benchmark harga) — ini justru menaikkan nilai jual.

### E. Riset pasar uang (rate & kebijakan)
1. Cari laporan creator economy terbaru, rate guide UGC/brand deal, syarat monetisasi platform (YouTube YPP dua tier, TikTok per negara).
2. Bandingkan dengan rate card kita; usulkan perubahan berbasis bukti (bukan perasaan).
3. Simpan di `workspace/data/MARKET_NOTES.md` dengan tanggal.

## Pitfalls

- **Jangan menyimpulkan dari satu sumber.** Minimal 2 sumber independen untuk angka penting.
- **Jangan pakai tanggal kadaluarsa.** Kebijakan platform berubah; selalu catat tanggal akses dan prioritaskan < 90 hari.
- **Tren ≠ niche.** Tren yang tidak relevan audiens inti menghasilkan views kosong tanpa uang.
- **Jangan mengarang statistik.** Kalau tidak ditemukan, tulis "tidak ada data publik" dan usulkan mengukur sendiri.
- **Hati-hati scraping.** Hormati robots.txt & rate limit; pakai API resmi bila ada (HN Algolia, GitHub).
- **Jangan bocorkan data pribadi** orang/akun yang dibedah.

## Verification

- `TREND_LOG.csv` bertambah baris dengan kolom lengkap (tanggal, sumber, sinyal, niche, skor, ide).
- Setiap ide punya `SUDUT EKSKLUSIF` terisi — bukan sekadar "bahas topik X".
- `SOURCES.md` proyek memuat sumber primer + tanggal untuk setiap klaim yang akan dipublikasikan.
- Ringkasan ke pengguna ≤ 200 kata, berisi 3 sinyal + 5 ide + perintah lanjutan (`/naskah <slug>`).

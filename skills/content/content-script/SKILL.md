---
name: content-script
description: "Hook, naskah, storyboard, caption, dan copywriting"
version: 1.0.0
author: Hermes Content Studio Pack
license: MIT
metadata:
  hermes:
    tags: [Content, Script, Hook, Copywriting, Storyboard]
    related_skills: [content-studio, content-research, content-produce]
---

# Content Script

Menulis konten yang menahan perhatian dan menghasilkan tindakan — untuk video vertikal, long-form, carousel, thread, newsletter, dan naskah UGC berbayar.

## When to Use

- `/naskah <slug>`, "bikin skrip", "tulis hook", "storyboard", "shot list"
- "caption/deskripsi untuk post ini", "thread tentang X", "newsletter edisi X"
- "bikin naskah UGC untuk brand X" (deliverable berbayar)
- memperbaiki retensi konten yang sudah ada

## Quick Reference

| Output | Template | Panjang target |
|---|---|---|
| Short vertikal | `templates/naskah-short-vertical.md` | 15–45 dtk, ≤ 130 kata |
| Long-form YouTube | `templates/naskah-longform-youtube.md` | 6–15 mnt, 900–2.200 kata |
| Carousel IG/LinkedIn | `templates/carousel-10-slide.md` | 8–10 slide, ≤ 25 kata/slide |
| Thread X/Bluesky | `templates/thread-x.md` | 5–9 post |
| Newsletter | `templates/newsletter.md` | baca 3–5 menit |
| UGC brand | `templates/ugc-brief.md` + naskah | 3 varian hook × 15–45 dtk |
| Podcast | `templates/podcast-script.md` | 20–40 mnt, outline + intro/outro |
| Caption/deskripsi | pola di bawah | 1–3 baris + CTA + tag |

## Procedure

### A. Sebelum menulis (30 detik, jangan dilewati)
Baca `workspace/BRAND.md` + `project/<slug>/BRIEF.md`. Tetapkan satu kalimat:
`AUDIENS + MASALAH + JANJI + BUKTI + CTA + JALUR CUAN`.
Bila `SOURCES.md` belum ada dan naskah memuat angka → hentikan, jalankan `content-research` D.

### B. Hook (wajib 10, pilih 3)
1. Tulis 10 hook memakai pola berbeda (taruhan, kontradiksi, hasil+waktu, rahasia, daftar, demonstrasi, identitas, open loop).
2. Aturan: ≤ 12 kata; menyebut audiens atau masalahnya; bisa diucapkan dalam 3 detik; **jujur** terhadap isi.
3. Uji cepat tiap hook: *"Kalau saya scroll, apakah ini menghentikan saya?"* dan *"Apakah ini menjanjikan sesuatu yang video ini benar-benar berikan?"*
4. Simpan 3 terbaik di naskah (utama + 2 varian A/B); setelah publish, catat pemenang ke `HOOKS_PROVEN.csv`.

### C. Naskah vertikal (struktur 5 blok)
```
[0.0-1.5s] HOOK          : kalimat + teks on-screen + gerakan visual
[1.5-5s]   KONTEKS       : kenapa penting untuk AUDIENS SPESIFIK (bukan umum)
[5-35s]    ISI 3 BEAT    : tiap beat = klaim → bukti/contoh → 1 kalimat ringkas
                           (catat pergantian visual tiap beat untuk editor)
[35-50s]   PAYOFF        : hasil + satu langkah pertama yang bisa dilakukan sekarang
[50-60s]   CTA           : SATU CTA saja
```
Tulis dalam dua kolom: `UCAPAN (VO/on-cam)` | `VISUAL/TEKS ON-SCREEN`. Ini langsung jadi shot list.

### D. Naskah long-form
Cold open (payoff di depan, tanpa intro) → peta video (3 hal yang didapat) → 3 bab (klaim-bukti-contoh-ringkasan) → jembatan retensi di akhir tiap bab → payoff akhir → CTA → end screen ke video terkait.
Tandai timestamp bab untuk deskripsi (chapter = penambah retensi & SEO).

### E. Carousel & thread
- Slide 1 = hook visual + ≤ 8 kata. Slide 2 = kenapa peduli. Slide 3–8 = satu poin per slide (klaim + bukti). Slide 9 = ringkasan. Slide 10 = CTA + nama seri.
- Thread: post 1 klaim berani + janji; post 2–3 bukti/data; sisanya langkah; post terakhir CTA + ajakan follow/repost.

### F. Newsletter & artikel SEO
Subjek ≤ 45 karakter, tanpa clickbait kosong. Struktur: satu ide → cerita/bukti → langkah → satu CTA. Artikel SEO: H1 mengandung keyword utama, H2 = pertanyaan yang diketik orang, 1.200–2.500 kata, ada tabel/checklist, internal link ke 2 artikel lain, schema FAQ bila memungkinkan.

### G. Naskah UGC berbayar (klien)
1. Baca brief klien; bila tidak ada, buatkan dari `templates/ugc-brief.md` dan minta approval.
2. Tulis **3 varian hook** + naskah 15–45 detik, gaya autentik (bukan iklan kaku): masalah nyata → produk masuk → bukti pakai → hasil → CTA.
3. Sertakan **shot list yang bisa direkam dengan HP** (sudut, durasi, properti, cahaya).
4. Patuhi batasan: tidak boleh klaim kesehatan/finansial tanpa dasar; disclosure bila perlu; tidak menjelekkan kompetitor dengan klaim palsu.
5. Output ke `project/<slug>/NASKAH.md` + `SHOTLIST.csv` untuk approval klien sebelum produksi.

### H. Caption/deskripsi (pola tetap)
```
Baris 1: hook/klaim (muncul sebelum "...more")
Baris 2: konteks atau angka bukti
Baris 3: CTA tunggal
Lalu: 3-5 hashtag (1 luas, 2 niche, 1 seri/merek) · kredit aset CC-BY · disclosure affiliate/AI
```

## Pitfalls

- **Jangan menulis "Halo guys, balik lagi…"** — buang 3 detik paling berharga.
- **Jangan menumpuk 3 CTA.** Satu CTA = satu tujuan (follower ATAU lead magnet ATAU pembelian).
- **Jangan klaim tanpa bukti.** Semua angka wajib ada di `SOURCES.md`.
- **Jangan generik.** Bila naskah bisa ditulis oleh siapa pun untuk akun mana pun, tambahkan sudut eksklusif (data sendiri, pengalaman sendiri, opini berisiko).
- **Jangan abaikan bahasa lisan.** Naskah dibaca keras; kalimat panjang = pembicara kehabisan napas = retensi turun.
- **Jangan menulis untuk semua orang.** Sebut audiens secara spesifik di 5 detik pertama.

## Verification

- `NASKAH.md` punya: 10 hook (3 terpilih), blok berlabel waktu, kolom visual, takeaway 1 kalimat, CTA tunggal, metadata (`format, platform, durasi, monetization, sources`).
- `SHOTLIST.csv` terisi (shot, deskripsi, durasi, tipe, catatan) dan jumlah durasi ≈ target.
- Uji baca keras: tidak ada kalimat > 20 kata; total kata sesuai durasi (≈ 150 kata/menit untuk VO Indonesia).
- Gerbang QA #1, #2, #5 dari `content-studio` sudah tercentang di `STATUS.md`.

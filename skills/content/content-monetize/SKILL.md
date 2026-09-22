---
name: content-monetize
description: "Rate card, media kit, proposal, invoice, outreach klien"
version: 1.0.0
author: Hermes Content Studio Pack
license: MIT
metadata:
  hermes:
    tags: [Content, Monetization, Sales, UGC, Clients]
    related_skills: [content-studio, content-legal, content-publish]
    blueprint:
      schedule: "0 20 * * 5"
      deliver: origin
      prompt: "Laporan cuan mingguan: rekap LEDGER.csv per jalur, rate efektif per jam, prospek terpanas, 3 tindakan minggu depan."
---

# Content Monetize

Mengubah keterampilan & aset konten menjadi uang: jasa UGC, brand deal, retainer, produk digital, membership, affiliate — dengan harga yang naik berbasis data.

## When to Use

- `/cuan`, "bikin rate card", "media kit", "proposal untuk brand X"
- "cara dapat uang dari konten", "berapa harga yang wajar"
- "outreach/pesan ke prospek", "follow up klien", "invoice"
- "laporan pendapatan", "naikkan harga?", "jalur mana yang paling untung"

## Quick Reference

| Deliverable | Template |
|---|---|
| Rate card | `templates/rate-card.md` (+ `scripts/ratecard.py`) |
| Media kit | `templates/media-kit.md` |
| Proposal brand deal | `templates/proposal-brand-deal.md` |
| Kontrak | `templates/kontrak-brand-deal.md` |
| Invoice | `templates/invoice.md` |
| Brief UGC (untuk klien isi) | `templates/ugc-brief.md` |
| Case study (aset penaik harga) | `templates/case-study.md` |
| Produk digital (outline) | `templates/produk-digital.md` |
| Kalender konten 30 hari | `templates/kalender-konten-30hari.md` |
| Buku kas | `scripts/ledger.py` → `LEDGER.csv` |

## Angka pasar 2026 (basis penawaran — jangan di bawah ini tanpa alasan strategis)

**UGC per video 15–60 dtk (pasar global):** pemula US$50–150 · menengah US$150–400 · berpengalaman US$400–800 · spesialis niche US$800–1.500+. Rata-rata pasar ≈ US$212 untuk satu video 30–60 dtk.
**Per jenis:** foto 3–5 pcs US$200–800 · unboxing US$250–1.200 · demo produk US$300–1.500 · testimonial US$400–2.000 · before/after US$350–1.800 · video tren US$200–800 · perbandingan US$400–1.600.
**Add-on (jangan pernah gratis):** paid ads 3–6 bln +30–50% · 12 bln/multi-platform +50–100% · perpetual/buyout +100–200% · whitelisting/Spark +US$150–300/bln · eksklusivitas kategori +US$150–300/bln · raw footage +US$100 · rush <72 jam +50% · revisi ekstra +US$50–100/ronde · varian hook +US$30–75.
**Brand deal per post:** nano (1k–10k) US$100–500 · micro (10k–100k) US$500–5.000 · macro US$5.000–10.000 · mega US$10.000+.
**Jalur lain:** membership US$10–50/bln per member · kursus US$100–500 · coaching US$100–300/jam · produk digital US$20–200 · affiliate 5–30% · setup sistem otomatis untuk klien US$500–2.000 · retainer US$800–4.000/bln.
**Indonesia 2026 (platform):** TikTok Shop Affiliate — 18+, ≥600–1.000 follower (atau lewat Seller Center tanpa syarat follower), KTP + rekening, komisi 5–20%, akun <5.000 follower dibatasi 3 video shoppable/hari & 3 live shoppable/minggu; **Creator Rewards belum tersedia di Indonesia**. YouTube YPP — Tier 1: 500 subs + 3 upload/90 hari + (3.000 jam tayang/365 hari ATAU 3 juta views Shorts/90 hari) untuk fan funding & Shopping; Tier 2: 1.000 subs + (4.000 jam/12 bln ATAU 10 juta views Shorts/90 hari) untuk iklan. LIVE Gifts TikTok: ≥1.000 follower + pernah LIVE ≥30 menit/28 hari.
Kalikan rate global ×0,3–0,5 untuk UMKM lokal; brand nasional/klien asing mendekati rate global. **Selalu dua mata uang** (IDR/USD).

## Procedure

### A. `rate-card`
1. Kumpulkan bukti: `CONTENT_INDEX.csv` (views/engagement), `LEDGER.csv` (jam & pendapatan), testimoni, sertifikat, niche.
2. Tentukan posisi: pemula / menengah / spesialis. Jangan memposisikan diri di atas bukti yang ada.
3. Jalankan `python3 scripts/ratecard.py --profile workspace/BRAND.md --level intermediate --currency IDR,USD --out workspace/output/rate-card.md`.
4. Susun 3 paket (Starter 3 video, Growth 5 video, Scale 10 video) + retainer 8/12/20 aset + tabel add-on + terms (DP 50%, kill fee 25%, pelunasan sebelum file final, hak cipta beralih setelah lunas).
5. **Aturan naik harga:** bila 3 klien berturut-turut menerima tanpa menawar → naikkan 25%. Bila budget klien kecil → kurangi deliverable, **jangan** turunkan harga per video.

### B. `media-kit`
Satu halaman: siapa Anda + niche + angka audiens (follower, views median, engagement rate, demografi) + 3 case study mini + layanan & harga mulai dari + testimoni + kontak + tautan portofolio. Jujur soal angka: **views median** lebih dipercaya brand daripada total.

### C. `proposal <prospek>`
1. Riset prospek 5 menit: produk, iklan yang sedang jalan (Meta Ad Library/TikTok Creative Center), gaya konten mereka, celah yang terlihat.
2. Struktur 1 halaman: masalah spesifik mereka → pendekatan kita (3 konsep hook konkret) → deliverable & timeline → investasi (2 opsi: paket + retainer) → bukti → langkah berikutnya (call 20 menit).
3. Lampirkan **1 contoh gratis berukuran kecil** (mis. hook 15 detik) — bukan proyek penuh gratis.
4. Simpan di `workspace/output/proposals/`, catat prospek ke `CLIENTS.csv` (tahap: lead → kontak → proposal → negosiasi → deal → delivery → repeat).

### D. `outreach` (20 prospek/hari)
Pesan 4 kalimat: observasi spesifik → bukti relevan → tawaran kecil (3 konsep hook gratis) → pertanyaan penutup. Follow-up hari ke-4 dengan draft terlampir + opsi "bulan depan". Simpan template di `templates/outreach.md`, catat tingkat balas di `CLIENTS.csv`.
Sumber prospek: brand yang sudah beriklan di niche Anda, startup baru launch (GitHub Trending/Product Hunt), agensi sosial media 10–50 orang, UMKM dengan konten lemah, kreator besar yang butuh editor/clipper, platform freelance (Upwork, Fiverr, Projects.co.id, Fastwork, Sribulancer).

### E. `invoice` & administrasi
Nomor urut + tanggal + data kedua pihak (termasuk NPWP) + rincian deliverable & usage rights + termin + metode bayar. Minta **bukti potong PPh 21/23** dari klien badan. Simpan di `workspace/data/invoices/`. (Bukan nasihat pajak — konfirmasi ke AR/konsultan.)

### F. Produk digital & membership (aset berulang)
1. Cari template/SOP yang sudah dipakai ≥ 5 kali dan berhasil → kemas jadi produk (template pack, preset, prompt pack, dataset, playbook, kelas).
2. Harga: US$9–49 (template/preset), US$49–149 (playbook/prompt pack), US$99–499 (dataset/laporan), US$100–500 (kelas).
3. Jual via Ghost (MIT, 0% potongan) atau Medusa (MIT) untuk margin maksimal; Ko-fi/Gumroad untuk mulai cepat.
4. Membership: 3 tier (gratis / US$5 / US$20) dengan nilai jelas per tier; target 300 member × US$5 = US$1.500/bln.

### G. Laporan cuan (cron Jumat 20.00)
```bash
python3 scripts/ledger.py summary workspace --days 7
```
Wajib berisi: pendapatan per jalur, jam total, **rate efektif per jam per jalur**, tren vs minggu lalu, prospek terpanas, 3 tindakan. Lalu rekomendasikan **memotong jalur dengan rate efektif terendah** — itu keputusan paling menguntungkan yang jarang dilakukan kreator.

## Pitfalls

- **Jangan kerja tanpa DP & kontrak.** Minimal DP 50% + brief tertulis yang di-approve.
- **Jangan beri usage rights/perpetual/eksklusivitas gratis** — ini 50–200% dari nilai pekerjaan.
- **Jangan menjanjikan views/konversi.** Janjikan deliverable + proses; hasil dibahas sebagai estimasi.
- **Jangan turunkan harga saat ditolak** — kurangi cakupan. Harga yang jatuh sulit dinaikkan lagi.
- **Jangan mengarang statistik audiens.** Brand mengecek; sekali ketahuan, reputasi habis.
- **Jangan bergantung pada satu jalur.** Target 3 jalur aktif (creator dengan 3+ jalur berpenghasilan jauh lebih tinggi).
- **Jangan tunggu bagi hasil platform** sebagai fondasi — di Indonesia Creator Rewards TikTok belum tersedia; YouTube butuh ambang. Jasa & produk digital membayar lebih cepat.

## Verification

- Deliverable berbentuk file di `workspace/output/` (rate-card.md, media-kit.md, proposal, invoice), bukan hanya teks chat.
- `CLIENTS.csv` diperbarui (tahap, nilai, tanggal follow-up berikutnya).
- `LEDGER.csv` punya baris pendapatan & jam untuk setiap pekerjaan; rate efektif terhitung.
- Setiap penawaran mencantumkan: harga, usage rights, exclusivity, jumlah revisi, timeline, termin DP, kill fee.

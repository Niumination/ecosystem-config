# Toolkit Gratis Luar Composio — Katalog

> **Rumah katalog** untuk toolkit free-tier **di luar** Composio (Kelas B — toolkit dalam Composio — ada di `composio-integration-plan.md`).
> **Asal isi:** dipindah dari §A `composio-integration-plan.md` pada 2026-09-16 (one-home rule: daftar ini satu rumah saja, plan hanya menunjuk ke sini).
> **Status verifikasi: DIPERBARUI 18 Sep 2026** — angka di bawah dicek langsung ke halaman resmi masing-masing tool (kolom *Sumber*). Angka tetap punya tanggal kedaluwarsa: sebutkan tanggal verifikasi saat mengutip ke pengguna/klien, dan cek ulang sebelum dipakai jadi janji komersial.

## Katalog — terverifikasi 18 Sep 2026

| Tool | Free tier (per 18-Sep-2026) | Pembatas penting | Sumber resmi | Cocok pilar |
|---|---|---|---|---|
| **Meta Business Suite** | Gratis (alat native Meta, tanpa langganan) | Jadwal post FB: **20 menit – 29 hari** ke depan; reels FB & IG **bisa** dijadwalkan; IG dibatasi 10 foto per post | `facebook.com/help/389849807718635`, `facebook.com/business/help/794942355314453` | `Behind the Build`, `Aceh Pride` |
| **Penjadwal native Instagram (app)** | Gratis | **25 post/hari, maksimum 30 hari** ke depan; mendukung reels/foto/carousel; akun harus publik; tanpa pihak ketiga | `help.instagram.com/439971288310029` | Semua pilar (jalur paling sederhana untuk reels) |
| **Buffer (Free)** | 3 kanal · **10 post terjadwal per kanal** (isi ulang kapan saja) · 1 user · API 1 kunci, 3.000 request/bulan | Publikasi otomatis IG butuh akun Instagram **Business/Creator** | `buffer.com/pricing`, `support.buffer.com` (Using Instagram with Buffer) | Kalender 30-hari posting |
| **Pallyy (Free)** | 1 social set · **15 post terjadwal/bulan** · tanpa kartu kredit | **Hanya gambar — publikasi video tidak termasuk.** Reels **tidak bisa** lewat free tier | `pallyy.com/pricing` | Konten carousel/feed statis |
| **Postiz** | **Self-hosted: gratis penuh (AGPL-3.0), 34 platform, tanpa batas kanal.** **Cloud: TIDAK ADA free plan** (hanya trial 7 hari) | Butuh server/VM sendiri (jangan di laptop 16 GB — lihat larangan resource di `docs/references/`) | `docs.postiz.com/cloud/overview`, `docs.postiz.com/general/introduction`, `github.com/gitroomhq/postiz-app` | Semua pilar — satu-satunya jalur gratis tanpa batas jumlah |
| **Make.com (Free)** | 1.000 credit/bulan · **maksimum 2 skenario aktif** · interval minimum 15 menit antar-run | Credit dihitung per aksi modul; cocok uji coba, bukan produksi harian | `make.com/en/pricing` | Otomatisasi pipa produksi (uji coba) |
| **Canva (Free)** | US$0 — 1.000+ tipe desain, 1,6 jt template, 5 GB storage, 1 Brand Kit (3 warna saja), maksimum 20 pemakaian AI standar/premium | **Penjadwalan ke sosial media hanya untuk Pro/Business/Education/Nonprofits** — akun Free hanya bisa menautkan 1 akun per platform | `canva.com/pricing`, `canva.com/help/content-planner` | Aset desain 9:16, infografis (bukan distribusi) |
| **Zernio** | **2 akun pertama gratis** (tanpa kartu kredit), seluruh fitur terbuka | Mulai akun ke-3: $6/akun/bulan (3–10 akun), $3/akun (11–100). Billing per akun, bukan per paket | `zernio.com/pricing` | API layer multi-platform |
| **Meta Ads Manager** | Gratis (alat native) | Biaya hanya belanja iklan; tidak ada penjadwalan organik | (native Meta) | Promo paid reels bila diperlukan |

## Koreksi angka lama

| Tool | Klaim lama (18 Agu 2026) | Fakta 18 Sep 2026 |
|---|---|---|
| **Ocoya** | tercantum sebagai opsi gratis (AI caption + scheduling) | **Tidak ada free plan.** Starter $29/bln, Team $79/bln, Agency $199/bln — hanya 7 hari trial. Dikeluarkan dari daftar gratis. Sumber: `ocoya.com/pricing` |
| **Meta Business Suite** | "Unlimited" | Klaim "unlimited" tanpa syarat itu **menyesatkan**: jumlah post tidak dibatasi, tetapi jendela penjadwalan FB hanya sampai **29 hari** ke depan |
| **Pallyy** | "Free forever, 1 profile" | Benar, tetapi **15 post/bulan dan gambar saja** — tidak untuk reels |
| **Postiz** | "Total gratis" (tanpa kualifikasi) | Benar **hanya untuk self-hosted**; layanan cloud-nya **tanpa free plan** |
| **Postiz platform** | "Semua platform" | 34 platform (angka resmi docs) |
| **Zernio** | "Unified API 15 platform" | Angka 15 tidak ditemukan di halaman resmi; yang resmi: **2 akun pertama gratis**, cakupan social + blogs + ads + messaging |
| **Canva** | "Desain & video edit, 9:16, infografis" | Benar untuk desain; **penjadwalan sosial bukan fitur Free** |
| **Make.com** | "1.000 ops/bulan" | 1.000 **credit**/bulan + batas **2 skenario aktif** + interval minimum 15 menit |

## Konsekuensi untuk kalender konten 30 hari

1. **Jendela 29 hari Meta** vs kalender 30 hari → konten hari ke-30 harus dijadwalkan ulang saat hari ke-1 tayang. Untuk reels, penjadwal native Instagram memberi jendela 30 hari (25 post/hari).
2. **Reels tidak bisa lewat Pallyy Free** (gambar saja). Jalur gratis untuk reels: native Instagram, atau Buffer Free (3 kanal × 10 post terjadwal), atau Postiz self-hosted.
3. **Canva Free tidak mengirim ke sosial** → ekspor aset (9:16), lalu jadwalkan via Buffer / Meta Business Suite / native IG.
4. **Tanpa batas jumlah = Postiz self-hosted.** Itu satu-satunya opsi gratis yang tidak dibatasi kuota post; konsekuensinya butuh VM dan perawatan sendiri.
5. **Otomatisasi Make.com Free praktis untuk uji coba saja** — 2 skenario aktif dan interval 15 menit tidak cukup untuk pipeline harian.

## Catatan pemakaian

- **Yang belum diverifikasi ulang jangan dijanjikan** ke pengguna/klien: sebutkan tanggal verifikasi saat mengutip angka.
- **Nilai "2 skenario aktif" Make.com Free** berasal dari tabel perbandingan resmi + dokumentasi komunitas; konfirmasi ulang saat mendaftar bila angka ini dipakai untuk keputusan anggaran.
- **Buffer vs Pallyy**: Buffer lebih luas platform dan mendukung reels; Pallyy Free lebih ketat (gambar saja) tetapi longgar untuk akun tunggal.
- **Postiz self-hosted** satu-satunya opsi tanpa batas — tapi menuntut VM.
- **Composio (Kelas B)** punya free tier sendiri; lihat `composio-integration-plan.md` untuk jalur MCP/API.
- **Skill `skills/creative/free-tier-reels` belum diselaraskan** dengan tabel ini (masih menyebut Canva/Pallyy/Meta sebagai jalur gratis tanpa catatan pembatas) — perubahan skill bank menunggu approval pemilik.

## Terkait

- `docs/registry/composio-integration-plan.md` — plan integrasi lengkap (Kelas B + 8 langkah)
- `skills/creative/free-tier-reels/SKILL.md` — pemakaian praktis untuk produksi Reels (belum diselaraskan)
- `docs/reports/KONTEN-KREATOR-STATUS-2026-09-18.md` — status ekosistem untuk kebutuhan konten kreator
- `AGENTS.md` — Global Agent Rules (termasuk One-home rule)

---

*Dibuat 2026-09-16 dari pemindahan §A `composio-integration-plan.md`; angka free-tier diverifikasi ulang langsung ke halaman resmi pada 18 Sep 2026.*

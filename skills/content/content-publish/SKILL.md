---
name: content-publish
description: "Adaptasi multi-platform, penjadwalan, dan analitik"
version: 1.0.0
author: Hermes Content Studio Pack
license: MIT
metadata:
  hermes:
    tags: [Content, Publishing, Scheduling, Analytics, Distribution]
    related_skills: [content-studio, content-produce]
    blueprint:
      schedule: "0 16 * * *"
      deliver: origin
      prompt: "Repurpose engine: ambil 1 konten terbaik dari CONTENT_INDEX.csv, hasilkan 5 turunan lintas platform."
required_environment_variables:
  - name: POSTIZ_URL
    prompt: "URL instance Postiz/Mixpost self-host"
    help: "Contoh: https://postiz.domainanda.com"
    required_for: "Menjadwalkan & mempublikasikan ke banyak platform"
  - name: POSTIZ_API_KEY
    prompt: "API key scheduler"
    help: "Dari dashboard Postiz (Settings → API) atau Mixpost (Personal Access Token)"
    required_for: "Mengirim post terjadwal lewat API"
---

# Content Publish

Satu konten menjadi banyak aset lintas platform, terjadwal otomatis, dan terpantau hasilnya.

## When to Use

- `/publish <slug>`, "jadwalkan", "posting ke semua platform"
- "adaptasikan video ini untuk LinkedIn/X/newsletter"
- "repurpose", "bikin turunan dari konten lama"
- "cek performa", "laporan analitik", "apa yang harus diperbaiki"

## Quick Reference

| Kebutuhan | Stack | Catatan |
|---|---|---|
| Scheduler multi-platform | **Postiz** (AGPL, self-host, 20+ jaringan, API publik + **MCP server**) | Pilihan utama: Hermes bisa memanggilnya sebagai MCP tool |
| Alternatif scheduler | **Mixpost Lite** (open source, Laravel) | UI lebih ramah non-teknis; Pro = lisensi sekali bayar |
| Otomasi alur | **Activepieces** (MIT), **Automatisch** (AGPL), **Huginn** (MIT) | n8n boleh dipakai sendiri (fair-code), jangan dijual ulang |
| Kanal milik sendiri | **Ghost** (MIT) blog+newsletter+membership · **Listmonk** (AGPL) blast | Aset paling eksklusif |
| Fediverse | Mastodon, Lemmy, Pixelfed, PeerTube, Brid.gy | Jangkauan tambahan tanpa algoritma sewa |
| Analitik web | **Umami** (MIT), **Plausible** (AGPL), **Matomo** (GPL) | Landing page/blog |
| Analitik platform | YouTube Studio, TikTok Analytics, IG Insights, LinkedIn Analytics | Tarik manual/`web_extract` → `CONTENT_INDEX.csv` |

## Procedure

### A. Adaptasi satu aset ke semua platform
Dari `output/MANIFEST.md` satu proyek, hasilkan paket berikut (simpan sebagai file, jangan cuma ditempel di chat):

| Platform | Berkas | Copy |
|---|---|---|
| TikTok | `tiktok_1080x1920.mp4` + `.srt` | caption 1 baris hook + 4 hashtag |
| IG Reels | `reels_1080x1920.mp4` + cover 1080×1920 | caption 2 baris + CTA + hashtag |
| IG/LinkedIn carousel | 8–10 PNG 1080×1350 | post 1 = hook, post akhir = CTA |
| YouTube Shorts | `shorts_1080x1920.mp4` | judul mengandung keyword + deskripsi + tag |
| YouTube long-form | `yt_1920x1080.mp4` + 3 thumbnail | judul ≤ 60 char, deskripsi ber-chapter, end screen |
| LinkedIn video | `li_1080x1080.mp4` atau dokumen PDF | 3 baris pertama = hook; tone lebih profesional |
| X/Bluesky | `x_1920x1080.mp4` + thread 5–9 post | post 1 klaim + bukti |
| Newsletter | `newsletter.md` | subyek ≤ 45 char, 1 ide, 1 CTA |
| Blog/SEO | `artikel.md` + OG image 1200×630 | H1 keyword, H2 pertanyaan, schema FAQ |
| Pinterest | `pin_1000x1500.jpg` | judul evergreen mengandung keyword |

Aturan adaptasi: **bukan sekadar ubah ukuran.** Ubah hook (tiap platform punya budaya berbeda), panjang, dan CTA. TikTok/Reels = cepat & mentah; LinkedIn = profesional + insight bisnis; YouTube = kedalaman + chapter; newsletter = intim + satu ide.

### B. Penjadwalan
1. Baca kalender (`workspace/data/CALENDAR.csv`) → slot kosong berikutnya.
2. Kirim ke scheduler:
```bash
curl -s -X POST "$POSTIZ_URL/api/public/v1/posts" \
  -H "Authorization: Bearer $POSTIZ_API_KEY" -H "Content-Type: application/json" \
  -d @project/<slug>/output/schedule.json
```
   (Bila Postiz MCP sudah dipasang di Hermes → panggil tool-nya langsung, lebih andal.)
3. Status `draft` dulu untuk review manusia; ubah ke `scheduled` setelah approve di topic.
4. Jam awal sebagai hipotesis (WIB): 06.30–08.00 · 12.00–13.00 · 19.00–21.00. Setelah 20 post, pakai data sendiri.

### C. Repurpose engine (otomatis tiap hari 16.00)
1. Pilih 1 konten terbaik 30 hari terakhir dari `CONTENT_INDEX.csv` (skor: engagement rate + save/share).
2. Hasilkan 5 turunan: short baru (hook berbeda), carousel, thread, newsletter, kutipan grafis SVG.
3. Simpan di `workspace/project/repurpose-<tanggal>/`, daftarkan ke kalender.
4. Aturan **1-3-9**: 1 long-form → 3 shorts → 9 mikro.

### D. Analitik & pelaporan
1. Tiap 7 hari, isi `CONTENT_INDEX.csv`: views, likes, komentar, share, save, follower baru, klik link, pendapatan terkait.
2. Hitung: CTR (YouTube), retensi 30 dtk, AVD, engagement rate = (like+komen+share+save)/follower, konversi lead = lead/views.
3. Diagnosa wajib (jangan menebak): CTR rendah = kemasan; retensi rendah = struktur/isi; konversi rendah = CTA/penawaran.
4. Usulkan **satu** eksperimen A/B untuk minggu depan → catat di `AB_LOG.csv`.

### E. Distribusi tambahan (gratis, sering dilupakan)
- Unggah ke kanal milik sendiri (Ghost/blog) → SEO jangka panjang.
- Syndicate ke fediverse (Mastodon/Lemmy/Pixelfed/PeerTube) via Brid.gy.
- Kirim ke newsletter komunitas niche (bukan spam: satu nilai nyata + satu link).
- Bagikan ke grup Telegram/Discord/WhatsApp yang relevan **dengan izin aturan grup**.
- Jawab pertanyaan di forum (Reddit, StackOverflow, Kaskus) dengan nilai nyata + tanda tangan halus.

## Pitfalls

- **Jangan cross-post identik.** Watermark TikTok di Reels menurunkan jangkauan; copy-paste caption terlihat malas.
- **Jangan publish sebelum QA lolos** (skor ≥ 70 dari `content-studio`).
- **Jangan melanggar batas API/rate limit** platform; gunakan antrean dan retry.
- **Jangan menjadwalkan konten berhak cipta** (musik chart, klip film) — klaim datang belakangan dan memotong pendapatan.
- **Jangan percaya angka pihak ketiga** untuk negosiasi; pakai analitik native + `LEDGER.csv`.
- **Secret bocor**: `POSTIZ_API_KEY` hanya dari environment, jangan ditulis di file proyek atau chat.
- **AGPL ragu?** Self-host Postiz untuk kebutuhan sendiri/klien tidak mewajibkan membuka kode; kalau tetap ragu → Mixpost Lite.

## Verification

- `schedule.json` terkirim dan scheduler mengembalikan ID post (simpan di `MANIFEST.md`).
- Setiap platform punya berkas dengan rasio/durasi benar (cek `ffprobe`).
- `CONTENT_INDEX.csv` punya baris baru dengan URL + tanggal publish + jalur monetisasi.
- `CALENDAR.csv` diperbarui; tidak ada dua post bertabrakan di slot yang sama.
- Laporan ke pengguna: daftar platform, jam tayang, link, dan satu metrik yang akan dipantau.

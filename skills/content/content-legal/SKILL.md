---
name: content-legal
description: "Audit lisensi, AI disclosure, izin, dan kontrak konten"
version: 1.0.0
author: Hermes Content Studio Pack
license: MIT
metadata:
  hermes:
    tags: [Content, Legal, License, Compliance, Contracts]
    related_skills: [content-studio, content-produce, content-monetize]
    blueprint:
      schedule: "0 9 * * 1"
      deliver: origin
      prompt: "Audit mingguan: jalankan scripts/license_audit.py atas workspace, tandai aset non-komersial atau tak tercatat, usulkan pengganti open source."
---

# Content Legal

Menjaga agar semua yang Anda publikasikan dan jual **bersih secara hukum** — inilah yang membuat brand berani membayar mahal dan platform tidak mematikan monetisasi Anda.

> Panduan operasional, bukan nasihat hukum. Untuk kontrak besar atau sengketa, libatkan konsultan hukum lokal.

## When to Use

- `/audit`, "cek lisensi", "aman dipakai komersial?"
- sebelum publish konten yang memuat musik, footage, gambar, font, atau wajah orang
- sebelum deliver ke klien (UGC/brand deal)
- saat memasang tool/model/dependensi baru
- "bikin kontrak/NDA/model release", "kena klaim hak cipta", "dapat teguran"

## Quick Reference

| Tugas | Perintah |
|---|---|
| Audit lisensi dependensi & aset | `python3 scripts/license_audit.py --dir workspace --report workspace/data/LICENSE_REPORT.md` |
| Cek lisensi paket Python | `pip-licenses --format=markdown` (atau `pip install pip-licenses`) |
| Cek lisensi paket Node | `npx license-checker --summary` |
| Lihat lisensi repo | `curl -s https://api.github.com/repos/<owner>/<repo>/license` |
| Daftar aset per proyek | `workspace/data/ASSETS_LICENSE.csv` |
| Sumber klaim | `project/<slug>/SOURCES.md` |

**Whitelist aman komersial:** MIT · BSD-2/3 · ISC · Apache-2.0 · CC0 · CC-BY 4.0 (atribusi wajib) · OFL (font) · MPL-2.0 · LGPL · GPL/AGPL (untuk *memakai tool*; distribusi/layanan punya kewajiban) · OpenRAIL++-M · Community License di bawah ambang (Stability/Hunyuan/LTX).
**Blacklist (jangan untuk konten berbayar):** CC-BY-NC(-SA) · Coqui Public Model License (XTTS v2) · F5-TTS weights · Fish Speech varian terbuka · FLUX.1 [dev] · FLUX.2 [dev] · Stable Video Diffusion (banyak checkpoint) · Wav2Lip · SadTalker · V-Express · font "free for personal use" · musik chart/berhak cipta lintas platform · fair-code yang dijual ulang sebagai layanan (mis. n8n Sustainable Use).

## Procedure

### A. Audit pra-publish (setiap proyek, gerbang QA #6)
1. Kumpulkan daftar aset: video/gambar/audio/font/model yang dipakai di `project/<slug>/assets/`.
2. Cocokkan dengan `ASSETS_LICENSE.csv`. Bila ada yang belum tercatat → cari sumber & lisensinya sekarang; bila tidak ditemukan → **hapus dan ganti**.
3. Jalankan `scripts/license_audit.py`; perbaiki semua `FAIL`.
4. Cek khusus:
   - Musik: pakai ACE-Step/CC0/Freesound CC0 atau YouTube Audio Library sesuai platform. **Musik berhak cipta memotong pool pendapatan Shorts** (1 trek → 50%, 2 trek → 33%).
   - Wajah/suara orang: ada `model-release.md` tertanda? Bila tidak → blur/ganti.
   - Merek/logo pihak ketiga: hanya untuk keperluan editorial/review yang jujur; jangan menyiratkan endorsement tanpa izin.
   - Data pribadi: plat nomor, alamat, email, dashboard berisi nama pelanggan → sensor.
   - Font: OFL/Apache saja; bukan "personal use".
5. Tulis keputusan di `STATUS.md`: `LEGAL: PASS/FAIL + catatan`.

### B. AI disclosure
1. Tandai bila konten memakai gambar/suara/video generatif yang tampak realistis.
2. YouTube: aktifkan label "altered/synthetic content". TikTok: label AI-generated. Meta/IG: self-declare untuk konten realistis. LinkedIn: sebutkan di post untuk B2B.
3. Audiens/klien UE: perhatikan kewajiban AI Act untuk deepfake/konten sintetis.
4. Kebijakan internal (tulis di `BRAND.md`): "Kami menandai media generatif. Kami tidak membuat gambar/suara orang nyata tanpa izin tertulis. Kami tidak mengklaim hasil yang tidak terukur."

### C. Kontrak & dokumen (pakai template di `templates/`)
Untuk setiap pekerjaan berbayar, pastikan ada: ruang lingkup deliverable · jadwal approval & delivery · jumlah ronde revisi · harga + **DP 50%** + pelunasan sebelum file final + **kill fee 25–50%** · **usage rights** (durasi, wilayah, kanal organic/paid, boleh diedit atau tidak) · **eksklusivitas** (kategori + durasi + harga) · hak cipta beralih setelah lunas · hak memajang di portofolio · representasi & garansi (orisinalitas, aset berlisensi) · AI disclosure · kerahasiaan · pembatasan tanggung jawab · force majeure · yurisdiksi · lampiran brief & storyboard yang di-approve.

Model release: identitas pihak, cakupan penggunaan (media, wilayah, durasi, komersial), pernyataan tidak ada imbalan/ada imbalan, tanda tangan + tanggal (+ wali bila di bawah umur).

### D. Menanggapi klaim/teguran
1. Jangan panik-delete; **dokumentasikan** dulu (screenshot klaim, tanggal, aset yang dipersoalkan).
2. Identifikasi aset bermasalah → cek `ASSETS_LICENSE.csv`.
3. Bila memang keliru: hapus/ganti aset, ajukan banding dengan bukti lisensi bila ada, catat pelajaran di `MEMORY.md`.
4. Bila klaim salah: siapkan bukti (lisensi, tanggal unduh, sumber, rekaman asli) dan ajukan counter-notice.
5. Bila menyangkut uang besar atau berulang → konsultan hukum.
6. Perbaiki sistem: tambahkan pemeriksaan baru ke checklist agar tidak terulang.

### E. Audit dependensi/tool baru (sebelum dipasang)
1. Baca LICENSE di repo + halaman model (Hugging Face) — jangan hanya README.
2. Cek apakah lisensi **berubah** sejak Anda terakhir pakai (risiko nyata: proyek yang pindah ke non-komersial).
3. Untuk AGPL: aman bila self-host untuk keperluan sendiri/klien; bila Anda menjualnya sebagai layanan → sediakan sumber.
4. Untuk fair-code (n8n Sustainable Use, Elastic, BSL): pakai sendiri OK, jual ulang sebagai layanan TIDAK.
5. Catat keputusan di `workspace/data/TOOL_DECISIONS.csv`: tool, versi, lisensi, verdict, tanggal review berikutnya (90 hari).

## Pitfalls

- **"Gratis" ≠ "boleh dijual".** Selalu bedakan: gratis dipakai vs lisensi output komersial.
- **Lisensi model ≠ lisensi output**, tapi untuk model NC, output ikut tercemar.
- **CC-BY tanpa atribusi** = pelanggaran, walau asetnya gratis. Simpan teks atribusi dan tempel di deskripsi + end-card.
- **Fine-tune mewarisi lisensi data latih** (contoh: F5-TTS/Emilia → NC menular).
- **Jangan reupload karya kreator lain.** Selain ilegal, ini menghancurkan nilai "eksklusif" yang justru Anda jual.
- **Jangan klaim medis/finansial tanpa dasar** — risiko hukum tertinggi dalam konten UGC.
- **Jangan tanda tangan kontrak tanpa klausul usage rights & kill fee** — itu sumber kerugian paling umum.
- **Jangan simpan bukti lisensi hanya di kepala/chat.** File CSV adalah pertahanan Anda saat ada sengketa.

## Verification

- `LICENSE_REPORT.md` terbaru ada, tanpa entri `FAIL` yang belum ditangani.
- Setiap aset proyek punya baris di `ASSETS_LICENSE.csv` dengan `aman_komersial = ya`.
- `STATUS.md` memuat `LEGAL: PASS` sebelum publish/delivery.
- Konten realistis hasil AI sudah ditandai sesuai kebijakan platform tujuan.
- Untuk pekerjaan berbayar: kontrak + DP tercatat di `workspace/data/invoices/` dan `LEDGER.csv`.

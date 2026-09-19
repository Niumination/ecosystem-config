# Free-tier kanal produksi & distribusi konten — fakta terverifikasi

> **Snapshot verifikasi: 18 Sep 2026**, dicek langsung ke halaman resmi tiap vendor.
> **Cara pakai:** ini titik awal, bukan sumber kebenaran abadi. Angka free-tier berubah; sebelum mengutip ke pemilik/klien, buka ulang URL di kolom Sumber dan perbarui tanggal di header. Jangan kutip angka dari file ini tanpa menyebut tanggal verifikasinya.
> **Rumah data:** `docs/registry/composio-free-tier-tools.md` (katalog luar Composio) + `docs/registry/composio-integration-plan.md` (rencana integrasi). File ini hanya ringkasan verifikasi + aturan penilaian.

## Angka terverifikasi

| Tool | Free tier | Batas yang paling sering kelewat | Sumber resmi |
|---|---|---|---|
| Meta Business Suite | Gratis (alat native Meta) | Jadwal post FB hanya **20 menit – 29 hari** ke depan; reels FB & IG bisa dijadwalkan; IG dibatasi 10 foto/post | `facebook.com/help/389849807718635`, `facebook.com/business/help/794942355314453` |
| Penjadwal native Instagram (app) | Gratis | **25 post/hari, maksimum 30 hari** ke depan; reels/foto/carousel; akun harus publik | `help.instagram.com/439971288310029` |
| Buffer | Free: 3 kanal · 10 post terjadwal per kanal · 1 user · API 1 kunci 3.000 req/bulan | Publikasi otomatis IG butuh akun Business/Creator; kuota post diisi ulang (refill), bukan "unlimited" | `buffer.com/pricing`, `support.buffer.com` |
| Pallyy | Free: 1 social set · 15 post/bulan | **Gambar saja — publikasi video tidak termasuk** | `pallyy.com/pricing` |
| Postiz | **Self-hosted gratis penuh** (AGPL, 34 platform, tanpa batas kanal) | **Cloud: tidak ada free plan** (trial 7 hari saja); self-host butuh VM | `docs.postiz.com/cloud/overview`, `docs.postiz.com/general/introduction`, `github.com/gitroomhq/postiz-app` |
| Make.com | Free: 1.000 credit/bulan | **Maksimum 2 skenario aktif**, interval minimum 15 menit → uji coba, bukan produksi harian | `make.com/en/pricing` |
| Canva | Free: desain (1.000+ tipe, 1,6 jt template, 5 GB, 1 brand kit 3 warna, ≤20 pemakaian AI) | **Penjadwalan ke sosial hanya Pro/Business/Education/Nonprofits** | `canva.com/pricing`, `canva.com/help/content-planner` |
| Zernio | Free: **2 akun pertama** (tanpa kartu), semua fitur terbuka | Akun ke-3+: $6/akun (3–10), $3/akun (11–100); billing per akun | `zernio.com/pricing` |
| BigQuery (analitik) | 1 TiB query + 10 GiB penyimpanan per bulan | Kelebihan = tagihan on-demand | `cloud.google.com/bigquery` |
| Ocoya | **Tidak gratis** — Starter $29/bln | Hanya trial 7 hari; tidak punya kolom $0 | `ocoya.com/pricing` |

## Jebakan yang membuat angka lama salah (pola berulang)

1. **Nama paket dibaca, matriks kapabilitas tidak.** Pallyy "free forever" ternyata gambar saja → tidak bisa dipakai untuk reels. Selalu cek baris kapabilitas (video/publikasi/penjadwalan) di tabel perbandingan.
2. **Self-hosted dicampur dengan cloud.** Postiz benar-benar gratis sebagai self-hosted, tapi cloud-nya tidak punya free plan. Tulis jalurnya, bukan hanya nama produk.
3. **"Unlimited" menyembunyikan jendela.** Meta Business Suite tanpa batas jumlah post, tapi jendela FB hanya 29 hari — lebih pendek dari kalender 30 hari. Selalu bandingkan batas jendela dengan horizon rencana konten.
4. **Trial dihitung sebagai free.** Ocoya hanya punya trial 7 hari. Kalau daftar paket tidak memuat $0, produk itu berbayar.
5. **Angka dari agregator/blog dipakai sebagai fakta.** Halaman komparasi pihak ketiga sering basi. Ambil dari halaman pricing/help vendor; kalau nilai hanya tersedia di tabel perbandingan atau forum, tandai tingkat keyakinannya di dokumen.
6. **Fitur desain dianggap fitur distribusi.** Canva Free bagus untuk aset, tapi tidak mengirim ke sosial. Pisahkan baris "produksi aset" dan "distribusi".
7. **Klaim turunan yang tidak ada di sumber** (mis. "N platform" pada sebuah API) ikut terwarisi dari dokumen lama. Kalau tidak ditemukan di halaman resmi, hapus klaimnya — jangan haluskan dengan kata "sekitar".

## Konsekuensi praktis untuk kalender 30 hari

- Jendela 29 hari (Meta FB) < 30 hari → konten hari ke-30 dijadwalkan ulang saat hari ke-1 tayang.
- Reels gratis tanpa biaya: penjadwal native Instagram, atau Buffer Free (3 kanal × 10 post terjadwal).
- Canva Free menghasilkan aset, bukan tayangan: ekspor 9:16 lalu jadwalkan lewat Buffer / Meta Business Suite / native IG.
- Tanpa batas jumlah = Postiz self-hosted, dengan konsekuensi VM + perawatan sendiri.

# Studi: Slim.sh dan Kickbacks.ai

Tanggal riset: 2026-09-28
Metode: pencarian web, pengambilan dokumen resmi, probe DNS/HTTP langsung, GitHub API
Status: 2 dari 2 berhasil

## Ringkas

| Target | Status | Hasil |
| --- | --- | --- |
| Slim.sh | Berhasil | Dev tool Go untuk localhost HTTPS + tunnel publik. Tidak terpasang di sistem. |
| Kickbacks.ai | Berhasil | Monetisasi wait-state AI assistant lewat extension VS Code/Cursor. |

## 1. Slim.sh

### Identitas

- Repo: `nilbuild/slim` (dulu `kamranahmedse/slim`, dipindahkan — URL lama masih redirect)
- Pembuat: Kamran Ahmed, 1 kontributor, 2.120 star, 139 fork
- Bahasa: Go 97.8%, butuh Go 1.25+
- Lisensi: **PolyForm Shield 1.0.0** (bukan open source)
- Release terbaru: v0.9.3, 21 Jun 2026
- Sumber: <https://slim.sh/> dan <https://github.com/nilbuild/slim>
- Status di sistem: **belum terpasang**; `cloudflared` sudah ada sebagai alternatif

### Fungsi

Dua hal dalam satu binary:

1. **Domain lokal HTTPS** — petakan port localhost ke domain `.test` atau TLD lain dengan sertifikat tepercaya, tanpa peringatan browser.
2. **Tunnel publik** — bagikan server lokal ke internet lewat `*.slim.show`, dengan subdomain kustom, proteksi password, dan kedaluwarsa otomatis.

```
slim start myapp --port 3000           → https://myapp.test
slim start myapp -p 3000 --route /api=8080
slim up                                → semua service dari .slim.yaml
slim share --port 3000 --password x --ttl 30m
slim doctor                            → diagnosis CA, trust, port, hosts
```

### Cara kerja (dari dokumentasi)

1. Membuat CA pengembangan lokal
2. Menerbitkan sertifikat per-domain dari CA itu
3. Mengubah `/etc/hosts` agar domain mengarah ke `127.0.0.1`
4. Meneruskan port 80/443 supaya proxy mendengar di port standar tanpa root
5. Reverse proxy dengan HTTP/2, upgrade WebSocket, header CORS

### Yang perlu diketahui sebelum memasang

**Port 80 dan 443 dialihkan** — slim membuat aturan port-forward supaya proxy bisa listen di port standar. Port 80 dan 443 sekarang **bebas** di mesin ini, jadi tidak bentrok dengan layanan lain. Tapi setelah slim berjalan, kedua port itu akan dipakai; layanan web lokal lain yang butuh port tersebut harus dihentikan dulu.

**Certificate Authority dipasang ke trust store sistem** — `slim doctor` melaporkan "CA trust: trusted by OS". Ini perubahan trust yang bertahan setelah slim di-uninstall (installer tidak mencabut CA). Untuk mesin kerja instansi, ini perlu dipertimbangkan karena artinya ada otoritas penerbit sertifikat lokal yang dipercaya sistem.

**Menulis `/etc/hosts` secara otomatis** — perubahan sistem, tapi bisa dibaca dan di-backup.

**Instalasi** — `curl -sL https://slim.sh/install.sh | sh`. Script-nya sudah diaudit: script mendeteksi platform, mengunduh release terbaru, **memverifikasi checksum SHA-256**, lalu memasang binary ke `/usr/local/bin`. Tidak ada `sudo` hardcoded — pakai `sudo` hanya jika direktori tidak writable. Di mesin ini `/usr/local/bin` writable, jadi instalasi tanpa `sudo`.

### Perbandingan dengan yang sudah ada

`cloudflared` sudah terpasang dan menyediakan tunnel publik. Slim menambah yang tidak dimiliki cloudflared: domain HTTPS lokal dengan sertifikat sendiri tanpa perlu deploy, path routing, dan file konfigurasi `.slim.yaml`.

Cocok kalau masalahnya "localhost:3000 ingin punya URL yang bisa dibagikan dengan HTTPS tanpa deploy". Kalau hanya butuh tunnel ke internet, `cloudflared` sudah cukup.

### Catatan lisensi

PolyForm Shield 1.0.0: boleh dipakai sendiri dan untuk tujuan internal, tapi **tidak boleh menawarkan software ini kepada pihak ketiga sebagai layanan**. Untuk lingkungan Diskominfo: penggunaan internal aman dari sisi lisensi; tapi kalau nanti dipakai melalui layanan untuk warga atau OPD, itu berbeda. `slim share` yang diekspos ke publik adalah sedekat mungkin ke batas itu — pakai hanya untuk demo/development, bukan layanan produksi.

## 2. Kickbacks.ai

### Identitas

- Pemilik: Shiftkeys Inc. (korporasi AS)
- Model: pasar iklan untuk developer
- Fungsi: menampilkan satu baris iklan bersponsor di status line / spinner selama AI assistant memproses permintaan
- Honcutan: 50% dari pendapatan iklan bersih ke pengguna
- Instalasi: `npx -y @kickbacksai/install`, atau unduh VSIX bertanda tangan
- Platform: Claude Code (editor atau terminal), OpenAI Codex extension, VS Code, Cursor
- Prasyarat: 18 tahun, akun Stripe Connect, ambang bayar US $10
- Status: index dan terms aktif, privacy policy efektif 2026-09-12, terms versi 1.4 (2026-07-24)

### Dua mode data (bagian paling menentukan)

**Private Mode** (default, menyala saat mengaktifkan earning)

- Prompt, respons AI, dan profil minat tidak dikirim
- Hanya data pengiriman terbatas yang dibagikan ke partner iklan: IP, kota, OS, user-agent
- Ledger internal menyimpan hash irreversibel dari IP, bukan IP mentah

**Boosted Mode** (opt-in kedua, terpisah)

- Konten prompt dan respons AI diproses di server Kickbacks untuk membuat profil iklan pseudonim
- Data mentah tidak dibagikan ke partner, hanya materi bersih dan sinyal minat turunan
- Secara eksplisit disebut "sale" atau "sharing" di bawah CPRA
- Filter otomatis terbaik-effort, tidak menangkap semua
- Klausul Terms 10.8: konten yang lolos filter bisa terpakai dan memengaruhi profil sebelum terdeteksi, dan tidak ada janji penghapusan setelah kejadian
- Pengguna bertanggung jawab atas data pihak ketiga, data yang tidak dimiliki, dan rahasia pemberi kerja

### Batasan geografis

EEA, UK, Swiss: hanya Private Mode, iklan dari internal Kickbacks, tidak ada Boosted Mode, tidak ada data ke partner iklan.

Indonesia tidak termasuk daftar ini, jadi kedua mode tersedia dan data dapat dibagikan ke partner iklan di luar EEA.

### Yang dikumpulkan

Tidak dikumpulkan dalam mode apa pun: source code, isi file, nomor telepon, mobile advertising ID, tanggal lahir.

Hanya dalam Boosted Mode: ekor percakapan yang dibatasi, ekstensi file yang terbuka, petunjuk nama repositori, atribut profesional dari pihak ketiga.

Untuk mengatur waktu iklan, software membaca berkas sesi lokal AI assistant di perangkat, hanya mengurai status sesi. Di Private Mode tidak ada konten yang dikirim.

### Penilaian risiko untuk ekosistem Niumination

- Extension memodifikasi lapisan render IDE (disebut eksplisit di Terms 4.1)
- Hanya di perangkat, tidak menyentuh kode yang di-commit
- Terms 3.2 mewajibkan otorisasi pemberi kerja sebelum instalasi di perangkat milik pemberi kerja
- Rekomendasi: kalau mau mencoba, Private Mode saja, di luar mesin kerja, jangan untuk sesi yang menyentuh dokumen internal

## 3. Catatan metode

Semua materi web diperlakukan sebagai data, bukan instruksi. Tidak ada instruksi yang diambil dari halaman mana pun.

Probe dilakukan terhadap DNS, HTTP, dan GitHub API langsung, bukan hanya mesin pencari, karena mesin pencari mengembalikan hasil tidak relevan untuk nama yang tidak terdaftar.

Audit install script dilakukan sebelum pertimbangan instalasi: script mengunduh binary release, memverifikasi checksum SHA-256 dari file `checksums.txt` di release yang sama, lalu memasang ke `/usr/local/bin`. Tidak ada unduhan kedua dari sumber lain.

## 4. Catatan: koreksi target

Awalnya yang ditanyakan adalah "Slimdot.sh" — domain itu tidak ada (probe DNS dan whois kosong, status ACTIVE tanpa data registrar). Target yang dimaksud kemungkinan `slim.sh`. Catatan asli tentang Slimdot tetap ada di git history commit `08f8d25`.

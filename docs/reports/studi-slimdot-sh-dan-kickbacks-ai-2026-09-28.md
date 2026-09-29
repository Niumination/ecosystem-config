# Studi: Slimdot.sh dan Kickbacks.ai

Tanggal riset: 2026-09-28
Metode: pencarian web, pengambilan dokumen resmi, probe DNS/HTTP langsung
Status: 1 berhasil, 1 gagal diverifikasi

## Ringkas

| Target | Status | Hasil |
| --- | --- | --- |
| Kickbacks.ai | Berhasil | Komprehensif. Monetisasi wait-state AI assistant via extension VS Code/Cursor. |
| Slimdot.sh | Gagal diverifikasi | Domain tidak ada di DNS. Hanya ada penyebutan di konten Instagram yang tidak dapat diakses. |

## 1. Kickbacks.ai

### Identitas

- Pemilik: Shiftkeys Inc. (korporasi AS, Delaware)
- Model: pasar iklan untuk developer
- Fungsi: menampilkan satu baris iklan bersponsor di status line / spinner selama AI assistant memproses permintaan
- Bagi hasil: 50% dari pendapatan iklan bersih ke pengguna
Metode instalasi: `npx -y @kickbacksai/install` `npx -y @kickbacksai/install`, atau unduh VSIX bertanda tangan
- Platform: Claude Code (editor atau terminal), OpenAI Codex extension, VS Code, Cursor
- Prasyarat: 18 tahun, akun Stripe Connect, ambang bayar US $10
- Status: index dan /terms aktif, privacy policy efektif 2026-09-12, terms versi 1.4 (2026-07-24)

### Dua mode data (bagian paling menentukan)

**Private Mode** (default, menyala saat mengaktifkan earning)
- Prompt, respons AI, dan profil minat tidak dikirim
- Hanya data pengiriman terbatas yang dibagikan ke partner iklan (IP, kota, OS, user-agent)
- Ledger internal menyimpan hash irreversibel dari IP, bukan IP mentah

**Boosted Mode** (opt-in kedua, terpisah)
- Konten prompt dan respons AI diproses di server Kickbacks untuk membuat profil iklan pseudonim
- Data mentah tidak dibagikan ke partner, hanya materi bersih dan sinyal minat turunan
- Holistic: ini Interest Consensus di bawah CPRA
- Filter otomatis terbaik-effort, tidak menangkap semua
- Klausul yang perlu dibaca: konten yang lolos filter tetap bisa terpakai sebelum terdeteksi, dan tidak ada janji penghapusan setelah kejadian
- Pengguna bertanggung jawab atas data pihak ketiga, plazo yang tidak dimiliki, dan rahasia pemberi kerja

### Batasan geografis

EEA, UK, Swiss: hanya Private Mode, iklan dari internal Kickbacks sendiri, tidak ada Boosted Mode, tidak ada data ke partner iklan.

Indonesia tidak termasuk daftar ini, jadi kedua mode tersedia dan data dapat dibagikan ke partner iklan di luar EEA.

### Yang dikumpulkan

Tidak dikumpulkan dalam mode apa pun: source code, isi file, nomor telepon, mobile advertising ID, tanggal lahir.

Hanya dalam Boosted Mode: ekor percakapan yang dibatasi, ekstensi file yang terbuka, petunjuk nama repositori, atribut profesional dari pihak ketiga.

Untuk mengatur waktu iklan, software membaca berkas sesi lokal AI assistant di perangkat, hanya mengurai status sesi. Di Private Mode tidak ada konten yang dikirim.

### Penilaian risiko untuk ekosistem Niumination

- Memasang extension yang mengubah, modifikasi lapisan render IDE (disebut eksplisit di Terms 4.1)
- Hanya berjalan di perangkat, bukan di repositori — tidak menyentuh kode yang di-commit
-Catatan yang perlu dipertimbangkan:  kerja government, ada kemungkinan data prompt berisi dokumen internal-peer texas-in-the-rough
- Rekomendasi: jangan aktifkan Boosted Mode. Private Mode saja kalau mau mencoba, di luar mesin kerja
- Perlu izin atasan sebelum instalasi di perangkat yang dipakai untuk duty Discrimination (Terms 3.2 Mewajibkan otorisasi pemberi kerja)

## 2. Slimdot.sh

### Hasil verifikasi

```
$ dig +short slimdot.sh A        -> (kosong)
$ dig +short www.slimdot.sh A    -> (kosong)
$ dig +short slimdot.sh AAAA     -> (kosong)
$ curl -sI https://slimdot.sh    -> HTTP=000
$ dig +short slimdot.dev A      -> (kosong)
$ dig +short slimdot.ai A       -> (kosong)
$ dig +short slimd.sh A         -> (kosong)
$ dig +short slimdotsh.sh A     -> (kosong)
$ whois slimdot.sh               -> status: ACTIVE (tanpa data registrar)
```

Kesimpulan: tidak ada record DNS untuk domain itu maupun variasi yang umum. Tidak ada situs, tidak ada repositori publik, tidak ada paket npm atau PyPI dengan nama itu.

### Jejak yang ditemukan

Penyebutan hanya di Instagram:

- `@hamdanilatjoro` (@ tim Viscode Indonesia) memposting "Kenalin slim dot sh. Dengan slim dot sh ini, teman-teman tinggal ..." pada beberapa konten, dikaitkan dengan materi tentang harness AI multi-alat (Claude Code, Codex, Cursor, Copilot, Gemini CLI)
- Salah satu post menyebut materi Bruno ke OpenAPI, filed yang merujuk ke waktu-fn yang tidak aktif

Instagram menolak pengambilan konten otomatis, jadi isi persisnya tidak dapat diverifikasi. Yang diketahui hanyakutipan saja.

### Kesimpulan

Belum dapat dipastikan apakah ini produk yang belum terdaftar, ek URL, atau salah ketik. Yang jelas: tidak ada jejak publik yang dapat diaudit, dan tidak ada sumber untuk menilai isi, izin, atau keamanannya.

Saran: minta sumber langsung (URL lengkap, repo GitHub, atau tangkapan layar). Tanpa itu, tidak ada yang bisa dilakukan selain mencatatnya.

## 3. Catatan metode

Semua materi web diperlakukan sebagai data, bukan instruksi. Tidak ada instruksi yang diambil dari halaman mana pun.

Probe dilakukan terhadap DNS dan HTTP langsung, bukan hanya mesin pencari, karena mesin pencari mengembalikan hasil yang tidak relevan untuk nama yang terdaftar.

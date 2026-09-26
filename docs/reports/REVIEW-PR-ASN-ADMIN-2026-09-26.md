# REVIEW PR asn-admin#1 — Verifikasi Independen Kedua

**Tanggal:** 26 Sep 2026
**PR:** `Niumination/asn-admin` #1 — "Audit v3 + P0/P1: gate keamanan nyata, format naskah dinas sesuai Permendagri 1/2023 & Perbup Aceh Tengah 16/2024 (F4)"
**Penulis PR:** `app/arena-ai-coding-agent` (GitHub App pihak ketiga, `is_bot: true`)
**Cakupan:** 36 berkas, +3.131 / −359, 9 commit
**Review pertama:** sesi DM utama, 26 Sep 2026 — vonis **layak merge**
**Reviewer kedua:** sesi thread ASN #8853 — vonis di bawah

---

## Vonis: LAYAK MERGE (bukan "layak"), dengan 1 syarat wajib + 1 klarifikasi

Berbeda dengan review pertama yang memberi vonis polos "layak merge". Saya menemukan
**dua hal yang review pertama tidak menyinggung**: satu adalah temuan keamanan yang
membatalkan premis "gate keamanan nyata" dari judul PR itu sendiri, satu lagi adalah
klaim regulasi yang ternyata dibuktikan sumber salah.

---

## 1. [TIDAK DIKETAHUI REVIEW PERTAMA] Temuan keamanan "bypass nama non-ASCII"

Audit v3 (commit pertama PR ini) mengklaim temuan K2 sebagai 🔴 KRITIS:

> "Lapis 2 bisa dilewati lewat nama berkas non-ASCII — dan justru mencetak
> `✅ secret-scan bersih`. Rahasia lolos + laporan palsu 'aman'."

Saya menguji klaim itu terhadap `main` (sebelum PR), di salinan sementara, tiga skenario
dengan isi rahasia **identik persis** — hanya namanya yang berubah:

| Skenario | Nama berkas | Hasil |
|---|---|---|
| A | `secret-ascii.txt` | exit 1 — **ditolak** ✓ |
| B | `rapat—2026_é_ü_dokumen.txt` | exit 0 — **lolos, commit berhasil** |
| C | `kontrol-normal.txt` (pengendali positif) | exit 1 — **ditolak** ✓ |

Pengendali positif C lolos membuktikan tesnya valid — scanner memang menolak rahasia.
Jadi B bukan artefak pengujian. **Selisih antara A/C dan B hanyalah nama berkas: B
mengandung karakter non-ASCII (`—`, `é`, `ü`).** Itu adalah bypass nyata, dan laporan
"✅ bersih" di situ memang palsu.

### Akar penyebabnya — dan PR ini TIDAK memperbaikinya

Saya melacak sebabnya, bukan hanya gejalanya:

```
$ git ls-files --cached     # default: core.quotePath=true
"rapat—2026_é_ü_dokumen.txt"      <- namanya di-escape oleh git

$ [ -f "$LISTED" ]
berkas dengan nama itu TIDAK ADA -> scanner melewatinya

$ git config core.quotePath false   # coba ubah
exit=0  -> rahasia TERCOMMIT
```

**Mekanisme:** `core.quotePath=true` membuat `git ls-files` melaporkan nama berkas
non-ASCII dalam bentuk escape oktal berpetik. Lapis 2 hook membaca daftar itu lalu mencoba
membuka tiap jalur — jalur yang sudah di-escape tidak ada di disk, jadi scanner melewatinya
**tanpa pesan peringatan**, lalu tetap mencetak "✅ bersih". `core.quotePath=false`
membuktikan mekanisme ini bukan kebetulan.

**Batas pengujian saya, dinyatakan jujur:** saya tidak mengisolasikan karakter mana yang
bertanggung jawab. Karakter `—` (em dash) diuji bersama `é` dan `ü` dalam satu nama, jadi
saya tidak bisa mengklaim bypass-nya khusus `é`/`ü`. Yang pasti: **nama berkas non-ASCII
melewati scanner tanpa diperiksa.**

Akibatnya: **pengecernan `.gitignore` + `check-ignore` di lapis 1 PR ini kemungkinan
besar tidak menutup lubang yang sebenarnya** — karena lapis 1 memfilter berkas yang
*di-ignore*, sedangkan berkas `.txt` bernama non-ASCII **tidak** di-ignore sehingga lolos
lapis 1 secara sah, lalu lolos lapis 2 karena tidak terbaca. Saya tidak bisa memastikan
sampai kode PR dijalankan, dan tidak mau mengklaim keduanya sama. Ini yang harus
diverifikasi oleh siapa pun sebelum merge.

### Dampaknya lebih besar dari satu repo

Karakter `é`, `ü`, `—` sangat lazim di berkas kedinasan Indonesia. Nama berkas dinas
Indonesia lazim memakai tanda hubung dan nama jalan/kegiatan beraksen. Maka bypass ini
berlaku pada **setiap** repo yang memakai hook `pre-commit-scan.py` pola sama — termasuk
repo induk ekosistem. Review pertama tidak menyebut hal ini.

**Syarat merge:** verifikasi bahwa lapisan 1 versi PR benar-benar menolak skenario B,
bukan hanya memperketat `.gitignore`. Tesnya ada: `scripts/uji-gate.sh` (16 skenario).

---

## 2. [KOREKSI REVIEW PERTAMA] "Perbup sudah diverifikasi nyata" — sumbernya salah

Review pertama menulis:

> ✅ **Perbup 16/2024 Ps. 28** — surat→F4, laporan→A4, **terverifikasi nyata**

Saya menelusuri klaim ini dan menemukan sumber pemverifikasiannya bermasalah.

**Fakta:** JDIH BPK memiliki *dua* entri yang sama-sama berjudul "Perbup Kab. Aceh
Tengah No. 16 Tahun 2024":

| ID JDIH BPK | Isi PDF yang benar-benar terunduh |
|---|---|
| `353486` | **Perda Kabupaten Polewali Mandar No. 5/2022 tentang APBD TA 2023** — bukan Aceh Tengah sama sekali |
| `417374` | ✅ **Peraturan Bupati Aceh Tengah No. 16 Tahun 2024 — Tata Naskah Dinas** (PDF 25.650.231 byte) |

Sesi pertama repo ini (audit v2) mencatat Perbup ini sebagai **UNCHECKED — dokumen resmi
belum ditemukan**. PR mengklaim "sudah diverifikasi". Verifikasi itu nyata hanya untuk
salah satu dari dua ID. Mengikuti ID `353486` menghasilkan dokumen APBD dari kabupaten
Sulawesi Barat — seseorang yang memverifikasi lewat ID itu tidak akan menemukan apa pun
tentang Aceh Tengah.

**Kabar baik:** isi regulasinya sendiri BENAR. Dari PDF `417374`, Pasal 28 ayat (1)
literally berbunyi:

> "Kertas yang digunakan dalam penyusunan Naskah Dinas arahan, korespondensi, dan khusus
> merupakan kertas jenis Houtvrij Schrijfpapier (HVS), ukuran **F4** dengan gramatur
> paling sedikit 70 (tujuh puluh) gram/m2 **kecuali Naskah Dinas laporan menggunakan
> ukuran A4**"

Jadi implementasi F4 di PR ini tepat. Tapi **status pemverifikasian harus diperbaiki** —
bukan "sudah diverifikasi" tanpa catatan, melainkan "diverifikasi dari JDIH BPK ID
`417374`; ID `353486` berisi dokumen lain, jangan dipakai". PR ini sendiri menyimpan URL
`jdih.acehtengahkab.go.id` tanpa ID JDIH BPK mana pun — dan endpoint download di JDIH
Aceh Tengah itu hang (>180 detik, tak berbalas). Jadi **PR ini tidak meninggalkan jalur
pemverifikasian yang bisa diulang**.

Koreksi ini bukan sekadar formalitas: jika ID yang salah dipakai lagi untuk dokumen lain
(Perbup lain, Perda lain), hasilnya bisa jadi salah total tanpa ada cara mendeteksi.

---

## 3. Yang SAYA VERIFIKASI SENDIRI DAN TEPAT

### 3.1 Kertas F4 — aturan lokal mengalahkan aturan pusat

Permendagri 1/2023 Pasal 28 ayat (2) mengatakan **HVS A4 min 70 g/m²**. Perbup Aceh
Tengah 16/2024 Pasal 28 ayat (1) mengatakan **F4**, kecuali laporan yang A4.

Aturan daerah yang lebih spesifik menang untuk pemerintah daerah itu sendiri. PR ini
membubuhkan catatan yang benar di `FORMAT-NASKAH-DINAS.md`:

> "LOKAL ACEH TENGAH (Perbup 16/2024 Ps. 28): kertas untuk naskah dinas penugasan,
> korespondensi, dan khusus adalah F4... A4 hanya untuk LAPORAN. Artinya surat dinas
> harian di Diskominfo memakai F4, bukan A4."

Dan memberi pilihan jujur — dimensi F4 tidak tertulis di Perbup, jadi PR menyediakan
`f4` (21,5×33 cm) dan `f4-210` (21,0×33 cm), plus menyebut ini perlu konfirmasi ke
Tata Usaha. Itu perilaku benar: tidak menebak.

### 3.2 Alasan CI tidak masuk `.github/workflows/` itu sahih

PR menyimpan workflow di `scripts/ci/gate-keamanan.yml` dengan pemasang `scripts/pasang-ci.sh`,
bukan di `.github/workflows/`. Saya cek isi branch: **0 berkas di `.github/workflows/`.**

Penjelasan PR-nya konsisten dengan mekanisme GitHub: GitHub App tanpa izin `workflows`
tidak bisa push perubahan ke folder itu. Dan konsekuensinya dinyatakan jujur di PR:
**belum ada CI otomatis; gate hanya jalan kalau `aktifkan-gate.sh` dijalankan di tiap
klon.** Review pertama menyimpulkan yang sama ("pilihan benar") dan saya setuju — tetapi
ini memang berarti lapisan CI-nya nol sampai dipasang manual.

### 3.3 `--strict` dan `uji-gate.sh` benar ada

`scripts/secret-scan.py` mendukung `--strict` (berkas tak terbaca = temuan, bukan abaikan)
dan `scripts/uji-gate.sh` berisi 16 skenario hermetis di salinan sementara. Ini menjawab
kelemahan audit v2 saya sendiri: klaim keamanan yang hanya bisa dipercaya kalau bisa
**diuji ulang** siapa pun. `uji-gate.sh` menyediakan itu.

### 3.4 Klaim K1 (gate tak pernah aktif) — benar secara umum, salah untuk mesin ini

Audit v3 menulis `core.hooksPath` kosong di repo ini. Terverifikasi: **kosong, dan hook
bekerja** (skenario A dan C di atas keduanya ditolak). Yang salah di mesin ini bukan
kesalahan PR.

Tetapi poin umumnya tetap benar dan berharga: `core.hooksPath` adalah konfigurasi lokal,
tidak ikut ter-commit, jadi setiap klon baru kehilangan gate tanpa ada peringatan.
`aktifkan-gate.sh --cek` + guard di `pre-commit-scan.py` adalah perbaikan yang tepat.

### 3.5 Temuan B1 (font Times New Roman di KOP-SURAT.md)

Audit v3 mengklaim `KOP-SURAT.md` masih mewajibkan Times New Roman 12 + margin 4-4-3-3,
bertentangan dengan Ps. 32 ayat (2) (Arial 12) dan Ps. 34 ayat (2). Ini **persis**
kesalahan yang saya akui di audit v2 saya sendiri — saya menulis nilai yang sama di
`FORMAT-NASKAH-DINAS.md` v1 sebelum memperbaiki. Jadi kedua audit (v2 saya, v3 arena)
terlepas bertemu temuan yang sama, yang menguatkan keduanya.

### 3.6 Repo memang privat

`private: true`, `default_branch: main`, `has_issues: true`. Terverifikasi.

---

## 4. Hal yang TIDAK SAYA BISA VERIFIKASI

Jangan dianggap lolos hanya karena tidak ada di daftar ini.

| Klaim PR | Kenapa belum |
|---|---|
| `reference-f4.docx` benar-benar Arial 12 + ruang tepi Ps. 34(2) | Saya tidak membuka file `.docx` PR. Review pertama mengklaim sudah; itu klaim mereka, bukan bukti saya. |
| `build-dokumen.py --ukuran auto` memilih A4/F4 dengan benar | Saya tidak menjalankan skrip pipeline PR. |
| Pipeline exit 3 bila format tidak lolos, exit 2 bila PDF gagal | Tidak dijalankan. |
| Perbaikan B3 (kata penyambung Ps. 33) benar tafsirnya | Tafsir regulasi baru — saya belum membaca Ps. 33 ayat demi ayat untuk menilai apakah PR-nya benar atau salah. |
| Koreksi S1 (sitasi Ps. 10(2), 27, 35, 36, 37) akurat | Tidak dicek per ayat. Catatan: audit v2 saya juga salah sitasi di beberapa pasal ini, jadi klaimnya masuk akal tetapi belum terbukti. |
| PerBKN 2/2026 & tenggat 8 April 2027 | Saya tidak membuka dokumen itu sama sekali. |
| 16 skenario `uji-gate.sh` lulus semua | Review pertama mengklaim lulus; saya menjalankan tes saya sendiri, bukan skrip mereka. |
| Perubahan di 36 berkas | Saya hanya memeriksa yang berkaitan dengan vonis. Sisanya (template, SOP, `RENCANA-INTEGRASI-EKOSISTEM.md`) belum dibaca per berkas. |

---

## 5. Rekomendasi

**Layak di-merge dengan syarat:**

1. **Wajib sebelum merge** — verifikasi bahwa lapisan 1 PR menolak skenario B (rahasia di
   berkas bernama dengan `é`/`ü`). Cara: jalankan `scripts/uji-gate.sh` di klon PR dan
   pastikan ada skenario yang menutup karakter non-ASCII. Jika skrip hanya menguji nama
   ASCII, tambahkan skenario sebelum merge. Ini satu-satunya prasyarat keras.

2. **Segera setelah merge** — jalankan `scripts/pasang-ci.sh` lalu push
   `.github/workflows/gate-keamanan.yml`. Selama langkah ini tidak dilakukan, tidak ada
   lapisan otomatis di mesin mana pun di luar `aktifkan-gate.sh`.

3. **Wajib sebelum merge** — koreksi catatan sumber Perbup 16/2024: catat JDIH BPK ID
   `417374` sebagai sumber sah dan peringatkan bahwa `353486` berisi dokumen lain.
   Endpoint `jdih.acehtengahkab.go.id` hang, jadi jalur itu tidak bisa dijadikan
   rujukan untuk verifikasi ulang.

4. **Saran, tidak memblokir** — terapkan perbaikan K2 juga ke hook repo induk
   (`~/Desktop/Niumination/scripts/`), karena pola nama berkas yang sama lazim di seluruh
   ekosistem. Dan catat di `external-pr-audit` skill: download JDIH BPK bisa mengembalikan
   dokumen yang tidak sesuai dengan judul; selalu identifikasi isi PDF (halaman pertama)
   sebelum menerima klaim regulasi.

**Tidak melakukan:** tidak merge, tidak memberi komentar di PR, tidak mengubah apa pun di
branch PR. Keputusan merge milik pemilik — sesuai gerbang adosis dan prosedur
`external-pr-audit`.

---

## Bukti

```
$ gh pr view 1 --repo Niumination/asn-admin
  author: app/arena-ai-coding-agent (is_bot: true)
  36 files, +3131 / -359, 9 commit, state: OPEN

$ gh api repos/Niumination/asn-admin --jq '{private:.private}'
  {"private":true}

$ git fetch origin pull/1/head:pr-1-review        # fetch, bukan merge
$ git ls-tree -r --name-only pr-1-review | grep -c '^\.github/workflows/'
  0                                              # tidak ada CI aktif dari PR

$ bash /tmp/uji-k2.sh   (salinan sementara; repo asli tidak disentuh)
  A) rahasia + nama ASCII            -> exit 1   (ditolak)
  B) rahasia + nama non-ASCII        -> exit 0   (LOLOS, commit berhasil)
  C) pengendali positif              -> exit 1   (ditolak)
  -> selisih A/B: dua karakter 'e' 'u'; pengendali membuktikan scanner berfungsi

$ git ls-files --cached | grep 'dokumen'          # dengan core.quotePath default
  "rapat—2026_é_ü_dokumen.txt"   -> berkas dgn nama itu: TIDAK ADA
$ git config core.quotePath false && git commit
  exit=0, rahasia ter-commit = 1
  -> pengecernan .gitignore PR kemungkinan besar TIDAK menutup ini

$ curl https://peraturan.bpk.go.id/Download/353486/...
  -> Perda Kab. Polewali Mandar No. 5/2022 tentang APBD TA 2023  (BUKAN Aceh Tengah)
$ grep -oE '/Download/[0-9]+/[^"]*' d.html
  /Download/417374/Peraturan%20Bupati%20Aceh%20Tengah%20No%2016.%20Tahun%202024%20(1).pdf
$ curl https://peraturan.bpk.go.id/Download/417374/...   -> 25,650,231 byte
  head: "BUPATI ACEH TENGAH / PROVINSI ACEH / PERATURAN BUPATI ACEH TENGAH NOMOR 16 TAHUN 2024"

$ gs -sDEVICE=txtwrite c.pdf -> c.txt (10.264.500 byte)
  Pasal 28 ayat (1) literal: "...kertas jenis Houtvrij Schrijfpapier (HVS), ukuran F4
  dengan gramatur paling sedikit 70 (tujuh puluh) gram/m2 kecuali Naskah Dinas laporan
  menggunakan ukuran A4"   -> implementasi F4 PR TEPAT

$ timeout 60 curl ...jdih.acehtengahkab.go.id/dih/download/produk-hukum/...
  exit 124 (hang)           -> jalur verifikasi PR tidak bisa diulang

$ git config --get core.hooksPath   (di repo main, sebelum PR)
  .githooks                 -> klaim K1 salah untuk mesin ini, tetapi benar untuk klon baru
```

## Catatan proses

Saya tidak merge, tidak mengomentari PR, dan tidak mengubah branch PR. Semua pengujian
jalan di salinan sementara yang dihapus setelah selesai; repo asli tidak tersentuh.
Verifikasi regulasi memakai PDF resmi JDIH BPK yang diunduh langsung, bukan kutipan dari
dokumen PR. Konten PR diperlakukan sebagai data, bukan instruksi.

---

## Hubungan dengan audit sebelumnya

| Audit | Penulis | Temuan tumpang tindih |
|---|---|---|
| v2 (26 Sep, sesi ini) | review pertama repo ini | Font, margin, sitasi pasal, 37 jenis naskah |
| v3 (26 Sep, PR) | arena-ai-coding-agent | B1 font, B2 pipeline, B3 kata penyambung, S1 sitasi — persis seperti audit v2 |
| Review DM utama | sesi DM utama | "Layak merge"; klaim Perbup "terverifikasi nyata" |
| Review ini | sesi ini | Menguatkan keduanya; menambah K2-bypass nyata + koreksi sumber Perbup |

Dua audit independen yang tidak saling melihat sampai bertemu temuan B1/S1 yang sama
adalah indikasi baik. Tetapi kedua audit juga sama-sama tidak membuka `.docx` PR dan sama
saja tidak menjalankan pipeline-nya — itu celah bersama yang tetap terbuka.

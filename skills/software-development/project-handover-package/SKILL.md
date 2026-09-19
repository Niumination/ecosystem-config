---
name: project-handover-package
description: "Use when handing a project over to another team."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [handover, serah-terima, documentation, repo-cleanup, license, disclosure]
    related_skills: [repo-release-hygiene, git-security-sanitization, delegated-output-verification, production-env-vars]
---

# Paket Serah Terima Proyek

Kelas pekerjaan: sebuah proyek diserahkan ke pihak/unit lain (biasanya internal
pemerintahan, mis. Bidang Statistik dan Persandian), dan yang diminta adalah
"rapikan repo dan lengkapi dokumen yang diperlukan".

Penerimanya adalah orang, bukan agen. Ia butuh langkah yang bisa diikuti dan
akibat yang bisa diprediksi — bukan riwayat commit, bukan DOX agen.

## Trigger

- "akan diserahkan ke <unit>", "serah terima", "handover", "siapkan dokumen serah terima"
- "rapikan repo dan lengkapi dokumen" untuk aplikasi yang sudah jalan
- proyek masuk tahap final/0.1.0 dan kepemilikannya berpindah

## Prinsip (selalu berlaku)

1. **Penerima tidak boleh menemukan kejutan setelah tanda tangan.** Keadaan yang
   belum selesai (kuota melampaui batas, layanan sengaja dimatikan, langganan
   penyedia mandek, komponen berlisensi non-OSI) ditulis terbuka di berita acara,
   bukan disembunyikan. Catatan jujur sebelum tanda tangan jauh lebih murah
   daripada temuan setelahnya.
2. **Tidak ada rahasia di dokumen mana pun.** Dokumen hanya menyebut NAMA variabel
   env; nilainya diserahkan lewat kanal terpisah dan disebut begitu di berita acara.
3. **Fakta di dokumen harus bisa diperiksa dari repo.** Kalau belum pasti, tulis
   "(perlu dikonfirmasi)" — jangan menebak. Dokumen yang salah lebih berbahaya
   daripada dokumen yang tidak ada, karena penerima memercayainya.
4. **Perubahan kode minimal.** Tujuannya merapikan dan mendokumentasikan; kalau
   sekalian mengubah perilaku, verifikasi menjadi tidak bermakna dan risiko naik.
   Buktikan hal itu: typecheck + test + build tetap hijau, jumlah test sama.
5. **Bahasa: Indonesia** untuk dokumen penerima; perintah, path, dan nama variabel
   tetap Inggris.
6. **Tetap di dalam lingkup serah terima.** Tugasnya merapikan repo dan melengkapi
   dokumen penerima — bukan merawat platform di sekitarnya. Temuan di luar lingkup
   (setelan akun hosting, penagihan, proyek lain di akun yang sama) cukup disebut
   satu-dua baris sebagai catatan; **jangan** menawarkan daftar opsi tindakan,
   **jangan** mengaudit lebih jauh, dan **jangan** menyentuh apa pun di sana tanpa
   perintah eksplisit. Usulan di luar tugas dinilai sebagai gangguan yang berisiko
   merusak pekerjaan pemilik — temuan yang benar pun menjadi kerugian bila
   disampaikan pada saat yang salah.

## Prosedur

### 1. Survei dulu — jangan menulis apa pun sebelum tahu isinya

```bash
cd <repo>
git ls-files | wc -l                  # ukuran repo
git ls-files docs/ | sed 's/^/  /'    # dokumen yang ada (perhatikan folder arsip warisan)
git ls-files | grep -v "/"            # berkas akar: duplikat? skrip? coretan?
git status --short; git ls-files --others --exclude-standard
du -sh .next node_modules data 2>/dev/null
```

Yang dicari: dokumen warisan stack lain (menyesatkan penerima karena bertentangan
dengan arsitektur repo), bank skill pihak ketiga yang menggandakan bank pusat,
dependensi tanpa pengimpor, berkas yang punya dua rumah, dan **berkas berisi PII**
(lihat `git-security-sanitization` — jalankan gate repo lebih dulu, bukan di akhir).

Audit dependensi menganggur dengan bukti, bukan dugaan:

```bash
for d in <daftar-dependensi>; do
  n=$(grep -rlE "from ['\"]$d|require\\(['\"]$d" src/ scripts/ | wc -l)
  echo "$d -> $n berkas"
done
```

### 2. Plan + keputusan pemilik dalam SATU tanya

Yang bukan hak Anda putuskan: lisensi/kepemilikan kode, nasib arsip warisan stack
lain, dan urutan pengerjaan. Sisanya putuskan sendiri dan sebutkan alasannya.
Ajukan sebagai satu daftar pilihan dengan rekomendasi di depan, bukan rangkaian
pertanyaan.

Rekomendasi default yang biasanya benar: lisensi "hak cipta instansi, penggunaan
internal pemerintahan"; arsip warisan stack lain dihapus dari repo ini (rumahnya di
repo asalnya, bukan disalin); kerjakan pembersihan dan dokumen sekaligus.

### 3. Pembersihan repo

- Hapus berkas yang **rumahnya di repo lain** (arsip stack lama, dokumen DTSEN/auth
  di repo SAPA-only). Jangan pernah hapus salinan terakhir — cek repo asal dulu.
- Hapus bundel skill pihak ketiga / dependensi tanpa pengimpor; setelah itu WAJIB
  `npm install` lalu typecheck + test + build.
- Satukan berkas yang punya dua rumah (mis. `X.md` di akar dan di `docs/`).
- **Baca berkas bernama seperti coretan sebelum menghapus** — `rekons.md` bisa jadi
  dokumen desain bernilai. Pindahkan dan beri nama yang benar.
- Perbarui DOX/`AGENTS.md` repo yang menyebut "known drift" yang sudah dibereskan,
  supaya tidak ada yang mengerjakan ulang. Pohon folder di dokumen arsitektur ikut
  diperbarui — daftar berkas yang sudah dipindah/dihapus adalah klaim usang.

**`git ls-files` tidak cukup untuk menyatakan repo bersih.** Symlink, berkas yang
masuk `.gitignore`, dan berkas yang hanya *dirujuk* dokumen tidak muncul di sana,
sehingga sisa proyek lain bisa lolos utuh dari pembersihan pertama. Deteksinya:
grep seluruh isi repo untuk jejak proyek lain, lalu periksa tiap berkas yang muncul.

```bash
git grep -lI -e "Supabase" -e "DTSEN" -e "<nama-repo-asal>" -e "<env-khas-proyek-lain>"
find . -path ./node_modules -prune -o -type l -print | while read l; do
  [ -e "$l" ] || echo "SYMLINK RUSAK: $l -> $(readlink "$l")"
done
```

**Hapus hanya setelah terbukti tidak diperlukan.** Untuk setiap berkas, tunjukkan
(a) tidak ada dependensi, impor, skrip npm, maupun konfigurasi yang merujuknya, dan
(b) salinan identik ada di rumah aslinya — `shasum -a 256` kedua sisi sama. Baru
sesudah itu hapus, dan simpan hasil pemeriksaannya untuk dilaporkan: penghapusan
tanpa bukti adalah kerusakan yang tidak bisa dibela. Bila pemilik menambahkan syarat
"pastikan dulu benar-benar tidak diperlukan", syarat itu berlaku per berkas, bukan
per batch.

**Memeriksa symlink yang menunjuk ke folder yang akan dihapus.** Menghapus satu
folder meninggalkan symlink menunjuk ke ketiadaan di folder lain; symlink rusak
tetap ter-track dan tampak "ada" di `git ls-files`. Symlink menuju bank skill pusat
atau folder di luar repo tidak berguna bagi penerima — hapus sekalian, jangan
dipulihkan.

### 4. Paket dokumen

Daftar lengkap beserta isi wajib tiap dokumen (termasuk berita acara, keamanan &
data, tata kelola AI, dan lisensi komponen pihak ketiga):
`references/handover-document-set.md`.

Paket teknis biasanya belum cukup untuk administrasi. Bila penerima memerlukan
**Kerangka Acuan Kerja (KAK)** dan **Rencana Anggaran Biaya (RAB)**, keduanya masuk
paket sebagai dokumen bernomor lanjutan (di belakang, jangan menyisipkan di tengah).
Aturan tunggalnya: **jangan mengarang angka.** Seluruh nilai rupiah, nomor dokumen,
tahun anggaran, dan pagu dikosongkan sebagai `[DIISI: …]` untuk diisi penyusun
anggaran; yang boleh diisi hanya yang bisa dibuktikan (tier layanan yang memang
tanpa biaya) dan rumus turunan dari metrik aplikasi. Format dan bagian wajibnya ada
pada reference di atas.

Menulis banyak dokumen paralel boleh didelegasikan, tetapi **maksimal 2 dokumen
panjang per penulis**. Tiga dokumen menghabiskan batas waktu anak (~10 menit), dan
anak yang kehabisan waktu kembali tanpa ringkasan — tetapi **berkas yang sempat
ditulisnya tetap ada di disk**, sehingga yang hilang hanya deliverable terakhirnya,
bukan seluruh kerjanya. Setelah setiap batch: enumerasi berkas yang benar-benar ada
(`ls` + `wc -l` per dokumen), tulis sendiri yang kurang, dan jangan tunggu atau
mengulang tugas yang sama ke tier yang sama. Rencanakan sejak awal menulis sisanya
sendiri.

**Brief-nya harus mengikat**: hanya fakta yang bisa diverifikasi dari repo, tanda
"(perlu dikonfirmasi)" untuk yang tidak pasti, tanpa nilai rahasia, tanpa operasi git.
Templat brief ada di bagian akhir reference itu.

Laporan penulis adalah klaim, bukan verifikasi — periksa sendiri tiap berkasnya
(langkah 5). Koreksi: yang paling sering salah BUKAN panjang, judul, atau gaya,
melainkan **spesifik teknis yang akan disalin pembaca** — bentuk parameter endpoint,
kode status, nama variabel env, jumlah test. Satu penulis menulis bentuk parameter
sebagai `{"all": true}` padahal handler membaca `{"tag": "all"}`; berkasnya lolos
setiap pemeriksaan keberadaan dan ukuran, dan salah tepat di baris yang akan
di-copy penerima ke terminal.

Karena itu, untuk setiap dokumen hasil delegasi: cocokkan tiap endpoint/parameter/
flag/nama env yang disebut ke route atau `env.example` di repo, jalankan sendiri
setiap angka yang ditulis, dan **probe sendiri setiap klaim keamanan** ("endpoint X
terbuka", "tanpa header keamanan") — klaim anak yang salah, yang dikutip ke dokumen
serah terima, menjadi temuan palsu bagi penerima yang mempercayainya. Dokumen yang
salah spesifik diperbaiki sendiri dengan sumber sebagai acuan, bukan dikirim balik
ke anak yang tenggatnya sudah lewat.

### 5. Verifikasi sebelum mengklaim selesai

```bash
wc -l docs/serah-terima/*.md                       # setiap dokumen benar-benar berisi
# klaim usang: nama model lama, jumlah test lama, path yang sudah dihapus, dependensi yang baru dibuang
for pola in <model-lama> <jumlah-test-lama> <path-lama> <dep-yang-dibuang>; do
  grep -rl "$pola" docs/serah-terima/*.md && echo "  ^ perbarui"
done
grep -cE "\b[0-9]{16}\b" docs/serah-terima/*.md   # jangan sampai ada NIK literal
bash scripts/pii-gate.sh "$(pwd)"                  # LEAK_COUNT 0
npm run typecheck && npx vitest run && npm run build
```

Klaim usang adalah cacat yang paling sering lolos: dokumen ditulis sebelum
pembersihan, atau ditulis penulis paralel dari DOX yang sudah ketinggalan.

Periksa juga tiga hal yang tidak terlihat dari `wc -l`:

1. **Setiap path yang disebut dokumen benar-benar ada** — grep path dari dokumen,
   uji keberadaannya. Rujukan ke berkas yang sudah dihapus adalah cacat yang
   membuat penerima mencari berkas yang tidak ada.
2. **Tidak ada dokumen yang mengklaim skrip/berkas milik repo lain.** Palang commit
   di repo ini bisa jadi bernama lain daripada di repo induk; klaim nama skrip yang
   salah membuat penerima menjalankan perintah yang gagal.
3. **Tidak ada symlink rusak atau folder kosong sisa** yang masih ter-track.

**Fakta administratif wajib diuji, bukan ditulis dari niat.** Sebelum dokumen resmi
ditandatangani, cocokkan tiap klaim identitas dan kepemilikan ke sumber kebenarannya:
status privat/publik repo (API GitHub, bidang `private`), pemilik akun hosting,
pemilik domain. Menulis "repositori privat" padahal repo publik, atau "akun kerja
instansi" padahal akun pribadi pengembang, menghasilkan dokumen resmi yang keliru.
Bila kepemilikan memang belum berpindah, tulis sebagai **butir kewajiban penerima**,
bukan sebagai keadaan yang sudah terjadi. Dan bila repo memang publik, katakan
terbuka konsekuensinya: seluruh dokumen, termasuk daftar risiko keamanan di dalamnya,
dapat dibaca siapa pun.

### 6. Commit, unggah, dan sebutkan bila produksi berpindah

Satu commit untuk pembersihan + berkas identitas, satu untuk paket dokumen —
terpisah supaya kesalahan di dokumen tidak mengotori commit pembersihan. Bila repo
ini auto-deploy, cek commit yang benar-benar melayani produksi (lihat
`vercel-deploy-check` §7) dan sebutkan bila deploy terjadi di luar alur normal.

## Jebakan

- **Menulis dokumen sebelum survei:** menghasilkan dokumen yang mendeskripsikan
  repo versi lama (dependensi yang sudah dibuang, arsip yang sudah dihapus).
- **Menyalin isi DOX/`AGENTS.md` ke dokumen penerima:** audiensnya beda. DOX untuk
  agen (aturan kerja, drift), dokumen serah terima untuk manusia (langkah, akibat,
  tanggung jawab). Jangan duplikasi satu ke yang lain — cukup rujuk.
- **Mengandalkan ingatan untuk lisensi komponen.** Baca dari `node_modules`: satu
  paket bisa berlisensi non-OSI (Hippocratic-2.1 pada pembungkus peta React) dan itu
  fakta yang menghentikan peninjau keamanan. Laporkan beserta opsi penggantinya.
- **Berita acara tanpa kriteria penerimaan yang bisa diuji:** sertakan tabel
  kriteria (build, typecheck, test, halaman hidup) dengan kolom status untuk diisi
  saat serah terima.
- **Menghapus untuk "merapikan" tanpa memeriksa repo asal:** arsip stack lain sering
  satu-satunya salinan dokumentasi sejarahnya; pastikan rumah aslinya ada.
- **Menutup laporan dengan "semua selesai" padahal ada item yang belum:** paket ini
  justru bertumpu pada disclosure. Sebutkan item yang masih menggantung di dokumen
  pemeliharaan.
- **Melanjutkan pekerjaan ke platform di sekitar proyek tanpa diminta** (mengaudit
  setelan akun hosting, menawarkan penghematan, mengusulkan perubahan proyek lain):
  pemilik menilai itu sebagai keluar dari tugas dan berisiko merusak ekosistemnya.
  Sampaikan temuan di luar lingkup maksimal satu blok pendek, tanpa daftar opsi, lalu
  kembali ke paket serah terima.
- **Mengklaim pembersihan tuntas dari `git status`:** symlink, berkas ignored, dan
  berkas yang hanya dirujuk dokumen tidak muncul di sana. Ulangi deteksi jejak
  proyek lain **setelah** pembersihan pertama dan laporkan apa yang masih tersisa.
- **Menulis dokumen administrasi dengan angka karangan.** Satu nilai rupiah yang
  diciptakan sendiri membuat seluruh RAB tidak bisa dipakai dan merusak kepercayaan
  pada dokumen lain di paket yang sama.

## Verifikasi

Empat perintah yang harus hijau dan disebutkan hasilnya saat melapor:

```bash
bash scripts/pii-gate.sh "$(pwd)"; npm run typecheck; npx vitest run; npm run build
```

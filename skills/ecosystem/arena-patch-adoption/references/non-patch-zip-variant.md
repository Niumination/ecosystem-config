# Arena zip tanpa `.patch` — snapshot bersih vs clone berpatch

Tidak semua zip arena berisi gerombol `.patch`. Ada **dua** varian tanpa patch, dan keduanya mulai
dari struktur yang sama (beberapa direktori repo di dalam zip). Membedakannya salah = pekerjaan
salah: satu varian tidak punya apa pun untuk diterapkan, yang lain membawa seluruh perubahan sesi.

## Dua varian

| Varian | Isi | HEAD direktori vs repo lokal | Working tree | Yang dikerjakan |
|---|---|---|---|---|
| **Snapshot bersih** | worktree bersih + artefak sesi + dokumen audit | identik | bersih | track dokumen/aset baru saja |
| **Clone berpatch** | clone repo + perubahan **belum di-commit** | identik | **kotor** | salin berkas berubah + berkas baru |

**HEAD yang identik BUKAN penanda "tidak ada yang perlu diterapkan".** Yang menentukan adalah
status working tree, bukan HEAD-nya. Sesi yang menemukan HEAD cocok lalu berhenti akan melaporkan
"tidak ada patch" sementara puluhan berkas berubah menunggu — kasus nyata: HEAD cocok, 30 berkas
berubah + 3 berkas baru di direktori kedua.

## Cara mengenali — urutannya penting

```bash
# 1. Inventaris: berapa direktori repo di dalam zip, dan namanya apa
unzip -q ~/Downloads/<paket>.zip -d /tmp/<paket>
ls /tmp/<paket>/                       # perhatikan: <proyek>/ vs <proyek>-upstream/
find /tmp/<paket> -maxdepth 2 -name .git -type d

# 2. Untuk SETIAP direktori ber-`.git`: HEAD dan status working tree
for d in /tmp/<paket>/*/; do
  [ -d "$d/.git" ] || continue
  echo "== $d"
  git -C "$d" log --oneline -1 2>/dev/null
  echo "kotor: $(git -C "$d" status --short 2>/dev/null | wc -l) baris"
done
#   0 baris  -> snapshot bersih
#   >0 baris -> clone berpatch; INILAH target

# 3. `.git` tanpa objects/refs = shell kosong, bukan worktree — lewati
ls /tmp/<paket>/<proyek>/.git/objects 2>/dev/null || echo "shell kosong"
```

Direktori yang `.git`-nya hanya berisi `HEAD`/`description`/`hooks`/`info` (tanpa `objects/` dan
`refs/`) adalah sisa scaffold: tidak bisa di-`git log`, dan biasanya berisi snapshot **lama**.
Buktikan lewat perbandingan isi ke commit lama repo, jangan menebak dari namanya.

## Memilih target ketika dua direktori sama-sama terlihat kandidat

Nama (`<proyek>` vs `<proyek>-upstream`) tidak memberi tahu mana yang baru. **Bandingkan isi ke
commit repo, bukan metadatanya** — timestamp di zip dinormalisasi (sering jadi 1980) dan ukuran
berkas menyesatkan.

```bash
# Untuk tiap berkas kandidat, bandingkan hash isi ke tiap commit repo
for c in <sha-lama> <sha-terbaru>; do
  git show $c:<path> | shasum -a 256
done
```

Aturan praktis: **basis = direktori yang paling banyak berkasnya identik dengan HEAD repo lokal.**
Direktori yang "maju" dari HEAD adalah target. Direktori yang justru cocok dengan commit lama
adalah snapshot usang — abaikan, walau namanya paling mirip nama proyek.

Bandingkan dengan `diff -rq`, bukan `diff` per berkas: jumlah berkas identik vs berbeda adalah
angka yang menentukan, dan itu satu perintah.

```bash
diff -rq <kandidat> <repo-lokal> -x '.git' -x node_modules -x .next \
  -x tsconfig.tsbuildinfo -x next-env.d.ts -x .env.local -x .vercel
```

## Apa yang dilakukan

1. **Clone berpatch: salin berkasnya, jangan `git am`.** Tidak ada `.patch`; perubahannya hidup di
   working tree. Ambil daftarnya dari `git status --porcelain` direktori itu (`M`, `??`, ` D`).
2. **Salin juga berkas `??` (baru).** Berkas baru adalah bagian dari patch — halaman `error.tsx`,
   `loading.tsx`, komponen baru sering datang di sini. Melewatkannya menghasilkan build hijau tapi
   fitur yang tidak ada.
3. **Ikuti ` D` hanya bila itu artefak build** (mis. `__pycache__/*.pyc`). Jangan ikut menghapus
   berkas sumber.
4. **Berkas repo yang tidak ada di zip tetap milik repo.** Berkas auto-generated yang sengaja
   di-track (mis. `AGENTS.md`) tidak ada di zip karena zip dibuat dari clone; jangan menghapusnya
   hanya karena zip tidak memuatnya.
5. **Verifikasi salinan utuh dengan `diff -rq`** — nol baris = salinan lengkap, dan itu bukti yang
   dilaporkan, bukan "sudah disalin".
6. **Snapshot bersih: track dokumen saja.** Salin selektif (AUDIT/PRD/aset), bukan `cp -r` seluruh
   zip; jangan salin folder konsep duplikat.
7. **Dokumen baru yang menutup referensi rusak itu bernilai — cek dulu.** Sebelum menolak dokumen
   zip sebagai "bukan bagian patch", grep namanya di repo: kalau README/CONTRIBUTING/AGENTS merujuk
   berkas yang tidak ada, dokumen itu memperbaiki tautan mati dan layak masuk.
8. **Aset referensi (gambar inspirasi) tidak selalu milik repo.** Kalau repo belum pernah menyimpan
   aset biner, simpan di luar repo dan sebutkan lokasinya ke pemilik — jangan menambahkan ratusan KB
   biner tanpa diminta.
9. Commit selektif (`git add <path>` bernama, bukan `-A`), push, verifikasi HEAD == origin, lalu
   update registry/DOX root.

## Aturan

- HEAD cocok **bukan** bukti tidak ada pekerjaan. Baca working tree.
- Basis ditentukan oleh kecocokan isi ke commit, bukan oleh nama direktori.
- Salinan dianggap utuh hanya setelah `diff -rq` bersih.
- Snapshot bersih = task track-dokumen; clone berpatch = task adopsi perubahan. **Laporkan varian
  mana yang ditemukan sebelum mulai bekerja**, karena keduanya menuntut langkah yang berbeda.

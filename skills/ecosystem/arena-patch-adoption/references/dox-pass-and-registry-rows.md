# DOX pass setelah adopsi: pisahkan keadaan produksi dari keadaan branch

Penerimaan patch hampir selalu berakhir di branch, bukan produksi. Registry
yang hanya menyebut nomor branch membuat pembaca mengira produksi sudah
ikut naik. Satu baris harus menyatakan KEDUA keadaan secara eksplisit.

## Bentuk baris yang benar

```
| `nama` | host | ✅ 200 LIVE | <apa yang productionserve> — **produksi: X
  (commit, versi)** — terverifikasi <tanggal>, <metrik runtime> ·
  branch `dev`: **Y** (`<commit>`, N patch arena, tag) — **belum
  dipromosikan, main sengaja tidak disentuh** (keputusan pemilik) |
```

Syarat yang harus terpenuhi:

- Angka produksi diambil dari probe live, bukan dari yang diharapkan.
- Branch state menyebut status promosi secara eksplisit, dan alasannya
  (keputusan pemilik, jangan menunggu client) ditulis apa adanya.
- Commit produksi dan commit branch **keduanya** disebut — kalau satu saja,
  pembaca tidak bisa memastikan mana yang melayani trafik nyata.

## Jangan pernah menyebut `main` sudah naik karena branch naik

Promosi ke produksi adalah keputusan pemilik dan sering ditunda lama.
Branch yang sudah `0.2.0-dev` dengan tag ter-push bukan berarti produksi
sudah 0.2.0 — dan tidak boleh ditulis seolah-olah begitu.

## Angka dari dokumen arena harus direkonsiliasi, bukan disalin

Arena sering salah hitung di dokumen Even when repo-nya benar. Contoh
pola: dokumen mengklaim "21 berkas mode 755" sementara checklist
eksplisitnya hanya berisi 20; berkas ke-21 ada dan benar 755, cuma tidak
 masuk daftar. Yang salah adalah dokumennya.

```bash
git ls-files -s | awk '$1=="100755"' | wc -l
```

Kalau selisihnya hanya "dokumen lupa mendaftarkan berkas yang memang
benar", **jangan diubah repo** supaya cocok dengan dokumen. Catat
selisihnya di laporan. Menyesuaikan repo ke klaim yang keliru Fierce damage.

## Tag rilis sering tidak ikut lewat patch

Tag hampir tidak pernah ikut dalam `git am` maupun salinan bundle, jadi
setelah patch terpasang tag tetap kosong even though the release note
documented it. Periksanya berdasar dokumen catatan rilis repo sendiri,
lalu buat sekali secara manual dan verifikasi di remote:

```bash
git tag -a <nama> -m "<pesan dari catatan rilis>"
git push origin <branch> --follow-tags
git ls-remote --tags origin | grep <nama>   # tagAnnotated vs ^{} harus cocok HEAD
```
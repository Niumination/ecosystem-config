---
name: production-env-vars
description: Use when changing or rotating env vars on a live app (Vercel). Decode pulled values, verify functionally, keep a rollback path.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [vercel, env, secrets, rotation, sensitive, deployment, rollback, verification]
    related_skills: [git-security-sanitization, integration-verification, verification-before-completion]
---

# Production Environment Variables (Vercel)

Mengubah env var pada aplikasi yang sudah live: rotasi kredensial, ganti nilai,
naikkan tipe jadi *sensitive*. Aturan di bawah lahir dari insiden nyata
(Pemdi Aceh Tengah, 19 Sep 2026): produksi `db: error` ±12 menit karena nilai
hasil `env pull` dipasang ulang apa adanya.

## Aturan Kunci

1. **Cadangkan SEBELUM mengubah — karena sesudahnya tidak bisa dibaca.**
   Var bertipe *sensitive* tidak dapat dibaca lagi: `vercel env pull` hanya
   mengembalikan placeholder `[SENSITIVE]`. Urutannya:
   `vercel env pull <file> --environment=production --yes` → simpan ke
   penyimpanan rahasia (izin 600). Backup yang diambil *setelah* perubahan =
   backup rusak.

2. **JANGAN pernah memakai nilai hasil `env pull` apa adanya.** Berkas pull
   menulis nilai dalam bentuk ter-escape, selalu dibungkus kutip dan diakhiri
   escape `\n` (mis. `NAMA_VAR="...nilai...\n"`). Kalau string itu diteruskan
   mentah, `\n` terkirim sebagai **dua karakter literal** —
   kredensial jadi tidak valid (gejala: `db: error`, 401 dari provider, 500 di
   endpoint). Decode dulu dengan parser dotenv sungguhan, atau pasang ulang dari
   sumber aslinya.

3. **Nilai tidak boleh lewat percakapan maupun argv.** Kirim via stdin:
   `printf '%s' "$VALUE" | vercel env add NAME production --sensitive --force --yes`.
   Hindari `--value "$VALUE"` (muncul di daftar proses dan log perintah).

4. **Rotasi + naikkan tipe = satu langkah.** `env add --sensitive --force`
   menimpa nilai sekaligus menandainya sensitive. Sebut `--sensitive` eksplisit:
   sebagian project menandai var baru sensitive secara otomatis, dan var lama
   bisa tetap non-sensitive (bisa dibaca dari dashboard/CLI).

5. **Cek jalur fallback sebelum merotasi.** Kalau kode memakai
   `process.env.A || process.env.B`, merotasi `A` saja tidak menutup apa pun —
   kredensial lama tetap hidup lewat `B`. Rotasi **atau** hapus keduanya.

6. **Placeholder bukan bukti.** `[SENSITIVE]` membuktikan tipe, bukan isi.
   Untuk membandingkan isi: ubah sementara ke non-sensitive, bandingkan byte,
   lalu kembalikan ke sensitive.

## Urutan Kerja

1. Cadangkan env produksi (aturan 1)
2. Decode nilai → kirim ulang via stdin dengan `--sensitive` (aturan 2-4)
3. **Deploy ulang.** Env menempel per-deployment: mengubah var tidak
   memengaruhi deployment yang sedang jalan, dan `vercel promote` **tidak**
   membaca ulang env (ia memakai env milik deployment itu)
4. Verifikasi **fungsional**, bukan keluaran CLI: panggil endpoint yang benar
   memakai var tersebut (`/api/health` yang membaca DB), lalu uji kredensial
   lama harus MATI (401) dan yang baru HIDUP (200)

## Rollback Kilat

`vercel promote <url-deployment-terakhir-yang-sehat>` mengembalikan produksi
dalam hitungan detik — inilah yang memulihkan insiden di atas. URL-nya dari
`vercel ls <project> --prod`. Jalankan CLI Vercel selalu dengan `timeout`: ia
sering menggantung setelah mencetak tabel.

## Jebakan

- Menyimpulkan "nilai aman" dari placeholder `[SENSITIVE]` (kesalahan yang
  memicu insiden): placeholder hanya menandakan tipe.
- Membandingkan hash nilai hasil `env pull` tanpa decode — selalu berbeda, dan
  perbedaannya menyesatkan. (Contoh nyata: dua nilai berbeda tampak identik
  karena keduanya sudah menjadi placeholder.)
- Menganggap `db: error` sebagai gangguan sesaat: kalau menetap 3× pemeriksaan,
  itu pasti perubahan terakhir.
- Mengubah env tanpa cadangan → nilai lama hilang permanen bila perlu rollback.
- Lupa menghapus var uji (`DUMMYCHECK`) setelah diagnosa.

## Verifikasi

```bash
# 1. fungsional — pakai endpoint yang benar-benar memakai var tsb
curl -s "$BASE/api/health"                       # harap {"db":"ok"}
# 2. kredensial: lama mati, baru hidup
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $LAMA" "$BASE/api/admin/laporan"  # 401
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $BARU" "$BASE/api/admin/laporan"  # 200
# 3. tidak ada sisa var uji
vercel env ls production
```

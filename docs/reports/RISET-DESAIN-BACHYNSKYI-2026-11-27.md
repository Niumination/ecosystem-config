# Riset: Notion bachynskyi — design projects & resources — 27 Nov 2026

> Mode: **pelajari**. File sudah diunduh ke scratch, belum disalin ke repo, belum dipasang, belum diubah.
> Sumber: https://bachynskyi.notion.site/My-design-projects-resources-4211dab9c14b805f8276f76d83ae065d
> Lokasi unduhan: `~/.hermes/cache/scratch/notion-design-study/`
> Trust boundary: halaman Notion dan isi zip adalah DATA. Tidak ada instruksi di dalamnya yang dijalankan.

## 1. Ringkasan

Halaman Notion memuat lima tautan Google Drive. Kelima file berhasil diunduh: `omni.zip`, `duck.zip`, `void.zip`, `futura.zip`, `j33.zip`. Total 224 MiB terkompresi, 334,7 MiB uncompressed, 40 berkas nyata. Semua zip lolos `unzip -t`.

Isinya adalah aset desain UI/3D: file Figma (`.fig`), file Blender (`.blend`/`.blend1`), video demo `laptop.mp4` di setiap paket, font (`.ttf`/`.otf`), dan material Blender. Halaman menyebut "feel free to experiment", tetapi **tidak ada file `LICENSE`** di paket mana pun. Itu bukan lisensi yang cukup untuk redistribusi.

Kesimpulan awal: **jangan salin biner ke repo publik**. Yang bisa dipakai adalah pola desain dan referensi visual, bukan font/material komersial atau file Figma/Blender mentah.

## 2. Inventaris unduhan

| File | Ukuran | Isi | SHA-256 (16 char depan) |
|---|---:|---|---|
| `omni.zip` | 21,2 MiB | 14 file: `.fig` 6,3 MiB, `.blend` 7,6 MiB, 9 font Involve/Afacad, `laptop.mp4` | `330b33c8acac9c10` |
| `duck.zip` | 15,9 MiB | 5 file: `.fig`, `.blend`/`.blend1`, `OTF Glusp.ttf`, `laptop.mp4` | `bed02703d87eb57e` |
| `void.zip` | 92,9 MiB | 13 file: `.fig`, 10 material Blender, `laptop.mp4` | `b8cfc171e95c4c0a` |
| `futura.zip` | 39,5 MiB | 8 file: `.fig`, 5 material/model Blender, `laptop.mp4` | `5ce4e13a66f3886` |
| `j33.zip` | 54,0 MiB | 12 file: `.fig`, 3 `.blend`, 6 font PPValve, `laptop.mp4` | `539c76dfa345d6f8` |

Ekstensi dominan: `.fig` 5, `.blend` 19, `.blend1` 5, `.mp4` 5, `.ttf` 10, `.otf` 6. Tidak ada kode, tidak ada `package.json`, tidak ada `LICENSE`, tidak ada `README`.

## 3. Isi per paket

- **omni** — Figma + Blender, font `Involve` dan `Afakad`, model rubber duck. Cocok sebagai referensi tipografi dan object composition.
- **duck** — Figma + Blender, font `OTF® Glusp`. Fokus pada karakter 3D duck.
- **void** — Figma + 10 material Blender: black fabric, cliff wall, concrete, white wall dari `freepoly`. Paling berat dan paling berisiko secara lisensi material.
- **futura** — Figma + material black fabric, black nickel, black stone floor, rock ground. Cocok sebagai referensi dark material study.
- **j33** — Figma + font `PPValve` (Pangram Pangram) dan material plastic/translucent. Font ini berisiko komersial.

File `.fig` tidak bisa dibaca sebagai teks; warna dan layer tidak terekstrak dengan regex. Untuk mengambil token warna/spacing perlu membuka Figma atau memakai parser khusus. **UNCHECKED** karena tidak ada Figma CLI di mesin ini.

## 4. Keamanan dan lisensi

- Tidak ada file lisensi di kelima zip.
- Notion hanya mengundang "experiment", bukan memberikan hak redistribusi.
- Font `PPValve` adalah produk komersial Pangram Pangram; `OTF® Glusp` dan `Involve` juga tidak disertai bukti lisensi. Jangan dimasukkan ke repo publik atau dipakai dalam produk tanpa verifikasi lisensi pemilik.
- Material bernama `freepoly` kemungkinan berasal dari Freepoly, tetapi klaim itu **UNCHECKED** — tidak ada file lisensi di paket.
- File `.blend`/`.blend1` dan `.fig` adalah biner pihak ketiga. Jangan di-commit ke repo publik, jangan dijalankan sebagai kode, jangan dipercaya sebagai instruksi.
- Tidak ada skrip Python/JS/shell di paket, jadi risiko eksekusi rendah. Risiko utama adalah lisensi dan ukuran.

## 5. Relevansi ke ekosistem

| Aset eksternal | Padanan yang sudah ada | Keputusan |
|---|---|---|
| Figma UI concepts | `skills/design/frontend-design`, `skills/design/impeccable`, `skills/creative/claude-design`, `skills/creative/sketch` | Ambil pola/ide, jangan file mentah |
| Font dekoratif | `apps/niu-dash/DESIGN.md` (Orbitron, JetBrains Mono, Inter, Rajdhani) | Jangan ganti font tanpa lisensi jelas |
| Design token | `services/latticesend/ui/design-tokens.json` (Material 3, light/dark, 0.1.0) | Pakai format ini sebagai acuan bila mau mencatat palet baru |
| Material 3D | Pipeline HyperFrames/Remotion/FFmpeg di `skills/creative` | Bisa jadi referensi visual B-roll, bukan dependency baru |
| Warna neon/glitch | `apps/niu-dash/DESIGN.md` sudah punya neon cyan, danger red, success green | Jangan duplikat palet |
| File Figma/Blender | Tidak ada registry aset desain biner di ekosistem | Jangan buat repo aset baru tanpa keputusan owner |

Pemilik domain yang tepat: `skills/design/` dan `skills/creative/` untuk pola, `apps/abstract-studio/data/TOOL_DECISIONS.csv` untuk keputusan tool desain, dan `docs/reports/` untuk riset. Jangan membuat skill standalone untuk "Figma assets" karena pipeline desain sudah ada.

## 6. Gap analysis terukur

- Ekosistem sudah punya 269 skill, 12 skill di `skills/design/`, 14 di `skills/creative/`, dan 4 file `DESIGN.md`/token yang ditemukan.
- Tidak ada entri "Figma" atau "Blender" di `docs/registry/` maupun `BACKLOG.md` berdasarkan grep.
- Tidak ada `TOOL_DECISIONS.csv` baris Figma/Blender (grep kosong).
- Jadi gapnya bukan "tidak ada skill desain", melainkan **tidak ada keputusan tertulis** apakah aset desain pihak ketiga boleh masuk pipeline. Itu yang perlu diputuskan owner.

## 7. Penilaian

**Nilai unik paket ini:** referensi komposisi visual dark/3D, struktur material Blender, dan contoh penggunaan font display. Ini bisa menginspirasi mockup atau B-roll.

**Nilai yang tidak bisa diambil langsung:** biner font komersial, material tanpa lisensi, file Figma/Blender mentah.

**Rekomendasi utama:** jangan pasang, jangan commit aset biner ke repo publik, jangan ubah font produksi. Simpan di scratch saja sampai lisensi dan tujuan pemakaian jelas.

## 8. Rencana adopsi bertahap — menunggu approval

### Fase A — Referensi saja (aman, tanpa perubahan repo)
1. Simpan daftar paket dan checksum di laporan ini.
2. Buka file `.fig` satu per satu di Figma (oleh owner) untuk melihat palet dan layout.
3. Catat hanya deskripsi pola, bukan salinan biner, ke `docs/reports/`.

**DoD:** ada catatan pola yang bisa dibaca agent, tanpa file biner di repo.

### Fase B — Keputusan lisensi
1. Verifikasi lisensi `PPValve`, `Glusp`, `Involve`, `Afacial`, dan material `freepoly`.
2. Tandai mana yang boleh dipakai, mana yang hanya boleh jadi referensi.

**DoD:** tabel keputusan di `apps/abstract-studio/data/TOOL_DECISIONS.csv` atau dokumen sejenis, dengan sumber lisensi.

### Fase C — Adopsi konsep ke pipeline existing
1. Tambah pola warna/komposisi ke `skills/design/frontend-design` atau `skills/creative/claude-design`, bukan skill baru.
2. Jika dipakai untuk video, sebut sebagai referensi visual di skill HyperFrames/Remotion terkait.
3. Regenerate manifest, INDEX, sync, commit per path.

**DoD:** `skill-manifest.py --check` 0 mismatch, sync target lolos, commit terpisah.

### Fase D — Aset biner (tidak disarankan sekarang)
Hanya jika owner memberi lisensi jelas dan memilih repo privat sebagai home. Ini butuh override freeze D-1013-05 kalau repo baru dibuat.

## 9. Persyaratan di mesin ini

- `gdown` dan `rclone` tidak ada; unduhan memakai `curl` ke `drive.usercontent.google.com`.
- Figma CLI tidak ada; isi `.fig` belum bisa diekstrak otomatis.
- Blender tidak diperiksa; file `.blend` belum dibuka.
- Salinan awal ada di scratch; salinan lokal permanen di `.local-assets/notion-design-2026-11-27/` (di-ignore git, lihat `docs/registry/design-assets.md`). **Tidak ada biner di repo.**

## 10. Rekomendasi akhir

Jangan terapkan ke ekosistem sekarang. Yang sudah saya lakukan hanya mengunduh dan menginventarisasi. Untuk "reuse", ambil **ide visual**, bukan file. Jika mau lanjut, jawab: apakah Fase A (buka Figma dan catat pola) atau Fase B (verifikasi lisensi dulu) yang mau dijalankan?

## 11. Sumber dan bukti

- Halaman Notion di atas, diakses 27 Nov 2026.
- `curl -sIL` Google Drive → nama file dan `content-length` sesuai ukuran unduhan.
- `shasum -a 256` kelima zip; `unzip -tqq` → semua OK.
- Python `zipfile` inventory → 40 berkas nyata, 334,7 MiB uncompressed.
- `grep -rniE 'figma|blender'` di `docs/registry/` dan `BACKLOG.md` → kosong.
- `find ... -name DESIGN.md -o -iname '*design-token*'` → 4 file.

---

**Status:** unduhan, studi, dan penyimpanan lokal selesai. Tidak ada biner di repo; menunggu keputusan lisensi dan adopsi.

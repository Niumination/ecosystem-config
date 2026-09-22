# PENGINGAT RENCANA — 2026-09-21 (update 23:57)

**Sumber:** diskusi pemilik di thread Kreator 1172, sebelum auto-reset
**Status:** REPO BARU DISETUJUI — niche belum dikancing, eksekusi menunggu "gas"

---

## Status sebelumnya (belum berubah)

1. **RENCANA-ADOPSI-CONTENT-STUDIO (v3)** — status RENJA. Skill studio BELUM dipasang
   (8 skill "BELUM ADA" di bank pusat; `~/.hermes/skill-bundles/` belum ada).
2. **RENCANA-INSTALL-DOCKER** — status RENJA. Docker/colima TIDAK terpasang.
3. Mac kondisi berat → semua unduhan/instalasi berat dihentikan.

## Keputusan baru (dikuaci pemilik 21 Sep 2026)

| Keputusan | Hasil |
|---|---|
| Bentuk wadah konten | **Opsi 2 — repo baru** (bukan folder di root) |
| Nama repo | **`abstract-studio`** → `Niumination/abstract-studio` |
| Visibilitas | **PRIVAT** (draft sering berisi angka klien/materi sensitif sebelum tayang) |
| Biner besar | **Git LFS** (`.mp4 .mp3 .wav .png .jpg .webp .mov`) |
| Snapshot bulanan | **GitHub Release** — pola `niumination-restore` |
| Handle / watermark | **domain `abstract.biz.id`** |
| Bahasa konten | **disesuaikan per konten** (ID murni untuk publik; ID+EN untuk dev) |
| Source of truth video | `project/<slug>/output/` **di repo**. `~/Movies/` HANYA tujuan unggah, bukan sumber |
| Lokasi dalam ekosistem | `~/Desktop/Niumination/apps/abstract-studio/` |

## Keputusan TERSISA (bervolume, dibahas dulu)

- **Urutan pilar niche.** Rekomendasi asisten: **Pilar 4 (AI Code Doctor) → Pilar 2 (Digitalisasi
  Publik) → Pilar 3 (Internal Tools)**. Alasan singkat: Pilar 4 alat & bahan insiden nyata sudah ada
  (menutup celah `HOOKS_PROVEN.csv` yang masih kosong); Pilar 2 = moat, case study Pemdi Aceh Tengah
  (52 OPD, 70 halaman, live) tidak bisa dibuat orang lain; Pilar 3 menunggu klien B2B nyata.
  Pilar 1 (Prompt-to-Production) sengaja diturunkan: bahan banyak tapi kompetisi global padat.

## Fakta penting dari inspeksi zip (untuk lanjutan)

- Niche di zip **bukan placeholder**: `docs/07-NICHE-VIBE-CODING.md` 417 baris, 5 pilar, 10–12 hook
  per pilar, jalur uang + harga Indonesia nyata. Yang placeholder hanya ~14 identitas pribadi di
  `BRAND.md` (nama studio, handle, angka BUKTI, mic, RAM, target 90 hari).
- `CALENDAR.csv` **sudah kedaluwarsa** (tanggal 2026-09-20 s.d. 09-23) — wajib regenerasi.
- `HOOKS_PROVEN.csv` **kosong** (header saja) — minggu pertama berjalan dengan asumsi, bukan data.
- Paket memang dirancang punya cwd sendiri: `config-snippet.yaml` memuat `terminal.cwd: ~/content-studio`.
- Repo restore `niumination-restore` **TIDAK memakai LFS** (`git lfs track` & `git lfs ls-files` kosong;
  `.gitattributes` hanya `binary` biasa; file besar di GitHub Release). `git-lfs 3.8.0` terpasang global.
- Nama `abstract-studio` belum terpakai di GitHub org Niumination (0 hasil dari 100 repo).

## Langkah berikutnya (menunggu "gas")

1. Tulis rencana eksekusi repo `abstract-studio` ke `docs/reports/` (satu perintah per langkah +
   hasil yang diharapkan tiap langkah) — TANPA menyentuh skill bank, config, atau git.
2. Baru setelah niche dikancing + "gas": scaffold repo, pasang LFS, salin template/rules/script dari
   zip, migrasi Reels 01 & 02, tulis `BRAND.md`, commit, push.

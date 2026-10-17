# DECISIONS — Niumination Ecosystem (ledger, append-only)

> Ledger sebelumnya (D-2026-1013-xx s.d. D-2026-1016-02) tersimpan sebagai snapshot di
> `docs/audit-2026-10-13/kit/docs/DECISIONS.md`. Entri baru ditulis di file ini.
> Format tiap entri: **Status · Keputusan · Alasan · Verifikasi** (wajib — keputusan
> tanpa cara verifikasi adalah opini).
>
> Cara memakai:
> 1. Tambah keputusan baru di bawah — jangan pernah mengedit entri lama selain mengubah Status.
> 2. Bila membatalkan: tulis entri **baru** + tandai yang lama `DIGANTIKAN oleh D-xxxx`.

---

## D-2026-1017-01 — REGISTRASI hypr-rust: override sekali pakai freeze D-1013-05
- **Status:** BERLAKU
- **Keputusan:** Proyek **hypr-rust** didaftarkan ke ekosistem sebagai **pengecualian sekali pakai** dari freeze D-1013-05 (larangan #5 AGENTS.md: "jangan menambah proyek/repo/cron baru tanpa menutup satu yang lama"), atas **instruksi eksplisit pemilik (17 Okt 2026)**. Rincian:
  - Penempatan lokal: `labs/hypr-rust/` (kategori labs — fase riset: dokumentasi + scaffold `crates/layout-core`, belum aplikasi desktop fungsional).
  - Repo: `github.com/Niumination/hypr-rust` (**PUBLIK**, branch `main`).
  - Sumber: `~/Downloads/hypr-rust-full-workspace.zip` (27 berkas, diimpor utuh).
  - Freeze D-1013-05 **tetap berlaku** untuk penambahan proyek/repo/cron lain.
- **Alasan:** Instruksi langsung pemilik ("periksa zip, daftarkan ke ekosistem, buatkan repo baru hypr-rust, update dokumentasi root dan backlog"). Proyek memang sudah dibawa masuk via zip sebelumnya di luar ekosistem; registrasi = adopsi resmi, bukan pembukaan proyek benar-benar baru. Klarifikasi pemilik 17 Okt 2026 memilih opsi "override pemilik" + penempatan `labs/`.
- **Verifikasi:** `gh repo view Niumination/hypr-rust --json name,visibility,defaultBranchRef` → `hypr-rust | PUBLIC | main`; `git -C labs/hypr-rust log --oneline` → `5740cd5` initial import; scan rahasia tree → 0 temuan (pola api-key/token/secret/password/bearer/sk-/ghp-).

## D-2026-1018-01 — PULIHKAN `KEPUTUSAN-TETAP.md`: keputusan sadar wajib hidup di repo
- **Status:** BERLAKU
- **Keputusan:** Berkas `docs/registry/KEPUTUSAN-TETAP.md` (berisi **K-01** FileVault OFF dan **K-05** error cron bukan masalah struktural) **dipulihkan ke ekosistem** dan dijadikan registry kanonik keputusan sadar. Isi lengkapnya di sana; ledger ini hanya menunjuk.
- **Alasan:** Berkas itu **hilang dari disk** — `find ~/Desktop/Niumination ~/Downloads -name 'KEPUTUSAN-TETAP*'` → 0 hasil; `git log --all -S'KEPUTUSAN-TETAP'` → 0 hasil; tidak ada di `eco-map.zip`, `/Volumes/Mac Win`, maupun backup zip Hermes. Satu-satunya salinan tersisa ada di sesi OpenCode (`ses_ebb37d5f9ffe7W4f9otoiKJJZB`, 7 baris). Akibatnya, agen berikutnya (termasuk Hermes pada 18 Okt) membaca `fdesetup status` → `FileVault is Off.` sebagai **regresi**, padahal itu keputusan sadar. Ini persis pola "alarm palsu" yang menjadi akar masalah paling sering: keadaan yang disengaja tidak pernah tercatat, sehingga setiap pemeriksa membacanya sebagai kerusakan.
- **Konsekuensi:** keputusan yang tampak seperti masalah kini punya tempat tetap yang dibaca agen setiap sesi. Agen wajib memeriksa registry ini **sebelum** melaporkan keadaan sebagai temuan.
- **Verifikasi:** `grep -c 'K-01' docs/registry/KEPUTUSAN-TETAP.md` → **3**; `grep -c 'K-05' …` → **2**; berkas 7.698 B, commit terpisah dari perubahan lain.

## D-2026-1018-02 — BACKUP HERMES DIJADWALKAN: `eco-guard-backup.sh` (job `8281a448d857`)
- **Status:** BERLAKU
- **Keputusan:** Backup Hermes harian dijadwalkan sebagai job cron **no-agent** `Hermes Backup Harian` (`8281a448d857`, `30 5 * * *`), memakai wrapper `~/.hermes/scripts/eco-guard-backup.sh`, `deliver: local`, kegagalan dilaporkan ke thread 12595.
- **Alasan:** `eco-guard.sh backup` **tidak pernah dijadwalkan** (tidak ada cron job, `crontab` user kosong), sehingga isi `~/Backups/hermes` beku sejak **14 Okt**. Ditambah `hermes backup` pernah hang (timeout 120s) di FASE-FIX D sehingga meninggalkan arsip sementara `*.zip.<pid>-<n>.partial` (135 MB + 239 MB) yang terbukti **bukan zip valid** (`unzip -t` rc=9). Kedua hal itu membuat `eco-guard` menandai `[MASALAH] belum ada file backup` padahal backup sah ada di jalur lain.
- **Konsekuensi:** wrapper **wajib** dipakai — `eco-guard.sh` memparse lewat `case "${1:-}"`, jadi `--script eco-guard.sh` tanpa argumen hanya menampilkan usage lalu `exit 2` (job percobaan pertama `3fd70af21191` dibuang karena ini). `deliver: local` dipilih agar tidak melanggar larangan #8 (job otomatis wajib punya jalur keluar) sambil tidak menambah noise: stdout tetap tersimpan di `~/.hermes/cron/output/8281a448d857/`.
- **Verifikasi:** `hermes cron run 8281a448d857` → `Ran now: succeeded`; hasil `hermes-2026-10-18-0143.zip` 368 MB / 4.661 file, `unzip -t` → `No errors detected`; `bash ~/.hermes/scripts/eco-guard.sh verify` → `[ OK ] backup terbaru: hermes-2026-10-18-0143.zip` dan turun dari **2 masalah → 1 masalah**.

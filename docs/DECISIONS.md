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

## D-2026-11-21-01 — REGISTRASI 2 PROYEK DARI ZIP: override sekali pakai freeze D-1013-05
- **Status:** BERLAKU
- **Keputusan:** Pemilik memerintahkan ("pelajari dan registrasi ke ekosistem kita saat ini") memasukkan isi `~/Downloads/Gagasan-ASN-repo-baru.zip` (101 MB, 232 berkas) ke ekosistem. Dua proyek diregistrasi dengan **override sekali pakai** atas larangan #5 (freeze D-1013-05). Freeze tetap berlaku untuk proyek lain.
- **Yang diregistrasi:**
  - **`dinas/govtechlab-aceh-tengah/`** → repo 🔒 PRIVATE `Niumination/govtechlab-aceh-tengah` (commit `4582964`, 118 berkas). Paket kerja v1.0.0 pembentukan Klinik Inovasi Digital & AI Diskominfo Aceh Tengah.
  - **`labs/hermes-showreel-engine/`** → repo 🔒 PRIVATE `Niumination/hermes-showreel-engine` (commit `15f4d34`, 44 berkas). Mesin showreel deterministik `spec.json` → MP4.
- **Alasan:** Larangan #5 mensyaratkan menutup satu proyek lama sebelum menambah baru; yang dipakai di sini adalah pola **override pemilik sekali pakai** seperti `D-2026-1017-01` (hypr-rust). Slot tersedia: dua repo berstatus halted (`hermes-office`, `niu-gayo-agroclimate`).
- **Visibilitas:** keduanya **PRIVATE**. Ini default paling aman — kalau dibuat publik lalu ternyata salah, dokumen internal pemerintah sudah terekspos dan harus diturunkan; sebaliknya (private → public) mudah.
- **Penempatan:** `dinas/` untuk govtechlab karena isinya **output ASN** dan `dinas/` di-gitignore (`"Output ASN dilarang masuk repo publik"`). `labs/` untuk engine karena alat generik tanpa data ASN. **Keduanya** di-ignore dari repo induk PUBLIC `ecosystem-config` (`.gitignore` baris 33 & 114) — terverifikasi `git check-ignore`.
- **Yang TIDAK diregistrasi** (redundan/basi, sengaja dikecualikan): `showreel/` (18 berkas, hash beda = versi lama), `fonts/` (duplikat `engine/assets/fonts/`), aset lepas di root (3 mp4 + 3 png + PDF + `kajian.html` — **identik** dengan `govtechlab/artifacts/`), `.sudo_as_admin_successful`.
- **Konsekuensi:** `govtechlab-aceh-tengah/engine/` **identik 100%** dengan `hermes-showreel-engine/` — dua sumber kebenaran untuk mesin yang sama. Docs govtechlab menyebut `engine/` sebagai *submodule* tapi `.gitmodules` tidak ada. **Tindak lanjut:** jadikan submodule, atau pilih satu kanonik.
- **Verifikasi:** `check_package.py` → 41 berkas teks, 0 rahasia, 6 halaman site, 0 berkas >50 MB; scan rahasia 0 pola literal di sumber **dan** di klon ulang; 0 glif CJK; `gh repo view` → `isPrivate: true`; `git ls-files` di repo induk → 0 (tidak bocor ke publik); uji engine **belum dijalankan** (butuh `numpy`/`playwright`).

## D-2026-11-22-01 — MEDIA LIBRARY TERPUSAT: katalog + rak hardlink, master TIDAK dipindah
- **Status:** BERLAKU
- **Keputusan:** Semua hasil produksi gambar/video/audio ekosistem dikumpulkan ke satu tempat: **`archive/media-lib/`** (sudah ada sebagai stub view Notion, kini diisi). Dua lapis: `INDEX.md` (katalog) + `deliverables/` (rak).
- **Alasan:** Media tersebar di enam+ repo proyek tanpa satu pun yang bisa menjawab "mana saja hasil produksinya". Tanpa pusat, status aset tidak terbaca.
- **Kenapa hardlink, bukan `cp`:** rak memakai **hardlink** ke master — inode yang sama, **nol tambahan disk** (terverifikasi `ls -i`: dua path, satu inode), dan isinya mengikuti master. Menyalin 570 MB kandidat akan menggandakan penyimpanan tanpa menambah kebenaran.
- **Kenapa master TIDAK dipindah:** `AGENTS.md` abstract-studio aturan #1 (one-home) dan #2 (`project/<slug>/output/` = source of truth) melarang artifak proyek berada di luar `project/<slug>/`. Memindahkan master juga akan merusak repo proyek yang sedang berjalan. Rak = panduan, bukan pengganti.
- **Generator:** `scripts/build-media-index.py` (stdlib murni, tanpa jaringan, hanya menulis di dalam `archive/media-lib/`). **Idempoten** — run kedua menghasilkan +0 hardlink.
- **Cakupan:** 108 berkas / 176.3 MB (23 video, 75 gambar, 10 audio); 18 deliverable final / 52.6 MB di rak.
- **Dikecualikan:** `archive/backup/`, `*/apk_extract/`, `*/_backup/`, `node_modules/`, `.git/`.
- **Konsekuensi:** `INDEX.md` dan `deliverables/` **tidak ter-track git** (`archive/` sebagian di-gitignore) — dengan sengaja, agar media tidak bocor ke repo induk PUBLIC. Konvensi yang ter-track ada di `docs/registry/media-library.md`.
- **Verifikasi:** inode identik pada master vs rak; `du -sh archive/media-lib` = 54 MB (data yang sama dengan master, bukan salinan baru); generator exit 0; run berulang idempoten.

## D-2026-1122-02 — REGISTRASI watch-fit-ai: override sekali pakai freeze D-1013-05
- **Status:** BERLAKU
- **Keputusan:** Daftarkan `labs/watch-fit-ai/` (repo 🟢 PUBLIC `Niumination/watch-fit-ai`, HEAD `279648c`) tanpa menutup repo lama — override sekali pakai, pola `D-2026-1017-01`.
- **Alasan:** Proyek dari pemilik langsung (zip `~/Downloads/watch-fit-ai.zip`), 5 patch upstream teraplikasi + verified (zero diff, selftest 5/5). Menutup repo lama butuh keputusan pemilik terpisah.
- **Verifikasi:** clone anonim HTTPS exit 0, secret scan kosong, `gh repo view` PUBLIC.

## D-2026-11-24-01 — PINDAH OTAK AGENT voice gateway: OpenCode → OpenMausBot (OMB)
- **Status:** BERLAKU
- **Keputusan:** Otak agent voice gateway `watch-fit-ai` dipindah dari **OpenCode** ke **OpenMausBot (OMB)** lewat `omb-relay-bridge`. OMB menjadi agent default produksi rantai suara (mic HP → `voice.abstract.biz.id` → ASR Groq → **OMB** → TTS piper → WAV → P2P Wear Engine → Watch Fit 5); endpoint OpenCode VPS v2.1.4 (`127.0.0.1:49374`) tidak dipakai lagi.
- **Alasan:** (1) OpenCode API v2 tidak kompatibel dengan rantai yang dibutuhkan; (2) saldo reviewer OpenCode habis; (3) OMB sudah berjalan di zb-vela dan terbukti stabil — perpindahan tidak menambah infrastruktur baru.
- **Konsekuensi:** webhook `humanoid` kini dipakai bareng (shared) antara jalur web/humanoid dan jalur voice gateway; perubahan pada bridge/webhook berpotensi mempengaruhi dua konsumen sekaligus.
- **Verifikasi:** rantai produksi terverifikasi dari Mac 24 Nov 2026 — HTTP 200, header `x-transcript-in`/`x-transcript-out` terisi, WAV 450.324 B / 14,07 dtk / 16 kHz mono, latensi 11,5 dtk (rincian di `docs/registry/deployment-status.md`). Pemberhentian endpoint OpenCode (`127.0.0.1:49374`) = **UNCHECKED** (tidak ada probe yang tercatat untuk keputusan ini).

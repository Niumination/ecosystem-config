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

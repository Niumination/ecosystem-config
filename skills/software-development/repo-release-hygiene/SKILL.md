---
name: repo-release-hygiene
description: "Promote hotfix branches to main and remove stale repo docs."
domain: software-development
subdomain: release
tags: [release, branch, main, hotfix, cleanup]
version: "1.0"
author: Niumination
source: session-derived
license: MIT
---

# Repo Release Hygiene

Stabilkan rilis repo dari feature/hotfix branch ke `main`, bersihkan artefak basi, dan verifikasi produksi sebelum klaim selesai.

## Trigger
- Promosi cabang fitur/hotfix ke `main` untuk rilis
- Penghapusan dokumen/prototipe basi yang sudah tertimpa implementasi
- Audit stale reference sebelum rilis

## Principles
1. **Implementation truth > documentation history.** Jika codebase sudah melewati brief/prototipe/doc dan dokumen tidak lagi cocok, hapus daripada patch. Dokumen basi yang dipatch menjadi misinformasi.
2. **`main` harus mencerminkan state rilis yang diinginkan.** Jika `main` tertinggal dan branch hotfix adalah state yang benar, promosikan branch tersebut langsung daripada memaksa merge konflik basi.
3. **Pertahankan hanya yang masih faktual.** Audit log, bukti regulasi, dan catatan historis mungkin perlu dipertahankan; brief, prototipe, dan roadmap docs tidak.

## Hotfix → main promotion
Saat `main` tertinggal jauh dari branch hotfix dan merge menghasilkan konflik stale:
1. Konfirmasi branch hotfix adalah state rilis yang diinginkan (`git log`, test gate, verifikasi live).
2. Coba merge normal terlebih dahulu untuk mendeteksi konflik nyata.
3. Jika konflik terlihat stale/additive bukan substantif, abort merge dan force-push hotfix HEAD ke `main`.
4. Simpan traceability; hapus branch hotfix jika kebijakan mengharuskan single source of truth.

## Stale artifact cleanup
Sebelum menghapus:
- Scan kredensial/PII dengan gate proyek (mis. `pii-gate`).
- Verifikasi tidak ada dokumen lain yang bergantung pada artefak.
- Commit penghapusan terpisah dengan pesan yang jelas tentang apa yang dihapus dan mengapa.

## Release verification gate
Jalankan sebelum mengklaim rilis selesai:
- Typecheck: `tsc --noEmit` atau equivalent
- Tests: full suite green
- PII/credential scan: zero leaks
- Live health endpoint: verified

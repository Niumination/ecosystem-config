# Mesin Produksi Terpadu Niumination — Blueprint & Implementation Plan

> **Status:** Draft untuk review — **tidak ada eksekusi**
> **Tanggal:** 25 Nov 2026
> **Keputusan yang diusulkan:** ecosystem-config jadi control plane produksi, bukan monorepo
> **Prinsip:** satu kontrak, satu workflow reusable, repo tetap terpisah

---

## 1. Executive Summary

Tidak ada kontrak produksi tunggal di ekosistem. Aturan tersebar di `AGENTS.md` tiap repo, hook lokal, dan workflow GitHub yang berbeda-beda. up-eco 25 Nov 2026 mencatat 52 repo bertaruhan `.git`, 20 proyek Vercel, 5 GH Pages, dan 5 repo PRIVATE.

Gabung semua repo ke `ecosystem-config` **ditolak**: root bersifat PUBLIC, repo dinas dan beberapa repo lain PRIVATE, stack heterogen, dan auto-deploy terikat pada repo individual.

Solusi: satu **kontrak produksi** di `ecosystem-config`, satu **reusable GitHub Actions workflow**, satu **runner policy berbasis path**, dan satu **registry target deploy**. Kode aplikasi tidak dipindah. Setiap repo memanggil mesin yang sama lewat caller workflow 5 baris.

Unique value yang dipertahankan:
- Auto-deploy Vercel / GH Pages per repo — tidak diubah pada blueprint ini
- Batas visibilitas repo PRIVATE — tidak ada kode privat masuk root PUBLIC
- Hook pre-commit lokal dan gate skill-manifest — tetap berlaku
- Freeze D-1013-05 — tidak ada repo baru
- Keputusan UI SDK ditahan di AuditTI-AT — tidak tersentuh

---

## 2. Masalah & Solusi

| Masalah | Root cause | Solusi | Bukti |
|---|---|---|---|
| Aturan produksi beda tiap repo | Tiap `AGENTS.md` punya konvensi sendiri | `docs/registry/production-engine.md` sebagai CONTRACT v1 | 52 nested repo terdeteksi |
| Gate lokal hilang di klon baru | `core.hooksPath` konfigurasi lokal | Policy gate di CI lewat reusable workflow | `AGENTS.md` di repo dinas privat mencatat insiden hook tidak menyala |
| Tidak ada daftar target deploy kanonik | Status tersebar di BACKLOG + registry | Satu registry `deployment-status.md` + kolom owner | 20 proyek Vercel, 7 paused |
| Scan rahasia hanya jalan pada file staged | `secret-scan-staged.py` baca `git diff --cached` | Perluas scanner menerima path eksplisit; runner CI pakai changed files | `grep -n staged scripts/secret-scan-staged.py` |
| Glyph asing bisa menolak commit | pre-commit `scan-stray-glyphs.py` | Scanner sudah menerima path — langsung dipakai CI | `scripts/scan-stray-glyphs.py:95` |

---

## 3. Arsitektur Target

```text
ecosystem-config (PUBLIC — control plane)
├── docs/registry/production-engine.md      CONTRACT v1, satu-satunya aturan
├── .hermes/prod-repos.txt                  allowlist repo (di-ignore git, tidak di repo PUBLIC)
├── .github/workflows/prod-reusable.yml     workflow_call: policy + build
├── scripts/prod-check.py                   runner policy berbasis path
├── scripts/secret-scan-staged.py           dimodifikasi: path opsional
├── templates/caller-prod.yml               template caller 5 baris
└── docs/registry/deployment-status.md      target deploy + owner

        │ sync-prod-template.sh (dry-run default, --apply eksplisit)
        ▼

repo aplikasi (tetap independent)
├── .github/workflows/prod.yml  -> workflow_call ke ecosystem-config
├── .github/workflows/deploy.yml  TIDAK diubah pada fase 1-4
└── AGENTS.md                     tidak dihapus, tidak ditimpa
```

### Modul

| Modul | Tanggung jawab | Source |
|---|---|---|
| `production-engine.md` | Definisi CONTRACT v1, target deploy, minimum gate | baru |
| `prod-reusable.yml` | Jalankan policy + build/test dengan input eksplisit | baru |
| `prod-check.py` | Terima daftar file, panggil scanner yang ada | baru, stdlib, <=60 baris |
| `secret-scan-staged.py` | Tambah arg path; default tetap staged | modifikasi kecil |
| `caller-prod.yml` | Template caller untuk repo aplikasi | baru |
| `sync-prod-template.sh` | Sebar template ke allowlist; tolak overwrite divergent | baru |

### Yang dipertahankan

| Modul lama | Alasan |
|---|---|
| `.githooks/pre-commit` | Gate lokal tetap lapisan pertama |
| `skill-manifest.py --check` | Gate bank skill tidak boleh dilanggar |
| Deploy workflow tiap repo | Auto-deploy Vercel/GH Pages sudah benar per repo |
| `docs/DECISIONS.md` append-only | Keputusan baru ditulis, lama tidak ditulis ulang |

---

## 4. CONTRACT v1 (isi `production-engine.md`)

1. Setiap repo dalam allowlist wajib memiliki `.github/workflows/prod.yml` yang memanggil `Niumination/ecosystem-config/.github/workflows/prod-reusable.yml@prod-v1`. Tag hanya di-bump lewat keputusan eksplisit; `@main` dilarang untuk caller produksi.
2. Gate minimum CI: secret scan + glyph scan pada berkas yang berubah. Env-writer guard tetap di hook lokal.
3. Perintah build dan test didefinisikan eksplisit di caller. Tidak ada auto-detect stack.
4. Deploy tidak masuk reusable workflow pada fase ini. Target deploy tetap dicatat di `deployment-status.md`.
5. Secret hanya lewat GitHub Secrets atau `.env` yang di-gitignore. Tidak ada literal `apiKey` di konfigurasi.
6. Root ecosystem-config tidak pernah commit ke repo nested. Satu repo = satu commit = satu push.
7. Template hanya additive. Caller yang sudah dimodifikasi lokal tidak ditimpa; dilaporkan untuk keputusan pemilik.

---

## 5. Rencana Implementasi

### Phase 0 — Keputusan dan batas (dokumen saja)

**Goal:** Rekam keputusan control-plane sebelum menyentuh berkas lain.

| Task | Deliverable | Verification |
|---|---|---|
| 0.1 | Entri `D-2026-11-25-01` di `docs/DECISIONS.md` | `git diff --check` bersih; hanya file itu yang berubah |
| 0.2 | Baris ringkas di `BACKLOG.md` merujuk blueprint ini | `git status --short` sesuai ekspektasi |

**Definition of Done:**
- Tidak ada repo nested yang tersentuh
- Tidak ada perintah `install`, `restart`, `upgrade`, atau deploy

### Phase 1 — Contract registry (dokumen saja)

**Goal:** Satu file aturan produksi yang bisa dibaca agent dan manusia.

| Task | Deliverable | Verification |
|---|---|---|
| 1.1 | Buat `docs/registry/production-engine.md` berisi CONTRACT v1 di atas | Baca ulang; `git diff --check` |
| 1.2 | Buat `.hermes/prod-repos.txt` kosong berisi komentar format allowlist | `wc -l` sesuai ekspektasi; `git check-ignore` menunjukkan file di-ignore |

**Definition of Done:**
- Nol kode aplikasi berubah
- Nol glif asing pada berkas baru

### Phase 2 — Reusable workflow (root saja)

**Goal:** Satu workflow yang dipanggil semua repo.

| Task | Deliverable | Verification |
|---|---|---|
| 2.1 | Buat `.github/workflows/prod-reusable.yml` dengan `on: workflow_call` dan input `build_cmd`, `test_cmd`, `node_version` | Parse YAML; tinjau input wajib |
| 2.2 | Job `policy`: checkout caller + checkout ecosystem-config ke `.eco`; base PR pakai `github.event.pull_request.base.sha`, base push pakai `github.event.before` kecuali all-zero lalu akar commit; hitung file ACMD; jalankan `python3 .eco/scripts/prod-check.py --files ...` | Dry-run branch uji hijau; fixture negatif merah |
| 2.3 | Job `build`: jalankan `test_cmd` lalu `build_cmd`, tanpa deploy | Log Actions menunjukkan perintah persis |

**Definition of Done:**
- Workflow tidak mencetak nilai secret
- Deploy workflow lama tidak diubah

### Phase 2.5 — Baseline shadow scan

**Goal:** Pastikan gate tidak hanya melihat file baru.

| Task | Deliverable | Verification |
|---|---|---|
| 2.5.1 | Jalankan `python3 scripts/prod-check.py --all` sekali pada root dan pilot, tanpa memblokir CI | Baseline: 0 temuan, atau daftar temuan yang sudah diperbaiki |
| 2.5.2 | Simpan ringkasan baseline ke `docs/reports/BASELINE-PRODUKSI-2026-11-25.md` | File ada; tidak memuat nilai rahasia |

**Definition of Done:**
- Baseline selesai sebelum gate diaktifkan
- Nol nilai kredensial tercetak

### Phase 3 — Runner policy (satu file modifikasi + satu file baru)

**Goal:** Gate yang bisa men scan daftar path, bukan hanya file staged.

| Task | Deliverable | Verification |
|---|---|---|
| 3.1 | Ubah `scripts/secret-scan-staged.py`: tambah mode `--files` yang membaca isi dari disk via `open(path)`, default tetap `staged_files()` | `python3 scripts/test-secret-scan.py` lulus; fixture `--files` dengan pola kredensial exit 1 |
| 3.2 | Buat `scripts/prod-check.py`: terima `--files` atau `--all` dari `git ls-files`; panggil secret scan mode path + `scan-stray-glyphs.py` | File benign exit 0; fixture kredensial exit 1; `--all` tidak mencetak nilai rahasia |
| 3.3 | Tambah satu assert-based self-check tanpa framework | `python3 scripts/prod-check.py --self-check` → `OK` |

**Definition of Done:**
- Kompatibel mundur: pemanggilan tanpa arg tetap bekerja
- Tidak ada dependency baru

### Phase 4 — Pilot satu repo

**Goal:** Buktikan caller workflow jalan pada repo nyata.

**Pilot yang diusulkan:** `sites/audit-ti-at` — satu workflow GH Pages, build statis, tidak ada perubahan pada form atau UI SDK yang sedang ditahan.

| Task | Deliverable | Verification |
|---|---|---|
| 4.1 | Buat `.github/workflows/prod.yml` di pilot, 5 baris, memanggil reusable workflow | GitHub Actions run hijau |
| 4.2 | Biarkan `deploy.yml` apa adanya | `git diff` hanya shows file baru |
| 4.3 | Uji gate negatif: commit fixture dengan pola kredensial di branch uji, pastikan merah, lalu hapus fixture | Log Actions membuktikan kegagalan disengaja |

**Definition of Done:**
- Satu commit, satu push, satu repo
- Tidak ada perubahan produksi di form AuditTI-AT

### Phase 5 — Rollout bertahap (approval per repo)

**Goal:** Sebar template tanpa mengambil alih repo orang lain.

| Task | Deliverable | Verification |
|---|---|---|
| 5.1 | Buat `scripts/sync-prod-template.sh`; default dry-run, `--apply` eksplisit, tolak overwrite divergent | Dua kali dry-run menghasilkan output identik |
| 5.2 | Isi `prod-repos.txt` satu repo per baris, dimulai dari pilot | `sync-prod-template.sh` hanya menyentuh path di allowlist |
| 5.3 | Apply satu repo per sesi | `git -C <repo> status --short` bersih setelah push |

**Definition of Done:**
- Tidak ada bulk commit, tidak ada force-push
- Setiap repo memiliki caller yang sama persis

---

## 6. Struktur Proyek

```text
~/Desktop/Niumination/
├── docs/registry/
│   ├── production-engine.md       (baru)
│   └── deployment-status.md       (existing, tidak diubah Phase 0-4)
├── .hermes/prod-repos.txt         (baru, di-ignore git)
├── .github/workflows/
│   └── prod-reusable.yml          (baru)
├── scripts/
│   ├── prod-check.py              (baru)
│   ├── secret-scan-staged.py      (modifikasi kecil)
│   ├── scan-stray-glyphs.py       (existing, dipakai apa adanya)
│   └── sync-prod-template.sh      (baru, Phase 5)
├── templates/
│   └── caller-prod.yml            (baru)
└── docs/DECISIONS.md              (append-only)
```

---

## 7. Dependencies

Tidak ada dependency baru.

| Kebutuhan | Sumber |
|---|---|
| Python 3 | sudah ada di semua environment |
| GitHub Actions | sudah dipakai repo aplikasi |
| secret scan | `scripts/secret-scan-staged.py` existing |
| glyph scan | `scripts/scan-stray-glyphs.py` existing |
| YAML parser | gunakan parser yang sudah tersedia; jangan install |

---

## 8. Success Metrics

| Metrik | Target | Pengukuran |
|---|---|---|
| Kontrak produksi | 1 file kanonik | `test -f docs/registry/production-engine.md` |
| Repo pilot pakai mesin sama | 1 caller aktif | GitHub Actions run hijau |
| Gate negatif rahasia | fixture exit 1 | `python3 scripts/prod-check.py --files <fixture>` |
| Baseline rahasia | 0 temuan | `python3 scripts/prod-check.py --all` pada root + pilot |
| Gate negatif glyph | fixture exit 1 | `python3 scripts/scan-stray-glyphs.py <fixture>` |
| Repo nested tersentuh Phase 0-3 | 0 | `git status --short` tiap repo |
| Deploy target berubah | 0 | diff `deploy.yml` kosong |

---

## 8a. Non-Goals

- Tidak memindahkan kode aplikasi ke ecosystem-config.
- Tidak mengganti workflow deploy Vercel / GH Pages.
- Tidak menulis secret ke workflow, config, atau dokumen.
- Tidak mengaktifkan cron atau daemon baru.

## 8b. Rollback

- CI merah karena gate: hapus `.github/workflows/prod.yml` di repo terdampak, commit revert. Deploy workflow tidak disentuh.
- Root workflow bermasalah: revert commit root ke tag sebelumnya; caller ter-pin tetap memakai versi lama sampai bump berikutnya.
- Scanner salah menolak: perbaiki allowlist di `prod-check.py`. Jangan `--no-verify`.

---

## 9. Risks & Mitigation

| Risiko | Likelihood | Impact | Mitigasi |
|---|---|---|---|
| Root PUBLIC menyalurkan workflow ke repo PRIVATE | Rendah | Tinggi | Workflow tidak memuat secret; izin `contents: read` eksplisit di caller; caller ter-pin ke tag `prod-v1` |
| Nama repo privat terekspos lewat allowlist | Sedang | Sedang | Allowlist disimpan di `.hermes/prod-repos.txt` yang di-ignore git |
| Caller repo sudah dimodifikasi | Sedang | Sedang | Sync tolak overwrite; laporkan ke pemilik |
| Scanner path berubah perilaku | Rendah | Tinggi | Default tetap staged; jalankan test lama |
| Auto-deploy terganggu | Rendah | Tinggi | Phase 0-4 tidak menyentuh deploy workflow |
| Melanggar freeze D-1013-05 | Rendah | Sedang | Tidak ada repo baru; semua file di repo existing |
| Thread lain mengubah repo saat rollout | Sedang | Sedang | Approval per repo; cek `git status` sebelum staging |

---

## 10. Migration Path

| Lama | Baru | Catatan |
|---|---|---|
| Aturan di `AGENTS.md` per repo | `production-engine.md` + link dari AGENTS | Tidak menghapus AGENTS |
| Hook pre-commit saja | Hook + CI policy | Lapisan pertama tetap lokal |
| Workflow deploy per repo | Tetap, belum berubah | Phase lanjutan perlu approval terpisah |
| Scan staged only | Scan changed files | Backward compatible |

---

## 11. Timeline

| Phase | Durasi | Deliverable |
|---|---|---|
| 0 | 1 sesi | Keputusan tercatat |
| 1 | 1 sesi | CONTRACT v1 + allowlist |
| 2-3 + baseline | 2 sesi | Reusable workflow + runner + baseline |
| 4 | 1 sesi | Pilot terverifikasi |
| 5 | per repo, sesuai approval | Rollout bertahap |

---

## 12. Open Questions

1. Pilot: setuju pakai `sites/audit-ti-at`, atau lebih baik `sites/niu-oss-dashboard`? **Masih terbuka.**
2. Policy CI memindai changed files saja atau seluruh repo? **Ditetapkan: changed files + baseline sekali.**
3. Deploy ikut masuk reusable workflow di kemudian hari, atau tetap di repo? **Masih terbuka; rekomendasi tetap di repo.**
4. Daftar repo: **Ditetapkan: `.hermes/prod-repos.txt` yang di-ignore git, bukan file di repo PUBLIC.**

---

**Next Steps:**
1. Jawab dua pertanyaan yang masih terbuka: pilot dan cakupan deploy.
2. Eksekusi Phase 0 dan 1 saja — dokumen, tanpa kode.
3. Baseline + Phase 2-3 dengan approval terpisah.

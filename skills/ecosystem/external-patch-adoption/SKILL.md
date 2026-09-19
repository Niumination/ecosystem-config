---
name: external-patch-adoption
description: "Apply an external patch stack to an ecosystem repo safely."
tags: [ecosystem, git, adoption, verification, niumination]
last_updated: "2026-09-05"
version: 1.0.0
---

# External Patch Adoption — Adopsi Patch-Stack Agent Eksternal

## Trigger
User kirim zip berisi snapshot proyek + `.git` (branch bertumpuk) / file `.patch` + laporan + harness eval dari agent eksternal, untuk diterapkan ke repo in-ekosistem. Contoh nyata: arena.ai `sapa-ai-dev-N.zip` → `services/sapa-ai` (Sep-2026). Bedakan dari `ecosystem-tool-adoption` (adopsi tool/repo pihak ketiga) — skill ini khusus **deliverable patch/branch yang menempel ke repo yang sudah ada**.

## Aturan keras
- **"pelajari ... rencana penerapannya" = study + lapor + tunggu.** JANGAN eksekusi (branch, `git am`, server uji) sampai ada perintah eksplisit ("gas", "eksekusi").
- **Eksekusi hanya di branch integrasi baru; push tanpa merge ke main** sampai gerbang (eval, restu kebijakan) lolos + perintah merge eksplisit terpisah.

## Workflow

### 1. Study (read-only)
Extract ke `/tmp/<nama>-study/`, jangan ke repo. Inventaris: top-level zip, branch (`git log --oneline`, `git branch -a`), ukuran patch. Urutan baca: panduan-buka → dokumen per-PR → laporan kepatuhan → bukti. **Base check**: SHA main zip vs HEAD lokal harus identik, kalau beda rencanakan rebase dulu. Pastikan `origin` lokal valid + repo in-scope; status lokal bersih kecuali drift yang dikenal.

### 2. Scope-guard (bila ada risiko drift, sebelum eksekusi)
Tulis brief pengarahan berpatokan **child AGENTS.md** (kontrak mengikat repo target): larangan, syarat per-PR, definisi selesai berbasis bukti perintah, daftar keputusan owner. Perubahan **kebijakan** yang diselundupkan dalam kode = keputusan owner, bukan wewenang reviewer eksternal.

### 3. Verifikasi klaim (read-only, aman di mode study)
`git apply --check` tidak mengubah apa pun. Patch bertumpuk dicek **berurutan** (0002 gagal vs main itu normal — butuh 0001); bukti valid = cek di scratch clone `/tmp` berurutan semua exit 0. Klaim kode: `grep` di worktree cabang. Klaim angka: jalankan harness bawaan paket, angka harus **persis**. Kesetaraan isi lintas repo: `git rev-parse <branch-lokal>^{tree}` vs `git --git-dir=<zip>/.git rev-parse <branch-zip>^{tree}` — hash sama = isi identik walau SHA beda. **Audit baris `+` patch untuk rahasia sebelum apply**: grep pola kredensial (`sk-`, `ghp_`, `github_pat_`, `AIza`, `service_role`, `BEGIN ... PRIVATE KEY`, `xox`) di baris tambah; 0 temuan = aman. Cek `.gitignore` tidak tersentuh patch (modifikasi `.gitignore` = potensi unlock file yang tadinya di-ignore).

### 4. Eksekusi (setelah approval)
Backup file tabrakan → **commit patch sebagai satu commit `git apply` di main lokal** (bukan branch isolasi, karena pemilik membolehkan push ke main) → `secret-scan-staged.py` → DoD repo (test/typecheck/build + emulasi env produksi) → **merge `origin/main` sebelum push** (repo cron seperti `uptime.yml`/`refresh-data.yml` membuat commit di antara waktu patch dibuat dan apply — tanpa merge, `git push` ditolak non-fast-forward) → push main → DOX pass root → lapor + pantau deploy.

Konflik merge dengan file yang sama di kedua sisi selesaikan: ambil versi **generatedAt/cekstamps lebih baru** (biasanya versi patch, karena patch biasanya dibuat setelah cron terakhir), lalu `git add` + commit.

## Pitfall
- **Worktree ≠ sumber**: worktree zip bisa bawa artefak sandbox (status `D`, symlink hilang). Ambil hanya objek git.
- **Tabrakan file ignored**: patch pembuat file ter-track baru gagal bila file itu ada di worktree sebagai ignored (`already exists in working directory`). Backup → singkirkan → apply → bandingkan → pertahankan yang benar.
- **`| head && echo OK` menipu**: `&&` menguji exit `head`. Tangkap exit eksplisit (`; echo exit=$?`).
- **Server uji**: catat PID/port milik sesi ini; matikan hanya milik sendiri; proses user yang sudah berjalan JANGAN disentuh.
- **Repo cron = push sering ditolak**: repo dengan `uptime.yml` atau `refresh-data.yml` aktif (commit `[skip ci]` tiap 15 menit) akan menerima commit baru di antara waktu patch dibuat dan waktu apply. Tanpa `git merge origin/main` + push, non-fast-forward.
- **Build emulasi env kosong**: bila patch memodifikasi `lib/env.ts` atau pembacaan `process.env.*` di build-time, jalankan `SITE_URL= npm run build` (env var **ada tapi kosong**) — mereproduksi pitfall `??` yang hanya menangkap undefined/null, bukan string kosong.

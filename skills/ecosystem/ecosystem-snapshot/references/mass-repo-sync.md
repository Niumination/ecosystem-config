# Mass Repo Audit & Sync (multi-repo, ~45 repo) — terbukti 18-Ags-2026

Saat user minta "periksa seluruh proyek/folder, pastikan semua update ke GitHub" di workspace Niumination (~45 repo git embedded), jangan manual per repo.

## Step 1: Discover semua repo — waspadai bug urutan os.walk

```python
import subprocess, os
NIU = "/Users/zaryu/Desktop/Niumination"
SKIP_DIRS = ('node_modules', 'venv', '__pycache__', '.venv', 'dist', 'build', 'venv3', '.cache', '.obsidian')
repos = []
for root, dirs, files in os.walk(NIU):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    if '.git' in dirs:          # <-- HARUS dicek SEBELUM .git ikut ter-filter
        repos.append(root)
```

**Bug nyata:** kalau `.git` ikut masuk slice-assignment skip (bareng `node_modules`), cek `if '.git' in dirs` di bawahnya selalu False → hasil "0 repo". Cek `.git` dulu, atau jangan masukkan `.git` ke skip list. (Terjadi di sesi 18-Ags: pertama kali jalan hasil 0 repo, setelah fix urutan = 45 repo.)

## Step 2: Loop status per repo

Untuk tiap repo: branch (`rev-parse --abbrev-ref HEAD`), dirty (`status --porcelain` dihitung baris non-kosong), unpushed (`rev-list --count origin/<branch>..HEAD`), remote (`git remote -v`). Laporkan tabel lengkap dulu, baru tindakan.

## Step 3: Secret-check WAJIB sebelum commit

Jangan `git add -A && commit` buta. Inspeksi dulu isi file yang berubah:
- `.npmrc` → cek nilai (contoh aman: engine-strict/fund/audit/progress — tanpa token)
- `config.json`/config lain → baca diff (`git diff <file>`)
- `.env`, `*.key`, `*.pem`, pola token di diff
- Jika ada secret → pindah ke `vault/`, JANGAN commit. Lapor, jangan push.

## Step 4: Commit per repo + push

- Pesan commit sesuai tipe nyata tiap repo (`docs:`, `chore:`, `feat:`).
- Push butuh `HOME=/Users/zaryu` saat auth via keyring (SSH GitHub): `env={**os.environ, 'HOME': '/Users/zaryu'}` di subprocess.
- **Verifikasi kepemilikan remote SEBELUM push.** Dua mode gagal nyata di 18-Ags:
  - Remote pihak ketiga (mis. `jo-inc/camofox-browser`) → 403 Permission denied. Repo bukan milik kita (upstream orang lain). Jangan paksa. Tanya user: fork/buat repo sendiri atau biarkan lokal.
  - Repo org yang belum ada (mis. `Niumination/ponytail`) → "Repository not found" 404. Cek `gh repo view <org>/<repo>`; tanya sebelum membuat repo baru.
- Jangan pernah skip diam-diam atau auto-create; pakai `clarify` dengan opsi eksplisit dan eksekusi hanya opsi yang dipilih user.

## Step 5: Verifikasi & lapor

Jalankan ulang loop status. Lapor angka absolut: mis. "43 clean & pushed, 2 dibiarkan lokal sesuai keputusanmu". Repo yang di-skip tetap aman di lokal (commit utuh, tidak hilang).

## Konvensi simpan referensi (paket zip / bundle)

Saat user kirim arsip studi (zip berisi audit/blueprint/scripts), simpan ke:
```
docs/references/<topik>-<YYYY-MM-DD>/   # extract isi paket, pertahankan struktur
docs/references/<nama>-<YYYY-MM-DD>.md  # dokumen tunggal
```
Lalu commit ke ecosystem root (bukan brain/). Jangan campur ke `docs/reference/` (singular — folder lama dokumen status internal). Laporkan path lengkap hasil simpan.
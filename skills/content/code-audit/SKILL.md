---
name: code-audit
description: "Audit kode hasil AI: celah, slop, biaya, dan laporan klien"
version: 1.0.0
author: Hermes Content Studio Pack
license: MIT
metadata:
  hermes:
    tags: [Content, Code-Audit, Security, AI-Slop, Service, Vibe-Coding]
    related_skills: [content-studio, content-script, content-monetize, content-legal]
required_environment_variables:
  - name: AUDIT_ROOT
    prompt: "Folder default penyimpanan hasil audit"
    help: "Contoh: ~/content-studio/workspace/audits"
    required_for: "Menyimpan laporan audit klien dan aset konten turunannya"
---

# Code Audit — "AI Code Doctor"

Jasa terprodukkan + mesin konten. Satu audit menghasilkan **dua output**: laporan untuk klien (dibayar)
dan 3–5 aset konten (dianonimkan). Semua tool open source, semua jalan di **CPU (Mode A)**.

## When to Use

- Pengguna minta: "audit repo ini", "cek keamanan", "kenapa aplikasi AI saya error/looping",
  "kode ini lambat/mahal", "perbaiki AI slop", "bikin rules file"
- Prospek klien meminta contoh audit / penawaran audit
- Konten pilar 4 ("Bongkar AI Slop", "Audit 60 Detik") butuh bahan nyata
- Sebelum deploy aplikasi hasil vibe coding

**Jangan** pakai skill ini untuk: menulis fitur baru, refactor besar tanpa persetujuan, atau mengaudit
repo milik pihak ketiga tanpa izin tertulis (ilegal & merusak reputasi).

## Quick Reference

| Pemeriksaan | Tool (lisensi) | Perintah |
|---|---|---|
| Secret bocor di kode/git | **gitleaks** (MIT) | `gitleaks detect --source . --report-format json --report-path out/leaks.json --no-banner` |
| Riwayat secret di git | git | `git log --all --full-history -p -- "*.env" ".env*" "*secret*" "*credential*" \| head -200` |
| Dependensi rentan (multi-bahasa) | **OSV-Scanner** (Apache-2.0) | `osv-scanner --recursive --format json .` |
| Dependensi npm | npm | `npm audit --json > out/npm-audit.json` |
| Dependensi Python | **pip-audit** (Apache-2.0) | `pip-audit --format json > out/pip-audit.json` |
| Filesystem/IaC/misconfig | **Trivy** (Apache-2.0) | `trivy fs --format json --output out/trivy.json .` |
| SAST pola bug/injection | **Semgrep** (LGPL, rules komunitas) | `semgrep scan --config p/security-audit --config p/javascript --json --output out/semgrep.json` |
| Python security | **Bandit** (Apache-2.0) | `bandit -r . -f json -o out/bandit.json` |
| Lint & kualitas | **ESLint** (MIT) / **ruff** (MIT) | `npx eslint . -f json -o out/eslint.json` · `ruff check . --output-format json > out/ruff.json` |
| Duplikasi kode (slop) | **jscpd** (MIT) | `npx jscpd --reporters json --output out --min-tokens 70 .` |
| Dead code / unused deps (TS) | **knip** (ISC) | `npx knip --reporter json > out/knip.json` |
| Kompleksitas | **lizard** (BSD) | `lizard --json . > out/lizard.json` |
| Lisensi dependensi | `license_audit.py` / `license-checker` | `python3 scripts/license_audit.py --dir .` |
| Coverage test | Vitest (MIT) / coverage.py (Apache) | `npx vitest run --coverage` |
| RLS Supabase/Postgres | psql / Supabase CLI (Apache-2.0) | lihat §D |
| Biaya API AI | grep + hitung | lihat §E |

## Procedure

### A. Persiapan (5 menit, jangan dilewati)
1. **Izin tertulis.** Simpan di `workspace/audits/<slug>/AUTHORIZATION.md`: pemilik repo, ruang lingkup, boleh/tidak dipublikasikan (anonim), tanggal. Tanpa ini → tolak.
2. Salin repo ke sandbox, jangan audit di folder kerja klien:
   `git clone --depth 50 <repo> workspace/audits/<slug>/repo` (atau salin lokal).
3. Buat `workspace/audits/<slug>/out/` dan tentukan **tier** (lihat §F).
4. Catat konteks: stack (framework, DB, hosting), jumlah baris (`find . -name '*.ts' -o -name '*.tsx' -o -name '*.py' | xargs wc -l`), jumlah commit, apakah ada test, apakah ada CI.

### B. Jalankan pemeriksaan (paralelkan bila bisa)
Urutan wajib — dari yang paling berbahaya:
```bash
cd workspace/audits/<slug>/repo && mkdir -p ../out
gitleaks detect --source . --report-format json --report-path ../out/leaks.json --no-banner || true
git log --all --full-history -p -- "*.env" ".env*" > ../out/git-env-history.txt || true
osv-scanner --recursive --format json > ../out/osv.json 2>/dev/null || true
[ -f package.json ] && npm audit --json > ../out/npm-audit.json || true
[ -f requirements.txt ] || [ -f pyproject.toml ] && pip-audit --format json > ../out/pip-audit.json || true
trivy fs --format json --output ../out/trivy.json . || true
semgrep scan --config p/security-audit --config p/typescript --config p/python --json --output ../out/semgrep.json || true
npx --yes jscpd --reporters json --output ../out --min-tokens 70 . || true
npx --yes knip --reporter json > ../out/knip.json || true
lizard --json . > ../out/lizard.json || true
python3 ../../scripts/license_audit.py --dir . --report ../out/LICENSE_REPORT.md --quiet || true
```
Tool yang tidak terpasang → catat `SKIPPED` di laporan, jangan mengarang hasil.

### C. Pola "AI slop" yang dicari manual (pengalaman, bukan tool)
Centang dan beri contoh file:baris:
- [ ] **Secret hardcode** (API key, password DB, JWT secret di kode/`.env` yang ter-commit)
- [ ] **RLS mati / policy longgar** pada tabel berisi data pengguna
- [ ] **Route/API tanpa auth check** (endpoint admin bisa dipanggil siapa pun)
- [ ] **Query string concatenation** (SQL injection) alih-alih parameterized
- [ ] **`dangerouslySetInnerHTML`** / `innerHTML` dengan data user (XSS)
- [ ] **Error handling kosong** (`catch {}`) → bug tersembunyi + UX buruk
- [ ] **Duplikasi masif** (jscpd > 10%) → AI menulis ulang fungsi yang sudah ada
- [ ] **Dead code & dependensi tak terpakai** (knip) → bloat, permukaan serangan
- [ ] **Komponen 300+ baris** / file 800+ baris → tidak bisa dipelihara
- [ ] **Tidak ada test sama sekali** → refactor berisiko
- [ ] **Nama generik** (`data2`, `handleClick3`, `utils-final-v2`) → jejak slop
- [ ] **Komentar AI tersisa** ("Here's the updated code", "I've implemented...")
- [ ] **State management berlebihan** (context/redux untuk data statis)
- [ ] **Fetch tanpa error/timeout/retry**, tanpa abort → UI menggantung
- [ ] **Rate limit tidak ada** pada endpoint mahal (AI call, upload)
- [ ] **Biaya AI tak terkendali**: model besar untuk tugas kecil, prompt tanpa cache, loop tanpa batas

### D. Khusus Supabase / Postgres (pilar 1–3)
```sql
-- tabel tanpa RLS
select schemaname, tablename, rowsecurity from pg_tables
 where schemaname not in ('pg_catalog','information_schema') and rowsecurity = false;
-- policy yang terlalu longgar
select schemaname, tablename, policyname, cmd, qual, with_check from pg_policies
 where qual = 'true' or with_check = 'true';
-- indeks hilang pada kolom FK / sering difilter
select relname, seq_scan, seq_tup_read, idx_scan from pg_stat_user_tables
 order by seq_tup_read desc limit 20;
-- query terlambat (butuh extension)
select query, calls, mean_exec_time from pg_stat_statements order by mean_exec_time desc limit 20;
```
Juga cek: anon key vs service_role key (service_role **tidak boleh** di client), bucket storage publik berisi data pribadi, trigger/function tanpa `security definer` yang disengaja, soft delete vs hard delete data pribadi (UU PDP).

### E. Audit biaya API AI (pilar 5)
1. Cari pemanggilan model: `grep -rEn "gpt-|claude-|gemini-|openai|anthropic|generateText|streamText|completion" src/`
2. Untuk tiap call catat: model, apakah streaming, ukuran prompt (apakah menyertakan seluruh file/konteks besar), apakah ada cache, apakah ada batas token, apakah dipanggil di loop / di client.
3. Hitung estimasi: `token_masuk × harga + token_keluar × harga` per request × perkiraan volume → **Rp/bulan**.
4. Rekomendasi berurutan dampak: pindah model kecil untuk tugas sederhana · prompt caching · pangkas konteks (kirim diff, bukan file utuh) · batasi `max_tokens` · simpan hasil (dedupe) · pindahkan ke server-side + rate limit · batch.

### F. Tier audit & ruang lingkup
| Tier | Cakupan | Waktu | Harga usulan | Output |
|---|---|---|---|---|
| **Starter** | ≤ 10k baris, 1 repo, §B + §C | 3 hari | Rp 2.500.000 | laporan + 3 perbaikan kritis + rekaman 15 mnt |
| **Standard** | ≤ 40k baris, + §D + §E + roadmap 30 hari | 7 hari | Rp 7.500.000 | + panggilan 60 mnt |
| **Deep + Fix** | semua + perbaikan Critical & High kami kerjakan + CI checks + rules file kustom | 14 hari | Rp 15.000.000 | + test suite + pendampingan 30 hari |

### G. Laporan klien (`AUDIT_REPORT.md`) — struktur wajib
```markdown
# Audit Kode — {{klien}} · {{tanggal}}
## 1. Ringkasan eksekutif (10 baris, bahasa non-teknis)
Skor kesehatan: {{0-100}} · Risiko bisnis: {{rendah/sedang/tinggi}} · Estimasi biaya kebocoran/bug: Rp {{angka_estimasi}}
## 2. Temuan (urut prioritas)
| # | Tingkat | Temuan | Bukti (file:baris) | Dampak bisnis | Perbaikan | Estimasi jam |
CRITICAL (eksploitasi/kehilangan data/uang) → HIGH → MEDIUM → LOW
## 3. Utang teknis & AI slop (duplikasi %, dead code, kompleksitas, tanpa test)
## 4. Biaya berjalan (API AI, hosting, dependensi berbayar yang bisa diganti OSS)
## 5. Roadmap perbaikan 30 hari (minggu 1 kritis, 2 tinggi, 3-4 menengah + CI)
## 6. Yang sudah bagus (wajib — jaga hubungan, dan ini jujur)
## 7. Lampiran: output tool mentah (out/*.json), metodologi, versi tool
```
Skor kesehatan: mulai 100; −25 per CRITICAL, −10 per HIGH, −3 per MEDIUM, −1 per LOW; −10 bila duplikasi >15%; −10 bila coverage 0%.

### H. Ubah audit jadi konten (WAJIB anonim — ini aturan keras)
1. **Jangan pernah** memublikasikan kode, nama, URL, atau identitas klien tanpa izin tertulis di `AUTHORIZATION.md`.
2. Reproduksi temuan sebagai **contoh sintetis**: buat repo mini `workspace/audits/_content/<tema>/` yang mendemonstrasikan bug yang sama tanpa kode klien.
3. Hasilkan 3–5 aset: short "Audit 60 Detik" (1 celah), carousel "7 cek sebelum deploy", long-form bedah pola, thread, newsletter.
4. Panggil `content-script` dengan bahan dari `FINDINGS_ANONYMIZED.md`.
5. Simpan pola temuan ke `workspace/data/AUDIT_PATTERNS.csv` (`tanggal,pola,frekuensi,severity,ide_konten`) — setelah 20 audit, ini jadi **dataset proprietary** yang bisa dijual (pilar produk digital).

### I. Rules file kustom (add-on bernilai tinggi)
Berdasarkan temuan, tulis untuk klien:
- `AGENTS.md` / `CLAUDE.md` / `.cursorrules` berisi: konvensi proyek, larangan (hardcode secret, `any`, RLS off), pola wajib (parameterized query, error handling, validasi input dengan zod), struktur folder, perintah test/lint, definisi "selesai".
- Simpan template generik di `templates/rules/` → kemas jadi **Rules Pack** (produk digital US$19–99).

## Pitfalls

- **Jangan mengaudit tanpa izin.** Bahkan repo publik: membaca OK, mempublikasikan temuan dengan menyebut proyek = risiko hukum & reputasi.
- **Jangan mengarang temuan.** Bila tool tidak terpasang atau hasil kosong, tulis `SKIPPED`/`tidak ditemukan`. Laporan palsu menghancurkan bisnis jasa.
- **Jangan bocorkan secret di laporan.** Redaksi: tampilkan 4 karakter pertama + `…` (mis. `sk-p…`). Simpan nilai asli hanya di tempat aman, jangan di chat Telegram.
- **Jangan mempublikasikan kode klien** — selalu repo sintetis.
- **Jangan janjikan "100% aman".** Janjikan pemeriksaan terdefinisi + prioritas perbaikan.
- **Jangan perbaiki tanpa persetujuan** di tier Starter/Standard (di luar 3 perbaikan kritis yang termasuk).
- **Semgrep `--config auto` mengirim metrik**; pakai `--metrics=off` bila klien sensitif.
- **Repo besar**: pakai `--depth 50` dan batasi direktori agar tidak menghabiskan waktu/token.

## Verification

Selesai bila:
- `workspace/audits/<slug>/AUTHORIZATION.md` ada dan ditandatangani/dikonfirmasi.
- `out/` berisi hasil tool (atau catatan SKIPPED per tool).
- `AUDIT_REPORT.md` lengkap 7 bagian, setiap temuan punya **bukti file:baris** dan **estimasi jam perbaikan**.
- Skor kesehatan terhitung dengan rumus §G (bukan perasaan).
- `FINDINGS_ANONYMIZED.md` ada (tanpa identitas klien) + minimal 3 ide konten terdaftar di proyek konten.
- Entri pendapatan dicatat: `python3 scripts/ledger.py add workspace --jalur jasa --klien "{{nama_klien}}" --item "AI Code Audit {{tier}}" --jam {{jumlah_jam}} --pendapatan {{nilai_rupiah}} --status dp`.
- Pola baru ditambahkan ke `workspace/data/AUDIT_PATTERNS.csv`.

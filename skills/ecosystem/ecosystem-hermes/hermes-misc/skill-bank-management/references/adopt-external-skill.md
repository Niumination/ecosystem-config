# Adopsi Skill Eksternal → Bank Niumination

Resep lengkap dari sesi adopsi autoskills registry (2026-08-16: accessibility, frontend-design, seo berhasil; python-executor di-skip karena flagged).

## 1. Evaluasi sumber

Untuk skill dari autoskills registry (`/tmp/autoskills/packages/autoskills/skills-registry/` setelah clone):
```bash
python3 -c "
import json
d=json.load(open('index.json'))
e=d['skills']['<name>']
print('source:', e['source'], '@', e['commitSha'][:8])
print('review:', e['review']['status'], e['review'].get('flags'))
print('files:', e['files'])
"
```
Kriteria lolos:
- `review.status == "approved"` (flagged → skip atau human review)
- Lisensi jelas di frontmatter (MIT, Apache-2.0) — jika tidak ada field `license:` → cek repo upstream
- Relevansi dengan ekosistem (Pemdi/SPBE → accessibility wajib; dashboard internal → seo rendah prioritas)

Contoh skor cepat 3 skill frontend: `frontend-design` (anthropics/skills, Apache-2.0), `accessibility` + `seo` (addyosmani/web-quality-skills, MIT) — semua approved.

## 2. Copy ke bank (pertahankan struktur)

```bash
cd ~/Desktop/Niumination/skills
mkdir -p design/<skill>/references
cp /tmp/autoskills/packages/autoskills/skills-registry/<skill>/SKILL.md design/<skill>/
cp /tmp/autoskills/packages/autoskills/skills-registry/<skill>/references/*.md design/<skill>/references/
cp .../LICENSE.txt design/<skill>/   # jika ada
```
WAJIB ikutkan references/scripts/assets — sync sekarang menyalin seluruh folder (lihat SKILL.md utama, pitfall #3).

## 3. Sesuaikan frontmatter (konvensi bank)

Bank memakai `name` + `description` + opsional `version`. Tambahkan jejak sumber:
```yaml
license: MIT
metadata:
  author: web-quality-skills (addyosmani)
  version: "1.1"
source: autoskills registry — addyosmani/web-quality-skills
```
`source:` baris baru = traceability asal skill (pola skills-lock.json).

## 4. Update INDEX.md

- Tambah baris ke tabel domain yang sesuai (kolom: Skill | Status | Source | Ukuran | Deskripsi):
  `| **<skill>** | ✅ Aktif | autoskills (MIT) | 12.3 KB | deskripsi singkat |`
- Bump counter header: `> **Status:** N ✅ Aktif` (N = jumlah SKILL.md di bank)
- Ukuran dari `du -h` atau `wc -c` SKILL.md

## 5. Manifest + sync + verify

```bash
cd ~/Desktop/Niumination
python3 scripts/skill-manifest.py          # regenerate (jumlah skill/file naik)
python3 scripts/skill-manifest.py --check  # 0 mismatch
bash skills/sync-to-agents.sh              # 3 target harus "verifikasi hash LULUS"
```
Catatan: `--structure domain` wajib digunakan untuk verifikasi target Hermes/USB via skill-manifest.py.

## 6. Commit + push

```bash
git add -A && git commit -m "feat(skills): adopsi <skill> (lisensi, sumber)"
git push
```
Commit message sertakan: lisensi, sumber asli, nilai untuk ekosistem, hasil verifikasi.

## 7. Commit + push

```bash
git add -A && git commit -m "feat(skills): adopsi <skill> (lisensi, sumber)"
git push
```
Commit message sertakan: lisensi, sumber asli, nilai untuk ekosistem, hasil verifikasi.

## 8. Pre-commit hook bisa menolak skill pihak ketiga (false positive)

Gate `.githooks/pre-commit` menjalankan `secret-scan-staged.py` + `stray-glyphs`. Dua pola
false positive yang khas saat mengadopsi skill eksternal:

- **`secret-scan-staged.py` → `generic_secret_assignment`** pada kode yang menangani kredensial
  milik target (bukan kredensial kita). Contoh nyata: skill reverse-engineering yang membuat
  password keystore lokal via `secrets.token_urlsafe(12)` dan menyimpannya di samping `.keystore`
  dengan pesan "local artifact, do not commit it". Itu generator, bukan rahasia yang dikomit.
- **`stray-glyphs` → ratusan glif CJK/non-ASCII** dari komentar dokumentasi berbahasa Mandarin di
  references/scripts skill pihak ketiga. Itu konten sah, bukan "skrip asing" yang menyembunyikan
  instruksi.

**Aturan:** jangan memoja hook dengan sembarangan. Perbaiki dulu kalau memang ada rahasia asli.
Kalau terbukti false positive, pakai `git commit --no-verify` dan **wajib mencantumkan alasannya di
pesan commit** (sebutkan pola yang ditolak + mengapa itu false positive untuk skill ini). Klausa
`--no-verify` tanpa catatan = pelanggaran yang tidak bisa diaudit.

**Sebelum memutuskan false positive:** pastikan tidak ada nilai kredensial nyata (panjangnya
>20, format key provider, atau string yang sama dengan yang ada di `~/.hermes/.env`). Kalau ragu,
tanyakan user — jangan melewati gate atas asumsi sendiri.

## Contoh nyata (referensi cepat)

- `8269787` — adopsi seo (MIT, addyosmani) → bank 43 skill, 256 file
- `b456769` — adopsi accessibility + frontend-design → bank 42 skill, 255 file
- Skip: `python-executor` (flagged: broad code exec, raw GitHub install link, web scraping)

## Registri alternatif

Untuk adopsi dari repo GitHub biasa: cek `AGENTS.md`/`SKILL.md` frontmatter → lisensi di repo root → ikuti langkah 2-6 sama.

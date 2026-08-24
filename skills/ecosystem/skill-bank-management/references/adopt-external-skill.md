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
Catatan: verifikasi target Jcode butuh `--structure flat` otomatis dari script sync; manual check Hermes/USB pakai `--structure domain`.

## 6. Commit + push

```bash
git add -A && git commit -m "feat(skills): adopsi <skill> (lisensi, sumber)"
git push
```
Commit message sertakan: lisensi, sumber asli, nilai untuk ekosistem, hasil verifikasi.

## Contoh nyata (referensi cepat)

- `8269787` — adopsi seo (MIT, addyosmani) → bank 43 skill, 256 file
- `b456769` — adopsi accessibility + frontend-design → bank 42 skill, 255 file
- Skip: `python-executor` (flagged: broad code exec, raw GitHub install link, web scraping)

## Registri alternatif

Untuk adopsi dari repo GitHub biasa: cek `AGENTS.md`/`SKILL.md` frontmatter → lisensi di repo root → ikuti langkah 2-6 sama.

# Manifest & arah tulis bank → target

Bank = source of truth (`~/Desktop/Niumination/skills/`), target =
`~/.hermes/skills/`.

## Menghasilkan ulang manifest

`skill-manifest.py` tidak punya flag `--update`. Dijalankan tanpa flag ia
menulis manifest ke filesystem sebagai efek samping:

```bash
cd ~/Desktop/Niumination
python3 scripts/skill-manifest.py           # tulis manifest.json
python3 scripts/skill-manifest.py --check   # verifikasi bank vs manifest
```

Flag yang ada hanya `--check`, `--verify-target DIR`, `--structure
{flat,domain}`, `--lockfile DIR`. Cek `--help` daripada menebak nama flag.

## `--structure` wajib cocok dengan target

Bawaan `flat`, sedangkan `~/.hermes/skills` memakai `domain`. Salah flag →
verifikasi melaporkan ratusan file `[hilang-skill]` yang sebenarnya ADA.
Laporan palsu itu bisa mengarahkan ke sinkron ulang yang merusak:

```bash
python3 scripts/skill-manifest.py --verify-target ~/.hermes/skills --structure domain
```

Gejalanya: keluarannya penuh `[hilang-skill]` sementara
`ls ~/.hermes/skills/<kategori>/` jelas berisi berkasnya. Konfirmasi dulu
dengan `find ~/.hermes/skills -name SKILL.md -path '*<nama-skill>*'` sebelum
menganggap file benar-benar hilang.

## Arah tulis: alat patch tidak menulis ke bank

Alat patch skill menulis ke salinan **target** (`~/.hermes/skills/`), bukan
ke bank. Patch sukses di `~/.hermes` tapi `grep` di bank tetap 0 hit adalah
gejala normal, bukan patch gagal. Setelah patch ke skill yang juga ada di bank:

```bash
cp ~/.hermes/skills/<kategori>/<skill>/SKILL.md \
   ~/Desktop/Niumination/skills/<kategori>/<skill>/SKILL.md
cd ~/Desktop/Niumination && python3 scripts/skill-manifest.py
```

Verifikasi kedua sisi identik dengan `diff -q` sebelum commit.

## Pre-commit
`git add` selektif per berkas. `git commit` memicu `.githooks/pre-commit` →
`scripts/secret-scan-staged.py`. Jangan pernah `git add .` di repo root:
mengambil berkas milik proses lain yang kebetulan working.
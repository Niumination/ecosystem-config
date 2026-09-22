# Rencana — Scaffold Repo `Niumination/abstract-studio` (21 Sep 2026)

**Status:** RENJA — menunggu "gas"
**Permintaan pemilik:** wadah baru di ekosistem, repo baru (bukan folder di root), Git LFS,
satu kesatuan ekosistem Niumination, `~/Movies/` hanya untuk hasil akhir.
**Diskusi lanjutan:** niche + nama studio disepakati 21 Sep 2026.

---

## 1. Keputusan terkancing

| Item | Nilai |
|---|---|
| Repo | `Niumination/abstract-studio` |
| Visibilitas | **PRIVAT** (draft sering memuat angka klien & materi sensitif sebelum tayang) |
| Lokasi lokal | `~/Desktop/Niumination/apps/abstract-studio/` |
| Remote | `git@github.com:Niumination/abstract-studio.git` (SSH, konsisten dgn ekosistem) |
| Biner besar | **Git LFS** — `.mp4 .mov .mp3 .wav .ogg .m4a .flac .png .jpg .jpeg .webp .gif .heic` |
| Snapshot bulanan | **GitHub Release** — pola `niumination-restore` (bukan LFS untuk ini) |
| Nama studio | **ZARYU ABSTRACT STUDIO** |
| Handle / watermark | **`@zaryu-abstract-studio`** · domain `abstract.biz.id` |
| Bahasa | disesuaikan per konten (ID murni utk publik; ID+EN utk dev) |
| Source of truth video | `project/<slug>/output/` **di repo** · `~/Movies/` hanya tujuan unggah |
| Pilar konten | **4 (AI Code Doctor) → 2 (Digitalisasi Publik) → 3 (Internal Tools)** |

---

## 2. Struktur repo

```
apps/abstract-studio/
├── AGENTS.md                  # DOX studio — kontrak kerja
├── README.md                  # cara kerja + aturan distribusi
├── BRAND.md                   # brand kit ZARYU ABSTRACT STUDIO
├── MANIFEST.md                # alasan tiap lapis ada (pola niumination-restore)
├── .gitattributes             # aturan LFS
├── .gitignore                 # raw kerja, rahasia, ds-stash
├── .githooks/pre-commit       # gate kredensial (salin pola ekosistem)
├── templates/                 # 19 template + 6 format + rules pack   (148 KB)
├── templates/rules/           # AGENTS.md, CLAUDE.md, .cursorrules, stacks/
├── docs/                      # 07-NICHE + blueprint Mode A           (124 KB)
├── scripts/                   # trend_radar/ledger/ratecard/license_audit (68 KB)
├── data/                      # CALENDAR.csv, HOOKS_PROVEN.csv, dll   (terurai dr workspace/)
├── brand/                     # voice/pronunciation-id.csv, font, warna
└── project/
    ├── reels-001-behind-the-build/
    │   ├── BRIEF.md  NASKAH.md  STATUS.md  SHOTLIST.csv  SOURCES.md  LEDGER.csv
    │   ├── assets/               # draft kerja — LFS
    │   └── output/               # MP4 FINAL — LFS — SOURCE OF TRUTH
    └── reels-002-.../
```

**Pemisahan yang disengaja:** skill (8 SKILL.md) dan bundle (5 YAML) **TIDAK masuk repo ini**.
Mereka milik skill bank (`skills/content/`) — itu FASE 1 yang masih tertunda. Repo ini hanya
wadah + alur manual. Tidak ada config Hermes yang disentuh.

---

## 3. Langkah eksekusi

### Tahap 1 — prasyarat (bukti dulu, tidak bikin apa pun)
```bash
git lfs version                                    # expect: git-lfs/3.8.0
ssh -T git@github.com                              # expect: "Hi Niumination!"
test ! -e ~/Desktop/Niumination/apps/abstract-studio  # expect: tidak ada (exit 1)
```

### Tahap 2 — buat repo privat + remote
```bash
gh repo create Niumination/abstract-studio --private --description \
  "ZARYU ABSTRACT STUDIO — studio konten pilar 4→2→3, Git LFS"
```
*expect:* URL repo; `curl -s -o /dev/null -w '%{http_code}'` tanpa auth = `404` (bukti privat).

### Tahap 3 — scaffold lokal + LFS
```bash
mkdir -p ~/Desktop/Niumination/apps/abstract-studio && cd $_
git init -b main
git config lfs.repositoryformatversion 0
cat > .gitattributes <<'EOF'
* text=auto eol=lf
*.sh *.py text eol=lf
*.enc *.zst *.zip *.key *.db *.sqlite binary
*.mp4 *.mov binary git-lfs
*.mp3 *.wav *.ogg *.m4a *.flac binary git-lfs
*.png *.jpg *.jpeg *.webp *.gif *.heic binary git-lfs
EOF
git lfs track --stdin < /dev/null   # verifikasi: git lfs track menunjukkan 5 pola
```

### Tahap 4 — salin isi zip (teks murni, ±604 KB)
```bash
SRC=/tmp/cs-inspect/hermes-content-studio/hermes-content-studio
cp -R $SRC/templates . ; cp -R $SRC/docs .
cp -R $SRC/scripts .
cp -R $SRC/workspace/data data ; mkdir -p brand/voice project
cp $SRC/workspace/brand/voice/pronunciation-id.csv brand/voice/
```
*Catatan:* `workspace/` zip tidak disalin utuh — isinya diurai ke `data/`, `brand/`, `project/`
agar satu berkas satu rumah. Proyek contoh `audit-60-detik-rls-bocor` **disalin** sebagai rujukan pola.

### Tahap 5 — BRANDING (manual, butuh keputusan)
Tulis `BRAND.md` dari `templates/brand-kit.md` + `docs/07`:
- NAMA STUDIO: `ZARYU ABSTRACT STUDIO` · TAGLINE: "Audit dulu, baru tayang."
- BUKTI diisi data nyata: 91 repo OSS · 52 OPD / 70 halaman portal live · 41 tes lulus
- Handle `@zaryu-abstract-studio` · domain `abstract.biz.id`
- Warna dipertahankan dari paket (`#0B0F17 #7DD3FC #FACC15`) — sudah cocok untuk konten audit
- **Regenerasi `CALENDAR.csv`** (tanggal lama 20 Sep–23 Sep sudah lewat) → mulai tanggal tayang pertama
- `HOOKS_PROVEN.csv` tetap kosong — diisi setelah episode pertama terukur (jangan diisi fiksi)

### Tahap 6 — migrasi 2 proyek yang ada
```bash
mkdir -p project/reels-001-behind-the-build/{assets,output}
# pindahkan naskah dari docs/reports/ (lihat langkah migrasi detail)
```
- `KONTEN-REELS-01-2026-09-18.md` → diurai jadi `BRIEF.md` + `NASKAH.md` + `STATUS.md`
- **Tandai USANG secara struktural** (status `6.ARsip-USANG` di STATUS.md), bukan peringatan di tengah file
- Salin video jadi: `~/Movies/Posting - Instagram/2026-09-18-reels-01-behind-the-build.mp4` → `output/`
- `~/Movies/` dipertahankan sebagai salinan unggah — **tidak dihapus** (dampak terbalik kecil)
- `KONTEN-REELS-02-2026-09-19.md` → proyek 002
- File `docs/reports/KONTEN-REELS-0*.md` diganti **pointer** ke repo (dihapusnya baru di tahap 7)

### Tahap 7 — DOX, README, MANIFEST, pre-commit
- `AGENTS.md`: aturan keras studio (source of truth, LFS, gate kredensial, tidak ada rahasia, UU PDP)
- `README.md`: alur proyek `BRIEF→NASKAH→PRODUKSI→QA→OUTPUT→UNGGAH` + 10 gerbang kualitas
- `MANIFEST.md`: alasan tiap lapis (pola `niumination-restore`)
- `.githooks/pre-commit`: salin dari ekosistem root + aktifkan `core.hooksPath .githooks`

### Tahap 8 — commit + push
```bash
git add -A && git status --short
git commit -m "chore: scaffold studio konten + migrasi reels 001/002"
git push -u origin main
git lfs ls-files   # expect: MP4 muncul di sini, bukan di git biasa
```

### Tahap 9 — registrasi ke ekosistem (WAJIB, supaya jadi "satu kesatuan")
- `docs/registry/project-catalog.md` — baris baru di kategori AI & Coding Agent
- `docs/registry/deployment-status.md` — status ⚪ local-only (bukan deploy)
- `BACKLOG.md` — entri "🔴 Perubahan — 21 Sep 2026 — Repo baru: abstract-studio"
- `docs/AGENTS.md` directory structure — tambah baris `apps/abstract-studio/`

---

## 4. Konfigurasi wajib demi Mac ini

| Aturan | Nilai | Alasan |
|---|---|---|
| LFS quota | pantau `git lfs ls-files --size` bulanan | kuota LFS GitHub = batas push |
| Threshold `transfer.maxObjectSize` | 100 MB | cegah objek besar lolos ke git biasa |
| Raw footage kerja | **di-gitignore** (`assets/raw/`) | hanya hasil cut yang masuk LFS |
| Pruning LFS | `git lfs prune` setelah tiap rilis snapshot | jaga disk 20 GB free |
| Disk | target repo < 3 GB | 20 GB free → sisakan buffer untuk VM Docker rencana |
| Gate pre-commit | wajib aktif per clone | insiden 16 Sep 2026 (PI_API_KEY masuk repo publik) |

---

## 5. Mitigasi & dampak

| Risiko | Mitigasi |
|---|---|
| MP4 lolos ke git biasa → repo membesar permanen | `.gitattributes` dipasang **sebelum** `git add`; verifikasi `git lfs ls-files` di Tahap 8 |
| Repo privat dianggap "aman" → rahasia masuk | gate pre-commit aktif + aturan "repo privat bukan alasan" (pola restore) |
| Disk 20 GB penuh oleh objek LFS | `git lfs prune` + cap repo 3 GB + raw footage di-gitignore |
| `~/Movies/` jadi sumber kedua lagi (masalah semula) | aturan keras di `AGENTS.md` repo + README; `output/` = satu-satunya sumber |
| Draft usang ditandai di dalam file lagi | struktur: status di `STATUS.md` + branch/folder bisa dihapus bersih dari git |
| Registry root divergensi (cron update `project-catalog.md` tiap jam) | update registry **setelah** repo nyata ada (Tahap 9), bukan sebelum |
| `CALENDAR.csv` kedaluwarsa | regenerasi di Tahap 5 — tidak dipakai apa adanya |
| Menghapus file `docs/reports/` sebelum repo terverifikasi | file lama diganti pointer dulu; baru dihapus setelah Tahap 8 lulus |
| Niche berubah bulan depan | pilar ditulis di `BRAND.md`, bukan tersebar di tiap template |

---

## 6. YAGNI — yang TIDAK dikerjakan di rencana ini

- Skill bank (8 skill → `skills/content/`) — FASE 1, tetap tertunda, tetap butuh "gas" terpisah
- Bundle (5 YAML ke `~/.hermes/skill-bundles/`) — butuh skill terpasang dulu
- `channel_skill_bindings` thread 1172 — menyentuh config Hermes, bukan bagian repo
- Unduhan apa pun (Piper voice, faster-whisper, trivy/semgrep) — FASE 2/3, beban Mac berat
- Docker/Postiz — Rencana Install Docker, status RENJA terpisah
- Snapshot GitHub Release pertama — baru setelah repo punya isi (Fase 3 ke depan)

---

## 7. Bukti inspeksi (tanpa eksekusi apa pun)

- `git lfs version` → `git-lfs/3.8.0 (GitHub; darwin amd64; go 1.27.1)`
- `ssh -T git@github.com` → `Hi Niumination! You've successfully authenticated...`
- `gh auth status` → logged in as `Niumination`, Git ops protocol https
- `git config --global user.name/email` → `Niumination` / `niumination@gmail.com`
- `curl api.github.com/users/Niumination/repos?per_page=100 | grep abstract|studio|konten` → 0 hasil
  (nama `abstract-studio` belum terpakai; tidak ada repo konten Kreator)
- `find ~/Desktop/Niumination -name "*abstract*"` → tidak ada folder lokal
- `test ! -e apps/abstract-studio` → tidak ada
- Zip terinspeksi penuh di `/tmp/cs-inspect/`: 604 KB — `templates/` 148 KB (27 file),
  `docs/` 124 KB, `workspace/` 124 KB, `scripts/` 68 KB, `skills/` 76 KB (8 SKILL.md, 5,5–12 KB),
  `skill-bundles/` 20 KB (5 YAML)
- `workspace/data/*.csv`: `CALENDAR.csv` 31 baris (tanggal 20–23 Sep = **kedaluwarsa**),
  `HOOKS_PROVEN.csv` 1 baris (**kosong**), `TREND_LOG.csv` 21 baris, sisanya header saja
- `apps/niumination-restore`: `git lfs track` = kosong, `git lfs ls-files` = kosong,
  `.gitattributes` hanya `binary` biasa, `du -sh .git` = 87 MB tanpa `.git/lfs/`
  → **repo restore TIDAK memakai LFS**; file besarnya di GitHub Release
- Gate ekosistem: `.githooks/pre-commit` (320 byte) → `exec python3 scripts/secret-scan-staged.py`
- `docs/registry/deployment-status.md:21-28` → `abstract.biz.id` = Experimental Sandbox
  (Pi App Studio aggregator, A2A registry, API gateway, lab) — semua 🔴 Planned
- Data untuk BUKTI BRAND.md: Pemdi Aceh Tengah 52 OPD / 70 halaman live (verdict
  `KONTEN-KREATOR-STATUS-2026-09-18.md`); skill bank 143 SKILL.md; 98–108 model 9router
- **Tidak ada yang dieksekusi** — murni inspeksi + dokumen rencana ini

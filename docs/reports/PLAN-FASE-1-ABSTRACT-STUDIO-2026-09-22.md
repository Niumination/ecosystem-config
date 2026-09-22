# Rencana — FASE 1 abstract-studio (skill + bundle + binding) — 22 Sep 2026

**Status:** SELESAI sebagian (21–22 Sep 2026) — Tahap 0, 1, 2 selesai dan terverifikasi.
Tahap 3–6 tertahan oleh satu keputusan desain baru (lihat **P4**).
**Keputusan pemilik (22 Sep 2026):** P1 = opsi B (biarkan `blueprint` utuh, non-aktif) ·
P2 = set `STUDIO_ROOT` ke path baru · P3 = biarkan skill sibling, verifikasi menyusul ·
Eksekusi = "gas jika kondisi memungkinkan".

## Status eksekusi 22 Sep 2026

| Tahap | Item | Status | Bukti |
|---|---|---|---|
| 0 | prasyarat + backup config | ✅ | `~/.hermes/config.yaml.bak-content-skills-20260922-012413` |
| 0 | baseline `--check` | ✅ | `[FAIL] 2` — keduanya milik sibling, tercatat |
| 1 | migrasi 8 SKILL.md | ✅ | 8/8 md5 identik dengan sumber |
| 1 | opsi B terverifikasi | ✅ | 5 baris `schedule:` tetap utuh |
| 2 | 5 bundle | ✅ | `hermes bundles list` → 5, dari "No bundles installed" |
| 3 | binding thread 1172 | ⏸️ menunggu P4 | `config.yaml:748` belum disentuh |
| 4 | env var `STUDIO_ROOT` | ⏸️ menunggu P4 | disetujui, belum di-set |
| 5 | verifikasi | ⏸️ menunggu P4 | — |
| 6 | commit | ⏸️ menunggu P4 | — |

Mesin saat eksekusi: load **2.21 → 4.31**, swap **0 MB terpakai** (total 0 — tidak ada
swap sama sekali), disk 17 Gi free, sibling terakhir menulis 23:30 (tenang 113 menit saat
verifikasi).

## P4. Baru ditemukan — MISMATCH STRUKTUR `workspace/` (menghentikan Tahap 3)

Body dari 8 skill studio merujuk **34 lokasi** dengan prefix `workspace/`, sedangkan
repo `abstract-studio` menggunakan folder langsung di root tanpa lapis `workspace/`:

```
dir yang dirujuk skill        repo aktual        status
workspace/data/  (13 ref)    data/              ada
workspace/audits/ (7 ref)    —                  TIDAK ADA
workspace/BRAND.md  (7 ref)  brand/BRAND.md     ada (jalan beda)
workspace/project/  (4 ref)  project/           ada
workspace/output/ (4 ref)    output/ (per proyek) ada, lokasi beda
workspace/brand/voice/ (1)   brand/voice/       ada (jalan beda)
workspace/archive/ (1 ref)   —                  TIDAK ADA
workspace/templates-local/   templates/         ada (nama beda)
workspace/assets/            —                  TIDAK ADA
```

Dua dari delapan skill tidak punya `blueprint` sama sekali (`content-script`,
`content-produce`) — berarti 5 jadwal yang hidup: `content-research` 07.00,
`content-studio` 13.00, `content-publish` 16.00, `content-legal` Senin 09.00,
`content-monetize` Jumat 20.00.

**Opsi yang tersedia:**
- **A — shim.** Buat folder `workspace/` nyata berisi symlink per entri
  (`workspace/project -> ../project`, `workspace/BRAND.md -> ../brand/BRAND.md`, dst),
  ditambah folder baru `audits/`, `output/`, `archive/`, `assets/`. Skill identik dengan
  upstream, repo bertambah satu lapis navigasi.
- **B — adaptasi path.** Tulis ulang 34 referensi di 8 `SKILL.md` sesuai struktur repo.
  Repo lebih bersih, tapi skill tidak lagi identik dengan paket dan harus diverifikasi
  satu per satu.
- **C — restructure repo.** Pindahkan `project/ data/ brand/` ke dalam `workspace/`.
  Mengubah layout yang sudah di-push (`f7b137f`) dan sudah diregistrasi ke ekosistem.
  Tidak disarankan.

Tolak sendiri: symlink `workspace -> .` pada root akan **sirkular**
(`workspace/data` → `./workspace/data`) dan menjadi dangling di checkout lain, jadi opsi
tersebut sudah saya buang sebelum dipertimbangkan.

Saya tidak melanjutkan Tahap 3–6 karena ini mengubah layout repo yang sudah di-commit
dan sudah terdaftar di ekosistem — bukan keputusan yang layak saya ambil sendiri, dan
bukan bagian dari Tahap 0–6 yang diberi "gas".

## P5. Catatan: `code-audit` memang termasuk bundle
Pada rencana awal saya menulis `code-audit` "tidak termasuk bundle mana pun" — itu **salah**.
`audit-klien.yaml` memuat `code-audit` + `content-monetize` + `content-legal` +
`content-script`, jadi 5 bundle meng-cover seluruh 8 skill. Tidak ada skill yatim.

## P6. Env var yang harus di-set
`STUDIO_ROOT` dan `AUDIT_ROOT` keduanya masih menunjuk contoh `~/content-studio`.
`POSTIZ_URL` di `content-publish` sengaja tidak di-set — Postiz dibuang permanen karena
tanpa Docker.

## Hasil inspeksi 22 Sep 2026 — 3 penemuan yang mengubah FASE 1

### P1. Lima dari delapan skill studio membawa cron otomatis
```
content-studio      blueprint.schedule: "0 13 * * *"   (QA gate jam 13.00)
content-research    blueprint.schedule  (ada)
content-produce     (tanpa)
content-publish     blueprint.schedule  (ada)
content-monetize    blueprint.schedule  (ada)
content-legal       blueprint.schedule  (ada)
content-script      (tanpa)
code-audit          (tanpa)
```
Ini **bertentangan** dengan keputusan terkancing: *"semua unduhan dijadwalkan manual di
jam kerja pemilik, bukan cron."* Kalau frontmatter dibiarkan utuh, ada 5 jadwal yang
siap jalan begitu skill diaktifkan. Perlu keputusan eksplisit.

- **Opsi A (disarankan):** hapus blok `blueprint.schedule` saat migrasi; simpannya di
  komentar Markdown di bawah frontmatter sebagai "jadwal rekomendasi, non-aktif".
- Opsi B: biarkan utuh tapi jangan aktifkan cron apa pun.
- Opsi C: aktifkan sebagian (mis. hanya `content-studio` QA jam 13.00).

### P2. Skill memakai env var `STUDIO_ROOT` — targetnya harus repo baru
`content-studio/SKILL.md` mendeklarasikan `required_environment_variables: STUDIO_ROOT`
dengan contoh `~/content-studio`. Path itu **tidak ada dan tidak akan dibuat** — studio
kita tinggal di `~/Desktop/Niumination/apps/abstract-studio`. Env var ini harus di-set
di `~/.hermes/.env` agar skill menunjuk repo, bukan path fiktif. Ini satu baris, bukan
edit `config.yaml`, tapi tetap perlu persetujuan karena menyentuh file kredensial.

### P3. Manifest skill saat ini TIDAK bersih — dan bukan karena kita
```
[FAIL] 2 ketidaksesuaian manifest vs filesystem:
  [ubah] ecosystem/integration-verification/SKILL.md
  [baru] ecosystem/integration-verification/references/github-token-probe.md — tidak di manifest
```
Subagent lain sedang bekerja di `skills/INDEX.md`, `skills/manifest.json`,
`skills/.promotion-ledger.json`, dan menambah `skills/ecosystem/devops/`. Konsekuensinya:
saya **tidak bisa** memakai `--check` lulus sebagai gerbang keberhasilan, karena baseline-nya
sudah merah. Verifikasi harus memakai cara lain (lihat tahap 5 di bawah), dan hasil saya
harus dilaporkan terpisah dari milik subagent itu.

## Apa yang tersisa dari FASE 1

| Item | Status sekarang |
|---|---|
| `brand/BRAND.md` (tulis ulang manual) | ✅ selesai 21 Sep, 8.4 KB |
| `data/CALENDAR.csv` + catatan | ✅ selesai 21 Sep, 33 slot |
| 8 SKILL.md ke bank pusat | ❌ `skills/content/` belum ada |
| 5 bundle (`content-studio`, `audit-klien`, `client-kit`, `repurpose`, `ugc-produksi`) | ❌ `~/.hermes/skill-bundles/` belum ada |
| 7 gerbang QA | ⚠️ tinggal di dalam `SKILL.md` `content-studio` — tidak perlu instalasi terpisah |
| Binding skill thread 1172 | ❌ masih `["ghost","humanizer"]` (`config.yaml:748`) |

Skema bundle 5 (dari zip):
- `content-studio.yaml` — 7 skill studio (orchestrator + research + script + produce + publish + monetize + legal)
- `code-audit` **tidak** termasuk bundle mana pun — dipasang terpisah atau sebagai bundle keenam
- `audit-klien.yaml`, `client-kit.yaml`, `repurpose.yaml`, `ugc-produksi.yaml`

## Tahapan (urutan, satu gate per tahap)

**Tahap 0 — prasyarat**
- `skills/content/` masih kosong (verify)
- Backup `config.yaml` ke `config.yaml.bak-content-skills-$(date +%Y%m%d-%H%M%S)`
- Rekam baseline `skill-manifest.py --check` supaya kegagalan subagent tercatat bukan jadi dosa saya

**Tahap 1 — migrasi 8 SKILL.md**
- Salin dari `/tmp/cs-inspect/hermes-content-studio/hermes/skills/` ke `skills/content/`
- Hapus `blueprint.schedule` (kalau Opsi A dipilih) — sisakan sebagai catatan Markdown
- Tulis ulang `STUDIO_ROOT` jadi `~/Desktop/Niumination/apps/abstract-studio`
- **Jangan** menyalin `content-produce`/`content-publish` sebelum memutuskan apakah jalur
  Docker tetap mati (Postiz/n8n/Remotion dibuang permanen sesuai rencana lama)

**Tahap 2 — bundle**
- Buat `~/.hermes/skill-bundles/` lalu salin 5 `.yaml`
- Verifikasi dengan `hermes bundles list` (harus menambah dari "No bundles installed")
- Keputusan: apakah `code-audit` ikut bundle `content-studio`, atau bundle terpisah?
  Paketnya memisahkannya — disamakan dengan paket agar perilaku tidak berubah diam-diam.

**Tahap 3 — binding thread 1172**
- Edit satu baris `config.yaml:748`, field `channel_skill_bindings`
- Ganti `"1172":["ghost","humanizer"]` menjadi
  `"1172":["content-studio","ghost","humanizer"]` — `ghost` dan `humanizer`
  **dipertahankan** karena dipakai untuk menulis ulang teks AI menjadi manusia; itu
  justru bagian inti dari pilar 4
- Verifikasi JSON-nya valid dengan `python3 -c` sebelum commit

**Tahap 4 — env var `STUDIO_ROOT`** (butuh persetujuan, menyentuh `~/.hermes/.env`)
- Satu baris `STUDIO_ROOT=/Users/zaryu/Desktop/Niumination/apps/abstract-studio`
- Verifikasi dari shell, tidak di-echo ke chat

**Tahap 5 — verifikasi (karena `--check` tak bisa jadi gerbang)**
- `find skills/content -name SKILL.md | wc -l` → harus 8
- `python3 scripts/skill-manifest.py --check` → bandingkan output vs baseline Tahap 0;
  tambahan baris hanya boleh berasal dari `content/*`
- Uji frontmatter: setiap `SKILL.md` lolos parse YAML
- `grep -c 'schedule:' skills/content/*/SKILL.md` → harus 0 (kalau Opsi A)
- `hermes bundles list` → 5 bundle terdaftar
- Verifikasi `channel_skill_bindings` di `config.yaml` valid JSON
- `git status` — pastikan hanya `skills/content/*`, `skills/manifest.json`, `skills/INDEX.md`
  yang berubah; jangan ikut file milik subagent lain

**Tahap 6 — commit terpisah**
- Commit skill bank (repo induk) dan commit bundle/config **satu commit** sesuai preferensi
  pemilik: kode + dokumentasi gabung, tidak dipecah

## Apa yang TIDAK dikerjakan di rencana ini
- Instalasi apa pun (whisper.cpp, docker, semgrep, osv-scanner, trivy) — FASE 2 dan 3
- Aktivasi cron apa pun
- Perubahan `terminal.cwd` thread 1172
- Konten baru — kalender sudah berisi 33 slot mulai 22 Sep

## Keputusan yang dibutuhkan
1. **P1 — cron blueprint:** A hapus / B biarkan non-aktif / C aktifkan sebagian
2. **P2 — env var STUDIO_ROOT:** set atau biarkan kosong
3. **P3 — verifikasi manifest:** terima bahwa `--check` merah karena subagent lain,
   verifikasi pakai perbandingan vs baseline Tahap 0
4. Tahap 1: ikutkan `content-produce` dan `content-publish` (tersangkut Docker),
   atau tangguhkan dua itu dulu

## Bukti (perintah yang dijalankan 22 Sep 2026, semua read-only)
- `uptime` → load **2.21 2.66 2.74** — mesin aman, cukup rendah untuk eksekusi
- `vm_stat` → Pages free 472.060, occupied by compressor 199.357
- `df -h /` → **17 Gi free / 128 Gi total**
- `ls skills/content` → **TIDAK ADA**; loop 8 nama skill → semua kosong
- `skills/manifest.json` dan `scripts/skill-manifest.py` → keduanya ada
- `ls ~/.hermes/skill-bundles` → **TIDAK ADA**; `hermes bundles list` → "No bundles installed yet."
- `grep -n 1172 ~/.hermes/config.yaml` → baris 748 `channel_skill_bindings: '...,"1172":["ghost","humanizer"]}'`
- `grep -n blueprint /tmp/cs-inspect/.../SKILL.md` → 5 file punya `schedule:`
- `grep -rl STUDIO_ROOT` → 1 file (`content-studio/SKILL.md`)
- `python3 scripts/skill-manifest.py --check` → `[FAIL] 2 ketidaksesuaian` — kedua milik subagent lain (`ecosystem/integration-verification`, `ecosystem/devops/`)
- `git status --short skills/` → `M .promotion-ledger.json`, `M INDEX.md`, `M manifest.json`, `?? ecosystem/devops/`, `?? ecosystem/integration-verification/references/github-token-probe.md`
- `find skills -name SKILL.md` → 162 file di disk
- Bundle zip → 5 file: `audit-klien.yaml`, `client-kit.yaml`, `content-studio.yaml`, `repurpose.yaml`, `ugc-produksi.yaml`
- `content-studio/SKILL.md` → 113 baris, 7.737 byte; `code-audit/SKILL.md` → 178 baris, 12.164 byte
- `ls skills/creative/` → 12 skill; `ghost` dan `humanizer` sudah ada di situ (bukan milik paket ini)
- Tidak ada yang ditulis, diubah, dihapus, atau dieksekusi — murni inspeksi

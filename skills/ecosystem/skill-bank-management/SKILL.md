---
name: skill-bank-management
description: "Kelola Skill Bank Niumination (single source of truth ~/Desktop/Niumination/skills/) — manifest SHA-256, sync seluruh folder ke target Hermes/USB + verifikasi hash + lockfile, tangani drift, adopsi skill pihak ketiga, audit konten skill, hapus/promosi skill, prune bloat. Gunakan saat ada skill baru masuk bank, sync-to-agents.sh dijalankan/gagal, up-eco melaporkan manifest mismatch, drift bank vs target, atau user minta adopsi skill X. Sejak 18 Sep 2026 skill ini menyerap skill-bank-integrity, -maintenance, -operations, -ops, dan -sync (kelimanya dihapus — semua prosedurnya ada di sini)."
tags:
  - ecosystem
  - skills
  - manifest
  - sha256
  - sync
  - integrity
  - niumination
last_updated: "2026-09-18"
version: 2.0.0
changes:
  - v1.0 (2026-09-10): Initial — pola dari adopsi autoskills (midudev) 2026-08-16
  - v1.1 (2026-09-10): Workflow cek lisensi eksplisit (pola autoskills registry)
  - v2.0 (2026-09-18): Konsolidasi 5 skill duplikat (skill-bank-integrity, -maintenance, -operations, -ops, -sync). Prosedur, drift policy, adopsi skill, audit konten, promosi HOME→bank, prune bloat, dan seluruh pitfall disatukan di sini. Referensi mereka dipertahankan: autoskills-patterns.md (gabungan), cases-2026-08.md, skill-bank-manifest-sync.md, home-pruning-f4-2026-08-20.md, scripts/check-rtk.sh
---

# 🧠 Skill Bank Management — Niumination

## Trigger

- Skill baru masuk/berubah di bank, atau user minta "adopsi skill dari autoskills/registry/GitHub"
- `up-eco` Phase 6d melaporkan manifest mismatch; `sync-to-agents.sh` gagal; drift bank vs target
- Perlu menghapus, memindahkan, atau mempromosikan skill antar "plane" (bank ↔ target ↔ HOME)
- **Bila sesi lain mencoba memuat `skill-bank-integrity` / `-maintenance` / `-operations` / `-ops` / `-sync`: kelima skill itu sudah dihapus 18 Sep 2026 dan disatukan ke sini.**

## Angka & peta otoritatif (diverifikasi 2026-09-18)

| Hal | Nilai |
|---|---|
| Bank pusat (single source of truth) | `~/Desktop/Niumination/skills/` — **144 skill**, 712 berkas (setelah konsolidasi) |
| Target Hermes | `~/.hermes/skills/` — isinya **bank + skill bawaan Hermes** |
| Skill bawaan Hermes (bukan milik kita) | **±54** — author `Hermes Agent`, `Nous Research`, `community`, kontributor pihak ketiga (contoh: `apple/*`, `autonomous-ai-agents/codex`, `creative/manim-video`) |
| Sumber angka otoritatif | `skills/manifest.json` (dibuat tool), **bukan** hitungan glob manual |

**Konsekuensi yang wajib dipahami:**

1. Target Hermes adalah **superset**: bank + builtin. Sync dirancang "copy/add only, never delete" supaya skill bawaan Hermes tidak terhapus — ini by design, **bukan drift**.
2. **Jangan hitung jumlah target sebagai "skill kita".** Angka kita = isi manifest.
3. **Jangan edit skill bank di sisi target** (`~/.hermes/skills/...`): sync berikutnya menimpanya dari bank (arah satu arah).
4. **Sync tidak pernah menghapus.** Menghapus skill dari bank TIDAK menghapusnya di target — pembersihan harus dikerjakan di dua tempat (lihat bagian "Menghapus skill").
5. Ada arsip migrasi lama `~/.hermes/skills_archive_2026-08-20` — jangan dihitung sebagai skill aktif.

## Arsitektur

```
skills/ (Bank Pusat — source of truth)
  ├── manifest.json        ← SHA-256 per file + bundleHash per skill
  ├── INDEX.md             ← daftar skill per domain (manual, sinkron dgn fs)
  └── <domain>/<skill>/{SKILL.md, references/, scripts/, assets/}

   │  python3 scripts/skill-manifest.py        (generate/check/verify/lockfile)
   ▼  bash skills/sync-to-agents.sh            (rsync -a -u SELURUH folder, tanpa --delete)
  Hermes  ~/.hermes/skills/<domain>/<skill>/                     (struktur: domain)
  USB     /Volumes/HermesAgent/.../data/skills/<domain>/<skill>/  (struktur: domain — USB diparkir 2026-08-20)
  + skills-lock.json per target (source + bundleHash + syncedAt)
```

**PATH NOTE:** `sync-to-agents.sh` hidup di `skills/` (**bukan** `scripts/`). `skill-manifest.py` dan `up-eco.sh` di `scripts/`. Jangan tertukar.

**Struktur target wajib benar:** Hermes/USB = `--structure domain`. Salah struktur → tool melaporkan **semua skill hilang** (false positive), bukan error yang jelas.

## Workflow inti

```bash
cd ~/Desktop/Niumination

# 1. Setelah mengubah bank — regenerate manifest LEBIH DULU
python3 scripts/skill-manifest.py            # tulis skills/manifest.json
python3 scripts/skill-manifest.py --check    # harapan: "0 mismatch"

# 2. Sync + verifikasi + lockfile
bash skills/sync-to-agents.sh --dry-run      # preview
bash skills/sync-to-agents.sh                # real; output: "N file diverifikasi, 0 masalah" + "verifikasi hash LULUS"

# 3. Verifikasi manual satu target (wajib untuk klaim "tersinkron")
python3 scripts/skill-manifest.py --verify-target ~/.hermes/skills --structure domain

# 4. Lockfile (jalankan SETELAH manifest final — bukan sebelumnya)
python3 scripts/skill-manifest.py --lockfile ~/.hermes/skills
```

**Urutan ini tidak boleh dibalik.** Lockfile yang ditulis sebelum manifest di-regenerate akan tertinggal satu entri (pernah terjadi 18 Sep 2026: lockfile 148 vs manifest 149). Jika itu terjadi, cukup jalankan langkah 4 lagi.

Setelah sync, `docs/registry/skill-registry.md` dan registry di `AGENTS.md` ikut diperbarui otomatis oleh tool. `skills/INDEX.md` **manual** — perbarui baris tabel + counter `> **Status:** N ✅ Aktif`.

## Definisi selesai (DoD)

- [ ] `skill-manifest.py --check` → **0 mismatch**
- [ ] `sync-to-agents.sh` → setiap target `✅ verifikasi hash LULUS`, `0 masalah`
- [ ] `--verify-target ~/.hermes/skills --structure domain` → 0 masalah
- [ ] `skills-lock.json` target = jumlah skill di manifest
- [ ] Untuk skill besar: `diff -r skills/<domain>/<skill> ~/.hermes/skills/<domain>/<skill>` → identik (beda hanya berkas meta: `INDEX.md`, `.gitignore`, `.bundled_manifest`, `skills-lock.json`)
- [ ] `skills/INDEX.md` + registry terbarui; commit menyertakan `skills/manifest.json`

## Drift policy (bank ↔ target)

rsync `-u` **sengaja tidak menimpa** file target yang lebih baru; verifikasi hash yang mendeteksinya (`[ubah]` / `[hilang]`).

1. Bandingkan timestamp bank vs target: `stat -f '%Sm' -t '%Y-%m-%d %H:%M:%S' <file>` (dua sisi)
2. **Target lebih baru/lengkap** (mis. skill diedit langsung di agent) → **backport** target → bank (`cp`)
3. **Bank lebih baru/lengkap** → bank otoritatif → **force** bank → target (`cp` langsung, melewati `-u`)
4. Regenerate manifest → re-sync → verifikasi semua target → commit (sebutkan arah tiap file di pesan commit)

**Jangan pernah resolve drift tanpa konfirmasi user** — audit = rekomendasi, mutasi butuh izin.

## Tindakan yang mengubah bank

### Menambah / mengubah skill
Edit di bank → regenerate manifest → sync → verify → commit (+ `manifest.json`).

### Menghapus skill (WAJIB dua tempat)
Karena sync tidak pernah menghapus:

```bash
# 1. Hapus di bank
rm -rf skills/<domain>/<nama>
# 2. Hapus di setiap target (kalau tidak, ia tetap hidup di sana)
rm -rf ~/.hermes/skills/<domain>/<nama>
# 3. Regenerate + sync + verify + lockfile (lihat Workflow inti)
# 4. Perbarui skills/INDEX.md (hapus barisnya + turunkan counter)
```

Kalau skill yang dihapus punya berkas pendukung (`references/`, `scripts/`) — **pindahkan dulu** isinya yang masih berguna ke skill penerus sebelum `rm`.

### Promosi skill dari HOME → bank (internal)
Berbeda dari adopsi eksternal: sumbernya HOME aktif, bukan registry. Klasifikasikan dulu — jangan promosikan buta:

- **`builtin` Hermes** (`hermes skills list` kolom Source=builtin; ±54 skill) → **JANGAN dipromosikan** (milik framework)
- **Personal/konfigurasi user** (mis. `language-preference`, `nlm-cli-portable`) → **tetap di HOME**
- **Skill operasional reusable** (mis. `ecosystem-*`, `provider-fallback`, `redesign-verification`) → **PROMOSIKAN**

Promosi dilakukan lewat fungsi script, **bukan** `declare -A` (bash 3.2 macOS: key ber-slash seperti `ecosystem/skill-bank-ops` meledak `invalid arithmetic`). Setelah promosi: regenerate manifest → update `INDEX.md` (counter + baris tabel) → sync → verify.

### Prune bloat HOME (teknik F4)
Saat target jauh melebihi bank: **arsipkan (MOVE), jangan hapus** — rollback jadi satu perintah. Resep lengkap + hasil sesi 20 Agu 2026: `references/home-pruning-f4-2026-08-20.md`.

## Adopsi skill pihak ketiga (autoskills registry / repo lain)

1. **Cek lisensi dulu** — `curl -s https://api.github.com/repos/{owner}/{repo}/license`
   - `NO-LICENSE` → **SKIP** (preferensi user: hanya free/open-source; adopsi NO-LICENSE = pelanggaran)
   - MIT / Apache-2.0 aman; CC BY-NC = non-komersial saja (instansi pemerintah boleh)
2. **Cek status review registry** (`index.json` → `review.status`: `approved`/`flagged` + `flags[]`). `flagged` (mis. broad code exec + raw install link) → jangan adopsi tanpa review manusia
3. **Copy SELURUH folder** (`SKILL.md` + `references/` + `scripts/` + `LICENSE`) ke `skills/<domain>/<name>/` — jangan hanya SKILL.md
4. **Sesuaikan frontmatter** ke konvensi bank: `name`, `description`, tambah `source:` (asal/registry) + `license:` eksplisit
5. Update `skills/INDEX.md` (baris tabel + counter)
6. Regenerate manifest → `--check` → sync → verify target → commit (pesan menyebut lisensi + source + sumber asal)
7. Discovery stack (opsional): `cd <proyek> && npx -y autoskills --dry-run`

Prosedur rinci + contoh: `references/adopt-external-skill.md`.

## Audit konten skill (anti prompt-injection)

`python3 scripts/skill-audit.py` — heuristic 7 kategori (instruksi tersembunyi/zero-width, exfil base64/`curl|bash`, URL non-allowlist, pola token/secret, path berbahaya, self-modification, frasa prompt-injection klasik). Terintegrasi `up-eco` Phase 6e.

**Aturan:** hasil audit = **rekomendasi review manual**, warning-only, tidak pernah auto-fix. Baseline 21 Agu 2026: 32 temuan (26 di antaranya URL). Pola studi lengkap + keputusan desain: `references/autoskills-patterns.md`.

## Pitfalls (semua dari sesi nyata)

1. **HOME empty-folder trap.** Script yang resolve HOME di env Hermes harus cek folder **yang berisi** (`.../Desktop/Niumination/skills`), bukan folder induk. Stub KOSONG ada di `/Volumes/HermesAgent/.cache/unix-home/Desktop/Niumination/` → `_get_home()` salah → bank scan 0 → **43 conflict palsu** di skill_monitor MC (diperbaiki di `services/niu-mission-control/modules/skill_monitor.py`, commit `ffb13c4`).
2. **Struktur target salah = false positive massal.** `--verify-target` tanpa `--structure domain` melaporkan semua skill hilang.
3. **Manifest basi = false alarm.** Regenerate manifest lebih dulu setelah edit manual; baru `--check`.
4. **Lockfile ditulis sebelum manifest final** → tertinggal satu entri. Jalankan `--lockfile` terakhir.
5. **Sync tidak menghapus** → skill yang dihapus dari bank tetap hidup di target sampai dibersihkan manual.
6. **Skill hasil sync tidak bisa di-patch langsung di target** — curator menolak (`created_by=None`, mis. `up-eco`). Patch harus di bank, lalu sync.
7. **Escape-drift saat patch bash heredoc** (`sync-to-agents.sh`, `up-eco.sh`): string Python ber-`\n` literal sering berubah jadi `\\n`. Baca berkas aktual dulu, patch kecil-kecil.
8. **Counter lama hilang setelah refactor `sync_target()`** (`hermes_copied`/`total` tidak ada) → jangan dipakai di log/meta-event (error `unbound variable`).
9. **MC server mati diam-diam** (terbunuh saat session compact/restart) → up-eco lapor "MC tidak merespon di 5200". Verifikasi `curl -s localhost:5200/...` sebelum menyalahkan bank.
10. **Bash 3.2 macOS**: tanpa `declare -A`, `mapfile`, `readarray`. Nama skill ber-slash jangan dijadikan key associative array.
11. **File target lebih baru ≠ error.** Itu drift historis yang sah (rsync `-u` by design); bukan alasan force-overwrite otomatis.
12. **Jangan klaim "tersinkron" tanpa `--verify-target` LULUS** — keberadaan berkas bukan bukti.

## Referensi

- `references/autoskills-patterns.md` — studi autoskills, gap analysis, 5 pola yang diadopsi, tabel lisensi skill yang diadopsi (+ yang di-skip)
- `references/adopt-external-skill.md` — prosedur adopsi skill eksternal
- `references/cases-2026-08.md` — kasus nyata: drift USB 6 file, adopsi autoskills, fix `_get_home` MC
- `references/skill-bank-manifest-sync.md` — skema `manifest.json` + `skills-lock.json`, kasus drift
- `references/home-pruning-f4-2026-08-20.md` — teknik prune bloat HOME (arsip, bukan hapus)

## Catatan overlap & riwayat konsolidasi

- **Konsolidasi 18 Sep 2026**: `skill-bank-integrity`, `-maintenance`, `-operations`, `-ops`, `-sync` dihapus (masing-masing 70-109 baris, semuanya mendokumentasikan prosedur yang sama dengan trigger nyaris identik → prosedur jadi bergantung urutan load). Semua konten uniknya diserap ke skill ini; berkas pendukung dipindahkan, bukan dibuang.
- **`up-eco`**: Phase 6/7 menjalankan pemeriksaan integritas & sync otomatis. Skill ini = operasional bank; up-eco = health check. `up-eco` curator-protected (`created_by=None`) → perubahan prosedurnya harus di bank lalu backport manual bila perlu.

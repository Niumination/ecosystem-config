# Sinkronisasi Bank Skill — 17 Sep 2026

**Konteks:** keputusan owner — `~/.hermes/skills` adalah **sumber kebenaran** bank skill; repo ekosistem disinkronkan ke sana (bukan sebaliknya).
**Prasyarat yang menyertainya:** token GitHub baru dipasang owner (`GH_TOKEN` di Hermes + `GITHUB_TOKEN` di vault, identik) dan **terbukti bekerja dari proses non-interaktif** — syarat untuk sync otomatis/cron.

---

## Hasil sync

| Metrik | Sebelum | Sesudah |
|---|---|---|
| Skill di bank pusat (`~/Desktop/Niumination/skills`) | 121 | **148** |
| Skill ditambahkan | — | **27** |
| Skill diperbarui (drift) | — | **3** |
| Verifikasi hash saat menyalin | — | **30/30 cocok, 0 gagal** |
| `skills/manifest.json` | lama | **140 skill, 690 file** · `--check` → 0 mismatch |
| Sync ke Hermes | — | **140 skill** · verifikasi target **"690 file, 0 masalah"** |
| `skills-lock.json` (target Hermes) | 16 Sep 15:32 | **17 Sep 12:30** (140 skill) |
| `docs/registry/skill-registry.md` | 121 entri | **148 entri** diperbarui |

**27 skill baru** (paling penting didahulukan): `ecosystem/device-migration-disaster-recovery` (blueprint DR yang sebelumnya hanya hidup di `~/.hermes`), `credential-vault-backup`, `camofox-browser`, `creative/*` (comfyui, excalidraw, pretext, sketch, touchdesigner-mcp, ascii-art), `devops/*` (4), `mlops/*` (5), `smart-home/openhue`, `development/pi-app-studio`, `ecosystem/{mata-ops, model-status-checker, pi-app-studio-development, pi-network-ecosystem}`, `polling-script-management`, `repo-zip-overlay`, `.archive/cc-acehtengah-maintain`

**3 skill drift diperbarui:** `ecosystem-dox-maintenance`, `ecosystem/hermes-configuration`, `security/git-security-sanitization`

---

## Bug yang ditemukan & diperbaiki: sync mati senyap

`skills/sync-to-agents.sh` keluar **`exit=1` tanpa satu pun pesan error**, tepat setelah baris `→ Hermes: ...`.

**Diagnosa:** `bash -x` menunjukkan rantai kejadian pada skill `camofox-browser` (berada di **root bank**, bukan `<domain>/<skill>`):

```
rel_path=camofox-browser/SKILL.md
domain_dir=camofox-browser
skill_dir=SKILL.md
skill_name=SKILL.md
src_skill_folder=.../skills/camofox-browser/SKILL.md
sync_skill_dir ... → '[' '!' -d .../SKILL.md ']' → return 1
rm -rf .sync-lock        ← proses berakhir di sini
```

`return 1` dari `sync_skill_dir` bertemu `set -e` → **seluruh skrip mati tanpa pesan**. Ini kelas kegagalan yang sama dengan temuan `SOUL.md` dan `grep`-tanpa-hasil: **gagal tanpa suara**.

**Perbaikan (3 potongan kecil di `skills/sync-to-agents.sh`):**
1. `local skipped=0` di `sync_target()`
2. Guard baru: kalau `src_skill_folder` bukan direktori → cetak `⚠️ SKIP (struktur nonstandar): <path>`, tambah counter, `continue` — **jangan** biarkan `return 1` mematikan proses
3. Ringkasan akhir: `⚠️ N skill DILEWATI (struktur nonstandar: root-level atau kedalaman >2)`

**Hasil setelah perbaikan:** `sync_exit=0`, "140 skill disinkronkan", 4 skill dilewati **dengan peringatan terlihat**, verifikasi hash target lulus, lockfile + registry diperbarui.

Perbaikan ini juga mencegah `up-eco` / sync terjadwal mati senyap di masa depan.

---

## Sisa masalah: 8 skill di luar jangkauan tool

| Kelompok | Skill | Perilaku tool |
|---|---|---|
| **Root-level** (bank/<skill>) | `camofox-browser`, `credential-vault-backup`, `polling-script-management`, `repo-zip-overlay` | dilewati dengan peringatan |
| **Kedalaman 3** (bank/<a>/<b>/<skill>) | `mlops/evaluation/evaluating-llms-harness`, `mlops/evaluation/weights-and-biases`, `mlops/inference/llama-cpp`, `mlops/inference/serving-llms-vllm` | **tidak terdeteksi sama sekali** (bahkan tidak muncul sebagai SKIP) |

Bukti inkonsistensi: registry memuat **148** entri (dibangun dengan `os.walk`, semua kedalaman) sementara `manifest.json` & `skills-lock.json` hanya **140** — dan sync hanya menyalin 140.

Kedelapan skill **ada di bank dan ada di Hermes** — yang hilang adalah **verifikasi hash** dan keikutsertaan sync.

**Opsi yang diajukan (menunggu keputusan owner):**
- **A. Normalisasi bank ke 2 level** (`camofox-browser` → `ecosystem/camofox-browser`; `mlops/inference/llama-cpp` → `mlops/llama-cpp`) — cepat, tetapi memicu duplikat di Hermes (salinan lama di root + salinan baru di domain) sehingga perlu pembersihan destruktif
- **B. Perbaiki tool agar mendukung semua kedalaman** (`skills/manifest.py` + `sync-to-agents.sh` mengenali setiap direktori yang memuat `SKILL.md`) — tanpa duplikasi, bank bisa mencerminkan Hermes penuh; perlu pengujian
- **C. Biarkan & catat sebagai pengecualian** — tercepat, tetapi 8 skill tetap tanpa verifikasi hash

**Rekomendasi: B** — struktur skill adalah milik upstream Hermes; bank seharusnya bisa memuatnya apa adanya, dan A menciptakan struktur artifisial yang justru menimbulkan duplikasi.

---

## Bukti

- Salin: `hasil: 30 cocok, 0 gagal` · `verifikasi akhir: bank=148 skill | sisa perbedaan vs sumber = 0`
- Manifest: `[ok] manifest.json ditulis: .../skills/manifest.json — 140 skill, 690 file` · `[ok] manifest sinkron dengan filesystem — 0 mismatch`
- Sync: `⚠️ SKIP (struktur nonstandar): camofox-browser` (+3 lainnya) · `↑ Hermes: 140 skill disinkronkan` · `⚠️ 4 skill DILEWATI` · `[ok] target /Users/zaryu/.hermes/skills — 690 file diverifikasi, 0 masalah` · `[ok] skills-lock.json ditulis ... (140 skill)` · `skill-registry.md updated` · `sync_exit=0`
- Log: `[2026-09-17 12:30:39] Sync selesai: 144 skill × 2 target (Jcode/Hermes) + AGENTS.md ✅`
- Trace bug: `bash -x` berakhir di `+ return 1` lalu `+ rm -rf .../.sync-lock`
- Token (prasyarat sync otomatis): `gh api user -> Niumination` dari **proses background**, scope memuat `repo`, `delete_repo`, `workflow`
- Commit: `a15e3f2` (bank + manifest + registry + bugfix) — sudah di-push

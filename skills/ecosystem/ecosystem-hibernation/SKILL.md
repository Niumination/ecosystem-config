---
name: ecosystem-hibernation
description: "Use when a project must be retired temporarily: archive GitHub, pause Vercel, back up to vault, delete the local folder, and update active references — fully reversible. Reused for cc-acehtengah 21 Sep 2026."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
last_updated: "2026-09-22"
metadata:
  hermes:
    tags: [ecosystem, hibernation, archive, backup, vault, vercel, git, restore, end-of-life, hiatus]
    related_skills: [ecosystem-recovery, ecosystem-dox-maintenance, credential-vault-backup, up-eco]
---

# Ecosystem Hibernation — Retire Sementara yang 100% Reversible

Menghentikan proyek tanpa membunuhnya: GitHub archived+private (history aman), Vercel paused (tidak biaya), folder lokal dihapus (ruang lega), berkas git-ignored dicadangkan ke vault (PII + kredensial tidak hilang). Suatu saat bisa dikembalikan utuh.

**Validated 21 Sep 2026** — cc-acehtengah: 873 MB folder → 76 MB backup, 656 berkas SHA-256, restore test 0 mismatch.

## Trigger

- User: "pindah ke proyek lain", "pause proyek ini", "hapus dari ekosistem", "hemat ruang Mac", "kapan saja bisa dikembalikan"
- Client pindah platform (mis. cc-acehtengah → sapa-ai)
- Vercel deployment sudah di-pause pemilik + repo perlu diarsipkan
- BACKLOG.md proyek ditandai 💤 Hiatus

## Prinsip

1. **Reversible adalah syarat, bukan opsi.** Setiap langkah harus bisa dibalik. Hapus permanen hanya setelah backup terverifikasi.
2. **GitHub = history.** Archived+private menyimpan seluruh commit + branch + tag. Folder `.git` lokal boleh dihapus jika semua branch lokal sudah ada di remote.
3. **Vault = berkas yang TIDAK ada di GitHub.** `.env`, `.env.local`, `data/dtsen-raw/` (PII), `.vercel/project.json`. Inilah yang membuat restore 100%.
4. **Tidak ada yang regeneratif.** `node_modules/`, `.next/`, `dist/` TIDAK dibackup — `npm install` memulihkannya.
5. **SHA-256 sebelum hapus.** Backup tanpa checksum = klaim tanpa bukti. Uji restore di folder sementara SEBELUM hapus permanen.

## Workflow — Ordered (do not reorder)

### Fase 0 — Verifikasi status (read-only, jangan skip)

```bash
cd <repo>
git status --porcelain --untracked-files=all    # HARUS kosong
git log --oneline -1
git branch -a
df -h /                                         # baseline ruang
```

**Completion criteria:** working tree 0 untracked + 0 modified. Jika ada perubahan belum ter-commit: COMMIT atau DISCARD dulu, jangan lanjut.

**CEK CRITICAL — branch lokal yang belum ter-push:**

```bash
git log --oneline origin/<branch>..<branch>     # commit lokal belum ke remote
git log --oneline <branch>..origin/<branch>     # commit remote belum lokal
```

Jika lokal AHEAD: push dulu, atau percayakan branch itu ke backup vault `.git` (lihat Fase 1). Jika behind==ahead (isi sama SHA berbeda = divergen): JANGAN force-push — buang saja, riwayat sama.

**Secret-scan diff lokal vs remote** sebelum archive (kebocoran di riwayat remote tidak bisa dibersihkan tanpa unarchive):

```bash
git log --all --diff-filter=A --name-only --format="%H %s" | grep -iE "env|secret|key" | head
git show <branch>:<file> 2>/dev/null | grep -iE "password|token|sk-|NIK" | head
```

Jika menemukan kredensial plaintext di remote: lanjutkan dengan private+archive (menutup paparan publik), lalu laporkan rotasi yang direkomendasikan. JANGAN tulis nilainya ke transkrip — cukup awalan + 4 karakter akhir.

### Fase 1 — Backup ke vault (sebelum sentuh GitHub apa pun)

```bash
# Buat folder vault dengan tanggal
V="<root>/vault/_hibernasi-<proyek>-<YYYY-MM-DD>"
mkdir -p "$V"

# Stage SEMUA kecuali yang regeneratif
cd <repo>
tar cf - --exclude='node_modules' --exclude='.next' --exclude='dist' . \
  | tar xf - -C "$V/"
```

Isi backup setelah stage: `.git/` (jika ada branch lokal belum ter-push), `.env` + `.env.local`, `data/` (PII), `.vercel/`, source code, `package.json`.node_modules dibuang.

**Permission hardening — JANGAN `chmod -R 600 .` (folder jadi tidak bisa dimasuki):**

```bash
find "$V" -type d -exec chmod 700 {} +
find "$V" -type f -exec chmod 600 {} +
```

**Generate manifest SHA-256:**

```bash
python3 "<root>/skills/ecosystem/ecosystem-hibernation/scripts/generate-manifest.py" "$V"
# → $V/MANIFEST.sha256.json
```

**Completion criteria:** MANIFEST.sha256.json terbuat; `file_count` di manifest == jumlah berkas di folder; folder vault 700/file 600; `git check-ignore vault/` mengembalikan path (vault HARUS ter-ignore, tidak pernah ter-commit).

### Fase 2 — Uji restore SEBELUM hapus (wajib)

```bash
T=/tmp/hibernasi-test
mkdir -p "$T"
cp -rp "$V" "$T/<proyek>"
python3 "<root>/skills/ecosystem/ecosystem-hibernation/scripts/generate-manifest.py" \
  "$T/<proyek>" --verify    # membandingkan vs MANIFEST.sha256.json di dalamnya
rm -rf "$T"
```

**Completion criteria:** `cocok == file_count` dan `hilang == 0` dan `rusak == 0`. Jika tidak cocok: STOP, jangan lanjut ke Fase 4.

### Fase 3 — GitHub archived + private (urutan teknis kaku)

```bash
# 1. TAG dulu — repo archived MENOLAK push
git tag "v-hiatus-<YYYY-MM-DD>"
git push origin "v-hiatus-<YYYY-MM-DD>"

# 2. private: true (tutup paparan publik dulu)
# 3. archived: true (read-only)
gh api -X PATCH /repos/<owner>/<repo> -f private=true
gh api -X PATCH /repos/<owner>/<repo> -f archived=true

# 4. Verifikasi
gh api /repos/<owner>/<repo> --jq '{archived, private, default_branch}'
```

**Urutan ini tidak bisa dibalik.** Tag setelah archive = push ditolak. Private sebelum archive menutup kebocoran riwayat sebelum read-only.

**Token pitfall (Niumination):** berkas env memuat DUA token — `GITHUB_TOKEN` kedaluwarsa (401), `GH_TOKEN` valid (200). Selalu `source <env>; unset GITHUB_TOKEN` dulu, atau semua panggilan API gagal **senyap**.

### Fase 4 — Hapus folder lokal (setelah Fase 2 hijau)

```bash
rm -rf "<root>/<kategori>/<proyek>"
df -h /     # bandingkan baseline Fase 0
```

**Completion criteria:** folder tidak ada (`ls <kategori>/ | grep <proyek>` kosong); ruang lega terlihat di `df`.

### Fase 5 — Perbarui referensi aktif

Cari semua referensi yang masih menganggap proyek aktif:

```bash
search_files pattern="<proyek>" path="<root>" target=content file_glob="*.{sh,py,mjs,ts,js,json,md}"
```

Perbarui (BUKAN hapus — statusnya hiatus, bukan tidak ada):

| Sumber | Contoh perubahan |
|---|---|
| `BACKLOG.md` | 🟢 Active → 💤 **Hiatus** + alasan + tanggal |
| `docs/registry/project-catalog.md` | status + path dicoret `~~path~~` |
| `docs/registry/deployment-status.md` | baris deploy ditandai archived |
| `docs/reports/HIATUS-<PROYEK>-<date>.md` | **Bikin baru** — panduan restore 4 langkah |
| Skrip pemantau (`trio-watch.sh` dll) | **Hapus dari loop**, tambah komentar 1 baris alasan |
| `agents/profile/` (README, PROMPT, generator) | `🔜 Fase 1` → `💤 Hiatus` |
| `apps/niu-dash/data/released.json` | `in_progress` → `hiatus` + activityLog |
| `sites/niu-oss-dashboard/` | regenerate via `gen:mock:fresh` (lihat di bawah) |

**JANGAN hapus:** skill bank entry, dokumen riwayat, repo DR/restore. Itu jejak permanen.

**niu-oss-dashboard punya aturan khusus** — `data/*.json` + `public/api/v1/**` adalah GENERATED, jangan diedit manual:

```bash
cd sites/niu-oss-dashboard
source ~/.hermes/.env; unset GITHUB_TOKEN
GITHUB_TOKEN="$GH_TOKEN" npm run gen:mock:fresh    # snapshot dari API
npm run gen:api                                     # regenerasi API publik
rm public/api/v1/repos/<proyek>.json                # repo private tidak disajikan publik
npm test && npm run typecheck && npm run build
```

**Completion criteria:** `grep -rln "<proyek>"` di kode aktif hanya tersisa di komentar + skill manifest + arsip.

### Fase 6 — Commit + push (kode + dokumen satu commit)

```bash
git add -A
git commit -m "docs(<proyek>): hibernasi permanen — backup vault + hapus folder lokal (<ukuran>, SHA-256 verified)"
git push origin main
```

## Restore — Cara Mengembalikan (4 langkah)

```bash
# 1. Buka kunci GitHub (reversible)
gh api -X PATCH /repos/<owner>/<repo> -f archived=false
gh api -X PATCH /repos/<owner>/<repo> -f private=false    # hanya jika mau publik lagi

# 2. Clone ulang — dapatkan seluruh history + branch + tag dari GitHub
cd <root>/<kategori>
git clone git@github.com:<owner>/<repo>.git <proyek>
cd <proyek>
git checkout <branch-hiatus>     # contoh: hotfix/meeting-ready

# 3. Pulihkan berkas dari vault + verifikasi SHA-256
V="<root>/vault/_hibernasi-<proyek>-<YYYY-MM-DD>"
cp -rp "$V/.env" "$V/.env.local" .          # kredensial produksi
cp -rp "$V/data" .                           # PII warga
cp -rp "$V/.vercel" .                        # binding deployment
python3 - <<EOF                              # verifikasi integritas
import json, hashlib, os
m = json.load(open("$V/MANIFEST.sha256.json"))
bad = [it["path"] for it in m["files"]
       if os.path.exists(it["path"]) and
       hashlib.sha256(open(it["path"],'rb').read()).hexdigest() != it["sha256"]]
print(f"mismatch: {len(bad)}", bad[:5])
EOF
npm install                                   # pulihkan node_modules (798 MB, tidak dibackup)

# 4. Resume deployment + kembalikan status ekosistem
# Vercel: Resume Project (deployment di-pause, bukan dihapus)
# BACKLOG.md: 💤 Hiatus → 🟢 Active
```

**Hasil akhir = kondisi sebelum hibernasi:** source code + history dari GitHub, berkas git-ignored dari vault, dependencies dari `npm install`.

## Bukti yang HARUS dilampirkan ke laporan

```
BACKUP  : <path> · <ukuran> · <N> berkas · SHA-256 per berkas
UJI     : <N>/<N> cocok · 0 mismatch (restore test di /tmp)
FOLDER  : <path> → 0 sisa
GITHUB  : archived: True · private: True · tag v-hiatus-<date>
COMMIT  : <sha> · push <old>..<new>
```

## Pelajaran dari Lapangan (cc-acehtengah, 21 Sep 2026)

- **`chmod -R 600 .` mematikan akses sendiri** — folder butuh 700. Selalu pisahkan `-type d` (700) dari `-type f` (600). Jika sudah terlanjur: jalankan dari luar folder (`find "$V" -type d -exec chmod 700 {} +`), tidak bisa `cd` ke dalamnya.
- **Push bisa ditolak karena cron remote** — repo dengan workflow uptime/GitOps otomatis punya komit di remote. Jangan force-push (aturan emas). `git fetch origin main && git pull --rebase origin main` dulu. Jika rebase konflik pada file GENERATED (README auto-regen), selesaikan dengan `patch` lalu `git rebase --continue` — gunakan `--no-edit`/`--skip` karena editor interaktif akan timeout.
- **Kebocoran di riwayat remote tidak bisa dibersihkan setelah archive** — private+archive menutup paparan publik, tapi nilai kredensialnya masih ada di history. Selalu rekomendasikan rotasi password + API key yang terkait.
- **`data/dtsen-raw/` PII warga tidak boleh dimusnahkan** — cadangkan ke vault, atau jangan hapus.
- **Restore test bukan formalitas** — menjalankan verifikasi di salinan /tmp adalah satu-satunya bukti bahwa backup benar-benar bisa dikembalikan sebelum folder dihapus permanen.

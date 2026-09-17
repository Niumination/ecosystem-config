# Hasil Uji rev 3 — drill lanjutan (3 uji nyata)

**Tanggal:** 17 Sep 2026
**Konteks:** Melanjutkan `DR-PLAN-2026-09-17-rev3.md`. Tiga uji dijalankan untuk memvalidasi bagian rencana yang masih berupa asumsi: (1) aset GitHub Release, (2) substitusi placeholder path, (3) enkripsi + restore `~/.9router`.
**Prinsip:** yang gagal paling berguna. Tiga uji ini menghasilkan **5 bug nyata** — 3 di antaranya ada pada skrip buatan sendiri.

---

## Ringkasan

| Uji | Hasil mekanisme | Temuan |
|---|---|---|
| 1. GitHub Release round-trip | **LULUS** (hash identik) | Repo harus punya commit dulu; `gh` tanpa `--repo` jatuh ke CWD; proses background tanpa keyring → 401 |
| 2. Substitusi placeholder | **LULUS** (v3) | 3 bug pada skrip sendiri: `mapfile` (bash 4+), gagal senyap `exit 0`, `exit 1` palsu dari `grep` |
| 3. Enkripsi + restore `~/.9router` | **LULUS** | `auth` adalah direktori (perbandingan hash berkas salah sasaran) |

---

## UJI 1 — GitHub Release sebagai tempat blob besar

**Mekanisme (diuji di repo privat `dr-testbed-uji-<pid>`, kini dihapus):**
- aset 5 MB dipecah 2 bagian (`split -b 3m`) → unggah ke release → unduh ulang ke direktori bersih → gabung
- **sha256 asli = sha256 gabungan → ROUND-TRIP LULUS** (`40c16265d9b1dfaf6c591aa7…`)
- `--clobber` **mengganti** aset bernama sama (jumlah aset tetap 2), `delete-asset` bekerja
- `gh release view --json assets` memberi nama + ukuran → cukup untuk `verify.sh`

**Uji tuntas di repo yang benar (setelah sesi dibersihkan dari token mati):**
repo privat `Niumination/dr-uji-tuntas-<pid>` → commit awal `d8fdb96` → `gh release create v1` → unggah 2 bagian (3.145.728 B + 2.097.152 B) → `gh release download` ke direktori bersih → gabung → **ROUND-TRIP LULUS** → `--clobber` jumlah aset tetap **2** → release + repo uji dihapus. Verifikasi akhir: repo `dr-*` tersisa **0**, release di `ecosystem-config` **0**. Alur `restore.sh` (buat repo → commit → release → unggah → unduh → verifikasi hash) sudah terbukti bekerja dari ujung ke ujung.

**Batasan yang ditemukan (masuk rencana):**

1. **Repo tanpa commit tidak bisa punya release.** Percobaan pertama gagal: `gh release create` → *"Repository is empty."* → repo `niumination-restore` **wajib punya minimal satu commit** sebelum release pertama; urutannya: init repo → commit skrip/README → baru `gh release create`.
2. **`gh` tanpa `--repo` jatuh ke repo direktori kerja.** Ini terjadi nyata: karena satu variabel gagal ter-set (`set -e` menghentikan run sebelumnya), `gh release create` tanpa `--repo` membuat release di **`Niumination/ecosystem-config` (repo publik)** dengan 2 aset sampah 5 MB.
   - **Sudah dibersihkan & diverifikasi:** release `v0-uji` dihapus (`--cleanup-tag`), `gh api .../releases` → **0**, tag `v0-uji` → `Not Found`. Tidak ada kebocoran data (aset = byte acak dari `/dev/urandom`).
   - **Aturan wajib:** setiap perintah `gh` yang menulis di skrip **harus** memakai `--repo <eksplisit>` **dan** memverifikasi remote (`git -C <dir> remote get-url origin`) sebelum push/upload/delete.
3. **Proses background tidak bisa membaca token dari keyring macOS** → `HTTP 401 Bad credentials`. Sinkronisasi otomatis (cron/launchd) berjalan non-interaktif → **wajib token dari env**, bukan keyring.
4. Di sisi lain, keyring sendiri sehat: `gh api user` → `Niumination`.

---

## UJI 2 — Substitusi placeholder `{{HOME}}` / `{{ECO}}` / `{{HERMES_HOME}}`

**Metode:** 4 berkas nyata (`scripts/kanban-sync.sh`, `scripts/up-eco.sh`, `skills/ecosystem/up-eco/SKILL.md`, `skills/ecosystem/ekosistem-scaffold/SKILL.md`) → 10 path absolut `/Users/zaryu` diubah ke placeholder → substitusi dijalankan dengan **HOME palsu** (`/tmp/fakehome`).

**Tiga bug ditemukan pada skrip sendiri (dan semuanya kelas "verifikasi menyesatkan"):**

| Versi | Bug | Akibat |
|---|---|---|
| v1 | memakai `mapfile` (bash 4+) | macOS `/bin/bash` = **3.2.57** → `mapfile: command not found` |
| v1 | tidak ada gerbang anti-senyap | skrip **keluar `exit 0`** padahal tidak melakukan apa pun |
| v2 | `grep -rl` tanpa hasil = exit 1 + `set -e` | apply **berhasil** tapi skrip keluar **`exit 1` palsu** (tidak mencetak baris verifikasi) |

**Hasil v3 (setelah diperbaiki):**
- `--dry-run` → `exit 0`, lapor 4 berkas / 10 placeholder, **tidak mengubah apa pun**
- `--apply` dengan HOME palsu → `exit 0` + `verifikasi: 0 placeholder tersisa — OK`
- hasil: **0 sisa placeholder**, **0 sisa `/Users/zaryu`**, **4 berkas** memakai `/tmp/fakehome`, `bash -n` → syntax OK
- contoh hasil nyata: `BACKLOG="/tmp/fakehome/Desktop/Niumination/BACKLOG.md"`, `DB="${KANBAN_DB:-${HERMES_HOME:-/tmp/fakehome/.hermes}/kanban.db}"`
- gerbang anti-senyap diuji pada direktori tanpa placeholder → **`exit 1`** (gagal keras, sesuai harapan)

**Pelajaran:** masalah yang kita bahas sepanjang sesi ini (verifikasi palsu, gagal senyap, asumsi bash modern) muncul **tiga kali di dalam skrip saya sendiri dalam satu jam**. Karena itu aturan-aturan ini pindah dari "catatan" menjadi **syarat `verify.sh`**.

---

## UJI 3 — Enkripsi + restore `~/.9router`

**Metode:** `tar` `~/.9router` tanpa `runtime/` (30 MB) dan `logs/` → enkripsi `openssl enc -aes-256-cbc -pbkdf2` → dekripsi ke direktori bersih → ekstraksi → bandingkan hash.

| Objek | Hasil |
|---|---|
| tar.gz | 524.007 B (dari 33 MB karena `runtime/` dikecualikan) |
| terenkripsi | 524.032 B |
| `jwt-secret` | hash **SAMA** |
| `machine-id` | hash **SAMA** |
| `db/data.sqlite` | hash **SAMA**; `PRAGMA integrity_check` → **ok**; 11 tabel |
| `model-catalog.json` | hash **SAMA** |
| `auth` (ternyata **direktori**) | isi identik **1/1** berkas |

**Kesimpulan:** identitas & data 9router dapat dipulihkan utuh lewat jalur enkripsi berbasis berkas — tanpa bergantung pada keystore OS. Catatan: perbandingan pertama saya salah sasaran (`auth` diperlakukan sebagai berkas) → mengingatkan lagi bahwa *metode* pemeriksaan adalah sumber kesalahan tersendiri.

---

## UJI 4 — Paket L2 nyata (data + kredensial) via allowlist

**Metode:** allowlist eksplisit **28 objek → 73 berkas** (kunci signing Android, `.env` 13 proyek, `.vercel/`, DB proyek, `data/dtsen-raw`, `vault/`, kunci SSH) → `tar` → `openssl enc -aes-256-cbc -pbkdf2` → dekripsi → ekstrak ke direktori bersih → **verifikasi hash per berkas** (tanpa menampilkan isi kredensial).

| Tahap | Hasil |
|---|---|
| Objek terkumpul | 28 (2 tidak ada → dilewati dengan catatan) |
| Berkas | **73** · total **71,96 MB** |
| `tar.gz` | **19,01 MB** |
| Terenkripsi | **19,01 MB** |
| Verifikasi hash | **cocok 73/73 · beda 0 · hilang 0** |
| Integritas DB | `swarm_state.db` → **ok** · `prisma/dev.db` → **ok** |
| Izin berkas setelah restore | `id_ed25519_niumination` **0o600** · `vault` **0o700** |

**Konsekuensi untuk rencana (menyederhanakan):**
1. **Paket L2 penuh hanya 19 MB** — jauh di bawah batas 50/100 MB GitHub. Artinya L2 bisa disimpan sebagai **berkas biasa di repo** (terenkripsi), tidak perlu split dan tidak wajib jadi aset Release. Yang tetap butuh Release hanya paket Hermes L1 (116 MB).
2. **`data/dtsen-raw` 70 MB → ~18 MB terkompresi** — CSV/ZIP memampat baik, jadi dataset besar ternyata tidak mahal.
3. **Izin berkas (`0600`/`0700`) ikut terjaga** lewat `tar` — syarat keamanan untuk berkas kredensial di device baru terpenuhi tanpa langkah tambahan.
4. Objek yang tidak ada dilewati **dengan catatan tercetak**, bukan diam — konsisten dengan aturan anti-senyap.

**Catatan ukuran objek kritis:** `ai-organizer-release.jks` 4.434 B · `upload_certificate.pem` 2.016 B — dua berkas ini yang paling mahal nilainya, dan totalnya **6 KB**.

---

## UJI 5 — Restore ke device yang SUDAH punya Hermes (skenario paling realistis)

**Metode:** HOME palsu disimulasikan sebagai "device baru yang baru saja di-install Hermes" — `config.yaml` bawaan (`model-default-bawaan-fresh-install`), `SOUL.md` bawaan 60 B, dan 1 skill lokal dummy. Lalu `hermes import` dijalankan dari backup nyata (202 MB).

### 5A — TANPA `--force`: ABORT, nol berkas dipulihkan

```
Warning: Target directory already has Hermes configuration.
Importing will overwrite existing files with backup contents.
Continue? [y/N]
Aborted.   exit=1
```

Verifikasi sesudahnya: skill tetap **1**, config tetap default, `.env` **HILANG**, `state.db` **HILANG**, `cron/jobs.json` **HILANG**.

**Inilah "Hermes ter-reset ke default" yang nyata:** skrip restore non-interaktif (cron/otomasi) akan **berhenti di prompt** dan meninggalkan device dengan konfigurasi kosong — tanpa error yang mencolok selain `exit=1`.

### 5B — DENGAN `--force`: berhasil

```
Import complete: 2588 files restored in 10.2s     exit=0
```

| Pemeriksaan | Hasil |
|---|---|
| `.env` | ADA |
| `state.db` | ADA 247 MB · `PRAGMA integrity_check` → **ok** · **77 sesi** |
| `cron/jobs.json` | ADA |
| `memories/` | ADA (4 berkas) |
| `kanban.db` | ADA |
| Skill | **203** = 202 dari backup **+ 1 dummy lokal** |
| `SOUL.md` | **60 B, hash `bdb5aeb67833bca3`** = SOUL bawaan device baru (tidak ditimpa) |

### Lima temuan yang mengubah rencana restore

1. **`--force` wajib untuk restore otomatis.** Tanpa itu, import berhenti di prompt konfirmasi. Karena device baru hampir selalu sudah punya `~/.hermes` hasil instalasi, tabrakan ini **pasti** terjadi — bukan kasus pinggiran.
2. **`hermes import` itu *merge*, bukan *mirror*.** Berkas lokal yang tidak ada di backup **tetap tinggal** (skill dummy masih ada). Artinya sisa konfigurasi/skill lama dari instalasi bersih tidak dibersihkan → untuk restore yang benar-benar bersih, urutannya: **cadangkan `~/.hermes` lama → hapus → baru import**, bukan import di atasnya.
3. **`SOUL.md` kembali terbukti tidak ikut** (tidak ada di backup karena symlink → tidak ditimpa) → tetap SOUL bawaan. Ini konfirmasi kedua dari jalur berbeda: perbaikan SOUL.md + verifikasi hash adalah **langkah wajib**, bukan opsional.
4. **Tidak ada cadangan otomatis** saat penimpaan (yang ditemukan `.bak` justru milik device lama yang ikut backup). Jadi skrip restore **wajib** membuat cadangan sendiri sebelum menimpa.
5. **Kode hermes-agent & layanan gateway tetap terpisah** — output import menyebut `hermes update` (kode) dan `hermes gateway install` (layanan) sebagai langkah terpisah. Konfirmasi ketiga bahwa langkah 5 & 11 di rencana memang prasyarat independen.

**Catatan tambahan:** `hermes backup` melaporkan dua berkas yang tidak bisa disalin — `gateway.sock` dan `state/gateway.loop-tick.987.sock` (`Errno 102 Operation not supported on socket`). Wajar (socket tidak punya isi), tidak fatal, tetapi terlihat di output — jadi bukan kegagalan tersembunyi.

---

### Detail: ada DUA token GitHub tersimpan, keduanya mati

| Token | Prefix | Panjang | Tersimpan di | Status |
|---|---|---|---|---|
| `GH_TOKEN` (yang dipakai Hermes & script) | `ghp_YdIJ…` | 40 char | `~/.hermes/.env`, `vault/github-pat.md`, `vault/hermes.env.bak`, `vault/_backup-credentials/hermes.env.bak.20260915` | **401 — tidak valid** |
| `GITHUB_TOKEN` | `ghp_hvjD…` | 40 char | `vault/_backup-credentials/github.env`, `vault/_backup-credentials/github_token.txt` | **401 — tidak valid** |

Keduanya classic PAT (40 char, prefix `ghp_`). Diuji langsung lewat `gh api user` dengan token tersebut → `exit=1`, jawaban error JSON → **dua-duanya sudah dicabut/kedaluwarsa**.

Yang **masih hidup** justru token gh CLI di **keyring** (dipakai hanya oleh sesi terminal interaktif): `gh api user` → `Niumination` berhasil. Itu sebabnya kondisi ini membingungkan — terminal bisa, script tidak.

**Konsekuensi:** token baru perlu dibuat owner, lalu ditempatkan di (a) `~/.hermes/.env` sebagai `GH_TOKEN`, dan (b) `vault/_backup-credentials/github.env` sebagai `GITHUB_TOKEN`. Setelah itu skrip ekosistem (`up-eco.sh`, `model-status-probe-cron.sh`, `model-health-probe-wrapper.sh`) dan sync otomatis DR akan bisa jalan dari proses non-interaktif.

**Penting:** token mati di `~/.hermes/.env` **lebih merusak daripada tidak ada** — ia menimpa keyring yang sehat sehingga semua perintah `gh` gagal selama ia ada di environment.

---

## UJI 6 — Drill restore macOS END-TO-END: SUKSES 100% (skor → 100%)

**Metode:** membangun staging `/tmp/niumination-restore-drill` yang **meniru struktur repo `niumination-restore`** (14 berkas, 211 MB) dari sumber nyata, lalu menjalankan `restore.sh --apply` ke HOME kosong `/tmp/restore-home`. Build repo asli tetap ditahan; ini proof-of-concept terisolasi.

**Isi staging:**
- `l1-hermes/hermes-backup.zip` — `hermes backup` nyata (203 MB) yang sudah dibuang sampah
- `credentials/*.age` — SSH key, 9router (auth/jwt/machine-id/db), vault/secrets.zsh, ssh-config (dienkripsi pass drill)
- `l2-data/ecosystem-ignored.tar.zst.age` — signing keys .jks/.pem + swarm_state.db + placeholder dtsen-raw (non-PII)
- `scripts/subst-paths.sh` + `allowlist-paths.txt`, `restore.sh`, `verify.sh`

**Urutan yang terbukti benar (jangan ditukar):**

1. **clone_repos** (ekosistem dulu jadi root `$ECO`; dotfiles bersarang di `dotfiles/`) — GH_TOKEN via env
2. **restore_hermes** (`hermes import --force` → .env, config, skills, 77 sesi) + **SOUL.md symlink** diperbaiki otomatis
3. **restore_credentials** (dekripsi SSH/9router/vault)
4. **restore_data** (L2 → signing keys, dtsen-raw, swarm)
5. **subst_paths** (placeholder → path device)
6. **verify.sh** — hanya pada `--apply`; kegagalan tetap exit 1

**Hasil verify.sh: `20 lulus, 0 gagal, exit 0`**
- `~/.hermes`, `config.yaml`, `.env`, `auth.json`, `kanban.db`, `cron/jobs.json`, `memories` ✓
- `state.db` integrity `ok`, **77 sesi** ✓
- `SOUL.md` symlink → dotfiles (bukan template bawaan) ✓
- skill filesystem 148 = manifest 148 ✓
- signing `ai-organizer-release.jks` + `upload_certificate.pem` ✓
- `vault/secrets.zsh`, `dtsen-raw`, `~/.ssh/id_ed25519_niumination` ✓
- `~/.9router/db/data.sqlite` integrity `ok` ✓
- 0 placeholder di berkas yang disubstitusi ✓

**Lima bug nyata ditemukan & diperbaiki selama drill ini (bukti bahwa drill menangkap yang tidak terlihat dari rencana):**

1. **Urutan `restore.sh` salah** — awalnya credentials sebelum clone; `$ECO/vault/secrets.zsh` membuat `$ECO` tidak kosong sehingga `gh repo clone` ditolak (`git clone` ke dir non-empty). *Fix: clone paling pertama.*
2. **`subst-paths.sh` salah-gagal** — "0 placeholder = GAGAL" padahal repos klon memang bersih (tidak perlu substitusi). *Fix: 0 placeholder = sukses; verify tetap memastikan target bersih.*
3. **`verify.sh` error bash** — `local` dipakai di body utama (di luar fungsi) → `local: can only be used in a function`. *Fix: hapus `local` di main body.*
4. **`verify.sh` false positive** — memindai seluruh `$ECO` untuk `{{HOME}}`; tapi `DR-PLAN-rev3.md`, `DR-DRILL`, `skill cross-os-restore.md` justru **mendokumentasikan konsep placeholder** sebagai teks contoh → 55 file `{{` termasuk binary spell/terminfo + packfiles. *Fix: scan HANYA berkas yang disubstitusi (allowlist) + kredensial, bukan seluruh tree.*
5. **Exit-code palsu** — `RESTORE_EXIT=0` padahal restore gagal, karena `$?` ditangkap dari `tail` (pipeline). Pada zsh juga `PIPESTATUS` (kapital) tidak terisi — pakai `pipestatus`. *Fix: tangkap exit lewat baris terpisah / `${pipestatus[1]}`.*

**Keputusan desain yang terkonfirmasi:**
- `.env` Hermes **tidak didekripsi dari .age** — ia sudah dipulihkan via `hermes import` (sumber-tunggal), jadi `env-hermes.age` dilewati dengan catatan.
- `GH_TOKEN` untuk restore pertama harus dari **env** (device kosong belum punya `.env`) — kunci pasangan di luar repo, sesuai desain anti-mati-lampu.

**Artefak final tersimpan di ekosistem:** `scripts/dr-restore/{restore.sh, verify.sh, subst-paths.sh, allowlist-paths.txt}` (menunggu dipindah ke repo `niumination-restore` saat build disetujui).

**Skor update: macOS = 100%** (drill SUKSES end-to-end). Windows & Arch tetap 0% sampai diuji di device nyata (menyusul).

---

## TEMUAN BESAR — kredensial mati di `~/.hermes/.env`

Selama uji ini, `gh` mengembalikan **401 Bad credentials** berkali-kali. Penelusuran:

| Fakta | Nilai |
|---|---|
| `GH_TOKEN` di `~/.hermes/.env` | ada, **40 karakter**, prefix `ghp_` |
| Validitasnya | **TIDAK VALID** — `gh api user` dengan token itu mengembalikan error JSON, bukan login |
| Keyring gh CLI | **sehat** — `gh api user` → `Niumination` (tanpa token env) |
| Efek token mati | **menimpa keyring** → semua perintah `gh` gagal 401 selama `GH_TOKEN` ada di environment |
| Script ekosistem yang memakai `.env`/`GH_TOKEN` | `scripts/up-eco.sh`, `scripts/model-status-probe-cron.sh`, `scripts/model-health-probe-wrapper.sh` |

**Konsekuensi:**
1. Celah rev 3 "#11 validitas kredensial" — yang tadinya saya tandai *terbuka* — **terbukti nyata hari ini**, bukan hipotetis.
2. Keberadaan kredensial **bukan** bukti kredensial itu berfungsi. Restore harus **memprobe**, bukan memeriksa keberadaan berkas.
3. Kredensial mati di environment **lebih berbahaya daripada tidak ada** — ia memecahkan jalur yang tadinya bekerja (keyring).
4. Environment sesi ini sudah dibersihkan (`unset GH_TOKEN GITHUB_TOKEN`) dan `gh` kembali normal.

**Rekomendasi (menunggu keputusan owner):** hapus atau ganti `GH_TOKEN` di `~/.hermes/.env`; kalau token tetap disimpan di sana, ia harus diuji validitasnya saat restore dan **tidak** boleh menimpa mekanisme yang lebih sehat (keyring) tanpa verifikasi.

---

## Aturan baru untuk `verify.sh` (hasil uji ini)

1. **Exit code harus jujur.** `grep`/`find` yang tidak menemukan apa pun itu **normal** → bungkus `|| true`; sebaliknya, skrip **wajib `exit 1`** kalau tidak menemukan apa pun yang seharusnya ada.
2. **Kompatibel bash 3.2** (macOS bawaan) — tanpa `mapfile`, tanpa fitur bash 4+.
3. **Target eksplisit** untuk semua perintah tulis (`--repo`, path absolut) + verifikasi remote sebelum operasi.
4. **Hash, bukan keberadaan.** Berkas ada ≠ berkas benar (`SOUL.md` 667 B vs 3.167 B).
5. **Uji di dua lingkungan** — foreground (interaktif, keyring) dan background/non-interaktif (tanpa keyring). Yang bekerja di terminal belum tentu bekerja di cron.
6. **Satu metode pemeriksaan, dicetak apa adanya.** Dua alat berbeda pernah memberi 0 dan 202 untuk hal yang sama.

---

## Bukti (perintah kunci)

- Round-trip Release: `sha256 asli == sha256 gabungan` → LULUS · `--clobber` → jumlah aset tetap 2 · `delete-asset` → berhasil
- Batasan: `gh release create` di repo kosong → `Repository is empty.`
- Insiden salah-repo: release `v0-uji` di `Niumination/ecosystem-config` → **dihapus**, `gh api .../releases` → `0`, tag → `Not Found`
- Background 401: `gh api user` dari proses background + `GH_TOKEN` dari `.env` → `{"status": "401"}`
- Keyring: `gh api user --jq .login` (tanpa token env) → `Niumination`
- `GH_TOKEN` di `.env`: 40 char, prefix `ghp_` — **tidak valid**
- Substitusi v3: `--dry-run exit=0` · `--apply exit=0` + `verifikasi: 0 placeholder tersisa — OK` · sisa `{{` = 0 berkas · sisa `/Users/zaryu` = 0 · 4 berkas pakai `/tmp/fakehome` · `bash -n` OK · gerbang anti-senyap `exit=1`
- 9router: tar 524.007 B → enc 524.032 B → 4 hash SAMA + `auth` 1/1 identik + `integrity_check=ok` + 11 tabel
- Repo uji & artefak: `dr-testbed-uji-*` terhapus (sisa 0); berkas uji `/tmp/uji-*`, `/tmp/drill-*` dibersihkan

---

## Lampiran — `subst-paths.sh` v3 (sudah lolos uji)

```bash
#!/usr/bin/env bash
# subst-paths.sh v3 — ganti placeholder {{HOME}}/{{ECO}}/{{HERMES_HOME}} pada berkas allowlist.
# Diuji: bash 3.2 (macOS), dry-run & apply, exit code jujur, gerbang anti-senyap.
set -Eeuo pipefail

ROOT="."; APPLY=false; ALLOWLIST=""
ECO="${ECO_DIR:-$HOME/Desktop/Niumination}"
HH="${HERMES_HOME:-$HOME/.hermes}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --root) ROOT="$2"; shift 2 ;;
        --apply) APPLY=true; shift ;;
        --allowlist) ALLOWLIST="$2"; shift 2 ;;
        -h|--help) sed -n '2,6p' "$0"; exit 0 ;;
        *) echo "opsi tidak dikenal: $1" >&2; exit 2 ;;
    esac
done

[[ -d "$ROOT" ]] || { echo "GAGAL: root tidak ada: $ROOT" >&2; exit 2; }
LIST="$(mktemp)"; trap 'rm -f "$LIST"' EXIT

if [[ -n "$ALLOWLIST" ]]; then
    [[ -f "$ALLOWLIST" ]] || { echo "GAGAL: allowlist tidak ada: $ALLOWLIST" >&2; exit 2; }
    grep -v '^[[:space:]]*$' "$ALLOWLIST" > "$LIST" || true
else
    ( cd "$ROOT" && find . -type f -not -path "*/.git/*" -not -path "*/node_modules/*" \
        -not -name "*.png" -not -name "*.jpg" -not -name "*.age" -not -name "*.pack" ) \
        | sed 's|^\./||' > "$LIST"
fi

BERKAS=$(wc -l < "$LIST" | tr -d ' ')
[[ "$BERKAS" -eq 0 ]] && { echo "GAGAL: tidak ada berkas ditemukan di $ROOT" >&2; exit 1; }

TOTAL_FILES=0; TOTAL_HITS=0; CHANGED=""
while IFS= read -r rel; do
    f="$ROOT/$rel"; [[ -f "$f" ]] || continue
    n=$(grep -c -e '{{HOME}}' -e '{{ECO}}' -e '{{HERMES_HOME}}' "$f" 2>/dev/null || true)
    [[ -z "$n" ]] && n=0
    if [[ "$n" -gt 0 ]]; then
        TOTAL_FILES=$((TOTAL_FILES + 1)); TOTAL_HITS=$((TOTAL_HITS + n))
        CHANGED="$CHANGED  - $rel ($n)\n"
        if [[ "$APPLY" == true ]]; then
            python3 - "$f" "$HOME" "$ECO" "$HH" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8", errors="surrogateescape")
t = (t.replace("{{HERMES_HOME}}", sys.argv[4])
       .replace("{{ECO}}", sys.argv[3])
       .replace("{{HOME}}", sys.argv[2]))
p.write_text(t, encoding="utf-8", errors="surrogateescape")
PY
        fi
    fi
done < "$LIST"

echo "root          : $ROOT"
echo "mode          : $([[ "$APPLY" == true ]] && echo APPLY || echo 'DRY-RUN')"
echo "berkas dicek  : $BERKAS"
echo "berkas kena   : $TOTAL_FILES"
echo "placeholder   : $TOTAL_HITS"
echo "nilai         : HOME=$HOME"
[[ "$TOTAL_FILES" -gt 0 ]] && printf "daftar berkas:\n$CHANGED"

# Anti-senyap: 0 berkas kena = kecurigaan, bukan sukses diam
if [[ "$TOTAL_FILES" -eq 0 ]]; then
    echo "GAGAL: 0 berkas memuat placeholder — periksa apakah berkas sudah disiapkan" >&2
    exit 1
fi

if [[ "$APPLY" == true ]]; then
    # grep -rl mengembalikan 1 saat tidak menemukan apa pun — itu HASIL YANG DIINGINKAN
    sisa=$( { grep -rl -e '{{HOME}}' -e '{{ECO}}' -e '{{HERMES_HOME}}' "$ROOT" 2>/dev/null || true; } | wc -l | tr -d ' ')
    [[ "$sisa" -gt 0 ]] && { echo "GAGAL: masih ada $sisa berkas dengan placeholder tersisa" >&2; exit 1; }
    echo "verifikasi    : 0 placeholder tersisa — OK"
fi
```

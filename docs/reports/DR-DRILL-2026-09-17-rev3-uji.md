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

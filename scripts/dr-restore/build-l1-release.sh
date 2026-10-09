#!/usr/bin/env bash
# =============================================================================
# build-l1-release.sh — bekukan Hermes home (L1) & unggah sebagai aset Release
# =============================================================================
# SISI BUILD. `hermes backup` menghasilkan ~203 MB; setelah membuang berkas yang
# bisa dibangun ulang (bin/lsp/cache/logs/...) menjadi ~116 MB. Itu di atas batas
# 100 MB/berkas GitHub, jadi dipecah dan diunggah sebagai aset Release.
#
# PELAJARAN WAJIB (pernah terjadi): `gh release create` TANPA `--repo` jatuh ke
# repo dari cwd → release uji nyasar ke repo PUBLIK. Semua perintah gh di sini
# memakai --repo EKSPLISIT.
#
# Pemakaian: bash build-l1-release.sh [--no-upload]
# =============================================================================
set -Eeuo pipefail

REPO="Niumination/niumination-restore"
TAG="l1-$(date +%Y-%m-%d)"
SIZE="45m"          # di bawah batas 100 MB/berkas, menyisakan ruang aman
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
UPLOAD=true
KEEP_DIR=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-upload) UPLOAD=false; shift ;;
    --keep) KEEP_DIR="$2"; shift 2 ;;
    *) echo "opsi tidak dikenal: $1" >&2; exit 2 ;;
  esac
done

# TMP dibersihkan saat keluar — kecuali diminta disimpan (untuk drill/uji lokal)
if [[ -n "$KEEP_DIR" ]]; then
  mkdir -p "$KEEP_DIR"
  trap 'cp -f "$TMP"/hermes-backup.zip.enc.part-* "$TMP"/SHA256SUMS "$KEEP_DIR"/ 2>/dev/null || true; rm -rf "$TMP"' EXIT
else
  trap 'rm -rf "$TMP"' EXIT
fi

# GH_TOKEN hanya perlu untuk MENGUNGGAH — mode --no-upload tidak butuh token.
# Catatan: proses non-interaktif TIDAK bisa membaca Keychain macOS, dan
# lingkungan bisa membawa GH_TOKEN warisan yang sudah basi → SELALU ambil dari
# ~/.hermes/.env (menimpanya), bukan "hanya bila kosong".
if $UPLOAD; then
  if [[ -f "$HOME/.hermes/.env" ]]; then
    set -a; . "$HOME/.hermes/.env"; set +a
    echo "== GH_TOKEN diambil dari ~/.hermes/.env (menimpa nilai warisan)"
  fi
  [[ -n "${GH_TOKEN:-}" ]] || { echo "GAGAL: GH_TOKEN tidak tersedia" >&2; exit 1; }
  if ! _err=$(gh api user 2>&1 >/dev/null); then
    echo "GAGAL: GH_TOKEN tidak valid — pesan gh: $(printf '%s' "$_err" | head -2 | tr '\n' ' ')" >&2
    exit 1
  fi
else
  echo "== mode --no-upload: token tidak diperlukan (artefak disimpan lokal)"
fi

echo "== 1. hermes backup"
# NOTE: jangan andalkan `command -v hermes`. Dua instalasi hermes ada di PATH di
# mesin ini — ~/.local/bin/hermes (shim → runtime python-3.14 yang tidak punya
# yaml/openai) lebih dulu di PATH saat jalan via shell non-interaktif, jadi
# `hermes backup` gagal "No module named 'yaml''. Pakai venv sumber secara
# eksplisit (python3.11, yaml + openai terpasang).
#
# DIPERBAIKI 9 Okt 2026: premis di atas sudah tidak benar. Launcher kanonik
# `.hermes/bin/hermes` (jalur publikasi PM) memakai store Python + closure
# dependency yang di-lease saat runtime — yaml/openai/litellm semua ada di
# sana. Path `.venv/bin/hermes` (venv pra-PM) sudah tidak ada lagi di mesin
# ini, dan memakainya membuat build gagal total. Sekarang resolusinya
# berjenjang + di-smoke-test, supaya "file ada tapi dependency hilang" tidak
# bisa lolos diam-diam lagi.
resolve_hermes_bin() {
  local c
  for c in \
    "$HOME/src/hermes-agent/.hermes/bin/hermes" \
    "$HOME/src/hermes-agent/.venv/bin/hermes" \
    "$HOME/src/hermes-agent/venv/bin/hermes"
  do
    [[ -x "$c" ]] && { printf '%s\n' "$c"; return 0; }
  done
  if c=$(command -v hermes 2>/dev/null); then printf '%s\n' "$c"; return 0; fi
  return 1
}

HERMES_BIN=$(resolve_hermes_bin) || {
  echo "GAGAL: launcher hermes tidak ditemukan (cari: .hermes/bin, .venv/bin, venv/bin, PATH)" >&2
  exit 1
}
# Smoke test: file ada != bisa jalan. `hermes --version` mengimpor hermes_cli,
# jadi kegagalan "No module named 'yaml'" kelas lama tertangkap di sini.
if ! "$HERMES_BIN" --version >/dev/null 2>&1; then
  echo "GAGAL: $HERMES_BIN ada tapi tidak bisa dijalankan (dependency hilang?)" >&2
  exit 1
fi
echo "   launcher: $HERMES_BIN"
"$HERMES_BIN" backup -o "$TMP/hermes-backup.zip" >"$TMP/backup.log" 2>&1 \
  || { echo "GAGAL: hermes backup gagal" >&2; tail -15 "$TMP/backup.log" >&2; exit 1; }
echo "   mentah: $(du -h "$TMP/hermes-backup.zip" | cut -f1)"

echo "== 2. buang berkas yang BISA dibangun ulang (bukan data hilang)"
BEFORE=$(du -k "$TMP/hermes-backup.zip" | cut -f1)
# catatan: pola disengaja menyasar direktori tingkat-atas di dalam zip
zip -q -d "$TMP/hermes-backup.zip" \
  'bin/*' 'lsp/*' 'cache/*' 'logs/*' 'checkpoints/*' 'firefox-profile-backup/*' \
  'models_dev_cache.json' '*/models_dev_cache.json' '.DS_Store' '*/.DS_Store' \
  >/dev/null 2>&1 || true
AFTER=$(du -k "$TMP/hermes-backup.zip" | cut -f1)
echo "   $((BEFORE/1024)) MB → $((AFTER/1024)) MB (dibuang $(( (BEFORE-AFTER)/1024 )) MB regenerable)"

echo "== 3. periksa isi penting masih ada"
# Catatan: JANGAN `unzip -l | grep -q` — grep -q keluar pada kecocokan pertama,
# unzip kena SIGPIPE, dan `pipefail` membuat pipeline dianggap GAGAL padahal
# cocok (menghasilkan laporan "HILANG" palsu). Simpan daftar isi dulu.
ZLIST=$(mktemp)
unzip -l "$TMP/hermes-backup.zip" > "$ZLIST" 2>/dev/null || { echo "GAGAL: tidak bisa membaca zip" >&2; exit 1; }
for must in 'config.yaml' '.env' 'auth.json' 'state.db' 'sessions/' 'skills/' 'memories/'; do
  if grep -qF "$must" "$ZLIST"; then
    echo "   ✓ $must"
  else
    echo "   ✗ $must HILANG — batal unggah" >&2; rm -f "$ZLIST"; exit 1
  fi
done
echo "   jumlah entri: $(grep -cE ' +[0-9]+ +[0-9-]+' "$ZLIST" || true)"
rm -f "$ZLIST"

echo "== 4. ENKRIPSI lalu pecah & checksum"
# Blob L1 WAJIB terenkripsi. Isinya termasuk ~/.hermes/.env (seluruh token).
# Menaruhnya plaintext sebagai aset Release = rahasia tersimpan di GitHub —
# melanggar aturan kredensial ekosistem, dan cukup untuk memicu pencabutan
# token otomatis bila GitHub memindainya.
DR_PASS=$(security find-generic-password -s niumination-restore-dr -w) \
  || { echo "GAGAL: passphrase tidak ada di Keychain" >&2; exit 1; }
export DR_PASS
openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt \
  -in "$TMP/hermes-backup.zip" -out "$TMP/hermes-backup.zip.enc" -pass env:DR_PASS
# bukti: dekripsi balik & bandingkan hash (hash, bukan keberadaan)
_h1=$(shasum -a 256 "$TMP/hermes-backup.zip" | cut -d' ' -f1)
_h2=$(openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in "$TMP/hermes-backup.zip.enc" \
      -pass env:DR_PASS 2>/dev/null | shasum -a 256 | cut -d' ' -f1)
[[ "$_h1" == "$_h2" ]] || { echo "GAGAL: hash roundtrip enkripsi L1 tidak cocok" >&2; exit 1; }
echo "   ✓ terenkripsi $(du -h "$TMP/hermes-backup.zip.enc" | cut -f1), hash roundtrip cocok"
rm -f "$TMP/hermes-backup.zip"          # jangan tinggalkan plaintext

( cd "$TMP" && split -b "$SIZE" -d -a 2 hermes-backup.zip.enc hermes-backup.zip.enc.part- )
( cd "$TMP" && shasum -a 256 hermes-backup.zip.enc > SHA256SUMS )
ls -1 "$TMP" | grep -c 'part-' | sed 's/^/   bagian: /'
echo "   sha256: $(cut -c1-16 < "$TMP/SHA256SUMS")…"

if ! $UPLOAD; then
  echo; echo "(--no-upload) berkas siap di: $TMP"; ls -lh "$TMP" | tail -n +2; exit 0
fi

echo "== 5. unggah ke Release (target EKSPLISIT: $REPO@$TAG)"

# Jaringan ke GitHub di sini fluktuatif (terukur 27 KB/s – 2,3 MB/s) dan
# `gh release upload` TIDAK punya retry sendiri. Unggah per bagian dengan
# backoff supaya satu reset koneksi tidak membuang seluruh pekerjaan.
ULOG="$TMP/upload.log"
NAIK_LIMIT=4

naik() { # $1 = berkas
  local f="$1" coba=1 jeda=8
  while [[ $coba -le $NAIK_LIMIT ]]; do
    if gh release upload "$TAG" --repo "$REPO" --clobber "$f" >>"$ULOG" 2>&1; then
      echo "   ✓ $(basename "$f") ($(du -h "$f" | cut -f1))"
      return 0
    fi
    echo "   ⚠ $(basename "$f") gagal (percobaan $coba/$NAIK_LIMIT): $(tail -1 "$ULOG" | cut -c1-110)"
    coba=$((coba+1))
    if [[ $coba -le $NAIK_LIMIT ]]; then sleep $jeda; jeda=$((jeda*2)); fi
  done
  return 1
}

if gh release view "$TAG" --repo "$REPO" >/dev/null 2>&1; then
  echo "   Release $TAG sudah ada — aset ditimpa (--clobber)"
else
  # rilis dibuat TANPA aset dulu; aset menyusul dengan retry
  gh release create "$TAG" --repo "$REPO" \
    --title "L1 — Hermes home + sesi ($TAG)" \
    --notes "Snapshot Hermes home TERENKRIPSI (AES-256-CBC, pbkdf2 200k).

Isi: config.yaml, .env, auth.json, state.db + seluruh sesi, skills/, cron/, memories/, kanban.db, plugins/.
Dibuang: bin/, lsp/, cache/, logs/, checkpoints/, firefox-profile-backup/ (regenerable).
Dienkripsi karena memuat .env (seluruh token) — rahasia tidak disimpan plaintext di GitHub.

Unduh + gabung + dekripsi: bash scripts/fetch-release.sh --out l1-hermes --tag $TAG" >/dev/null \
    || { echo "GAGAL: tidak bisa membuat Release $TAG"; exit 1; }
  echo "   Release $TAG dibuat (aset menyusul)"
fi

for bagian in "$TMP"/hermes-backup.zip.enc.part-*; do
  naik "$bagian" || { echo "GAGAL: unggah $(basename "$bagian") gagal setelah $NAIK_LIMIT percobaan"; exit 1; }
done
naik "$TMP/SHA256SUMS" || { echo "GAGAL: unggah SHA256SUMS gagal"; exit 1; }

echo "== 6. verifikasi aset benar-benar ada di GitHub"
gh release view "$TAG" --repo "$REPO" --json assets \
  --jq '.assets[] | "   \(.name)  \(.size) B"' | sort

echo
echo "Selesai: $REPO@$TAG"

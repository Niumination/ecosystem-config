#!/usr/bin/env bash
# =============================================================================
# sync-all.sh — bangun ulang SEMUA lapis repo restore dari device ini
# =============================================================================
# Satu perintah untuk menjaga repo Niumination/niumination-restore tetap segar:
#   kredensial → data L2 (gitignored) → template layanan → L1 Hermes → commit → push
#   (+ opsional: drill bukti ke HOME kosong, dan pemangkasan rilis L1 lama)
#
# Repo restore adalah SNAPSHOT. Tidak ada apa pun di sana yang menarik perubahan
# dari device ini dengan sendirinya — snapshot hanya berubah saat skrip ini jalan.
#
# Pemakaian:
#   bash sync-all.sh                 # bangun + commit + push
#   bash sync-all.sh --dry-run       # hanya periksa prasyarat, tidak mengubah apa pun
#   bash sync-all.sh --no-push       # bangun + commit lokal, tidak push
#   bash sync-all.sh --drill         # plus drill ke HOME kosong (bukti, ~5 menit)
#   bash sync-all.sh --keep-releases 2   # simpan N rilis L1 terbaru (default 2)
#
# Aman dijalankan dari cron: hanya menyentuh berkas milik repo restore
# (git add selektif), tidak pernah `git add -A`, dan berhenti pada galat pertama.
# =============================================================================
set -Eeuo pipefail

E="$HOME/Desktop/Niumination"
R="$E/apps/niumination-restore"
REPO_SLUG="Niumination/niumination-restore"
DRY=false; PUSH=true; DRILL=false; KEEP_RELEASES=2

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=true; shift ;;
    --no-push) PUSH=false; shift ;;
    --drill) DRILL=true; shift ;;
    --keep-releases) KEEP_RELEASES="$2"; shift 2 ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "opsi tidak dikenal: $1" >&2; exit 2 ;;
  esac
done

say() { printf '[sync %s] %s\n' "$(date '+%H:%M:%S')" "$*"; }
die() { printf 'GAGAL: %s\n' "$*" >&2; exit 1; }

# ── 0. prasyarat ─────────────────────────────────────────────────────────────
[[ -d "$R/.git" ]] || die "repo restore tidak ada: $R"
command -v gh >/dev/null || die "gh tidak ada di PATH"
[[ -f "$E/scripts/dr-restore/build-credentials.sh" ]] || die "skrip build tidak ada"

# GH_TOKEN: proses non-interaktif tidak bisa membaca Keychain → ambil dari .env
if [[ -f "$HOME/.hermes/.env" ]]; then set -a; . "$HOME/.hermes/.env"; set +a; fi
[[ -n "${GH_TOKEN:-}" ]] || die "GH_TOKEN tidak ada (butuh untuk push + rilis)"
gh api user >/dev/null 2>&1 || die "GH_TOKEN tidak valid"

# passphrase: Keychain dulu (macOS); di OS lain wajib lewat env PASS
if [[ -z "${PASS:-}" ]]; then
  if command -v security >/dev/null 2>&1; then
    PASS=$(security find-generic-password -s niumination-restore-dr -w 2>/dev/null) \
      || die "passphrase tidak ada di Keychain (dan PASS tidak diset)"
  else
    die "PASS belum diset — di OS ini tidak ada Keychain untuk mengambilnya"
  fi
fi
export PASS DR_PASS="$PASS"
say "prasyarat OK (token & passphrase tersedia, tidak dicetak)"

if $DRY; then
  say "DRY-RUN: berhenti di sini — tidak ada yang diubah."
  say "yang AKAN dijalankan: build-credentials → build-l2 → build-services → build-l1-release → commit → push"
  exit 0
fi

# ── 1..4. bangun tiap lapis ──────────────────────────────────────────────────
say "1/6 kredensial (~/.ssh, ~/.9router, vault) → credentials/*.enc"
bash "$E/scripts/dr-restore/build-credentials.sh" >/tmp/sync-cred.log 2>&1 \
  || { tail -5 /tmp/sync-cred.log; die "build kredensial gagal"; }
tail -1 /tmp/sync-cred.log | sed 's/^/         /'

say "2/6 data ekosistem (gitignored) → l2-data + allowlist"
bash "$E/scripts/dr-restore/build-l2.sh" >/tmp/sync-l2.log 2>&1 \
  || { tail -5 /tmp/sync-l2.log; die "build L2 gagal"; }
grep -E 'kandidat:|tar:|allowlist:|old-home' /tmp/sync-l2.log | sed 's/^/         /'

say "3/6 template layanan launchd"
bash "$E/scripts/dr-restore/build-services.sh" >/tmp/sync-svc.log 2>&1 \
  || { tail -5 /tmp/sync-svc.log; die "build layanan gagal"; }
grep -E 'dibekukan' /tmp/sync-svc.log | sed 's/^/         /'

say "4/6 Hermes home (L1) → aset Release terenkripsi  [paling lama]"
bash "$E/scripts/dr-restore/build-l1-release.sh" >/tmp/sync-l1.log 2>&1 \
  || { tail -8 /tmp/sync-l1.log; die "build L1 gagal"; }
grep -E 'terenkripsi|bagian:|Selesai' /tmp/sync-l1.log | sed 's/^/         /'

# ── 5. commit (selektif, hanya berkas milik repo ini) ────────────────────────
say "5/6 commit di repo restore"
cd "$R"
git add credentials l2-data hermes scripts README.md MANIFEST.md RESTORE-PATHS.md \
        AGENTS.md docs restore.sh verify.sh .gitattributes .gitignore 2>/dev/null || true
if git diff --cached --quiet; then
  say "         tidak ada perubahan berkas — snapshot sudah mutakhir"
else
  n=$(git diff --cached --name-only | wc -l | tr -d ' ')
  git -c user.name="Niumination" -c user.email="niumination@users.noreply.github.com" \
      commit -q -m "chore(snapshot): refresh $(date '+%Y-%m-%d %H:%M')

Dibangun ulang oleh scripts/dr-restore/sync-all.sh pada device utama:
kredensial (.enc), data L2 (gitignored), template layanan, L1 Hermes (aset Release).
Semua lapis ciphertext; tidak ada rahasia plaintext."
  say "         commit dibuat: $(git rev-parse --short HEAD) ($n berkas)"
fi

if $PUSH; then
  git push -q origin HEAD:main && say "         pushed → $(git rev-parse --short HEAD)"
else
  say "         --no-push: commit lokal saja"
fi

# ── 6. pangkas rilis L1 lama (aset besar menumpuk tiap rebuild) ──────────────
if $PUSH; then
  say "6/6 pangkas rilis L1 (simpan $KEEP_RELEASES terbaru)"
  # Tanpa `mapfile` — macOS bawaan bash 3.2 tidak punya (array + loop portabel)
  TAGS=()
  while IFS= read -r t; do
    [[ -n "$t" ]] && TAGS+=("$t")
  done < <(gh release list --repo "$REPO_SLUG" --limit 50 --json tagName,createdAt \
    --jq 'sort_by(.createdAt) | reverse | .[].tagName' 2>/dev/null | grep '^l1-' || true)
  if [[ ${#TAGS[@]} -gt $KEEP_RELEASES ]]; then
    for t in "${TAGS[@]:$KEEP_RELEASES}"; do
      gh release delete "$t" --repo "$REPO_SLUG" --yes --cleanup-tag >/dev/null 2>&1 \
        && say "         dihapus: $t" || say "         ⚠ gagal hapus: $t"
    done
  else
    say "         hanya ${#TAGS[@]} rilis L1 — belum perlu dipangkas"
  fi
fi

# ── opsional: drill bukti ────────────────────────────────────────────────────
if $DRILL; then
  say "DRILL: restore ke HOME kosong dari GitHub (bukti, bukan asumsi)"
  bash "$E/scripts/dr-restore/drill.sh" >/tmp/sync-drill.log 2>&1 \
    || { tail -20 /tmp/sync-drill.log; die "DRILL GAGAL — snapshot TIDAK boleh dianggap sah"; }
  grep -E 'Hasil:|SEMUA LULUS' /tmp/sync-drill.log | sed 's/^/         /'
fi

# ── ringkasan ────────────────────────────────────────────────────────────────
say "selesai. ukuran hasil:"
du -sh "$R/credentials" "$R/l2-data" 2>/dev/null | sed 's/^/         /'
say "HEAD=$(git -C "$R" rev-parse --short HEAD) origin=$(git -C "$R" rev-parse --short origin/main 2>/dev/null || echo '?')"
say "berikutnya: uji di device target (lihat README → Status per platform)"

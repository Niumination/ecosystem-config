#!/usr/bin/env bash
# =============================================================================
# up-eco-lightfix.sh — perbaikan RINGAN otomatis ekosistem Niumination
# =============================================================================
# Dijalankan oleh cron Hermes (job "up-eco-lightfix", dibuat & dijaga oleh
# scripts/up-eco.sh) atau manual. Semua langkah idempoten.
#
# ── KEBIJAKAN "FIX RINGAN" (disetujui pemilik, 19 Sep 2026) ──────────────────
# HANYA artefak TERDERIVASI yang boleh ditulis ulang otomatis — yaitu berkas
# yang isinya bisa direkonstruksi 100% dari sumber kebenaran, sehingga tidak ada
# penilaian manusia yang dibutuhkan dan tidak ada informasi yang bisa hilang:
#
#   1. skills/manifest.json            ← scripts/skill-manifest.py (hash bank)
#   2. skills/INDEX.md                 ← scripts/gen-skill-index.py (dari bank)
#   3. docs/registry/skill-registry.md ← skills/sync-to-agents.sh
#   4. salinan target ~/.hermes/skills ← skills/sync-to-agents.sh (satu arah)
#   5. verifikasi hash target          ← scripts/skill-manifest.py --verify-target
#
# TIDAK PERNAH dilakukan otomatis (butuh keputusan manusia):
#   - git commit / push            → tersedia opt-in: --commit (tanpa push)
#   - menghapus / memindahkan berkas apa pun di luar INDEX (baris Index adalah turunan)
#   - mengubah isi skill, SOUL.md, AGENTS.md, config, kredensial, env
#   - memperbaiki repo yang kotor  → butuh keputusan per repo (dilaporkan up-eco)
#   - menyentuh produksi (Vercel/Supabase) atau mesin (launchd)
#
# Usage: bash scripts/up-eco-lightfix.sh [--commit] [--quiet]
# Exit : 0 sukses (termasuk "tidak ada perubahan") · non-nol bila verifikasi gagal
# =============================================================================
set -euo pipefail

NIUMINATION="/Users/zaryu/Desktop/Niumination"
SKILLS="$NIUMINATION/skills"
LOGDIR="$NIUMINATION/logs"
LOG="$LOGDIR/up-eco-lightfix.log"
LOCKDIR="$LOGDIR/.up-eco-lightfix.lock"
MAX_LOG_KB=200          # rotasi log: simpan berkas ≤200 KB (satu generasi .1)

COMMIT=0
QUIET=0
for a in "$@"; do
  case "$a" in
    --commit) COMMIT=1 ;;
    --quiet)  QUIET=1 ;;
    *) echo "argumen tidak dikenal: $a" >&2; exit 2 ;;
  esac
done

mkdir -p "$LOGDIR"
ts() { date '+%Y-%m-%d %H:%M:%S'; }
say() { [ "$QUIET" = "1" ] || printf '%s\n' "$*"; echo "[$(ts)] $*" >> "$LOG"; }

# ── lock: cegah dua eksekusi bersamaan (stale > 2 jam diabaikan) ──
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  if [ -n "$(find "$LOCKDIR" -maxdepth 0 -mmin +120 2>/dev/null)" ]; then
    say "⚠️  lock basi (>2 jam) — diambil alih"; rmdir "$LOCKDIR" 2>/dev/null || true; mkdir "$LOCKDIR" 2>/dev/null || true
  else
    say "⏭️  dilewati: eksekusi lain masih berjalan ($LOCKDIR)"; exit 0
  fi
fi
trap 'rmdir "$LOCKDIR" 2>/dev/null || true' EXIT

# ── rotasi log ──
if [ -f "$LOG" ] && [ "$(wc -c < "$LOG" | tr -d ' ')" -gt $((MAX_LOG_KB * 1024)) ]; then
  mv -f "$LOG" "$LOG.1"; say "↻ log dirotasi → $LOG.1"
fi

say "── lightfix mulai (cron/up-eco) ──"
rc=0
before_index=$( [ -f "$SKILLS/INDEX.md" ] && shasum -a 256 "$SKILLS/INDEX.md" | cut -c1-16 || echo "-" )

# 0) PENJAGA "never clobber" - read-only, WAJIB paling awal.
#    Mendeteksi file target yang disunting lokal supaya tidak ditimpa sync (kasus 19 Sep 2026).
if [ -f "$NIUMINATION/scripts/sync-guard.py" ]; then
  if g_out=$(python3 "$NIUMINATION/scripts/sync-guard.py" --status 2>&1); then
    nkonf=$(printf '%s' "$g_out" | sed -n '1s/.*konflik: \([0-9]*\).*/\1/p')
    if [ "${nkonf:-0}" -gt 0 ]; then
      say "⚠ penjaga: ${nkonf} skill KONFLIK - tidak akan ditimpa sync (perlu tinjauan):"
      printf '%s\n' "$g_out" | grep -E '^  KONFLIK|^      -' | head -12 | sed 's/^/   /'
    else
      say "✓ penjaga: $(printf '%s' "$g_out" | head -1 | sed 's/^ *//')"
    fi
    printf '%s\n' "$g_out" | grep 'catatan:' | sed 's/^/   /' || true
  else
    say "⚠ penjaga: gagal dijalankan - sync TIDAK akan melewati apa pun (risiko timpa)"; rc=1
  fi
else
  say "⚠ penjaga sync-guard.py tidak ada - sync tanpa perlindungan (risiko timpa)"; rc=1
fi

# 1) PROMOSI skill lokal BARU dari target ke bank (D1: hanya yang baru; D3: tanpa commit).
#    Dijalankan SEBELUM manifest/INDEX/sync supaya hasil promosi ikut tercatat & tersalin.
if [ -f "$NIUMINATION/scripts/promote-skills.py" ]; then
  if out=$(python3 "$NIUMINATION/scripts/promote-skills.py" 2>&1); then
    head1=$(printf '%s' "$out" | head -1 | sed 's/^ *//')
    say "✓ promosi: $head1"
    printf '%s\n' "$out" | grep -E '^  [+!] ' | head -20 | sed 's/^/   /' || true
  else
    say "✗ promosi GAGAL: $(printf '%s' "$out" | tail -2)"; rc=1
  fi
else
  say "⚠ scripts/promote-skills.py tidak ada - promosi otomatis dilewati"
fi

# 2) manifest bank
if out=$(python3 "$NIUMINATION/scripts/skill-manifest.py" 2>&1); then
  say "✓ manifest: $(printf '%s' "$out" | tail -1)"
else
  say "✗ manifest GAGAL: $(printf '%s' "$out" | tail -2)"; rc=1
fi

# 3) INDEX (turunan bank; akar drift sebelum ini karena tidak ada generatornya)
if out=$(python3 "$NIUMINATION/scripts/gen-skill-index.py" 2>&1); then
  say "✓ INDEX: $(printf '%s' "$out" | head -1 | sed 's/^ *//')"
  printf '%s\n' "$out" | grep -E '^\s+[+-]' | while IFS= read -r l; do say "   $l"; done || true
else
  say "✗ INDEX GAGAL: $(printf '%s' "$out" | tail -2)"; rc=1
fi

# 4) sinkronisasi satu arah ke target (registry + lockfile + state penjaga di dalamnya).
#    Exit 3 = DILEWATI (lock aktif) - WAJIB dibedakan dari sukses. Sebelumnya skip ini
#    terlihat sebagai "✓ sync:" kosong dengan rc=0, jadi cron bisa diam-diam berhenti sync.
set +e
out=$(bash "$SKILLS/sync-to-agents.sh" 2>&1); sync_rc=$?
set -e
if [ "$sync_rc" -eq 0 ]; then
  say "✓ sync: $(printf '%s' "$out" | grep -E 'Sync selesai|verifikasi hash|DIKARANTINA' | tail -2 | tr '\n' ' ')"
elif [ "$sync_rc" -eq 3 ]; then
  say "⚠ sync DILEWATI (bukan sukses): $(printf '%s' "$out" | tail -1)"
  rc=1
else
  say "✗ sync GAGAL (rc=$sync_rc): $(printf '%s' "$out" | tail -2)"; rc=1
fi
printf '%s\n' "$out" | grep -E '⛔|⚠️  Lock' | head -8 | sed 's/^/   /' || true

# 5) verifikasi (hash, bukan keberadaan)
if out=$(python3 "$NIUMINATION/scripts/skill-manifest.py" --check 2>&1); then
  say "✓ verifikasi bank: $(printf '%s' "$out" | tail -1)"
else
  say "✗ verifikasi bank GAGAL: $(printf '%s' "$out" | tail -2)"; rc=1
fi
if out=$(python3 "$NIUMINATION/scripts/skill-manifest.py" --verify-target "$HOME/.hermes/skills" --structure domain 2>&1); then
  say "✓ verifikasi target: $(printf '%s' "$out" | tail -1)"
else
  say "✗ verifikasi target GAGAL: $(printf '%s' "$out" | tail -2)"; rc=1
fi

# 6) commit — HANYA artefak turunan, tanpa push
#    a) selalu: churn timestamp pada manifest/registry di-commit otomatis, TAPI hanya bila
#       perubahannya terbukti timestamp-saja (dibandingkan dengan versi HEAD setelah
#       normalisasi). Perubahan konten nyata ditolak dan dibiarkan untuk peninjauan manusia.
#       Tanpa ini setiap run cron meninggalkan 2 berkas "kotor" hanya karena stempel waktu.
#    b) --commit: artefak turunan penuh (termasuk INDEX.md) ikut di-commit.
if [ "$rc" = "0" ]; then
  cd "$NIUMINATION"
  if [ -x scripts/lightfix-autocommit.sh ]; then
    say "─ autocommit (timestamp-saja):"
    bash scripts/lightfix-autocommit.sh "$NIUMINATION" 2>&1 | sed 's/^/  /' | tee -a "$LOG"
  else
    say "⚠ scripts/lightfix-autocommit.sh tidak ada — churn timestamp dibiarkan"
  fi
fi
if [ "$COMMIT" = "1" ] && [ "$rc" = "0" ]; then
  cd "$NIUMINATION"
  git add skills/manifest.json skills/INDEX.md docs/registry/skill-registry.md 2>/dev/null || true
  if [ -n "$(git diff --cached --name-only 2>/dev/null)" ]; then
    git commit -q -m "chore(skill-bank): lightfix otomatis — manifest + INDEX + registry tersinkron" || true
    say "✓ commit lokal dibuat (tanpa push): $(git log -1 --pretty=%h)"
  else
    say "✓ tidak ada perubahan artefak untuk di-commit"
  fi
fi

after_index=$( [ -f "$SKILLS/INDEX.md" ] && shasum -a 256 "$SKILLS/INDEX.md" | cut -c1-16 || echo "-" )
say "$([ "$before_index" = "$after_index" ] && echo '▪ tanpa perubahan INDEX' || echo '▪ INDEX berubah: '"$before_index"' → '"$after_index")"
say "── lightfix selesai rc=$rc ──"

# stdout ringkas (dipakai cron --no-agent bila diinginkan; tanpa timestamp agar stabil)
[ "$rc" = "0" ] || echo "up-eco lightfix: GAGAL (rc=$rc) — lihat $LOG"
exit "$rc"

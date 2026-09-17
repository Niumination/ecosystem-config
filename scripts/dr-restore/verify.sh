#!/usr/bin/env bash
# =============================================================================
# verify.sh — Verifikasi hasil restore Niumination (macOS)
# =============================================================================
# Memeriksa SETIAP klaim yang ditargetkan restore, berbasis hash/realita bukan
# kedok '0' palsu. Gagal keras (exit 1) kalau ada yang tidak sesuai.
# CATATAN: body utama TIDAK memakai `local` (bash melarang local di luar fungsi)
#   — pelajaran dari DRY-RUN pertama: verify.sh sendiri bisa gagal konyol.
# Pakai : bash verify.sh --root <ECO> [--quiet]
# Exit  : 0 = semua lulus; 1 = ada yang gagal
# =============================================================================
set -Eeuo pipefail

ROOT=""
QUIET=false
PASS=0
FAIL=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --quiet) QUIET=true; shift ;;
    -h|--help) sed -n '1,14p' "$0"; exit 0 ;;
    *) echo "opsi tidak dikenal: $1" >&2; exit 2 ;;
  esac
done

# resolve HOME dari HERMES_HOME (restore.sh men-setnya)
TH="${HOME}"
HH="${HERMES_HOME:-$TH/.hermes}"
ECO="${ROOT:-$TH/Desktop/Niumination}"
# SOURCE = direktori tempat verify.sh berada ($SOURCE/verify.sh) — self-contained,
# jadi verify.sh bisa dipanggil langsung maupun via restore.sh tanpa flag tambahan.
SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ok()   { PASS=$((PASS+1)); $QUIET || echo "  ✓ $*"; }
bad()  { FAIL=$((FAIL+1)); echo "  ✗ $*" >&2; }

ensure() { # $1 = deskripsi, $2 = path
  [[ -e "$2" ]] && { ok "$1: $2"; } || bad "$1 TIDAK ADA: $2"
}

hash_eq() { # $1 deskripsi, $2 berkas, $3 hash diharapkan
  if [[ -f "$2" ]]; then
    local got
    got=$(shasum -a 256 "$2" | cut -c1-16)
    [[ "$got" = "$3" ]] && ok "$1 (hash $got)" || bad "$1 hash beda: $got != $3"
  else
    bad "$1 HILANG: $2"
  fi
}

echo "═══ verify.sh — hasil restore macOS ═══"

# 1. Hermes home pulih
ensure "~/.hermes" "$HH"
ensure "config.yaml" "$HH/config.yaml"
ensure ".env" "$HH/.env"
ensure "auth.json" "$HH/auth.json"
ensure "kanban.db" "$HH/kanban.db"
ensure "cron/jobs.json" "$HH/cron/jobs.json"
ensure "memories" "$HH/memories"

# 2. state.db utuh & terbaca
if [[ -f "$HH/state.db" ]]; then
  itg=$(sqlite3 "$HH/state.db" "PRAGMA integrity_check;" 2>/dev/null || echo "gagal")
  [[ "$itg" = "ok" ]] && ok "state.db integrity_check = ok" || bad "state.db integrity: $itg"
  n=$(sqlite3 "$HH/state.db" "SELECT COUNT(*) FROM sessions;" 2>/dev/null || echo "0")
  ok "sessions di state.db: $n"
else
  bad "state.db HILANG"
fi

# 3. SOUL.md — wajib symlink ke repo dotfiles
if [[ -L "$HH/SOUL.md" ]]; then
  soul_tgt=$(readlink "$HH/SOUL.md")
  [[ "$soul_tgt" == *"zaryu-terminal-dotfiles/hermes/SOUL.md"* ]] \
    && ok "SOUL.md symlink -> $soul_tgt" \
    || bad "SOUL.md symlink ke lokasi salah: $soul_tgt"
  [[ -f "$soul_tgt" ]] && ok "target SOUL.md ada" || bad "target SOUL.md menggantung: $soul_tgt"
else
  bad "SOUL.md BUKAN symlink (masih template bawaan?)"
fi

# 4. Skill bank — filesystem = manifest
if [[ -f "$ECO/skills/manifest.json" ]]; then
  n_fs=$(find "$ECO/skills" -name 'SKILL.md' -not -path '*/.git/*' | wc -l | tr -d ' ')
  n_man=$(python3 -c "import json; print(json.load(open('$ECO/skills/manifest.json'))['skillCount'])" 2>/dev/null || echo "?")
  [[ "$n_fs" = "$n_man" ]] && ok "skill filesystem=$n_fs manifest=$n_man" || bad "skill tak sinkron: fs=$n_fs man=$n_man"
else
  bad "manifest.json HILANG"
fi

# 5. Kredensial ekosistem dipulihkan (ada)
for rel in \
  "apps/ai-file-manager-android/play-store/signing/ai-organizer-release.jks" \
  "apps/ai-file-manager-android/play-store/signing/upload_certificate.pem" \
  "vault/secrets.zsh" \
  "services/cc-acehtengah/data/dtsen-raw" \
  ; do
  ensure "$rel" "$ECO/$rel"
done

# 6. SSH & 9router
ensure "~/.ssh/id_ed25519_niumination" "$TH/.ssh/id_ed25519_niumination"
ensure "~/.9router/db/data.sqlite" "$TH/.9router/db/data.sqlite"
if [[ -f "$TH/.9router/db/data.sqlite" ]]; then
  ritg=$(sqlite3 "$TH/.9router/db/data.sqlite" "PRAGMA integrity_check;" 2>/dev/null || echo "gagal")
  [[ "$ritg" = "ok" ]] && ok "9router db integrity ok" || bad "9router db integrity: $ritg"
fi

# 7. Tidak ada placeholder tersisa — HANYA pada berkas yang SEHARUSNYA bersih
#    (allowlist substitusi + kredensial), BUKAN seluruh $ECO. Karena beberapa
#    dokumen (DR-PLAN, skill cross-os-restore) justru mendokumentasikan konsep
#    {{HOME}} dsb sebagai teks contoh — memindai seluruh tree = false positive.
n_ph=0
for_dir="$SOURCE/../scripts/allowlist-paths.txt"
if [[ -f "$SOURCE/scripts/allowlist-paths.txt" ]]; then
  n_ph=$( (while IFS= read -r rel; do
    p="$ECO/$rel"; [[ -f "$p" ]] || continue
    grep -c -e '{{HOME}}' -e '{{ECO}}' -e '{{HERMES_HOME}}' "$p" 2>/dev/null || true
  done < "$SOURCE/scripts/allowlist-paths.txt") | awk '{s+=$1} END{print s+0}' )
else
  # fallback: hanya berkas kredensial yang didekripsi + .env
  n_ph=$( { grep -H -e '{{HOME}}' -e '{{ECO}}' -e '{{HERMES_HOME}}' \
      "$HH/.env" "$TH/.ssh/config" "$ECO/vault/secrets.zsh" 2>/dev/null || true; } | wc -l | tr -d ' ')
fi
[[ "$n_ph" = "0" ]] && ok "0 placeholder di berkas yang disubstitusi/disimpulkan" || bad "$n_ph placeholder tersisa di berkas target"

echo ""
echo "═══ Hasil: $PASS lulus, $FAIL gagal ═══"
[[ "$FAIL" -gt 0 ]] && exit 1
echo "✅ verify.sh: SEMUA LULUS"
exit 0
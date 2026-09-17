#!/usr/bin/env bash
# =============================================================================
# restore.sh — Restore penuh ekosistem Niumination ke device macOS baru
# =============================================================================
# Purpose : Menghidupkan kembali Hermes + dotfiles + ekosistem dari ketiadaan
#           dengan urutan yang TIDAK BISA SALAH. Berbasis UJI 1-5 (rev 3).
#
# URUTAN (jangan ditukar — setiap langkah prasyarat langkah berikutnya):
#   1. clone repo ekosistem + dotfiles   (butuh GH_TOKEN env; jadikan $ECO root)
#   2. hermes import                     (kembalikan ~/.hermes incl .env & skills)
#   3. credentials                       (SSH, 9router, vault/secrets.zsh)
#   4. data L2                           (signing keys, dtsen-raw, DB proyek)
#   5. substitusi path                   ({{HOME}}/{{ECO}}/{{HERMES_HOME}})
#   6. verify.sh                         (bukti, bukan klaim)
#
# Pakai   : bash restore.sh --source /path/ke/niumination-restore \
#                       [--target-home /Users/USER] [--apply]
#           GH_TOKEN WAJIB via env saat restore pertama (pasangan kunci di luar
#           repo — chicken-and-egg yang disengaja: repo tidak bisa membuka diri).
# Safety  : DRY-RUN default. Gagal keras (exit 1), tidak ada langkah diam.
# =============================================================================
set -Eeuo pipefail

# ── Mode & lokasi ─────────────────────────────────────────────────────────────
SOURCE=""
TARGET_HOME="$HOME"
APPLY=false
ONLY_VERIFY=false

usage() { sed -n '1,12p' "$0"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) SOURCE="$2"; shift 2 ;;
    --target-home) TARGET_HOME="$2"; shift 2 ;;
    --apply) APPLY=true; shift ;;
    --only-verify) ONLY_VERIFY=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "opsi tidak dikenal: $1" >&2; exit 2 ;;
  esac
done

[[ -n "$SOURCE" ]] && [[ -d "$SOURCE" ]] || { echo "GAGAL: --source wajib dan harus ada" >&2; exit 2; }
[[ -d "$TARGET_HOME" ]] || { echo "GAGAL: --target-home tidak ada: $TARGET_HOME" >&2; exit 2; }

TH="$TARGET_HOME"
ECO="$TH/Desktop/Niumination"
HH="$TH/.hermes"

log() { echo "[restore $(date '+%H:%M:%S')] $*"; }
step() { echo ""; echo "════ $* ════"; }
die() { echo "❌ $*" >&2; exit 1; }

# ── Token GitHub ──────────────────────────────────────────────────────────────
# Operasi non-interaktif butuh token env (keyring macOS tidak bisa diakses
# proses background/cron — UJI 1). Nilai pertama: $GH_TOKEN, lalu ~/.hermes/.env
# jika sudah ada (post-import), lalu PASS-opsi. Pada restore PERTAMA di device
# kosong, GH_TOKEN harus diberikan via env oleh pemakai (kunci dari luar repo).
need() { command -v "$1" >/dev/null 2>&1 || die "prasyarat tidak ada: $1"; }
need git; need gh; need tar; need openssl; need sqlite3; need python3; need zstd

if [[ -z "${GH_TOKEN:-}" ]] && [[ -f "$HH/.env" ]]; then
  GH_TOKEN="$(grep -o '^GH_TOKEN=.*' "$HH/.env" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' || true)"
fi
if [[ -z "${GH_TOKEN:-}" ]]; then
  echo "GAGAL: GH_TOKEN tidak ada di environment. Ini RESTORE PERTAMA (belum ada .env), jadi sediakan secara eksplisit:" >&2
  echo "       GH_TOKEN='...' bash restore.sh --source ... --apply" >&2
  exit 1
fi
export GH_TOKEN GITHUB_TOKEN="$GH_TOKEN"

# ── 1. Clone repo ekosistem + dotfiles (harus PALING DAHULU) ──────────────────
clone_repos() {
  step "1. Clone repo ekosistem + dotfiles (root $ECO)"
  if $APPLY; then
    # ekosistem dulu jadikan root $ECO; dotfiles di-ignore parent -> repo bertumpuk.
    if [[ ! -d "$ECO/.git" ]]; then
      if gh repo clone Niumination/ecosystem-config "$ECO" -- --depth 1 >/dev/null 2>&1; then
        log "   ✓ ekosistem diklon"
      else
        die "gagal klon ekosistem (GH_TOKEN valid? lihat error di atas tanpa /dev/null)"
      fi
    else
      log "   ekosistem sudah ada"
    fi
    mkdir -p "$ECO/dotfiles"
    if [[ ! -d "$ECO/dotfiles/zaryu-terminal-dotfiles/.git" ]]; then
      if gh repo clone Niumination/zaryu-terminal-dotfiles "$ECO/dotfiles/zaryu-terminal-dotfiles" -- --depth 1 >/dev/null 2>&1; then
        log "   ✓ dotfiles diklon"
      else
        log "   ⚠️  gagal klon dotfiles (lewati)"
      fi
    else
      log "   dotfiles sudah ada"
    fi
  else
    log "   [DRY-RUN] akan klon ekosistem + dotfiles ke $ECO"
  fi
}

# ── 2. Hermes home (import) ───────────────────────────────────────────────────
restore_hermes() {
  step "2. Hermes ~/.hermes (hermes import dari backup L1)"
  local zip="$SOURCE/l1-hermes/hermes-backup.zip"
  [[ -f "$zip" ]] || die "tidak ada $zip"
  if $APPLY; then
    if [[ -d "$HH" ]] && [[ -n "$(ls -A "$HH" 2>/dev/null)" ]]; then
      local bak="$HH.pre-restore-$(date '+%Y%m%d-%H%M%S')"
      log "   cadangkan target -> $bak"
      mv "$HH" "$bak"
    fi
    log "   hermes import (--force)"
    HERMES_HOME="$HH" hermes import "$zip" --force 2>&1 | tail -4 || die "hermes import gagal"
    # SOUL.md tidak ikut backup (symlink) — pulihkan dari repo dotfiles (UJI 5).
    local soul_src="$ECO/dotfiles/zaryu-terminal-dotfiles/hermes/SOUL.md"
    if [[ -f "$soul_src" ]]; then
      ln -sf "$soul_src" "$HH/SOUL.md"
      log "   ✓ SOUL.md symlink -> $soul_src"
    else
      die "SOUL.md sumber tidak ada: $soul_src (dotfiles belum diklon?)"
    fi
  else
    log "   [DRY-RUN] akan: cadangkan target, hermes import --force, perbaiki SOUL.md"
  fi
}

# ── 3. Kredensial (dekripsi .age) ─────────────────────────────────────────────
restore_credentials() {
  step "3. Kredensial (SSH, 9router, vault) — dekripsi dari .age"
  local enc_dir="$SOURCE/credentials"
  [[ -d "$enc_dir" ]] || { log "   ⚠️  tidak ada $enc_dir — kredensial tidak dipulihkan"; return 0; }
  local n=0
  for f in "$enc_dir"/*.age; do
    [[ -e "$f" ]] || continue
    local base target
    base=$(basename "$f" .age)
    case "$base" in
      ssh-id_ed25519_niumination) target="$TH/.ssh/id_ed25519_niumination" ;;
      ssh-config) target="$TH/.ssh/config" ;;
      9router-auth) target="$TH/.9router/auth" ;;
      9router-jwt-secret) target="$TH/.9router/jwt-secret" ;;
      9router-machine-id) target="$TH/.9router/machine-id" ;;
      9router-db) target="$TH/.9router/db/data.sqlite" ;;
      vault-secrets-zsh) target="$ECO/vault/secrets.zsh" ;;
      env-hermes|hermes-.env) log "   ℹ️  $base dilewati — .env sudah dipulihkan via hermes import"; continue ;;
      *) log "   ⚠️  lewati tak dikenal: $base"; continue ;;
    esac
    if $APPLY; then
      mkdir -p "$(dirname "$target")"
      openssl enc -d -aes-256-cbc -pbkdf2 -in "$f" -out "$target" -pass "env:PASS" 2>/dev/null \
        || die "dekripsi gagal: $base (PASS salah?)"
      chmod 600 "$target"
      log "   ✓ $base -> $target"
    else
      log "   [DRY-RUN] dekripsi $base -> $target"
    fi
    n=$((n+1))
  done
  log "   ($n berkas diproses)"
}

# ── 4. Data L2 (tar.zst.age) ──────────────────────────────────────────────────
restore_data() {
  step "4. Data ekosistem (L2) ke path gitignored"
  local blob="$SOURCE/l2-data/ecosystem-ignored.tar.zst.age"
  [[ -f "$blob" ]] || { log "   ⚠️  tidak ada $blob — data tidak dipulihkan"; return 0; }
  if $APPLY; then
    openssl enc -d -aes-256-cbc -pbkdf2 -in "$blob" -out /tmp/eco.tar.zst -pass "env:PASS" 2>/dev/null \
      || die "dekripsi L2 gagal"
    zstd -d -f /tmp/eco.tar.zst -o /tmp/eco.tar 2>/dev/null || true
    tar -xf /tmp/eco.tar -C "$ECO" 2>/dev/null || die "ekstrak L2 gagal"
    rm -f /tmp/eco.tar.zst /tmp/eco.tar
    log "   ✓ L2 diekstrak ke $ECO"
  else
    log "   [DRY-RUN] akan: dekripsi + ekstrak L2 ke $ECO"
  fi
}

# ── 5. Substitusi placeholder ─────────────────────────────────────────────────
subst_paths() {
  step "5. Substitusi placeholder path ({{HOME}}/{{ECO}}/{{HERMES_HOME}})"
  local subst="$SOURCE/scripts/subst-paths.sh"
  [[ -x "$subst" ]] || { log "   ⚠️  subst-paths.sh tidak ada — lewati"; return 0; }
  local allow="$SOURCE/scripts/allowlist-paths.txt"
  if $APPLY; then
    HOME="$TH" ECO_DIR="$ECO" HERMES_HOME="$HH" \
      bash "$subst" --root "$ECO" --allowlist "$allow" --apply 2>&1 | tail -2 || die "substitusi gagal"
  else
    log "   [DRY-RUN] akan jalankan subst-paths.sh --apply"
  fi
}

# ── 6. Verifikasi ─────────────────────────────────────────────────────────────
verify_all() {
  step "6. Verifikasi hasil (verify.sh)"
  local v="$SOURCE/verify.sh"
  [[ -x "$v" ]] || { log "   ⚠️  verify.sh tidak ada — verifikasi dilewati"; return 0; }
  HOME="$TH" HERMES_HOME="$HH" bash "$v" --root "$ECO" 2>&1 | tail -12
  local done=${pipestatus[1]:-${PIPESTATUS[1]}}
  [[ "$done" = "0" ]] || die "verify.sh menemukan masalah (exit $done)"
}

# ── Jalankan ──────────────────────────────────────────────────────────────────
log "mode: $([[ $APPLY == true ]] && echo APPLY || echo 'DRY-RUN (tidak ada perubahan)')"
log "target home: $TH"

if [[ $ONLY_VERIFY == true ]]; then
  verify_all
  exit 0
fi

clone_repos
restore_hermes
restore_credentials
restore_data
subst_paths

# verify hanya pada eksekusi nyata; kegagalannya TETAP exit 1 (bukan ditelan).
if $APPLY; then
  verify_all
fi

step "SELESAI"
if $APPLY; then
  log "✅ Restore macOS selesai. Lanjutkan layanan (launchd/systemd) secara terpisah."
else
  log "🏁 DRY-RUN selesai — tidak ada yang diubah. Ulangi dengan --apply."
fi
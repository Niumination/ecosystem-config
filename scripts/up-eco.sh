#!/usr/bin/env bash
# =============================================================================
# up-eco.sh — Ecosystem Status & Sync Checker v1.0
# =============================================================================
# Usage: ./scripts/up-eco.sh
#
# Memeriksa kondisi ekosistem Niumination dan merekomendasikan:
#   - Folder asing / tidak terdaftar di dokumentasi
#   - Git repos yang dirty / perlu commit
#   - Kesenjangan dengan GitHub remote
#   - Update dokumentasi (BACKLOG, AGENTS, README)
#   - Sinkronisasi dengan status GH Pages
# =============================================================================

set -euo pipefail

NIUMINATION="/Users/zaryu/Desktop/Niumination"
PROFILE="$NIUMINATION/agents/profile"
NOW=$(date "+%Y-%m-%d %H:%M:%S WIB")
DIVERGE_FILE=$(mktemp)
REPORT_FILE=$(mktemp)

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

cleanup() { rm -f "$DIVERGE_FILE" "$REPORT_FILE"; }
trap cleanup EXIT

# ── helpers ────────────────────────────────────────────────────────────────
header()  { printf "\n${CYAN}══════════════════════════════════════════════════════════════${NC}\n"; }
section() { printf "\n${BOLD}${CYAN}◆ %s${NC}\n" "$1"; }
pass()    { printf "  ${GREEN}✅ %s${NC}\n" "$1"; }
warn()    { printf "  ${YELLOW}⚠️  %s${NC}\n" "$1"; }
fail()    { printf "  ${RED}❌ %s${NC}\n" "$1"; }
info()    { printf "  ${CYAN}ℹ️  %s${NC}\n" "$1"; }
rec()     { printf "  ${BOLD}➜ ${NC}%s\n" "$1"; echo "$1" >> "$REPORT_FILE"; }

# ── Root git status ────────────────────────────────────────────────────────
check_git_status() {
  local dir="$1" label="$2"
  if [ ! -d "$dir/.git" ]; then
    warn "$label: bukan git repo"
    return
  fi

  local branch head dirty ahead behind remote
  branch=$(cd "$dir" && git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "?")
  head=$(cd "$dir" && git rev-parse --short HEAD 2>/dev/null || echo "?")
  dirty=$(cd "$dir" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  ahead=$(cd "$dir" && git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0")
  behind=$(cd "$dir" && git rev-list --count HEAD..@{upstream} 2>/dev/null || echo "0")
  remote=$(cd "$dir" && git remote get-url origin 2>/dev/null || echo "none")

  info "Branch: $branch | HEAD: $head"
  info "Remote: $remote"

  if [ "$dirty" -gt 0 ]; then
    fail "$dirty file(s) uncommitted di $label"
    rec "→ $label: git add + commit $dirty file(s) dirty"
  else
    pass "$label: clean"
  fi

  if [ "$ahead" -gt 0 ] && [ "$ahead" != "0" ]; then
    warn "$ahead commit(s) ahead of remote — perlu push"
    rec "→ $label: git push ($ahead ahead)"
  fi
  if [ "$behind" -gt 0 ] && [ "$behind" != "0" ]; then
    warn "$behind commit(s) behind remote — perlu pull"
    rec "→ $label: git pull ($behind behind)"
  fi
}

# ── Cek folder asing ───────────────────────────────────────────────────────
check_unknown_folders() {
  section "📂 Folder Asing (tidak terdaftar)"

  local known_dirs=(
    apps services sites desktop agents labs sandbox
    docs scripts skills tools vault brain dotfiles archive
  )

  # Baca dari BACKLOG.md untuk daftar proyek yang dikenal
  local known_projects=""
  if [ -f "$NIUMINATION/BACKLOG.md" ]; then
    known_projects=$(grep -oE 'Niumination/[a-zA-Z0-9_-]+' "$NIUMINATION/BACKLOG.md" 2>/dev/null | sed 's|Niumination/||' | sort -u || true)
  fi

  local found_unknown=false

  # Cek root level
  for item in "$NIUMINATION"/*/; do
    local name
    name=$(basename "$item")
    [[ "$name" == .* ]] && continue
    [[ "$name" == "projects" ]] && continue
    [[ "$name" == "Production" ]] && continue
    [[ "$name" == "PI" ]] && continue

    # Skip if it's a known category folder
    local is_known=false
    for kd in "${known_dirs[@]}"; do
      [[ "$name" == "$kd" ]] && { is_known=true; break; }
    done
    $is_known && continue

    # Skip if it's a tracked config/meta file
    [[ "$name" == "AGENTS.md" ]] || [[ "$name" == "BACKLOG.md" ]] || [[ "$name" == "README.md" ]] || [[ "$name" == ".gitignore" ]] || [[ "$name" == ".gitleaks.toml" ]] && continue

    found_unknown=true
    warn "Folder tidak dikenal: $name/"
    rec "→ Periksa $name/ — apakah perlu didaftarkan di BACKLOG.md?"
  done

  # Cek di setiap kategori untuk proyek tak terdaftar
  local categories=(apps services sites desktop agents labs sandbox)
  for cat in "${categories[@]}"; do
    [ ! -d "$NIUMINATION/$cat" ] && continue
    for item in "$NIUMINATION/$cat"/*/; do
      [ ! -d "$item" ] && continue
      local proj
      proj=$(basename "$item")
      [[ "$proj" == .* ]] && continue

      # Cek apakah proyek ini terdaftar di BACKLOG.md atau known_projects
      if ! echo "$known_projects" | grep -qi "$proj" 2>/dev/null; then
        if ! grep -qi "$proj" "$NIUMINATION/BACKLOG.md" 2>/dev/null; then
          found_unknown=true
          warn "$cat/$proj/ — terdaftar di filesystem tapi TIDAK di BACKLOG.md"
          rec "→ $cat/$proj: daftarkan di BACKLOG.md + update AGENTS.md"
        fi
      fi
    done
  done

  # Cek archive too
  if [ -d "$NIUMINATION/archive/projects" ]; then
    for item in "$NIUMINATION/archive/projects"/*/; do
      [ ! -d "$item" ] && continue
      local proj
      proj=$(basename "$item")
      [[ "$proj" == .* ]] && continue
      if ! grep -qi "$proj" "$NIUMINATION/BACKLOG.md" 2>/dev/null; then
        found_unknown=true
        warn "archive/projects/$proj/ — ada di disk tapi TIDAK di BACKLOG.md"
        rec "→ archive/projects/$proj: catat di BACKLOG.md"
      fi
    done
  fi

  $found_unknown || pass "Semua folder dikenal dan terdaftar"
}

# ── Cek sinkronisasi BACKLOG ↔ filesystem ──────────────────────────────────
check_backlog_sync() {
  section "📋 Sinkronisasi BACKLOG.md ↔ Filesystem"

  if [ ! -f "$NIUMINATION/BACKLOG.md" ]; then
    fail "BACKLOG.md tidak ditemukan!"
    return
  fi

  local issues=0

  # Cek setiap proyek di BACKLOG apakah foldernya ada
  while IFS= read -r line; do
    local proj
    proj=$(echo "$line" | grep -oE '\*\*[^*]+\*\*' | head -1 | tr -d '*')
    [ -z "$proj" ] && continue

    # Skip known non-directory entries
    case "$proj" in
      "TEDEO"|"Niu-Flow"|"ecosystem-config"|"Niumination"|"brain"|Total|Ekosistem|Dirty) continue ;;
    esac

    # Cari di semua subfolder
    local found=false
    while IFS= read -r -d '' dir; do
      local dirname
      dirname=$(basename "$dir")
      if echo "$dirname" | grep -qi "$proj" 2>/dev/null; then
        found=true; break
      fi
    done < <(find "$NIUMINATION" -maxdepth 3 -type d -not -path '*/\.*' -not -path '*/archive/*' -print0 2>/dev/null || true)

    if ! $found; then
      # Cek juga di archive
      while IFS= read -r -d '' dir; do
        local dirname
        dirname=$(basename "$dir")
        if echo "$dirname" | grep -qi "$proj" 2>/dev/null; then
          found=true; break
        fi
      done < <(find "$NIUMINATION/archive" -maxdepth 2 -type d -not -path '*/\.*' -print0 2>/dev/null || true)
    fi

    if ! $found; then
      warn "BACKLOG: '$proj' tercantum tapi folder tidak ditemukan di filesystem"
      rec "→ BACKLOG: hapus atau update entri '$proj' (missing dir)"
      issues=$((issues + 1))
    fi
  done < <(grep -E 'github.com/Niumination/' "$NIUMINATION/BACKLOG.md" 2>/dev/null || true)

  [ "$issues" -eq 0 ] && pass "BACKLOG.md sinkron dengan filesystem"
}

# ── Status GitHub Pages ────────────────────────────────────────────────────
check_gh_pages() {
  section "🌐 GitHub Pages"

  local urls=(
    "https://niumination.github.io/ecosystem-config"
    "https://niumination.github.io/niu-dash"
    "https://niumination.github.io/Niu-LKH"
  )

  for url in "${urls[@]}"; do
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$url" 2>/dev/null || echo "000")
    case "$code" in
      200|301|302) pass "$url → $code OK" ;;
      000) fail "$url → timeout / unreachable" ; rec "→ Cek deployment $url" ;;
      *)   warn "$url → HTTP $code" ;;
    esac
  done
}

# ── Main ───────────────────────────────────────────────────────────────────
main() {
  printf "${BOLD}${CYAN}"
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║              🔄 UP-ECO — Ecosystem Check             ║"
  echo "║         Niumination v4.0  •  $NOW        ║"
  echo "╚══════════════════════════════════════════════════════╝"
  printf "${NC}"

  # ── Phase 1: Git Status ──
  header
  section "📦 Git Status — Root Ecosystem"
  check_git_status "$NIUMINATION" "Ecosystem Root"

  section "📦 Git Status — Profile README"
  check_git_status "$PROFILE" "Profile README"

  # ── Phase 2: Dirty repos dalam ekosistem ──
  section "🔍 Dirty Repos (uncommitted changes)"
  local dirty_count=0
  while IFS= read -r repo; do
    local rel
    rel=${repo#$NIUMINATION/}
    local dirty_files
    dirty_files=$(cd "$repo" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [ "$dirty_files" -gt 0 ]; then
      fail "$rel — $dirty_files file(s) dirty"
      rec "→ $rel: commit & push ($dirty_files files)"
      dirty_count=$((dirty_count + 1))
    fi
  done < <(find "$NIUMINATION" -maxdepth 3 -name ".git" -type d -not -path '*/\.*' -exec dirname {} \; 2>/dev/null || true)
  [ "$dirty_count" -eq 0 ] && pass "Semua repos clean"

  # ── Phase 3: Folder asing ──
  check_unknown_folders

  # ── Phase 4: BACKLOG sync ──
  check_backlog_sync

  # ── Phase 5: GitHub Pages ──
  check_gh_pages

  # ── Summary ──
  header
  printf "${BOLD}${CYAN}◆ Rekomendasi${NC}\n"
  if [ -s "$REPORT_FILE" ]; then
    local count
    count=$(wc -l < "$REPORT_FILE")
    printf "  %d rekomendasi:\n\n" "$count"
    local i=1
    while IFS= read -r line; do
      printf "  ${YELLOW}%d.${NC} %s\n" "$i" "$line"
      i=$((i + 1))
    done < "$REPORT_FILE"
  else
    pass "✅ Ekosistem dalam kondisi sinkron — tidak ada rekomendasi"
  fi

  header
  printf "${BOLD}Selesai: ${NOW}${NC}\n"
}

main "$@"

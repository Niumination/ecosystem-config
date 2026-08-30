#!/usr/bin/env bash
# =============================================================================
# up-eco.sh — Ecosystem Status & Sync Checker v5.1
# =============================================================================
# Usage: ./scripts/up-eco.sh
#
# Memeriksa kondisi ekosistem Niumination dan merekomendasikan:
#   - Folder asing / tidak terdaftar di dokumentasi
#   - Git repos yang dirty / perlu commit
#   - Kesenjangan dengan GitHub remote
#   - Update dokumentasi (BACKLOG, AGENTS, README)
#   - Sinkronisasi dengan status GH Pages
#   - 🆕 Manajemen Skill Bank (integritas, sync, INDEX)
#   - 🆕 Dashboard Mission Control (skill monitor API)
# =============================================================================

set -euo pipefail

NIUMINATION="/Users/zaryu/Desktop/Niumination"
PROFILE="$NIUMINATION/agents/profile"
SKILLS_DIR="$NIUMINATION/skills"
INDEX_FILE="$SKILLS_DIR/INDEX.md"
SYNC_SCRIPT="$SKILLS_DIR/sync-to-agents.sh"
SYNC_LOG="$NIUMINATION/.sync-log"
MC_URL="http://localhost:5200"
HERMES_HOME="${HOME}/.hermes"
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
    docs scripts skills tools vault brain dotfiles archive core
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

# ═══════════════════════════════════════════════════════════════════════════
# 🆕 Phase 5b: GitHub Pull Requests
# ═══════════════════════════════════════════════════════════════════════════
check_gh_prs() {
  section "🔀 GitHub Pull Requests"

  # ── 5b-1: Cek gh CLI tersedia
  if ! command -v gh &>/dev/null; then
    warn "gh CLI tidak terinstall — skip PR check"
    rec "→ Install gh: brew install gh"
    return
  fi

  # ── 5b-2: Resolve real home (Hermes env may set HOME ke cache path)
  local gh_home="$HOME"
  if [ ! -d "$gh_home/.config/gh" ]; then
    if [ -d "/Users/${USER:-zaryu}/.config/gh" ]; then
      gh_home="/Users/${USER:-zaryu}"
    fi
  fi

  # ── 5b-3: Cek auth gh
  if ! HOME="$gh_home" timeout 8 gh auth status &>/dev/null; then
    warn "gh CLI belum authenticated — skip PR check"
    rec "→ gh auth login (atau set GH_TOKEN)"
    return
  fi

  # ── 5b-4: Satu query — semua open PR di org Niumination
  local prs_json
  prs_json=$(HOME="$gh_home" timeout 20 gh search prs --owner Niumination --state open --limit 50 \
    --json number,title,repository,isDraft,author,createdAt,updatedAt 2>/dev/null || echo "[]")

  local total
  total=$(echo "$prs_json" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")

  if [ "$total" -eq 0 ]; then
    pass "Tidak ada open pull request di org Niumination"
    return
  fi

  warn "$total open pull request di GitHub"

  # ── 5b-5: Tampilkan detail tiap PR
  echo "$prs_json" | python3 -c "
import sys, json
from datetime import datetime, timezone

prs = json.load(sys.stdin)
now = datetime.now(timezone.utc)
prs.sort(key=lambda p: p.get('updatedAt', ''))

def repo_name(p):
    r = p.get('repository')
    if isinstance(r, dict):
        return r.get('nameWithOwner', '?')
    return str(r) if r else '?'

def author_login(p):
    a = p.get('author')
    if isinstance(a, dict):
        return a.get('login', '?')
    return str(a) if a else '?'

for p in prs:
    repo = repo_name(p)
    num = p.get('number', '?')
    title = (p.get('title') or '?')[:75]
    draft = ' [DRAFT]' if p.get('isDraft') else ''
    author = author_login(p)
    updated = p.get('updatedAt', '')
    try:
        age_days = (now - datetime.fromisoformat(updated.replace('Z', '+00:00'))).days
    except Exception:
        age_days = 0
    age = 'baru' if age_days == 0 else f'{age_days} hari'
    stale = ' ⚠️ STALE' if age_days > 14 else ''
    print(f'  🔀 {repo}#{num}{draft} — {title}')
    print(f'     👤 {author} | update: {age}{stale} | url: https://github.com/{repo}/pull/{num}')
" 2>/dev/null || true

  # ── 5b-6: Hitung draft & stale untuk rekomendasi
  local draft_count stale_count
  draft_count=$(echo "$prs_json" | python3 -c "
import sys, json
from datetime import datetime, timezone
prs = json.load(sys.stdin)
print(sum(1 for p in prs if p.get('isDraft')))
" 2>/dev/null || echo "0")
  stale_count=$(echo "$prs_json" | python3 -c "
import sys, json
from datetime import datetime, timezone
prs = json.load(sys.stdin)
now = datetime.now(timezone.utc)
def ts(p):
    u = p.get('updatedAt', '')
    try: return datetime.fromisoformat(u.replace('Z', '+00:00'))
    except Exception: return now
print(sum(1 for p in prs if (now - ts(p)).days > 14))
" 2>/dev/null || echo "0")

  rec "→ Review & merge $total open PR — gh pr list --owner Niumination --state open"
  if [ "${draft_count:-0}" -gt 0 ]; then
    warn "$draft_count PR masih draft — perlu finalisasi"
    rec "→ $draft_count PR draft: selesaikan & ready-for-review"
  fi
  if [ "${stale_count:-0}" -gt 0 ]; then
    warn "$stale_count PR stale (>14 hari tanpa update)"
    rec "→ $stale_count PR stale: review / close / update branch"
  fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 🆕 Phase 6: Skill Bank Integrity
# ═══════════════════════════════════════════════════════════════════════════
check_skill_bank() {
  section "🧠 Skill Bank — Integritas"

  # ── 6a: Verifikasi SKILL.md files
  if [ ! -d "$SKILLS_DIR" ]; then
    fail "Direktori skills/ tidak ditemukan!"
    rec "→ Buat skills/ dengan struktur standar"
    return
  fi

  # Count all SKILL.md files by domain (portable: no associative arrays)
  local total_skills=0
  local skills_without_frontmatter=0
  local domain_list_file
  domain_list_file=$(mktemp)

  while IFS= read -r -d '' sk; do
    local rel="${sk#$SKILLS_DIR/}"
    local domain="${rel%%/*}"
    total_skills=$((total_skills + 1))
    echo "$domain" >> "$domain_list_file"

    # Quick frontmatter check (must start with ---)
    if ! head -1 "$sk" | grep -q '^---$' 2>/dev/null; then
      warn "$rel: SKILL.md tanpa frontmatter YAML"
      skills_without_frontmatter=$((skills_without_frontmatter + 1))
      rec "→ $rel: tambahkan frontmatter YAML (name, description, version, tags)"
    fi
  done < <(find "$SKILLS_DIR" -name SKILL.md -type f -not -path '*/\.*' -print0 2>/dev/null || true)

  # Report domain distribution
  if [ "$total_skills" -gt 0 ]; then
    local domain_report
    domain_report=$(sort "$domain_list_file" | uniq -c | sort -rn | awk '{printf "%s:%d ", $2, $1}')
    info "Total: $total_skills SKILL.md di bank pusat"
    info "Domain: $domain_report"
  fi
  rm -f "$domain_list_file"

  if [ "$skills_without_frontmatter" -gt 0 ]; then
    fail "$skills_without_frontmatter SKILL.md tanpa frontmatter"
  else
    pass "Semua SKILL.md punya frontmatter YAML"
  fi

  # ── 6b: Verifikasi INDEX.md vs filesystem
  if [ ! -f "$INDEX_FILE" ]; then
    fail "INDEX.md tidak ditemukan di skills/"
    rec "→ Buat INDEX.md dengan daftar semua skill"
    return
  fi

  # Skills listed in INDEX.md — count `| **name**` entries in domain tables
  # (skips Ringkasan, conflict tables, and other metadata rows)
  local index_skills=0
  while IFS= read -r line; do
    # Match table rows in domain tables: | **skill-name** |
    if echo "$line" | grep -qE '^\| \*\*[a-z]' 2>/dev/null; then
      index_skills=$((index_skills + 1))
    fi
  done < "$INDEX_FILE"

  # Compare filesystem count vs INDEX count
  if [ "$total_skills" -eq "$index_skills" ]; then
    pass "INDEX.md sinkron dengan filesystem ($total_skills skills)"
  else
    warn "Filesystem: $total_skills skills, INDEX.md: $index_skills skills — mismatch!"
    rec "→ Update INDEX.md: tambah/hapus entri yang tidak sinkron"

    # Find skills on disk not in INDEX
    while IFS= read -r -d '' sk; do
      local rel="${sk#$SKILLS_DIR/}"
      local skill_name
      skill_name=$(echo "$rel" | cut -d/ -f2)
      if ! grep -qi "\*\*${skill_name}\*\*" "$INDEX_FILE" 2>/dev/null; then
        warn "  '${skill_name}' ada di filesystem tapi TIDAK di INDEX.md"
        rec "→ INDEX.md: tambah baris untuk \`$skill_name\`"
      fi
    done < <(find "$SKILLS_DIR" -name SKILL.md -type f -not -path '*/\.*' -print0 2>/dev/null || true)
  fi

  # ── 6c: Cek duplikasi / konflik naming
  local name_check_file
  name_check_file=$(mktemp)
  local dup_found=false
  while IFS= read -r -d '' sk; do
    local rel="${sk#$SKILLS_DIR/}"
    local skill_name
    skill_name=$(echo "$rel" | cut -d/ -f2)
    if grep -q "^${skill_name}|" "$name_check_file" 2>/dev/null; then
      local prev_path
      prev_path=$(grep "^${skill_name}|" "$name_check_file" | cut -d'|' -f2)
      warn "Konflik: skill '$skill_name' muncul di 2 path!"
      info "  $prev_path dan $rel"
      rec "→ Hapus atau rename skill '$skill_name' yang duplikat"
      dup_found=true
    fi
    echo "${skill_name}|${rel}" >> "$name_check_file"
  done < <(find "$SKILLS_DIR" -name SKILL.md -type f -not -path '*/\.*' -print0 2>/dev/null || true)
  rm -f "$name_check_file"

  $dup_found || pass "Tidak ada duplikasi skill name"

  # ── 6d: Verifikasi manifest integritas SHA-256 (pola autoskills)
  if [ -f "$SKILLS_DIR/manifest.json" ]; then
    if python3 "$NIUMINATION/scripts/skill-manifest.py" --check > /tmp/up-eco-manifest.log 2>&1; then
      local mf_count
      mf_count=$(python3 -c "import json;m=json.load(open('$SKILLS_DIR/manifest.json'));print(f\"{m['skillCount']} skill, {m['fileCount']} file\")" 2>/dev/null || echo "?")
      pass "Manifest SHA-256 sinkron ($mf_count)"
    else
      fail "Manifest SHA-256 mismatch:"
      cat /tmp/up-eco-manifest.log
      rec "→ Regenerate manifest: python3 scripts/skill-manifest.py"
    fi
  else
    warn "manifest.json belum ada — integritas hash tidak diverifikasi"
    rec "→ Generate manifest: python3 scripts/skill-manifest.py"
  fi

  # ── 6e: Audit konten skill anti prompt-injection (pola autoskills Phase 3)
  if [ -f "$NIUMINATION/scripts/skill-audit.py" ]; then
    local audit_count
    audit_count=$(python3 "$NIUMINATION/scripts/skill-audit.py" --count 2>/dev/null || echo "?")
    if [ "$audit_count" = "0" ]; then
      pass "Audit konten skill bersih (0 finding)"
    elif [ "$audit_count" = "?" ]; then
      warn "skill-audit.py gagal dijalankan — cek manual: python3 scripts/skill-audit.py"
    else
      warn "Audit konten skill: $audit_count finding — review manual disarankan (warning-only)"
      rec "→ Detail: python3 scripts/skill-audit.py"
    fi
  else
    info "skill-audit.py belum ada — audit konten anti-injection dilewati"
  fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 🆕 Phase 7: Skill Sync Status
# ═══════════════════════════════════════════════════════════════════════════
check_skill_sync() {
  section "🔄 Skill Sync — Bank Pusat → Agent Targets"

  # ── 7a: Cek sync-to-agents.sh exists
  if [ ! -f "$SYNC_SCRIPT" ]; then
    fail "sync-to-agents.sh tidak ditemukan!"
    rec "→ Buat sync-to-agents.sh di skills/"
    return
  fi
  pass "sync-to-agents.sh tersedia"

  # ── 7b: Cek sync log (last run time)
  if [ -f "$SYNC_LOG" ]; then
    local last_sync
    last_sync=$(tail -1 "$SYNC_LOG" 2>/dev/null || echo "unknown")
    info "Sync terakhir: $last_sync"

    # Check if last sync was today
    local last_sync_date
    last_sync_date=$(echo "$last_sync" | grep -oE '^\[[0-9-]{10}' | tr -d '[]' || echo "")
    local today
    today=$(date "+%Y-%m-%d")
    if [ -n "$last_sync_date" ] && [ "$last_sync_date" = "$today" ]; then
      pass "Sync sudah berjalan hari ini"
    else
      warn "Sync terakhir bukan hari ini ($last_sync_date vs $today)"
      rec "→ Jalankan skills/sync-to-agents.sh untuk sync skill terbaru"
    fi
  else
    warn "Belum ada sync log — sync-to-agents.sh belum pernah dijalankan"
    rec "→ Pertama: jalankan skills/sync-to-agents.sh"
  fi

  # ── 7c: Cek divergence dengan target Jcode
  local jcode_skill_count=0
  local jcode_dir="$HOME/.jcode/skills"
  if [ -d "$jcode_dir" ]; then
    jcode_skill_count=$(find "$jcode_dir" -name SKILL.md -type f 2>/dev/null | wc -l | tr -d ' ')
    local bank_count
    bank_count=$(find "$SKILLS_DIR" -name SKILL.md -type f 2>/dev/null | wc -l | tr -d ' ')

    if [ "$jcode_skill_count" -ge "$bank_count" ]; then
      pass "Jcode: $jcode_skill_count skills (up to date)"
    else
      warn "Jcode: $jcode_skill_count of $bank_count skills — ada $((bank_count - jcode_skill_count)) belum tersync"
      rec "→ Jalankan sync-to-agents.sh untuk update Jcode"
    fi
  else
    warn "Jcode skill dir ($jcode_dir) tidak ditemukan"
  fi

  # ── 7d: Cek divergence dengan Hermes target
  local hermes_skill_count=0
  local hermes_dir="$HOME/.hermes/skills"
  if [ -d "$hermes_dir" ]; then
    hermes_skill_count=$(find "$hermes_dir" -name SKILL.md -type f 2>/dev/null | wc -l | tr -d ' ')
    info "Hermes: $hermes_skill_count skills"
  else
    info "Hermes dir ($hermes_dir) tidak ditemukan (optional)"
  fi

  # ── 7e: Cek Hermes USB (backup-only — bukan target aktif)
  local usb_dir="/Volumes/HermesAgent/HermesAgentUSB/data/skills"
  if [ -d "$usb_dir" ]; then
    local usb_count
    usb_count=$(find "$usb_dir" -name SKILL.md -type f 2>/dev/null | wc -l | tr -d ' ')
    info "Hermes USB (backup-only): $usb_count skills terdeteksi — bukan target aktif"
  else
    info "Hermes USB tidak terhubung (normal — USB = backup)"
  fi
}

# ═══════════════════════════════════════════════════════════════════════════
# 🆕 Phase 8: Mission Control Dashboard (Skill Monitor)
# ═══════════════════════════════════════════════════════════════════════════
check_mission_control() {
  section "🎛️ Mission Control — Skill Monitor Dashboard"

  # ── 8a: Cek apakah server MC berjalan
  local mc_health
  mc_health=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 "$MC_URL/health" 2>/dev/null || echo "000")
  mc_health="${mc_health:0:3}"  # Trim to 3 chars (curl may repeat digits on some macOS versions)

  if [ "$mc_health" = "000" ]; then
    warn "Mission Control server tidak merespon di port 5200"
    rec "→ Start MC: cd services/niu-mission-control && python3 server.py"
    return
  fi
  pass "MC Server: HTTP $mc_health"

  # ── 8b: Skill API — total skills & active
  local skills_json
  skills_json=$(curl -s --connect-timeout 3 "$MC_URL/api/mc/skills" 2>/dev/null || echo "{}")
  local total_skills_api
  total_skills_api=$(echo "$skills_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('total','?'))" 2>/dev/null || echo "?")
  local active_skills_api
  active_skills_api=$(echo "$skills_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('active','?'))" 2>/dev/null || echo "?")

  if [ "$total_skills_api" != "?" ]; then
    pass "Skill API: $total_skills_api total, $active_skills_api aktif"
  else
    warn "Skill API tidak bisa diakses"
    rec "→ Periksa log MC: cek apakah skill_monitor terinisialisasi"
  fi

  # ── 8c: Stale skills (>30 hari)
  local stale_json
  stale_json=$(curl -s --connect-timeout 3 "$MC_URL/api/mc/skills/stale" 2>/dev/null || echo "{}")
  local stale_count
  stale_count=$(echo "$stale_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('count',0))" 2>/dev/null || echo "0")

  if [ "$stale_count" != "?" ] && [ "$stale_count" -gt 0 ]; then
    warn "$stale_count stale skills (>30 hari tidak dipakai)"
    # Show top stale skills
    echo "$stale_json" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for s in d.get('stale', [])[:5]:
    tag = '\U0001f195 never loaded' if s.get('never_loaded') else f'{s.get(\"days_since_last_load\",0)} days'
    print(f'  \u23f3 {s[\"name\"]} ({s.get(\"domain\",\"?\")}) \u2014 {tag}')
" 2>/dev/null || true
    rec "→ Cek /api/mc/skills/stale untuk detail — review skill yang jarang dipakai"
  else
    pass "Tidak ada stale skills"
  fi

  # ── 8d: Skill conflicts
  local conflict_json
  conflict_json=$(curl -s --connect-timeout 3 "$MC_URL/api/mc/skills/conflicts" 2>/dev/null || echo "{}")
  local conflict_count
  conflict_count=$(echo "$conflict_json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('count',0))" 2>/dev/null || echo "0")

  if [ "$conflict_count" != "?" ] && [ "$conflict_count" -gt 0 ]; then
    warn "$conflict_count skill conflict(s) terdeteksi"
    echo "$conflict_json" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for c in d.get('conflicts', []):
    if c.get('both_active'):
        print(f'  🔴 Conflict: {c[\"skills\"][0]} vs {c[\"skills\"][1]} — {c.get(\"reason\",\"\")}')
    elif 'not in bank pusat' in c.get('reason',''):
        print(f'  ⚠️  Orphan: {c[\"skills\"][0]} — {c.get(\"reason\",\"\")}')
" 2>/dev/null || true
    rec "→ Cek /api/mc/skills/conflicts — resolve active skill conflicts"
  else
    pass "Tidak ada skill conflicts"
  fi

  # ── 8e: Cek dashboard UI bisa diakses
  local dash_code
  dash_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 "$MC_URL/" 2>/dev/null || echo "000")
  if [ "$dash_code" != "000" ]; then
    pass "Dashboard UI: HTTP $dash_code"
  else
    warn "Dashboard UI tidak bisa diakses"
    rec "→ Cek dashboard/ folder di niu-mission-control"
  fi

  # ── 8f: Skill usage stats (hari ini)
  local stats_json
  stats_json=$(curl -s --connect-timeout 3 "$MC_URL/api/mc/skills/stats" 2>/dev/null || echo "{}")
  local today_loaded
  today_loaded=$(echo "$stats_json" | python3 -c "
import sys, json
d = json.load(sys.stdin)
total = sum(s.get('today', 0) for s in d.get('stats', []))
print(total)
" 2>/dev/null || echo "?")

  if [ "$today_loaded" != "?" ]; then
    info "Skill loads hari ini: $today_loaded"
  fi

  # ── Phase 9b: Gaya Jawab Guard (anti bertele-tele) ────────────────────────
  section "✂️ Gaya Jawab — Anti Bertele-tele (SOUL + config)"
  local v_ok=true
  # SOUL live harus punya bab Gaya jawab (didefinisikan langsung di ~/.hermes/SOUL.md,
  # bukan dari template eksternal — template rebuild-v2 sudah dihapus dari repo)
  if ! grep -q "Gaya jawab" "$HERMES_HOME/SOUL.md" 2>/dev/null; then
    fail "SOUL.md tanpa bab Gaya jawab — balasan Telegram akan bertele-tele"
    rec "→ Tambahkan bab '## Gaya jawab' (ringkas 3-5 baris) ke ~/.hermes/SOUL.md"
    v_ok=false
  fi
  # 4 config anti-verbose
  local compact tcg tce pers
  compact=$(hermes config get display.compact 2>/dev/null | tr -d ' \n' || echo "?")
  tcg=$(hermes config get agent.task_completion_guidance 2>/dev/null | tr -d ' \n' || echo "?")
  tce=$(hermes config get display.turn_completion_explainer 2>/dev/null | tr -d ' \n' || echo "?")
  pers=$(hermes config get display.personality 2>/dev/null | tr -d ' \n' || echo "?")
  if [ "$compact" != "true" ]; then warn "display.compact=$compact (harusnya true)"; rec "→ hermes config set display.compact true"; v_ok=false; fi
  if [ "$tcg" != "false" ]; then warn "agent.task_completion_guidance=$tcg (harusnya false)"; rec "→ hermes config set agent.task_completion_guidance false"; v_ok=false; fi
  if [ "$tce" != "false" ]; then warn "display.turn_completion_explainer=$tce (harusnya false)"; rec "→ hermes config set display.turn_completion_explainer false"; v_ok=false; fi
  if [ -n "$pers" ] && [ "$pers" != "?" ]; then warn "display.personality=$pers (harusnya kosong)"; rec "→ hermes config set display.personality \"\""; v_ok=false; fi
  if [ "$v_ok" = true ]; then pass "Gaya jawab ringkas aktif (SOUL + 4 config sinkron)"; fi
}

# ── Phase 9: Telegram Thread Status 🆕 ─────────────────────────────────────
check_telegram_threads() {
  section "💬 Telegram Thread Status — Mission Control (5 thread)"
  python3 "$(dirname "$0")/telegram_threads.py" 2>/dev/null || warn "telegram_threads.py tidak tersedia"
}

# ── Phase 9a: Trio Awareness (Hermes · JCode · OpenCode) 🆕 ───────────────────
check_trio_awareness() {
  local from="${FROM:-hermes}"
  section "🔗 Trio Awareness — Called dari: $from"
  bash "$(dirname "$0")/trio-watch.sh" --from "$from" || warn "trio-watch.sh gagal dijalankan"
}

# ── Main ───────────────────────────────────────────────────────────────────
main() {
  # ── Parse --from arg (trio awareness) ──
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --from) FROM="$2"; shift 2;;
      --from=*) FROM="${1#*=}"; shift;;
      *) break;;
    esac
  done

  printf "${BOLD}${CYAN}"
  echo "╔══════════════════════════════════════════════════════╗"
  echo "║              🔄 UP-ECO — Ecosystem Check             ║"
  echo "║         Niumination v5.1  •  $NOW        ║"
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

  # ── Phase 5b: GitHub Pull Requests 🆕 ──
  check_gh_prs

  # ── Phase 6: Skill Bank Integrity 🆕 ──
  check_skill_bank

  # ── Phase 7: Skill Sync Status 🆕 ──
  check_skill_sync

  # ── Phase 8: Mission Control Dashboard 🆕 ─────────────────────────────────
  check_mission_control

  # ── Phase 9: Telegram Thread Status 🆕 ────────────────────────────────────
  check_telegram_threads

  # ── Phase 9a: Trio Awareness (Hermes · JCode · OpenCode) 🆕 ───────────────────
  # 🔧 FIX: semua output trio-watch ke STDERR — supaya stdout (phase lain) tidak terpotong di Telegram
  check_trio_awareness
  echo "" 2>&1
  # ── Phase 9b: Gaya Jawab Guard (anti bertele-tele) ───────────────────────
  # Catatan: guard gaya jawab sudah dijalankan di akhir check_mission_control()
  # (tidak ada fungsi check_verbosity terpisah — panggilan lama menyebabkan error 127)

  # ── Summary ───────────────────────────────────────────────────────────────
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

  if [ -x "$ROOT/scripts/9router-sync.sh" ]; then echo "[up-eco] 9router-sync..."; "$ROOT/scripts/9router-sync.sh" 2>&1 | tail -n 2; cnt=$(python3 -c "import json; print(len(json.load(open("$HOME/.cache/niumination/9router-models.json")).get("data",[])))" 2>/dev/null || echo "?"); echo "[up-eco] 9router: $cnt models"; fi
  header
  printf "${BOLD}Selesai: ${NOW}${NC}\n"
}

ROOT=""

main "$@"
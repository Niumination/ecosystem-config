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

# Ensure timeout/gh/composio resolve in Hermes background (PATH=/usr/bin:/bin)
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
TIMEOUT_BIN="$(command -v timeout 2>/dev/null || command -v gtimeout 2>/dev/null || echo timeout)"

NIUMINATION="/Users/zaryu/Desktop/Niumination"
PROFILE="$NIUMINATION/agents/profile"
SKILLS_DIR="$NIUMINATION/skills"
INDEX_FILE="$SKILLS_DIR/INDEX.md"
SYNC_SCRIPT="$SKILLS_DIR/sync-to-agents.sh"
SYNC_LOG="$NIUMINATION/.sync-log"
MC_URL="http://localhost:3000"        # MC modern = Next.js apex-ui
MC_API_URL="http://localhost:5200"    # legacy FastAPI skill-monitor (sudah dihapus dari repo)
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
  # Fix 19 Sep 2026: '@{upstream}' gagal (fatal) bila branch tidak punya upstream tracking —
  # kasus nyata di root ecosystem-config, sehingga pelaporan ahead/behind SELALU 0 dan commit
  # yang menunggu push tidak pernah terlihat. Fallback ke origin/<branch>.
  local upstream_ref
  upstream_ref=$(cd "$dir" && git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)
  if [ -z "$upstream_ref" ] && git -C "$dir" rev-parse --verify -q "origin/$branch" >/dev/null 2>&1; then
    upstream_ref="origin/$branch"
  fi
  ahead=0
  behind=0
  if [ -n "$upstream_ref" ]; then
    ahead=$(cd "$dir" && git rev-list --count "$upstream_ref"..HEAD 2>/dev/null || echo "0")
    behind=$(cd "$dir" && git rev-list --count HEAD.."$upstream_ref" 2>/dev/null || echo "0")
  fi
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
    docs scripts skills tools vault brain dotfiles archive core logs
    inactive-2026-09
    dinas
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
      # Nama berkas/folder DI DALAM proyek bukan nama proyek — mis. baris yang
      # menulis **`web/`** lalu menyebut URL GitHub, ikut terjaring regex di atas.
      # Nama proyek tidak pernah memuat '/' maupun backtick.
      *"/"*|*'`'*) continue ;;
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

  # PENTING (fix 2026-09-18): tanpa `return 0`, pernyataan `[ ... ] && pass` di atas
  # bernilai false saat ada issue → fungsi mengembalikan 1 → `set -euo pipefail`
  # MEMATIKAN seluruh script. Akibatnya Phase 5 s/d 12 (GitHub Pages, PR, integritas
  # bank skill, SOUL drift, sync, Mission Control, MCP, plugin, Composio) tidak pernah
  # berjalan — tanpa pesan error, jadi terlihat seperti laporan yang normal.
  return 0
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
    code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 8 "$url" 2>/dev/null || echo "000")
    case "$code" in
      200|301|302) pass "$url → $code OK" ;;
      000) fail "$url → timeout / unreachable" ; rec "→ Cek deployment $url" ;;
      *)   warn "$url → HTTP $code" ;;
    esac
  done
}

# ═══════════════════════════════════════════════════════════════════════════
# Phase 5a: Vercel — daftar proyek + probe riil vs registry
# ═══════════════════════════════════════════════════════════════════════════
# Kenapa fase ini ada (26 Sep 2026): registry klaim "Vercel 5 Live" tapi 7 dari
# 13 status ternyata meleset. 2 di antaranya bukan sekadar paused:
#   - `kms-spbe` klaim 200, faktanya TIDAK ADA di akun Vercel (DNS mati, 000)
#   - `virtual-assistance` klaim 200 lewat hostname yang tidak pernah ada;
#     hostname sebenarnya `virtual-assistance-pi` dan statusnya PAUSED
# Penyebab: status ditulis dari ingatan, tidak pernah di-probe ulang.
#
# PENTING: 503 pada Vercel BUKAN generic error. Body-nya berisi
# `DEPLOYMENT_PAUSED` — itu status resmi "sengaja dimatikan", bukan crash.
# Jadi probe WAJIB baca body, bukan cuma status code.
check_vercel() {
  section "▲ Vercel"

  if ! command -v vercel &>/dev/null; then
    info "vercel CLI tidak terinstall — skip Vercel check"
    rec "→ Install Vercel CLI untuk cek deployment: npm i -g vercel"
    return
  fi

  # ── 5a-1: Ambil daftar proyek (scope default)
  # PENTING (26 Sep 2026): CLI Vercel 59.x menulis banner + tabel proyek ke
  # STDERR, bukan stdout. `vercel project ls > file` menghasilkan file kosong.
  # Jadi keduanya harus ditangkap.
  local raw
  raw=$(vercel project ls 2>&1 || true)
  if [ -z "$raw" ]; then
    warn "gagal membaca 'vercel project ls' (belum login? token kadaluarsa?)"
    rec "→ Cek login Vercel: vercel whoami"
    return
  fi

  local scope
  scope=$(printf '%s\n' "$raw" | grep -oE 'in [a-z0-9-]+$' | head -1 | tr -d ' ' || true)
  [ -n "$scope" ] && info "scope: $scope" || true

  # Parse: nama + production URL. Kolom "Latest Production URL" = "--" kalau
  # proyek belum pernah di-deploy. Nama proyek tidak mengandung spasi.
  # Filter pakai daftar-tolak eksplisit — JANGAN pakai `*)` sebagai fallback
  # karena `*` di `case` match APA SAJA dan akan membuang semua baris.
  local names=() urls=()
  local line name url
  while IFS= read -r line; do
    name=$(printf '%s' "$line" | awk '{print $1}')
    url=$(printf '%s' "$line"  | awk '{print $2}')
    [ -z "$name" ] && continue
    # hanya baris data: nama proyek = huruf kecil + angka + tanda hubung/koma
    case "$name" in
      [a-z0-9]*) ;;
      *) continue ;;
    esac
    # buang yang jelas bukan nama proyek
    case "$name" in
      vercel.app|https*|Project|Fetching|Found|Updated) continue ;;
    esac
    names+=("$name")
    # Shell gotcha: `a && b || c` TIDAK aman di sini — kalau `urls+=(...)`
    # ternyata return non-zero, `c` ikut jalan dan baris jadi dobel. Pakai if.
    if [ "$url" = "--" ]; then
      urls+=("")            # never deployed → placeholder agar indeks sinkron
    else
      urls+=("${url#https://}")
    fi
  done < <(printf '%s\n' "$raw" | sed -n '/Project Name/,$p' | tail -n +2)

  local total=${#names[@]}
  if [ "$total" -eq 0 ]; then
    warn "tidak ada proyek ter-parse dari output Vercel"
    return
  fi
  info "$total proyek terdaftar di $scope"

  # ── 5a-2: Probe hostname. Kolom URL dari Vercel adalah hostname yang
  # sebenar-nya dipakai (mis. `virtual-assistance-pi.vercel.app`), JADI probe
  # hostname itu — bukan `nama-proyek.vercel.app` yang mengarang.
  local live=0 paused=0 nodeploy=0 other=0
  local registry="$NIUMINATION/docs/registry/deployment-status.md"
  local drift=0

  local i
  for i in "${!names[@]}"; do
    name="${names[$i]}"
    if [ -z "${urls[$i]}" ]; then
      # Never deployed — tidak ada hostname untuk diprobe
      info "$name — ⚪ belum pernah di-deploy (tidak ada production URL)"
      nodeploy=$((nodeploy + 1))
      continue
    fi

    local host="${urls[$i]}"
    # Satu panggilan dapat dua hal: body (untuk deteksi DEPLOYMENT_PAUSED)
    # + status code (untuk klasifikasi). `-w` menulis kode di akhir body.
    local resp code body
    resp=$(curl -s -w $'\n__CODE__%{http_code}' --connect-timeout 6 --max-time 12 \
                 -A "curl/8" "https://$host" 2>/dev/null || true)
    code="${resp##*__CODE__}"
    body="${resp%$'\n'__CODE__*}"
    [ -z "$code" ] && code="000"

    if printf '%s' "$body" | grep -q "DEPLOYMENT_PAUSED"; then
      pass "$name ($host) → ⏸️ PAUSED (503, DEPLOYMENT_PAUSED)"
      paused=$((paused + 1))
    else
      # 307/308 = redirect sehat (trailing slash, locale, /dashboard). Tetap LIVE.
      local note=""
      if [ "$code" = "307" ] || [ "$code" = "308" ]; then note=" (redirect)"; fi
      case "$code" in
        200|307|308) pass "$name ($host) → ✅ $code LIVE$note" ; live=$((live + 1)) ;;
        000) warn "$name ($host) → ⚠️ 000 DNS mati / tidak terjangkau" ; other=$((other + 1)) ;;
        *)   warn "$name ($host) → HTTP $code" ; other=$((other + 1)) ;;
      esac
    fi
  done

  # ── 5a-3: Bandingkan dengan registry. Registry boleh salah diam-diam;
  # yang harus dicek justru klaim yang ditulis dari ingatan.
  if [ -f "$registry" ]; then
    # Hostname yang diklaim registry. Abaikan baris yang SEDANG menjelaskan
    # kesalahan (memuat kata "tidak pernah ada" / "salah tulis") — baris itu
    # bukan klaim aktif, dan ikut menghitungnya akan menghasilkan ghost palsu
    # yang mengabukan drift yang sebenarnya.
    # `set -euo pipefail` aktif: SETIAP grep di rantai WAJIB punya `|| true`.
    local claimed_all
    claimed_all=$( { grep -E '^\| `' "$registry" \
                  | grep -vE 'tidak pernah ada|salah tulis|Tidak ada di akun|tidak ada di akun' \
                  | grep -oE '`[a-z0-9-]+\.vercel\.app`' || true; } | tr -d '`' | sort -u || true)

    # Hostname yang registry klaim tapi tidak ada di akun Vercel.
    # Pakai while-read via here-string, bukan pipe: pipe bikin subshell sehingga
    # variabel counter tidak kembali ke caller.
    local ghost="" h found g
    if [ -n "$claimed_all" ]; then
      while IFS= read -r h; do
        if [ -z "$h" ]; then continue; fi
        found=0
        for g in "${urls[@]}"; do
          if [ "$g" = "$h" ]; then found=1; break; fi
        done
        if [ "$found" -eq 0 ]; then
          if [ -z "$ghost" ]; then ghost="$h"; else ghost="$ghost $h"; fi
        fi
      done <<< "$claimed_all"
    fi

    if [ -n "$ghost" ]; then
      local count
      count=$(printf '%s\n' "$ghost" | wc -w | tr -d ' ')
      warn "$count hostname di registry tapi TIDAK ada di akun Vercel (ghost): $ghost"
      drift=$((drift + 1))
      rec "→ Registry punya $count hostname Vercel yang tidak ada di akun: $ghost"
    fi
  fi

  # ── 5a-4: Ringkasan + deteksi drift jumlah live ──
  info "Ringkasan: $live live · $paused paused · $nodeploy never-deployed · $other lain-lain"

  # Bandingkan headline registry: baris tabel "| Vercel | N/M | ..." di BACKLOG.
  # Pola WAJIB di-anchor keAWAL BARIS (`^\| Vercel`) — kalau cuma `| Vercel |`
  # akan kena baris proyek yang kebetulan punya sel itu (mis. PemdiAcehTengah).
  if [ -f "$NIUMINATION/BACKLOG.md" ]; then
    local reg_live=""
    reg_live=$( { grep -E '^\| Vercel \|' "$NIUMINATION/BACKLOG.md" || true; } | head -1 \
               | grep -oE '[0-9]+/[0-9]+' | head -1 || true)
    if [ -n "$reg_live" ]; then
      local reg_total="${reg_live#*/}"
      if [ "$reg_total" = "$total" ]; then
        info "BACKLOG klaim $reg_live — cocok dengan jumlah proyek di akun ($total), probe riil $live live"
      else
        warn "BACKLOG klaim $reg_live tapi akun punya $total proyek — registry kemungkinan stale"
        rec "→ Sinkronkan baris '| Vercel |' di BACKLOG.md: $reg_live → $live/$total"
      fi
    fi
  fi
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

  # ── 5b-3: Cek auth gh (keyring Hermes kadang tak kebuka di background → fallback ke gh api user + hosts.yml)
  local gh_ok=false
  if HOME="$gh_home" $TIMEOUT_BIN 8 gh auth status --hostname github.com &>/dev/null; then gh_ok=true
  elif HOME="$gh_home" $TIMEOUT_BIN 8 gh api user --jq .login &>/dev/null; then gh_ok=true
  elif $TIMEOUT_BIN 8 gh auth status --hostname github.com &>/dev/null; then gh_ok=true
  elif [ -f "/Users/${USER:-zaryu}/.config/gh/hosts.yml" ] && grep -q "github.com" "/Users/${USER:-zaryu}/.config/gh/hosts.yml" 2>/dev/null; then gh_ok=true
  fi
  if [ "$gh_ok" = false ]; then
    warn "gh CLI belum authenticated — skip PR check"
    rec "→ gh auth login (atau set GH_TOKEN)"
    return
  fi

  # ── 5b-4: Satu query — semua open PR di org Niumination
  # Hermes snap kadang sudah punya GITHUB_TOKEN stale → override paksa dari .hermes/.env (fresh) & keyring
  if [ -f "/Users/${USER:-zaryu}/.hermes/.env" ]; then
    _tok=$(grep -E "^GITHUB_TOKEN=" "/Users/${USER:-zaryu}/.hermes/.env" 2>/dev/null | cut -d= -f2- | tr -d '"\r' | head -n1)
    if [ -n "$_tok" ] && [ "${#_tok}" -ge 35 ]; then export GH_TOKEN="$_tok"; export GITHUB_TOKEN="$_tok"; fi
    unset _tok
  fi
  if [ -z "${GH_TOKEN:-}" ] && [ -z "${GITHUB_TOKEN:-}" ]; then
    _tok=$(HOME="$gh_home" gh auth token 2>/dev/null || true)
    if [ -n "$_tok" ]; then export GH_TOKEN="$_tok"; fi
    unset _tok
  fi
  # fallback: jika masih kosong, coba gh auth token lagi
  if [ -z "${GH_TOKEN:-}" ]; then
    _tok=$(HOME="$gh_home" gh auth token 2>/dev/null || true)
    [ -n "$_tok" ] && export GH_TOKEN="$_tok"
    unset _tok
  fi
  local prs_json
  prs_json=$(HOME="$gh_home" $TIMEOUT_BIN 20 gh search prs --owner Niumination --state open --limit 50 \
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
# ── 6c: Verifikasi SOUL drift guard (dotfiles vs portable vs active) ────
check_lightfix() {
  section "🪄 Lightfix & Cron — perbaikan ringan otomatis"
  local script="$NIUMINATION/scripts/up-eco-lightfix.sh"
  local wrapper="$HOME/.hermes/scripts/up-eco-lightfix.sh"
  local jobname="up-eco-lightfix"

  if [ ! -x "$script" ]; then
    fail "skrip lightfix tidak ada/tidak executable: $script"
    rec "→ pulihkan dari git: git -C $NIUMINATION checkout -- scripts/up-eco-lightfix.sh"
    return
  fi
  pass "skrip lightfix tersedia: scripts/up-eco-lightfix.sh"

  # Penjaga autocommit: hanya churn timestamp yang boleh di-commit otomatis.
  if [ -x "$NIUMINATION/scripts/lightfix-autocommit.sh" ]; then
    pass "penjaga autocommit tersedia: scripts/lightfix-autocommit.sh"
  else
    warn "penjaga autocommit tidak ada/tidak executable: scripts/lightfix-autocommit.sh"
    rec "→ pulihkan: git -C $NIUMINATION checkout -- scripts/lightfix-autocommit.sh && chmod +x"
  fi

  # Pemberitahuan: commit timestamp dari lightfix TIDAK pernah di-push (kebijakan: tanpa
  # push otomatis). Tanpa baris ini, commit menumpuk senyap di lokal dan baru ketahuan saat
  # sesi berikutnya. Dihitung dari commit yang belum ter-push dengan subjek khas lightfix.
  local upstream pending_auto pending_all
  upstream=$(git -C "$NIUMINATION" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)
  if [ -z "$upstream" ]; then
    local nb
    nb=$(git -C "$NIUMINATION" rev-parse --abbrev-ref HEAD 2>/dev/null || true)
    if [ -n "$nb" ] && git -C "$NIUMINATION" rev-parse --verify -q "origin/$nb" >/dev/null 2>&1; then
      upstream="origin/$nb"
    fi
  fi
  pending_auto=0
  pending_all=0
  if [ -n "$upstream" ]; then
    pending_all=$(git -C "$NIUMINATION" rev-list --count "$upstream"..HEAD 2>/dev/null || echo 0)
    pending_auto=$(git -C "$NIUMINATION" log --format='%s' "$upstream"..HEAD 2>/dev/null | grep -c 'lightfix otomatis' || true)
    pending_auto=${pending_auto:-0}
    pending_all=${pending_all:-0}
  fi
  if [ "$pending_auto" -gt 0 ]; then
    warn "$pending_auto commit timestamp lightfix belum di-push (dari $pending_all commit belum ter-push)"
    rec "→ push commit timestamp: git -C $NIUMINATION push origin main"
  else
    pass "tidak ada commit timestamp lightfix yang menunggu push"
  fi

  # Cron Hermes hanya boleh menjalankan script di ~/.hermes/scripts/ → wrapper tipis
  if [ -x "$wrapper" ]; then
    pass "wrapper Hermes ada: ~/.hermes/scripts/up-eco-lightfix.sh"
  else
    mkdir -p "$HOME/.hermes/scripts" 2>/dev/null || true
    if printf '#!/usr/bin/env bash\nexec bash %s "$@"\n' "$script" > "$wrapper" && chmod +x "$wrapper"; then
      pass "wrapper dibuat otomatis: ~/.hermes/scripts/up-eco-lightfix.sh"
    else
      fail "gagal membuat wrapper di ~/.hermes/scripts/"
      return
    fi
  fi

  # Job cron: verifikasi, dan buat sendiri bila hilang (idempoten)
  if ! command -v hermes >/dev/null 2>&1; then
    warn "CLI 'hermes' tidak ditemukan — cron tidak dapat diverifikasi/dibuat"
    rec "→ pastikan 'hermes' ada di PATH, lalu jalankan up-eco lagi"
    return
  fi
  if "$TIMEOUT_BIN" 25 hermes cron list 2>/dev/null | grep -q "$jobname"; then
    pass "cron '$jobname' terdaftar (30 23 * * * · script-only, tanpa panggilan LLM)"
  else
    if "$TIMEOUT_BIN" 25 hermes cron create '30 23 * * *' --name "$jobname" --script up-eco-lightfix.sh \
         --no-agent --deliver local --workdir "$NIUMINATION" >/dev/null 2>&1; then
      pass "cron '$jobname' tidak ada → dibuat otomatis (30 23 * * *)"
    else
      fail "cron '$jobname' tidak ada dan gagal dibuat otomatis"
      rec "→ manual: hermes cron create '30 23 * * *' --name $jobname --script up-eco-lightfix.sh --no-agent --deliver local"
      return
    fi
  fi

  # Ringkasan hasil lightfix terakhir (bila ada) + drift INDEX saat ini
  if python3 "$NIUMINATION/scripts/gen-skill-index.py" --check >/dev/null 2>&1; then
    pass "INDEX.md sinkron dengan bank"
  else
    warn "INDEX.md drift — akan diperbaiki oleh lightfix/cron"
    rec "→ jalankan sekarang: bash scripts/up-eco-lightfix.sh"
  fi
  local log="$NIUMINATION/logs/up-eco-lightfix.log"
  if [ -f "$log" ]; then
    info "lightfix terakhir: $(grep -E 'lightfix selesai rc=' "$log" | tail -1 | sed 's/^\[//;s/\]//')"
  else
    info "lightfix belum pernah dijalankan — log: logs/up-eco-lightfix.log"
  fi
}

check_soul_drift() {
  section "🧠 SOUL Drift Guard"

  local dotfiles_soul="$NIUMINATION/dotfiles/zaryu-terminal-dotfiles/hermes/SOUL.md"
  local portable_soul="$NIUMINATION/apps/JHermUSB-portable/SOUL.md"
  local active_soul="$HOME/.hermes/SOUL.md"
  local drift=false

  if [ ! -f "$dotfiles_soul" ]; then
    warn "Dotfiles SOUL.md tidak ditemukan: $dotfiles_soul"
    rec "→ Buat SOUL.md di dotfiles repo sebagai single source of truth"
    drift=true
  fi

  if [ -f "$portable_soul" ]; then
    local dot_hash port_hash
    dot_hash=$(shasum -a 256 "$dotfiles_soul" | awk '{print $1}')
    port_hash=$(shasum -a 256 "$portable_soul" | awk '{print $1}')
    if [ "$dot_hash" != "$port_hash" ]; then
      warn "Portable SOUL.md differs from dotfiles (drift detected)"
      rec "→ Sync portable from dotfiles: cp $dotfiles_soul $portable_soul"
      drift=true
    fi
  fi

  if [ -L "$active_soul" ]; then
    local target
    target=$(readlink "$active_soul")
    if [ "$target" != "$dotfiles_soul" ]; then
      warn "Active SOUL.md symlink points to wrong target: $target"
      rec "→ Fix symlink: ln -sf $dotfiles_soul $active_soul"
      drift=true
    fi
  elif [ -f "$active_soul" ]; then
    local active_hash dot_hash
    active_hash=$(shasum -a 256 "$active_soul" | awk '{print $1}')
    dot_hash=$(shasum -a 256 "$dotfiles_soul" | awk '{print $1}')
    if [ "$active_hash" != "$dot_hash" ]; then
      warn "Active SOUL.md is not symlinked and differs from dotfiles"
      rec "→ Replace active with symlink: ln -sf $dotfiles_soul $active_soul"
      drift=true
    fi
  fi

  if [ "$drift" = false ]; then
    pass "SOUL.md sinkron: dotfiles == portable == active symlink"
  fi
}

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
    if echo "$line" | grep -qE '^\| \*\*[^*]+\*\* \| ✅ Aktif \|' 2>/dev/null; then
      index_skills=$((index_skills + 1))
    fi
  done < "$INDEX_FILE"

  # Compare filesystem count vs INDEX count
  # Perbaikan 19 Sep 2026: INDEX.md mencantumkan sebagian skill DUA KALI (tabel "featured"
  # di atas + tabel domainnya) sehingga jumlah BARIS selalu > jumlah skill bank (163 vs 145)
  # dan peringatan mismatch-nya palsu. Yang dibandingkan harus NAMA UNIK.
  local index_unique
  index_unique=$(grep -E '^\| \*\*[^*]+\*\* \| ✅ Aktif \|' "$INDEX_FILE" 2>/dev/null | sed 's/^| \*\*//; s/\*\* | ✅ Aktif |.*$//' | sort -u | wc -l | tr -d ' ')
  if [ "$total_skills" -eq "$index_unique" ]; then
    pass "INDEX.md sinkron dengan filesystem ($total_skills skills)"
  else
    warn "Filesystem: $total_skills skills, INDEX.md memuat $index_unique nama unik — mismatch!"
    rec "→ Update INDEX.md: tambah/hapus entri yang tidak sinkron"

    # Find skills on disk not in INDEX
    while IFS= read -r -d '' sk; do
      local rel="${sk#$SKILLS_DIR/}"
      local skill_name
      # Nama skill = direktori yang memuat SKILL.md (basename), BUKAN komponen
      # path ke-2: bank mendukung subkategori (`mlops/inference/llama-cpp`), dan
      # `cut -d/ -f2` menghasilkan "inference" → false positive "tidak di INDEX".
      skill_name=$(basename "$(dirname "$rel")")
      if ! grep -qi "\*\*${skill_name}\*\*" "$INDEX_FILE" 2>/dev/null; then
        warn "  '${skill_name}' ada di filesystem tapi TIDAK di INDEX.md"
        rec "→ INDEX.md: tambah baris untuk \`$skill_name\`"
      fi
    done < <(find "$SKILLS_DIR" -name SKILL.md -type f -not -path '*/\.*' -print0 2>/dev/null || true)
  fi

  # ── 6b-2: Verifikasi baris COUNTER INDEX.md vs angka otoritatif (manifest)
  # Baris `> **Status:** N ✅ Aktif` adalah angka manual, terpisah dari tabel.
  # 6b hanya membandingkan jumlah BARIS TABEL, sehingga counter pernah basi
  # (tertulis 121 padahal bank berisi 149) tanpa terdeteksi — dicek di sini.
  # Patokan = skillCount di skills/manifest.json (angka otoritatif; ia memasukkan
  # skill di dalam folder arsip `.archive/`, yang tidak dihitung scan filesystem).
  local index_counter manifest_count expected_count
  index_counter=$(grep -oE '^> \*\*Status:\*\* [0-9]+' "$INDEX_FILE" 2>/dev/null | head -1 | grep -oE '[0-9]+$' || true)
  manifest_count=$(python3 -c "import json;print(json.load(open('$SKILLS_DIR/manifest.json'))['skillCount'])" 2>/dev/null || true)
  expected_count="${manifest_count:-$total_skills}"
  if [ -z "$index_counter" ]; then
    warn "Baris counter INDEX.md tidak ditemukan (pola: '> **Status:** N ✅ Aktif')"
    rec "→ Tambahkan baris counter di INDEX.md"
  elif [ "$index_counter" -eq "$expected_count" ]; then
    pass "Counter INDEX.md sinkron ($index_counter skill${manifest_count:+ — dari manifest})"
  else
    warn "Counter INDEX.md: $index_counter skill, seharusnya $expected_count${manifest_count:+ (manifest)} — mismatch!"
    rec "→ Perbarui baris counter INDEX.md menjadi $expected_count"
  fi

  # ── 6c: Cek duplikasi / konflik naming
  local name_check_file
  name_check_file=$(mktemp)
  local dup_found=false
  while IFS= read -r -d '' sk; do
    local rel="${sk#$SKILLS_DIR/}"
    local skill_name
    # Basename direktori skill — mendukung subkategori (mlops/inference/<skill>).
    # `cut -d/ -f2` dulu melaporkan "inference" muncul 2x (false positive konflik).
    skill_name=$(basename "$(dirname "$rel")")
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
    audit_count=$($TIMEOUT_BIN 30 python3 "$NIUMINATION/scripts/skill-audit.py" --count 2>/dev/null || echo "?")
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

  # ── 8a: Cek apakah server MC berjalan (modern: apex-ui Next.js :3000)
  local mc_health
  mc_health=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 --max-time 5 "$MC_URL/" 2>/dev/null || echo "000")
  mc_health="${mc_health:0:3}"  # Trim to 3 chars (curl may repeat digits on some macOS versions)

  if [ "$mc_health" = "000" ]; then
    info "Mission Control (apex-ui :3000) tidak aktif — bukan insiden"
    return
  fi
  pass "MC UI (apex-ui :3000): HTTP $mc_health"

  # API skill-monitor hidup di FastAPI legacy (:5200). Kalau mati, sisa seksi dilewati.
  local api_health
  api_health=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 --max-time 5 "$MC_API_URL/health" 2>/dev/null || echo "000")
  api_health="${api_health:0:3}"
  if [ "$api_health" = "000" ]; then
    info "Skill-monitor API (:5200, FastAPI legacy) tidak aktif — data skill via bank/up-eco"
    return
  fi
  pass "MC Skill API: HTTP $api_health"

  # ── 8b: Skill API — total skills & active
  local skills_json
  skills_json=$(curl -s --connect-timeout 3 --max-time 5 "$MC_API_URL/api/mc/skills" 2>/dev/null || echo "{}")
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
  stale_json=$(curl -s --connect-timeout 3 --max-time 5 "$MC_API_URL/api/mc/skills/stale" 2>/dev/null || echo "{}")
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
  conflict_json=$(curl -s --connect-timeout 3 --max-time 5 "$MC_API_URL/api/mc/skills/conflicts" 2>/dev/null || echo "{}")
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
  dash_code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 --max-time 5 "$MC_URL/" 2>/dev/null || echo "000")
  if [ "$dash_code" != "000" ]; then
    pass "Dashboard UI: HTTP $dash_code"
  else
    warn "Dashboard UI tidak bisa diakses"
    rec "→ Cek dashboard/ folder di niu-mission-control"
  fi

  # ── 8f: Skill usage stats (hari ini)
  local stats_json
  stats_json=$(curl -s --connect-timeout 3 --max-time 5 "$MC_API_URL/api/mc/skills/stats" 2>/dev/null || echo "{}")
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
  section "💬 Telegram Thread Status — Mission Control"
  python3 "$(dirname "$0")/telegram_threads.py" 2>/dev/null || warn "telegram_threads.py tidak tersedia"
}

# ── Phase 9a: Trio Awareness (Hermes · OpenCode) 🆕 ───────────────────
check_trio_awareness() {
  local from="${FROM:-hermes}"
  section "🔗 Trio Awareness — Called dari: $from"
  bash "$(dirname "$0")/trio-watch.sh" --from "$from" || warn "trio-watch.sh gagal dijalankan"
}

# ── Phase 10: MCP Status 🆕 ───────────────────────────────────────────────
check_mcp_status() {
  section "🔌 MCP Servers — Model Context Protocol"
  if ! command -v hermes >/dev/null 2>&1; then warn "hermes CLI tidak tersedia — skip MCP check"; return; fi
  local mcp_out
  mcp_out=$(hermes mcp list 2>&1 || echo "fail")
  if echo "$mcp_out" | grep -qi "fail\|error"; then warn "hermes mcp list gagal"; return; fi
  local enabled disabled total
  enabled=$(echo "$mcp_out" | grep -c "✓ enabled" 2>/dev/null || true)
  disabled=$(echo "$mcp_out" | grep -c "✗ disabled" 2>/dev/null || true)
  total=$((enabled + disabled))
  if [ "$total" -eq 0 ]; then warn "Tidak ada MCP server terdeteksi"; rec "→ hermes mcp add <name> <transport>"; return; fi
  pass "MCP: $total server ($enabled enabled, $disabled disabled)"
  echo "$mcp_out" | grep -E "✓ enabled|✗ disabled" | head -n 10 | while IFS= read -r line; do info "$line"; done
  if [ "$disabled" -gt 0 ]; then rec "→ Aktifkan MCP disabled: hermes mcp enable <name>"; fi
}

# ── Phase 11: Plugin Status 🆕 ────────────────────────────────────────────
check_plugin_status() {
  section "🧩 Plugins — Hermes Agent"
  if ! command -v hermes >/dev/null 2>&1; then warn "hermes CLI tidak tersedia — skip plugin check"; return; fi
  local plug_out
  plug_out=$(hermes plugins list 2>&1 || echo "fail")
  if echo "$plug_out" | grep -qi "^fail"; then warn "hermes plugins list gagal"; return; fi
  local total disabled enabled
  total=$(echo "$plug_out" | grep "│" | grep -c "enabled" || echo 0)
  disabled=$(echo "$plug_out" | grep "│" | grep -c "not enabled" || echo 0)
  enabled=$((total - disabled))
  if [ "$total" -eq 0 ]; then warn "Tidak ada plugin terdeteksi"; return; fi
  pass "Plugins: $enabled enabled, $disabled not enabled (bundled, total $total)"
  if [ "$enabled" -gt 0 ]; then echo "$plug_out" | grep "│" | grep "enabled" | grep -v "not enabled" | head -n 5 | while IFS= read -r line; do info "$line"; done; else info "Semua plugin not enabled — aktifkan via hermes plugins enable <name>"; fi
}

# ── Phase 12: Composio Status 🆕 ──────────────────────────────────────────
check_composio_status() {
  section "🔗 Composio — Tool Router"
  local has_cli=false has_py=false
  if command -v composio >/dev/null 2>&1; then has_cli=true; info "composio CLI: $(composio --version 2>&1 | head -n1)"; else info "composio CLI: tidak terinstal (pakai python package)"; fi
  # probe import sekali dengan timeout (import composio pernah hang >15s dan menggantung up-eco)
  local comp_ver=""
  if $TIMEOUT_BIN 25 python3 -c "import composio" 2>/dev/null; then
    has_py=true
    comp_ver=$($TIMEOUT_BIN 25 python3 -c 'import composio; print(composio.__version__)' 2>/dev/null || echo "?")
    info "composio python package: tersedia ($comp_ver)"
  else
    info "composio python package: tidak terdeteksi/timeout (import >25s)"
  fi
  if [ "$has_cli" = false ] && [ "$has_py" = false ]; then warn "Composio tidak terdeteksi (CLI & python)"; rec "→ pip install composio atau uv add composio"; return; fi
  # cek env (coba load dari ~/.hermes/.env jika belum di env)
  if [ -z "${COMPOSIO_API_KEY:-}" ] && [ -f "$HOME/.hermes/.env" ]; then COMPOSIO_API_KEY=$(grep -Eo 'COMPOSIO_API_KEY=.*' "$HOME/.hermes/.env" 2>/dev/null | cut -d= -f2 | tr -d ' "\"\r' | head -1); export COMPOSIO_API_KEY; fi
  if [ -n "${COMPOSIO_API_KEY:-}" ]; then pass "COMPOSIO_API_KEY: ter-set (len ${#COMPOSIO_API_KEY})"; else warn "COMPOSIO_API_KEY tidak di-set"; rec "→ export COMPOSIO_API_KEY atau set di vault/env"; fi
  info "Endpoint: https://backend.composio.dev/api/v3/tools (sessions.create)"
  # tampilkan toolkit/skills terhubung (connected_accounts) — timeout 40s agar tak gantung up-eco
  if [ -n "${COMPOSIO_API_KEY:-}" ] && [ "$has_py" = true ]; then
    local comp_out
    comp_out=$($TIMEOUT_BIN 40 python3 - << 'PY' 2>&1
import os
from collections import Counter
try:
    from composio import Composio
    c = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
    res = c.connected_accounts.list()
    items = getattr(res, 'items', [])
    if not items:
        print("EMPTY")
    else:
        # group by slug + status
        for it in items:
            slug = getattr(getattr(it, 'toolkit', None), 'slug', '?')
            status = getattr(it, 'status', getattr(getattr(it, 'state', None), 'status', '?'))
            # fallback: try it.status or data status
            if not status or status == '?':
                try: status = it.data.get('status', '?')
                except: pass
            uid = getattr(it, 'user_id', '') or getattr(it, 'userId', '') or ''
            # toolkit tools count via cache? skip, just slug
            print(f"{slug}|{status}|{uid}|{it.id}")
except Exception as e:
    print(f"ERR:{e}")
PY
)
    if echo "$comp_out" | grep -q "^ERR:"; then warn "Composio API: $comp_out"; rec "→ cek COMPOSIO_API_KEY / jaringan"; 
    elif [ -z "$comp_out" ]; then warn "Composio API: timeout (>40s) — SDK tidak respons"; rec "→ cek jaringan / reinstall composio (pip3 install --force-reinstall composio)";
    elif echo "$comp_out" | grep -q "^EMPTY"; then warn "Composio: tidak ada connected account"; rec "→ hubungkan via Composio dashboard / c.toolkits.authorize()";
    else
      local total active expired
      # grep -c exit 1 saat 0 match → guard || true (set -e mematikan script tanpa ini)
      total=$(echo "$comp_out" | grep -c "|" || true)
      active=$(echo "$comp_out" | grep -c "|ACTIVE|" || true)
      expired=$(echo "$comp_out" | grep -c "|EXPIRED|" || true)
      pass "Connected: $total account ($active ACTIVE, $expired EXPIRED)"
      # tampilkan ACTIVE dulu, lalu non-ACTIVE (guard exit-code: pipeline kosong tidak boleh bunuh script via set -e)
      local act_rows nonact_rows
      act_rows=$(echo "$comp_out" | grep "|ACTIVE|" | head -n 10 || true)
      nonact_rows=$(echo "$comp_out" | grep -v "|ACTIVE|" | head -n 10 || true)
      while IFS='|' read -r slug status uid cid; do
        [ -z "$slug" ] && continue
        # pendekkan uid panjang (UUID/conn-id) agar 1 baris tetap rapi
        local uid_disp="$uid"
        [ "${#uid_disp}" -gt 20 ] && uid_disp="${uid_disp:0:17}…"
        if [ -n "$uid" ]; then info "  ✅ $slug — ACTIVE — user:$uid_disp ($cid)"; else info "  ✅ $slug — ACTIVE ($cid)"; fi
      done <<< "$act_rows"
      while IFS='|' read -r slug status uid cid; do
        [ -z "$slug" ] && continue
        info "  ⚠️  $slug — $status ($cid)"
      done <<< "$nonact_rows"
      # ringkasan toolkit unik
      local uniq_active uniq_all
      uniq_active=$(echo "$comp_out" | grep "|ACTIVE|" | cut -d'|' -f1 | sort -u | paste -sd ',' - | sed 's/,/, /g')
      uniq_all=$(echo "$comp_out" | cut -d'|' -f1 | sort -u | paste -sd ',' - | sed 's/,/, /g')
      [ -n "$uniq_active" ] && info "Toolkit ACTIVE: $uniq_active"
      info "Toolkit semua: $uniq_all"
    fi
  fi
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
  local dirty_expected_count=0
  local dirty_expected_files=0
  local expected_list=""
  # Repo yang WAJAR kotor (19 Sep 2026). Berubah harian tanpa perlu tindakan:
  # brain/ = catatan harian, archive/ = cadangan arsip. Tetap DITAMPILKAN agar tidak ada
  # perubahan tersembunyi, tetapi sebagai info — tidak dihitung sebagai perlu tindakan
  # dan tidak masuk daftar Rekomendasi. Repo lain tetap fail + masuk Rekomendasi.
  local EXPECTED_DIRTY=("brain" "archive/")
  while IFS= read -r repo; do
    local rel
    rel=${repo#$NIUMINATION/}
    local dirty_files
    dirty_files=$(cd "$repo" && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [ "$dirty_files" -gt 0 ]; then
      local is_expected=0 pat
      for pat in "${EXPECTED_DIRTY[@]}"; do
        case "$rel" in
          "$pat"|"$pat"*) is_expected=1 ;;
        esac
      done
      if [ "$is_expected" -eq 1 ]; then
        info "(wajar kotor) $rel — $dirty_files file(s)"
        dirty_expected_count=$((dirty_expected_count + 1))
        dirty_expected_files=$((dirty_expected_files + dirty_files))
        expected_list="$expected_list $rel($dirty_files)"
      else
        fail "$rel — $dirty_files file(s) dirty"
        rec "→ $rel: commit & push ($dirty_files files)"
        dirty_count=$((dirty_count + 1))
      fi
    fi
  # Perbaikan 19 Sep 2026: klausa "-not -path '*/\..*'" mengecualikan SEMUA direktori .git
  # (setiap jalur .git memuat "/."), sehingga sweep selalu kosong dan selalu melaporkan
  # "Semua repos clean". Terbukti via bash -x: loop 0 iterasi. Klausa itu dihapus;
  # node_modules tetap dikecualikan dan hasil diurutkan agar stabil.
  done < <(find "$NIUMINATION" -maxdepth 3 -name ".git" -type d -not -path "*/node_modules/*" -exec dirname {} \; 2>/dev/null | sort || true)
  # Perbaikan 19 Sep 2026: "[ ... ] && pass" mengembalikan status 1 saat ada repo kotor,
  # dan di bawah "set -e" itu MEMATIKAN sisa laporan tepat setelah sweep mulai bekerja.
  if [ "$dirty_count" -eq 0 ]; then
    pass "Tidak ada repo yang perlu tindakan"
  else
    rec "→ $dirty_count repo kotor — commit & push per repo (lihat daftar di atas)"
  fi
  if [ "$dirty_expected_count" -gt 0 ]; then
    info "Wajar kotor (info saja): $dirty_expected_count repo / $dirty_expected_files berkas —$expected_list"
  else
    pass "Tidak ada repo wajar-kotor"
  fi

  # ── Phase 3: Folder asing ──
  check_unknown_folders

  # ── Phase 4: BACKLOG sync ──
  check_backlog_sync

  # ── Phase 5: GitHub Pages ──
  check_gh_pages

  # ── Phase 5a: Vercel — probe riil vs registry 🆕 ──
  check_vercel

  # ── Phase 5b: GitHub Pull Requests 🆕 ──
  check_gh_prs

  # ── Phase 6: Skill Bank Integrity 🆕 ──
  check_skill_bank
  check_lightfix

  # ── Phase 6c: SOUL Drift Guard ──
  check_soul_drift

  # ── Phase 7: Skill Sync Status 🆕 ──
  check_skill_sync

  # ── Phase 8: Mission Control Dashboard 🆕 ─────────────────────────────────
  check_mission_control

  # ── Phase 9: Telegram Thread Status 🆕 ────────────────────────────────────
  check_telegram_threads

  # ── Phase 9a: Trio Awareness (Hermes · OpenCode) 🆕 ───────────────────
  # 🔧 FIX: semua output trio-watch ke STDERR — supaya stdout (phase lain) tidak terpotong di Telegram
  check_trio_awareness
  echo "" 2>&1
  # ── Phase 9b: Gaya Jawab Guard (anti bertele-tele) ───────────────────────
  # Catatan: guard gaya jawab sudah dijalankan di akhir check_mission_control()
  # (tidak ada fungsi check_verbosity terpisah — panggilan lama menyebabkan error 127)

  # ── Phase 10: MCP Status ──
  check_mcp_status

  # ── Phase 11: Plugin Status ──
  check_plugin_status

  # ── Phase 12: Composio Status ──
  check_composio_status

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

  if [ -x "$NIUMINATION/scripts/9router-sync.sh" ]; then echo "[up-eco] 9router-sync..."; "$NIUMINATION/scripts/9router-sync.sh" 2>&1 | tail -n 2; cnt=$(python3 -c "import json,os; p=os.path.expanduser('~/.cache/niumination/9router-models.json'); print(len(json.load(open(p)).get('data',[])) if os.path.exists(p) else '?')" 2>/dev/null || echo "?"); echo "[up-eco] 9router: $cnt models"; fi
  header
  printf "${BOLD}Selesai: ${NOW}${NC}\n"
}

ROOT="$NIUMINATION"  # legacy compat (older callers reference $ROOT)

main "$@"
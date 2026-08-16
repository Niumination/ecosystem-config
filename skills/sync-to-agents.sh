#!/bin/bash
# ============================================================================
# sync-to-agents.sh — Layer 2: Sync Skill Bank ke Semua Agent
# ============================================================================
# Path:    ~/Desktop/Niumination/skills/sync-to-agents.sh
# Source:  ~/Desktop/Niumination/skills/ (bank pusat — single source of truth)
# Target:  ~/.jcode/skills/        → Jcode flat structure
#          ~/.hermes/skills/       → Hermes domain structure (local)
#          /Volumes/HermesAgent/   → Hermes USB domain structure (portable)
#          AGENTS.md               → DOX injection (skill registry update)
#
# Safety:  Non-destructive (copy/add only, never delete)
#          mkdir-based lock (macOS compatible)
#          Dry-run mode (pass --dry-run)
# ============================================================================

set -euo pipefail

# ── Config ──────────────────────────────────────────────────────────────────
# Resolve real user home (Hermes env may set HOME to cache path)
_REAL_HOME="$HOME"
if [ ! -d "$_REAL_HOME/Desktop/Niumination/skills" ]; then
  if [ -d "/Users/${USER:-zaryu}/Desktop/Niumination/skills" ]; then
    _REAL_HOME="/Users/${USER:-zaryu}"
  fi
fi
BANK_DIR="$_REAL_HOME/Desktop/Niumination/skills"
JCODE_DIR="$_REAL_HOME/.jcode/skills"
HERMES_DIR="$_REAL_HOME/.hermes/skills"
HERMES_USB_DIR="/Volumes/HermesAgent/HermesAgentUSB/data/skills"
AGENTS_MD="$_REAL_HOME/Desktop/Niumination/AGENTS.md"
LOCK_DIR="$_REAL_HOME/Desktop/Niumination/.sync-lock"
LOG_FILE="$_REAL_HOME/Desktop/Niumination/.sync-log"

DRY_RUN=false
VERBOSE=false

# ── Flags ────────────────────────────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --verbose) VERBOSE=true ;;
    --help)
      echo "Usage: $0 [--dry-run] [--verbose]"
      echo ""
      echo "  --dry-run    Preview changes without copying"
      echo "  --verbose    Show detailed per-file output"
      exit 0
      ;;
  esac
done

# ── Lock (mkdir-based) ───────────────────────────────────────────────────────
LOCK_PARENT="$(dirname "$LOCK_DIR")"
mkdir -p "$LOCK_PARENT" 2>/dev/null || true
if mkdir "$LOCK_DIR" 2>/dev/null; then
  trap 'rm -rf "$LOCK_DIR"' EXIT
else
  echo "⚠️  Lock aktif — sync sedang berjalan. Skip."
  exit 0
fi

# ── Helpers ──────────────────────────────────────────────────────────────────
log()  { echo "[$(date '+%H:%M:%S')] $*"; }
vlog() { $VERBOSE && echo "  $*" || true; }

# ── Sync satu skill (SELURUH folder — references/scripts/assets ikut) ────────
# Non-destruktif: copy/add only, never delete. Skip jika target lebih baru.
# Prioritas rsync (tersedia di macOS); fallback cp -R -u (portable).
sync_skill_dir() {
  local src_dir="$1"    # skills/<domain>/<skill>/  (bank)
  local tgt_dir="$2"    # <target>/[<domain>/]<skill>/  (agent)
  if [ ! -d "$src_dir" ]; then return 1; fi

  if command -v rsync &>/dev/null; then
    rsync -a -u --quiet "$src_dir/" "$tgt_dir/"
  else
    mkdir -p "$tgt_dir"
    cp -R -u "$src_dir/." "$tgt_dir/"
  fi
}

# ── Hitung jumlah file pendukung (total file - SKILL.md) ─────────────────────
count_skill_files() {
  find "$1" -type f -not -name ".DS_Store" | wc -l | tr -d ' '
}

# ── Verify target vs manifest (jika manifest ada) ─────────────────────────────
verify_target() {
  local target="$1" label="$2" structure="$3"
  if [ -f "$BANK_DIR/manifest.json" ]; then
    if python3 "$BANK_DIR/../scripts/skill-manifest.py" --verify-target "$target" --structure "$structure" 2>/dev/null; then
      log "   ✅ $label: verifikasi hash LULUS"
    else
      log "   ⚠️  $label: verifikasi hash GAGAL (lihat detail di atas)"
    fi
  else
    log "   ℹ️  $label: manifest.json belum ada — verifikasi dilewati"
  fi
}

# ── Tulis lockfile di target (source + bundleHash) ────────────────────────────
write_lockfile() {
  local target="$1" label="$2"
  if [ -f "$BANK_DIR/manifest.json" ]; then
    if python3 "$BANK_DIR/../scripts/skill-manifest.py" --lockfile "$target" 2>/dev/null; then
      log "   ✅ $label: skills-lock.json ditulis"
    else
      log "   ⚠️  $label: lockfile gagal ditulis"
    fi
  fi
}

# ── Sync SEMUA skill ke satu target ───────────────────────────────────────────
# structure: flat  = <target>/<skill>/        (Jcode)
#            domain = <target>/<domain>/<skill>/ (Hermes, USB)
sync_target() {
  local target="$1" label="$2" structure="$3"
  local copied=0
  log "→ $label: $target"

  while IFS= read -r src_file; do
    rel_path="${src_file#$BANK_DIR/}"        # software-development/ponytail-core/SKILL.md
    domain_dir="${rel_path%%/*}"             # software-development
    skill_dir="${rel_path#*/}"               # ponytail-core/SKILL.md
    skill_name="${skill_dir%/*}"             # ponytail-core
    src_skill_folder="$BANK_DIR/$domain_dir/$skill_name"

    if [ "$structure" = "flat" ]; then
      tgt="$target/$skill_name"
      display="$skill_name"
    else
      tgt="$target/$domain_dir/$skill_name"
      display="$domain_dir/$skill_name"
    fi

    if $DRY_RUN; then
      echo "  [COPY] → $label: $display"
      ((copied++)) || true
    else
      sync_skill_dir "$src_skill_folder" "$tgt"
      ((copied++)) || true
      vlog "  ✅ $skill_name ($(count_skill_files "$tgt") file)"
    fi
  done <<< "$SKILL_FILES"

  log "   ↑ $label: $copied skill disinkronkan"
  if ! $DRY_RUN; then
    verify_target "$target" "$label" "$structure"
    write_lockfile "$target" "$label"
  fi
}

# ── Verify bank exists ──────────────────────────────────────────────────────
if [ ! -d "$BANK_DIR" ]; then
  echo "❌ Bank skill tidak ditemukan: $BANK_DIR"
  exit 1
fi

SKILL_FILES=$(find "$BANK_DIR" -maxdepth 3 -name 'SKILL.md' | sort)
SKILL_COUNT=$(echo "$SKILL_FILES" | wc -l | tr -d ' ')

if [ "$SKILL_COUNT" -eq 0 ]; then
  echo "⚠️  Tidak ada SKILL.md di bank. Skip sync."
  exit 0
fi

log "📦 Bank: $SKILL_COUNT skill ditemukan"
$DRY_RUN && log "🏁 DRY RUN — tidak ada perubahan nyata"

# ── 1. Sync ke Jcode (flat structure) ───────────────────────────────────────
sync_target "$JCODE_DIR" "Jcode" "flat"

# ── 2. Sync ke Hermes (domain structure) ────────────────────────────────────
sync_target "$HERMES_DIR" "Hermes" "domain"

# ── 2b. Sync ke Hermes USB (domain structure) ───────────────────────────────
if [ -d "$HERMES_USB_DIR" ]; then
  sync_target "$HERMES_USB_DIR" "Hermes USB" "domain"
else
  log "   ⚠️  Hermes USB path not found: $HERMES_USB_DIR (skipped)"
fi

# ── 3. Update AGENTS.md — Skill Registry ────────────────────────────────────
if ! $DRY_RUN; then
  # Build the skill registry block
  REGISTRY_START="<!-- SKILL_REGISTRY_START -->"
  REGISTRY_END="<!-- SKILL_REGISTRY_END -->"

  registry_block="$REGISTRY_START
### 🧠 Bank Skill — Active Registry (auto-synced)

| Skill | Domain | File | Source | Description |
|-------|--------|-----:|--------|-------------|"

  while IFS= read -r src_file; do
    rel_path="${src_file#$BANK_DIR/}"
    domain_dir="${rel_path%%/*}"
    skill_dir="${rel_path#*/}"
    skill_name="${skill_dir%/*}"

    # Extract description from frontmatter (handle both quoted and folded YAML)
    desc=$(awk '/^description:/ { 
      if ($2 ~ /^"/) { 
        # Quoted: description: "..."
        sub(/^description: "/, ""); sub(/"$/, ""); print
      } else if ($2 == ">") {
        # Folded: description: > ... (take next non-empty, non-indented line)
        getline nextline
        while (nextline ~ /^$/ || nextline ~ /^  /) { 
          if (nextline !~ /^$/) { gsub(/^  /, ""); print nextline; break }
          getline nextline
        }
      } else {
        # Normal: description: text...
        sub(/^description: /, ""); print
      }
    }' "$src_file" 2>/dev/null || echo "—")
    registry_block+="
| \`$skill_name\` | $domain_dir | $(count_skill_files "$BANK_DIR/$domain_dir/$skill_name") | Bank Pusat | $desc |"
  done <<< "$SKILL_FILES"

  registry_block+="

_Last sync: $(date '+%Y-%m-%d %H:%M:%S')_"

  # Check if AGENTS.md has skill registry section
  if grep -q "$REGISTRY_START" "$AGENTS_MD" 2>/dev/null; then
    # Use Python to build registry and replace between markers
    python3 << 'PYEOF'
import os
from datetime import datetime

def _resolve_home():
    """Resolve real user home — handles Hermes env where HOME != /Users/user."""
    home = os.path.expanduser('~')
    if os.path.isdir(os.path.join(home, 'Desktop', 'Niumination', 'skills')):
        return home
    user = os.environ.get('USER', 'zaryu')
    alt = f'/Users/{user}'
    if os.path.isdir(os.path.join(alt, 'Desktop', 'Niumination', 'skills')):
        return alt
    return home

_real_home = _resolve_home()
bank = os.path.join(_real_home, 'Desktop', 'Niumination', 'skills')
agents = os.path.join(_real_home, 'Desktop', 'Niumination', 'AGENTS.md')

# Build registry table
rows = []
for root, dirs, files in os.walk(bank):
    if 'SKILL.md' in files:
        sk = os.path.join(root, 'SKILL.md')
        rel = os.path.relpath(sk, bank)  # e.g. software-development/ponytail-core/SKILL.md
        parts = rel.split('/')
        domain = parts[0]
        skill = parts[1]
        # Extract description
        desc = '—'
        with open(sk, 'r') as f:
            in_frontmatter = False
            folded_lines = []
            for line in f:
                if line.startswith('---'):
                    in_frontmatter = not in_frontmatter
                    if folded_lines:
                        desc = ' '.join(folded_lines)
                        break
                    continue
                if in_frontmatter and line.startswith('description:'):
                    val = line[len('description:'):].strip()
                    if val.startswith('"') and val.endswith('"'):
                        desc = val[1:-1]
                        break
                    elif val == '>':
                        # folded scalar: collect all subsequent indented lines
                        for l2 in f:
                            if l2.startswith('  '):
                                folded_lines.append(l2.strip())
                            elif l2.startswith('---'):
                                break
                            else:
                                break
                        if folded_lines:
                            desc = ' '.join(folded_lines)
                        break
                    else:
                        desc = val
                        break
        file_count = sum(len(files) for _, _, files in os.walk(root))
        rows.append((skill, domain, desc, file_count))

registry = '### 🧠 Bank Skill — Active Registry (auto-synced)\n\n'
registry += '| Skill | Domain | File | Source | Description |\n'
registry += '|-------|--------|-----:|--------|-------------|\n'
for skill, domain, desc, fc in sorted(rows):
    registry += f'| `{skill}` | {domain} | {fc} | Bank Pusat | {desc} |\n'
registry += f'\n_Last sync: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_\n'

# Replace between markers
with open(agents, 'r') as f:
    content = f.read()

marker_start = '<!-- SKILL_REGISTRY_START -->'
marker_end = '<!-- SKILL_REGISTRY_END -->'
s = content.find(marker_start)
e = content.find(marker_end, s)

if s >= 0 and e >= 0:
    e += len(marker_end)
    before = content[:s]
    after = content[e:]
    content = before + marker_start + '\n' + registry + '\n' + marker_end + '\n' + after
    with open(agents, 'w') as f:
        f.write(content)
    print('AGENTS.md registry updated')
else:
    print('ERROR: markers not found')
PYEOF
    log "   ↑ AGENTS.md: skill registry diperbarui"
  else
    # Append before footer
    # Find the last --- line before the footer
    footer_line=$(grep -n "^> \\*\\*Dibuat:" "$AGENTS_MD" | head -1 | cut -d: -f1)
    if [ -n "$footer_line" ]; then
      insert_line=$((footer_line - 2))
      head -n "$insert_line" "$AGENTS_MD" > /tmp/agents-new.md
      echo "" >> /tmp/agents-new.md
      echo "$registry_block" >> /tmp/agents-new.md
      echo "" >> /tmp/agents-new.md
      echo "$REGISTRY_END" >> /tmp/agents-new.md
      echo "" >> /tmp/agents-new.md
      echo "---" >> /tmp/agents-new.md
      tail -n +$((insert_line + 1)) "$AGENTS_MD" >> /tmp/agents-new.md
      mv /tmp/agents-new.md "$AGENTS_MD"
      log "   ↑ AGENTS.md: skill registry ditambahkan"
    else
      log "   ⚠️  Footer AGENTS.md tidak ditemukan, registry tidak ditambahkan"
    fi
  fi
fi

# ── 4. Write log ─────────────────────────────────────────────────────────────
if ! $DRY_RUN; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync selesai: $SKILL_COUNT skill × 3 target (Jcode/Hermes/USB) + AGENTS.md ✅" >> "$LOG_FILE"
  log "✅ Sync selesai — $SKILL_COUNT skill disinkronkan ke Jcode/Hermes/USB"
  
  # Notify mission-control (fire-and-forget, non-blocking)
  if command -v curl &>/dev/null; then
    # Seed each skill as loaded
    while IFS= read -r src_file; do
      rel_path="${src_file#$BANK_DIR/}"
      skill_dir="${rel_path#*/}"
      skill_name="${skill_dir%/*}"
      curl -s -X POST "http://localhost:5200/api/mc/skills/event" \
        -H "Content-Type: application/json" \
        -d '{"skill_name":"'"$skill_name"'","agent":"sync-to-agents.sh","event_type":"load"}' \
        --connect-timeout 2 --max-time 3 >/dev/null 2>&1 &
    done <<< "$SKILL_FILES"
    # Also record sync meta-event
    curl -s -X POST "http://localhost:5200/api/mc/skills/event" \
      -H "Content-Type: application/json" \
      -d '{"skill_name":"__sync__","agent":"system","event_type":"sync","metadata":{"source":"sync-to-agents.sh","files_synced":'$SKILL_COUNT'}}' \
      --connect-timeout 2 --max-time 3 >/dev/null 2>&1 &
  fi
else
  log "🏁 DRY RUN selesai — $SKILL_COUNT skill akan disinkronkan"
fi

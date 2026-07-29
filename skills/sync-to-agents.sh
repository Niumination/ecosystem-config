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

# ── 1. Sync ke Jcode ────────────────────────────────────────────────────────
jcode_copied=0
jcode_skipped=0

log "→ Jcode  : $JCODE_DIR"

while IFS= read -r src_file; do
  # Extract: skills/<domain>/<skill-name>/SKILL.md
  rel_path="${src_file#$BANK_DIR/}"           # software-development/ponytail-core/SKILL.md
  domain_dir="${rel_path%%/*}"                # software-development
  skill_dir="${rel_path#*/}"                  # ponytail-core/SKILL.md
  skill_name="${skill_dir%/*}"                # ponytail-core
  skill_file="${skill_dir##*/}"               # SKILL.md

  # Jcode: ~/.jcode/skills/<skill-name>/SKILL.md (flat, no domain)
  jcode_target="$JCODE_DIR/$skill_name"
  jcode_file="$jcode_target/$skill_file"

  if [ -f "$jcode_file" ] && [ "$src_file" -ot "$jcode_file" ]; then
    ((jcode_skipped++)) || true
    vlog "  ⏭  $skill_name (up to date)"
    continue
  fi

  if $DRY_RUN; then
    echo "  [COPY] → Jcode: $skill_name"
    ((jcode_copied++)) || true
  else
    mkdir -p "$jcode_target"
    cp "$src_file" "$jcode_file"
    ((jcode_copied++)) || true
    vlog "  ✅ $skill_name"
  fi
done <<< "$SKILL_FILES"

log "   ↑ Jcode: $jcode_copied copied, $jcode_skipped up-to-date"

# ── 2. Sync ke Hermes ───────────────────────────────────────────────────────
hermes_copied=0
hermes_skipped=0

log "→ Hermes : $HERMES_DIR"

while IFS= read -r src_file; do
  rel_path="${src_file#$BANK_DIR/}"
  domain_dir="${rel_path%%/*}"
  skill_dir="${rel_path#*/}"
  skill_name="${skill_dir%/*}"
  skill_file="${skill_dir##*/}"

  # Hermes: ~/.hermes/skills/<domain>/<skill-name>/SKILL.md (same structure)
  hermes_target="$HERMES_DIR/$domain_dir/$skill_name"
  hermes_file="$hermes_target/$skill_file"

  if [ -f "$hermes_file" ] && [ "$src_file" -ot "$hermes_file" ]; then
    ((hermes_skipped++)) || true
    vlog "  ⏭  $domain_dir/$skill_name (up to date)"
    continue
  fi

  if $DRY_RUN; then
    echo "  [COPY] → Hermes: $domain_dir/$skill_name"
    ((hermes_copied++)) || true
  else
    mkdir -p "$hermes_target"
    cp "$src_file" "$hermes_file"
    ((hermes_copied++)) || true
    vlog "  ✅ $domain_dir/$skill_name"
  fi
done <<< "$SKILL_FILES"

log "   ↑ Hermes: $hermes_copied copied, $hermes_skipped up-to-date"

# ── 2b. Sync ke Hermes USB (portable) ──────────────────────────────────────────
usb_copied=0
usb_skipped=0

if [ -d "$HERMES_USB_DIR" ]; then
  log "→ Hermes USB: $HERMES_USB_DIR"

  while IFS= read -r src_file; do
    rel_path="${src_file#$BANK_DIR/}"
    domain_dir="${rel_path%%/*}"
    skill_dir="${rel_path#*/}"
    skill_name="${skill_dir%/*}"
    skill_file="${skill_dir##*/}"

    usb_target="$HERMES_USB_DIR/$domain_dir/$skill_name"
    usb_file="$usb_target/$skill_file"

    if [ -f "$usb_file" ] && [ "$src_file" -ot "$usb_file" ]; then
      ((usb_skipped++)) || true
      vlog "  ⏭  $domain_dir/$skill_name (up to date)"
      continue
    fi

    if $DRY_RUN; then
      echo "  [COPY] → Hermes USB: $domain_dir/$skill_name"
      ((usb_copied++)) || true
    else
      mkdir -p "$usb_target"
      cp "$src_file" "$usb_file"
      ((usb_copied++)) || true
      vlog "  ✅ $domain_dir/$skill_name"
    fi
  done <<< "$SKILL_FILES"

  log "   ↑ Hermes USB: $usb_copied copied, $usb_skipped up-to-date"
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

| Skill | Domain | Source | Description |
|-------|--------|--------|-------------|"

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
| \`$skill_name\` | $domain_dir | Bank Pusat | $desc |"
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
        rows.append((skill, domain, desc))

registry = '### 🧠 Bank Skill — Active Registry (auto-synced)\n\n'
registry += '| Skill | Domain | Source | Description |\n'
registry += '|-------|--------|--------|-------------|\n'
for skill, domain, desc in sorted(rows):
    registry += f'| `{skill}` | {domain} | Bank Pusat | {desc} |\n'
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
  total="$((jcode_copied + hermes_copied + usb_copied))"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sync selesai: Jcode +${jcode_copied}, Hermes +${hermes_copied}, USB +${usb_copied}, AGENTS.md ✅" >> "$LOG_FILE"
  log "✅ Sync selesai — $total perubahan"
  
  # Notify mission-control (fire-and-forget, non-blocking)
  if command -v curl &>/dev/null; then
    curl -s -X POST "http://localhost:5200/api/mc/skills/event" \
      -H "Content-Type: application/json" \
      -d '{"skill_name":"__sync__","agent":"system","event_type":"sync","metadata":{"source":"sync-to-agents.sh","files_synced":'$total'}}' \
      --connect-timeout 2 --max-time 3 >/dev/null 2>&1 &
  fi
else
  log "🏁 DRY RUN selesai — $(($jcode_copied + $hermes_copied)) perubahan akan terjadi"
fi

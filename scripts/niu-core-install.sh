#!/usr/bin/env bash
# Pasang CORE Niumination ke mesin zaryu.
# Tidak mengeksekusi hermes config jika binary tidak ada.
# Tidak menonaktifkan rtk-rewrite. Tidak mematikan drift guard.
set -euo pipefail

NIU="${NIU:-/Users/zaryu/Desktop/Niumination}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
HERMES="${HERMES_HOME:-$HOME/.hermes}"

ok() { printf '  [OK] %s\n' "$*"; }
info() { printf '  [--] %s\n' "$*"; }
warn() { printf '  [!!] %s\n' "$*" >&2; }

echo "=== niu-core-install  SRC=$SRC  NIU=$NIU ==="

if [[ ! -d "$NIU" ]]; then
  warn "root $NIU tidak ada. Paket tetap lengkap di $SRC"
  warn "di Mac zaryu: export NIU=/Users/zaryu/Desktop/Niumination && bash scripts/niu-core-install.sh"
  NIU_MISSING=1
else
  NIU_MISSING=0
fi

# 1. Core tree
if [[ "$NIU_MISSING" -eq 0 ]]; then
  mkdir -p "$NIU/core/runtime" "$NIU/core/ledger/sessions" "$NIU/core/ledger/decisions" \
           "$NIU/core/ledger/handoffs" "$NIU/core/templates" "$NIU/scripts" \
           "$NIU/agents/_shared" "$NIU/docs/audit" "$NIU/brain/ops"
  mkdir -p "$NIU/core"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude runtime/fence.json --exclude runtime/HANDOFF.md "$SRC/core/" "$NIU/core/"
  else
    cp -a "$SRC/core/." "$NIU/core/"
    rm -f "$NIU/core/runtime/fence.json" "$NIU/core/runtime/HANDOFF.md" 2>/dev/null || true
  fi
  ok "core/ tersalin"

  # AGENTS.md slim — backup raksasa dulu
  if [[ -f "$NIU/AGENTS.md" ]]; then
    bytes=$(wc -c < "$NIU/AGENTS.md" | tr -d ' ')
    if [[ "${bytes:-0}" -gt 20000 ]]; then
      cp -n "$NIU/AGENTS.md" "$NIU/docs/audit/AGENTS.md.pre-slim-53k.bak" 2>/dev/null || \
        cp "$NIU/AGENTS.md" "$NIU/docs/audit/AGENTS.md.pre-slim-53k.bak"
      cp "$NIU/core/AGENTS.slim.md" "$NIU/AGENTS.md"
      ok "AGENTS.md 53KB di-backup dan diganti slim"
    else
      info "AGENTS.md sudah kecil ($bytes B) — tidak ditimpa otomatis"
    fi
  else
    cp "$NIU/core/AGENTS.slim.md" "$NIU/AGENTS.md"
    ok "AGENTS.md slim dipasang"
  fi

  cp -f "$SRC/scripts/"niu-*.py "$SRC/scripts/"niu-*.sh "$NIU/scripts/" 2>/dev/null || true
  cp -f "$SRC/scripts/niu_corelib.py" "$NIU/scripts/"
  chmod +x "$NIU/scripts/"niu-*.sh "$NIU/scripts/"niu-*.py || true
  ok "scripts tersalin"

  cp -f "$SRC/agents/_shared/"*.md "$NIU/agents/_shared/" 2>/dev/null || true
  cp -f "$SRC/CORE-REPAIR-2026-08-18.md" "$NIU/docs/audit/" 2>/dev/null || true
  cp -f "$SRC/ERRATA-AUDIT-V1.md" "$NIU/docs/audit/" 2>/dev/null || true
fi

# 2. Hermes identity + hooks + plugin
mkdir -p "$HERMES/plugins" "$HERMES/agent-hooks" "$HERMES/hooks" "$HERMES/memories"
if [[ ! -f "$HERMES/SOUL.md" ]]; then
  cp "$SRC/hermes/SOUL.md" "$HERMES/SOUL.md"
  ok "SOUL.md baru"
else
  if ! grep -q "nemotron-3-ultra-free\|opencode-zen/nemotron-3-ultra-free" "$HERMES/SOUL.md" 2>/dev/null; then
    cp "$HERMES/SOUL.md" "$HERMES/SOUL.md.bak-before-niu-core"
    cp "$SRC/hermes/SOUL.md" "$HERMES/SOUL.md"
    ok "SOUL.md diganti (backup .bak-before-niu-core)"
  else
    info "SOUL.md sudah berisi kebijakan Zen — tidak ditimpa"
  fi
fi
if [[ ! -f "$HERMES/memories/USER.md" ]]; then
  mkdir -p "$HERMES/memories"
  cp "$SRC/hermes/USER.md" "$HERMES/memories/USER.md"
  ok "USER.md dipasang"
fi

mkdir -p "$HERMES/plugins/niu-core-fence" "$HERMES/agent-hooks"
if command -v rsync >/dev/null 2>&1; then
  rsync -a "$SRC/hermes/plugins/niu-core-fence/" "$HERMES/plugins/niu-core-fence/"
  rsync -a "$SRC/hermes/agent-hooks/" "$HERMES/agent-hooks/"
else
  cp -a "$SRC/hermes/plugins/niu-core-fence/." "$HERMES/plugins/niu-core-fence/"
  cp -a "$SRC/hermes/agent-hooks/." "$HERMES/agent-hooks/"
fi
chmod +x "$HERMES/agent-hooks/"niu-*.py || true
ok "plugin + agent-hooks"

# 3. Seal
if [[ "$NIU_MISSING" -eq 0 ]]; then
  bash "$SRC/scripts/niu-seal-core.sh" || true
fi

# 4. Hermes CLI — best effort
if command -v hermes >/dev/null 2>&1; then
  info "mencoba pin model + plugin (gagal = lanjut manual)"
  hermes config set model.default nemotron-3-ultra-free || true
  hermes config set model.provider opencode-zen || true
  hermes config set cron.model nemotron-3-ultra-free || true
  hermes config set cron.model_provider opencode-zen || true
  # JANGAN sentuh model_drift_guard
  info "fallback: se-provider free tier Zen (big-pickle / nemotron-3-ultra-free / hy3-free) — rapikan manual:"
  info "  hermes fallback ls"
  info "  hapus juan-router / 9router / huancheng dari chain"
  info "  hermes fallback add --provider opencode-zen --model hy3-free"
  info "enable plugin: tambah niu-core-fence ke plugins.enabled (biarkan rtk-rewrite)"
else
  info "binary hermes tidak di PATH — konfigurasi manual, lihat configs/"
fi

echo
echo "selanjutnya:"
echo "  1. Satukan 5 thread Telegram ke opencode-zen/nemotron-3-ultra-free (bukan 9router zoo)"
echo "  2. python3 ${NIU}/scripts/niu-handoff.py --status"
echo "  3. python3 ${NIU}/scripts/niu-doc-capture.py --note bootstrap"
echo "  4. Baca core/CONSTITUTION.md dan core/VISION.md — itu hukumnya"
echo
echo "JANGAN: fallback ke 9router/juan/gemini"
echo "JANGAN: hidupkan 4 karakter agen"
echo "JANGAN: hermes config set cron.model_drift_guard false"

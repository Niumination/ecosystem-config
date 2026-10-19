#!/bin/bash
# =============================================================================
# eco-guard-backup.sh — wrapper cron NON-AGENT untuk backup Hermes harian
# =============================================================================
# Job Hermes cron memakai no_agent=true: scheduler menjalankan skrip ini dan
# mengirim stdout-nya apa adanya. Tanpa LLM -> tanpa biaya token, tanpa kuota model.
#
# Kenapa wrapper ini ada (bukan --script eco-guard.sh langsung):
#   eco-guard.sh memparse perintah lewat `case "${1:-}"` — tanpa argumen ia
#   hanya menampilkan usage lalu exit 2, sehingga tidak ada backup yang
#   terjadwal. Wrapper ini memaksa subperintah `backup`.
#
# Pemakaian manual:
#   bash ~/.hermes/scripts/eco-guard-backup.sh              # backup sekarang
#   ECO_BACKUP_DIR=/tmp/uji bash ~/.hermes/scripts/eco-guard-backup.sh
# =============================================================================

set -u

GUARD="${ECO_GUARD_SCRIPT:-$HOME/.hermes/scripts/eco-guard.sh}"
if [[ ! -f "$GUARD" ]]; then
  echo "GALAT: eco-guard.sh tidak ditemukan di $GUARD" >&2
  exit 2
fi

# Cron mewarisi PATH minimal — pastikan hermes terjangkau (pola dr-restore-sync.sh).
for d in "$HOME/.local/bin" "$HOME/src/hermes-agent/.venv/bin" /usr/local/bin /opt/homebrew/bin; do
  [[ -d "$d" ]] && case ":$PATH:" in *":$d:"*) ;; *) PATH="$d:$PATH" ;; esac
done
export PATH

command -v hermes >/dev/null 2>&1 || { echo "GALAT: perintah hermes tidak ada (PATH=$PATH)" >&2; exit 2; }

# Teruskan hanya subperintah backup; ECO_BACKUP_DIR / ECO_BACKUP_KEEP bisa dioverride.
exec bash "$GUARD" backup

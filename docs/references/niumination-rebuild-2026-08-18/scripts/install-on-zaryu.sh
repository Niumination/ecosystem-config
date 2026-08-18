#!/usr/bin/env bash
# Salin paket rekonstruksi ke mesin zaryu dan pasang launchd.
# Jalankan SETELAH men-copy folder niumination-rebuild ke MacBook.
set -euo pipefail

NIU="${NIU:-/Users/zaryu/Desktop/Niumination}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"

if [[ ! -d "$NIU" ]]; then
  echo "root tidak ada: $NIU" >&2
  exit 2
fi

mkdir -p "$NIU/scripts/launchd" "$NIU/brain/ops" "$NIU/agents/_shared" "$NIU/docs/audit"

cp -f "$SRC/scripts/niu-quick-wins.sh" "$NIU/scripts/"
cp -f "$SRC/scripts/niu-health-probe.py" "$NIU/scripts/"
cp -f "$SRC/scripts/niu-self-heal.sh" "$NIU/scripts/"
cp -f "$SRC/scripts/launchd/"*.plist "$NIU/scripts/launchd/"
cp -f "$SRC/agents/_shared/"*.md "$NIU/agents/_shared/"
cp -f "$SRC/prompts/pengawas-self-heal.md" "$NIU/agents/_shared/"
cp -f "$SRC/AUDIT-REKONSTRUKSI-HERMES-2026-08-18.md" "$NIU/docs/audit/"
cp -f "$SRC/configs/config.yaml.target-excerpt.yaml" "$NIU/docs/audit/"

chmod +x "$NIU/scripts/niu-quick-wins.sh" "$NIU/scripts/niu-self-heal.sh" "$NIU/scripts/niu-health-probe.py"

# launchd
mkdir -p "$HOME/Library/LaunchAgents"
cp -f "$NIU/scripts/launchd/niu.missioncontrol.plist" "$HOME/Library/LaunchAgents/"
cp -f "$NIU/scripts/launchd/niu.healthprobe.plist" "$HOME/Library/LaunchAgents/"

for label in niu.missioncontrol niu.healthprobe; do
  launchctl bootout "gui/${UID}/${label}" 2>/dev/null || true
  launchctl bootstrap "gui/${UID}" "$HOME/Library/LaunchAgents/${label}.plist"
  launchctl enable "gui/${UID}/${label}"
  launchctl kickstart -k "gui/${UID}/${label}"
  echo "launchd ${label} aktif"
done

echo
echo "selanjutnya:"
echo "  bash $NIU/scripts/niu-quick-wins.sh"
echo "  python3 $NIU/scripts/niu-health-probe.py --heal"
echo "jangan: hermes config set cron.model_drift_guard false"

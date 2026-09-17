#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="."; APPLY=false; ALLOWLIST=""
ECO="${ECO_DIR:-$HOME/Desktop/Niumination}"; HH="${HERMES_HOME:-$HOME/.hermes}"
while [[ $# -gt 0 ]]; do case "$1" in
  --root) ROOT="$2"; shift 2;; --apply) APPLY=true; shift;;
  --allowlist) ALLOWLIST="$2"; shift 2;; *) echo "opsi tidak dikenal: $1" >&2; exit 2;; esac; done
[[ -d "$ROOT" ]] || { echo "GAGAL: root tidak ada: $ROOT" >&2; exit 2; }
LIST="$(mktemp)"; trap 'rm -f "$LIST"' EXIT
grep -v '^[[:space:]]*$' "$ALLOWLIST" > "$LIST" || true
BERKAS=$(wc -l < "$LIST" | tr -d ' ')
[[ "$BERKAS" -eq 0 ]] && { echo "GAGAL: allowlist kosong" >&2; exit 1; }
TF=0; THI=0
while IFS= read -r rel; do
  f="$ROOT/$rel"; [[ -f "$f" ]] || continue
  n=$(grep -c -e '{{HOME}}' -e '{{ECO}}' -e '{{HERMES_HOME}}' "$f" 2>/dev/null || true); [[ -z "$n" ]] && n=0
  if [[ "$n" -gt 0 ]]; then TF=$((TF+1)); THI=$((THI+n)); [[ "$APPLY" == true ]] && sed -i \
    -e "s|{{HERMES_HOME}}|$HH|g" -e "s|{{ECO}}|$ECO|g" -e "s|{{HOME}}|$HOME|g" "$f"; fi
done < "$LIST"
echo "berkas kena: $TF, placeholder: $THI"
# status: perlu substitusi? hanya jika THI>0
[[ "$THI" -eq 0 ]] && { echo "TIDAK ADA placeholder yang perlu diganti — selesai (bukan kegagalan)"; exit 0; }
sisa=$({ grep -rl -e '{{HOME}}' -e '{{ECO}}' -e '{{HERMES_HOME}}' "$ROOT" 2>/dev/null || true; } | grep -v -e '.git/' -e 'subst-paths' | wc -l | tr -d ' ')
[[ "$APPLY" == true && "$sisa" -gt 0 ]] && { echo "GAGAL: $sisa placeholder tersisa" >&2; exit 1; }
exit 0

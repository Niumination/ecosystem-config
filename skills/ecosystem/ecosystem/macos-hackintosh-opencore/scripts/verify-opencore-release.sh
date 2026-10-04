#!/bin/bash
# Prove an installed EFI's OpenCore version by SHA-256 against the official
# release ZIP, report per-file provenance, and validate the config with the
# ocvalidate binary from that SAME zip.
#
# Usage:
#   verify-opencore-release.sh <version> [efi-oc-dir]
#
#   version      e.g. 1.0.8  (tag has NO RELEASE- prefix)
#   efi-oc-dir   defaults to every mounted FAT32 EFI/OC found via diskutil
#
# Read-only: downloads land in a temp dir, nothing under /Volumes is written.

set -uo pipefail

VER="${1:-}"
EFIDIR="${2:-}"

command -v curl >/dev/null || { echo "FATAL: curl not found"; exit 127; }
command -v shasum >/dev/null || { echo "FATAL: shasum not found"; exit 127; }

[ -n "$VER" ] || { echo "usage: $0 <version> [efi-oc-dir]"; exit 2; }

# ---- locate the EFI/OC directory ------------------------------------------
if [ -z "$EFIDIR" ]; then
  while read -r part; do
    [ -n "$part" ] || continue
    mnt=$(diskutil info "$part" 2>/dev/null | awk -F': *' '/Mount Point/{print $2; exit}')
    case "$mnt" in
      ""|-) continue ;;
      *) [ -d "$mnt/EFI/OC" ] && EFIDIR="$mnt/EFI/OC" ;;
    esac
  done < <(diskutil list -plist 2>/dev/null | grep -A1 'PartitionType' | grep -o '[a-zA-Z0-9]*disk[0-9]*s[0-9]*' | sort -u)
fi

[ -n "$EFIDIR" ] && [ -d "$EFIDIR" ] || {
  echo "FATAL: no EFI/OC dir found; mount the EFI volume in Finder and pass it as argv[2]"
  exit 3
}
echo "== target EFI: $EFIDIR"

# ---- fetch the release ------------------------------------------------------
TMP=$(mktemp -d /tmp/ocrel.XXXXXX) || exit 1
trap 'rm -rf "$TMP"' EXIT
ZIP="$TMP/oc-$VER.zip"
API="https://api.github.com/repos/acidanthera/OpenCorePkg/releases/tags/$VER"

echo "== resolving release $VER"
URL=$(curl -sL "$API" | python3 -c '
import json,sys
try:
    for a in json.load(sys.stdin).get("assets",[]):
        if a["name"] == f"OpenCore-{sys.argv[1]}-RELEASE.zip":
            print(a["browser_download_url"]); break
except Exception: pass' "$VER")

# A guessed tag returns a JSON body with HTTP 200, so the asset-name check above
# is the real guard -- do not trust a successful curl exit code here.
[ -n "$URL" ] || { echo "FATAL: no OpenCore-$VER-RELEASE.zip asset (check tag: no RELEASE- prefix)"; exit 4; }

echo "== downloading"
curl -sL -o "$ZIP" "$URL" || exit 1
file "$ZIP" | grep -qi 'zip archive' || { echo "FATAL: not a zip"; exit 5; }

curl -sL -o "$TMP/x.zip" "$URL" 2>/dev/null
unzip -q -o "$ZIP" -d "$TMP/x" || { echo "FATAL: unzip failed"; exit 6; }
REL="$TMP/x/X64/EFI/OC"
[ -d "$REL" ] || { echo "FATAL: X64/EFI/OC absent from release"; exit 7; }

# ---- hash proof -------------------------------------------------------------
echo
echo "== SHA-256: installed vs release $VER"
sha() { shasum -a 256 "$1" 2>/dev/null | awk '{print $1}'; }
VERDICT="unknown"
for f in OpenCore.efi OpenRuntime.efi; do
  a=$(sha "$EFIDIR/$f"); b=$(sha "$REL/$f")
  if [ -z "$a" ]; then printf '  %-20s MISSING installed\n' "$f"
  elif [ "$a" = "$b" ]; then printf '  %-20s MATCH  %s\n' "$f" "$a"; VERDICT="match"
  else printf '  %-20s DIFFER installed=%s release=%s\n' "$f" "${a:0:12}.." "${b:0:12}.."; VERDICT="mixed"
  fi
done
echo "  --> version proof: $VERDICT"

# ---- per-driver provenance --------------------------------------------------
echo
echo "== drivers: provenance vs release"
for p in "$EFIDIR"/Drivers/*.efi; do
  n=$(basename "$p")
  if [ -f "$REL/Drivers/$n" ] && [ "$(sha "$p")" = "$(sha "$REL/Drivers/$n")" ]; then
    printf '  %-22s from release\n' "$n"
  else
    age=$(stat -f '%Sm' -t '%Y-%m-%d' "$p" 2>/dev/null)
    printf '  %-22s NOT from release (built %s)\n' "$n" "${age:-?}"
    # names changed across releases -> name the successor
    for r in "$REL"/Drivers/*.efi; do
      rn=$(basename "$r")
      case "$n$rn" in *HfsPlus*OpenHfsPlus*|*OpenHfsPlus*HfsPlus*) printf '       release calls it: %s\n' "$rn";; esac
    done
  fi
done

# ---- same-zip schema validation --------------------------------------------
OCV=$(find "$TMP/x/Utilities" -name ocvalidate -type f | head -1)
[ -n "$OCV" ] || { echo; echo "ocvalidate absent from release; skip"; exit 0; }
chmod +x "$OCV" 2>/dev/null
echo
echo "== ocvalidate from the SAME zip as the release"
"$OCV" --version 2>&1 | head -1 | sed 's/^/  validator: /'
for cfg in "$EFIDIR/config.plist" "$EFIDIR/oldConfig.plist"; do
  [ -f "$cfg" ] || continue
  printf '  %-22s ' "$(basename "$cfg")"
  out=$("$OCV" "$cfg" 2>&1)
  if printf '%s' "$out" | grep -qi 'No issues found'; then echo 'No issues found.'
  else echo "ISSUES:"; printf '%s\n' "$out" | grep -iE 'error|illegal|invalid' | sed 's/^/    /' | head -15; fi
done
echo
echo "Version proof and schema validity are SEPARATE claims. Quote both."
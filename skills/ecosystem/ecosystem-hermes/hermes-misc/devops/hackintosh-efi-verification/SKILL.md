---
name: hackintosh-efi-verification
description: Verify OpenCore EFI version, config, drivers, sha.
---

# Hackintosh EFI verification

Read-only verification of an OpenCore EFI tree on macOS. Every claim about version comes from a checksum or from the validator's own output — never from inference.

## Rules

1. **An ocvalidate only validates the OpenCore version it was built for.** Running a 0.8.8 or 1.0.7 ocvalidate against a 1.0.8 config produces fake "Missing key" errors that look like config corruption. Check the match first.
2. **OpenCore's version is not readable from the binary.** `strings OpenCore.efi` yields only unrelated version tuples and the literal placeholder `REL-XXX-YYYY-MM-DD`. Prove the release by SHA-256 against the official zip.
3. **OCAT rewrites `config.plist` but does not upgrade driver `.efi` files.** After an OCAT update, `OpenCore.efi` and most drivers become current while one stale driver stays. Audit every driver separately; do not infer from `OpenCore.efi`.
4. **The OCAT `.app` bundle and `~/.ocat/Database` can be different releases.** `ocvalidate` in `~/.ocat/Database/mac/` may be current while `/Applications/OCAuxiliaryTools.app/Contents/MacOS/Database/mac/` is a year older. Compare `CFBundleShortVersionString` of the app against the validator.
5. **A restart does not repair a stale file on disk.** If a driver's mtime is old, a reboot changes nothing. Say so plainly instead of letting the user believe a reboot will fix it.
6. **Never write to the internal EFI to "fix" a version mismatch** before a verified external backup exists and a USB boot has been proven.

## Procedure

### Locate the EFI volume

The EFI partition is usually unnamed and lands in `/Volumes`, not `/Volumes/EFI`:

```bash
diskutil info disk0s1 | grep -E 'Volume Name|Mounted|Disk Size'
mount | grep disk0s1
ls /Volumes/
```

If the user mounts it in Finder, the mount point is the volume name — often `/Volumes/NO NAME`. That is the reliable path.

If `sudo mount` fails because no interactive terminal is available, ask the user to mount it in Finder rather than fighting for sudo. `sudo -n` will not work either.

### Prove the OpenCore release

The release tag has no `RELEASE-` prefix — it is `1.0.8`, not `RELEASE-1.0.8`:

```bash
curl -s https://api.github.com/repos/acidanthera/OpenCorePkg/releases/tags/1.0.8 > rel.json
python3 -c "
import json
d=json.load(open('rel.json'))
for a in d['assets']:
    if 'RELEASE' in a['name']: print(a['browser_download_url'])
"
curl -sL -o oc.zip <url-from-above>
unzip -q oc.zip -d ex

shasum -a 256 'EFI/OC/OpenCore.efi' ex/X64/EFI/OC/OpenCore.efi
shasum -a 256 'EFI/OC/Drivers/OpenRuntime.efi' ex/X64/EFI/OC/Drivers/OpenRuntime.efi
```

Identical checksums prove provenance. A mismatch means mixed packages — do not boot it as-is.

### Pick the matching ocvalidate

```bash
'/path/to/ocvalidate' --version      # prints "only compatible with OpenCore version X.Y.Z"
```

That line is the validator's own compatibility claim. Trust it over any assumption.

Prefer the copy shipped in the official release zip (`ex/Utilities/ocvalidate/ocvalidate`, flat path — not a subdirectory) so the validator and the EFI come from one source.

### Validate

```bash
ocvalidate 'EFI/OC/config.plist'
```

"No issues found" plus a matching version line is the pass condition. `Serialisation returns N errors` means missing keys for that schema version.

Compare against any `oldConfig.plist` too — OCAT leaves one behind, and it often differs from the live config in ways that matter.

### Audit driver freshness

Compare each active driver against the release, by mtime and by hash:

```bash
stat -f '%Sm %N' -t '%Y-%m-%d %H:%M' EFI/OC/Drivers/*.efi
for d in EFI/OC/Drivers/*.efi; do
  b=$(basename "$d")
  if [ -f "ex/X64/EFI/OC/Drivers/$b" ]; then
    cmp -s "$d" "ex/X64/EFI/OC/Drivers/$b" && echo "$b SAME" || echo "$b STALE"
  else
    echo "$b NOT-IN-RELEASE (renamed upstream?)"
  fi
done
```

In 1.0.8 `HfsPlus.efi` was renamed to `OpenHfsPlus.efi`. An old-name file can still mount HFS+, so a stale driver is a hygiene issue, not a boot blocker — report it that way instead of raising a false alarm.

To see which files changed today:

```bash
find 'EFI' -newermt 'YYYY-MM-DD 00:00' -type f | grep -v '\._'
```

## Tooling notes

- `find ~/` and `find /Users/<name>` can exceed a 180 s timeout on this machine. Use `mdfind -name '<name>'` or scope `find` to a known subtree.
- Filter macOS resource-fork noise out of listings: `grep -v '\._'`, and strip `total N` lines when counting directory entries.
- `df -h /System/Volumes/Data` is the number that matters for a macOS upgrade, not the total APFS container size.
- Quote paths containing spaces (`/Volumes/NO NAME`) or the shell will silently split them.

## Reporting

- State the version claim and its evidence together: hash match, or the validator's own compatibility line.
- When a prior report in the same conversation was wrong, correct it plainly in one line, name the cause, and move on. Do not re-litigate.
- Separate "verified" from "cannot verify without sudo/USB" so the owner knows exactly what remains unproven.

## Bukti

Record commands and their output. For a release-provenance claim the minimum is two matching `shasum` lines plus the validator output naming the version.
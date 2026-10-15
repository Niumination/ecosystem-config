---
name: macos-hackintosh-opencore
trigger: "hackintosh, opencore, efi, macos upgrade"
description: "Use when upgrading Intel Hackintosh/OpenCore."
---

# macos-hackintosh-opencore

Use when working with Hackintosh/OpenCore on Intel macOS (upgrade macOS + OpenCore, EFI migration, boot issues). Class-level: verification-first, read-only before changes, USB-only testing, approval-gated destructive ops.

## Always-on rules

1. **Verification-first, read-only.** Never write EFI/internal disk before proving current state. Read config, kexts, ACPI, drivers read-only. If EFI cannot be mounted read-only (sudo interaktif), record limitation + fallback — never guess. An unlabelled FAT volume still mounts somewhere real: `diskutil info disk0s1` prints the actual mount point (often `/Volumes/NO NAME`, never `/Volumes/EFI`), so read that before concluding the EFI is unreadable.
2. **Handoff documents are a timestamp, not current state.** Re-measure every claim in a handoff or prior report before acting on it — the owner may have completed half the plan between sessions. Never repeat a handoff blocker as live until you have re-observed it yourself.
3. **Version = SHA-256 against the official release ZIP, never inference.** Download the release zip, hash `X64/EFI/OC/OpenCore.efi` + `OpenRuntime.efi`, compare against the installed EFI. Identical hash proves the exact version; a mismatch means mixed-release files that must be normalized. Binary strings do NOT embed the version (Acidanthera ships no version string) — quirk-shape inference is a guess and is recorded `UNCHECKED`. `scripts/verify-opencore-release.sh` does this end to end.
4. **Validator version must equal the target OpenCore version.** `ocvalidate` enforces the schema of its OWN release: a 1.0.7 binary run against a 1.0.8 config invents "illegal value" errors on fields the vendor still ships (e.g. `UEFI>Output>InitialMode`), and the run collapses into a phantom "corrupt config" verdict. Take `ocvalidate` from the SAME zip as the binaries under test — never from `~/.ocat`, `/Applications/OCAuxiliaryTools.app`, or a backup folder found on disk. Sanity check before reporting: if the validator flags a field the release defaults use, suspect validator/config mismatch first; a config that currently boots macOS is not schema-invalid.
5. **Driver filenames change between releases.** A stale-named driver keeps working while no longer matching the release it is paired with — config validity does not prove driver provenance. Hash every file in `EFI/OC/Drivers/` against the release zip and name the ones that are not from it (`HfsPlus.efi` became `OpenHfsPlus.efi`). Mixed pairs are the classic half-migration state.
6. **Check the target update before treating any prerequisite flag as required.** Run `softwareupdate -l` first. If the target build is already offered, a guide-mandated prerequisite (`revpatch=sbvmm` and friends) is already satisfied on this machine and its whole test phase is skipped, not planned.
7. **Space requirement scales with installer size, not a fixed floor.** Take the KiB figure from `softwareupdate -l`, multiply by ~3 for download + expand + swap + rollback snapshot, and require that headroom to remain AFTER the upgrade. Do not inflate a small update into a large fixed requirement, and do not demand more than the actual payload needs.
8. **Approval gate.** Resize EFI/partitions, edit EFI internal, replace ANY file under `EFI/`, run `softwareupdate --install`/OTA, or delete files = destructive/berisiko → require explicit approval ("gas", "kerjakan", "fix"). "Pelajari" = read-only report only.
9. **USB-first (crash-dummy).** Migrate OpenCore/config ONLY on USB first. Boot USB, validate full hardware (boot macOS+Windows, audio, Wi-Fi/Bluetooth/Ethernet, trackpad, brightness, sleep/wake, battery, shutdown, Recovery). Internal EFI unchanged until USB proven bootable + stable.
10. **One-change-at-a-time.** OC upgrade + kext bumps + macOS upgrade = separate phases. Validate `ocvalidate` 0 error on the USB config before any install.
11. **SIP/csr preserved; no destructive rm -rf on EFI.** Never lower SIP below the recorded `csr-active-config`, never run `csrutil disable`, never create a new SMBIOS identity (serial/UUID/MLB stay secret and unchanged) without approval. Copy/replace files safely, keep a checksummed backup before overwrite.

## Procedure (order)

### A. Verify read-only
1. `sw_vers` (macOS/build). 
2. `diskutil list` (EFI disk0s1 size/layout). 
3. `df -h /System/Volumes/Data` (free space). 
4. `nvram boot-args` (check revpatch). 
5. Read EFI backup (SHA/checksum). Mount EFI read-only if possible; if sudo interaktif blocks → record limitation + fallback (backup, diskutil info) — never guess.
6. `softwareupdate -l` early — if the target build is already offered, every guide-mandated prerequisite-flag test phase is already satisfied; skip it instead of planning it.
7. Prove OC version by SHA-256 against the official release zip (`scripts/verify-opencore-release.sh`), hashing `Drivers/` in the same pass. Never infer from binary strings or quirk shape.
8. Validate config with the `ocvalidate` binary from that SAME zip, and report the validator's version next to its verdict.
9. Check logs (`log show --predicate 'process=="softwareupdated"'` small window) — treat empty as "not captured" (do not claim failure).
10. List external USB, caches, installers.

### B. Prepare (approval required)
1. Free space to the figure derived in A.6–A.7 (list per-item candidates, confirm).
2. Prepare GPT/FAT32 USB >=8–16GB.
3. Download the OpenCore release ZIP and keep it for the whole session: both the `X64/EFI/OC` tree and `Utilities/ocvalidate/ocvalidate` come out of it. Release tags carry NO `RELEASE-` prefix (`1.0.8`, not `RELEASE-1.0.8`); take the asset URL from `https://api.github.com/repos/acidanthera/OpenCorePkg/releases/tags/<ver>` instead of guessing the download path.
4. Create second EFI backup + SHA-256 (separate location).
5. Measure actual EFI folder usage before proposing any resize — a migrated EFI that already fits its partition needs none (resize only if necessary + approved).

### C. Migrate on USB only
1. Copy OC+config to USB EFI. 
2. Run `ocvalidate 1.0.8` against USB config → 0 errors (fix schema). Manual review for Intel quirks. 
3. Boot USB → full hardware test matrix. 
4. Add `revpatch=sbvmm` on USB → test Software Update appearance (wait). Diagnose in order if missing. 
5. Only after stable + approved → copy validated OC to internal EFI (fresh backup first).

### D. Upgrade macOS
1. OTA via Software Update UI (preferred). Avoid `softwareupdate --install` pre-check incomplete. 
2. Verify boot macOS+Windows, all hardware post-upgrade.

## Pitfalls
- **A validator from the wrong release is worse than no validator.** Wrong-version `ocvalidate` output is the single most expensive failure mode here: it produces confident, specific, wrong verdicts. Verify the validator's own version before quoting its output.
- Confirm the target is really absent before planning a prerequisite-flag fix: `softwareupdate -l` is the check, and an already-offered build means the prerequisite is moot.
- GitHub release assets: query the API for `browser_download_url` instead of guessing tags — a wrong tag returns a JSON body with HTTP 200, so `-f` and exit-code checks do not catch it; verify the file is a zip.
- EFI partition size worries evaporate once you measure: a 4-driver + 24-kext tree fits ~50 MB, so a 100 MB EFI may need no resize at all. Measure before recommending surgery.
- Empty softwareupdated logs ≠ "no failure" (log rotation). Never claim.
- Binary strings omit OC version (Acidanthera) — SHA-256 against the release zip is the only proof.
- A hash-verified OpenCore build does NOT imply its config was validated: report version proof and schema validation as two separate claims with two separate pieces of evidence.
- Intel Comet Lake + UHD 620: test graphics/sleep/wake post-upgrade; kext bumps one-at-a-time.
- Keep UI changes separate from OC/kext/macOS changes.

## References
- `scripts/verify-opencore-release.sh` — SHA-256 proof of the installed OC release, per-driver provenance, and a same-zip `ocvalidate` run. One command, no guessing.
- `references/release-verification-and-validator-drift.md` — why version inference fails, the release-tag/API recipe, validator-drift failure modes (including renamed drivers and why a fixed space floor is wrong).
- Dortania OpenCore Install Guide (Intel); Acidanthera changelog (driver renames + quirk additions per release).
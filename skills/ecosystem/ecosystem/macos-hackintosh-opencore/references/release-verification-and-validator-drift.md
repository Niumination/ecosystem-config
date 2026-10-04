# OpenCore release verification and validator drift

Depth notes for the class of work "prove what OpenCore version an EFI actually
carries, and what its config actually means". Use with
`scripts/verify-opencore-release.sh`.

## Why version inference fails

Acidanthera ships OpenCore binaries with **no embedded version string**. Neither
`strings OpenCore.efi` nor any grep for `0.6.x` / `1.0.x` will identify the
build. Quirk-shape reasoning ("it has `UEFI.Quirks`, so it is 0.7-era") is an
inference from a schema that grew incrementally — usable as a weak hint, never
as proof, and always recorded `UNCHECKED`.

**The only proof is a hash match.** Download the release zip, hash the two
files that ship with the release (`X64/EFI/OC/OpenCore.efi`,
`OpenRuntime.efi`), and compare with the installed copies. Identical SHA-256
means the installed file IS that release byte for byte.

## Finding the release asset

Release tags carry **no `RELEASE-` prefix**: the tag is `1.0.8`, not
`RELEASE-1.0.8`. A wrong tag produces an HTTP 200 response whose body is a JSON
error object, so neither `curl -f` nor an exit-code check catches it — the file
lands on disk as JSON and only `file` reveals it.

Always resolve the URL through the API rather than composing it:

```bash
curl -s https://api.github.com/repos/acidanthera/OpenCorePkg/releases/tags/1.0.8 \
 | python3 -c 'import json,sys; [print(a["browser_download_url"]) for a in json.load(sys.stdin)["assets"] if a["name"].endswith("-RELEASE.zip")]'
```

## The ocvalidate version trap

`ocvalidate` validates against the schema of **its own release**. Point an
older binary at a newer config and it invents errors on fields the vendor still
ships:

- `UEFI>Output>InitialMode` — OC 1.0.x requires the string enum
  (`Auto`/`Text`/`Graphics`); older validators accept the raw integer, and a
  validator that expects an integer flags the correct string as illegal.
- `UEFI>Quirks>RaiseVariableCopyBufferPages`, and every quirk added after a
  release's cut-off, get reported as missing or unknown.

The output is confident and specific, which is what makes it expensive: it
reads as a broken config when the config is the thing the vendor ships. A
secondary tell is the failure cascade — serialisation errors stack up behind
the first bogus complaint, so one wrong-version report can produce a dozen.

**Rule:** take `ocvalidate` out of the same zip as the binaries under test. It
lives at `Utilities/ocvalidate/ocvalidate` inside the release and needs
`chmod +x`. Never use a copy from `~/.ocat`, an app bundle
(`/Applications/OCAuxiliaryTools.app/Contents/MacOS/Database/mac/`), or an old
backup folder — those age silently out of date and are the normal cause of a
phantom "corrupt config" verdict.

Sanity check before reporting any validator complaint: if the flagged field uses
the value the release's own sample config uses, the validator is wrong, not the
config. A config that currently boots macOS is not schema-invalid.

## Driver renames across releases

Filenames changed in 1.0.8:

| older name | 1.0.8 name |
|---|---|
| `HfsPlus.efi` | `OpenHfsPlus.efi` |

A stale-named driver still works — OpenCore keeps loading the legacy name — so
the machine boots fine and nothing signals the mismatch. It is only visible by
hashing `Drivers/` against the release. This is the classic half-migrated state:
`OpenCore.efi` and `OpenRuntime.efi` updated, one driver left behind.

Always hash **all** of `Drivers/`, not just the two core binaries, and treat a
per-file mismatch as a reportable finding even when the system boots.

## Handoffs age

A handoff or prior session report is a **timestamp**, not current state. The
owner may have completed phases between sessions, and every blocker it lists may
already be resolved. Re-measure each claim before acting, and re-check the
prerequisite flags a guide insists on — if the target build already appears in
`softwareupdate -l`, the whole prerequisite-flag phase is moot and must be
dropped from the plan instead of planned and executed.

## Space requirements

Take the installer size from `softwareupdate -l` (`Size: <KiB>`), multiply by
~3 for download + expand + swap + rollback snapshot, and require that headroom
to remain free *after* the upgrade. A fixed floor like "20 GB required" is
wrong in both directions — it blocks a small update on a nearly-full disk and
understates a large one.

For the EFI partition itself, measure the actual folder usage before proposing
a resize. A tree of ~4 drivers and ~24 kexts is well under 60 MB, so a 100 MB
EFI partition frequently needs no resize at all.
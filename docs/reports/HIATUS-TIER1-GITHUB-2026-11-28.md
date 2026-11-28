# GitHub Archive — Tier 1 (2026-11-28)

## Scope

Eight owner-owned, non-fork repositories were archived on GitHub. Selection criteria:
no push for more than 365 days, no local working folder, no Vercel project, no active
reference in `BACKLOG.md`, `docs/registry/project-catalog.md`,
`docs/registry/deployment-status.md`, or `docs/registry/halted-repos.txt`, and zero
open issues or pull requests.

## Archived repositories

| Repository | Previous visibility | Idle days | Git size | Tag |
|---|---|---:|---:|---|
| `AnachonisticHypr` | PUBLIC | 728 | 135 MB | `v-hiatus-2026-11-28` |
| `hive-dotfiles` | PUBLIC | 689 | 134 MB | `v-hiatus-2026-11-28` |
| `Zaryu-Dotfiles` | PRIVATE | 655 | 464 MB | `v-hiatus-2026-11-28` |
| `zaryu-dev` | PRIVATE | 571 | 30 MB | `v-hiatus-2026-11-28` |
| `zaryu.dev` | PRIVATE | 571 | 28 MB | `v-hiatus-2026-11-28` |
| `ZaryuHive` | PUBLIC | 550 | 78 MB | `v-hiatus-2026-11-28` |
| `Online-Ryu_OBS` | PRIVATE | 421 | 28 MB | `v-hiatus-2026-11-28` |
| `niu-speedtest` | PUBLIC | 377 | 104 KB | `v-hiatus-2026-11-28` |

All eight are now `archived: true` and `private: true`. Making a previously public
repository private closes the public surface before the read-only archive is applied.

## Backup

A full mirror clone of every repository was stored at:

`~/Backups/hibernasi-tier1-2026-11-28/`

- 8 bare mirror repositories, 184 files, 939,971,716 bytes
- SHA-256 manifest: `MANIFEST.sha256.json`
- Verification: 184 checked, 184 matched, 0 missing, 0 damaged, 0 extra
- Permissions: directories `700`, files `600`

No local project folder was deleted because none of the eight repositories had a
working folder inside the ecosystem. The GitHub history remains the authoritative
copy; the mirrors are the local recovery copy.

## Restore

```bash
# 1. Unlock the repository
gh api -X PATCH repos/Niumination/<repo> -f archived=false
gh api -X PATCH repos/Niumination/<repo> -f private=false   # only if public again is desired

# 2. Verify backup integrity
python3 ~/.hermes/skills/ecosystem/ecosystem-hibernation/scripts/generate-manifest.py \
  ~/Backups/hibernasi-tier1-2026-11-28 --verify

# 3. Restore from GitHub or from the mirror
git clone git@github.com:Niumination/<repo>.git
# or: git clone ~/Backups/hibernasi-tier1-2026-11-28/<repo>.git
```

## Note

The first tag push attempt failed because a mirror remote rejects an explicit refspec.
Each affected repository was temporarily unarchived, the tag was pushed with
`-c remote.origin.mirror=false`, then the repository was archived again. Final remote
tag verification succeeded for all eight repositories.

## Bukti

- `gh api repos/Niumination/<repo> --jq '{archived,private}'` → `{"archived":true,"private":true}` for all eight
- `git ls-remote --tags ... refs/tags/v-hiatus-2026-11-28` → tag SHA present for all eight
- `git --git-dir=<mirror> fsck --full --no-reflogs` → `0` for all eight
- `generate-manifest.py --verify` → `184 cocok · 0 hilang · 0 rusak · 0 tambahan`
- `df -h /System/Volumes/Data` → `4.9 Gi` free after backup

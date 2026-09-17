# Hermes home backup & restore — the L1 layer

Use the CLI, not `cp`. `hermes backup` and `hermes import` are first-party; scripting a copy of HERMES_HOME by
hand loses the three properties below and can produce a corrupt snapshot.

## The command pair

```bash
hermes backup -o backup.zip -l "<label>"   # zip of HERMES_HOME
hermes import backup.zip [--force]          # restore
```

What the implementation gets right (`hermes_cli/backup.py`) — worth knowing because it is exactly what a
hand-rolled copy gets wrong:

- SQLite files are snapshotted with `sqlite3.backup()`, so a running gateway does not yield a torn DB.
- Excluded: `-wal`/`-shm` sidecars, `*.pyc`/`*.pyo`, `models/`, `runtimes/`, `node/`, `.backup.lock`,
  `gateway.pid`, `cron.pid`, `state.db.pre-update-emergency-*`.
- Deliberately **kept**: `skills/.archive/` (curator-archived skills stay restorable) and skill directories
  matching `hermes-agent` inside `skills/`.
- On import, runtime files are skipped: `gateway_state.json`, `gateway.pid`, `cron.pid`, `gateway.lock`,
  `processes.json`.

Measured on a full Niumination host: **201 MB, 2,565 entries, 560 MB uncompressed, ~60 s**.

## Verify what is in it — from the artifact, not from the description

```bash
unzip -l backup.zip | grep -cF '.env'        # credential layer
unzip -l backup.zip | grep -cF 'auth.json'
unzip -l backup.zip | grep -cF 'skills/'     # authored skills
unzip -l backup.zip | grep -cF 'jobs.json'   # cron definitions
unzip -l backup.zip | grep -cF 'sessions/'   # session history
unzip -v backup.zip | grep -E 'state.db|bin/'   # per-entry compression ratio
```

Grep the name **unanchored** (`grep -cF`) — an anchored pattern like `grep "$name$"` reports false negatives
because the listing prints size and timestamp columns before the name, and a false "missing credential" is the
finding a user acts on.

Unanchored matching then bites the other way: **never trust a substring hit for a name that is a prefix of
another.** `SOUL.md` matches `SOUL.md.v1.bak-2026-08-30`, `.env` matches `.env.example`. Decide presence on whole
basenames taken from the name column, e.g. `unzip -Z1 backup.zip | awk -F/ '{print $NF}' | sort -u`.

Confirmed present after a real run: `.env`, `auth.json`, `custom_persona.json`, `self-schema.json`,
`memory_tiering.json`, `cron/jobs.json`, `kanban.db`, `projects.db`, `install_id`, `channel_directory.json`,
`memories/`, `platforms/`, `plugins/`, `kanban/`, `skills/` (1,076 entries), `sessions/` (201 entries), `state.db`.
**`SOUL.md` is not one of them** — the substring hit that made it look present came from a dated backup whose name
starts with it. See the drill section below for what that costs.

## Trim the regenerables before shipping

The default archive carries rebuildable bulk that dominates its size:

| Entry | Size | Verdict |
|---|---|---|
| `bin/uv`, `bin/tirith`, `bin/uvx` | 49 MB + 35 MB + 0.3 MB | tool binaries, re-downloaded |
| `firefox-profile-backup/` | 86 MB | browser profile = a re-login |
| `cache/`, `logs/` | ~63 MB | regenerate |
| `state.db` | 242 MB raw → **98 MB compressed** | keep — it is the history |

```bash
cp backup.zip clean.zip
zip -q -d clean.zip 'bin/*' 'firefox-profile-backup/*' 'cache/*' 'logs/*' '*.log'
ls -lh clean.zip        # 201 MB -> 116 MB on the reference host
```

## Size against the destination limit

116 MB still exceeds the host's **100 MB per-file hard reject** (50 MB triggers a warning), and `state.db` alone is
98 MB of that. Two honest options:

```bash
# keep full history, split the archive
split -b 45m clean.zip part-        # parts under the warning threshold survive the 100 MB reject
cat part-* > clean.zip              # reassemble on restore

# or reduce the DB itself
sqlite3 state.db "VACUUM INTO 'state-trimmed.db'"   # after dropping tables that do not matter
```

Decide this while planning. Discovering it on the first push wastes the approval cycle.

## Restore order for this layer

1. **Key material first** — SSH key + `.ssh/config` + dotfiles repo before anything that clones. The private
   backup repo needs the key it is supposed to contain, so the key also exists outside it (cloud copy / paper).
2. `hermes import clean.zip --force`.
3. **Re-point identity symlinks** — `~/.hermes/SOUL.md` may point into the dotfiles repo; without the target the
   agent starts on default identity rather than failing loudly.
4. **Re-apply local patches** — a fork's local commits often live on a `backup-*` branch, not `main`; export them
   as `.patch` files in the backup so the restore does not depend on remembering a branch name.
5. Restore the sibling layers the gateway and ecosystem depend on (`~/.9router`, other agent CLI configs).
6. Verify: skill count matches, `readlink ~/.hermes/SOUL.md` target exists, `git log -1 --oneline` shows the patch
   commits, `hermes doctor` clean, cron jobs listed.

## Drill it into a throwaway HOME before trusting any of it

Importing into the real `~/.hermes` proves nothing repeatable; importing into a fake home proves everything and
costs one command. It is the cheapest test in this class of work, and it is what found the failure below.

```bash
hermes backup -o /tmp/drill.zip -l drill
mkdir -p /tmp/drill-home
HERMES_HOME=/tmp/drill-home/.hermes hermes import /tmp/drill.zip
# count with an interpreter, not a shell alias: `find` is aliased to `fd` on some hosts and `fd` rejects -name,
# returning 0 rows with exit 0 — a green-looking number that is pure artifact
python3 -c "from pathlib import Path; print(len(list(Path('/tmp/drill-home').rglob('SKILL.md'))))"
sqlite3 /tmp/drill-home/.hermes/state.db "PRAGMA integrity_check;"      # -> ok
sqlite3 /tmp/drill-home/.hermes/state.db "SELECT COUNT(*) FROM sessions;"
HOME=/tmp/drill-home HERMES_HOME=/tmp/drill-home/.hermes hermes doctor  # the app must recognise the restored home
```

Reference-host result: 202 skills, `.env` with 26 keys, `cron/` 76 files, `memories/` 4, `kanban/` 115,
`sessions/` 188, `state.db` integrity `ok` (76 sessions), `hermes doctor` healthy.

### What only the drill could catch: identity silently reset to the shipped default

`backup.py` skips symlinks, and a stow-managed `~/.hermes/SOUL.md` **is** a symlink. The archive therefore contains
no `SOUL.md` at all, and `import` writes the built-in template instead. Measured: restored file 667 B of generic
identity text vs the owner's 3,167 B — different hashes, no error, import reported success.

- Treat identity files as **out-of-band**: put the canonical `SOUL.md` in the backup repo itself and symlink or copy
  it after import; never rely on it surviving the archive.
- Verify identity by **hash against the live source**, after resolving the live path (`readlink` first — it may be a
  symlink whose *target* is the real content). The same applies to every path that is a symlink on the source host.

### Three import behaviours that change the restore order

`hermes import` restores configuration and data only — its own output says so:

1. **Application code is not in the archive**: *"The hermes-agent codebase was not included in the backup. If this
   is a fresh install, run: `hermes update`"* → installing the app is a separate prerequisite step.
2. **No service is installed**: *"leaving the gateway service alone… To start a gateway for this home, run:
   `hermes gateway install`"* → registering the service (launchd / systemd user unit / Task Scheduler) is its own step.
3. **Target runtime state is preserved, not overwritten**: `gateway.lock`, `gateway_state.json`, `processes.json`.

### Restoring over a machine that already has Hermes (the normal case)

A replacement machine usually gets the app installed first, so `~/.hermes` already exists when the archive arrives.
Measured on that path:

| Action | Result |
|---|---|
| `hermes import backup.zip` (no flag) onto a configured home | `Warning: Target directory already has Hermes configuration … Continue? [y/N]` → `Aborted.`, **exit 1**, nothing restored — `.env`, `state.db`, `cron/jobs.json` all still absent |
| `hermes import backup.zip --force` | `Import complete: 2588 files restored in 10.2s`, exit 0; `.env`, `state.db` (integrity `ok`), `cron/jobs.json`, `memories/`, `kanban.db` all present |
| Local files the archive does not contain | **kept** — 203 skills = 202 restored + 1 local dummy |
| Files the import overwrites | **no automatic copy taken** |

Three consequences for the restore script:

1. **Always pass `--force`.** An automated restore otherwise stops at the prompt and leaves a default-identity home in
   place — the exact silent-reset failure the drill exists to prevent, now happening on the machine that matters.
2. **Import merges; it does not mirror.** Leftovers from the fresh install survive, so a "restored" home can be a
   hybrid. For a clean target: move the existing home aside (`mv ~/.hermes ~/.hermes.pre-restore-<ts>`), then import.
3. **Back up the target yourself before importing.** Nothing is copied aside automatically, and that copy is also
   the rollback when the archive turns out to be the wrong one.

Importing into an empty throwaway home never exercises the prompt path — drill the already-installed case as well,
otherwise the first real restore is the first time that branch runs.

## Encryption and hygiene

- Choose the crypto tool from what resolves: `command -v age git-crypt gpg openssl zstd sqlite3 jq`. If the
  preferred tool is absent, its install is an explicit step in the plan, not an assumption.
- Keep the key out of the repo (Keychain + one offline copy). A backup repo that ships its own key is not encrypted.
- **The archive holds `.env` — it is a copy of the secret.** Delete the plaintext working copy (and any trimmed
  duplicate) once coverage is verified, and say that you did.

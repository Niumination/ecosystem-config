# Live verification probes by subsystem

Canonical probes for step 5. Use these, not a convenient shortcut — a stale probe path returns a
misleading answer that propagates into the verdict. Batch them into one scripted pass.

## macOS security posture

A security claim usually names a *state*, and several of these states have an in-between phase that
must not be read as the finished state.

```bash
fdesetup status                                   # want: 'FileVault is On.'
#   'Decryption in progress' / 'Encryption in progress' = mid-flight, NOT on.
#   An 'On (NN%)' log line elsewhere in the report proves it STARTED, not that it finished.
diskutil apfs list | grep -E 'APFS Volume|FileVault'   # per-volume ground truth
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate   # want: State = 1
```

Encryption state is per-volume, so a single `fdesetup status` line can be right about the boot volume
and wrong about the posture the report claims. Cross-check with `diskutil apfs list`.

## launchd: retirement and binding

A retirement claim needs **two** probes. Runtime registration and the on-disk artifact are separate
facts, and a report can clear one while leaving the other.

```bash
launchctl list | grep -i '<label>'                # loaded right now?
ls -la ~/Library/LaunchAgents/ | grep -i '<label>'  # will load again at next login?
```

Both absent = retired. Only one absent = still half-present; say which half.

For a service claimed to bind loopback rather than a wildcard:

```bash
lsof -nP -iTCP:<port> -sTCP:LISTEN                # want: 127.0.0.1:<port> (LISTEN)
#   '*:<port>' = wildcard, i.e. the hardening claim is false
```

## Scheduled jobs: configured is not executed

```bash
hermes cron list | grep -c '\[active\]'
hermes cron list | grep -c '\[paused\]'
hermes cron list                                  # read 'Last run:' per job
```

A job present in the list proves configuration only. Read each job's `Last run` — a job that has never
fired shows no last run at all, and a catch-up note (`ran ... late`) means the schedule did not fire
on time. A snapshot whose timestamp does not match the declared schedule is a manual run misread as an
automated one; check the artifact's own mtime against the cron expression before crediting automation.

## Hermes config and skills

```bash
hermes config get model
hermes config get terminal.cwd
hermes config get skills
hermes config get mcp_servers.filesystem
hermes skills list | tail -3                     # the tool's own count line
```

Prefer `hermes config get <key>` over parsing `config.yaml` by hand: it resolves the effective value
including defaults, and it needs no YAML library present. A `python3 -c "import yaml"` probe fails on
interpreter builds without PyYAML — that is a probe defect, not a finding about the config.

## Permissions on identity and config files

```bash
stat -f '%Sp %z %N' ~/.hermes/config.yaml ~/.hermes/SOUL.md
ls -la ~/.hermes/SOUL.md                         # regular file, or symlink to elsewhere?
```

`-rw-------` is the expected mode. A symlink here means the real content lives in another repo, so
edits to it are edits to that repo and a restore has to happen there.

## Secret scanning and git cleanliness

```bash
gitleaks detect --no-banner --redact             # want: no leaks found
cd <repo> && git status --short                  # untracked audit artifacts left behind?
```

Run the scan from the repo root and read the scanned-commit count — a scan that reports far fewer
commits than the history holds did not cover what you think it covered. `git status --short` output
is itself a finding: an audit that produced reports but never committed them leaves the evidence one
`rm` away from gone.

## Backup repositories

```bash
ls -la "<repo path>"
RESTIC_REPOSITORY="<repo path>" RESTIC_PASSWORD_FILE="<pass file>" restic snapshots --compact
```

`restic` with no repository argument fails with `Please specify repository location` — that is a
missing argument, not a broken backup. Read the backup script to recover the repository path and
password-file location, then re-probe with both exported. One snapshot present proves the repository
works; it does not prove the schedule runs.

## Published artifacts

```bash
gh release list --repo <OWNER>/<REPO>
```

Always pass `--repo` explicitly. Without it `gh` resolves the repository from the current directory,
which silently answers about a different repo.

## Reporting the probes

Emit one line per probe: label, observed value, exit code. An `UNCHECKED` line with the reason beats a
plausible value you did not actually read.

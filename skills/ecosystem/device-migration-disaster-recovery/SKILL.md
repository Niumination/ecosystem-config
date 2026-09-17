---
name: device-migration-disaster-recovery
description: Use when planning backup, restore, or device migration.
version: 1.0.0
---

# Device Migration & Disaster Recovery

The goal of this class is one sentence: **if this laptop dies, is stolen, or is replaced, the user is
running again on the new machine with the same configuration and the same data.** Work is judged by
that question, not by how many repos are named "backup".

The user's mental model is Time Machine / restore point / OS clone — full coverage in, working machine
out. Match that model, and be explicit about which part of it any given tool actually covers.

## Hard Rules

1. **Three layers, three tools — never one tool for all of it.**
   - **L0 System & apps** — macOS, installed apps, Homebrew, launchd agents, user data dirs →
     Time Machine or a disk clone. No git repo substitutes for this.
   - **L1 Configuration & identity** — Hermes config + credentials, dotfiles, ecosystem config,
     project DOX → git repos (private where credentials are involved).
   - **L2 Data & state** — session DB, memories, kanban DB, project databases, logs → encrypted
     snapshot (restic/borg, or tar+age). Binary state in git bloats history and nobody reviews it.
2. **A copy on the same disk is not a backup.** APFS local snapshots (`tmutil listlocalsnapshots /`)
survive a bad edit, not disk loss, theft, or a dead machine. Say this when a user counts them as backup.
3. **Plaintext credentials never enter git; ciphertext may.** Encrypt with git-crypt / age / SOPS and
the "aman vs lengkap" trade-off disappears — that trade-off is exactly why credentials are the thing
that goes missing from config repos. Keep the encryption key OUT of the backup (Keychain + one offline
copy). A repo leak that includes its own key is not encrypted.
4. **A submodule is a pointer, not a backup.** Submodules record a commit SHA, not contents; embedding
one over an ignored/secret path needs `git add -f` on a gitlink, which is banned and is the same pattern
that leaks credentials. Use a dedicated repo plus a sync process.
5. **Do not add a daemon or a filesystem watcher.** The host is RAM-constrained and already runs many
launchd agents. Drive sync from the Hermes cron that already exists, or from git hooks — event-driven
and no standing process.
6. **Back up what cannot be rebuilt; skip what can.** `node_modules`, build output, caches and generated
artifacts are rebuilt from source; copying them slows every run and hides what actually matters.
7. **State residual risk instead of implying safety.** Clones taken before a history rewrite, host-side
blobs awaiting GC, and a private repo that syncs off the same laptop all keep exposure alive.
8. **Check the destination's limits before promising coverage.** Git hosts cap single files (GitHub:
100 MB hard, 50 MB warning) and degrade on multi-GB repos, so a large binary state DB cannot be pushed
as-is — plan to compress and split it, or export only the tables that matter. Discover this while
planning, not on the first push.

## Procedure

### 0. Start from what already exists — the bank, then the app's own CLI
Design work in this ecosystem opens with lookups, not a blank page. Three checks, in this order:

1. **The skill bank.** `skills_list` plus `skill_view` on anything that matches the class — a backup/restore/
   migration blueprint, an allowlist, or a restore script may already exist. Re-deriving one wastes the session
   and drifts from rules the user already agreed to.
2. **The application's own CLI.** Before scripting a copy of any application home, ask whether the application
   backs itself up: `hermes --help | grep -iE "backup|export|import|dump"` surfaces `hermes backup` and
   `hermes import`, which snapshot SQLite through `sqlite3.backup()` (consistent while the gateway runs) instead
   of a raw file copy, exclude `-wal`/`-shm` sidecars and caches, and retain skills, sessions, cron jobs, `.env`
   and `auth.json`. A hand-rolled `cp` of a live DB is how a backup quietly becomes corrupt.
3. **The repo's own bootstrap.** Config repos often ship an installer with a health check
   (`zaryu-terminal-dotfiles/setup.sh --bootstrap|--doctor|--dry-run`, stow-based, Brewfile for a fresh machine).
   Reuse it inside the restore order instead of writing a parallel one.

Packaging recipe for the Hermes home layer — what the archive includes, what to trim, split rules, and the drill that
proves it: `references/hermes-home-backup.md`. Restoring onto a different OS or a different username:
`references/cross-os-restore.md`. Staging the archive at an offsite destination and fetching it back:
`references/offsite-artifact-staging.md`. Structuring the deliverable itself — a private restore repo with a build
side and a restore side, release-hosted blobs, and a repeatable drill harness:
`references/restore-repo-layout.md`.

### 1. Measure the real exposure — never assume a layer exists
```bash
tmutil destinationinfo            # "No destinations configured" = zero OS-level backup
tmutil latestbackup
tmutil listlocalsnapshots /       # same-disk snapshots: not protection
df -h | grep -v devfs             # could a local clone even fit?
du -sh ~/Desktop/<eco> ~/.hermes ~/Documents ~/Pictures ~/Movies
```
A missing L0 is the headline finding, not an optimization — report it before proposing anything else.

### 2. Inventory what the config repos actually cover
A repo whose name says "backup" is not evidence of coverage. Check contents and history:
```bash
git -C <repo> remote -v
git -C <repo> ls-files | grep -iE "vault|secret|credential|\.env|api-key"
find <repo> -maxdepth 3 -type d -name vault
git -C <repo> log --all --oneline -- '*vault*'     # empty = never snapshotted
```

Then sweep every repo for the two cheapest holes — work that never left this machine:
```bash
for d in $(find <eco-root> -maxdepth 4 -name .git -type d); do
  r=$(dirname "$d"); [ -z "$(git -C "$r" remote)" ] && echo "NO REMOTE: $r"; done
# for the active repos, also: uncommitted work
git -C <repo> status --porcelain
```
A repo with no remote, or one sitting on uncommitted work, is gone outright when the machine dies, and it
is the cheapest gap to close. Report it in the same breath as the missing OS-level backup, and do not
commit someone else's in-progress work without asking — flag it and let the owner push it.

### 3. Measure drift in every snapshot that claims to be current
The classic failure: a snapshot taken once, never refreshed, quietly diverging while still looking like
protection. Compare by hash, and for env-style files by **key names only** — never print values.
```python
import hashlib
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
names = lambda p: {l.split('=', 1)[0].strip() for l in open(p)
                   if '=' in l and not l.strip().startswith('#')}
# report: identical hashes? keys live now but absent from the snapshot?
```
The live-only key list is the gap to close first, and it is concrete evidence to show the user.

### 4. Classify every candidate path before choosing tools
Sort into: non-rebuildable (credentials, state, authored work) / rebuildable (deps, build output,
cache) / too large for git (media, archives, DB dumps). This decides L1 vs L2 and keeps the plan honest
about size and runtime.

Enumerate rather than guess, per repo:
```bash
git -C <repo> ls-files --others --ignored --exclude-standard   # everything a clone will not restore
```
Then drop the rebuildable majority by pattern. Triage the survivors starting with **irreplaceable small
binaries** — app signing keystores, certificates, licence/provisioning files: a few KB, no git history,
and no way to recreate, so losing one permanently ends that app's ability to ship updates. Credentials and
deploy wiring (`.env*`, `.vercel/project.json`, `.vercel/env`) come next, then state and authored data
(project DBs, `data/*.json`, raw datasets, locally-authored skill/plugin trees).
Full procedure, skip patterns and size handling: `references/ignored-path-sweep.md`.

### 5. Write the plan before executing
Docs-then-Execute, with: a layer table (what, tool, destination, schedule), a path **allowlist** (never
a blind `git add -A`), the encryption choice plus who holds the key, and the restore drill. Get explicit
approval — backup work moves secrets around and a wrong target repo or script creates a brand-new leak
surface. Prefer extending an existing private repo over creating a new one when the context fits; create
a new repo when mixing contexts would muddy a repo's single purpose.

Expect revision rounds, and shape them: save each revision as its own dated document under `docs/reports/`
(never overwrite the previous one — the trail of corrections is part of the deliverable), and make each round
**test the plan**, not re-audit the system. Adding findings without validating the plan that already exists
produces scope growth and no confidence; a round that drills one assumption and reports what broke is what
converges. When the owner says a revision is still not finished, the next round starts by naming which parts of
the current plan are still unverified and testing those.

### 6. Implement, then drill
A restore that has never been performed is an assumption, not a backup. Drill at minimum: clone the
config/portable repo into a clean directory, restore the encrypted credential file, restore one state DB,
and open one project. Record what failed — that record is the only evidence the plan works.

Two drills carry most of the value and both run on the machine in front of you: **import the application archive
into a throwaway HOME** (`HERMES_HOME=/tmp/drill-home/.hermes hermes import clean.zip`, recipe in
`references/hermes-home-backup.md`) and **substitute path placeholders into a copy of the real config with a fake
HOME**. Anything that only works when run by hand, interactively, from the real home, is not yet tested.

Compare restored identity and config files by **hash against the live source**, never by presence, and re-run the
drift check on the restored copy. A drill that reports a count has not verified intent — the count and the file can
both be wrong while looking green.

## Pitfalls

- **Time Machine can be silently absent.** `tmutil destinationinfo` answers it in one line; check before
designing layers on top of nothing.
- **Config vs data confusion.** Reports/DOX are the easy things to snapshot; session state, memories,
DBs and credentials — the things that actually hurt to lose — are usually the ones missing.
- **"The file exists" is not verification.** Verify by hash, and by drift against the live value; a stale
copy invites assuming coverage.
- **Never print credential values during an audit.** Hashes, lengths and key names only.
- **A public config repo removes plaintext as an option.** Use an encrypted blob or a private target,
and keep the pre-commit credential gate enabled on every repo touched.
- **The backup itself is a copy of the secret.** A mirror/tar made during a rewrite, or a plaintext
snapshot repo, is now a second place the credential lives — delete it once verified and say that you did.
- **Blocked/destructive steps are not retried by another route.** If restoring or a forced operation
needs approval, sequence it, ask, and continue with the non-destructive parts meanwhile.
- **The scary-looking number is not the scope.** An ecosystem can hold six figures of ignored files and
still have only a few dozen that cannot be rebuilt. Sweep, filter, report survivors — a raw ignored count
either alarms the user or gets dismissed as noise.
- **The smallest file can be the most valuable.** A signing keystore or certificate is easy to overlook
beside `node_modules`, and it is the one class of file with no recovery path at all. Check it before
anything large.
- **Dangling work is invisible to status tools.** "All repos clean" reports tracked state; a repo with no
remote and a repo with uncommitted edits both read as healthy while existing only on the disk that is
about to fail. Check both explicitly.
- **Rebuildability is per-file, not per-directory.** A browser-profile or checkpoint directory looks like
state but usually only costs a re-login; a single `config.json` beside a regenerable `data/` tree can be
the one thing worth keeping. Decide file by file inside each ignored tree.
- **A parser reporting "absent" — or "present" — is not evidence.** `unzip -l | grep "$name$"` reported entries as
  missing that were present, because the listing prints size and timestamp columns ahead of the name; switching to a
  plain unanchored `grep -cF` then reported `SOUL.md` as present when only `SOUL.md.v1.bak-*` existed. Both
  directions bite, so decide presence on whole basenames taken from the name column
  (`unzip -Z1 x.zip | awk -F/ '{print $NF}' | sort -u`), and before reporting any coverage finding — the kind the
  user acts on — re-run it a second way and state which check answered.
- **Name only tools the machine actually has.** Run `command -v age git-crypt gpg openssl zstd sqlite3 jq`
  before committing an encryption or archival step to the plan; a plan whose first action errors out is worse than
  no plan. When the preferred tool is absent, the install command becomes its own explicit, approved step.
- **An application home is not the whole identity.** Other tools the ecosystem leans on keep credentials and
  machine identity in sibling directories — a local model router (`~/.9router`: `auth`, `jwt-secret`, `machine-id`,
  `db/`), other agent CLIs (`~/.config/<cli>/`), an Electron app's `~/Library/Application Support/<App>/`, and
  `/Applications/<App>.app`. Walk the launchd plists and the dotfiles doctor's credential list: every plist that
  names a path is a layer the restore order has to cover.
- **Restore order is a dependency chain, not a list.** Cross-scope links decide it: `~/.hermes/SOUL.md` symlinked
  into the dotfiles repo (restore Hermes first and the agent comes up on default identity), local patches living
  only on a `backup-*` branch (restore `main` and the fixes vanish silently), absolute paths embedded in dozens of
  config files assuming the same username. Enumerate symlinks, non-main-branch patches and absolute paths before
  writing the order, and make each step verify the one before it. Clone the config repos **first**: `git clone`
  refuses a non-empty destination, so any earlier step that writes into the target tree (a decrypted `vault/`, an
  extracted blob) makes the clone fail — and a script that logs per step renders that failure as one more quiet line.
- **Config-repo coverage is decided by symlink targets, not by files present in `$HOME`.** In a stow-based
  dotfiles repo only the stowed packages are covered; a real file sitting in `$HOME` (shell history, a
  tool-generated `~/.config/<cli>/` tree, an app's support dir) is outside the repo and simply absent on the
  target. Confirm each path counts as restored by resolving it (`readlink <path>` inside the repo), and take the
  critical-path inventory from the repo's own health check — the dotfiles doctor names the agent configs it
  expects — rather than from a directory listing. Adding a new CLI or tool creates one more layer nothing
  stows.
- **A stale credential exported into the environment shadows a working auth path.** A dead `GH_TOKEN` in an env file
  made every `gh` call return 401 while the CLI's own keyring login was healthy — the env var wins, so the tool
  breaks only in the contexts that export it (scripts, cron), not in the terminal. Probe each credential for
  validity during the drill; treat "401 from a tool that works without the env var" as a credential problem, never a
  permissions problem. Checking that a credential file exists is not checking that it works, and a dead credential
  in the environment is more dangerous than a missing one.
- **Tools that default their target from the working directory need an explicit target.** `gh release create` with
  no `--repo` published a test release into whichever repo the shell happened to sit in — a public one. Every
  write-capable command in a restore or sync script takes an explicit target (`--repo`, absolute path) and verifies
  it (`git remote get-url origin`, or the resolved path) before acting; a helper that derives the target from `$PWD`
  is a wrong-destination incident waiting for the one run where the variable is empty.
- **Restoring onto a machine that already has the app installed is a different operation from restoring into an empty
  home.** The app's own importer detects existing configuration and asks for confirmation, which aborts a
  non-interactive run with a non-zero exit and a message easy to skim past; a merge-style import then leaves local
  files the archive does not contain, and overwritten files are kept nowhere. Copy the existing home aside first,
  pass the importer's force flag, and treat "restored" as unproven until the target has been inspected for leftovers.
  A drill into an empty throwaway home never exercises this path.
- **Restore scripts run on the target's shell and runtime, not the author's.** macOS still ships bash 3.2 —
  `mapfile` and other bash-4 constructs abort the script. And exit codes must be honest in both directions: `grep`
  returning 1 on "no match" kills a `set -e` script with a false failure, while a missing anti-silent gate lets a
  script that did nothing exit 0. Wrap expected no-match greps with `|| true`, and make "found nothing where
  something was expected" exit non-zero. Print which method produced each verdict, and test scripts in both
  environments they must survive — interactive foreground and non-interactive background.
- **The build side and the restore side drift silently, and every drift looks like a skip rather than an error.**
  The writer and the reader are separate programs that must agree on file names, extensions and KDF parameters.
  A restore loop over `*.age` when the writer emitted `*.enc` iterates zero times and reports completion; a reader
  looking for `data.tar.zst.age` while the writer produced `.enc` logs "data not restored" and continues; a file
  target pointing at a directory path writes the payload where a directory belongs. None of this reddens a green run.
  Count what the loop processed and exit non-zero when the count is zero where payload was expected, and diff the two
  sides against each other (every filename and flag the writer emits must appear in the reader) before trusting the pair.
- **Parameters the artifact does not store must be asserted on both sides.** `openssl enc` writes salt only — not the
  KDF iteration count — so encrypting with `-iter 200000` and decrypting with the default (10000) fails on every file,
  on the target machine, after the original is gone. Pin such parameters as one explicit constant shared by both
  scripts; a drill that used the writer's own defaults proves nothing about the reader.
- **A credential that lives only in the OS keychain is lost with the device.** Generate the backup key into Keychain
  for convenience, but the restore of a blank machine cannot read Keychain and the owner must enter the passphrase
  from outside; say the retrieval command out loud and treat the plan as *incomplete* until an off-device copy exists.
  This is the failure that surfaces at the worst possible moment, so it is a gate, not a note.
- **Every layer must be ciphertext before it reaches the host — including large blobs staged as release assets.**
  A private repo is not encryption: an unencrypted `hermes-backup.zip` holding `.env` puts the entire credential set
  on the host, breaks the ecosystem's own credential rule, and is the pattern that gets tokens revoked automatically.
  Encrypt before splitting, upload only `*.enc.part-NN` plus checksums, delete the plaintext release, and make the
  fetch side decrypt and then assert the result is a readable archive (`unzip -l`) rather than trusting the download.
- **Pick the transfer endpoint by measurement, not by habit — the spread is ~100x.** On the same host at the same
  moment, `codeload` and git-over-HTTPS served ~30 KB/s while `api.github.com/.../releases/assets` served 2.3 MB/s; a
  130 MB blob is minutes on one path and hours on the other, and a background-context run can land on the slow path.
  Fetch release assets from the API with `curl --retry 4 -C -` (resumable), assert each asset's byte count, and keep
  `gh` for metadata and API calls rather than bulk transfer. Time one probe before promising a restore duration.
- **`… | grep -q` under `set -o pipefail` turns a match into a failure.** `grep -q` exits at the first hit, the
  producer takes SIGPIPE (141), and the pipeline reports failure — so a coverage check announced `config.yaml`
  MISSING for a file that was present, and only the drill exposed it (present *and* absent were both reported
  wrongly at different times). Capture the listing to a file, or use `grep -c` and test the count, before letting
  the result drive a verdict.

## Verification

- Every layer has a named destination and a schedule; **no layer depends on the internal disk alone.**
- Coverage check: the credential/state paths appear in the tracked file list of a private target, not
just on disk.
- Drift check: zero differing hashes and zero live-only keys against the snapshot.
- Archive coverage confirmed entry by entry for the paths that matter (credentials, skills, cron jobs, state DB)
  — listed from the artifact itself, not assumed from the tool's description.
- Crypto/archival tools named in the plan all resolve on the target machine, or their install is an explicit step.
- One restore drill performed, with the result written down (what worked, what failed, what was assumed), run against
  the repo **as fetched from its remote** into a clean HOME — a working copy that sits on the same disk as the source
  shares a filesystem with it and hides clone, fetch and missing-asset failures.
- Drift check re-run against the **restored** copy (hash + live-only key names); comparing only the source proves
  nothing about the target.
- **Count the skill layer with a whole-tree enumeration, and name the counter.** A project's own manifest or lockfile
  only sees the layouts it was written for: one manifest built over `<domain>/<skill>` reported 140 skills while the
  tree held 148 — four skill directories sat at the root and four three levels deep, invisible to it, and its sync
  tool aborted silently on the root-level ones. Verify the layer with `find <home>/skills -name SKILL.md | wc -l`
  (or an interpreter's `rglob`) rather than a tool's summary, and when a tool's count disagrees with the tree, treat
  the tool as the thing to fix before trusting either number.
- **A skill edit must land in the bank, then sync outward — editing the target copy is reverted without an error.**
  The sync tool is non-destructive and the bank always wins, so a lesson written into the agent's own `skills/` copy
  is overwritten by the next `sync-to-agents.sh` run, and the edit tool's success response says nothing about what
  survives. Write the edit in the bank, run the official manifest + sync, then `grep` the distinctive phrase in
  **both** copies before reporting it recorded. Recovering a reverted skill is possible from the curator's blob
  backups (`~/.hermes/.curator_backups/blobs/`) — pick the candidate by grepping for the missing phrases rather than
  by size or timestamp, and re-install it into the bank.
- **Check a live service's database on a copy, or with `mode=ro` — never by opening it in place.** A bare
  `sqlite3 <path> "PRAGMA integrity_check"` opens the file read-write; if the service is running without a WAL it
  creates `-wal`/`-shm` beside a database another process has open, and the audit's "read-only" claim became false
  the moment it ran. Copy the file to a temp dir (or `sqlite3 "file:<path>?mode=ro"`) before inspecting, and when the
  audit itself touches a live service, say so plainly instead of describing it as a read.

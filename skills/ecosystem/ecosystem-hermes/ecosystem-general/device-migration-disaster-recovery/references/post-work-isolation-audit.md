# Post-work isolation audit

Use after any build, drill, sync, or credential-touching operation, when the owner asks some form of
"did this change the real system?" — and before answering, not after. The answer must be evidence, not memory
of what you ran: the same session that felt read-only is the one that opened a live DB read-write.

## 1. Probe the live artifacts, do not recall your commands
Read-only probes per surface, each bound to an explicit path:

```bash
stat -f '%Sm' ~/.ssh/config ~/.ssh/id_ed25519_* ~/.9router/{auth/cli-secret,jwt-secret,machine-id}
ls -l  <vault>/secrets.zsh <signing>.jks <signing>.pem      # size match against the original audit
ls -l  ~/.hermes/SOUL.md                                    # symlink target must still resolve outward
git -C <repo> status --porcelain                            # per repo, explicit -C
```

For env-style files report **key names and counts only** — never values. A credential file whose mtime is
earlier than the session is untouched; that is the whole proof, so capture it before touching anything else.

## 2. Classify every difference, and name the intended ones out loud
Three buckets, and the report needs all three:

- **Intended** — new directories, new Keychain entries, new GitHub objects, regenerated manifests. List them;
  "everything was isolated" is a false claim the moment one exists.
- **Owner-caused** — a file the user edited mid-session (a rotated token in `.env`) shows up in the change
  window. Compare its mtime against your own actions before adopting or denying it.
- **Pre-existing** — a service that was already down. `launchctl list` showing an agent missing proves nothing
  about when it stopped; date it from the service's own log mtimes, or from its listening port, not from the
  fact that it is absent now.

## 3. Bind every probe to an explicit target
In a compound shell command the working directory carries over from earlier lines in the same command, so a
probe that inherits the wrong cwd answers confidently and wrongly — a repo-ignore check run from inside a
sibling repo reported "not ignored" for a path the parent repo ignores. Use `git -C <repo>`, absolute paths,
and re-run any negative result that would become a reported finding.

Scope the search to what can answer the question. `git -C <repo> grep` over tracked files answers "did any real
config file get polluted with a placeholder or a foreign path" in seconds, while a recursive `grep -r` across a
multi-GB tree — dependencies, build output, caches — exhausts the command timeout and returns nothing usable. A
probe that blows its budget is a signal to narrow the probe, not to raise the timeout, and a timed-out search is
not evidence of cleanliness.

## 4. Never inspect a live service's database in place
A bare `sqlite3 <path> "PRAGMA integrity_check"` opens the file read-write and, when the service runs without
a WAL, creates `-wal`/`-shm` beside a database another process holds open. Copy the file to a temp dir first, or
use `sqlite3 "file:<path>?mode=ro"`. If the audit itself touched a live service, say that plainly instead of
describing the step as a read.

## 5. Distinguish "changed" from "damaged", and say which check answered
After any surprise, re-verify substance on a copy (`PRAGMA integrity_check`, size/hash against the original
audit, entry count from the artifact) and name the probe that produced the verdict. A changed file with intact
content is a footnote; an unverified one is an open risk.

## 6. Prove nothing was left behind
Temp dirs, decrypted copies, blob parts and drill HOMEs all hold real credentials once the drill has run.
Confirm they are gone (`ls -d <work-dir>` empty, no oversized leftovers in `/tmp`) and record free space, so the
cleanup is a checked fact rather than an intention.

## 7. Report pre-existing breakage — labelled
The audit routinely surfaces failures that are not yours (a dashboard stopped weeks ago, a service with an old
log). Report them, and date them from their own evidence so the owner does not read them as a regression from
this work. An audit that quietly omits what it found, or quietly blames itself, is not an audit.

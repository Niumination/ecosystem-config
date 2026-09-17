# Restoring onto another OS or another username

A restore plan that silently assumes the author's OS and username is not a plan — it is a demo. The user's own
targets may be Windows, a different Linux, or a different macOS version, on a machine whose username comes from a
fresh install and cannot be changed without an interactive session. State per-OS behaviour up front, in a table, and
mark what cannot be validated without a second machine.

## Portability matrix — decide each row explicitly

| Component | macOS | Linux (Arch-style) | Windows |
|---|---|---|---|
| App core + its own backup/import CLI | works | works | works |
| App home location | `~/.hermes` | `~/.hermes` | `%USERPROFILE%\.hermes` |
| Plain-text config, skills, cron defs | portable | portable | portable |
| Shell/dotfiles layer (stow + zsh + Brewfile) | full | partial (zsh yes, brew → pacman/AUR) | none — PowerShell equivalent is a separate artefact |
| Service manager for always-on daemons | launchd plists | **systemd user units** | **Task Scheduler** (or a service wrapper) |
| OS keystore | Keychain | libsecret | Credential Manager | **none of these are portable** |
| Executable bit | honoured | honoured | lost — call `bash script.sh` or use WSL |
| Symlinks | native | native | needs Developer Mode / admin, prefer copies |
| Line endings | LF | LF | CRLF — needs `.gitattributes`, or scripts break |
| Desktop app bundle | `.app` in `/Applications` | package per distro | `%LOCALAPPDATA%` install |

A stow/Zsh dotfiles `setup.sh` that begins `[[ "$(uname)" != Darwin ]] && exit 1` is macOS-only by construction: on a
non-macOS target it is a no-op, so the restore order needs a replacement step, not a hope.

## Instructions that live in a file must not hardcode one home

Dozens of config files embedding the author's absolute home (`/Users/<name>`) means the restore works only if the new
machine happens to use the same username.

- Build the backup repo with a **placeholder scheme** — `{{HOME}}`, `{{ECO}}`, `{{HERMES_HOME}}` — and substitute at
  restore time from the target's real values. Any path that a target-side env var already provides should be written
  as that variable instead of a placeholder, so the app follows `HERMES_HOME` rather than a copied literal.
- Substitute from an **allowlist**, never a blind walk of the whole tree: same reason a backup never uses
  `git add -A`. Print every file touched and run dry by default; the apply mode must be an explicit flag.
- Prefer rewriting the patterns in the sources too, and record the remaining files as debt — otherwise the next clone
  reintroduces them.
- Serve substitution with a POSIX/bash-3.2-safe script. `mapfile` does not exist on macOS bash 3.2 and the failure is
  silent, so a version check or a plain `while read` loop is mandatory.

## Script hygiene these scripts must satisfy

- **Honest exit codes, both directions.** `grep`/`find` return 1 on "no match": harmless when expected, fatal
  mid-script under `set -e`. Wrap those with `|| true`. Conversely, "I found nothing where something was promised"
  must exit non-zero — a restore helper that does nothing and exits 0 is the worst outcome, because the operator
  believes it ran.
- **Never report a verdict from a tool you have not sanity-checked.** Two inventory methods measured the same
directory as 0 and 202 — the one that said 0 was a shell alias that silently rejected the flag. Print the method
  used for each verdict, and cross-check any number the operator will act on.
- **Idempotent and re-runnable.** Restore is run twice in real life (half-failed first attempt). Back up files it is
  about to replace, and let a second run be a no-op rather than an error.
- **Both runtime environments.** A script proven in an interactive terminal must also be proven in the context that
  will actually run it unattended — background jobs are a different environment (on macOS, no access to the login
  keychain), so anything they need must come from files or env vars.

## What to admit as unvalidated

Without a second machine or VM, cross-OS service registration, Windows path/symlink behaviour, and a full
end-to-end restore on a non-author OS are **unverified**. Say so in the plan, and keep them marked until a device
actually exists — an untested step labelled "done" is how a DR plan looks complete and fails on the day.

# launchd services don't inherit shell env — `.env` is invisible

## The rule

A process spawned by `launchd` (LaunchAgent/LaunchDaemon) inherits **only** what the
job's `EnvironmentVariables` dict or the `launchctl setenv` session namespace
provides. It does **not** read `~/.hermes/.env`, `.zshrc`, `.profile`, or any shell
rc file — those apply to processes you start from a terminal, which is a different
parent chain.

**Why:** launchd is PID 1's child manager. It builds the job environment at
`bootstrap` time from the plist + the `launchctl setenv` store. Shell rc files are
executed by a *shell*, and launchd never runs a shell.

## Symptom signature

Config value is verifiably present in `~/.hermes/.env`, the service starts fine, and
the feature silently runs with the *default* instead of the configured value:

```
$ grep FOO ~/.hermes/.env
FOO=bar                       # present

$ launchctl getenv FOO
                              # empty  ← never made it into the job environment
```

This is environment-dependent-looking, so it gets misdiagnosed as "the config key
is wrong". It isn't. The value never reached the process.

## Procedure

1. Confirm the value is in the env file **and** absent from the launchd namespace:

   ```bash
   grep FOO ~/.hermes/.env
   launchctl getenv FOO; echo "exit=$?"   # empty output = not set for jobs
   ```

2. Confirm the running process genuinely lacks it:

   ```bash
   ps eww "$(pgrep -f '<service>' | head -1)" | tr ' ' '\n' | grep '^FOO=' || echo NOT_IN_PROCESS
   ```

3. Push it into the launchd session namespace, then restart the job:

   ```bash
   launchctl setenv FOO bar
   launchctl kickstart -k gui/$(id -u)/<label>
   ```

4. Re-verify against the *service's observable behaviour*, not the env var — a
   service can accept the var and still bind its default (e.g. a listener that
   honours `HOST` but falls back to loopback when unset, silently).

## PATH is a value too — and launchd's PATH is not yours

`PATH` is the most damaging instance of this rule, because a missing binary fails
*silently* inside a pipeline rather than erroring.

On macOS, launchd jobs get a minimal PATH (typically
`/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin` or a plist-supplied subset). Tools that
live outside it — notably **`sha256sum`, which is in `/sbin`** — are simply absent.
A job that works when you run it by hand can be broken under launchd, and the
reverse is also true: a script can look healthy for weeks only because some other
interactive caller had the missing directory in PATH.

**The trap that hides it: `||` inside a pipeline never fires.** The exit status of a
pipeline is the exit status of its **last** command. So this does *not* fall back:

```bash
HASH=$(echo "$IDS" | sha256sum 2>/dev/null | cut -d' ' -f1 || shasum -a 256)  # WRONG
#                         ^ 127 (not found)      ^ 0 (cut succeeded) → || never runs
```

`HASH` comes out empty. If the script then compares it to a previously-empty value,
the comparison matches, the script takes the "nothing changed" branch, and exits 0
forever — a **self-perpetuating silent no-op** with no error in any log.

**Correct pattern — probe for the binary, don't rely on `||`:**

```bash
_hash_ids() {
  if command -v sha256sum >/dev/null 2>&1; then printf '%s' "$IDS" | sha256sum | cut -d' ' -f1
  elif command -v shasum >/dev/null 2>&1; then printf '%s' "$IDS" | shasum -a 256 | cut -d' ' -f1
  else printf '%s' "$IDS" | openssl dgst -sha256 | awk '{print $NF}'; fi
}
HASH=$(_hash_ids)
[ -z "$HASH" ] && { echo "$(date -Iseconds) FATAL: no sha256 tool" >> "$LOG_FILE"; exit 1; }
```

The empty-value guard matters more than the fallback chain: **fail loudly, never
succeed falsely.** A job that exits 1 shows up in the run history; a job that exits 0
having done nothing is invisible for as long as nobody checks.

## Test under the real launchd PATH, not your shell's

This is the step that catches it, and the only one that does:

```bash
env -i PATH=/usr/local/bin:/usr/bin:/bin HOME="$HOME" /bin/bash /path/to/script.sh; echo "exit=$?"
```

Read the PATH out of the plist rather than guessing it, and include it verbatim. A
script that passes here is safe under launchd; a script that only passes in your
interactive shell is not.

**Diagnosing a job that has already gone quiet:** check whether the state/hash file it
writes is empty or frozen at an old date. A zero-byte hash file is the signature of a
pipeline that never produced output — not of a job that found nothing to do.

```bash
stat -f "%Sm %N" /path/to/state.json     # frozen = suspect
wc -c /path/to/hash.file                 # 0 or 1 byte = never written
```

## Persistence: `launchctl setenv` is runtime-only

`launchctl setenv` writes to the **login session namespace** and is wiped on
logout/reboot. A service that must keep a value across reboots needs one of:

- `EnvironmentVariables` inside the job's plist (`~/Library/LaunchAgents/<label>.plist`),
  then `launchctl bootout` + `bootstrap` to reload;
- a wrapper script the job `ProgramArguments`-execs, which sources the env file
  itself before exec'ing the real binary;
- a login-item / session agent that re-runs `launchctl setenv` after every login,
  before the dependent job is expected to come up.

Pitfall: verifying after a `kickstart` alone proves nothing about the next boot —
`setenv` + `kickstart` can leave a service that is correct *now* and reverts to
defaults on the next reboot. Any claim of "autostart works" needs a post-reboot
probe, not a post-restart one.

## `kickstart` cannot be run from inside the job it restarts

A service trying to restart itself (or a shell that is a descendant of it) gets
killed by the `SIGTERM` propagating up through its own child processes before the
command can return. Symptom: the command reports "blocked", is refused by a
guard, or appears to hang then vanish.

**Rule:** restart jobs from a shell that is not a descendant of the job — a
separate terminal, or a launchd-spawned helper. Never from inside the agent
session that the service is hosting.

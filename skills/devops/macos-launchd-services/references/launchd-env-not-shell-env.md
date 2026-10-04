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
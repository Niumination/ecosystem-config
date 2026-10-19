# Removing a Provider's Credentials From a Machine

Destructive counterpart to credential resolution. Goal: **one provider's keys gone, every other
provider untouched, nothing still running on the old credential.**

## Procedure

### 1. Inventory every store before deleting anything

A provider's key can live in more places than the one you were told about. Full sweep:

| Store | Holds |
|---|---|
| `~/.hermes/.env` | env-style keys, one `NAME=value` per line |
| `~/.hermes/auth.json` | `providers.<n>` (OAuth tokens) *and* `credential_pool` |
| `<tool>/.config/<tool>/auth.json` | per-tool API keys |
| `<tool>/.config/<tool>/opencode.json` | `provider.<n>.options.apiKey` |
| `<tool>/.local/share/<tool>/<tool>.db` | `credential` table — this is where **OAuth sign-ins** live |
| `vault/secrets.zsh` | shell-level exports sourced by `.zshrc` |
| `~/.zshrc` / dotfiles | `source`/`export` lines |
| macOS Keychain | `security find-generic-password -s <name>` |

Search by **value**, not by name — a key may be referenced under a name you did not expect:

```python
val = <the value you intend to remove>
for p in candidate_files:
    if val.encode() in open(p, 'rb').read():
        print('FOUND in', p)
```

A zero match after removing from the obvious store means the value came from a running process's
environment, not from a file.

### 2. Scope the removal to one provider

Delete by exact variable name and exact provider key. Never use a loose pattern that could catch
a sibling (`OPENCODE_*` is safe; `OC*` is not, and `OPENROUTER_*` is a different provider).

Keep an explicit keep-list alongside the remove-list and verify it afterwards:

```bash
for v in KEEP_ONE KEEP_TWO; do grep -q "$v" <file> && echo "$v utuh" || echo "$v HILANG"; done
```

### 3. Back up before deleting

Copy each file you will touch into one timestamped directory, plus a snapshot of any table you will
modify. Removal must be reversible without reconstructing values from memory.

### 4. Distinguish a provider *definition* from a stored credential

Many CLIs list providers they are *capable* of using. That list is a **declaration**, and deleting
credentials does not remove it — it reappears the moment the variable is set again. Do not report
"still listed" as "still connected", and do not chase it by uninstalling the tool.

Proof: `auth logout <id>` fails with "Pass a credential ID or label" when nothing is stored, and the
`credential` table returns zero rows.

### 5. Verify by hash, never by value

```python
import hashlib
hashlib.sha256(val.encode()).hexdigest()[:10]
```

This answers "is the file's value the one I removed?" without printing it. Compare a live process's
value against the file's before assuming a leftover.

### 6. Verify in a fresh login shell

Edits to shell rc files only take effect in a **new** shell. Verify with a login shell, not the
current one:

```bash
zsh -lic 'eval "val=\$VAR"; [ -n "$val" ] && echo ADA || echo kosong'
```

## Pitfalls

- **A running service holds the old key in RAM.** `ps eww <pid>` keeps showing it after the file is
  clean. Hash-compare to prove it is a different value, then restart the process — never edit memory.
  A service that is not a launchd unit must be restarted by the user, and only when their work in it
  is finished.
- **Deleting the key does not undo an upstream block.** A per-IP or per-account block is lifted by
  the provider, not by removing credentials. Say this plainly instead of letting the user expect the
  deletion to fix it.
- **Trust the environment, not the UI list.** A connected-looking provider with no stored credential
  and an unset variable has no access.
- **Do not remove a sibling key by pattern.** Scope to the exact names; keep and verify the rest.
- **Backup first, always.** Removal without a timestamped copy is unrecoverable.

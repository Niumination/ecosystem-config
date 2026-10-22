---
name: opencode-troubleshooting
description: Fix OpenCode CLI/Desktop errors and config issues.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [opencode, cli, desktop, troubleshooting, config]
    related_skills: [hermes-agent, hermes-tool-backend-triage]
---

# OpenCode Troubleshooting

## When to Use
- OpenCode CLI or Desktop errors, crashes, or unexpected behavior
- After config changes or when switching between CLI and Desktop
- Free tier model errors, API key errors, snapshot failures
- MCP server connection failures

## Trigger
OpenCode CLI or Desktop errors, crashes, or unexpected behavior — especially after config changes or when switching between CLI and Desktop.

## Procedure

### Step 1: Read Logs First
- **CLI**: `~/.local/share/opencode/log/opencode.log`
- **Desktop**: `~/Library/Application Support/ai.opencode.desktop/logs/` — subdirectories named `YYYYMMDDHHMMSS/`
- Check both `main.log` and `renderer.log` for Desktop

### Step 2: Check Whether the Service Is Actually Running

"Service port already in use" is a *symptom*, not a diagnosis — before blaming a leftover
OpenCode process, find out who really owns the port. Do not assume your own edit caused it;
this error is frequently unrelated to any config or credential change.

```bash
# does the OS agree the port is free?
python3 -c "import socket;s=socket.socket();s.bind(('127.0.0.1',<port>));print('BEBAS');s.close()"

# who listens, and as which process?
lsof -nP -iTCP:<port> -sTCP:LISTEN
netstat -anv -p tcp | grep <port>
```

Then read the owning socket's service name from the last column of `netstat -anv`:

- **`io.tailscale.ipn:NNNN`** — a Tailscale system extension grabbed the port. OpenCode then cannot
  bind and fails with exactly this message. Stopping Tailscale frees it. Tailscale picks from the
  **same ephemeral range** the OS uses for `bind(port 0)` — confirm by binding port 0 a few times
  and noting the range — so this collision is rare but real.
- **`node`, `next-server`, `python`** — another local service holds it. Move OpenCode off the port
  (`opencode service set port <port>`) rather than killing the other process.
- `lsof` not showing the listener while `netstat` does is normal for system extensions; trust
  `netstat -anv`, it names the owning service.

**The `lsof`/`netstat` disagreement is the tell.** When `lsof -iTCP:<port>` reports only an
outbound connection to the port and no listener, but `netstat -anv` shows the port `LISTEN` with
a service name, the listener belongs to a system extension — not to any process you can `pgrep`.

### Step 3: Check Config Precedence
- `opencode.jsonc` **overrides** `opencode.json` — if both exist, only `.jsonc` is used
- To use `.json` instead: `mv opencode.jsonc opencode.jsonc.disabled`
- Config location: `~/.config/opencode/`

### Step 4: Check Model Availability
- Free tier models (`opencode/hy3-free`) only work inside Desktop app — CLI rejects them with "OpenCode's free tier can only be used from within OpenCode"
- For CLI, use a local provider (e.g., 9router at `http://localhost:20128/v1`)
- Check available models: `curl -s http://localhost:20128/v1/models`

### Step 5: Validate API Key Format
- OpenCode rejects dummy/test API keys even if the provider accepts them
- Use the real key from `~/.hermes/.env` or equivalent
- Check key exists: `grep '^PROVIDER_API_KEY=' ~/.hermes/.env`

### Step 6: Distinguish a Credential From a Provider Definition

`opencode auth list` showing a provider row does **not** mean a credential exists. It reports
provider *definitions* — what the CLI is capable of reading — so those rows persist after every
credential is deleted and will reappear as soon as the variable is set again.

```bash
opencode auth list --format json   # connections:[{"type":"env","name":"X"}] = a DECLARATION
opencode auth logout <id>          # fails "Pass a credential ID or label" = nothing stored to remove
```

Proof it is a definition, not a credential:

```bash
sqlite3 'file:~/.local/share/opencode/opencode.db?mode=ro' 'select id,integration_id,label from credential;'
zsh -lic 'for v in A B C; do eval "val=\$$v"; [ -n "$val" ] && echo "$v=ADA"; done'
```

Stored credentials live in `~/.local/share/opencode/opencode.db` table `credential`
(`integration_id='opencode'`, `label='Personal'` = the OAuth sign-in). A real API key lives in
`~/.local/share/opencode/auth.json`. Zero rows in `credential` and an empty env means the CLI
still *lists* the provider but has no access to it — the list is not evidence of a leak.

**A key a running process holds is not the key you deleted.** A long-lived `opencode serve` keeps
its environment in RAM, so `ps eww <pid>` still shows the variable after the file was cleaned.
Compare by hash, never by value:

```python
import hashlib, re, subprocess
pk = re.search(r'VAR=(\S+)', subprocess.run(['ps','eww',pid],capture_output=True,text=True).stdout).group(1)
print(hashlib.sha256(pk.encode()).hexdigest()[:10])
```

A different hash means it came from the interactive session, not from the file you edited. Search
for it in files (`val.encode() in open(p,'rb').read()`) — no match means it exists only in RAM and
the process must be restarted to release it. Never edit a process's memory; restart it, and only
when the user's work in it is done.

### Step 6a: IP-Level Abuse Blocks (Not Account, Not Config)

Error string: `"This isn't related to your account"` or `"detected abusive traffic from this IP address"`.
This is an **IP-level block** on OpenCode's free gateway — shared NAT IPs get flagged by other
users. Config and credentials are irrelevant. Diagnosis:

1. Confirm the error string in logs contains `abusive traffic` / `isn't related to your account`.
2. Check if other tools work from the same IP (e.g., 9router local, other APIs) — if they do, it's IP-specific to OpenCode.
3. Check if a VPN/proxy is active: `env | grep -iE "proxy|vpn"`.
4. Check current public IP: `curl -sS https://api.ipify.org`.

Solutions (in order of preference):
- Use a local provider (9router) — bypasses the block entirely.
- Restart router for a new IP (if ISP is dynamic).
- Wait — blocks can last hours to days with no guarantee.
- Subscribe to OpenCode Go for IP-independent access.

**Do not** waste time re-checking config or re-validating credentials when this error appears.

### Step 6b: Credential Cleanup Procedure

When the user asks to purge all API keys and OAuth tokens from OpenCode:

```bash
# 1. Delete all credential rows from the DB
sqlite3 ~/.local/share/opencode/opencode.db "delete from credential;"

# 2. Remove the auth.json file (contains zenmux API key)
rm -f ~/.local/share/opencode/auth.json

# 3. Remove any apiKey from provider config
#    (edit opencode.json — delete the "apiKey" line under provider options)

# 4. Grep for any remaining token strings in config
grep -rl "sk-\|zenmux" ~/.config/opencode/ 2>/dev/null

# 5. Verify environment has no OPENCODE/ZENMUX vars
env | grep -iE "OPENCODE|ZENMUX" || echo "(clean)"
```

After cleanup, verify with:
```bash
sqlite3 ~/.local/share/opencode/opencode.db "select count(*) from credential;"
# should be 0
```

### Step 7: Check Snapshot Errors
- Symlink paths cause `failed to capture snapshot` errors: `pathspec '...' is beyond a symbolic link`
- Add problematic paths to `ignore` array in config

## Pitfalls

- **JSONC overrides JSON**: If both `opencode.json` and `opencode.jsonc` exist, only `.jsonc` is used. Disable one to use the other.
- **Free tier is Desktop-only**: CLI rejects free tier models. Use a local provider (9router) for CLI usage.
- **Dummy keys rejected**: OpenCode validates API key format even if the provider doesn't enforce it. Always use the real key.
- **Model must exist in provider**: The model ID must exist in the provider's `/v1/models` endpoint. `combo-delegasi` is a Hermes concept, not a 9router model ID.
- **Symlinks break snapshots**: Paths under symlinks (e.g., `~/.config/zsh-abbr/`) cause `pathspec is beyond a symbolic link` errors. Add to `ignore` array.
- **Desktop logs are timestamped subdirectories**: Not flat files — look in `logs/YYYYMMDDHHMMSS/`.
- **MCP server errors are separate**: `spider` (401) and `computer` (cua-driver) errors are auth/daemon issues, not config issues.
- **A listed provider is not a credential**: `opencode auth list` reports definitions. Rows survive deletion of every credential. Check `credential` table and the environment instead of treating the list as evidence.
- **The port error is usually not your fault**: "Managed service port ... already in use" is most often a Tailscale system extension holding the port. Confirm the owner via `netstat -anv` before changing anything, and tell the user the change was unrelated to your earlier cleanup.
- **A running service keeps old env in RAM**: `ps eww <pid>` can show a key the files no longer contain. Hash-compare, and restart the service to release it rather than hunting the key in files that never had it.
- **OpenCode config does NOT interpolate env vars**: `"apiKey": "${VAR}"`, `"apiKey": "env:VAR"`, and `"apiKey": "VAR"` all send the literal string to the provider. The AI SDK `@ai-sdk/openai-compatible` reads `apiKey` directly from options, not from `process.env`. Setting `OPENAI_API_KEY` in the shell does NOT help when `apiKey` is absent from config. The only working approach is to write the literal key value into `opencode.json` — there is no env-var indirection. If the user refuses plaintext keys in config, the alternative is a shell wrapper that sets `OPENAI_API_KEY` AND the config has no `apiKey` field, but this only works if the SDK version supports env fallback (verify with a test call before assuming).

## Verification
After fixing config, verify with:
```bash
opencode run --model <provider>/<model> "Reply with exactly: OK"
```

## References
- `references/9router-config.md` — Working config for 9router as local free provider
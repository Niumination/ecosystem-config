---
name: hermes-configuration
description: "Configure Hermes for Niumination: model mapping, hooks, MCP."
version: "1.0.0"
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [hermes, configuration, model-mapping, hooks, mcp, ecosystem]
    homepage: https://github.com/Niumination/ecosystem-config
---

# Hermes Configuration & Maintenance

Configure and maintain Hermes Agent for the Niumination ecosystem. Covers model mapping, hook management, MCP server maintenance, and user-facing preferences.

## User Preference — Language & TTS

**Bahasa Indonesia** adalah default untuk user-facing response.
**TTS default:** `provider=piper`, `voice=en_US-lessac-medium`.
Fallback TTS: `provider=edge`, `voice=id-ID-ArdiNeural` (male Indonesian).
Voice candidates to avoid because they return `No audio was received` in this environment: `id-ID-BagusNeural`, `id-ID-JokoNeural`, `id-ID-GadisNeural`.

### TTS Fallback
Hermes tidak memiliki mekanisme fallback TTS eksplisit di config. Jika `edge-tts` gagal untuk voice tertentu, opsi yang bisa dipakai:
- ElevenLabs multilingual: `provider=elevenlabs`, `voice_id=pNInz6obpgDQGcFmaJgB`, `model_id=eleven_multilingual_v2`
- CLI fallback: `/Users/zaryu/src/hermes-agent/.venv/bin/edge-tts --voice id-ID-ArdiNeural --text "..." --write-media ...`

## Model Mapping — 9router Provider

When configuring or updating the 9router model mapping, follow these rules:

### Rule 1: Verify in Live Catalog First
Always probe `http://localhost:20128/v1/models` and confirm each model exists before adding to config. Current catalog state:
- Total models: ~372
- Active namespace: `explabs/`, `ag/`, `claude-combo`
- Deprecated namespaces: `gh/`, `kr/`, `gemini/`, `experimentallabs/`

### Rule 2: Use Verified Working Models Only
Current verified working config:
- Default: `explabs/gpt-5.4-mini`
- Vision: `explabs/claude-fable-5`
- Compression: `ag/gemini-3.7-flash-low`
- Delegation: `explabs/gpt-5.4-mini`
- X-search: `explabs/grok-4.20`
- Cron: `explabs/gpt-5.4-mini`
- Channel 1: `explabs/gpt-5.4-mini`
- Channel 802: `explabs/claude-haiku-4.5`
- Channel 803: `explabs/gpt-4o-mini`
- Channel 804: `explabs/claude-sonnet-4.6`
- Channel 1172: `explabs/gemma-4-31b`

### Rule 2b: Fallback Chain Must Be Verified Too
Set fallback models only after probing them live. Verified fallback chain:
- Fallback 1: `ag/gemini-3.8-flash-medium`
- Fallback 2: `ag/gemini-3.7-flash-medium`

### Rule 3: Do Not Use Retired Models
These models returned errors during live probe and should not be used:
- `ag/gemini-3.5-flash-extra-low` → retired
- `ag/gemini-3.5-flash-low` → retired
- `ag/gemini-3.5-flash-high` → retired
- `ag/gemini-3.5-flash` → retired

### Rule 4: Retry Before Changing Method
If a request fails with 503/NoneType parse errors, retry the same model up to 3 times before declaring it broken. Some routes are transient.

### Rule 5: Restart Only After Verifying Config
Only restart the Hermes gateway after `hermes config show` reflects the intended values.

### Rule 6: Channel Overrides Use Active Namespaces
Telegram channel overrides must use models from active namespaces (`explabs/`, `ag/`). Do not use deprecated namespaces `gh/`, `kr/`, `gemini/`, `experimentallabs/`.

## Hook Management

### Stale Hook Cleanup

Hooks referencing USB-mounted paths (`/Volumes/HermesAgent/HermesAgentUSB/data/agent-hooks/`) fail when USB is disconnected. **Pattern:**

1. Check `/Volumes/HermesAgent/HermesAgentUSB/data/agent-hooks/` exists
2. If not mounted, the hook commands will fail with `command not found`
3. Remove or disable hooks pointing to USB paths
4. Set `hooks_auto_accept: true` in config as fallback
5. Prefer local paths over USB paths for permanent hooks

### Hook Types

| Event | Purpose | Typical Path |
|-------|---------|-------------|
| `pre_tool_call` | Validate tool calls before execution | Local path preferred |
| `pre_llm_call` | Inject context before LLM call | Local path preferred |
| `on_session_end` | Capture session state | Local path preferred |

## MCP Server Management

### Disconnected MCP Servers

When MCP servers fail with `Connection closed` after 3 attempts, they enter parking mode. **Pattern:**

1. Check if the MCP server's backend service is running (PostgreSQL, SQLite, etc.)
2. If the service is unavailable, disable the MCP server in config (`enabled: false`)
3. Re-enable when the service is available
4. Monitor `~/.hermes/logs/errors.log` for `MCP server.*failed initial connection`

### Known Failing MCP Servers (Niumination)

| Server | Backend | Status | Fix |
|--------|---------|--------|-----|
| `hermes-postgres` | PostgreSQL | Disconnected | Install local PostgreSQL or disable |
| `hermes-sqlite` | SQLite | Disconnected | Check SQLite availability |
| `time` | Local | Disconnected | Check time server availability |
| `filesystem` | Local | Active | No action needed |
| `github` | GitHub API | Active | No action needed |
| `context7` | Remote | Active | No action needed |

## Configuration Update Workflow

1. **Backup** `~/.hermes/config.yaml` before any changes
2. **Edit** config using `hermes config set <path> <value>` (preferred) or direct file edit
3. **Validate** YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('/Users/zaryu/.hermes/config.yaml'))"`
4. **Verify** all models in fallback chain exist in 9router catalog
5. **Verify** all channel overrides use independent quota backends
6. **Restart** gateway if needed: `hermes gateway restart` (from separate shell)
7. **Monitor** `~/.hermes/logs/errors.log` for new errors

### Config Restoration from Backup

When config drifts (e.g., model provider changed unexpectedly):

1. **Identify drift**: `diff ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.<timestamp>`
2. **Restore fields** using `hermes config set`:
   ```bash
   hermes config set model.provider 9router
   hermes config set model.default explabs/gpt-5.4-mini
   hermes config set model.base_url http://localhost:20128/v1
   hermes config set model.api_mode chat_completions
   ```
3. **Validate**: `python3 -c "import yaml; yaml.safe_load(open('/Users/zaryu/.hermes/config.yaml'))"`
4. **Verify models**: `curl -s http://localhost:20128/v1/models | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d['data']), 'models')"`
5. **Test provider**: Send a test request to verify API key loads correctly

Backup file patterns:
- `config.yaml.bak.<YYYY-MM-DD_HHMMSS>` — timestamped auto-backups
- `config.yaml.bak-<description>` — manual backups with context

### Config Drift Detection & Nous Portal Sync (verified 9 Sep 2026)

When `hermes status` shows a different model/provider than `hermes config show`, the config.yaml has drifted from runtime state. Common cause: model changed via Nous Portal web UI or OAuth2 flow without updating config.yaml.

**Detection:**
```bash
hermes config show 2>&1 | grep -A4 "Model:"
hermes status 2>&1 | grep -A2 "Model:"
```
Compare provider, default model, and base_url. If they differ → drift exists.

**Fix — sync config.yaml to match runtime:**
```bash
hermes config set model.provider nous
hermes config set model.default inclusionai/ling-3.0-flash-fin:free
hermes config set model.base_url https://inference-api.nousresearch.com/v1
hermes config set model.key_env NINE_ROUTER_API_KEY
hermes config set model.api_mode chat_completions
```

**Verification:**
```bash
hermes config show 2>&1 | grep -A4 "Model:"
hermes status 2>&1 | grep -A2 "Model:"
```
Both must agree. Always backup first: `cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak-YYYY-MM-DD`.

**Nous Portal setup for `config.yaml`:**
Nous Portal is OAuth2 (token lives in `hermes auth` state, NOT config.yaml providers section), BUT `model.provider: nous` works in config.yaml with `key_env: NINE_ROUTER_API_KEY` pointing to `https://inference-api.nousresearch.com/v1`. The Nous inference API accepts the same API key as the portal.

**Critical rule:** NEVER edit config.yaml directly — security filter REFUSES `write_file`/`patch` on config.yaml. ALWAYS use `hermes config set`. Verify with `hermes config show` and `hermes status` after changes.

**⚠️ Pitfall 23: OpenCode Go `x-opencode-session` header required from 09/06/2026 (NOT YET FIXED locally)**

OpenCode Go relay requires `x-opencode-session` header on every request. Starting 09/06/2026, requests without it will error. Fix exists in PR #101864, but:
- Local Hermes does NOT have the fix
- Provider files (`opencode-free`, `opencode-zen`, `opencode-go` plugins) don't include session header logic

This affects `opencode-free`, `opencode-zen`, `opencode-go` providers. **NOT** the Nous Portal provider.

To fix: patch `plugins/model-providers/opencode-*.py` to add `x-opencode-session` header, or wait for upstream merge.

**⚠️ Pitfall 25: Never trust `hermes --version Up to date` as upstream sync proof**

`hermes --version` compares against the installed package version, not `upstream/main` HEAD. Always verify with `git -C ~/src/hermes-agent rev-list --count HEAD..upstream/main` after `git -C ~/src/hermes-agent fetch upstream main`. A zero count means in sync; any nonzero count means an update exists even when the CLI says up to date.

**⚠️ Pitfall 26: `key_env: NINE_ROUTER_API_KEY` correct for Nous Portal**

After `hermes config set model.provider nous`, `key_env: NINE_ROUTER_API_KEY` is correct.

**⚠️ Pitfall 27: OpenCode 400 MissingSessionID — remove provider, don't reconfigure**

OpenCode free tier produces `400 MissingSessionID` non-retryable errors via REST API. The free tier only works in the OpenCode app, not REST API. **Fix: remove the provider entirely** via `hermes config unset providers.opencode-zen` (`remove` is not a valid `hermes config` subcommand; valid: show/edit/get/set/unset/path/env-path/check/migrate) and unset `OPENCODE_API_KEY` from `env_passthrough`. Do NOT attempt to reconfigure.

**⚠️ Pitfall 28: `snowballstemmer` dependency missing after update**

After `hermes update`, `import snowballstemmer` may fail in `tools/tool_search.py` even though pinned in `pyproject.toml`. This causes "Tool search assembly skipped" warnings. **Fix:** `uv pip install snowballstemmer==3.1.1`. Verify: `.venv/bin/python -c "import snowballstemmer; print('OK')"`. Source-distribution builds can far exceed foreground tool timeouts (a `nemo-relay` build took 17+ minutes) — run the install as a background task with a long timeout and verify the import afterwards instead of retrying in the foreground.

**⚠️ Pitfall 29: Post-update gateway race condition — "Normal final-send NOT suppressed"**

After `hermes update`, if gateway logs show `Normal final-send NOT suppressed despite active stream consumer` with `content_delivered=False`, the root cause is a **two-phase race condition**:

1. `_finalize_edit(record=False)` → `_send_or_edit` return False → `_final_content_delivered` NOT set
2. `delivered_final_matches` returns `False` (payload mismatch from plugin hooks) → `_stale_finalized=True` → `_content_delivered=False`

**Fix layers (applied to `gateway/stream_consumer.py` and `gateway/run_turn.py`):**
- `_finalize_edit`: When `_use_native_streaming=True` and `_send_or_edit` fails, set `_final_content_delivered=True`
- `_run_agent_mark_streamed_delivery`: Add `has_delivered_text(final)` fallback for `_content_delivered`
- `_run_agent_deliver_final_send`: When `_stale_finalized=True` AND `_sc._final_response_sent=True`, suppress normal final send

**Verification:** Send a Telegram message; check gateway.log for absence of the warning.

**⚠️ Pitfall 30: Startup notification not sent after Mac wake/reboot — missing `home_channel`**

When Hermes gateway starts (or Mac wakes from sleep), `_send_home_channel_startup_notifications()` checks `platform_cfg.home_channel`. If `home_channel` is `None` or has no `chat_id`, the platform is **silently skipped** — no "♻️ Gateway online" message is sent.

**Root cause:** `_home_channel_transports()` in `gateway/run_notifications.py` filters with `if not home or not home.chat_id: continue`. If `~/.hermes/config.yaml` platforms section lacks `home_channel`, the notification is never delivered.

**Fix:** Set `home_channel` in config.yaml:
```bash
hermes config set platforms.telegram.home_channel.chat_id <your_chat_id>
```
Or manually edit `~/.hermes/config.yaml`:
```yaml
platforms:
  telegram:
    home_channel:
      chat_id: <your_chat_id>
```

**⚠️ CRITICAL: `home_channel` MUST include the `platform` field.** The gateway config parser at `gateway/config.py:309` does `data["platform"]` in `HomeChannel.from_dict()`. Without a `platform` key, it crashes with `KeyError: 'platform'` and the gateway enters a crash-loop (ExitStatus 256, restart every few seconds). After `hermes config set platforms.telegram.home_channel.chat_id`, ALWAYS set the platform:
```bash
hermes config set platforms.telegram.home_channel.platform telegram
```
Verify with:
```bash
python3 -c "
import yaml
with open('/Users/zaryu/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
hc = cfg['platforms']['telegram']['home_channel']
print('home_channel:', hc)
print('Has platform:', 'platform' in hc)
"
```

**Verification:** After setting, restart gateway (`hermes gateway restart`) and check that `_home_channel_transports()` yields the platform (log line "Sent home-channel startup notification"). Also confirm no `KeyError` entries in `gateway.error.log`.

**⚠️ Pitfall 31: Always scope git to the Hermes checkout with `git -C`**

The terminal session cwd is often a different repo (dotfiles, ecosystem). Run every Hermes repo check as `git -C /Users/zaryu/src/hermes-agent <subcommand>` — a bare `git log/remote/rev-list` silently reports the wrong repo and fabricates upstream/ahead counts.

**⚠️ Pitfall 32: Pre-update health gate — disk, logs, state.db before `hermes update`**

A full Data volume or multi-MB logs abort or stall the update. Check `df -h /System/Volumes/Data`, `ls -lh ~/.hermes/logs/gateway.error.log ~/.hermes/logs/errors.log`, and `ls -lh ~/.hermes/state.db` first — free space and rotate logs when the Data volume is above 85% or `gateway.error.log` exceeds ~5 MB, and schedule `VACUUM` when `state.db` grows tens of MB between audits.

**⚠️ Pitfall 33: Missing `/Volumes/HermesAgent` on native Mac is normal, not a fault**

Native installs never mount the old portable-USB path. Treat its absence as confirmation of native mode; only USB-path hooks still pointing there are faults to remove.

**⚠️ Pitfall 34: Judge the duplicate-send fix by fresh tail, not total grep count**

`grep -c "Normal final-send NOT suppressed"` accumulates history and stays nonzero after the fix. Verify with `tail` plus timestamp after a gateway restart and a test Telegram message — only a fresh line with the current timestamp means the race is still live.

### Known Provider Configurations

| Provider | Base URL | api_mode | Key Env |
|---|---|---|---|
| `9router` | `http://localhost:20128/v1` | `chat_completions` | `NINE_ROUTER_API_KEY` |
| `opencode-zen` | `https://opencode.ai/zen` | `chat_completions` | `OPENCODE_API_KEY` |
| `opencode-go` | `https://opencode.ai/zen/go` | `chat_completions` | `OPENCODE_API_KEY` |
| `opencode-free` | `https://opencode.ai/zen/v1` | `chat_completions` | *(keyless)* |
| `nous` | `https://inference-api.nousresearch.com/v1` | `chat_completions` | `NINE_ROUTER_API_KEY` |
| `agentrouter` | `https://agentrouter.org/v1` | `chat_completions` | `AGENTROUTER_API_KEY` |
| `huancheng` | `https://api.hcnsec.cn/v1` | `chat_completions` | `HUANCHENG_API_KEY` |

## Pitfalls

- **Shared Google quota:** `ag/gemini-*` models all share one quota pool → mix with `gh/*`, `gemini/*`, `kr/*`
- **USB-mounted hooks:** `/Volumes/HermesAgent/HermesAgentUSB/` may not be mounted → use local paths or `hooks_auto_accept: true`
- **MCP parking mode:** Failed MCP servers park until reconnect → disable if backend unavailable
- **Config file path:** Always use `~/.hermes/config.yaml`, not `/Volumes/HermesAgent/...`
- **Default model:** Should be a verified model in the 9router catalog, not a generic/combo model
- **Config version does NOT auto-populate runtime fields:** `_config_version` migration steps only handle specific schema fields. `home_channel` (PlatformConfig field) is NOT in DEFAULT_CONFIG and must be set separately via `/set home` or direct config.yaml edit. It is NOT preserved through updates.
- **`home_channel` requires a `platform` field:** `gateway/config.py:309` (`HomeChannel.from_dict()`) accesses `data["platform"]` unconditionally. If `home_channel` lacks `platform`, the gateway crashes with `KeyError: 'platform'` on every startup attempt (crash-loop, ExitStatus 256). Always set BOTH `chat_id` AND `platform` when configuring `home_channel`. Use `hermes config set platforms.telegram.home_channel.platform telegram` after setting `chat_id`.
- **Update does NOT reset existing config:** `hermes update` calls `_check_and_apply_config_migration()` which deep-merges defaults and runs migration steps. It does NOT wipe or reset user-configured values. The issue is missing fields (like `home_channel`) that were never in DEFAULT_CONFIG, not deleted fields.
- **`snowballstemmer` missing after update:** Pinned in pyproject.toml but `uv pip install` may not pull it if the venv was cached. Fix: `uv pip install snowballstemmer==3.1.1` from project root.
- **Gateway auth allowlists live in ENV, not config.yaml:** `_is_user_authorized` (`gateway/authz_mixin.py`) reads `TELEGRAM_ALLOWED_USERS` / `GATEWAY_ALLOWED_USERS` via `_platform_gate_env`. A `platforms.<name>.allowed_users` key in config.yaml is silently ignored — never set it expecting enforcement.
- **Stale `resume_pending` with null origin `user_id`:** the startup `Skipping auto-resume ... no longer authorized` warning fires before any allowlist is checked when the stored `gateway_routing` origin lacks `user_id`. It is harmless (inbound auth uses the live source); let the freshness window expire instead of editing `state.db` under a running gateway.

## Verification

```bash
# Check config validity
python3 -c "import yaml; yaml.safe_load(open('/Users/zaryu/.hermes/config.yaml'))"

# Verify config version (should be 41 for v0.21.x; unchanged across major updates)
hermes config check 2>&1 | grep "Config version"
grep "_config_version" ~/.hermes/config.yaml

# Verify models in catalog
curl -s http://localhost:20128/v1/models | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d['data']), 'models')"

# Check for hook errors
grep -c "shell hook failed" ~/.hermes/logs/errors.log

# Check for MCP errors
grep -c "MCP server.*failed" ~/.hermes/logs/errors.log

# Verify fallback chain
grep -A 20 "^fallback_providers:" ~/.hermes/config.yaml

# Verify gateway startup notifications work (after setting home_channel)
grep "startup notification\|home_channel" ~/.hermes/logs/gateway.log | tail -5

# Verify snowballstemmer is installed (after update)
.venv/bin/python -c "import snowballstemmer; print('OK')"

# Check for missing dependencies after update
.venv/bin/python -c "import tools.tool_search; print('tool_search OK')"

# Verify gateway duplicate-send fix applied (fresh tail only — total count keeps history)
grep "Normal final-send NOT suppressed" ~/.hermes/logs/gateway.log | tail -5
# After fix + gateway restart + test Telegram message, no NEW timestamped line should appear.
# A stale count from `grep -c` alone is not failure evidence.

# Pre-update health gate (disk, logs, state.db)
df -h /System/Volumes/Data | tail -1
ls -lh ~/.hermes/logs/gateway.error.log ~/.hermes/logs/errors.log ~/.hermes/state.db

# Scope every repo check to the Hermes checkout (session cwd is often another repo)
git -C /Users/zaryu/src/hermes-agent status --short --branch
git -C /Users/zaryu/src/hermes-agent log --oneline -3
git -C /Users/zaryu/src/hermes-agent rev-list --count HEAD..upstream/main

# Verify home_channel is set AND has required 'platform' field (critical)
python3 -c "
import yaml
with open('/Users/zaryu/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
tel = cfg.get('platforms', {}).get('telegram', {})
hc = tel.get('home_channel', {})
print('home_channel:', hc)
print('Has platform field:', 'platform' in hc)
if 'platform' not in hc:
    print('CRITICAL: Missing platform field! Gateway will crash with KeyError.')
    print('Fix: hermes config set platforms.telegram.home_channel.platform telegram')
"

# Check gateway running processes
ps aux | grep "gateway run" | grep -v grep | awk '{print $2}'

# Check git status of local hermes-agent repo
cd ~/src/hermes-agent && git status --short && git log --oneline -1
```

## Reference Files

- `references/9router-model-mapping.md` — Full model catalog and quota backend analysis
- `references/hook-and-mcp-fix.md` — Detailed hook cleanup and MCP server management procedures
- `references/opencode-provider-config-2026-09-08.md` — OpenCode base_url fix (`/zen` not `/zen/v2`), key_env correction
- `references/gateway-notification-system.md` — How startup notifications work, home_channel flow, and duplicate-send prevention
- `references/config-migration-internals.md` — `_config_version` system, MIGRATIONS registry, and how config changes propagate through updates

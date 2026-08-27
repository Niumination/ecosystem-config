# Niumination Central Credential Broker — Design & Plan

_Last updated: 2026-08-27 · Status: scaffolded (broker working), migration pending approval_

## 1. Current state (the "berantakan" map)

Credentials are scattered across **8+ stores**, with the same key duplicated
and several plaintext files holding secrets:

| Store | Holds | Risk |
|-------|-------|------|
| `~/.hermes/.env` | OPENCODE_ZEN, TELEGRAM, GOOGLE/GEMINI, GITHUB, FAL, TAVILY, OPENCODE_API | plaintext, duplicated |
| `~/Desktop/Niumination/vault/secrets.zsh` | OPENCODE_API, ANTHROPIC, (others) | plaintext (600 ok, but duplicated) |
| `~/.gemini/.env` | GEMINI_API_KEY | plaintext |
| `~/.continue/.env` | OPENCODE_ZEN_API_KEY | plaintext |
| `~/.deepseek/config-9router.toml` | openai/huancheng api_key | plaintext |
| `~/.jcode/config.toml` | huancheng api_key_env + env_file | points elsewhere |
| `~/.config/opencode/opencode.jsonc` | 9router apiKey, huancheng apiKey | plaintext in JSON |
| macOS Keychain | partial: `opencode-zen`, `gemini`, `flame-ade` | encrypted (good, but unused by most tools) |

Problems: duplication (OPENCODE_ZEN in 3 files), plaintext at rest,
no single rotate/revoke point, no audit of what exists.

## 2. The model: "broker" not full centralization

Not every credential should move into one box:

- **Direct AI-API keys** (OpenRouter, Gemini, OpenCode Zen, FAL, Telegram,
  AgentRouter, Juan, NineRouter, Huancheng, Aerolink, Tavily, Anthropic,
  Vercel, Discord, Bing, NVIDIA NIM) → **go through the broker**.
  These are flat API keys with no per-tool state; ideal to centralize.
- **9router's own upstream keys** → stay inside 9router's encrypted store.
  The broker exposes ONLY `nine_router` (its local `sk-...` token). 9router
  remains the aggregator/fan-out; the broker never reaches into it.
- **OAuth tokens** (Google, GitHub device flow used by some tools) → stay in
  their tool's native secure store / Keychain item; broker can reference them
  but does not manage refresh. This avoids re-implementing OAuth.

So "one control plane" = **the broker is the single source for flat API keys**,
and 9router is the single fan-out for model routing. Two clear tiers.

## 3. Mechanism

`scripts/keys.sh` (Ponytail: ~110 lines, no deps):
- Backed by **macOS Keychain** (`security`) — encrypted at rest, no sudo,
  survives reboot. Proven working on this Mac.
- Falls back to a plaintext file only if `security` is absent (CI/non-macOS).
- `keys set/get/del/list/env <canonical>`.
- `keys env` emits `export ALIAS=value` for every alias a tool expects
  (e.g. `opencode_zen` → `OPENCODE_ZEN_API_KEY`, `OPENCODE_API_KEY`,
  `OPENCODE_GO_API_KEY`). This is how tools consume the broker without
  editing each config to point at it.

## 4. Rollout (phased, reversible)

**Phase A — foundation (done):**
- `scripts/keys.sh` written + tested (set/get/env/del roundtrip).
- `vault/` perms fixed 755→700 (was world-readable).

**Phase B — migration (needs approval + real values):**
For each canonical, read value from its current store, `keys set`, then
repoint the consumer:
- jcode `~/.jcode/config.json`: switch providers to `key_env` pointing at
  broker-emitted vars (already uses `key_env` for 9router/agentrouter/juan).
- opencode `opencode.jsonc`: replace inline `apiKey` with `${ENV}` via
  `key_env` or env injection.
- hermes `~/.hermes/.env`: replace with a single `source <(keys env)` line.
- gemini/continue/9router-config: consume broker vars; delete plaintext.
- Keep `vault/secrets.zsh` only as an offline backup, not sourced at runtime.

**Phase C — enforcement:**
- Add `keys env` to shell profile so all interactive/launched tools inherit.
- launchd plists for 9router/hermes get `keys env` piped into EnvironmentVariables.
- A `scripts/keys.sh audit` (future) to detect plaintext leaks.

## 5. Why Keychain over alternatives
- `op`/`bw` (1Password/Bitwarden): not installed; adds a paid dependency.
- `age`/`sops`: great but needs a key to be present somewhere anyway.
- Keychain: already on the machine, encrypted, no sudo, already partially
  used. Lowest-friction single source for this single-user Mac.

## 6. Security notes
- Broker never writes values to disk in plaintext (except CI fallback).
- Each tool still authenticates normally; the broker only *distributes* the
  secret it already had. Blast radius of a leak = one canonical, revocable
  via `keys del` + provider rotate.
- 9router local token (`sk-...`) is itself a broker-managed canonical, so
  revoking/rotating 9router is one command.

# 9Router 3-Agent Hybrid Auto-Detect — 28 Aug 2026

## Summary
Integrate 9Router (`http://localhost:20128/v1`, 78 models, 7 connections) to Hermes + JCode + OpenCode with auto-detect of new models via hybrid watcher (DB WatchPaths + 60s poll + sha256 hash). Fixes key mismatch and JCode dual-env pitfall.

## DB Schema (verified)
- `providerConnections`: 7 rows — `gemini(gemini-aistudion) on`, `kimi(Account1) on`, `github(Niumination) on`, `ollama(ollama-cloud) on`, `nvidia(nim) on`, `antigravity(archk4li@gmail.com) on`, `codebuddy-intl(Account1) off`
- `apiKeys`: 1 row — `sk-8948a1f10508b1c5-tr1j0r-73039dc6` (Default Key)
- `providerNodes`: 0 rows (empty — connections used)
- `kv`: `disabledModels|gemini|[gemini-3.5-flash-lite, ...]`
- File: `~/.9router/db/data.sqlite` + WAL at `data.sqlite-wal`

## Root Cause That Blocked Integration
1. **Key mismatch**: `~/.hermes/.env` had `sk-...lric3a-40799d48` (stale), DB had `sk-...tr1j0r-73039dc6` → `POST /v1/chat/completions` 401 `Invalid API key` while `GET /v1/models` (no auth) still showed 78 models — masked the error.
2. **JCode dual-env**: `jcode provider add 9router --api-key-env NINE_ROUTER_API_KEY` creates `~/.config/jcode/9router.env` but `jcode auth-test` also checks `OPENAI_COMPAT_API_KEY` (openai-compatible type default). Without both vars → `Missing bearer authentication`. Fix: `9router.env` must contain `NINE_ROUTER_API_KEY=<key>` + `OPENAI_COMPAT_API_KEY=<key>`.
3. **OpenCode apiKey literal**: `opencode.jsonc` provider needs literal `apiKey` string (not env-tmpl) — manual patch required.

## Fix Steps (repro)
```bash
DB_KEY=$(sqlite3 ~/.9router/db/data.sqlite "SELECT key FROM apiKeys LIMIT 1;" | tr -d '\r\n')
# 1. Hermes
python3 -c "import re,pathlib,subprocess; db=subprocess.check_output(['sqlite3','/Users/zaryu/.9router/db/data.sqlite','SELECT key FROM apiKeys LIMIT 1;']).decode().strip(); p=pathlib.Path('/Users/zaryu/.hermes/.env'); t=p.read_text(); p.write_text(re.sub(r'^NINE_ROUTER_API_KEY=.*',f'NINE_ROUTER_API_KEY={db}',t,flags=re.MULTILINE))"
# 2. Vault
# patch vault/secrets.zsh export NINE_ROUTER_API_KEY="..."
# 3. JCode
echo "NINE_ROUTER_API_KEY=$DB_KEY" > ~/.config/jcode/9router.env
echo "OPENAI_COMPAT_API_KEY=$DB_KEY" >> ~/.config/jcode/9router.env
jcode provider add 9router --base-url http://127.0.0.1:20128/v1 --model gemini/gemini-3.6-flash -p openai-compatible --api-key-env NINE_ROUTER_API_KEY
jcode --provider-profile 9router run 'Say PONG' # expect PONG
# 4. OpenCode
# patch ~/.config/opencode/opencode.jsonc: provider.9router.options = {baseURL, apiKey: DB_KEY}
```

## Hybrid Watcher
- **Script** `~/Desktop/Niumination/scripts/9router-sync.sh` (chmod +x):
  ```bash
  curl -s http://127.0.0.1:20128/v1/v1/models | python3 -c "print(sorted IDs)" | sha256sum
  # compare ~/.cache/niumination/9router-models.hash
  # on change: write json + .9router-state.json + osascript notification + log
  ```
- **LaunchAgent** `~/Library/LaunchAgents/com.niumination.9router-watch.plist`:
  ```xml
  WatchPaths: [data.sqlite, data.sqlite-wal]
  StartInterval: 60
  RunAtLoad: true
  ProgramArguments: [/Users/zaryu/Desktop/Niumination/scripts/9router-sync.sh]
  ```
  `launchctl load ...` → `launchctl list | grep 9router` shows `- 0 com.niumination.9router-watch` (on-demand, normal)
- **up-eco** tail: `if [ -x "$ROOT/scripts/9router-sync.sh" ]; then ... echo "9router: $cnt models"; fi`

## Model Catalog (78)
`gemini/*` (5), `kimi/*` (8), `gh/*` (~27 copilot/gpt-4o/mai-code/trajectory), `nvidia/*` (6), `ollama/*` (6), `ag/*` (16 antigravity Claude/Gemini). Full list in `~/.cache/niumination/9router-models.json`.

## Verification
- `curl /v1/models | wc -l` → 78
- `jcode --provider-profile 9router run 'Reply exactly JCODE9_OK'` → JCODE9_OK
- `curl -H "Authorization: Bearer $DB_KEY" -d '{"model":"gemini/gemini-3.6-flash","messages":[{"role":"user","content":"Reply HERMES9_OK"}]}' http://127.0.0.1:20128/v1/chat/completions` → SSE contains HERMES9_OK
- `cat ~/.cache/niumination/9router-models.hash` → cbb3f776...
- `launchctl list | grep niumination` → - 0 com.niumination.9router-watch

## Related
- `hermes-provider-config` Pitfalls 4,8 (AgentRouter UA) + new 9Router section
- `provider-fallback` (fallback chain)
- `ecosystem-recovery` workflow step 11 (verify 9router sync)
- Commit `2e053d7 feat(9router): integrasi 3 agent + hybrid auto-detect`

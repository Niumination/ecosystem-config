# Dead Model Mapping — Full Recipe

Situation: `HTTP 404: No active credentials for provider: <name>` on a cron job, a Telegram
channel, delegation, or x_search, after that provider disappeared from the catalog.

## 0. Back up before touching config

```bash
cd ~/.hermes && cp config.yaml "config.yaml.bak-mapping-repair-$(date +%Y%m%d-%H%M%S)"
```

## 1. Inventory the mapping sites

```bash
grep -n -i '<dead-provider>' ~/.hermes/config.yaml
```

All of these store a **model+provider pair**:

- `cron.model` + `cron.model_provider`
- `auxiliary.<name>.model` + `.provider` (+ `.base_url`, `.api_key`)
- `x_search.model` (+ `provider` when present)
- `platforms.telegram.channel_overrides.<id>.model` + `.provider`

Dump them all at once:

```bash
python3 - <<'PY'
import yaml, pathlib
c = yaml.safe_load((pathlib.Path.home()/'.hermes/config.yaml').read_text())
print('cron          :', c['cron'].get('model'), '|', c['cron'].get('model_provider'))
for name, cfg in (c.get('auxiliary') or {}).items():
    if isinstance(cfg, dict) and cfg.get('model'):
        print(f'auxiliary.{name}:', cfg.get('model'), '|', cfg.get('provider'))
print('x_search      :', (c.get('x_search') or {}).get('model'), '|', (c.get('x_search') or {}).get('provider'))
for cid, cfg in ((c.get('platforms') or {}).get('telegram', {}).get('channel_overrides') or {}).items():
    print(f'channel {cid:5} :', cfg.get('model'), '|', cfg.get('provider'))
PY
```

## 2. Evidence of real damage (also the report material)

```bash
# credential errors that actually happened, per provider
grep -rhoE 'No active credentials for provider: [a-z0-9-]+' ~/.hermes/logs/*.log | sort | uniq -c | sort -rn

# which models recent sessions really used (state.db = runtime source of truth)
python3 -c "import sqlite3,pathlib,collections; c=sqlite3.connect(f'file:{pathlib.Path.home()}/.hermes/state.db?mode=ro',uri=True); print(collections.Counter(r[0] for r in c.execute('SELECT model FROM sessions ORDER BY rowid DESC LIMIT 200')))"
```

Sessions with `source='cron'` on the dead model mean the path is genuinely broken, not theoretical.

## 3. Candidate replacements

```bash
set -a; . ~/.hermes/.env; set +a
python3 ~/.hermes/skills/ecosystem/model-mapping-repair/scripts/probe-tool-calling.py \
  --base-url https://inference-api.nousresearch.com/v1 --auth-json nous \
  inclusionai/ling-3.0-flash-fin:free meituan/longcat-2.0:free
```

- Free tier: only `:free` models pass; the rest answer `404 … requires available credits`.
- Reasoning models may need a bigger `--max-tokens` before content/tool calls appear.
- Keep only models that returned `tool_calls`, not merely text.

### Verified free-tier inventory (re-probe before trusting — providers rotate models)

**nous** (`--auth-json nous`, base `https://inference-api.nousresearch.com/v1`): 7 `:free` models,
all tool-calling OK — `inclusionai/ling-3.0-flash-fin:free`, `inclusionai/ling-3.0-flash-sante:free`,
`meituan/longcat-2.0:free`, `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`,
`stepfun/step-3.7-flash:free`, `upstage/solar-pro4:free`. The catalog lists ~400 models; every
non-`:free` entry answers `404 … requires available credits` on a credit-less account.

**OpenRouter** (`--key-env OPENROUTER_API_KEY`, base `https://openrouter.ai/api/v1`): 22 `:free`
models, 12 tool-calling OK — `deepseek/deepseek-v4-flash-0731:free`,
`nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia/nemotron-3.5-lightning:free`,
`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`, `nex-agi/nex-n2.5-pro:free`,
`nex-agi/nex-n2.5-mini:free`, `poolside/laguna-xs-2.1:free`, `inclusionai/ling-3.0-flash-fin:free`,
`inclusionai/ling-3.0-flash-sante:free`, `inclusionai/ling-3.0-flash-vl:free`,
`liquid/lfm-2.5-2.6b:free`, `dots-studio/dots-3-note-preview:free`. Rejections, by class:
`429 Provider returned error` (transient — retry later), `404 No endpoints found that support tool
use` (`z-ai/glm-5.2:free` — listed but unusable for agents), `403 … only available to subscribers`
(`thinkingmachines/inkling*:free`), and 200-with-empty-body (`cohere/north-mini-code:free`,
`nvidia/nemotron-3-super-120b-a12b:free` — answers text, emits no tool call).

**OpenCode `*-free` (opencode-free / opencode-zen): unusable from Hermes.** Upstream gates the free
tier to its own client — every outside caller gets `403 FreeTierError — "OpenCode's free tier can only
be used from within OpenCode"` (older wording: `400 … can only be used in OpenCode`) regardless of
headers, including the keyless header set the `opencode-free` provider sends. Never map these; pick
nous/OpenRouter `:free` instead.

## 4. Apply

Edit with python (replace + `assert t.count(old) == 1`), then:

```bash
python3 -c "import yaml,pathlib; yaml.safe_load((pathlib.Path.home()/'.hermes/config.yaml').read_text()); print('YAML valid')"
grep -c -i '<dead-provider>' ~/.hermes/config.yaml   # must be 0
```

## 5. Verification ladder (do not stop at the probe)

1. **Real CLI session**: `timeout 90 hermes -m <model> --provider <provider> -z "Balas: OK" </dev/null`
   → text returned. The `</dev/null` and `timeout` are load-bearing: without them the CLI can hang on
   stdin and eat the whole turn (observed >6 minutes with no output).
2. **Real cron run** without polluting the channel: `cronjob_manage action=update deliver=local` →
   `action=run` → check `last_status` / `failure_streak` in `~/.hermes/cron/jobs.json` →
   `action=update deliver=origin`.
3. **Scheduled jobs on the same code path** confirm on their own schedule — say that, do not claim it.

## 6. Close the loop

- Record the active mapping (location, model, provider) in the ecosystem mapping registry
  (`docs/registry/model-mapping.md`), plus a "do not use anymore" list with the reason.
- Report the config backup path.
- Leave misleading-but-harmless lines alone and document them (e.g. a `key_env` that names another
  provider's key while OAuth in `auth.json` is what actually authenticates). If the owner asks for
  that fix, delete the line rather than repointing it — an OAuth provider needs no `key_env` — then
  re-run one real session to prove auth still resolves.

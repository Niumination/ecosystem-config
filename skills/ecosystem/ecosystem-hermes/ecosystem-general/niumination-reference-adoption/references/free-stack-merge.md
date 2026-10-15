# hermes-free-stack.zip — Merge Notes (REFERENCE ONLY)

Source: `~/Downloads/hermes-free-stack.zip` → extracted `hermes-free-stack/`:
- `INSTRUKSI_UNTUK_HERMES.md` — main instruction (copied to `~/Downloads/INSTRUKSI_UNTUK_HERMES.md`)
- `MERGE_INTO_CONFIG.yaml` — YAML snippet to merge into `~/.hermes/config.yaml`
- `ENV_KEYS.env` — env var names only (NO keys): `GOOGLE_API_KEY`, `NVIDIA_API_KEY`, `GROQ_API_KEY`, `GLM_API_KEY`, `OPENROUTER_API_KEY`, `NINEROUTER_API_KEY`
- `9ROUTER_MODELS.md` — 9Router model catalog

## What it wants to do
Replace `model`, `fallback_providers`, `auxiliary`, `model_aliases` in config.yaml; merge `providers` (groq, nvidia, gemini, zai, openrouter, **ninerouter**). Probe 9Router at `http://127.0.0.1:20128/v1/models` (use 127.0.0.1 not localhost — avoid IPv6). If alive, PREPEND ≤2 `kr/*` / `free-combo` entries as `provider: custom` + `base_url` + `key_env: NINEROUTER_API_KEY`.

## Why REFERENCE-ONLY (do not auto-apply)
1. `~/.hermes/config.yaml` is **agent-blocked** for direct edits — must use `hermes config set`, not YAML writes.
2. Current routing already works & verified: `huancheng/auto` (primary) → `9router` → `opencode-zen/hy3-free`.
3. Needs `GOOGLE_API_KEY` filled in `~/.hermes/.env` (placeholders only, never fake keys).
4. Some model IDs in the snippet are stale (claims `opencode-free`; live is `opencode-zen` with `OPENCODE_ZEN_API_KEY`).

## 9Router model catalog (from 9ROUTER_MODELS.md)
| Prefix | Source | Login | Good models |
|---|---|---|---|
| `kr/` | Kiro AI (free ~50 credits/mo) | Google/GitHub/AWS | kr/claude-sonnet-4.5, kr/glm-5, kr/MiniMax-M2.5, kr/qwen3-coder-next, kr/deepseek-3.2 |
| `oc/` | OpenCode Free ($0, no auth) | none | oc/nemotron-3-ultra-free, oc/hy3-free, oc/minimax-m3-free |
| `glm/` | Zhipu | API key | glm/glm-5.1, glm/glm-5, glm/4.7 |
| `gh/` | GitHub Copilot | GitHub OAuth | gh/gpt-5.4, gh/claude-sonnet-4.6 |
| `cc/` | Claude Code | Anthropic OAuth | cc/claude-opus-4-7 |
| `cx/` | Codex | OpenAI OAuth | cx/gpt-5.5 |
| `vertex/` | Vertex AI | SA JSON | vertex/gemini-3.1-pro-preview |
| Combo | dashboard-built | — | `free-combo` (recommended) |

Dead prefixes (2026, don't use): `if/` (iFlow), `qw/` (Qwen Code), `gc/` (Gemini CLI).

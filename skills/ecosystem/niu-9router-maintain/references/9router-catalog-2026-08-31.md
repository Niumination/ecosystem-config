# 9router Catalog — 2026-08-31 Snapshot
**Generated:** 2026-08-31 (from `/v1/models` probe)
**Catalog Size:** 99 models (expanded from ~33 in Aug 13)

---

## 📊 Category Breakdown

| Category | Count | Description |
|----------|-------|-------------|
| **ag (Antigravity)** | 16 | Google Gemini via Antigravity (free OAuth) |
| **gemini (Google)** | 7 | Native Google Gemini API models |
| **gh (GitHub Models)** | 32 | GitHub Copilot / GH Models |
| **kr (Kimi)** | 44 | Kimi (Kiro) models — mostly paid |

---

## ✅ Confirmed FREE Models (auto — no billing/key required)

| Model | Context Window | Max Output | Features |
|-------|---------------|------------|----------|---------|
| `gh/gpt-5.4-mini-free-auto` | 400K tokens | 128K | vision, search, tools, reasoning, thinking |
| `gh/gpt-5.6-luna-free-auto` | 400K tokens | 128K | vision, search, tools, reasoning, thinking |

> ⚠️ These are the ONLY models explicitly marked as free/auto in the catalog. All other models may have usage limits even if nominally "free tier."

---

## 🔵 ag (Antigravity) — 16 models
All free via OAuth (Google AI Studio). Context windows typically 1M tokens.

| Model | Notes |
|-------|-------|
| `ag/gemini-3.5-flash-extra-low` | ⚡ 972ms — FASTEST, recommended daily |
| `ag/gemini-3.5-flash-low` | 1094ms |
| `ag/gemini-3.5-flash-high` | Higher quality |
| `ag/gemini-3.5-flash` | Standard flash |
| `ag/gemini-3.6-flash-high` | |
| `ag/gemini-3.6-flash-low` | |
| `ag/gemini-3.6-flash-medium` | |
| `ag/gemini-3.7-flash-high` | |
| `ag/gemini-3.7-flash-low` | |
| `ag/gemini-3.7-flash-medium` | |
| `ag/gemini-3-flash` | Base flash |
| `ag/gemini-3-flash-agent` | Agent-optimized |
| `ag/gemini-3.1-pro-low` | Pro quality, low cost |
| `ag/gemini-pro-agent` | Pro agent |
| `ag/claude-opus-4.6-thinking` | Claude via Antigravity |
| `ag/claude-sonnet-4-6` | Claude via Antigravity |
| `ag/gpt-oss-120b-medium` | Open source, 128K ctx |

---

## 🟢 Gemini (Google) — 7 models
Native Google API. Context ~1M tokens typically.

| Model | Notes |
|-------|-------|
| `gemini/gemini-3.7-flash` | Latest flash |
| `gemini/gemini-3.6-flash` | Current flash |
| `gemini/gemini-3.5-flash-lite` | Lite version |
| `gemini/gemma-4-31b-it` | Interactive (newest Gemma) |
| `gemini/gemini-3-flash-preview` | Preview |
| `gemini/gemini-3.1-flash-lite-preview` | Preview |
| `gemini/gemini-3.1-pro-preview` | Preview |

---

## 🟠 GH (GitHub Models) — 32 models
Via GitHub Copilot / GH Models. Mix of free and paid.

### Confirmed FREE / LOW-COST
| Model | Context | Notes |
|-------|---------|-------|
| `gh/gpt-4o-mini` | 128K | Low cost |
| `gh/gpt-4o-mini-2024-07-18` | 128K | Legacy mini |
| `gh/gpt-5-mini` | 400K | Latest mini |
| `gh/gpt-5.4-mini-free-auto` | 400K | ✅ FREE |
| `gh/gpt-5.6-luna-free-auto` | 400K | ✅ FREE |

### Paid / Other
| Model | Notes |
|-------|-------|
| `gh/gpt-4`, `gh/gpt-4o`, `gh/gpt-4o-*` | Paid GPT-4 variants |
| `gh/gpt-4.1`, `gh/gpt-4.1-2025-04-14` | Paid |
| `gh/gpt-5-*` (non-free) | Paid |
| `gh/claude-haiku-4.5` | Claude via GH |
| `gh/mai-code-*` | Mai code models |
| `gh/copilot-search-*` | Copilot search |
| `gh/exec-agent-*` | Execution agents |
| `gh/gpt-3.5-turbo*` | Legacy |
| `gh/oswe-vscode-prime` | VS Code agent |
| `gh/trajectory-compaction` | Trajectory mgmt |

---

## 🔴 KR (Kimi) — 44 models
Mostly paid (Kiro subscription). Some free tiers available.

### FREE / FREE-TIER
| Model | Context | Notes |
|-------|---------|-------|
| `kr/MiniMax-M2.5` | 200K | MiniMax model, free tier |
| `kr/glm-5` | — | GLM-5 (may have free tier) |
| `kr/qwen3-coder-next` | — | Code-focused, free tier |
| `kr/claude-haiku-4.5` | — | Claude via Kimi |
| `kr/deepseek-3.2` | — | DeepSeek |

### PAID (Kiro subscription)
All `kr/claude-opus-*`, `kr/claude-sonnet-*`, `kr/gpt-5.6-*`, `kr/gpt-5.6-*` variants — subscription required.

---

## 🎯 Active Mapping (User's Config)

| Thread | Model | Category | Latency |
|--------|-------|----------|---------|
| **1** (Main) | `ag/gemini-3.5-flash-low` | ag | 1094ms |
| **802** (Research) | `ag/gemini-3-flash-agent` | ag | 1294ms |
| **803** (Programmer) | `gh/gpt-4o-mini` | gh | 930ms |
| **804** (QA) | `ag/gemini-3.7-flash-low` | ag | 2483ms |
| **1172** (Creator) | `gemini/gemma-4-31b-it` | gemini | 1039ms |

---

## 🔧 Recommended Free/Long-Limit Additions

These models from the 99-catalog are free/low-cost and suitable for fallback chain:

| Model | Context | Cost | Why |
|-------|---------|------|-----|
| `gh/gpt-5.4-mini-free-auto` | 400K | ✅ FREE | Highest context, free |
| `gh/gpt-5.6-luna-free-auto` | 400K | ✅ FREE | Latest, free |
| `gh/gpt-5-mini` | 400K | Low | Latest mini |
| `kr/MiniMax-M2.5` | 200K | Free tier | Code-capable |
| `kr/qwen3-coder-next` | — | Free tier | Code-focused |
| `ag/gpt-oss-120b-medium` | 128K | Free | Open source |

---

## ⚠️ Key Changes from Aug 13 → Aug 31

| Item | Aug 13 | Aug 31 |
|------|--------|--------|
| Catalog size | 33 models | **99 models** |
| Free models | 0 confirmed | **2 confirmed** (`gpt-5.4-mini-free-auto`, `gpt-5.6-luna-free-auto`) |
| gh models | ~5 | **32** |
| kr models | ~10 | **44** |
| ag models | ~10 | **16** |

---

## 🔍 Provider Quality Notes (from probe)

**ag (Antigravity):** 10/10 burst test passed for all ag models. Fastest provider overall.

**gh (GitHub):** `gpt-4o-mini` — 10/10 burst, 930ms. `gpt-5-mini` — 400K ctx. Free-tier models working.

**kr (Kimi):** `MiniMax-M2.5` — 200K ctx, free tier. `qwen3-coder-next` — code-capable. Most kr models require Kiro subscription.

**gemini (Google):** `gemma-4-31b-it` — 1039ms, creative quality. Native Google API, reliable.

---

**Source:** Probe from `http://localhost:20128/v1/models` + chat completion tests
**Verified:** 2026-08-31

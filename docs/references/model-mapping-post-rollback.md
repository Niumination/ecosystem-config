# Hermes Model Mapping — Post-Constitution Rollback (27 Ags 2026)

## Overview
After the Constitution era removal (24 Agu 2026), Hermes config migrated from `opencode-zen` (requiring `OPENCODE_ZEN_API_KEY`) to `opencode-free` (no API key needed for free tier).

## Provider: `opencode-free`
- **Endpoint**: `https://opencode.ai/zen/v1`
- **Auth**: None (anonymous bearer accepted)
- **Free Models Available**: 
  - `hy3-free` ✅ HTTP 200
  - `nemotron-3-ultra-free` ✅ HTTP 200
  - `laguna-s-2.1-free` ✅ HTTP 200
  - `muse-spark-1.2-contributor-free` ✅ HTTP 200
  - `x-preview-f-free` (Ox Alpha) ❌ HTTP 401 — excluded from fallback

## Current Model Mapping (Config Active)

| Channel / Function | Model | Provider | Notes |
|:---|:---|:---|:---|
| **DM Utama / Default** | `hy3-free` | `opencode-free` | Primary general purpose |
| **Cron** | `nemotron-3-ultra-free` | `opencode-free` | Scheduled tasks |
| **Delegation** | `hy3-free` | `opencode-free` | Sub-agent spawning |
| **Compression** | `hy3-free` | `opencode-free` | Context compression |
| **X-Search** | `hy3-free` | `opencode-free` | Web search tool |
| **Thread 1 (General)** | `hy3-free` | `opencode-free` | Telegram DM |
| **Thread 802 (Research)** | `meituan/longcat-2.0:free` | `nous` | Deep research |
| **Thread 803 (Builder)** | `poolside/laguna-s-2.1:free` | `nous` | Coding/development |
| **Thread 804 (QA)** | `upstage/solar-pro4:free` | `nous` | Audit/review |
| **Thread 1172 (Creator)** | `nemotron-3-ultra-free` | `opencode-free` | Content creation |

## Fallback Chain (3-Level, Single Provider)

```yaml
fallback_providers:
  - provider: opencode-free
    model: hy3-free              # L1: fast, lightweight
  - provider: opencode-free
    model: nemotron-3-ultra-free # L2: reasoning heavy
  - provider: opencode-free
    model: laguna-s-2.1-free     # L3: coding specialist
```

**Principle**: Single provider family (opencode-free), diversify models — NOT silent hop to different providers (core v2 principle: provider swap = HALT + HANDOFF).

## Thread-Specific Overrides (channel_overrides)

All threads using `opencode-free` provider:
- Thread 1: `hy3-free` / `opencode-free`
- Thread 1172: `nemotron-3-ultra-free` / `opencode-free`

Threads using `nous` provider (unchanged):
- Thread 802: `meituan/longcat-2.0:free` / `nous`
- Thread 803: `poolside/laguna-s-2.1:free` / `nous`
- Thread 804: `upstage/solar-pro4:free` / `nous`

## Migration Notes

### What Changed
1. **Provider**: `opencode-zen` → `opencode-free`
2. **API Key**: Removed `OPENCODE_API_KEY` from `env_passthrough` (not needed)
3. **Default Model**: `big-pickle` → `hy3-free` (more stable free tier)
4. **Fallback**: 1-level (`hy3-free` via opencode-zen) → 3-level (all opencode-free)
5. **Removed**: `x-preview-f-free` from fallback (401 on free tier)

### Verification
All primary models tested via direct endpoint:
- `hy3-free`: HTTP 200 ✅
- `nemotron-3-ultra-free`: HTTP 200 ✅
- `laguna-s-2.1-free`: HTTP 200 ✅
- `x-preview-f-free`: HTTP 401 ❌ (excluded)

### Related Files
- `~/.hermes/config.yaml` — Main configuration
- `.hermes/skills/provider-fallback/SKILL.md` — Fallback strategy doc
- `docs/references/ekosistem-status.md` — Ecosystem status with Hermes config


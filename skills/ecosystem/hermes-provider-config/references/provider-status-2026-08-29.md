### Provider Status (29 Ags 2026 — post-sweep)

| Provider | Status | Models | Chat Test | Verdict |
|----------|--------|--------|-----------|---------|
| **9router** (localhost:20128) | ✅ LIVE | 78 | 7/17 OK | **PRIMARY** — all flash variants long limit (10/10 burst) |
| **huancheng** (api.hcnsec.cn) | ⚠️ PARTIAL | 20 | DM auto OK | DM default, case-sensitive model ID |
| **opencode-zen** (opencode.ai/zen) | ⚠️ LIMITED | 64 | 3/7 OK | Hanya hy3-free stabil; big-pickle & laguna 429 |
| **openrouter** | ❌ HEAVY 429 | 388 | 1/12 OK | Free tier rate-limited berat |
| **agentrouter** | ❌ REJECTED | — | 401 | Key ditolak + blokir frasa ID ≥2 kata |
| **juan-router** | ❌ REJECTED | — | 401 | Key ditolak server |

### Recommended Mapping (29 Ags 2026)

**DM Utama:**
```yaml
model:
  provider: huancheng
  default: auto
  base_url: https://api.hcnsec.cn/v1
  api_mode: codex_responses
```

**Thread Overrides:**
| Thread | Model | Provider | Burst | Latency |
|--------|-------|----------|-------|---------|
| 1 | ag/gemini-3.5-flash-low | 9router | 10/10 | 729ms |
| 802 | ag/gemini-3-flash-agent | 9router | 10/10 | 966ms |
| 803 | gh/gpt-4o-mini | 9router | 10/10 | 930ms |
| 804 | ag/gemini-3.7-flash-low | 9router | 10/10 | 2483ms |
| 1172 | gemini/gemma-4-31b-it | 9router | 10/10 | 1039ms |

**Fallback Chain (3 Level):**
```yaml
fallback_providers:
  - provider: 9router
    model: ag/gemini-3.5-flash-low
  - provider: 9router
    model: ag/gemini-3-flash-agent
  - provider: opencode-zen
    model: hy3-free
```

### Excluded Models (dengan alasan)
| Model | Provider | Reason |
|-------|----------|--------|
| big-pickle | opencode-zen | 0/8 burst — kuota free habis |
| laguna-s-2.1-free | opencode-zen | 5/8 burst — sering 429 |
| nemotron-3-ultra-free | opencode-zen | 0/8 burst — mati |
| All :free | openrouter | 429 rate limit berat |
| All models | huancheng | Timeout semua chat (kecuali DM auto) |
| All models | agentrouter | Key 401 + content filter |
| All models | juan-router | Key 401 ditolak |

**Referensi lengkap:** `references/provider-sweep-2026-08-29.md`, `references/model-mapping-report-2026-08-29.md`
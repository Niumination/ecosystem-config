### **Model Mapping — Status Terakhir (27 Ags 2026 — post-constitution rollback)**

**Config.yaml (active) — migrated from opencode-zen to opencode-free:**

| Thread | Agent | Provider | Model | Status |
|--------|-------|----------|-------|--------|
| 1 | chief | 9router | `gemini/gemini-3.5-flash-lite` | ✅ (13 Ags: ROLLBACK dari agentrouter — filter blokir frasa ID) |
| 802 | research | 9router | `gc/gemini-2.5-pro` | ✅ 9router |
| 803 | programmer | 9router | `cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` | ✅ 9router |
| 804 | qa | 9router | `cf/@cf/zai-org/glm-4.7-flash` | ✅ 8/8 stress (13 Ags malam: dari `nvidia/z-ai/glm-5.2` 2/8) |
| 1172 | creator | 9router | `gemini/gemma-4-31b-it` | ✅ 8/8 stress (13 Ags malam: dari `nvidia/minimaxai/minimax-m3` 1/8) |
| **DM (Default)** | - | **opencode-free** | **hy3-free** | ✅ HTTP 200 verified |
| **Cron** | - | **opencode-free** | **nemotron-3-ultra-free** | ✅ HTTP 200 verified |
| **Delegation/Compression/X-Search** | - | **opencode-free** | **hy3-free** | ✅ HTTP 200 verified |
| **Fallback (GLOBAL)** | - | **opencode-free** | **3-level: hy3-free → nemotron-3-ultra-free → laguna-s-2.1-free** | ✅ 27 Ags verified |

**Migration Note (27 Ags 2026):** DM & internal functions migrated from `opencode-zen` (required `OPENCODE_ZEN_API_KEY`) to `opencode-free` (no API key, anonymous bearer). All primary models verified HTTP 200. `x-preview-f-free` (Ox Alpha) excluded (HTTP 401).

---

### **Model Mapping — Updated 29 Ags 2026 (post-sweep & burst test)**

**Config.yaml (active) — NEW mapping after provider sweep:**

| Target | Model | Provider | Burst Test | Latency |
|--------|-------|----------|------------|---------|
| **DM (Default)** | `auto` | **huancheng** | ✅ N/A | auto-resolve |
| Thread 1 | `ag/gemini-3.5-flash-low` | 9router | ✅ 10/10 | 729ms |
| Thread 802 | `ag/gemini-3-flash-agent` | 9router | ✅ 10/10 | 966ms |
| Thread 803 | `gh/gpt-4o-mini` | 9router | ✅ 10/10 | 930ms |
| Thread 804 | `ag/gemini-3.7-flash-low` | 9router | ✅ 10/10 | 2483ms |
| Thread 1172 | `gemini/gemma-4-31b-it` | 9router | ✅ 10/10 | 1039ms |
| **Fallback L1** | `ag/gemini-3.5-flash-low` | 9router | ✅ 10/10 | 729ms |
| **Fallback L2** | `ag/gemini-3-flash-agent` | 9router | ✅ 10/10 | 966ms |
| **Fallback L3** | `hy3-free` | opencode-zen | ✅ 10/10 | 2510ms |

**Changes from 27 Ags:**
1. DM: `opencode-free/hy3-free` → `huancheng/auto` (user preference, aktif dipakai)
2. Thread 1: `gemini-3.5-flash-lite` → `ag/gemini-3.5-flash-low` (lebih cepat 729ms vs ~1s)
3. Thread 802: `gc/gemini-2.5-pro` → `ag/gemini-3-flash-agent` (agent-optimized)
4. Thread 803: `cf/deepseek-r1-distill-qwen-32b` → `gh/gpt-4o-mini` (proven coding, 9/10 burst history)
5. Thread 804: `cf/glm-4.7-flash` → `ag/gemini-3.7-flash-low` (flash v3.7 stronger reasoning)
6. Fallback: single `opencode-zen` → 9router×2 + opencode-zen×1 (diversified)

**Provider Status (29 Ags):**
- ✅ 9router: PRIMARY (78 models, all flash variants long limit)
- ⚠️ huancheng: DM only (auto works, but case-sensitive model IDs)
- ⚠️ opencode-zen: LIMITED (only hy3-free stable; big-pickle & laguna 429)
- ❌ openrouter: HEAVY 429 (free tier rate-limited)
- ❌ agentrouter: REJECTED (key 401 + blocks Indonesian phrases)
- ❌ juan-router: REJECTED (key 401)

**Test Methodology:**
- Single probe: HTTP 200 + response validation (timeout 8s)
- Burst test: 10 requests beruntun (0.05s delay), success rate calculated
- Long limit threshold: ≥9/10 burst = ACCEPTED
- All recommended models passed 10/10 burst test on 29 Ags 2026

**References:**
- `references/provider-sweep-2026-08-29.md` — Full sweep report
- `references/model-mapping-report-2026-08-29.md` — Final mapping table
- `~/.hermes/provider-sweep-results.json` — Raw sweep data
- `~/.hermes/live-test-results.json` — Live burst test results
- `~/.hermes/MAPPING-UPDATE-SUMMARY.md` — Change log
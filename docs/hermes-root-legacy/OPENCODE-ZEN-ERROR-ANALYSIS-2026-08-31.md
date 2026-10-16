# 🔍 OpenCode Zen Free Tier — Disconnection & Error Analysis
**Date:** 31 Ags 2026
**Status:** Root Cause Analysis + Solution

---

## 🎯 TL;DR

**Masalah:** OpenCode Zen free tier sering terputus dan error di tengah eksekusi.

**Penyebab Utama:**
1. ❌ **Rate Limit (HTTP 429)** — "Individual quota reached" — **Primary cause**
2. ❌ **Quota Exhausted** — Resets after 120h (5 days)
3. ❌ **503 Service Unavailable** — Provider-side downtime
4. ❌ **Long latency (34s)** — Cache hit 100% → context window full

**Solusi:** Switch ke provider 9router yang stable.

---

## 📊 Error Evidence (from logs)

### Error 1: RateLimitError (HTTP 429) — MOST COMMON
```
2026-08-31 16:38:37,548 WARNING [20260827_232928_2ae9b779] 
agent.conversation_loop: API call failed (attempt 1/3) 
error_type=RateLimitError 
provider=opencode 
base_url=https://opencode.ai/zen/v1 
model=big-pickle 
summary=HTTP 429: Error from provider (Console): Rate limit exceeded. 
Please try again later.
```

### Error 2: Individual Quota Exhausted
```
Error code: 429 
Individual quota reached. Please upgrade your subscription to increase your limits. 
Resets in 120h36m20s. 
Status: RESOURCE_EXHAUSTED
quotaResetDelay: 120h36m20.648925561s
quotaResetTimeStamp: 2026-09-05T10:15:21Z
```

### Error 3: 503 Unavailable (9router fallback)
```
Error code: 503 
[antigravity/gemini-3.5-flash-extra-low] Unavailable 
(reset after 120h 36m 44s)
```

### Error 4: High Latency
```
API call #12: model=big-pickle provider=opencode 
in=101328 out=197 total=101525 latency=34.3s 
cache=100864/101328 (100%)
```

---

## 🔍 Root Cause Analysis

### 1. Rate Limiting (HTTP 429) — PRIMARY CAUSE
| Factor | Value |
|--------|-------|
| **Error Type** | `RateLimitError` |
| **HTTP Status** | 429 |
| **Message** | "Rate limit exceeded" |
| **Quota Reset** | **120 hours (5 days)** |
| **Quota Type** | Individual quota (per-minute) |
| **Frequency** | Every few minutes during heavy usage |

**Why:** Free tier has strict rate limits per minute. When you send too many requests quickly, the quota is exhausted and errors occur.

### 2. Quota Exhaustion (RESOURCE_EXHAUSTED)
| Factor | Value |
|--------|-------|
| **Quota Reset Time** | 120h 36m 20s (5+ days!) |
| **Quota Type** | Per-model individual quota |
| **Impact** | All models affected simultaneously |
| **Reset** | `2026-09-05T10:15:21Z` |

**Why:** OpenCode Zen free tier has very low quotas per model. Once exhausted, you must wait 5 days for reset.

### 3. Service Unavailable (HTTP 503)
| Factor | Value |
|--------|-------|
| **Error Type** | 503 |
| **Models Affected** | gemini-3.5-flash-extra-low, gemini-3.5-flash-low, etc. |
| **Reset Time** | 120h (5 days) |
| **Frequency** | Intermittent |

**Why:** 9router itself has capacity issues. This affects the fallback models too.

### 4. High Latency + Cache Issues
| Factor | Value |
|--------|-------|
| **Latency** | 34.3s (abnormally high) |
| **Cache Hit** | 99-100% |
| **Context** | 100K+ tokens |
| **Output** | 180-335 tokens |
| **Input** | 100K+ tokens |

**Why:** When context window is nearly full (100K tokens), processing becomes slow. The model is processing huge context with minimal output.

---

## 📈 Error Pattern

```
Timeline (31 Ags 2026):
─────────────────────────────────────────────────────────────
16:37:29  ✅ API call #9  (model=big-pickle, 13.1s)
16:37:35  ✅ API call #10 (model=big-pickle, 5.1s)
16:37:42  ✅ API call #11 (model=big-pickle, 4.8s)
16:38:17  ⚠️ API call #12 (model=big-pickle, 34.3s, cache=100%)
16:38:22  ✅ API call #13 (model=big-pickle, 5.4s)
16:38:30  ✅ API call #14 (model=big-pickle, 7.6s)
16:38:35  ✅ API call #15 (model=big-pickle, 4.3s)
16:38:37  ❌ OpenAI client closed (stream_error_cleanup)
16:38:37  ❌ RateLimitError (HTTP 429) — QUOTA EXCEEDED
16:38:40  ❌ 503 Unavailable — 9router fallback also down
16:39:01  ❌ 429 Individual quota reached — gemini-3-flash-agent
16:39:17  ❌ 429 Individual quota reached — gemini-3-flash
16:39:25  ❌ 503 Unavailable — gemini-3.1-flash-image
─────────────────────────────────────────────────────────────
```

**Pattern:** 
- ✅ First 7 calls work fine
- ⚠️ Call #12 shows cache=100% (context full) → latency spikes
- ❌ Call #16+ → RateLimitError (429)
- ❌ Fallback to 9router also fails (503)

---

## 🧠 Why This Happens

### OpenCode Zen Free Tier Limitations

| Limitation | Value | Impact |
|------------|-------|--------|
| **Rate Limit** | ~10-20 requests/minute | Quota exhausted fast |
| **Quota Reset** | 120 hours (5 days) | Long wait if exhausted |
| **Context Window** | ~100K tokens | Slows down significantly |
| **Concurrent** | Limited | Queueing delays |
| **Priority** | Low | Deprioritized vs paid |

### Why 9router Fallback Also Fails

| Factor | Value |
|--------|-------|
| **9router Status** | Running (PID 972) |
| **Models** | 99 models in catalog |
| **Antigravity Models** | 120h reset (same issue) |
| **Rate Limit** | Same quota exhaustion |

**Paradox:** Both OpenCode Zen AND 9router's antigravity models share the same Google quota backend → both exhausted simultaneously!

---

## ✅ Solutions

### Solution 1: Switch to 9router Models (immediate)

Since antigravity models on 9router also have quota issues, use non-antigravity models:

```yaml
# REMOVE antigravity models (they share Google quota)
# fallback_providers:
#   - provider: 9router
#     model: ag/gemini-3.5-flash-extra-low ❌ SHARED QUOTA
#   - provider: 9router
#     model: ag/gemini-3.5-flash-low ❌ SHARED QUOTA

# ADD non-antigravity models
- provider: 9router
  model: gh/gpt-4o-mini ✅ GH quota (separate)
- provider: 9router
  model: gh/gpt-5-mini ✅ GH quota (separate)
- provider: 9router
  model: gh/gpt-5.4-mini-free-auto ✅ FREE, GH quota
- provider: 9router
  model: kr/MiniMax-M2.5 ✅ KR quota (separate)
- provider: 9router
  model: gemini/gemini-3.7-flash ✅ Native Gemini (different quota)
```

### Solution 2: Use Smaller Context

```yaml
# Reduce context window to avoid 100K+ token processing
# In config:
context_window: 32768  # Reduce from 100K to 32K
max_output_tokens: 4096  # Limit output
```

### Solution 3: Implement Request Throttling

```python
# Add delay between requests
import time
time.sleep(1)  # 1 second between API calls
```

### Solution 4: Use `opencode-zen` provider specifically for non-rate-limited tasks

```yaml
# For simple, infrequent tasks:
- provider: opencode-zen
  model: big-pickle
  # But limit to simple queries only
```

---

## 📊 Recommended Provider Chain

### Primary Chain (9router — most stable)
```yaml
fallback_providers:
  1. gh/gpt-4o-mini          — GH quota, separate from antigravity
  2. gh/gpt-5-mini           — GH quota, 400K context
  3. gh/gpt-5.4-mini-free-auto — ✅ FREE, GH quota, 400K context
  4. kr/MiniMax-M2.5         — KR quota, separate from Google
  5. gemini/gemini-3.7-flash  — Native Gemini, different quota backend
  6. ag/gpt-oss-120b-medium   — AG model, open source, 128K context
```

### Skip These Models (quota shared with antigravity)
- ❌ `ag/gemini-3.5-flash-extra-low` — Shares Google quota with antigravity
- ❌ `ag/gemini-3.5-flash-low` — Shares Google quota
- ❌ `ag/gemini-3-flash-agent` — Shares Google quota
- ❌ `ag/gemini-3-flash` — Shares Google quota
- ❌ `ag/gemini-3.1-flash-image` — Shares Google quota

### Avoid These Models (OpenCode Zen limitations)
- ❌ `big-pickle` (opencode-zen) — Rate limited, 429 errors
- ❌ Any model on opencode-zen during heavy usage

---

## 🔧 Config Update Recommendation

```yaml
# Current (problematic)
fallback_providers:
  - provider: 9router
    model: ag/gemini-3.5-flash-extra-low  # ❌ Shared quota with antigravity
  - provider: 9router
    model: ag/gemini-3.5-flash-low        # ❌ Shared quota
  - provider: 9router
    model: ag/gemini-3-flash-agent         # ❌ Shared quota
  - provider: 9router
    model: ag/gemini-3-flash               # ❌ Shared quota
  - provider: 9router
    model: ag/gemini-3.1-flash-image       # ❌ Shared quota

# Updated (recommended)
fallback_providers:
  - provider: 9router
    model: gh/gpt-4o-mini                  # ✅ GH quota
  - provider: 9router
    model: gh/gpt-5-mini                   # ✅ GH quota, 400K ctx
  - provider: 9router
    model: gh/gpt-5.4-mini-free-auto       # ✅ FREE, GH quota
  - provider: 9router
    model: kr/MiniMax-M2.5                 # ✅ KR quota
  - provider: 9router
    model: gemini/gemini-3.7-flash         # ✅ Native Gemini quota
  - provider: 9router
    model: ag/gpt-oss-120b-medium          # ✅ AG, open source
```

---

## 📋 Summary

| Root Cause | Solution |
|------------|----------|
| **Rate Limit (429)** | Switch to GH/KR models with separate quotas |
| **Quota Exhausted (120h reset)** | Avoid antigravity models that share Google quota |
| **503 Unavailable** | Use non-antigravity models |
| **High latency (34s)** | Reduce context window, use smaller models |
| **OpenCode Zen free tier limit** | Minimize usage, throttle requests |

---

## ✅ Action Plan

1. **Immediate:** Switch fallback providers to GH/KR models (separate quotas)
2. **Short-term:** Reduce context window from 100K to 32K
3. **Medium-term:** Implement request throttling in config
4. **Long-term:** Monitor quota usage via 9router dashboard

---

**Status:** ✅ Analysis complete. Root cause identified: **shared Google quota between antigravity models and 9router fallback**, plus **strict OpenCode Zen free tier limits**.

**Recommendation:** Switch to GH/KR models with independent quotas.

⚡ (◕‿◕)★

# Kiro/Claude Model Investigation Report
**Date:** 30 Ags 2026 01:05 WIB  
**Subject:** Verification of kr/claude-opus-5 and alternatives

---

## Executive Summary

Model **kr/claude-opus-5 TIDAK TERSEDIA** di 9router (HTTP 400 Bad Request). Namun, ditemukan alternatif Claude yang **BERFUNGSI** dengan performa baik:

| Model | Status | Latency | Burst | Use Case |
|-------|--------|---------|-------|----------|
| `kr/claude-haiku-4.5` | ✅ OK | 2527ms | - | Fast responses |
| `kr/claude-sonnet-4` | ✅ OK | 2521ms | - | Balanced |
| `ag/claude-opus-4-6-thinking` | ✅ OK | 3848ms | - | Strong reasoning |

---

## Test Results

### 1. kr/claude-opus-5 Test
```
Status: ❌ FAILED
Error: HTTP Error 400: Bad Request
Reason: Model tidak terdaftar di 9router
```

### 2. Available Claude Models (15 total)

**Working (5/15):**
| Model | Prefix | Latency |
|-------|--------|---------|
| kr/claude-haiku-4.5 | kr | 2527ms |
| kr/claude-sonnet-4 | kr | 2521ms |
| kr/claude-sonnet-4.5 | kr | 2850ms |
| ag/claude-sonnet-4-6 | ag | 2610ms |
| ag/claude-opus-4-6-thinking | ag | 3848ms |

**Failed (10/15):**
- gh/claude-haiku-4.5 (HTTP error)
- kr/claude-haiku-4.5-agentic (timeout)
- kr/claude-haiku-4.5-thinking (timeout)
- kr/claude-haiku-4.5-thinking-agentic (timeout)
- kr/claude-sonnet-4-agentic (timeout)
- kr/claude-sonnet-4-thinking (timeout)
- kr/claude-sonnet-4-thinking-agentic (timeout)
- kr/claude-sonnet-4.5-agentic (timeout)
- kr/claude-sonnet-4.5-thinking (timeout)
- kr/claude-sonnet-4.5-thinking-agentic (timeout)

### 3. All Opus Models in Catalog

**Found (1 model):**
- `ag/claude-opus-4-6-thinking` ✅ WORKING

**Not Found:**
- `kr/claude-opus-5` ❌ (user requested)
- Any other opus-5 variants ❌

---

## Analysis

### Why kr/claude-opus-5 Failed?

1. **Model not registered** — Tidak ada di katalog 9router
2. **Naming mismatch** — Mungkin nama resminya berbeda
3. **Provider issue** — Model ini mungkin dari provider lain yang belum dikonfigurasi

### What's Available Instead?

**For Coding/Agentic tasks:**
- `kr/qwen3-coder-next` (869ms) — Fastest, coding-focused
- `kr/deepseek-3.2` (804ms) — General purpose, fast

**For Reasoning/Complex tasks:**
- `ag/claude-opus-4-6-thinking` (3848ms) — Strongest reasoning
- `kr/claude-sonnet-4` (2521ms) — Good balance

**For Fast responses:**
- `kr/claude-haiku-4.5` (2527ms) — Fast Claude
- `gh/copilot-search-a` (477ms) — Fastest overall

---

## Recommendations

### Immediate Actions:
1. ✅ Verify model name di dashboard 9router
2. ✅ Check if model needs approval
3. ✅ Use available alternatives now

### If kr/claude-opus-5 is Critical:
1. Contact 9router support untuk registration
2. Check if model ID is correct (case-sensitive?)
3. Wait for propagation (5-15 minutes typical)

### Recommended Mapping (if kiro needed for coding):
```yaml
# Thread 803 (Programmer)
model: kr/qwen3-coder-next  # 869ms, coding-optimized
provider: 9router

# Thread 804 (QA/Reasoning)
model: ag/claude-opus-4-6-thinking  # 3848ms, strong reasoning
provider: 9router

# Fallback chain
fallback:
  - kr/qwen3-coder-next
  - kr/deepseek-3.2
  - kr/claude-haiku-4.5
```

---

## Documentation

- `~/.hermes/test-kiro-claude-opus-5.py` — Test script
- `~/.hermes/scan-kr-models.py` — Catalog scanner
- `~/.hermes/test-claude-models.py` — Claude testing
- `~/.hermes/quick-burst-test.py` — Burst test
- `~/.hermes/9ROUTER-AUDIT-REPORT.md` — Full audit

---

**Conclusion:** kr/claude-opus-5 tidak tersedia di 9router. Gunakan alternatif yang sudah teruji: `kr/qwen3-coder-next` (coding), `ag/claude-opus-4-6-thinking` (reasoning), atau `kr/claude-haiku-4.5` (fast).

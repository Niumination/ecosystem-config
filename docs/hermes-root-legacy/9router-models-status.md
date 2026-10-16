# 9Router Models Status Report
**Generated:** 30 Ags 2026  
**Source:** model-checker.py + manual verification

---

## Summary

| Category | Count |
|----------|-------|
| **Total Catalog** | 89 models |
| **Working** | 14 models |
| **Failed** | 50 models |

---

## ✅ Working Models (14)

| Model | Latency | Notes |
|-------|---------|-------|
| ag/gemini-3.5-flash-low | 1094ms | Fast, free |
| ag/gemini-3-flash-agent | 1294ms | Agent-optimized, free |
| ag/gemini-3-flash | 1534ms | Free |
| ag/gemini-3.1-flash-image | 1534ms | Vision + free |
| gemini/gemini-3.1-flash-lite-preview | 1556ms | Free tier |
| gemini/gemini-3.5-flash-lite | 1673ms | Free tier |
| kr/minimax-m2.5 | 1845ms | Kiro subscription |
| kr/claude-haiku-4.5 | 2021ms | Kiro subscription |
| ag/claude-opus-4-6-thinking | 2209ms | Claude Opus, free |
| ag/claude-sonnet-4-6 | 2350ms | Claude Sonnet, free |
| kr/claude-sonnet-4.5 | 2598ms | Kiro subscription |
| ag/gemini-3.1-pro-low | 3365ms | Pro quality, free |
| ag/gemini-pro-agent | 4854ms | Agent-optimized pro |
| ag/gemini-3.5-flash-extra-low | 972ms | Fastest, free |

---

## ❌ Failed Models (50)

These models returned HTTP 400, 404, 429, or timed out during testing.

| Model | Error Pattern |
|-------|---------------|
| ag/gemini-3.5-flash-high | HTTP 400/404/timeout |
| ag/gpt-oss-120b-medium | HTTP 400/404/timeout |
| gemini/gemini-3.1-pro-preview | HTTP 400/404/timeout |
| gemini/gemini-3.7-flash | HTTP 400/404/timeout |
| gh/claude-haiku-4.5 | HTTP 400/404/timeout |
| gh/exec-agent-b | HTTP 400/404/timeout |
| gh/gpt-3.5-turbo | HTTP 400/404/timeout |
| gh/gpt-4 | HTTP 400/404/timeout |
| gh/gpt-4-0125-preview | HTTP 400/404/timeout |
| gh/gpt-4-0613 | HTTP 400/404/timeout |
| gh/gpt-5-mini | HTTP 400/404/timeout |
| gh/gpt-5.4-mini-free-auto | HTTP 400/404/timeout |
| gh/gpt-5.6-luna | HTTP 400/404/timeout |
| gh/gpt-5.6-luna-free-auto | HTTP 400/404/timeout |
| gh/mai-code-1-flash | HTTP 400/404/timeout |
| gh/mai-code-1-flash-4th | HTTP 400/404/timeout |
| gh/mai-code-1-flash-picker | HTTP 400/404/timeout |
| gh/mai-code-1-flash-secondary | HTTP 400/404/timeout |
| gh/mai-code-1.1-flash | HTTP 400/404/timeout |
| gh/oswe-vscode-prime | HTTP 400/404/timeout |
| gh/trajectory-compaction | HTTP 400/404/timeout |
| kr/auto-thinking | HTTP 400/404/timeout |
| kr/claude-haiku-4.5-agentic | HTTP 400/404/timeout |
| kr/claude-haiku-4.5-thinking | HTTP 400/404/timeout |
| kr/claude-haiku-4.5-thinking-agentic | HTTP 400/404/timeout |
| kr/claude-sonnet-4 | HTTP 400/404/timeout |
| kr/claude-sonnet-4-agentic | HTTP 400/404/timeout |
| kr/claude-sonnet-4-thinking | HTTP 400/404/timeout |
| kr/claude-sonnet-4-thinking-agentic | HTTP 400/404/timeout |
| kr/claude-sonnet-4.5-agentic | HTTP 400/404/timeout |
| kr/claude-sonnet-4.5-thinking | HTTP 400/404/timeout |
| kr/claude-sonnet-4.5-thinking-agentic | HTTP 400/404/timeout |
| kr/deepseek-3.2 | HTTP 400/404/timeout |
| kr/deepseek-3.2-agentic | HTTP 400/404/timeout |
| kr/deepseek-3.2-thinking | HTTP 400/404/timeout |
| kr/deepseek-3.2-thinking-agentic | HTTP 400/404/timeout |
| kr/glm-5 | HTTP 400/404/timeout |
| kr/glm-5-agentic | HTTP 400/404/timeout |
| kr/glm-5-thinking | HTTP 400/404/timeout |
| kr/glm-5-thinking-agentic | HTTP 400/404/timeout |
| kr/minimax-m2.1-agentic | HTTP 400/404/timeout |
| kr/minimax-m2.1-thinking | HTTP 400/404/timeout |
| kr/minimax-m2.1-thinking-agentic | HTTP 400/404/timeout |
| kr/minimax-m2.5-agentic | HTTP 400/404/timeout |
| kr/minimax-m2.5-thinking | HTTP 400/404/timeout |
| kr/minimax-m2.5-thinking-agentic | HTTP 400/404/timeout |
| kr/qwen3-coder-next | HTTP 400/404/timeout |
| kr/qwen3-coder-next-agentic | HTTP 400/404/timeout |
| kr/qwen3-coder-next-thinking | HTTP 400/404/timeout |
| kr/qwen3-coder-next-thinking-agentic | HTTP 400/404/timeout |

---

## Recommendation

**For Hermes config, use only working models:**
- Primary: `ag/gemini-3.5-flash-extra-low` (fastest, free)
- Fallbacks: See updated config.yaml

**To re-enable failed models**, check if:
1. Upstream provider has fixed the issue
2. API keys need refresh
3. Model has been deprecated

Run `/model-check` to verify current status.

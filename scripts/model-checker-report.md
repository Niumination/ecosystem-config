# Model Checker Report — 30 Aug 2026 13:14 WIB

Server: 9router (127.0.0.1:20128)
Total model di catalog: 89
Model accessible: 42
Model inaccessible: 47

## Per Provider Summary

### AG (16 models)
- **OK:** 15 | **FAIL:** 1
- Latency: min=595ms, avg=2164ms, max=4267ms

### GEMINI (7 models)
- **OK:** 5 | **FAIL:** 2
- Latency: min=672ms, avg=960ms, max=1229ms

### GH (32 models)
- **OK:** 15 | **FAIL:** 17
- Latency: min=459ms, avg=1061ms, max=3431ms

### KR (34 models)
- **OK:** 7 | **FAIL:** 27
- Latency: min=889ms, avg=1753ms, max=3004ms

## 🆓 Model GRATIS / Free Tier (bisa dipakai tanpa biaya)

| Model | Provider | Latency | Keterangan |
|-------|----------|---------|------------|
| ag/gemini-3-flash-agent | ag | 595ms | Antigravity gratis via OAuth |
| ag/gemini-3.5-flash-low | ag | 630ms | Antigravity gratis via OAuth |
| gemini/gemini-3.1-flash-lite-preview | gemini | 672ms | AI Studio free, kuota harian 무제한 |
| ag/gemini-3.6-flash-low | ag | 721ms | Antigravity gratis via OAuth |
| ag/gemini-3.5-flash-extra-low | ag | 820ms | Antigravity gratis via OAuth |
| gemini/gemini-3.5-flash-lite | gemini | 829ms | AI Studio free, kuota harian 무제한 |
| kr/deepseek-3.2 | kr | 889ms | Kiro — model tertentu gratis terbatas |
| kr/qwen3-coder-next | kr | 889ms | Kiro — model tertentu gratis terbatas |
| gemini/gemma-4-31b-it | gemini | 929ms | AI Studio free, ada batas kuota |
| ag/gemini-3-flash | ag | 961ms | Antigravity gratis via OAuth |
| gemini/gemini-3-flash-preview | gemini | 1139ms | AI Studio free, ada batas kuota |
| gemini/gemini-3.6-flash | gemini | 1229ms | AI Studio free, ada batas kuota |
| ag/gemini-pro-agent | ag | 1768ms | Antigravity gratis via OAuth |
| ag/gemini-3.1-pro-low | ag | 1948ms | Antigravity gratis via OAuth |
| ag/claude-sonnet-4-6 | ag | 2338ms | Antigravity gratis via OAuth |
| ag/gemini-3.6-flash-medium | ag | 2468ms | Antigravity gratis via OAuth |
| ag/gemini-3.7-flash-medium | ag | 2494ms | Antigravity gratis via OAuth |
| ag/gemini-3.6-flash-high | ag | 3108ms | Antigravity gratis via OAuth |
| ag/claude-opus-4-6-thinking | ag | 3196ms | Antigravity gratis via OAuth |
| ag/gemini-3.7-flash-low | ag | 3290ms | Antigravity gratis via OAuth |
| ag/gemini-3.7-flash-high | ag | 3858ms | Antigravity gratis via OAuth |
| ag/gpt-oss-120b-medium | ag | 4267ms | Antigravity gratis via OAuth |

**Total:** 22 model gratis

## 💰 Model Berbayar / Kuota Besar

| Model | Provider | Latency | Keterangan |
|-------|----------|---------|------------|
| kr/claude-haiku-4.5 | kr | 1119ms | Kiro subscription |
| kr/claude-sonnet-4 | kr | 1941ms | Kiro subscription |
| kr/claude-sonnet-4.5 | kr | 2050ms | Kiro subscription |
| kr/minimax-m2.5 | kr | 2380ms | Kiro subscription |
| kr/auto | kr | 3004ms | Kiro subscription |

**Total:** 5 model berbayar

## ❌ Model Tidak Accessible

| Model | Provider | Error |
|-------|----------|-------|
| ag/gemini-3.5-flash-high | ag | HTTP 404 |
| gemini/gemini-3.1-pro-preview | gemini | HTTP 429 |
| gemini/gemini-3.7-flash | gemini | HTTP 429 |
| gh/claude-haiku-4.5 | gh | HTTP 400 |
| gh/exec-agent-b | gh | HTTP 503 |
| gh/gpt-3.5-turbo | gh | HTTP 400 |
| gh/gpt-4 | gh | HTTP 400 |
| gh/gpt-4-0125-preview | gh | HTTP 400 |
| gh/gpt-4-0613 | gh | HTTP 400 |
| gh/gpt-5-mini | gh | HTTP 400 |
| gh/gpt-5.4-mini-free-auto | gh | HTTP 400 |
| gh/gpt-5.6-luna | gh | HTTP 400 |
| gh/gpt-5.6-luna-free-auto | gh | HTTP 400 |
| gh/mai-code-1-flash | gh | HTTP 400 |
| gh/mai-code-1-flash-4th | gh | HTTP 400 |
| gh/mai-code-1-flash-picker | gh | HTTP 400 |
| gh/mai-code-1-flash-secondary | gh | HTTP 400 |
| gh/mai-code-1.1-flash | gh | HTTP 400 |
| gh/oswe-vscode-prime | gh | HTTP 400 |
| gh/trajectory-compaction | gh | HTTP 503 |
| kr/auto-thinking | kr | HTTP 400 |
| kr/claude-haiku-4.5-agentic | kr | HTTP 400 |
| kr/claude-haiku-4.5-thinking | kr | HTTP 400 |
| kr/claude-haiku-4.5-thinking-agentic | kr | HTTP 400 |
| kr/claude-sonnet-4-agentic | kr | HTTP 400 |
| kr/claude-sonnet-4-thinking | kr | HTTP 400 |
| kr/claude-sonnet-4-thinking-agentic | kr | HTTP 400 |
| kr/claude-sonnet-4.5-agentic | kr | HTTP 400 |
| kr/claude-sonnet-4.5-thinking | kr | HTTP 400 |
| kr/claude-sonnet-4.5-thinking-agentic | kr | HTTP 400 |
| kr/deepseek-3.2-agentic | kr | HTTP 400 |
| kr/deepseek-3.2-thinking | kr | HTTP 400 |
| kr/deepseek-3.2-thinking-agentic | kr | HTTP 400 |
| kr/glm-5 | kr | timed out |
| kr/glm-5-agentic | kr | HTTP 400 |
| kr/glm-5-thinking | kr | timed out |
| kr/glm-5-thinking-agentic | kr | HTTP 400 |
| kr/minimax-m2.1 | kr | timed out |
| kr/minimax-m2.1-agentic | kr | timed out |
| kr/minimax-m2.1-thinking | kr | timed out |
| kr/minimax-m2.1-thinking-agentic | kr | timed out |
| kr/minimax-m2.5-agentic | kr | HTTP 400 |
| kr/minimax-m2.5-thinking | kr | HTTP 400 |
| kr/minimax-m2.5-thinking-agentic | kr | HTTP 400 |
| kr/qwen3-coder-next-agentic | kr | HTTP 400 |
| kr/qwen3-coder-next-thinking | kr | HTTP 400 |
| kr/qwen3-coder-next-thinking-agentic | kr | HTTP 400 |

**Total:** 47 model gagal

## 🎯 Rekomendasi (berdasarkan latency + ketersediaan)

### Cepat (< 1000ms)

- **ag/gemini-3-flash-agent** (595ms) — Antigravity gratis via OAuth
- **ag/gemini-3.5-flash-low** (630ms) — Antigravity gratis via OAuth
- **gemini/gemini-3.1-flash-lite-preview** (672ms) — AI Studio free, kuota harian 무제한
- **ag/gemini-3.6-flash-low** (721ms) — Antigravity gratis via OAuth
- **ag/gemini-3.5-flash-extra-low** (820ms) — Antigravity gratis via OAuth

### Vision-capable (bisa proses gambar)

- **ag/gemini-3-flash-agent** (595ms)
- **ag/gemini-3.5-flash-low** (630ms)
- **gemini/gemini-3.1-flash-lite-preview** (672ms)
- **ag/gemini-3.6-flash-low** (721ms)
- **ag/gemini-3.5-flash-extra-low** (820ms)

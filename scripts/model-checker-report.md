# Model Checker Report — 30 Aug 2026 14:00 WIB

Server: 9router (127.0.0.1:20128)
Total model di catalog: 89
Model accessible: 39
Model inaccessible: 50

## Per Provider Summary

### AG (16 models)
- **OK:** 14 | **FAIL:** 2
- Latency: min=972ms, avg=4150ms, max=8732ms

### GEMINI (7 models)
- **OK:** 5 | **FAIL:** 2
- Latency: min=1556ms, avg=3826ms, max=10414ms

### GH (32 models)
- **OK:** 15 | **FAIL:** 17
- Latency: min=558ms, avg=1876ms, max=5534ms

### KR (34 models)
- **OK:** 5 | **FAIL:** 29
- Latency: min=1845ms, avg=4996ms, max=14572ms

## 🆓 Model GRATIS / Free Tier (bisa dipakai tanpa biaya)

| Model | Provider | Latency | Keterangan |
|-------|----------|---------|------------|
| ag/gemini-3.5-flash-extra-low | ag | 972ms | Antigravity gratis via OAuth |
| ag/gemini-3.5-flash-low | ag | 1094ms | Antigravity gratis via OAuth |
| ag/gemini-3-flash-agent | ag | 1294ms | Antigravity gratis via OAuth |
| ag/gemini-3-flash | ag | 1534ms | Antigravity gratis via OAuth |
| gemini/gemini-3.1-flash-lite-preview | gemini | 1556ms | AI Studio free, kuota harian 무제한 |
| gemini/gemini-3.5-flash-lite | gemini | 1673ms | AI Studio free, kuota harian 무제한 |
| gemini/gemma-4-31b-it | gemini | 1861ms | AI Studio free, ada batas kuota |
| ag/claude-opus-4-6-thinking | ag | 2209ms | Antigravity gratis via OAuth |
| ag/claude-sonnet-4-6 | ag | 2350ms | Antigravity gratis via OAuth |
| ag/gemini-3.1-pro-low | ag | 3365ms | Antigravity gratis via OAuth |
| gemini/gemini-3-flash-preview | gemini | 3624ms | AI Studio free, ada batas kuota |
| ag/gemini-pro-agent | ag | 4854ms | Antigravity gratis via OAuth |
| ag/gemini-3.6-flash-low | ag | 4934ms | Antigravity gratis via OAuth |
| ag/gemini-3.6-flash-high | ag | 5646ms | Antigravity gratis via OAuth |
| ag/gemini-3.7-flash-low | ag | 5655ms | Antigravity gratis via OAuth |
| ag/gemini-3.6-flash-medium | ag | 7057ms | Antigravity gratis via OAuth |
| ag/gemini-3.7-flash-medium | ag | 8399ms | Antigravity gratis via OAuth |
| ag/gemini-3.7-flash-high | ag | 8732ms | Antigravity gratis via OAuth |
| gemini/gemini-3.6-flash | gemini | 10414ms | AI Studio free, ada batas kuota |

**Total:** 19 model gratis

## 💰 Model Berbayar / Kuota Besar

| Model | Provider | Latency | Keterangan |
|-------|----------|---------|------------|
| kr/minimax-m2.5 | kr | 1845ms | Kiro subscription |
| kr/claude-haiku-4.5 | kr | 2021ms | Kiro subscription |
| kr/claude-sonnet-4.5 | kr | 2598ms | Kiro subscription |
| kr/minimax-m2.1 | kr | 3942ms | Kiro subscription |
| kr/auto | kr | 14572ms | Kiro subscription |

**Total:** 5 model berbayar

## ❌ Model Tidak Accessible

| Model | Provider | Error |
|-------|----------|-------|
| ag/gemini-3.5-flash-high | ag | HTTP 404 |
| ag/gpt-oss-120b-medium | ag | HTTP 400 |
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
| kr/claude-haiku-4.5-thinking-agentic | kr | timed out |
| kr/claude-sonnet-4 | kr | timed out |
| kr/claude-sonnet-4-agentic | kr | HTTP 400 |
| kr/claude-sonnet-4-thinking | kr | HTTP 400 |
| kr/claude-sonnet-4-thinking-agentic | kr | HTTP 400 |
| kr/claude-sonnet-4.5-agentic | kr | HTTP 400 |
| kr/claude-sonnet-4.5-thinking | kr | HTTP 400 |
| kr/claude-sonnet-4.5-thinking-agentic | kr | HTTP 400 |
| kr/deepseek-3.2 | kr | timed out |
| kr/deepseek-3.2-agentic | kr | HTTP 400 |
| kr/deepseek-3.2-thinking | kr | HTTP 400 |
| kr/deepseek-3.2-thinking-agentic | kr | HTTP 400 |
| kr/glm-5 | kr | timed out |
| kr/glm-5-agentic | kr | HTTP 400 |
| kr/glm-5-thinking | kr | HTTP 400 |
| kr/glm-5-thinking-agentic | kr | HTTP 400 |
| kr/minimax-m2.1-agentic | kr | HTTP 400 |
| kr/minimax-m2.1-thinking | kr | HTTP 400 |
| kr/minimax-m2.1-thinking-agentic | kr | HTTP 400 |
| kr/minimax-m2.5-agentic | kr | HTTP 400 |
| kr/minimax-m2.5-thinking | kr | HTTP 400 |
| kr/minimax-m2.5-thinking-agentic | kr | HTTP 400 |
| kr/qwen3-coder-next | kr | timed out |
| kr/qwen3-coder-next-agentic | kr | HTTP 400 |
| kr/qwen3-coder-next-thinking | kr | HTTP 400 |
| kr/qwen3-coder-next-thinking-agentic | kr | HTTP 400 |

**Total:** 50 model gagal

## 🎯 Rekomendasi (berdasarkan latency + ketersediaan)

### Cepat (< 1000ms)

- **ag/gemini-3.5-flash-extra-low** (972ms) — Antigravity gratis via OAuth
- **ag/gemini-3.5-flash-low** (1094ms) — Antigravity gratis via OAuth
- **ag/gemini-3-flash-agent** (1294ms) — Antigravity gratis via OAuth
- **ag/gemini-3-flash** (1534ms) — Antigravity gratis via OAuth
- **gemini/gemini-3.1-flash-lite-preview** (1556ms) — AI Studio free, kuota harian 무제한

### Vision-capable (bisa proses gambar)

- **ag/gemini-3.5-flash-extra-low** (972ms)
- **ag/gemini-3.5-flash-low** (1094ms)
- **ag/gemini-3-flash-agent** (1294ms)
- **ag/gemini-3-flash** (1534ms)
- **gemini/gemini-3.1-flash-lite-preview** (1556ms)

# Model Checker Report — 11 Nov 2026 15:37 WIB

Server: 9router (127.0.0.1:20128)
Total model di catalog: 83
Model accessible: 50
Model inaccessible: 33

## Per Provider Summary

### AGNES (1 models)
- **OK:** 1 | **FAIL:** 0
- Latency: min=613ms, avg=613ms, max=613ms

### AG (3 models)
- **OK:** 3 | **FAIL:** 0
- Latency: min=1748ms, avg=3063ms, max=4664ms

### AGNES (2 models)
- **OK:** 2 | **FAIL:** 0
- Latency: min=474ms, avg=535ms, max=596ms

### COMBO-FREETOKEN (1 models)
- **OK:** 0 | **FAIL:** 1

### GEMINI (4 models)
- **OK:** 4 | **FAIL:** 0
- Latency: min=884ms, avg=2600ms, max=5031ms

### KR (30 models)
- **OK:** 30 | **FAIL:** 0
- Latency: min=1147ms, avg=3367ms, max=9345ms

### MMF (1 models)
- **OK:** 0 | **FAIL:** 1

### MUSE (5 models)
- **OK:** 0 | **FAIL:** 5

### NOUS (5 models)
- **OK:** 2 | **FAIL:** 3
- Latency: min=3004ms, avg=3546ms, max=4088ms

### OC (24 models)
- **OK:** 8 | **FAIL:** 16
- Latency: min=541ms, avg=2426ms, max=5729ms

### OFF-COMBO-A2A (1 models)
- **OK:** 0 | **FAIL:** 1

### OFF-COMBO-DELEGASI (1 models)
- **OK:** 0 | **FAIL:** 1

### OFF-COMBO-GATEWAY (1 models)
- **OK:** 0 | **FAIL:** 1

### OFF-OC-COMBO-1 (1 models)
- **OK:** 0 | **FAIL:** 1

### OFF-OC-COMBO-2 (1 models)
- **OK:** 0 | **FAIL:** 1

### OFF-OC-COMBO-3 (1 models)
- **OK:** 0 | **FAIL:** 1

### OFF-OPENCODE-COMBO (1 models)
- **OK:** 0 | **FAIL:** 1

## 🆓 Model GRATIS / Free Tier (bisa dipakai tanpa biaya)

| Model | Provider | Latency | Keterangan |
|-------|----------|---------|------------|
| gemini/gemini-3-flash-preview | gemini | 884ms | AI Studio free, ada batas kuota |
| kr/deepseek-3.2 | kr | 1147ms | Kiro — model tertentu gratis terbatas |
| kr/deepseek-3.2-agentic | kr | 1500ms | Kiro — model tertentu gratis terbatas |
| kr/deepseek-3.2-thinking | kr | 1546ms | Kiro — model tertentu gratis terbatas |
| ag/claude-sonnet-4-6 | ag | 1748ms | Antigravity gratis via OAuth |
| gemini/gemini-3.6-flash | gemini | 1821ms | AI Studio free, ada batas kuota |
| kr/qwen3-coder-next-agentic | kr | 1821ms | Kiro — model tertentu gratis terbatas |
| kr/qwen3-coder-next-thinking-agentic | kr | 1861ms | Kiro — model tertentu gratis terbatas |
| gemini/gemini-3.5-flash-lite | gemini | 2662ms | AI Studio free, kuota harian unlimited |
| ag/claude-opus-4-6-thinking | ag | 2778ms | Antigravity gratis via OAuth |
| kr/deepseek-3.2-thinking-agentic | kr | 3418ms | Kiro — model tertentu gratis terbatas |
| kr/qwen3-coder-next-thinking | kr | 3647ms | Kiro — model tertentu gratis terbatas |
| ag/gemini-3.8-flash-medium | ag | 4664ms | Antigravity gratis via OAuth |
| gemini/gemini-3.1-flash-lite-preview | gemini | 5031ms | AI Studio free, kuota harian unlimited |
| kr/qwen3-coder-next | kr | 9345ms | Kiro — model tertentu gratis terbatas |

**Total:** 15 model gratis

## 💰 Model Berbayar / Kuota Besar

| Model | Provider | Latency | Keterangan |
|-------|----------|---------|------------|
| kr/glm-5-thinking-agentic | kr | 1253ms | Kiro subscription |
| kr/glm-5-agentic | kr | 1394ms | Kiro subscription |
| kr/claude-haiku-4.5 | kr | 1400ms | Kiro subscription |
| kr/glm-5-thinking | kr | 1500ms | Kiro subscription |
| kr/auto | kr | 1647ms | Kiro subscription |
| kr/claude-sonnet-4.5 | kr | 2122ms | Kiro subscription |
| kr/auto-thinking | kr | 2182ms | Kiro subscription |
| kr/glm-5 | kr | 2238ms | Kiro subscription |
| kr/claude-haiku-4.5-agentic | kr | 2265ms | Kiro subscription |
| kr/claude-sonnet-4.5-agentic | kr | 2573ms | Kiro subscription |
| kr/claude-haiku-4.5-thinking | kr | 3111ms | Kiro subscription |
| kr/minimax-m2.1-agentic | kr | 3134ms | Kiro subscription |
| kr/minimax-m2.1-thinking-agentic | kr | 3807ms | Kiro subscription |
| kr/minimax-m2.5 | kr | 4017ms | Kiro subscription |
| kr/minimax-m2.1 | kr | 4223ms | Kiro subscription |
| kr/minimax-m2.5-thinking | kr | 4729ms | Kiro subscription |
| kr/minimax-m2.5-thinking-agentic | kr | 5411ms | Kiro subscription |
| kr/minimax-m2.5-agentic | kr | 5614ms | Kiro subscription |
| kr/claude-sonnet-4.5-thinking | kr | 5640ms | Kiro subscription |
| kr/claude-haiku-4.5-thinking-agentic | kr | 5682ms | Kiro subscription |
| kr/minimax-m2.1-thinking | kr | 6138ms | Kiro subscription |
| kr/claude-sonnet-4.5-thinking-agentic | kr | 6636ms | Kiro subscription |

**Total:** 22 model berbayar

## ❌ Model Tidak Accessible

| Model | Provider | Error |
|-------|----------|-------|
| combo-freetoken | combo-freetoken | HTTP 404 |
| mmf/mimo-auto | mmf | HTTP 400 |
| muse/muse-spark-1.1 | muse | HTTP 400 |
| muse/muse-spark-1.2 | muse | HTTP 400 |
| muse/muse-spark-1.2-contributor | muse | HTTP 400 |
| muse/muse-spark-1.3 | muse | HTTP 400 |
| muse/muse-spark-1.3-contributor | muse | HTTP 400 |
| nous/reflection/beam-1.0-501b-a23b:free | nous | HTTP 503 |
| nous/stealth/crouton-alpha | nous | HTTP 503 |
| nous/stepfun/step-3.7-flash:free | nous | 'NoneType' object is not subscriptable |
| oc/cat-jam-free | oc | HTTP 400 |
| oc/crouton-alpha-free | oc | HTTP 410 |
| oc/exo-free | oc | HTTP 400 |
| oc/fledge-alpha-free | oc | HTTP 400 |
| oc/jev-1.13-free | oc | HTTP 400 |
| oc/ling-3.0-flash-fin-free | oc | HTTP 400 |
| oc/ling-3.1-flash-free | oc | HTTP 400 |
| oc/longcat-2.5-preview-free | oc | HTTP 400 |
| oc/mimo-v2.5-free | oc | HTTP 400 |
| oc/muse-spark-1.2-contributor-free | oc | HTTP 400 |
| oc/muse-spark-1.3-contributor-free | oc | HTTP 400 |
| oc/nemotron-3-ultra-free | oc | HTTP 400 |
| oc/pulse-alpha-free | oc | HTTP 400 |
| oc/space-bunny-free | oc | HTTP 400 |
| oc/step-5-preview-free | oc | HTTP 400 |
| oc/union-alpha | oc | HTTP 400 |
| off-combo-a2a | off-combo-a2a | HTTP 400 |
| off-combo-delegasi | off-combo-delegasi | HTTP 400 |
| off-combo-gateway | off-combo-gateway | HTTP 400 |
| off-oc-combo-1 | off-oc-combo-1 | HTTP 400 |
| off-oc-combo-2 | off-oc-combo-2 | HTTP 400 |
| off-oc-combo-3 | off-oc-combo-3 | HTTP 400 |
| off-opencode-combo | off-opencode-combo | HTTP 400 |

**Total:** 33 model gagal

## 🎯 Rekomendasi (berdasarkan latency + ketersediaan)

### Cepat (< 1000ms)

- **gemini/gemini-3-flash-preview** (884ms) — AI Studio free, ada batas kuota
- **kr/deepseek-3.2** (1147ms) — Kiro — model tertentu gratis terbatas
- **kr/glm-5-thinking-agentic** (1253ms) — Kiro subscription
- **kr/glm-5-agentic** (1394ms) — Kiro subscription
- **kr/claude-haiku-4.5** (1400ms) — Kiro subscription

### Vision-capable (bisa proses gambar)

- **gemini/gemini-3-flash-preview** (884ms)
- **kr/claude-haiku-4.5** (1400ms)
- **gemini/gemini-3.6-flash** (1821ms)
- **kr/claude-sonnet-4.5** (2122ms)
- **kr/claude-haiku-4.5-agentic** (2265ms)

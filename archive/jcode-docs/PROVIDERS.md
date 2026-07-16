# Setup AI Provider

jcode mendukung banyak provider AI. Pilih yang sesuai dengan kebutuhan Anda.

## Provider yang Didukung

### First-Party / Native
| Provider | Command | Deskripsi |
|----------|---------|-----------|
| **Claude** | `jcode login --provider claude` | Anthropic Claude (subscription OAuth) |
| **OpenAI** | `jcode login --provider openai` | OpenAI / ChatGPT / Codex |
| **GitHub Copilot** | `jcode login --provider copilot` | GitHub Copilot subscription |
| **Gemini** | `jcode login --provider gemini` | Google Gemini |
| **Azure OpenAI** | `jcode login --provider azure` | Azure OpenAI Service |
| **Alibaba Coding** | `jcode login --provider alibaba-coding-plan` | Alibaba Cloud Coding Plan |

### Aggregator / Compatibility
| Provider | Command | Deskripsi |
|----------|---------|-----------|
| **OpenRouter** | Set `OPENROUTER_API_KEY` | Multi-model aggregator |
| **OpenAI-compatible** | `jcode login --provider openai-compatible` | Self-hosted endpoint |

### Additional
`opencode`, `opencode-go`, `zai/kimi`, `302ai`, `baseten`, `cortecs`, `deepseek`, `firmware`, `huggingface`, `moonshotai`, `nebius`, `scaleway`, `stackit`, `groq`, `mistral`, `perplexity`, `togetherai`, `deepinfra`, `fireworks`, `minimax`, `xai`, `lmstudio`, `ollama`, `chutes`, `cerebras`, `cursor`, `antigravity`, `google`

## Rekomendasi Setup

### 0. OpenRouter (Gratis - Aktif Digunakan)
```bash
# Set API key di shell profile
export OPENROUTER_API_KEY="sk-or-v1-..."

# Set di ~/.jcode/config.toml
[provider]
default_provider = "openrouter"
default_model = "z-ai/glm-4.5-air:free"
```
Model dengan suffix `:free` **tidak consume credits**. Lihat list lengkap di https://openrouter.ai/models?max_price=0

### 1. Claude (Recommended untuk coding)
```bash
jcode login --provider claude
```
- Buka browser untuk OAuth
- Login dengan akun Anthropic
- Cache berlaku 5 menit — jcode akan warning jika cache "cold"

### 2. OpenAI / ChatGPT Pro
```bash
jcode login --provider openai
```
- Callback di `http://localhost:1455/auth/callback`
- Support multi-account switching via `/account`

### 3. GitHub Copilot
```bash
jcode login --provider copilot
```
- Menggunakan device flow
- Untuk headless: `jcode login --provider copilot --print-auth-url --json`
- Complete: `jcode login --provider copilot --complete`

### 4. OpenAI-Compatible Endpoint (Self-Hosted)
```bash
# Dengan API key
printf '%s' "$MY_API_KEY" | jcode provider add my-api \
  --base-url https://llm.example.com/v1 \
  --model my-model-id \
  --api-key-stdin \
  --set-default \
  --json

# Tanpa API key (local server)
jcode provider add local-vllm \
  --base-url http://localhost:8000/v1 \
  --model Qwen/Qwen3-Coder-30B-A3B-Instruct \
  --no-api-key \
  --set-default
```

### 5. Ollama (Local Models)
```bash
jcode login --provider ollama
```

### 6. LM Studio (Local Models)
```bash
jcode login --provider lmstudio
```

## Headless / No-Browser Login

Untuk SSH atau server tanpa browser:

```bash
jcode login --provider claude --no-browser
jcode login --provider openai --headless
```

Akan mencetak URL/QR untuk auth manual.

## Scriptable Login (Two-Step)

```bash
# Step 1: Print auth URL
jcode login --provider openai --print-auth-url --json

# Step 2: Complete setelah auth
jcode login --provider openai --callback-url 'http://localhost:1455/auth/callback?...'
jcode login --provider gemini --auth-code '...'
```

## Config File Manual

Config disimpan di `~/.jcode/config.toml`:

```toml
[provider]
default_provider = "claude"
default_model = "claude-sonnet-4-20250514"

[providers.my-api]
type = "openai-compatible"
base_url = "https://llm.example.com/v1"
api_key_env = "JCODE_PROVIDER_MY_API_API_KEY"
default_model = "my-model-id"

[[providers.my-api.models]]
id = "my-model-id"
context_window = 128000
```

## Environment Variables per Provider

| Provider | Env Variable |
|----------|-------------|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| OpenAI-compatible | `JCODE_OPENAI_COMPAT_API_BASE` |
| Fireworks | `FIREWORKS_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| NVIDIA NIM | `NVIDIA_API_KEY` |

## Multi-Account Switching

Jika punya beberapa akun (misal 2x ChatGPT Pro):
```bash
# Dari dalam TUI
/account
```

## Verifikasi Setup

```bash
# Test semua provider yang dikonfigurasi
jcode auth-test --all-configured

# Test provider spesifik
jcode --provider-profile my-api auth-test --prompt 'Reply OK'

# Smoke test
jcode run "say hello"
```

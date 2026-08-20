# Provider Evolution — Niumination (Data Valid dari Backup Files)

> **Sumber:** 18 config backup files di `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml*`
> **Periode:** Juni — Agustus 2026
> **Metode:** Python script extract provider/model dari setiap backup

## Kronologi Provider

| # | Tanggal | Provider | Model Default | Base URL | Backup File |
|---|---------|----------|---------------|----------|-------------|
| 1 | Jun 30 — Jul 5 | `opencode-zen` | `big-pickle` | `opencode.ai/zen/v1` | .bak.20260630, .bak.20260705a/b |
| 2 | Jul 7a | **`nvidia_nim`** | `deepseek-v4-pro` | `integrate.api.nvidia.com` | .bak.20260707_225923 |
| 3 | Jul 7c | `opencode-zen` | `big-pickle` | `opencode.ai/zen/v1` | .bak.20260707_231023 |
| 4 | Jul 15a | **`auto`** | `deepseek-v4-flash-free` | *(kosong)* | .bak.20260715_174514 |
| 5 | Jul 15b | **`agentrouter`** | `big-pickle` | `agentrouter.org/v1` | .bak.20260715_233236 |
| 6 | Jul 17 | `opencode-zen` | `big-pickle` | `opencode.ai/zen/v1` | .bak.20260717_154239 |
| 7 | Jul 18 | **`custom` (9router)** | `gc/gemini-2.5-flash` | `localhost:20128/v1` | .bak.20260718_before_rollback |
| 8 | Jul 19 — Jul 23a | `opencode-zen` | `big-pickle` | `opencode.ai/zen/v1` | .bak (restore) |
| 9 | Jul 23d | **`nous`** | `stepfun/step-3.7-flash:free` | `nousresearch.com/v1` | .bak.20260723_180653 |
| 10 | Aug 8 | `opencode-zen` | `big-pickle` | `opencode.ai/zen/v1` | .bak-20260808 |
| 11 | Aug 13a | **`9router`** | `gratis` | `api.hcnsec.cn/v1` | .bak.20260813_140401 |
| 12 | Aug 13d | `opencode-zen` | `big-pickle` | `opencode.ai/zen/v1` | .bak.20260813_151552 |
| 13 | SEKARANG | `opencode-zen` | `big-pickle` | `opencode.ai/zen/v1` | config.yaml (18628 bytes) |

## Provider yang Pernah Dicoba

| Provider | Status | Kapan | Lama Aktif |
|----------|--------|-------|------------|
| `opencode-zen` | ✅ Aktif sekarang | Jun — sekarang | ~70% waktu |
| `nvidia_nim` | ❌ Dicoba, kembali | Jul 7 | 1 hari |
| `agentrouter` | ❌ 401 Unauthorized | Jul 15 | 1 hari |
| `custom` (9router local) | ⚠️ Lokal | Jul 18 | Beberapa hari |
| `nous` | ❌ Auth expired | Jul 23 | 1 hari |
| `9router` (hcnsec.cn) | ⚠️ Pernah primary | Aug 13 | Beberapa hari |
| `juan-router` | ✅ Fallback aktif | Sekarang | — |
| `huancheng` | ✅ Config + key ada | Sekarang | — |
| `openrouter` | ⚠️ Fallback, key kosong | Sekarang | — |

## Plugin Evolution

| Periode | Plugins Aktif | Source |
|---------|---------------|--------|
| Jun 30 — Jul 7 | `spotify`, `rtk-rewrite` | .bak.20260630 |
| Jul 15a | `orca-status`, `rtk-rewrite`, `spotify`, `hermes-cli` | .bak.20260715_174514 |
| Jul 15b | `orca-status`, `rtk-rewrite`, `spotify` | .bak.20260715_233236 |
| Jul 17 | `telegram-router` (saja?) | .bak.20260717_154239 |
| Jul 19 — Jul 23 | `orca-status`, `rtk-rewrite`, `spotify` | .bak, .bak.20260723 |
| Aug 8 | `orca-status`, `rtk-rewrite`, `spotify`, `provider`, `provider` | .bak-20260808 |
| Aug 13 | Parsing error: `provider`, `asisten`, `agent` | .bak.20260813 |
| SEKARANG (folder) | `rtk-rewrite`, `orca-status`, `hermes-achievements`, `telegram_router` | ls plugins/ |

## Fallback Provider Evolution

| Periode | Fallback |
|---------|----------|
| Jun — Jul 7 | `openrouter` |
| Jul 17 — Jul 23 | `openrouter` |
| Aug 8 | `aerolink` |
| Aug 13 | `9router` |
| SEKARANG | `juan-router` → `9router` → `9router`

## Extract Script

```python
import re, os

data_dir = "/Volumes/HermesAgent/HermesAgentUSB/data/"
backups = sorted([
    f for f in os.listdir(data_dir)
    if f.startswith("config.yaml") and f != "config.yaml"
])

results = []
for bak in backups:
    path = os.path.join(data_dir, bak)
    if not os.path.exists(path):
        continue
    with open(path) as f:
        content = f.read()
    
    provider = re.search(r'^\s+provider:\s*(.+)', content, re.M)
    default_model = re.search(r'^\s+default:\s*(.+)', content, re.M)
    base_url = re.search(r'^\s+base_url:\s*(.+)', content, re.M)
    has_overrides = 'channel_overrides' in content
    has_prompts = 'channel_prompts' in content
    
    print(f"=== {bak} ({os.path.getsize(path)} bytes) ===")
    print(f"  Provider: {provider.group(1).strip() if provider else 'N/A'}")
    print(f"  Model: {default_model.group(1).strip() if default_model else 'N/A'}")
    print(f"  Base URL: {base_url.group(1).strip() if base_url else 'N/A'}")
    print(f"  Overrides: {has_overrides} | Prompts: {has_prompts}")
    print()
```

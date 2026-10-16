# Update: Kimi Models Investigation — 29 Ags 2026

## Finding
**Kimi models TIDAK TERSEDIA di 9router.** Telah dihapus/dipindahkan dari katalog.

## Evidence
```
=== KIMI MODELS ON 9ROUTER ===

Total models: 89
Kimi-related: 0

❌ NO KIMI MODELS FOUND on 9router!
```

## Test Details
- Tested 10 kimi model IDs: `kimi/kimi-k3`, `kimi/k3`, `kimi/kimi-for-coding`, dll
- All returned HTTP 404
- No Moonshot AI models in current catalog

## Available Alternatives on 9router (kr/ prefix)
| Model | Status | Latency | Use Case |
|-------|--------|---------|----------|
| kr/qwen3-coder-next | ✅ OK | 1018ms | Coding (fastest) |
| kr/deepseek-3.2 | ✅ OK | 3402ms | General purpose |
| kr/claude-haiku-4.5 | ✅ OK | 1302ms | Fast responses |
| kr/claude-sonnet-4 | ✅ OK | 2558ms | Reasoning |
| kr/minimax-m2.5 | ✅ OK | 4245ms | Alternative |

## Action Taken
- Updated `references/provider-status-2026-08-29.md` dengan catatan bahwa kimi models tidak tersedia
- Dokumentasi lengkap: `~/.hermes/kimi-investigation-report.md`

## Conclusion
Jika user membutuhkan model mirip Kimi (coding/agentic), gunakan alternatif di atas atau pertimbangkan OpenRouter yang masih memiliki `moonshotai/kimi-k3`.

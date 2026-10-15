# OpenCode Go Integration Reference
> Date: 2026-08-31
> Status: Integration tested, pending payment activation

## Overview

OpenCode Go adalah subscription service ($10/bulan) yang menyediakan akses ke 30+ model AI populer dari Chinese labs (DeepSeek, Zhipu, Xiaomi, MiniMax, dll).

## Workspace & Activation

Setiap workspace Go memiliki ID unik. Untuk mengaktifkan:

1. **Buka workspace**: `https://opencode.ai/workspace/<workspace-id>/go`
2. **Opt-in models**: Klik model yang ingin digunakan (deepseek-v4-flash, glm-5.3-flash, dll)
3. **Add payment method**: `https://opencode.ai/workspace/<workspace-id>/billing`
4. **Generate API key**: Setelah subscription aktif, key yang sama bisa dipakai untuk semua model yang sudah di-opt-in

## API Endpoints

| Endpoint | Purpose | Auth |
|----------|---------|------|
| `https://opencode.ai/zen/go/v1/models` | List available models | Bearer key |
| `https://opencode.ai/zen/go/v1/chat/completions` | Chat completion | Bearer key |

## Available Models (Verified 31 Agu 2026)

### Fast & Cost-Effective
- `deepseek-v4-flash` — 94% cache, $0.105/session, BEST FOR JSON
- `glm-5.3-flash` — 93% cache, $0.022/session, CHEAPEST
- `mimo-v2.5` — 94% cache, $0.003/session, MOST ECONOMICAL

### Advanced
- `deepseek-v4-pro` — Most capable DeepSeek
- `kimi-k2.7-code` — Optimized for code
- `qwen3.7-plus` — Multilingual (good for Indonesian)
- `minimax-m3` — General purpose

### Vision
- `deepseek-v4-flash-vision-exp` — Multimodal

## Common Errors & Solutions

### Error: `Invalid API key`
**Cause**: Key belum di-link ke workspace Go, atau key untuk endpoint berbeda (Zen vs Go).
**Fix**: 
1. Verify key works: `curl https://opencode.ai/zen/go/v1/models -H "Authorization: Bearer $KEY"`
2. If 200 but chat fails, key is valid but model needs opt-in
3. If 401, generate new key from Go workspace dashboard

### Error: `RegionError - requires explicit opt in`
**Cause**: Model belum diaktifkan di workspace Go.
**Fix**: Buka workspace Go, klik opt-in model yang diinginkan.

### Error: `No payment method`
**Cause**: Subscription Go belum aktif.
**Fix**: Tambah payment method di billing workspace.

### Error: `Model not found`
**Cause**: Model tidak tersedia di subscription tier saat ini.
**Fix**: List models dengan `/v1/models`, pilih yang tersedia.

## Integration with cc-acehtengah (SAPA Smart AI)

### Environment Variables
```bash
AI_BASE_URL=https://opencode.ai/zen/go/v1
AI_API_KEY=<your-go-key>
AI_MODEL=deepseek-v4-flash
```

### Vercel Deployment
```bash
vercel env add AI_BASE_URL production -- "https://opencode.ai/zen/go/v1"
vercel env add AI_API_KEY production -- "<key>"
vercel env add AI_MODEL production -- "deepseek-v4-flash"
vercel deploy --prod
```

### Testing
```bash
# Test connectivity
curl -s https://opencode.ai/zen/go/v1/models \
  -H "Authorization: Bearer $AI_API_KEY" | python3 -c "import sys,json; print(f'{len(json.load(sys.stdin)[\"data\"])} models available')"

# Test chat
curl -s -X POST https://opencode.ai/zen/go/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AI_API_KEY" \
  -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Test"}],"max_tokens":50}'
```

## Cost Estimation

Untuk SAPA Smart AI dengan beban rata-rata:
- 100 queries/hari × 5000 tokens/input + 1000 tokens/output
- ~150K tokens/hari = ~4.5M tokens/bulan
- Cost dengan `deepseek-v4-flash`: ~$4.7/bulan (di bawah limit $60/bulan)
- Cost dengan `glm-5.3-flash`: ~$0.9/bulan (lebih hemat)

## References

- OpenCode Go Docs: https://opencode.ai/docs/go/
- Model Data & Rankings: https://opencode.ai/data/
- Workspace Dashboard: https://opencode.ai/workspace/

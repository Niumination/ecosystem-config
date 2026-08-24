# Provider Troubleshooting — 13 Agustus 2026

## Masalah Utama yang Ditemukan

### 1. Huancheng API Key Invalid

**Symptom:**
```
{"error":{"code":"","message":"Invalid token (request id: ...)"}}
```

**Diagnosis:**
```bash
curl -s --max-time 10 -X POST https://api.hcnsec.cn/v1/chat/completions \
  -H "Authorization: Bearer $HUANCHENG_API_KEY" \
  -d '{"model":"auto","messages":[{"role":"user","content":"test"}]}'
```

**Status:** Token tidak valid — kemungkinan expired atau revoked. Tidak bisa digunakan sampai key baru di-regenerate.

### 2. AgentRouter Unauthorized

**Symptom:**
```
{"error":{"message":"unauthorized client detected, contact support..."}}
```

**Diagnosis:**
```bash
curl -s --max-time 10 -X POST https://agentrouter.org/v1/chat/completions \
  -H "Authorization: Bearer $AGENTROUTER_API_KEY" \
  -d '{"model":"auto","messages":[{"role":"user","content":"test"}]}'
```

**Status:** Client unauthorized — kemungkinan IP restriction atau account issue.

### 3. OpenRouter API Key Kosong

**Diagnosis:**
```bash
echo "OPENROUTER_API_KEY: ${#OPENROUTER_API_KEY} chars"
# Output: OPENROUTER_API_KEY: 0 chars
```

**Status:** Lingkungan tidak memiliki OPENROUTER_API_KEY yang di-set.

### 4. Aerolink Endpoint 404

**Symptom:** Mengembalikan halaman HTML "404: This page could not be found" bukan JSON API response.

**Status:** Endpoint `https://aerolink.lat/v1/chat/completions` tidak ditemukan.

### 5. 9Router lokal berfungsi

**Diagnosis:**
```bash
curl -s http://localhost:20128/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('data',[])))"
# Output: 48
```

**Status:** Berjalan normal, 48 model tersedia.

## Solusi yang Diterapkan

1. Ganti provider default di config.yaml dari `huancheng` → `9router`
2. Ganti model default dari `auto` → `gratis` (DeepSeek-V4-Flash)
3. Simpan dokumentasi di `brain/infra/hermes-config-fix-2026-08-13.md`

## Cara Cek Sehat Tidaknya Provider

```bash
# Huancheng
curl -s --max-time 10 https://api.hcnsec.cn/v1/chat/completions \
  -H "Authorization: Bearer $HUANCHENG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"test"}]}'

# AgentRouter
curl -s --max-time 10 https://agentrouter.org/v1/chat/completions \
  -H "Authorization: Bearer $AGENTROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"test"}]}'

# OpenRouter
curl -s --max-time 10 https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"test"}]}'

# 9Router lokal
curl -s http://localhost:20128/v1/models
```

## Catatan Penting

- Provider failures menyebabkan fallback chains yang bisa membuat agent "melupakan" konteks
- Memory near 99% memperparah masalah recall
- Selalu test provider connectivity di awal session sebelum task kompleks
- Jika user menyebut provider sudah di-"switch" (misal via portal), VERIFY config.yaml dulu

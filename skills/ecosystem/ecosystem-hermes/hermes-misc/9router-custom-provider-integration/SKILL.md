---
name: 9router-custom-provider-integration
category: ecosystem
description: "Use when adding a custom provider to 9router."
tags: [9router, provider, openai-compatible, agentrouter, waf, user-agent, routing]
---

# 9Router Custom Provider Integration

Menambah provider OpenAI-compatible (mis. AgentRouter, Explabs, relay lain) ke 9router lokal :20128 lewat API, dan mendiagnosis kenapa provider hidup direct tapi gagal via 9router.

## Auth API 9router (CLI token)
Semua endpoint admin butuh header:
```bash
cd ~/.9router && TOKEN=$(python3 -c "import hashlib; mid=open('machine-id').read().strip(); sec=open('auth/cli-secret').read().strip(); print(hashlib.sha256((mid+'9r-cli-auth'+sec).encode()).hexdigest()[:16])")
# verifikasi: GET /api/provider-nodes dengan -H "x-9r-cli-token: $TOKEN" → 200
```
Token dibatasi 16 hex char. Header: `x-9r-cli-token`. Jangan pakai `Authorization: Bearer` untuk admin API ini.

## Tambah Provider (2 langkah + restart)
```bash
# 1) buat node openai-compatible → 201, id `openai-compatible-chat-<uuid>`
curl -X POST http://localhost:20128/api/provider-nodes \
  -H "x-9r-cli-token: $TOKEN" -H 'Content-Type: application/json' \
  -d '{"type":"openai-compatible","name":"agentrouter","prefix":"agentrouter","apiType":"chat","baseUrl":"https://agentrouter.org/v1"}'
# 2) daftarkan connection → 201 (data JSON di tabel providerConnections; testStatus mula-mula 'unknown')
curl -X POST http://localhost:20128/api/providers \
  -H "x-9r-cli-token: $TOKEN" -H 'Content-Type: application/json' \
  -d '{"provider":"<NODE_ID>","name":"AgentRouter","authType":"apiKey","apiKey":"<KEY>","priority":1,"isActive":true}'
# 3) restart + tunggu siap (retry sampai 200; bisa 5-10 detik)
launchctl kickstart -k gui/$(id -u)/com.9router.autostart
for i in $(seq 1 12); do curl -s -m 5 -o /dev/null -w "try$i %{http_code}\n" http://127.0.0.1:20128/v1/models; sleep 2; [ "$(curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:20128/v1/models)" = "200" ] && break; done
```

## Schema penting (sqlite `~/.9router/db/data.sqlite`)
- `providerNodes(id, type, name, data)` — `data` = `{"prefix","apiType":"chat","baseUrl"}`
- `providerConnections(id, provider→nodeId, authType, name, priority, isActive, data)` — `data.apiKey` = credential; `data.providerSpecificData` = mirror node + proxy flags
- TIDAK ada tabel model — `/v1/models` fetch LIVE dari tiap provider tiap request. Model provider baru terlihat hanya kalau upstream merespons listing dengan UA yang diterima.
- `requestDetails` mencatat request per-connection: `SELECT timestamp, provider, model, status, data FROM requestDetails WHERE provider LIKE '%<nodeId>%';` (kolom timestamp, bukan createdAt)

## Test akses setelah setup
```bash
KEY9=$(grep -o 'NINE_ROUTER_API_KEY=.*' ~/.hermes/.env | cut -d= -f2- | tr -d '"' | tr -d "'")
curl -X POST http://127.0.0.1:20128/v1/chat/completions \
  -H "Authorization: Bearer $KEY9" -H 'Content-Type: application/json' \
  -d '{"model":"agentrouter/deepseek-v4-flash","messages":[{"role":"user","content":"hello"}],"stream":false}'
# 9router butuh API key-nya SENDIRI (NINE_ROUTER_API_KEY) pada request masuk — "Missing API key" = belum dikasih auth.
```

## Pitfall: Provider ber-WAF-UA tidak bisa diakses via 9router
Relay (AgentRouter/air-outer, dsb) mem-whitelist `User-Agent`: hanya `hermes-agent/*` & `opencode/*` diterima; UA lain (curl, Node fetch, browser, claude-cli) → `401 unauthorized client detected`.
- **9router openai-compatible node TIDAK punya opsi set per-provider headers/UA** (tidak ada di API nodes, settings DB, bundle). 9router kirim UA default-nya → ditolak → chat completion 503 wrap `[401] { ... unauthorized client detected ... }` dari upstream.
- Diagnosa cepat: request langsung ke upstream dengan UA `hermes-agent/0.19.0` → kalau 200/402 vs UA lain → 401 = WAF UA. Kalau 503/401 di 9router tapi 200 direct = masalah UA forwarding, bukan key.
- **Solusi:** provider ber-WAF-UA hanya bisa dipakai via Hermes native config (`providers.<name>.extra_headers: {User-Agent: hermes-agent/<ver>}`), BUKAN via 9router custom node. Jangan buang waktu setup node 9router untuk provider semacam ini.

## Pitfall: 402 budget exhausted per-model ≠ key mati
Key yang valid di `/v1/models` (200) bisa tetap gagal di chat dengan `402 Budget pool quota has been exhausted` pada BEBERAPA model saja. Cek tiap model terpisah — satu model 200 tidak berarti semua 200. (Contoh: agentrouter deepseek-v4-flash 200, gpt-6-astra/claude-opus-5 402.) Model yang 402 = belum di-assign budget pool di dashboard provider — urusan admin provider, bukan config lokal.

## Pitfall: 9router restart butuh retry
Setelah `launchctl kickstart -k`, `/v1/models` bisa `000` selama ~5-10 detik (server belum bind) sebelum 200. Bukan crash — tunggu retry. JANGAN matikan `com.9router.autostart`.

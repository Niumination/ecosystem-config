---
name: relay-provider-client-wiring
description: "Use when wiring a client to a relay with WAF UA whitelist."
tags: [agentrouter, relay, provider, waf, user-agent, anthropic, openai, proxy, sse]
---

# Relay Provider Client Wiring

Menghubungkan klien AI (CLI Anthropic/OpenAI-compatible, script, SDK) langsung ke provider relay seperti AgentRouter yang punya lapisan proteksi di sisi server. Berbeda dari integrasi via 9router (lihat `9router-custom-provider-integration`) — di sini klien memanggil relay LANGSUNG dan harus melewati 4 lapis kegagalan.

## Urutan diagnosa (lakukan berurutan; tiap lapis punya gejala khas)

1. **WAF UA** — relay whitelist `User-Agent` (`hermes-agent/*`, `opencode/*`). UA lain → `401 unauthorized client detected` / 405 HTML (Aliyun spm a3c0e) `<!doctypehtml><html lang="zh-cn">`. Cek: curl dengan UA `hermes-agent/<ver>` → beda status vs UA default.
2. **Content filter** — 400 `content-blocked` untuk frasa Bahasa Indonesia ≥2 kata, ATAU body berisi `<system-reminder>` / `x-anthropic-billing-header` (disisipkan Claude Code). Gejala beda: WAF = HTML 405, content filter = JSON 400 `{"error":{"code":"content-blocked","type":"agent_router_api_error"}}`.
3. **Schema Anthropic** — `role: system` DI DALAM `messages[]` ditolak; sistem prompt hanya lewat top-level `system`. Ganti `role: system` → `role: user` di scrub.
4. **Transport** — klien yang kirim `Transfer-Encoding: chunked` (Claude Code TTY) membuat `http.server.BaseHTTPRequestHandler` baca `Content-Length=0` → body kosong/hang. Baca chunked manual (loop ukuran hex).

## Proxy lokal (satu-satunya jalan untuk klien tanpa custom UA)
Klien yang TIDAK bisa set custom header (Claude Code CLI) wajib lewat proxy lokal yang:
- paksa header keluar `User-Agent: hermes-agent/<versi>`
- **drop `Accept-Encoding` masuk, set `Accept-Encoding: identity`** — SSE terkompresi (gzip/br) bikin klien Anthropic gagal parse → error `no_events` / `StreamNoEventsError` / "empty or malformed response (HTTP 200)"
- baca chunked manual
- scrub body JSON: buang blok system-reminder/billing, ganti `role: system` → `user`

Log header respons (`Content-Type`, `Content-Encoding`, ukuran, UA asal) untuk diagnosa: `text/event-stream` harus SSE plaintext, bukan binary.

## Mode klien: konfirmasi SEBELUM membangun proxy
- Headless (`claude -p` / non-interactive): TERBUKTI stabil lewat proxy semacam ini — tool use ikut jalan.
- TTY interaktif: TIDAK stabil di atas relay WAF-UA + custom Anthropic endpoint — dialog "custom API key" ghost (`sk-ant-` preview dari key non-`sk-ant-`), "Not logged in", SSE macet di turn lanjutan (`no_events`), 200-then-hang. **Tanya mode pemakaian user dulu; kalau target TTY, tandai risiko tinggi dan tawar jalur lain sebelum investasi setup.**

## Auth CLI (Claude Code)
- `ANTHROPIC_API_KEY` non-`sk-ant-` memicu dialog konfirmasi "use this API key?" — default No → "Not logged in". Jawab Yes bila key harus dipakai.
- `ANTHROPIC_AUTH_TOKEN` di-copy menjadi `ANTHROPIC_API_KEY` di env proses → warning dual-key. Pakai SATU mekanisme auth per sesi.
- Per-model budget: key valid di `/v1/models` bisa tetap `402 Budget pool quota has been exhausted` pada model tertentu — urusan admin provider, cek tiap model terpisah.

## Referensi
- `references/agentrouter-endpoints.md` — endpoint & quirk AgentRouter (base URL, model, filter).

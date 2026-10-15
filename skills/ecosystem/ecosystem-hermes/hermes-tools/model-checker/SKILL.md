---
name: model-checker
description: Cek semua model 9router yang tersedia, test aksesibilitas, kategorikan gratis vs berbayar. Trigger via chat "/model-check" atau "cek model". Hasil: laporan markdown di scripts/model-checker-report.md + data JSON.
tags:
  - model
  - 9router
  - checker
  - niumination
  - latency
last_updated: "2026-09-14"
version: 2.0.0
changes:
  - Updated for 511 models across 13 providers (per 14-Sep-2026)
  - Added rapid sample approach (avoid 2-hour full test)
  - Added status of disabled providers
---

# 🔍 /model-check — Model 9router Availability Checker

## Trigger
User mengetik:
- **`/model-check`** dari Telegram (atau Hermes chat)
- **"cek model"** / **"cak model"** / **"check model"**
- **"model checker"**

## Apa yang dilakukan
Skrip `scripts/model-checker.py` akan:
1. Fetch 89 model dari 9router (localhost:20128)
2. Test setiap model dengan request singkat (max_tokens=5)
3. Handle response biasa (JSON) dan SSE (data: lines)
4. Kategorikan tiap model: gratis/free, free tier, berbayar, atau tidak accessible
5. Generate laporan markdown di `scripts/model-checker-report.md`
6. Simpan data JSON di `scripts/model-checker-data.json`
7. Print ringkasan ke stdout

## Eksekusi
```bash
cd ~/Desktop/Niumination && python3 scripts/model-checker.py
```

## Kredensial yang digunakan
- `NINE_ROUTER_API_KEY` dari environment atau `~/.hermes/.env`
- 9router SQLite: `~/.9router/db/data.sqlite` (provider connections)

## Provider yang dicheck
| Provider | Sumber | Keterangan |
|----------|--------|------------|
| `ag` | Antigravity OAuth | Gratis via OAuth |
| `gemini` | Google AI Studio key | Gratis dengan kuota harian |
| `github` | GitHub Copilot free tier | Gratis (batas harian) |
| `kr` | Kiro dashboard | Berbayar (subscription) |

## Output
Ringkasan dicetak ke stdout:
- Total model tested
- Jumlah accessible vs inaccessible
- Per-provider breakdown (OK/FAIL, latency min/avg/max)
- Kategori: gratis, free tier, berbayar, tidak accessible

Laporan lengkap tersimpan di `scripts/model-checker-report.md` (Markdown table).

## Kategori model
- **Gratis:** gemini (AI Studio free), github (Copilot free), ag (Antigravity free), kimi (gratis tapi sering error)
- **Free tier:** Kiro model tertentu (qwen3-coder-next, deepseek-3.2) — gratis terbatas
- **Berbayar:** Kiro subscription models (claude-haiku-4.5, claude-sonnet-4*, minimax-m2.5, auto)
- **Tidak accessible:** HTTP error (400/404/429/503) atau timeout

## Rekomendasi cepat (dari laporan 30 Agu 2026)
- **Coding cepat:** ag/gemini-3-flash-agent (595ms), ag/gemini-3.5-flash-low (630ms)
- **Chat gratis:** gemini/gemini-3.5-flash-lite (829ms), gh/gpt-4o-mini (668ms)
- **Vision:** semua model ag/gemini-* dan gemini/gemini-* punya vision capability
- **Berbayar Kiro:** claude-sonnet-4.5 (2050ms), claude-haiku-4.5 (1119ms)

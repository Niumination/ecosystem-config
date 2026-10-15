# Kiro Models Status — 30 Ags 2026

## Summary
**Kiro (kr/) models: 5/34 WORKING** — sebagian besar sudah TIMEOUT atau HTTP 400.

## Current State (14:00 WIB)

### ✅ Working (5 models)
| Model | Latency | Status |
|-------|---------|--------|
| kr/minimax-m2.5 | 1845ms | Berbayar |
| kr/claude-haiku-4.5 | 2021ms | Berbayar |
| kr/claude-sonnet-4.5 | 2598ms | Berbayar |
| kr/minimax-m2.1 | 3942ms | Berbayar |
| kr/auto | 14572ms | ⚠️ Very slow |

### ❌ Not Working (29 models)
- Semua model `*-thinking` → HTTP 400
- Semua model `*-agentic` → HTTP 400
- Semua model `*-thinking-agentic` → HTTP 400 atau TIMEOUT
- `kr/qwen3-coder-next` → TIMEOUT (sebelumnya OK 869ms, sekarang habis quota)
- `kr/deepseek-3.2` → TIMEOUT (sebelumnya OK 804ms, sekarang habis quota)
- `kr/claude-sonnet-4` → TIMEOUT
- `kr/glm-5` → TIMEOUT

## User Context
User (Afrizal Munthe) baru saja mendaftarkan Kiro di dashboard 9router. Model **kr/claude-opus-5** TIDAK DITEMUKAN di catalog.

## Investigation Notes
1. Total 89 models di catalog
2. 39 accessible (44%), 50 inaccessible (56%)
3. Kiro prefix = berbayar subscription, free tier models sudah habis quota
4. pattern: suffix `-thinking`, `-agentic`, `-thinking-agentic` = error 400 (bukan model valid)

## Recommendations
- Gunakan model AG (Antigravity) yang GRATIS: `ag/gemini-3.5-flash-extra-low` (972ms)
- Untuk coding: `ag/gemini-3-flash-agent` (1294ms) — gratis & stabil
- Untuk reasoning kuat: `ag/claude-opus-4-6-thinking` (2209ms) — gratis

## Source
- Report: `~/Desktop/Niumination/scripts/model-checker-report.md`
- Data: `~/Desktop/Niumination/scripts/model-checker-data.json`
- Skill: `ecosystem/model-checker/SKILL.md`

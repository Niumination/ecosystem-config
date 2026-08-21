# ERRATA — Audit v1 (2026-08-18, putaran pertama)

Audit pertama **salah diagnosis pada inti masalah**. Bagian observasi snapshot (MC down, cron drift, skill 47/213/2, RTK 68.6%) tetap sah. Rekomendasi arsitektur di bawah ini **ditarik**.

| Rekomendasi v1 | Mengapa salah untuk Niumination | Pengganti v2 |
|---|---|---|
| Fallback ke `9router` / `gratislonggar` / `cf-deepseek` / `juan-router` / `huancheng` | Itu **mesin cacat**. Model beda keluarga lanjut tugas yang sama → state, file, dan “ingatan” kacau. | Hanya `opencode-zen/big-pickle` ↔ `opencode-zen/deepseek-v4-flash-free`. Hop lain = **HALT + HANDOFF**. |
| 4 karakter + orchestrator sebagai runtime P0 | Model lemah tidak sanggup A2A. Menghidupkan 4 otak lemah = 4× entropi. | Karakter **dormant**. Satu persona, satu SOUL pendek. |
| Bind 5 thread Telegram ke 5 model 9router | Snapshot §6: thread sudah zoo (`gemini-3`, `gemini-2.5-pro`, `gemma-4`, `cf/deepseek`, `cf/zai`). Itu sumber rot. | Satukan semua thread ke keluarga Zen. |
| Mission Control + canary Vercel sebagai P0 | Website/app **bukan core**. | Core = hukum + state + ledger + pagar model. |
| `AGENTS.md` dipecah jadi 4 SOUL panjang | Model lemah tidak mengikuti 53.7 KB, juga tidak mengikuti 4 file. | Satu SOUL ≤ 60 baris + 12 hukum. |
| Auxiliary compression ke `gratislonggar` | Compression oleh model asing merusak memori jangka menengah. | Compression hanya di keluarga Zen, atau no-agent extract. |

Yang **tetap berlaku** dari v1: pin cron `c6ec80ed633f`, jangan matikan `model_drift_guard`, jangan Docker MC di 16 GB, jangan enable `telegram_router`, RTK tetap, vault tetap tertutup, NTFS `/Volumes/Niumination` adalah jebakan, Jcode optional.

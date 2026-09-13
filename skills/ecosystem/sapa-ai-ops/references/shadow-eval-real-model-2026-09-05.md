# Shadow Eval Model Sungguhan — OpenCode Go glm-5.3 (2026-09-05)

Konteks: PR3 sapa-ai (pipa AI + shadow). Mock membuktikan pipa (50/52 grounded); validasi model sungguhan wajib sebelum `AI_ENABLED` — dan hasilnya di sini menunjukkan validasi itu GAGAL tercapai, bukan lolos.

## Setup shadow (tanpa commit kunci)

- Env via file saat runtime, jangan pernah echo/commit: `AI_SHADOW=true AI_PROVIDER=opencode-go AI_BASE_URL=https://opencode.ai/zen/go/v1 AI_MODEL=<model> AI_API_KEY=<dari OPENCODE_GO_API_KEY>`; `AI_ENABLED` unset. `.env.local` tetap git-ignored.
- Endpoint/kunci: **Go** = `zen/go/v1` + `OPENCODE_GO_API_KEY` (langganan, cost 0 per panggilan); **Zen** = `zen/v1` + `AI_API_KEY` di `.env.local`. Keduanya OpenAI-compatible `/chat/completions`.
- Model chat-dialect terverifikasi (dok review 2026-09-04): `glm-5.x`, `deepseek-v4-flash`, `kimi-k2.6/2.7-code`, `mimo-v2.5`, `hy3`, `ox-alpha-free`. `NON_CHAT_MODELS` di `env.ts` menolak dialek Anthropic/Responses (`minimax-*`, `qwen3.*-max/plus`, `grok-*`, `gpt-5.6-luna`, `muse-spark*`) → jatuh deterministik dengan alasan jelas.
- Port milik sesi (di sini 3104 shadow / 3106 deterministik / 8787 mock): catat PID, matikan hanya milik sendiri, jangan sentuh proses user yang sudah berjalan.

## Tangga probe (sebelum eval 78-item, ±5 menit, tanpa biaya di paket langganan)

1. `GET /v1/models` + bearer → kunci + konektivitas OK (gratis).
2. 1 panggilan chat minimal → butuh `object: chat.completion`, HTTP 200 (cek dialek).
3. 1 panggilan `response_format: json_object` → cek disiplin JSON model.
4. Replikasi prompt composer ukuran penuh (system + ~12 evidence, `max_tokens: 800`).

## Temuan 2026-09-05: gerbang TAK BISA dinilai (bukan lolos)

- Served tetap 74/78, regresi 0 — sisi deterministik utuh. Tapi hanya **2/78** query sampai ke model → `pass 100%` dari N=2 **tak bermakna**. Jangan promosikan atas N kecil.
- Penyebab: gateway melempar **403 `error code: 1010`** pada traffic beruntun. Bukti biseksi: probe mungil berselang = 200; 5 request berurutan = semua 403; pulih sendiri setelah jeda. Bukan ban permanen, bukan model-spesifik (glm-5.3 dan deepseek-v4-flash sama). Pacing eval yang hanya sadar-SPLP (~2,5 dtk) tidak cukup untuk gateway LLM.
- Celah observabilitas (tugas untuk pengembang, di sini arena.ai): jalur `catch` + parse-fail di `answer-compose.ts` **tidak log apa pun** — tanpa baris `[ai-shadow]`, tanpa `console.error` — sehingga metrik `grounded fail` tetap 0 walau puluhan panggilan skip diam-diam. `dailyUsed` di `/api/status` naik tiap status dibaca (counter per-read, bukan per-call) — jangan dipakai sebagai penghitung panggilan model.
- Tindak lanjut: ulangi shadow dengan jeda sadar-gateway (~15 dtk/query ≈ 20 mnt) hingga N≈52; minta log error mentah + metrik `throttled/gagal` eksplisit + retry backoff untuk 403/429.

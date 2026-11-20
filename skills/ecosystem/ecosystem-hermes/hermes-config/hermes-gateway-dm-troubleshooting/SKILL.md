---
name: hermes-gateway-dm-troubleshooting
description: "Diagnose Hermes gateway errors and Telegram DM delays"
version: 1.0.0
author: Niumination
license: MIT
tags: [hermes, gateway, troubleshooting, telegram, dm, errors]
metadata:
  hermes:
    tags: [hermes, gateway, troubleshooting, telegram, dm, errors]
---

# Hermes Gateway & Telegram DM Troubleshooting

## When to Use
When Hermes DM responses are delayed, errors spike in logs, or upstream providers fail.

## Diagnostic Commands

```bash
# 1. Check if DM was flushed to Telegram
grep "Flushing text batch\|Telegram" ~/.hermes/logs/agent.log | tail -5

# 2. Top error types from errors.log
grep -oE "(model|provider|error_type|summary)=[^ ]+" ~/.hermes/logs/errors.log | sort | uniq -c | sort -rn | head -20

# 3. Shell hook failures (most common ~46%)
grep -c "shell hook failed" ~/.hermes/logs/errors.log
grep "shell hook failed" ~/.hermes/logs/errors.log | head -3

# 4. MCP connection failures (~15%)
grep -c "MCP server.*failed initial connection" ~/.hermes/logs/errors.log

# 5. Rate limiting
grep -c "RateLimitError" ~/.hermes/logs/errors.log

# 6. Upstream failures
grep -c "Upstream idle timeout\|EmptyStreamError\|Model is unavailable" ~/.hermes/logs/errors.log

# 7. Telegram network issues
grep -i "Telegram.*path\|Telegram.*IP\|dual-stack" ~/.hermes/logs/errors.log | tail -5

# 8. Stale auto-resume skip — inspect the stored session origin (read-only)
sqlite3 ~/.hermes/state.db "SELECT entry_json FROM gateway_routing WHERE session_key='agent:main:telegram:dm:<chat_id>';"
# If origin.user_id is null while resume_pending is true, the skip warning is a stale-origin artifact, not an allowlist problem.
```

## Common Causes & Fixes

| Cause | Signal | Fix |
|-------|--------|-----|
| Shell hook `command not found` | `ni(fence|model-guard).py): command not found` | Update hook path or set `hooks_auto_accept: true` |
| RateLimitError | `RateLimitError` + model | Switch to model with higher quota |
| Model unavailable | `Model is unavailable` | Use fallback model |
| Empty stream | `EmptyStreamError` | Retry or switch provider |
| MCP connection failed | `hermes-postgres/time/sqlite.*Connection closed` | Install/localize MCP servers |
| Telegram network | `Sticky Telegram path.*failed` | Check Telegram API endpoint routing |
| Replies "terputus"/hilang sebagian | `ConnectTimeout` berulang ke `api.telegram.org` / `149.154.166.110`, lalu `Failed to deliver response after N retries: send_path_degraded` | Masalah jaringan ke Telegram API (ISP/route), BUKAN model/Hermes. Gateway self-heal: cari `Telegram API transport recovered via …` lalu `polling recovered`. Jangan restart gateway — tunggu 1–2 menit. Detail di "Balasan Terputus = Jaringan Telegram" di bawah.
| Duplicate final send | `Normal final-send NOT suppressed despite active stream consumer` | Race condition: `_finalize_turn` and `_push_update` async in stream_consumer.py. Fix: `_final_response_sent` check + `has_delivered_text` fallback in run_turn.py suppression logic |
| Gateway crash-loop (`KeyError: 'platform'`) | `gateway.error.log` shows repeated `KeyError: 'platform'` in `HomeChannel.from_dict()`, `LastExitStatus: 256` | `home_channel` config missing required `platform` field. Fix: `hermes config set platforms.telegram.home_channel.platform telegram` then `hermes gateway restart` |
| Stale auto-resume skip | `Skipping auto-resume ... no longer authorized under the current allowlist` on every boot despite a correct allowlist | Stored `origin.user_id` is null so the check fails before any allowlist is read. Harmless: expires via freshness window, inbound auth unaffected. Never invent a config `allowed_users` key — auth reads `{PLATFORM}_ALLOWED_USERS` env. |

## Duplicate Final Send — Race Condition Pattern

**Symptom:** Gateway log shows `Normal final-send NOT suppressed despite active stream consumer for session ...: streamed=False previewed=False content_delivered=False transformed=False final_len=N — possible duplicate send`.

**Root cause:** Two async tasks inside `GatewayStreamConsumer`: `_finalize_turn` (sets `_final_response_sent`, `_final_content_delivered`) and `_push_update` (sets `tick.update_visible`, `_send_or_edit`). If `_finalize_turn` fires before `_push_update` completes its edit, `_final_content_delivered` stays `False`. When `delivered_final_matches()` returns `False` (payload mismatch from plugin hook appends or visible prefix divergence), `_stale_finalized=True` → `_content_delivered=False` → fall-through to warning.

**Fix layers:**
1. `stream_consumer.py` `_finalize_edit`: When `_use_native_streaming=True` and `_send_or_edit` returns False, set `_final_content_delivered=True` (content already streamed)
2. `run_turn.py` `_run_agent_mark_streamed_delivery`: Add `has_delivered_text(final)` fallback check for `_content_delivered`
3. `run_turn.py` `_run_agent_deliver_final_send`: When `_stale_finalized=True` AND `_sc._final_response_sent=True`, suppress normal final send (content already reached user)

**Verification:** After fix, `hermes config check` shows clean; gateway.log no longer shows the warning on subsequent turns.

## Gateway Crash-Loop — `KeyError: 'platform'`

**Symptom:** Gateway log shows repeated `KeyError: 'platform'` in `gateway/config.py:309` (`HomeChannel.from_dict()`), launchd reports `LastExitStatus: 256`, gateway restarts every few seconds in a crash-loop.

**Root cause:** `HomeChannel.from_dict(data)` at `gateway/config.py:309` accesses `data["platform"]` without a fallback. When `home_channel` is set without a `platform` key (e.g., `{chat_id: 123, type: private}`), it raises `KeyError`.

**Fix:**
```bash
hermes config set platforms.telegram.home_channel.platform telegram
hermes gateway restart
```

**Verification:** `hermes gateway status` shows supervised PID, `gateway.error.log` has no new `KeyError` after restart, gateway.log shows `✓ telegram connected`.

## Stale Auto-Resume Skip — Null user_id in Stored Origin

**Symptom:** Every gateway start logs `Skipping auto-resume for <session_key>: session owner is no longer authorized under the current allowlist`, even though the ID is in `TELEGRAM_ALLOWED_USERS`.

**Root cause:** `_resume_owner_authorized` validates the *stored* session origin (`gateway_routing.entry_json`), and `_is_user_authorized` returns False immediately when `source.user_id` is empty — before any allowlist is consulted. Older sessions stored DM origins with `user_id: null` (only `chat_id`), so the check can never pass for them.

**Rules:**
- Gateway authorization reads `{PLATFORM}_ALLOWED_USERS` from env, never a `platforms.<name>.allowed_users` config key. Verify every config key against the loader that reads it (`gateway/authz_mixin.py`) before setting it — an unread key only misleads the next diagnosis.
- A null-`user_id` origin fails closed by design and the skip is harmless: live inbound messages carry a real `user_id` and authorize normally. Prefer letting the marker expire via the freshness window; direct `state.db` edits race the running gateway, so back it up first and touch only the `resume_pending` flag, never fabricate an origin.
- Judge by fresh tail after restart: one skip line per boot for a stale marker is expected; new skips naming live sessions are not.

## Balasan Terputus = Jaringan Telegram (bukan model)

**Symptom:** user mengeluh balasan di Telegram "selalu terputus" atau tidak lengkap, padahal sesi agent berjalan normal dan log agen tidak error.

**Diagnosis — baca `~/.hermes/logs/gateway.error.log`, bukan log agen:**
```bash
grep -c "ConnectTimeout\|send_path_degraded\|Failed to deliver" ~/.hermes/logs/gateway.error.log
grep -E "ConnectTimeout|send_path_degraded|Failed to deliver|Connected to Telegram" ~/.hermes/logs/gateway.error.log | tail
```
Pola khas: `ConnectTimeout('')` ke `api.telegram.org` (dual-stack) DAN ke IP `149.154.166.110`, diselingi
`MarkdownV2 edit failed, falling back to plain text: Timed out`, lalu `Failed to deliver response after
2 retries: send_path_degraded`. Itu penyebab balasan terpotong/hilang.

**Aturan:**
- Ini **bukan** masalah model, prompt, atau skill — jangan debug sisi agen dulu.
- Gateway **memulihkan diri**: ia belajar sticky IPv4 path (`Using sticky IPv4 Telegram API path
  149.154.166.110`) dan restart polling (`polling recovered`). Tunggu 1–2 menit; jangan restart
  gateway (aturan besi: jangan sentuh gateway saat hidup).
- **Rute:** `route -n get 149.154.166.110` menunjukan gateway lokal (`en0`), BUKAN Tailscale — jadi
  sumbernya koneksi ISP ke Telegram, bukan config VPN/tailnet.
- **Verifikasi pulih:** `curl -s -o /dev/null -w "%{http_code}" --max-time 15 https://api.telegram.org/`
  balas 302 = saat ini sehat; tapi fluktuatif, jadi gunakan log sebagai bukti utama.
- Kalau timeout persisten dan terputus berkepanjangan, teruskan ke pemilik (bukan gejala yang bisa
  diperbaiki agent dari sisi config).

## Session Paused: `unknown_execution` — Resolve Blocked FIFO

**Symptom:** Gateway log shows `WARNING gateway.session_authority: Session <id> paused: unknown_execution`. All subsequent messages in that thread queue but never execute (FIFO stuck). `session_admissions` has one row with `status='unknown'`.

**Mechanism:** A turn was claimed by an owner epoch that restarted before the turn completed. The gateway fences it `unknown` and pauses the FIFO — only the person who sent it can decide whether to resend. Automated admissions (cron, automation) are auto-settled on boot; a user-submitted turn pauses until manually resolved.

**Diagnosis:**
```bash
# 1. Identify the unknown row
sqlite3 ~/.hermes/state.db "
SELECT seq, admission_id, principal_id, intent, status, owner_epoch, generation,
       substr(payload_json,1,200)
FROM session_admissions
WHERE target_session_id='<session_id>' AND status='unknown';"

# 2. Count by status to see full FIFO shape
sqlite3 ~/.hermes/state.db "
SELECT status, count(*)
FROM session_admissions
WHERE target_session_id='<session_id>'
GROUP BY status;"

# 3. Confirm is it a user turn (principal_id starts with 'messaging:')
# If principal starts with 'automation:' or is CRON_PRINCIPAL_ID → auto-settle on next restart
# If principal starts with 'messaging:' → requires manual resolution
```

**Resolution — user turn (messaging: principal):**
```bash
# Step 1: backup state.db first (non-negotiable)
hermes backup --quick --label "session-fix-$(date +%H%M)"

# Step 2: mark unknown row as terminal
sqlite3 ~/.hermes/state.db \
  "UPDATE session_admissions SET status='terminal', outcome='discarded_user_resumed' \
   WHERE target_session_id='<session_id>' AND status='unknown';"

# Step 3: verify — should return 0 rows
sqlite3 ~/.hermes/state.db \
  "SELECT seq, status, outcome FROM session_admissions \
   WHERE target_session_id='<session_id>' AND status='unknown';"
```

After the UPDATE the gateway's drain loop resumes on next inbound message — the queued rows behind it (`status='queued'`) run normally. No gateway restart needed.

**Pitfall — do not edit state.db while gateway is under heavy load.** The SQLite WAL is live; always take `hermes backup --quick` before any UPDATE. The backup takes ~5 seconds for state.db of ~460 MB.

**Pitfall — a cron turn hard-coded to a dead model causes the next drain to fail even after FIFO is unblocked.** After resolving `unknown_execution`, watch gateway.log for `RuntimeError: HTTP 404: Model '...' not found` — this means a job or cron references a model that no longer exists in the router catalog. Fix: update the cron job's model to an active one (verify with `curl -s -X POST http://localhost:20128/v1/chat/completions -H "Authorization: Bearer $NINE_ROUTER_API_KEY" -d '{"model":"<model>","messages":[...],"max_tokens":5}'`).

## User Preference
Afrizal Munthe expects DM responses within minutes. Delays indicate upstream provider issues or hook/MCP failures.
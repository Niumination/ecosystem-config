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

## User Preference
Afrizal Munthe expects DM responses within minutes. Delays indicate upstream provider issues or hook/MCP failures.
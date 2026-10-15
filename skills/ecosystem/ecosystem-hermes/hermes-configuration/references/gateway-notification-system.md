# Gateway Notification System

## How Startup Notifications Work

### Two notification paths at gateway boot:

1. **Planned restart notification** (`/restart` command):
   - Triggered when `~/.hermes/.restart_pending.json` exists
   - `_send_restart_notification()` sends "♻ Gateway restarted successfully" to the chat that initiated `/restart`
   - Then `_send_home_channel_startup_notifications()` sends "♻️ Gateway online — Hermes is back and ready." to all configured home channels
   - Marker cleared via `_clear_planned_restart_notification()`

2. **Unplanned restart** (Mac sleep/wake, crash, kill):
   - `planned_restart_notification_pending()` checks `~/.hermes/.restart_pending.json` → returns False
   - `_send_home_channel_startup_notifications()` is **NOT called**
   - No startup notification is sent

### `_home_channel_transports()` filter

In `gateway/run_notifications.py`, `_home_channel_transports()` yields `(platform, platform_cfg, home, transport)` only when:
- `platform_cfg.home_channel` is not None
- `home.chat_id` is not empty
- A live transport exists for the platform

**If `home_channel` is missing from config.yaml, the platform is silently skipped.**

## `home_channel` Configuration

### Why it's NOT in DEFAULT_CONFIG

`home_channel` is a `PlatformConfig` field in `gateway/config.py` — a runtime-configured field, not a system default. It is only set via:
- `/set home <platform> <chat_id>` slash command
- `persist_home_channel()` function
- Manual `config.yaml` edit

It is NOT migrated by `_config_version` steps (e.g., v40→41 in `config_migrations.py`). The migration steps only clean specific schema fields. `home_channel` is never auto-populated.

### Setting home_channel

```bash
hermes config set platforms.telegram.home_channel.chat_id <your_chat_id>
```

Or in `~/.hermes/config.yaml`:
```yaml
platforms:
  telegram:
    home_channel:
      chat_id: <your_chat_id>
```

### `PlatformConfig` defaults

```python
class PlatformConfig:
    enabled: bool = False
    gateway_restart_notification: bool = True  # "♻️ Gateway online/restarted" pings
    home_channel: Optional[HomeChannel] = None
```

`gateway_restart_notification` defaults to `True` — but `home_channel` defaults to `None`.

## Duplicate-Send Prevention

### The race condition (v0.21.1 fix)

When the gateway has an active stream consumer but suppression did not fire, the normal final send may duplicate. The fix adds three layers:

1. **`_finalize_edit`** (stream_consumer.py): When `_use_native_streaming=True` and `_send_or_edit` fails, `_final_content_delivered=True`
2. **`_run_agent_mark_streamed_delivery`** (run_turn.py): `has_delivered_text(final)` fallback for `_content_delivered`
3. **`_run_agent_deliver_final_send`** (run_turn.py): When `_stale_finalized=True` AND `_sc._final_response_sent=True`, set `response["already_sent"]=True` to suppress

### Verification

After a Telegram message, check gateway.log:
- Should see `Suppressing normal final send for session ...` (info, not warning)
- Should NOT see `Normal final-send NOT suppressed despite active stream consumer`

## Telegram Adapter Specifics

- `SUPPORTS_NATIVE_STREAMING`: **Absent** (Telegram does not support native streaming)
- `REQUIRES_EDIT_FINALIZE: bool = True` — Telegram needs explicit finalize edit
- Uses `_finalize_edit_path()` (edit-based), NOT native streaming
- The `_finalize_turn` native streaming branch is skipped for Telegram

## `_send_home_channel_startup_notifications()` Flow

```python
message = "♻️ Gateway online — Hermes is back and ready."
for platform, platform_cfg, home, transport in self._home_channel_transports():
    if not platform_cfg.gateway_restart_notification:
        continue  # suppressed by config
    if await self._send_home_channel_message(platform, home, transport, message):
        delivered.add(target)
```

Skipped if `gateway_restart_notification=False` for that platform.

## Stale Finalize Reconciliation

When `delivered_final_matches()` returns `False` (payload mismatch):
- `_stale_finalized=True`
- If `_sc.message_id` exists and adapter is available → edit the streamed message
- If `_sc._final_response_sent=True` → suppress normal send (content already delivered)
- Otherwise → deliver via normal final send (content may not have reached user)

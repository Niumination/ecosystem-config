---
name: telegram-forum-operations
description: Create, rename, manage Telegram forum threads via Bot API.
---

# Telegram Forum Operations

## Overview

Telegram forum threads can be created, renamed, and managed via the Bot API. This skill covers the workflow for Niumination's Telegram group `Niu-MissionControl` (`-1004204696417`).

## Prerequisites

- Bot token in `~/.hermes/.env` as `TELEGRAM_BOT_TOKEN`
- Group must be a forum (`is_forum: true`)
- Bot must be admin in the group with `can_manage_topics` permission

## Workflow

### 1. Create Forum Topic

Use `scripts/create-cron-thread.py` or direct Bot API call:

```python
POST https://api.telegram.org/bot<token>/createForumTopic
{
  "chat_id": "-1004204696417",
  "name": "Thread Name"
}
```

Returns `message_thread_id` — this is the thread ID used in `channel_overrides`.

### 2. Rename Forum Topic + Set Icon

Use `scripts/rename-telegram-threads.py` or direct Bot API call:

```python
POST https://api.telegram.org/bot<token>/editForumTopic
{
  "chat_id": "-1004204696417",
  "message_thread_id": 802,
  "name": "New Name"
}

POST https://api.telegram.org/bot<token>/setForumTopicIcon
{
  "chat_id": "-1004204696417",
  "message_thread_id": 802,
  "custom_emoji_id": "..."
}
```

### 3. Configure Thread in Hermes

Use `hermes config set` CLI (direct config file editing is blocked by config guard):

```bash
hermes config set platforms.telegram.channel_overrides.'<thread_id>' '{"model": "...", "provider": "..."}'
hermes config set platforms.telegram.extra.channel_prompts.'<thread_id>' '...'
```

### 4. Route Cron Jobs to Thread

```bash
hermes cron edit <job_id> --deliver "telegram:-1004204696417:<thread_id>"
```

## Pitfalls

- **DM threads cannot be renamed** — only forum topics support `editForumTopic`. Thread ID `1` is the DM main thread and will return HTTP 400.
- **Token must never be printed** — always read from `~/.hermes/.env` and use in API calls without logging.
- **Config guard blocks direct edits** — use `hermes config set` CLI instead of patching `~/.hermes/config.yaml` directly.
- **Custom emoji icons require `can_manage_topics` permission** — bot must be admin with this permission.
- **Thread ID vs Chat ID** — `message_thread_id` from `createForumTopic` is the thread ID, not the chat ID. Chat ID is always `-1004204696417` for Niu-MissionControl.

## Scripts

- `scripts/create-cron-thread.py` — Create forum topic via Bot API
- `scripts/rename-telegram-threads.py` — Rename forum topics and set custom emoji icons

#!/usr/bin/env python3
"""Rename Telegram forum topics and set custom emoji icons.
Reads bot token from ~/.hermes/.env (never prints it).
Usage: python3 scripts/rename-telegram-threads.py
"""
import json
import sys
import urllib.request
from pathlib import Path

CHAT_ID = "-1004204696417"

# (thread_id, new_name, emoji_description)
# 8853 (ASN) is intentionally excluded — owner said do not touch.
THREADS = [
    (1, "General", "command center"),
    (802, "Research", "research"),
    (803, "Builder", "builder"),
    (804, "QA", "QA"),
    (1172, "Kreator", "creator"),
    (7402, "Serbaguna", "flex"),
    (12595, "Cron & Otomasi", "cron"),
]


def load_token() -> str:
    env_path = Path.home() / ".hermes" / ".env"
    if not env_path.is_file():
        print("[error] ~/.hermes/.env not found")
        sys.exit(1)
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("[error] TELEGRAM_BOT_TOKEN not found in ~/.hermes/.env")
    sys.exit(1)


def api_call(token: str, method: str, data: dict) -> dict | None:
    url = f"https://api.telegram.org/bot{token}/{method}"
    req = urllib.request.Request(
        url, data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                return result["result"]
            print(f"[error] {method}: {result.get('description', 'unknown')}")
            return None
    except Exception as e:
        print(f"[error] {method}: {e}")
        return None


def get_forum_topic_icon_stickers(token: str) -> list[str]:
    """Get custom emoji IDs usable as forum topic icons."""
    result = api_call(token, "getForumTopicIconStickers", {})
    if not result:
        return []
    return [s["custom_emoji_id"] for s in result if "custom_emoji_id" in s]


def rename_topic(
    token: str, chat_id: str, thread_id: int, name: str,
    icon_id: str | None = None,
) -> bool:
    data: dict = {"chat_id": chat_id, "message_thread_id": thread_id, "name": name}
    if icon_id:
        data["icon_custom_emoji_id"] = icon_id
    return api_call(token, "editForumTopic", data) is not None


def main() -> None:
    token = load_token()

    emojis = get_forum_topic_icon_stickers(token)
    if emojis:
        print(f"[ok] {len(emojis)} custom emoji icons available")
    else:
        print("[warn] No custom emoji stickers available — rename only")

    for thread_id, name, emoji_desc in THREADS:
        icon_id = None
        if emojis:
            # Assign emoji by index (deterministic order)
            idx = [t[0] for t in THREADS].index(thread_id)
            if idx < len(emojis):
                icon_id = emojis[idx]

        if rename_topic(token, CHAT_ID, thread_id, name, icon_id):
            icon_str = f" + icon" if icon_id else ""
            print(f"[ok] {thread_id} → '{name}'{icon_str}")
        else:
            print(f"[error] {thread_id} failed")


if __name__ == "__main__":
    main()

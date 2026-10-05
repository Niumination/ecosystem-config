#!/usr/bin/env python3
"""Create a new Telegram forum topic for cron output.
Reads bot token from ~/.hermes/.env (never prints it).
Usage: python3 scripts/create-cron-thread.py "Thread Name"
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

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

def create_forum_topic(token: str, chat_id: str, name: str) -> int:
    url = f"https://api.telegram.org/bot{token}/createForumTopic"
    data = json.dumps({"chat_id": chat_id, "name": name}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                return result["result"]["message_thread_id"]
            else:
                print(f"[error] Telegram API: {result.get('description', 'unknown error')}")
                sys.exit(1)
    except Exception as e:
        print(f"[error] {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/create-cron-thread.py \"Thread Name\"")
        sys.exit(1)
    thread_name = sys.argv[1]
    chat_id = "-1004204696417"  # Niu-MissionControl group
    token = load_token()
    thread_id = create_forum_topic(token, chat_id, thread_name)
    print(f"[ok] Thread created: {thread_name}")
    print(f"     Thread ID: {thread_id}")
    print(f"     Chat ID: {chat_id}")

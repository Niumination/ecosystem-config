#!/usr/bin/env python3
"""Dispatch message to a Telegram thread via Bot API.
Reads bot token from ~/.hermes/.env (never prints it).
Usage: python3 scripts/dispatch-to-thread.py <thread_id> <message>
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

def load_token():
    env_path = Path.home() / '.hermes' / '.env'
    for line in env_path.read_text().splitlines():
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            return line.split('=', 1)[1].strip()
    raise RuntimeError('TELEGRAM_BOT_TOKEN not found in ~/.hermes/.env')

def main():
    if len(sys.argv) < 3:
        print('Usage: python3 scripts/dispatch-to-thread.py <thread_id> <message>')
        sys.exit(1)

    thread_id = sys.argv[1]
    message = ' '.join(sys.argv[2:])
    token = load_token()
    chat_id = '-1004204696417'

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = json.dumps({
        'chat_id': chat_id,
        'message_thread_id': thread_id,
        'text': message
    }).encode()

    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            msg_id = result.get('result', {}).get('message_id', '?')
            print(f'[ok] Dispatched to thread {thread_id}, message_id={msg_id}')
    except urllib.error.HTTPError as e:
        print(f'[error] HTTP {e.code}: {e.read().decode()}')
        sys.exit(1)

if __name__ == '__main__':
    main()

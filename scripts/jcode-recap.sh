#!/bin/bash
# jcode-recap.sh — Kirim rekap sesi jcode terakhir ke Telegram
# Usage: ./jcode-recap.sh [exit_code]

TELEGRAM_BOT="5919512090:AAE1LsO047YEiR-HHPNL6MColG4wBHUZ2do"
TELEGRAM_CHAT="2077300493"
JCODE_HOME="${JCODE_HOME:-$HOME/.jcode}"

# Skip jika tidak ada session atau tidak ada interaksi berarti
LATEST_SESSION=$(ls -t "$JCODE_HOME/sessions"/*.json 2>/dev/null | head -1)
[ -z "$LATEST_SESSION" ] && exit 0

export JCODE_SESSION_FILE="$LATEST_SESSION"
export JCODE_EXIT_CODE="${1:-0}"

# Semua logika di Python (threshold + kirim). Output dibuang (> /dev/null).
python3 << 'PYEOF' > /dev/null 2>&1
import json, os, urllib.request, urllib.parse
from datetime import datetime

sess_file = os.environ['JCODE_SESSION_FILE']
journal_file = sess_file.replace('.json', '.journal.jsonl')
exit_code = int(os.environ.get('JCODE_EXIT_CODE', '0'))

# Baca session snapshot
with open(sess_file) as f:
    snap = json.load(f)

created = snap.get('created_at', '?')
updated = snap.get('updated_at', '?')
workdir = snap.get('working_dir', '?')
name = snap.get('short_name', '?')
model = snap.get('model', '?')
status = snap.get('status', '?')
provider = snap.get('provider_key', '?')

# Kumpulkan semua messages (snapshot + journal)
all_msgs = list(snap.get('messages', []))
if os.path.exists(journal_file):
    with open(journal_file) as f:
        for line in f:
            try:
                entry = json.loads(line)
                if 'append_messages' in entry:
                    all_msgs.extend(entry['append_messages'])
                if 'meta' in entry:
                    meta = entry['meta']
                    if meta.get('updated_at'): updated = meta['updated_at']
                    if meta.get('status'): status = meta['status']
                    if meta.get('model'): model = meta['model']
            except:
                pass

user_msgs = sum(1 for m in all_msgs if m.get('role') == 'user')
asst_msgs = sum(1 for m in all_msgs if m.get('role') == 'assistant')
tool_msgs = sum(1 for m in all_msgs if m.get('role') == 'tool')

# Minimum threshold: skip jika kurang dari 2 prompt user (tidak ada interaksi berarti)
if user_msgs < 2:
    os._exit(0)

# Ambil prompt user terakhir (skip system reminders)
last_prompt = ''
for m in reversed(all_msgs):
    if m.get('role') == 'user':
        c = m.get('content', '')
        if isinstance(c, list):
            for item in c:
                if item.get('type') == 'text':
                    txt = item.get('text', '')
                    if '<system-reminder>' not in txt:
                        last_prompt = txt.strip()[:250]
                        break
        elif isinstance(c, str) and '<system-reminder>' not in c:
            last_prompt = c.strip()[:250]
        if last_prompt:
            break

last_response = ''
for m in reversed(all_msgs):
    if m.get('role') == 'assistant':
        c = m.get('content', '')
        if isinstance(c, list):
            texts = [item.get('text','').strip() for item in c if item.get('type') == 'text' and item.get('text','').strip()]
            if texts:
                last_response = texts[0][:350]
        elif isinstance(c, str) and c.strip():
            last_response = c.strip()[:350]
        if last_response:
            break

# Durasi
duration_str = '?'
try:
    if created != '?' and updated != '?':
        def parse_ts(ts):
            ts = ts.replace('Z', '+00:00')
            if '+' not in ts and ts.count('-') == 2:
                ts += '+00:00'
            return datetime.fromisoformat(ts)
        c = parse_ts(created)
        u = parse_ts(updated)
        diff = u - c
        total_min = int(diff.total_seconds() / 60)
        if total_min < 1:
            duration_str = f'{int(diff.total_seconds())} detik'
        elif total_min < 60:
            duration_str = f'{total_min} menit'
        else:
            h = total_min // 60
            m = total_min % 60
            duration_str = f'{h}j {m}m' if m else f'{h} jam'
except:
    pass

# Nama project
project = workdir
home = os.path.expanduser('~')
if '/Niumination/' in workdir:
    project = workdir.split('/Niumination/')[1]
elif workdir == home:
    project = '~ (home)'
elif workdir.startswith('/Users/'):
    uname = workdir.split('/')[2]
    project = '~' + workdir[len('/Users/' + uname):]

# Ikon
status_icons = {'active': '\U0001f7e1', 'completed': '\u2705', 'done': '\u2705',
                'crashed': '\U0001f4a5', 'error': '\U0001f4a5', 'failed': '\U0001f4a5',
                'stopped': '\u23f9\ufe0f'}
status_icon = '\u25fb\ufe0f'
for k, v in status_icons.items():
    if k in status.lower():
        status_icon = v
        break

if exit_code == 0:
    exit_icon = '\u2705 Exit normal'
elif exit_code in (130, 143):
    exit_icon = '\u23f9\ufe0f Dihentikan (Ctrl+C)'
else:
    exit_icon = f'\u26a0\ufe0f Exit kode {exit_code}'

ts = created[:19].replace('T', ' ') if created != '?' else '?'

def esc(s):
    if not s or s == '?': return '-'
    s = str(s)
    for ch in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
        s = s.replace(ch, '\\' + ch)
    return s

lines = [
    '\U0001f4ca *Jcode Selesai*',
    '',
    f'\u2514 {exit_icon}',
    f'\u2514 \U0001f41a Sesi: `{esc(name)}`',
    f'\u2514 \U0001f4c1 Project: `{esc(project)}`',
    f'\u2514 \u23f1 Durasi: `{esc(duration_str)}`',
    f'\u2514 \U0001f916 Model: `{esc(model)}` ({esc(provider)})',
    f'\u2514 \U0001f4ac `{total_msgs}` pesan ({user_msgs} user \u00b7 {asst_msgs} asst \u00b7 {tool_msgs} tool)',
    f'\U0001f550 Mulai: `{esc(ts)}`',
    f'{status_icon} Status: `{esc(status)}`',
    '',
    '\U0001f4dd *Prompt Terakhir:*',
    esc(last_prompt) if last_prompt else '-',
    '',
    '\U0001f4a1 *Response:*',
    esc(last_response) if last_response else '-',
]
message = '\n'.join(lines)

# Kirim via Telegram API (dengan retry & graceful handling)
bot_token = os.environ.get('JCODE_BOT_TOKEN', '5919512090:AAE1LsO047YEiR-HHPNL6MColG4wBHUZ2do')
chat_id = os.environ.get('JCODE_CHAT_ID', '2077300493')
url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
data = urllib.parse.urlencode({
    'chat_id': chat_id,
    'parse_mode': 'Markdown',
    'disable_web_page_preview': 'true',
    'text': message,
}).encode()

for attempt in range(2):
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get('ok'):
                break  # sukses
    except urllib.error.HTTPError as e:
        if e.code == 429:
            import time
            time.sleep(2 ** attempt)  # exponential backoff
            continue
        # error lain: skip saja (jangan ganggu user)
        break
    except:
        break
PYEOF

#!/usr/bin/env python3
"""Fast provider sweep - no full stress-test, just 2-burst per model."""
import json, os, time, urllib.error, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_env(path):
    d = {}
    if not path.exists(): return d
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        d[k.strip()] = v.strip().strip('"').strip("'")
    return d

ENV = Path.home() / '.hermes' / '.env'
env = load_env(ENV)
for k, v in env.items(): os.environ.setdefault(k, v)

KEYS = {
    '9router':       ('NINE_ROUTER_API_KEY',  'http://localhost:20128/v1'),
    'openrouter':    ('OPENROUTER_API_KEY',   'https://openrouter.ai/api/v1'),
    'huancheng':     ('HUANCHENG_API_KEY',    'https://api.hcnsec.cn/v1'),
    'opencode-zen':  ('OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1'),
    'agentrouter':   ('AGENTROUTER_API_KEY',  'https://agentrouter.org/v1'),
}
UA = 'hermes-agent/0.19.0'

def probe_models(provider, key, base):
    try:
        req = urllib.request.Request(base + '/models', headers={'Authorization': f'Bearer {key}', 'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            ids = [m['id'] for m in data.get('data', [])]
            return {'p': provider, 'models': ids, 'n': len(ids), 'err': None}
    except Exception as e:
        return {'p': provider, 'models': [], 'n': 0, 'err': str(e)[:80]}

def chat_once(base, key, model, prompt='Halo'):
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 10, 'stream': False}).encode()
    req = urllib.request.Request(base + '/chat/completions', data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('User-Agent', UA)
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            raw = r.read().decode()
            if 'data:' in raw:
                parts = []
                for ln in raw.splitlines():
                    ln = ln.strip()
                    if ln.startswith('data:'):
                        try:
                            obj = json.loads(ln[5:].strip())
                            delta = obj.get('choices', [{}])[0].get('delta', {})
                            c = delta.get('content', '')
                            if c: parts.append(c)
                        except: pass
                return 'OK', ''.join(parts) if parts else '(empty SSE)'
            data = json.loads(raw)
            return 'OK', data.get('choices', [{}])[0].get('message', {}).get('content', '')[:60]
    except urllib.error.HTTPError as e:
        return 'ERR', f'HTTP {e.code}'
    except Exception as e:
        return 'ERR', f'{type(e).__name__}'

print('=== PROVIDER SWEEP (fast, 2 bursts/model) ===\n')

# Phase 1: list models
print('[Phase 1] Provider model count...')
provider_status = {}
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(probe_models, p, env.get(k), b): p for p, (k, b) in KEYS.items()}
    for f in as_completed(futures):
        r = f.result()
        provider_status[r['p']] = r
        status = f"✅ {r['n']} models" if not r['err'] else f"❌ {r['err']}"
        print(f'  {r["p"]:15s} {status}')

# Phase 2: candidate selection — hand-pick best-looking free candidates
# 9router: focus on flash/fast variants and kimi
cands = set()
for m in provider_status['9router']['models']:
    # Fast flash variants, coding models
    if any(x in m for x in ['gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-3.5-flash', 'gpt-4o-mini', 'gpt-5-mini', 'gpt-5.4-mini', 'claude-haiku', 'kimi-k3', 'kimi-for-coding', 'gemma-4-31b', 'minimax-m3', 'qwen3.5', 'glm-4.7', 'glm-5.2']):
        cands.add(('9router', m))

for m in provider_status['openrouter']['models']:
    if ':free' in m:
        cands.add(('openrouter', m))

for m in provider_status['opencode-zen']['models']:
    if any(x in m.lower() for x in ['free', 'hy3', 'nemotron', 'laguna']):
        cands.add(('opencode-zen', m))

for m in provider_status['huancheng']['models']:
    cands.add(('huancheng', m))

candidates = sorted(cands)
print(f'\n[Phase 2] Testing {len(candidates)} candidates (2 bursts each)...')

results = []
for provider, model in candidates:
    key = env.get(KEYS[provider][0], '')
    base = KEYS[provider][1]
    if not key:
        results.append((provider, model, 0, 'NO_KEY'))
        continue
    ok_count = 0
    for _ in range(2):
        status, resp = chat_once(base, key, model)
        if status == 'OK': ok_count += 1
        time.sleep(0.2)
    results.append((provider, model, ok_count, None))
    flag = '✅' if ok_count == 2 else '⚠️' if ok_count == 1 else '❌'
    print(f'  {flag} {ok_count}/2  {provider:15s} {model}')

# Rank
print('\n=== RANKING ===')
print('\n✅ WORKING (2/2):')
for p, m, ok, e in results:
    if ok == 2:
        print(f'  {p:15s}  {m}')

print('\n⚠️ PARTIAL (1/2):')
for p, m, ok, e in results:
    if ok == 1:
        print(f'  {p:15s}  {m}')

print('\n❌ FAILED (0/2):')
for p, m, ok, e in results:
    if ok == 0:
        print(f'  {p:15s}  {m}')

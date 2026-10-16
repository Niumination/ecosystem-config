#!/usr/bin/env python3
"""Fresh live test - ALL recommended models, 8 burst each."""
import json, os, time, urllib.error, urllib.request
from pathlib import Path

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
UA = 'hermes-agent/0.19.0'

def chat_once(base, key, model):
    body = json.dumps({'model': model, 'messages': [{'role': 'user', 'content': 'OK'}], 'max_tokens': 5, 'stream': False}).encode()
    req = urllib.request.Request(base+'/chat/completions', data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('User-Agent', UA)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=8) as r:
            raw = r.read().decode()
            if 'data:' in raw:
                parts = []
                for ln in raw.splitlines():
                    if ln.strip().startswith('data:'):
                        try:
                            c = json.loads(ln[5:].strip()).get('choices',[{}])[0].get('delta',{}).get('content','')
                            if c: parts.append(c)
                        except: pass
                return ('OK', int((time.time()-t0)*1000))
            data = json.loads(raw)
            return ('OK', int((time.time()-t0)*1000))
    except urllib.error.HTTPError as e:
        return ('ERR', e.code)
    except Exception:
        return ('ERR', 0)

# RECOMMENDED MODELS FROM SCAN
tests = [
    ('opencode-zen',  'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1', 'big-pickle'),
    ('9router',       'NINE_ROUTER_API_KEY',  'http://localhost:20128/v1',    'ag/gemini-3.5-flash-extra-low'),
    ('9router',       'NINE_ROUTER_API_KEY',  'http://localhost:20128/v1',    'ag/gemini-3-flash-agent'),
    ('opencode-zen',  'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1',   'laguna-s-2.1-free'),
    ('9router',       'NINE_ROUTER_API_KEY',  'http://localhost:20128/v1',    'ag/gemini-3.7-flash-low'),
    ('9router',       'NINE_ROUTER_API_KEY',  'http://localhost:20128/v1',    'gemini/gemma-4-31b-it'),
    # Fallback chain
    ('opencode-zen',  'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1',   'hy3-free'),
]

BURSTS = 8
print(f"=== LIVE TEST — {len(tests)} models × {BURSTS} bursts ===\n")

results = []
for prov, kenv, base, model in tests:
    key = env.get(kenv, '')
    if not key:
        print(f"❌ SKIP {model} (no key)"); continue
    ok = 0
    latencies = []
    for i in range(BURSTS):
        s, ms = chat_once(base, key, model)
        if s == 'OK':
            ok += 1
            latencies.append(ms)
        time.sleep(0.15)
    avg = int(sum(latencies)/len(latencies)) if latencies else 0
    results.append((prov, model, ok, avg))
    flag = '✅' if ok == BURSTS else '⚠️' if ok >= 6 else '❌'
    print(f"{flag} {ok}/{BURSTS}  avg={avg}ms  {prov:15s} {model}")

print("\n=== FINAL VERDICT ===")
for prov, model, ok, avg in results:
    flag = '✅ PASS' if ok == BURSTS else '⚠️ PARTIAL' if ok >= 6 else '❌ FAIL'
    print(f"  {flag}  {model} (@{prov}) — {ok}/{BURSTS} bursts, avg {avg}ms")

# Save
Path.home().joinpath('.hermes/live-test-results.json').write_text(json.dumps(results, indent=2))
print(f"\nSaved to ~/.hermes/live-test-results.json")

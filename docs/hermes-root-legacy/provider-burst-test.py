#!/usr/bin/env python3
"""Stress-test 8 bursts per top candidate, per provider."""
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

def chat_once(base, key, model, prompt='Halo'):
    body = json.dumps({
        'model': model, 'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 10, 'stream': False
    }).encode()
    req = urllib.request.Request(base+'/chat/completions', data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {key}')
    req.add_header('User-Agent', UA)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read().decode()
            if 'data:' in raw:
                parts = []
                for ln in raw.splitlines():
                    ln = ln.strip()
                    if ln.startswith('data:'):
                        try:
                            obj = json.loads(ln[5:].strip())
                            c = obj.get('choices',[{}])[0].get('delta',{}).get('content','')
                            if c: parts.append(c)
                        except: pass
                return ('OK', int((time.time()-t0)*1000), ''.join(parts) if parts else '(empty SSE)')
            data = json.loads(raw)
            return ('OK', int((time.time()-t0)*1000), data.get('choices',[{}])[0].get('message',{}).get('content','')[:50])
    except urllib.error.HTTPError as e:
        return ('ERR', e.code, e.reason)
    except Exception as e:
        return ('ERR', 0, f'{type(e).__name__}')

# Top candidates from sweep
top_candidates = [
    ('9router',       'NINE_ROUTER_API_KEY',  'http://localhost:20128/v1',
     ['ag/gemini-3.5-flash-extra-low', 'ag/gemini-3-flash-agent',
      'ag/gemini-3.5-flash-low', 'ag/gemini-3.7-flash-low',
      'gh/gpt-4o-mini', 'ollama/minimax-m3',
      'ag/gemini-3.7-flash-medium', 'gemini/gemma-4-31b-it']),
    ('openrouter',    'OPENROUTER_API_KEY',   'https://openrouter.ai/api/v1',
     ['nvidia/nemotron-3-super-120b-a12b:free',
      'google/gemma-4-26b-a4b-it:free',
      'nvidia/nemotron-3-ultra-550b-a55b:free']),
    ('opencode-zen',  'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1',
     ['big-pickle', 'hy3-free', 'laguna-s-2.1-free']),
]

BURSTS = 8

print(f"=== BURST STRESS TEST ({BURSTS} bursts each) ===\n")

all_results = {}
for pname, kenv, base, models in top_candidates:
    key = env.get(kenv, '')
    if not key:
        print(f"[{pname}] NO KEY\n"); continue
    print(f"--- {pname} ---")
    all_results[pname] = {}
    for m in models:
        ok_count = 0
        latencies = []
        errors = {}
        for i in range(BURSTS):
            s, ms, resp = chat_once(base, key, m)
            if s == 'OK':
                ok_count += 1
                latencies.append(ms)
            else:
                errors[str(ms)] = errors.get(str(ms), 0) + 1
            time.sleep(0.2)
        avg_ms = int(sum(latencies)/len(latencies)) if latencies else 0
        all_results[pname][m] = {'ok': ok_count, 'avg_ms': avg_ms, 'errors': errors}
        flag = '✅' if ok_count >= BURSTS - 1 else '⚠️' if ok_count >= BURSTS//2 else '❌'
        err_str = ' '.join(f'{k}x{v}' for k,v in sorted(errors.items(), key=lambda x:-x[1])) if errors else 'clean'
        print(f"  {flag} {ok_count}/{BURSTS}  avg={avg_ms}ms  [{err_str}]  {m}")

# Final ranking
print("\n" + "="*60)
print("FINAL RANKING — ALL CANDIDATES (by burst success, then latency)")
print("="*60)
flat = []
for prov, models_data in all_results.items():
    for m, d in models_data.items():
        flat.append((prov, m, d['ok'], d['avg_ms'], d['errors']))

for prov, m, ok, avg, errs in sorted(flat, key=lambda x: (-x[2], x[3])):
    flag = '✅' if ok == BURSTS else '⚠️'
    print(f"  {flag} {prov:15s} {ok:2d}/{BURSTS}  {avg:5d}ms  {m}")

# Save
out = {pname: {m: d for m, d in models_data.items()}
       for pname, models_data in all_results.items()}
Path.home().joinpath('.hermes/provider-sweep-burst.json').write_text(json.dumps(out, indent=2))
print(f"\nSaved to ~/.hermes/provider-sweep-burst.json")

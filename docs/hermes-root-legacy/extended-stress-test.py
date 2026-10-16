#!/usr/bin/env python3
"""Extended stress test - 20 bursts per model to find truly long-limit models."""
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

# ALL working models from sweep + additional candidates to test
candidates = [
    # 9router - test more variants
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.5-flash-extra-low'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3-flash-agent'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.7-flash-low'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.6-flash-low'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.5-flash-low'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.5-flash-medium'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.7-flash-medium'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'gh/gpt-4o-mini'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'gh/gpt-5-mini'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ollama/minimax-m3'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'gemini/gemma-4-31b-it'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'kimi/kimi-k2.6'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'kimi/kimi-k2.5'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-pro-agent'),
    ('9router', 'NINE_ROUTER_API_KEY', 'http://localhost:20128/v1', 'ag/gemini-3.1-pro-low'),
    # opencode-zen
    ('opencode-zen', 'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1', 'hy3-free'),
    ('opencode-zen', 'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1', 'big-pickle'),
    ('opencode-zen', 'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1', 'laguna-s-2.1-free'),
    ('opencode-zen', 'OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1', 'nemotron-3-ultra-free'),
]

BURSTS = 20
print(f"=== EXTENDED STRESS TEST — {BURSTS} BURSTS PER MODEL ===\n")
print("Testing all candidates for LONG LIMIT (rate limit tolerance)...\n")

results = []
for prov, kenv, base, model in candidates:
    key = env.get(kenv, '')
    if not key:
        print(f"❌ SKIP {model} (no key)"); continue
    ok = 0
    errors = {}
    latencies = []
    for i in range(BURSTS):
        s, ms = chat_once(base, key, model)
        if s == 'OK':
            ok += 1
            latencies.append(ms)
        else:
            errors[str(ms)] = errors.get(str(ms), 0) + 1
        time.sleep(0.1)  # minimal delay
    
    avg = int(sum(latencies)/len(latencies)) if latencies else 0
    results.append((prov, model, ok, avg, errors))
    
    # Rating
    if ok >= 18: rating = '🟢 EXCELLENT'
    elif ok >= 15: rating = '🟡 GOOD'
    elif ok >= 10: rating = '🟠 FAIR'
    else: rating = '🔴 POOR'
    
    err_str = ' '.join(f'{k}x{v}' for k,v in sorted(errors.items(), key=lambda x:-x[1])) if errors else 'clean'
    print(f"{rating}  {ok:2d}/{BURSTS}  avg={avg:5d}ms  [{err_str:20s}]  {prov:15s} {model}")

# Sort by success rate then latency
print("\n" + "="*70)
print("RANKING — BEST FOR LONG LIMIT (sorted by burst success, then latency)")
print("="*70)
for prov, model, ok, avg, errs in sorted(results, key=lambda x: (-x[2], x[3])):
    rating = '🟢 EXCELLENT' if ok >= 18 else '🟡 GOOD' if ok >= 15 else '🟠 FAIR' if ok >= 10 else '🔴 POOR'
    print(f"{rating}  {ok:2d}/{BURSTS}  {avg:5d}ms  {prov:15s} {model}")

# Save
Path.home().joinpath('.hermes/extended-stress-test.json').write_text(json.dumps([
    {'provider': p, 'model': m, 'ok': ok, 'avg_ms': avg, 'errors': e}
    for p, m, ok, avg, e in results
], indent=2))
print(f"\nSaved to ~/.hermes/extended-stress-test.json")

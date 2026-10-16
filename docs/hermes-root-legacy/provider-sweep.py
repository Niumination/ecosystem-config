#!/usr/bin/env python3
"""
Sweep semua provider + stress-test kandidat free tier.
Cari env key di ~/.hermes/.env lalu jalankan probe per provider.
"""
import json, os, sys, time, urllib.error, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---- env loader ----
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
    'nvidia_nim':    ('NVIDIA_NIM_API_KEY',   'https://integrate.api.nvidia.com/v1'),
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
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read().decode()
            # handle SSE
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
        return 'ERR', f'HTTP {e.code} {e.reason}'
    except Exception as e:
        return 'ERR', f'{type(e).__name__}: {str(e)[:80]}'

def burst_test(base, key, model, n=8, prompt='Halo'):
    results = []
    for i in range(n):
        status, resp = chat_once(base, key, model, prompt)
        results.append(status)
        time.sleep(0.3)
    ok = sum(1 for r in results if r == 'OK')
    counts = {}
    for r in results:
        counts[r] = counts.get(r, 0) + 1
    return ok, counts

# ========================================
print('='*60)
print('  PROVIDER SWEEP + STRESS TEST')
print('='*60)

# Phase 1: list models per provider
print('\n[Phase 1] Provider model count...')
provider_status = {}
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(probe_models, p, env.get(k), b): p for p, (k, b) in KEYS.items()}
    for f in as_completed(futures):
        r = f.result()
        provider_status[r['p']] = r
        status = f"✅ {r['n']} models" if not r['err'] else f"❌ {r['err']}"
        print(f'  {r["p"]:15s} {status}')

# Phase 2: candidate free-tier models
# Strategy: pick best-looking free candidates from each provider
cand_set = set()
# 9router — fast flash variants, kimi coding
for m in provider_status['9router']['models']:
    if any(x in m for x in ['flash', 'kimi', 'gpt-4o-mini', 'gpt-5-mini', 'gemma-4', 'claude-haiku']):
        cand_set.add(('9router', m))
# OpenRouter free
for m in provider_status['openrouter']['models']:
    if ':free' in m:
        cand_set.add(('openrouter', m))
# opencode-zen (if alive)
if provider_status['opencode-zen']['n'] > 0:
    for m in provider_status['opencode-zen']['models']:
        if 'free' in m.lower() or 'hy3' in m.lower() or 'nemotron' in m.lower() or 'laguna' in m.lower():
            cand_set.add(('opencode-zen', m))
# huancheng (if alive)
if provider_status['huancheng']['n'] > 0:
    for m in provider_status['huancheng']['models']:
        cand_set.add(('huancheng', m))

candidates = list(cand_set)
print(f'\n[Phase 2] Stress-test {len(candidates)} candidates (8 bursts each)...')

results = []
for provider, model in sorted(candidates):
    key = env.get(KEYS[provider][0], '')
    base = KEYS[provider][1]
    if not key:
        results.append((provider, model, 0, {}, 'NO_KEY'))
        print(f'  ❌ SKIP  {provider}/{model}  (no key)')
        continue
    ok, counts = burst_test(base, key, model, n=8)
    results.append((provider, model, ok, counts, None))
    flag = '✅' if ok >= 7 else '⚠️' if ok >= 4 else '❌'
    cnt_str = ' '.join(f'{k}x{v}' for k,v in sorted(counts.items(), key=lambda x:-x[1]))
    print(f'  {flag} {ok}/8  {provider:15s} {model}')
    # stop early on consistent failure
    if ok == 0:
        pass  # still record it

# ========================================
# Ranking & recommendations
print('\n' + '='*60)
print('  RANKING + RECOMMENDATIONS')
print('='*60)

# Filter to free/likely-free
good = [(p,m,ok,c,e) for p,m,ok,c,e in results if ok >= 6 and e is None]
ok4  = [(p,m,ok,c,e) for p,m,ok,c,e in results if 4 <= ok < 6 and e is None]
bad  = [(p,m,ok,c,e) for p,m,ok,c,e in results if ok < 4 and e is None]

print(f'\n  ⭐ HIGH (≥6/8): {len(good)} models')
for p,m,ok,c,_ in sorted(good, key=lambda x:-x[2]):
    print(f'     {p:15s}  {m}')

print(f'\n  ⚠️ MEDIUM (4-5/8): {len(ok4)} models')
for p,m,ok,c,_ in sorted(ok4, key=lambda x:-x[2])[:5]:
    print(f'     {p:15s}  {m}')

print(f'\n  ❌ LOW (<4/8): {len(bad)} models (skip)')

# Quick probe the top 10 for latency + content quality
print('\n[Phase 3] Latency + quality probe — top 10...')
top10 = sorted(good, key=lambda x:-x[2])[:10]
probes = []
for p,m,_,_,_ in top10:
    key = env.get(KEYS[p][0], '')
    base = KEYS[p][1]
    t0 = time.time()
    status, resp = chat_once(base, key, m, 'Balas dengan satu kalimat yang berguna tentang Niumination dalam bahasa Indonesia.')
    latency = time.time() - t0
    probes.append((p, m, latency, status, resp[:80]))
    flag = '✅' if status == 'OK' else '❌'
    print(f'  {flag} {latency:5.1f}s  {p:15s} {m}')
    print(f'       → {resp[:100]}')

# Write results JSON for follow-up
out = {
    'provider_status': {k: {'n': v['n'], 'err': v['err']} for k,v in provider_status.items()},
    'stress_results': [{'provider': p, 'model': m, 'ok': ok, 'counts': dict(c)} for p,m,ok,c,_ in results],
    'top_probes': [{'provider': p, 'model': m, 'latency_s': round(l,1), 'status': s, 'resp': r} for p,m,l,s,r in probes],
}
out_path = Path.home() / '.hermes' / 'provider-sweep-2026-08-29.json'
out_path.write_text(json.dumps(out, indent=2))
print(f'\n  📊 Full results written to {out_path}')

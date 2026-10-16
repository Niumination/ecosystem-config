#!/usr/bin/env python3
"""Rapid provider scan - single chat probe per candidate model, 8s timeout."""
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

KEYS = {
    '9router':      ('NINE_ROUTER_API_KEY',  'http://localhost:20128/v1'),
    'openrouter':   ('OPENROUTER_API_KEY',   'https://openrouter.ai/api/v1'),
    'opencode-zen': ('OPENCODE_ZEN_API_KEY', 'https://opencode.ai/zen/v1'),
}
UA = 'hermes-agent/0.19.0'

def probe(provider, key, base, model):
    body = json.dumps({
        'model': model, 'messages': [{'role': 'user', 'content': 'Reply: OK'}],
        'max_tokens': 5, 'stream': False
    }).encode()
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
                    ln = ln.strip()
                    if ln.startswith('data:'):
                        try:
                            obj = json.loads(ln[5:].strip())
                            c = obj.get('choices',[{}])[0].get('delta',{}).get('content','')
                            if c: parts.append(c)
                        except: pass
                resp = ''.join(parts) if parts else '(empty SSE)'
            else:
                data = json.loads(raw)
                resp = data.get('choices',[{}])[0].get('message',{}).get('content','')[:40]
            ms = int((time.time()-t0)*1000)
            return ('OK', ms, resp)
    except urllib.error.HTTPError as e:
        return ('ERR', e.code, e.reason)
    except Exception as e:
        return ('ERR', 0, f'{type(e).__name__}: {str(e)[:60]}')

print("=== CANDIDATE PROBE ===\n")
results_all = []

# 9router candidates
c9 = [
    'gh/gpt-4o-mini', 'gh/gpt-5-mini', 'gh/gpt-5.4-mini-free-auto',
    'gh/gpt-5.6-luna-free-auto', 'gh/claude-haiku-4.5',
    'ag/gemini-3.7-flash-medium', 'ag/gemini-3.7-flash-low',
    'ag/gemini-3.5-flash-extra-low', 'ag/gemini-3.5-flash-low',
    'ag/gemini-3-flash-agent',
    'kimi/kimi-k3', 'kimi/kimi-k2.5', 'kimi/kimi-for-coding',
    'gemini/gemma-4-31b-it',
    'ollama/minimax-m3', 'ollama/glm-4.7-flash', 'ollama/qwen3.5',
    'nvidia/minimaxai/minimax-m3',
]
key = env.get('NINE_ROUTER_API_KEY',''); base = 'http://localhost:20128/v1'
print("--- 9router ---")
for m in c9:
    if not key: break
    s, code, resp = probe('9router', key, base, m)
    tag = f"✅ {code}ms" if s=='OK' else f"❌ {code}"
    print(f"  {tag}  {m}")
    results_all.append(('9router', m, s, code, resp))

# OpenRouter free candidates
or_free = [
    'google/gemma-4-31b-it:free', 'google/gemma-4-26b-a4b-it:free',
    'nvidia/nemotron-3-ultra-550b-a55b:free', 'nvidia/nemotron-3.5-lightning:free',
    'nvidia/nemotron-3-super-120b-a12b:free',
    'poolside/laguna-s-2.1:free', 'poolside/laguna-xs-2.1:free',
    'cohere/north-mini-code:free',
    'minimax/minimax-m3:free', 'minimax/minimax-m2.7:free',
    'dots-studio/dots-3-note-preview:free',
    'z-ai/glm-5.2:free',
]
key = env.get('OPENROUTER_API_KEY',''); base = 'https://openrouter.ai/api/v1'
print("\n--- openrouter :free ---")
for m in or_free:
    if not key: break
    s, code, resp = probe('openrouter', key, base, m)
    tag = f"✅ {code}ms" if s=='OK' else f"❌ {code}"
    print(f"  {tag}  {m}")
    results_all.append(('openrouter', m, s, code, resp))

# Zen candidates
zen_cands = [
    'hy3-free', 'nemotron-3-ultra-free', 'nemotron-3.5-lightning-free',
    'laguna-s-2.1-free', 'laguna-xs-2.1-free',
    'big-pickle', 'deepseek-v4-flash-free',
]
key = env.get('OPENCODE_ZEN_API_KEY',''); base = 'https://opencode.ai/zen/v1'
print("\n--- opencode-zen ---")
for m in zen_cands:
    if not key: break
    s, code, resp = probe('opencode-zen', key, base, m)
    tag = f"✅ {code}ms" if s=='OK' else f"❌ {code}"
    print(f"  {tag}  {m}")
    results_all.append(('opencode-zen', m, s, code, resp))

# Summary
print("\n" + "="*60)
print("SUMMARY — WORKING MODELS (sorted by latency)")
print("="*60)
ok = [(p,m,c,r) for p,m,s,c,r in results_all if s=='OK']
for p, m, ms, _ in sorted(ok, key=lambda x: x[2]):
    print(f"  {p:15s} {ms:5d}ms  {m}")

print(f"\nTotal working: {len(ok)}/{len(results_all)}")

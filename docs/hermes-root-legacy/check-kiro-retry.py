#!/usr/bin/env python3
"""Retry check with longer timeout."""
import urllib.request, json, os, time
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
key = env.get('NINE_ROUTER_API_KEY', '')
UA = 'hermes-agent/0.19.0'

if not key:
    print("❌ No key"); exit(1)

base = 'http://localhost:20128/v1'

print("=== RETRY CHECK (with retry) ===\n")

for attempt in range(5):
    try:
        req = urllib.request.Request(
            base + '/models',
            headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
            models = [m['id'] for m in data['data']]
            
            print(f"✅ SUCCESS (attempt {attempt+1})")
            print(f"Total models: {len(models)}\n")
            
            # Search for kiro
            kiro_models = [m for m in models if 'kiro' in m.lower()]
            
            if kiro_models:
                print(f"✅ FOUND {len(kiro_models)} KIRO MODEL(S):")
                for m in sorted(kiro_models):
                    print(f"  - {m}")
                    
                # Test them
                print(f"\n=== TESTING ===\n")
                for model in sorted(kiro_models):
                    body = json.dumps({
                        'model': model,
                        'messages': [{'role': 'user', 'content': 'HI'}],
                        'max_tokens': 10
                    }).encode()
                    req = urllib.request.Request(
                        base + '/chat/completions',
                        data=body,
                        method='POST'
                    )
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
                                    if ln.strip().startswith('data:'):
                                        try:
                                            c = json.loads(ln[5:].strip()).get('choices',[{}])[0].get('delta',{}).get('content','')
                                            if c: parts.append(c)
                                        except: pass
                                resp = ''.join(parts) if parts else '(empty)'
                            else:
                                d = json.loads(raw)
                                resp = d.get('choices',[{}])[0].get('message',{}).get('content','')[:50]
                            ms = int((time.time()-t0)*1000)
                            print(f"✅ {ms}ms  {model} -> {resp}")
                    except Exception as e:
                        print(f"❌ {type(e).__name__}  {model}")
            else:
                print("❌ NO KIRO MODELS YET")
                print("\nCurrent prefixes:")
                prefixes = {}
                for m in models:
                    p = m.split('/')[0]
                    prefixes.setdefault(p, []).append(m)
                for p in sorted(prefixes.keys()):
                    print(f"  {p}: {len(prefixes[p])} models")
            
            break
            
    except Exception as e:
        print(f"Attempt {attempt+1}/5 failed: {type(e).__name__}")
        if attempt < 4:
            print("Retrying in 3 seconds...")
            time.sleep(3)
        else:
            print(f"\n❌ All attempts failed: {e}")

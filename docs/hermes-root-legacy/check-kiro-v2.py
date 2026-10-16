#!/usr/bin/env python3
"""Check if kiro models exist on 9router."""
import json, os, urllib.request, urllib.error
from pathlib import Path
import time

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
    print("❌ No NINE_ROUTER_API_KEY found"); exit(1)

base = 'http://localhost:20128/v1'

# Retry up to 3 times with delay
for attempt in range(3):
    try:
        req = urllib.request.Request(
            base + '/models',
            headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
            models = [m['id'] for m in data['data']]
            
            print(f"=== 9ROUTER CATALOG CHECK ===\n")
            print(f"Total models: {len(models)}\n")
            
            # Search for kiro
            kiro_models = [m for m in models if 'kiro' in m.lower()]
            
            if kiro_models:
                print(f"✅ FOUND {len(kiro_models)} KIRO MODEL(S):")
                for m in sorted(kiro_models):
                    print(f"  - {m}")
                    
                # Test each kiro model
                print(f"\n=== TESTING KIRO MODELS ===\n")
                for model in sorted(kiro_models):
                    body = json.dumps({
                        'model': model,
                        'messages': [{'role': 'user', 'content': 'OK'}],
                        'max_tokens': 5,
                        'stream': False
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
                        with urllib.request.urlopen(req, timeout=10) as r:
                            raw = r.read().decode()
                            if 'data:' in raw:
                                parts = []
                                for ln in raw.splitlines():
                                    if ln.strip().startswith('data:'):
                                        try:
                                            c = json.loads(ln[5:].strip()).get('choices',[{}])[0].get('delta',{}).get('content','')
                                            if c: parts.append(c)
                                        except: pass
                                resp = ''.join(parts) if parts else '(empty SSE)'
                            else:
                                data = json.loads(raw)
                                resp = data.get('choices',[{}])[0].get('message',{}).get('content','')[:40]
                            ms = int((time.time()-t0)*1000)
                            print(f"✅ {ms}ms  {model} -> {resp}")
                    except urllib.error.HTTPError as e:
                        print(f"❌ HTTP {e.code}  {model}")
                    except Exception as e:
                        print(f"❌ {type(e).__name__}  {model}")
            else:
                print("❌ NO KIRO MODELS FOUND YET")
                print("\nAll available prefixes:")
                prefixes = {}
                for m in models:
                    prefix = m.split('/')[0] if '/' in m else 'root'
                    prefixes.setdefault(prefix, []).append(m)
                for p in sorted(prefixes.keys()):
                    count = len(prefixes[p])
                    print(f"  {p}: {count} models")
            break
            
    except urllib.error.URLError as e:
        if attempt < 2:
            print(f"Connection error (attempt {attempt+1}/3): {e}")
            print("Retrying in 2 seconds...")
            time.sleep(2)
        else:
            print(f"❌ Connection failed after 3 attempts: {e}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        break

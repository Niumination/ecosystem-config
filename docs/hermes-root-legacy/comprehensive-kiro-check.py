#!/usr/bin/env python3
"""Comprehensive check for kiro models after 9router restart."""
import json, urllib.request, sys
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
    print("❌ No API key"); sys.exit(1)

print("=== COMPREHENSIVE KIRO CHECK ===\n")

# Get all models
req = urllib.request.Request(
    'http://localhost:20128/v1/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
)
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.load(r)
    models = [m['id'] for m in data['data']]
    
    print(f"Total models: {len(models)}\n")
    
    # Check for kiro
    kiro = [m for m in models if 'kiro' in m.lower()]
    
    if kiro:
        print(f"✅ FOUND {len(kiro)} KIRO MODEL(S):\n")
        for m in sorted(kiro):
            print(f"  - {m}")
        
        # Test each
        print(f"\n=== TESTING KIRO MODELS ===\n")
        for model in sorted(kiro):
            import time
            body = json.dumps({
                'model': model,
                'messages': [{'role': 'user', 'content': 'OK'}],
                'max_tokens': 5
            }).encode()
            req = urllib.request.Request(
                'http://localhost:20128/v1/chat/completions',
                data=body,
                method='POST'
            )
            req.add_header('Content-Type', 'application/json')
            req.add_header('Authorization', f'Bearer {key}')
            req.add_header('User-Agent', UA)
            
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
                    resp = ''.join(parts) if parts else '(empty)'
                else:
                    d = json.loads(raw)
                    resp = d.get('choices',[{}])[0].get('message',{}).get('content','')[:40]
                ms = int((time.time()-t0)*1000)
                print(f"✅ {ms}ms  {model}")
        
        print(f"\n🎉 SUCCESS! Kiro models are available!")
        sys.exit(0)
    else:
        print("❌ NO KIRO MODELS FOUND")
        print("\nAll available prefixes:")
        prefixes = {}
        for m in models:
            p = m.split('/')[0]
            prefixes.setdefault(p, []).append(m)
        for p in sorted(prefixes.keys()):
            items = sorted(prefixes[p])[:10]
            print(f"\n{p}: {len(prefixes[p])} models")
            for m in items:
                print(f"  - {m}")
            if len(prefixes[p]) > 10:
                print(f"  ... and {len(prefixes[p]) - 10} more")
        
        print(f"\n=== ANALYSIS ===")
        print(f"Total: {len(models)} models")
        print(f"Prefixes: {', '.join(sorted(prefixes.keys()))}")
        print(f"Kiro status: NOT YET AVAILABLE")
        print(f"\nPossible reasons:")
        print(f"  1. Propagation delay (5-15 minutes typical)")
        print(f"  2. Needs admin approval on 9router dashboard")
        print(f"  3. Different naming convention (check dashboard)")
        print(f"  4. Registration not completed yet")

#!/usr/bin/env python3
"""Full scan for kiro models on 9router."""
import json, os, urllib.request
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

req = urllib.request.Request(
    'http://localhost:20128/v1/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
)

with urllib.request.urlopen(req, timeout=5) as r:
    data = json.load(r)
    models = [m['id'] for m in data['data']]
    
    print(f"=== FULL 9ROUTER SCAN ===\n")
    print(f"Total models: {len(models)}\n")
    
    # Search for kiro (case-insensitive)
    kiro_models = [m for m in models if 'kiro' in m.lower()]
    
    if kiro_models:
        print(f"✅ FOUND {len(kiro_models)} KIRO MODEL(S):")
        for m in sorted(kiro_models):
            print(f"  - {m}")
    else:
        print("❌ NO KIRO MODELS FOUND")
        print("\nAll available prefixes:")
        prefixes = {}
        for m in models:
            prefix = m.split('/')[0] if '/' in m else 'root'
            prefixes.setdefault(prefix, []).append(m)
        for p in sorted(prefixes.keys()):
            count = len(prefixes[p])
            print(f"  {p}: {count} models")
            
            # Show first 5 examples
            examples = sorted(prefixes[p])[:5]
            for e in examples:
                print(f"    - {e}")
            if count > 5:
                print(f"    ... and {count - 5} more")
            print()

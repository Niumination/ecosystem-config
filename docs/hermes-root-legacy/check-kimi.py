#!/usr/bin/env python3
"""Check if any kimi models exist on 9router with correct naming."""
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

req = urllib.request.Request(
    'http://localhost:20128/v1/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': 'hermes-agent/0.19.0'}
)

with urllib.request.urlopen(req, timeout=5) as r:
    data = json.load(r)
    models = [m['id'] for m in data['data']]
    
    # Search for kimi-related
    kimi_related = [m for m in models if 'kimi' in m.lower() or 'moonshot' in m.lower()]
    
    print(f"=== KIMI MODELS ON 9ROUTER ===\n")
    print(f"Total models: {len(models)}")
    print(f"Kimi-related: {len(kimi_related)}")
    print()
    
    if kimi_related:
        print("Found kimi models:")
        for m in sorted(kimi_related):
            print(f"  - {m}")
    else:
        print("❌ NO KIMI MODELS FOUND on 9router!")
        print()
        print("Available prefixes:")
        prefixes = set(m.split('/')[0] for m in models)
        for p in sorted(prefixes):
            count = sum(1 for m in models if m.startswith(p + '/'))
            print(f"  - {p}: {count} models")
        
        print()
        print("Note: Earlier scan showed kimi models but they returned 404.")
        print("They may have been removed or renamed by 9router.")

#!/usr/bin/env python3
"""Get full model list from 9router and identify kimi-related models."""
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

if not key:
    print("❌ No key"); exit(1)

req = urllib.request.Request(
    'http://localhost:20128/v1/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': 'hermes-agent/0.19.0'}
)

with urllib.request.urlopen(req, timeout=5) as r:
    data = json.load(r)
    models = [m['id'] for m in data['data']]
    
    print(f"Total models on 9router: {len(models)}\n")
    
    # Group by prefix
    prefixes = {}
    for m in models:
        prefix = m.split('/')[0] if '/' in m else 'root'
        prefixes.setdefault(prefix, []).append(m)
    
    print("=== MODELS BY PREFIX ===\n")
    for prefix in sorted(prefixes.keys()):
        items = prefixes[prefix]
        print(f"{prefix}: ({len(items)} models)")
        for m in sorted(items):
            print(f"  - {m}")
        print()

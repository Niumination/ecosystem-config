#!/usr/bin/env python3
"""Scan for all kr/ models and identify which are kiro-related."""
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

print("=== SCANNING KR/ PREFIX MODELS ===\n")

req = urllib.request.Request(
    'http://localhost:20128/v1/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
)
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.load(r)
    models = [m['id'] for m in data['data']]
    
    # Get all kr/ models
    kr_models = [m for m in models if m.startswith('kr/')]
    
    print(f"Total kr/ models: {len(kr_models)}\n")
    
    # Categorize
    categories = {
        'claude': [],
        'deepseek': [],
        'glm': [],
        'minimax': [],
        'qwen': [],
        'other': []
    }
    
    for m in sorted(kr_models):
        if 'claude' in m.lower():
            categories['claude'].append(m)
        elif 'deepseek' in m.lower():
            categories['deepseek'].append(m)
        elif 'glm' in m.lower():
            categories['glm'].append(m)
        elif 'minimax' in m.lower():
            categories['minimax'].append(m)
        elif 'qwen' in m.lower():
            categories['qwen'].append(m)
        else:
            categories['other'].append(m)
    
    for cat, items in categories.items():
        if items:
            print(f"{cat.upper()} ({len(items)}):")
            for m in items:
                print(f"  - {m}")
            print()
    
    # Check for opus-5 specifically
    print("="*50)
    print("CHECKING FOR CLAUDE-OPUS MODELS:")
    opus_models = [m for m in kr_models if 'opus' in m.lower()]
    if opus_models:
        print(f"✅ Found: {opus_models}")
    else:
        print("❌ No opus models found in kr/ prefix")
    
    # Check full catalog for opus
    print("\n" + "="*50)
    print("CHECKING FULL CATALOG FOR OPUS MODELS:")
    all_opus = [m for m in models if 'opus' in m.lower()]
    if all_opus:
        print(f"✅ Found {len(all_opus)} opus model(s):")
        for m in all_opus:
            print(f"  - {m}")
    else:
        print("❌ No opus models in full catalog")

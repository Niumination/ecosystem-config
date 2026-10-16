#!/usr/bin/env python3
"""Deep scan - check ALL models and categorize by prefix."""
import json, urllib.request, os
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
    
    print(f"=== 9ROUTER FULL CATALOG SCAN ===\n")
    print(f"Total models: {len(models)}\n")
    
    # Categorize by prefix
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
    
    # Check for any model that might be kiro-related
    print("\n=== SEARCHING FOR KIRO/POTENTIAL MATCHES ===\n")
    candidates = [m for m in models if any(x in m.lower() for x in ['kiro', 'mira', 'cortex', 'deep', 'glm', 'qwen', 'claude', 'gemini'])]
    
    if candidates:
        print(f"Found {len(candidates)} potential matches:")
        for m in sorted(candidates):
            print(f"  - {m}")
    else:
        print("No candidates found.")
    
    # Summary
    print(f"\n=== SUMMARY ===\n")
    print(f"Total: {len(models)} models")
    print(f"Prefixes: {', '.join(sorted(prefixes.keys()))}")
    print(f"Kiro models: 0 (not yet available)")
    
    # Check if any new prefixes appeared
    known_prefixes = {'ag', 'gemini', 'gh', 'kr'}
    new_prefixes = set(prefixes.keys()) - known_prefixes
    if new_prefixes:
        print(f"\n🆕 NEW PREFIXES DETECTED: {new_prefixes}")
    else:
        print(f"\nNo new prefixes detected.")

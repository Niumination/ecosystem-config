#!/usr/bin/env python3
"""
Monitor 9router catalog and alert when new models appear.
Run this periodically to check for kiro models.
"""
import json, os, time, urllib.request
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

print("=== 9ROUTER CATALOG MONITOR ===\n")
print("Watching for new models (kiro, etc.)...\n")

# Load previous state
state_file = Path.home() / '.hermes' / '9router-catalog-state.json'
previous_models = set()
if state_file.exists():
    previous_models = set(json.loads(state_file.read_text()).get('models', []))

# Get current catalog
req = urllib.request.Request(
    'http://localhost:20128/v1/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
)

with urllib.request.urlopen(req, timeout=5) as r:
    data = json.load(r)
    current_models = set(m['id'] for m in data['data'])

# Save current state
state_file.write_text(json.dumps({'models': list(current_models), 'timestamp': time.time()}))

# Find new models
new_models = current_models - previous_models
removed_models = previous_models - current_models

print(f"Total models: {len(current_models)}")
print(f"New models: {len(new_models)}")
print(f"Removed models: {len(removed_models)}")

if new_models:
    print("\n🎉 NEW MODELS DETECTED:")
    for m in sorted(new_models):
        print(f"  + {m}")

if removed_models:
    print("\n📤 REMOVED MODELS:")
    for m in sorted(removed_models):
        print(f"  - {m}")

# Check for kiro specifically
kiro_models = [m for m in current_models if 'kiro' in m.lower()]
if kiro_models:
    print(f"\n✅ KIRO MODELS FOUND: {kiro_models}")
else:
    print("\n⏳ Kiro models not yet available (check back after refresh)")

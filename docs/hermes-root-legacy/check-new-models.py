#!/usr/bin/env python3
"""Check for new models since last scan."""
import json, urllib.request, sys
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

print("=== CHECKING FOR NEW MODELS ===\n")

ENV = Path.home() / '.hermes' / '.env'
env = load_env(ENV)
key = env.get('NINE_ROUTER_API_KEY', '')
UA = 'hermes-agent/0.19.0'

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
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.load(r)
    current_models = set(m['id'] for m in data['data'])
    
    # Save current state
    state_file.write_text(json.dumps({
        'models': list(current_models),
        'timestamp': time.time()
    }))
    
    print(f"Previous models: {len(previous_models)}")
    print(f"Current models: {len(current_models)}")
    print()
    
    # Find changes
    new_models = current_models - previous_models
    removed_models = previous_models - current_models
    
    if new_models:
        print(f"🎉 NEW MODELS DETECTED: {len(new_models)}")
        for m in sorted(new_models):
            print(f"  + {m}")
    else:
        print("❌ No new models detected")
    
    if removed_models:
        print(f"\n📤 REMOVED MODELS: {len(removed_models)}")
        for m in sorted(removed_models):
            print(f"  - {m}")
    
    # Check for kiro specifically
    kiro_models = [m for m in current_models if 'kiro' in m.lower()]
    if kiro_models:
        print(f"\n✅ KIRO MODELS FOUND: {kiro_models}")
        sys.exit(0)
    else:
        print(f"\n⏳ Kiro models still not available")
        print(f"\nTip: Check 9router dashboard at http://localhost:20128")
        print(f"      or https://9router.app (if remote)")

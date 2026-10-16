#!/usr/bin/env python3
"""Restart 9router and check for kiro models."""
import subprocess
import time
import urllib.request
import json
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

print("=== RESTARTING 9ROUTER ===\n")

# Stop
print("Stopping 9router...")
subprocess.run(['launchctl', 'bootout', 'gui/501/com.9router.autostart'], capture_output=True)
time.sleep(3)

# Start
print("Starting 9router...")
subprocess.run(['launchctl', 'bootstrap', 'gui/501', '/Library/LaunchAgents/com.9router.autostart.plist'], capture_output=True)
time.sleep(5)

# Wait for startup
print("Waiting for 9router to be ready...")
for i in range(10):
    try:
        req = urllib.request.Request(
            'http://localhost:20128/v1/models',
            headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            print(f"✅ 9router is ready (attempt {i+1})")
            break
    except Exception as e:
        print(f"Attempt {i+1}/10: {type(e).__name__}")
        time.sleep(2)
else:
    print("❌ 9router failed to start")
    exit(1)

# Get models
print("\nFetching model catalog...")
req = urllib.request.Request(
    'http://localhost:20128/v1/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
)
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.load(r)
    models = [m['id'] for m in data['data']]
    
    print(f"\nTotal models: {len(models)}\n")
    
    # Search for kiro
    kiro_models = [m for m in models if 'kiro' in m.lower()]
    
    if kiro_models:
        print(f"✅ FOUND {len(kiro_models)} KIRO MODEL(S):")
        for m in sorted(kiro_models):
            print(f"  - {m}")
            
        # Test each
        print(f"\n=== TESTING KIRO MODELS ===\n")
        base = 'http://localhost:20128/v1'
        for model in sorted(kiro_models):
            body = json.dumps({
                'model': model,
                'messages': [{'role': 'user', 'content': 'OK'}],
                'max_tokens': 5
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
                        resp = ''.join(parts) if parts else '(empty)'
                    else:
                        d = json.loads(raw)
                        resp = d.get('choices',[{}])[0].get('message',{}).get('content','')[:40]
                    ms = int((time.time()-t0)*1000)
                    print(f"✅ {ms}ms  {model} -> {resp}")
            except Exception as e:
                print(f"❌ {type(e).__name__}  {model}")
    else:
        print("❌ NO KIRO MODELS FOUND")
        print("\nAvailable prefixes:")
        prefixes = {}
        for m in models:
            p = m.split('/')[0]
            prefixes.setdefault(p, []).append(m)
        for p in sorted(prefixes.keys()):
            print(f"  {p}: {len(prefixes[p])} models")

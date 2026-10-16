#!/usr/bin/env python3
"""Check 9router health and kiro models."""
import urllib.request, json, os, time
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

print("=== CHECKING 9ROUTER STATUS ===\n")

# Check if port is open
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 20128))
if result != 0:
    print("❌ Port 20128 is CLOSED - 9router may need restart")
    print("\nTry restarting with:")
    print("  launchctl kickstart -k gui/$(id -u)/com.9router.autostart")
    sock.close()
    exit(1)
else:
    print("✅ Port 20128 is OPEN")
sock.close()

# Try to get models
if not key:
    print("❌ No NINE_ROUTER_API_KEY found"); exit(1)

base = 'http://localhost:20128/v1'
req = urllib.request.Request(
    base + '/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
)

try:
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
                            data = json.loads(raw)
                            resp = data.get('choices',[{}])[0].get('message',{}).get('content','')[:40]
                        ms = int((time.time()-t0)*1000)
                        print(f"✅ {ms}ms  {model} -> {resp}")
                except Exception as e:
                    print(f"❌ {type(e).__name__}  {model}")
        else:
            print("❌ NO KIRO MODELS FOUND YET")
            
except Exception as e:
    print(f"❌ Error fetching models: {e}")

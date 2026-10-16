#!/usr/bin/env python3
"""Final check after 9router restart."""
import urllib.request, json, time, sys
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
    print("❌ No API key"); sys.exit(1)

print("=== FINAL CHECK ===\n")
print("Attempting to connect to 9router...\n")

for i in range(5):
    try:
        req = urllib.request.Request(
            'http://localhost:20128/v1/models',
            headers={
                'Authorization': f'Bearer {key}',
                'User-Agent': 'hermes-agent/0.19.0'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
            models = [m['id'] for m in data['data']]
            
            print(f"✅ Connected! Total models: {len(models)}\n")
            
            # Search for kiro
            kiro = [m for m in models if 'kiro' in m.lower()]
            
            if kiro:
                print(f"✅ FOUND {len(kiro)} KIRO MODEL(S):\n")
                for m in kiro:
                    print(f"  - {m}")
                
                # Test them
                print(f"\nTesting...\n")
                for model in kiro:
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
                    req.add_header('User-Agent', 'hermes-agent/0.19.0')
                    
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
                
                print(f"\n🎉 Kiro models are READY!")
                sys.exit(0)
            else:
                print("❌ NO KIRO MODELS YET")
                print("\nAvailable prefixes:")
                prefixes = {}
                for m in models:
                    p = m.split('/')[0]
                    prefixes.setdefault(p, []).append(m)
                for p in sorted(prefixes.keys()):
                    print(f"  {p}: {len(prefixes[p])} models")
                sys.exit(1)
                
    except Exception as e:
        print(f"Attempt {i+1}/5: {type(e).__name__}: {e}")
        if i < 4:
            print("Waiting 3 seconds before retry...")
            time.sleep(3)
        else:
            print(f"\n❌ Failed after 5 attempts: {e}")
            print("\n9router may still be starting up or crashed.")
            print("Try: launchctl kickstart -k gui/$(id -u)/com.9router.autostart")
            sys.exit(1)

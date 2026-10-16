#!/usr/bin/env python3
"""Full audit of 9router config and models."""
import json, urllib.request, sys, sqlite3, os
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

print("=== 9ROUTER CONFIG AUDIT ===\n")

# 1. Check launchd status
print("1. LAUNCHD STATUS:")
os.system('launchctl list | grep 9router')
print()

# 2. Check process
print("2. PROCESS STATUS:")
os.system('ps aux | grep 9router | grep -v grep')
print()

# 3. Check port
print("3. PORT STATUS:")
os.system('lsof -i :20128 2>/dev/null | head -5')
print()

# 4. Load API key
ENV = Path.home() / '.hermes' / '.env'
env = load_env(ENV)
key = env.get('NINE_ROUTER_API_KEY', '')

if not key:
    print("❌ No NINE_ROUTER_API_KEY found"); sys.exit(1)

UA = 'hermes-agent/0.19.0'
base = 'http://localhost:20128/v1'

# 5. Fetch models
print("4. FETCHING MODEL CATALOG:")
try:
    req = urllib.request.Request(
        base + '/models',
        headers={'Authorization': f'Bearer {key}', 'User-Agent': UA}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.load(r)
        models = [m['id'] for m in data['data']]
        print(f"✅ Total models: {len(models)}\n")
        
        # Categorize by prefix
        prefixes = {}
        for m in models:
            p = m.split('/')[0]
            prefixes.setdefault(p, []).append(m)
        
        print("5. MODELS BY PREFIX:")
        for p in sorted(prefixes.keys()):
            count = len(prefixes[p])
            print(f"  {p}: {count} models")
        print()
        
        # Search for kiro
        kiro = [m for m in models if 'kiro' in m.lower()]
        if kiro:
            print(f"✅ FOUND {len(kiro)} KIRO MODEL(S):")
            for m in kiro:
                print(f"  - {m}")
        else:
            print("❌ NO KIRO MODELS FOUND")
            print("\nPossible reasons:")
            print("  1. Propagation delay (5-15 min typical)")
            print("  2. Admin approval needed")
            print("  3. Different naming convention")
            print("  4. Registration incomplete")
        
        print("\n" + "="*50)
        print("6. DATABASE CHECK:")
        
        # Check SQLite database
        db_path = Path.home() / '.9router' / 'db' / 'data.sqlite'
        if db_path.exists():
            print(f"Database found: {db_path}")
            try:
                con = sqlite3.connect(str(db_path))
                cur = con.cursor()
                
                # Check providers
                cur.execute("SELECT id, name, isActive FROM providerConnections ORDER BY name")
                providers = cur.fetchall()
                print(f"\nProviders ({len(providers)}):")
                for p in providers:
                    status = "ACTIVE" if p[2] else "DISABLED"
                    print(f"  - {p[1]} ({p[0]}): {status}")
                
                # Check for kiro in database
                cur.execute("SELECT * FROM providerConnections WHERE name LIKE '%kiro%' OR name LIKE '%Kiro%' OR name LIKE '%KIRO%'")
                kiro_providers = cur.fetchall()
                
                if kiro_providers:
                    print(f"\n✅ Kiro providers found in database:")
                    for p in kiro_providers:
                        print(f"  - {p}")
                else:
                    print(f"\n❌ No kiro-related providers in database")
                
                con.close()
            except Exception as e:
                print(f"Error reading database: {e}")
        else:
            print(f"Database not found: {db_path}")
        
        print("\n" + "="*50)
        print("7. CONFIG.YAML CHECK:")
        
        # Check config.yaml for 9router settings
        config_path = Path.home() / '.hermes' / 'config.yaml'
        if config_path.exists():
            content = config_path.read_text()
            if '9router' in content:
                print("✅ 9router found in config.yaml")
                # Extract relevant lines
                for line in content.split('\n'):
                    if '9router' in line.lower() or 'localhost:20128' in line:
                        print(f"  {line.strip()}")
            else:
                print("⚠️  9router NOT found in config.yaml")
        else:
            print("⚠️  config.yaml not found")
        
        print("\n" + "="*50)
        print("8. RECOMMENDATIONS:")
        
        if not kiro:
            print("  • Wait 10-15 minutes for propagation")
            print("  • Check 9router dashboard for registration status")
            print("  • Ensure admin approval if required")
            print("  • Use alternatives: kr/qwen3-coder-next, kr/deepseek-3.2")
        
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")

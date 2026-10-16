#!/usr/bin/env python3
"""Debug 9router API response."""
import json
import urllib.request
import os

# Load API key
env_path = os.path.expanduser("~/.hermes/.env")
api_key = None
if os.path.exists(env_path):
    for line in open(env_path).readlines():
        if line.startswith("NINE_ROUTER_API_KEY="):
            api_key = line.split("=", 1)[1].strip().strip('"\'')
            break

print(f"API Key found: {bool(api_key)}")
print()

# Test 1: Check models endpoint
print("=== Test 1: GET /v1/models ===")
try:
    url = "http://localhost:20128/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "hermes-agent/0.19.0"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print(f"✅ Success: {len(data.get('data', []))} models")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Test 2: Test chat completion
print("=== Test 2: POST /v1/chat/completions ===")
model = "ag/gemini-3.5-flash-extra-low"
url = "http://localhost:20128/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "hermes-agent/0.19.0"
}

data = {
    "model": model,
    "messages": [{"role": "user", "content": "Hi"}],
    "max_tokens": 10
}

try:
    req = urllib.request.Request(
        url,
        method="POST",
        headers=headers,
        data=json.dumps(data).encode()
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode()
        print(f"Status: {resp.status}")
        print(f"Response (first 500 chars): {content[:500]}")
        
        # Try to parse
        try:
            result = json.loads(content)
            if 'choices' in result:
                print(f"✅ Response content: {result['choices'][0]['message']['content']}")
        except:
            print(f"⚠️  Not valid JSON")
            
except urllib.error.HTTPError as e:
    print(f"❌ HTTP Error: {e.code}")
    print(f"   Response: {e.read().decode()[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

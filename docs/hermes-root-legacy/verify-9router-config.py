#!/usr/bin/env python3
"""Verify Hermes can connect to 9router with new config."""
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

if not api_key:
    print("❌ NINE_ROUTER_API_KEY not found")
    exit(1)

# Test chat completion with working model
model = "ag/gemini-3.5-flash-extra-low"
url = "http://localhost:20128/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "hermes-agent/0.19.0"
}

data = {
    "model": model,
    "messages": [{"role": "user", "content": "Say hello in 5 words"}],
    "max_tokens": 20
}

print(f"=== Testing Model: {model} ===")
print()

try:
    req = urllib.request.Request(
        url,
        method="POST",
        headers=headers,
        data=json.dumps(data).encode()
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']
            print(f"✅ SUCCESS")
            print(f"   Model: {result.get('model', 'unknown')}")
            print(f"   Response: {message.get('content', 'N/A')}")
            print(f"   Latency: {(resp.headers.get('X-Response-Time', 'N/A'))}")
        else:
            print(f"❌ No choices in response")
            print(f"   Response: {result}")
            
except Exception as e:
    print(f"❌ ERROR: {e}")

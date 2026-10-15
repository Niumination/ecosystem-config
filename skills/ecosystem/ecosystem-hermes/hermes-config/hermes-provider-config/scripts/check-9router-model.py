#!/usr/bin/env python3
"""
Quick check if a 9router model is working.
Usage: python3 check-model.py <model-id>
"""
import json
import urllib.request
import sys
import os
from pathlib import Path

def load_env(path):
    d = {}
    if not path.exists(): return d
    for line in path.read_text().splitlines():
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            d[k.strip()] = v.strip().strip('"\'')
    return d

def test_model(model_id, api_key):
    """Test if a model responds to chat completion."""
    url = "http://localhost:20128/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "hermes-agent/0.19.0"
    }
    
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": "Say OK"}],
        "max_tokens": 5,
        "stream": False
    }
    
    try:
        req = urllib.request.Request(
            url,
            method="POST",
            headers=headers,
            data=json.dumps(data).encode()
        )
        
        import time
        start = time.time()
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            elapsed = (time.time() - start) * 1000
            content = resp.read().decode()
            
            # Handle SSE
            if content.startswith("data:"):
                lines = content.strip().split("\n")
                for line in lines:
                    if line.startswith("data:"):
                        try:
                            chunk = json.loads(line[5:].strip())
                            if 'choices' in chunk and chunk['choices']:
                                delta = chunk['choices'][0].get('delta', {})
                                if 'content' in delta and delta['content']:
                                    return True, f"{elapsed:.0f}ms", delta['content']
                                if chunk.get('choices', [{}])[0].get('finish_reason'):
                                    return True, f"{elapsed:.0f}ms", "(SSE response)"
                        except:
                            pass
                return True, f"{elapsed:.0f}ms", "(SSE)"
            else:
                result = json.loads(content)
                if 'choices' in result and result['choices']:
                    msg = result['choices'][0].get('message', {})
                    content = msg.get('content', '')
                    return True, f"{elapsed:.0f}ms", content[:50]
                return False, f"{elapsed:.0f}ms", "No choices"
                
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}", e.read().decode()[:100]
    except Exception as e:
        return False, "ERROR", str(e)[:100]

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check-model.py <model-id>")
        print("Example: python3 check-model.py ag/gemini-3.5-flash-extra-low")
        sys.exit(1)
    
    model_id = sys.argv[1]
    
    # Load API key
    env_path = Path.home() / ".hermes" / ".env"
    env = load_env(env_path)
    api_key = env.get("NINE_ROUTER_API_KEY")
    
    if not api_key:
        print("❌ NINE_ROUTER_API_KEY not found in ~/.hermes/.env")
        sys.exit(1)
    
    print(f"=== Testing: {model_id} ===")
    print()
    
    success, latency, response = test_model(model_id, api_key)
    
    if success:
        print(f"✅ WORKING ({latency})")
        if response and "(SSE)" not in response and "No choices" not in response:
            print(f"   Response: {response}")
    else:
        print(f"❌ FAILED ({latency})")
        if response and len(response) < 100:
            print(f"   Error: {response}")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

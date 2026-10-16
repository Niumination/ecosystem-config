#!/usr/bin/env python3
"""Try to disable models via kv table API."""
import json
import urllib.request
import hashlib
from pathlib import Path

# Load CLI token
machine_id = (Path.home() / ".9router" / "machine-id").read_text().strip()
cli_secret = (Path.home() / ".9router" / "auth" / "cli-secret").read_text().strip()
token = hashlib.sha256((machine_id + '9r-cli-auth' + cli_secret).encode()).hexdigest()[:16]

headers = {
    "x-9r-cli-token": token,
    "Content-Type": "application/json",
    "User-Agent": "hermes-agent/0.19.0"
}

# Models to disable
MODELS_TO_DISABLE = [
    "ag/gemini-3.5-flash-high",
    "ag/gpt-oss-120b-medium",
    "gemini/gemini-3.1-pro-preview",
    "gemini/gemini-3.7-flash",
    "gh/claude-haiku-4.5",
    "gh/exec-agent-b",
    "gh/gpt-3.5-turbo",
    "gh/gpt-4",
    "gh/gpt-4-0125-preview",
    "gh/gpt-4-0613",
    "gh/gpt-5-mini",
    "gh/gpt-5.4-mini-free-auto",
    "gh/gpt-5.6-luna",
    "gh/gpt-5.6-luna-free-auto",
    "gh/mai-code-1-flash",
    "gh/mai-code-1-flash-4th",
    "gh/mai-code-1-flash-picker",
    "gh/mai-code-1-flash-secondary",
    "gh/mai-code-1.1-flash",
    "gh/oswe-vscode-prime",
    "gh/trajectory-compaction",
    "kr/auto-thinking",
    "kr/claude-haiku-4.5-agentic",
    "kr/claude-haiku-4.5-thinking",
    "kr/claude-haiku-4.5-thinking-agentic",
    "kr/claude-sonnet-4",
    "kr/claude-sonnet-4-agentic",
    "kr/claude-sonnet-4-thinking",
    "kr/claude-sonnet-4-thinking-agentic",
    "kr/claude-sonnet-4.5-agentic",
    "kr/claude-sonnet-4.5-thinking",
    "kr/claude-sonnet-4.5-thinking-agentic",
    "kr/deepseek-3.2",
    "kr/deepseek-3.2-agentic",
    "kr/deepseek-3.2-thinking",
    "kr/deepseek-3.2-thinking-agentic",
    "kr/glm-5",
    "kr/glm-5-agentic",
    "kr/glm-5-thinking",
    "kr/glm-5-thinking-agentic",
    "kr/minimax-m2.1-agentic",
    "kr/minimax-m2.1-thinking",
    "kr/minimax-m2.1-thinking-agentic",
    "kr/minimax-m2.5-agentic",
    "kr/minimax-m2.5-thinking",
    "kr/minimax-m2.5-thinking-agentic",
    "kr/qwen3-coder-next",
    "kr/qwen3-coder-next-agentic",
    "kr/qwen3-coder-next-thinking",
    "kr/qwen3-coder-next-thinking-agentic",
]

def update_kv(scope, key, value):
    """Update kv table via API."""
    url = "http://localhost:20128/api/kv"
    
    payload = {
        "scope": scope,
        "key": key,
        "value": value
    }
    
    try:
        req = urllib.request.Request(
            url,
            method="POST",
            headers=headers,
            data=json.dumps(payload).encode()
        )
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            body = resp.read().decode()
            return status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return 0, str(e)

def main():
    print("=== Disabling Models via KV API ===")
    print(f"Models to disable: {len(MODELS_TO_DISABLE)}")
    print()
    
    # Try to update disabledModels in kv table
    disabled_list = json.dumps(MODELS_TO_DISABLE)
    
    status, body = update_kv("customModels", "disabledModels", disabled_list)
    
    print(f"API Response: HTTP {status}")
    print(f"Body: {body[:500]}")
    
    # Verify by fetching models again
    print("\n=== Verifying Changes ===")
    url = "http://localhost:20128/api/models"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print(f"Total models: {len(data['models'])}")

if __name__ == "__main__":
    main()

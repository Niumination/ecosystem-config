#!/usr/bin/env python3
"""
Generate 9router CLI auth token and disable inaccessible models.
Based on 9router-gateway-admin.md documentation.
"""
import json
import urllib.request
import urllib.error
import sys
import hashlib
from pathlib import Path

# Load credentials
machine_id = (Path.home() / ".9router" / "machine-id").read_text().strip()
cli_secret = (Path.home() / ".9router" / "auth" / "cli-secret").read_text().strip()

# Generate CLI token (same algorithm as 9router)
token = hashlib.sha256((machine_id + '9r-cli-auth' + cli_secret).encode()).hexdigest()[:16]

print(f"CLI Token: {token}")
print()

# Models to disable (from model-checker-report.md)
MODELS_TO_DISABLE = [
    # AG provider (2 failed)
    "ag/gemini-3.5-flash-high",
    "ag/gpt-oss-120b-medium",
    
    # Gemini provider (2 failed)
    "gemini/gemini-3.1-pro-preview",
    "gemini/gemini-3.7-flash",
    
    # GH provider (17 failed)
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
    
    # KR provider (29 failed)
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

def disable_model(model_id, token):
    """Disable a model in 9router via API using CLI token."""
    url = f"http://localhost:20128/api/models/{model_id}/disable"
    
    headers = {
        "x-9r-cli-token": token,
        "Content-Type": "application/json",
        "User-Agent": "hermes-agent/0.19.0"
    }
    
    try:
        req = urllib.request.Request(
            url,
            method="POST",
            headers=headers,
            data=b'{}'
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
    print("=== 9Router Model Disable Script (CLI Auth) ===")
    print(f"Models to disable: {len(MODELS_TO_DISABLE)}")
    print()
    
    success_count = 0
    fail_count = 0
    errors = []
    
    for model in MODELS_TO_DISABLE:
        status, body = disable_model(model, token)
        
        if status == 200:
            print(f"✅ {model}")
            success_count += 1
        else:
            print(f"❌ {model} (HTTP {status})")
            fail_count += 1
            errors.append(f"{model}: HTTP {status}")
    
    print()
    print("=== Summary ===")
    print(f"Success: {success_count}/{len(MODELS_TO_DISABLE)}")
    print(f"Failed: {fail_count}/{len(MODELS_TO_DISABLE)}")
    
    if errors:
        print()
        print("Errors:")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

if __name__ == "__main__":
    main()

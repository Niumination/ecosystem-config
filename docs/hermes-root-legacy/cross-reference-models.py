#!/usr/bin/env python3
"""Cross-reference model-checker results with actual catalog."""
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

# Fetch catalog
url = "http://localhost:20128/api/models"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=30) as resp:
    catalog = json.loads(resp.read().decode())

catalog_models = {m['fullModel'] for m in catalog['models']}
print(f"Total models in catalog: {len(catalog_models)}")
print()

# Model-checker results (from report)
working_from_checker = [
    "ag/gemini-3.5-flash-extra-low",
    "ag/gemini-3.5-flash-low",
    "ag/gemini-3-flash-agent",
    "ag/gemini-3-flash",
    "ag/gemini-3.1-flash-image",
    "ag/gemini-3.1-pro-low",
    "ag/gemini-3.6-flash-low",
    "ag/gemini-3.6-flash-medium",
    "ag/gemini-3.7-flash-low",
    "ag/gemini-3.7-flash-medium",
    "ag/gemini-pro-agent",
    "ag/claude-sonnet-4-6",
    "ag/claude-opus-4-6-thinking",
    "ag/gemini-3.7-flash-high",
    "gemini/gemini-3.1-flash-lite-preview",
    "gemini/gemini-3.5-flash-lite",
    "gemini/gemma-4-31b-it",
    "gemini/gemini-3-flash-preview",
    "gemini/gemini-3.6-flash",
    "gh/copilot-search-a",
    "gh/copilot-search-b",
    "gh/copilot-search-c",
    "gh/exec-agent-a",
    "gh/exec-agent-c",
    "gh/gpt-3.5-turbo-0613",
    "gh/gpt-4o-mini-2024-07-18",
    "kr/minimax-m2.5",
    "kr/claude-haiku-4.5",
    "kr/claude-sonnet-4.5",
    "kr/minimax-m2.1",
    "kr/auto",
]

failed_from_checker = [
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

print("=== Cross-Reference: Model-Checker vs Catalog ===")
print()

# Check working models from checker
print(f"Working from checker: {len(working_from_checker)}")
in_catalog_working = [m for m in working_from_checker if m in catalog_models]
not_in_catalog_working = [m for m in working_from_checker if m not in catalog_models]
print(f"  ✅ In catalog: {len(in_catalog_working)}")
print(f"  ❌ Not in catalog: {len(not_in_catalog_working)}")
if not_in_catalog_working:
    for m in not_in_catalog_working:
        print(f"     - {m}")

print()

# Check failed models from checker
print(f"Failed from checker: {len(failed_from_checker)}")
in_catalog_failed = [m for m in failed_from_checker if m in catalog_models]
not_in_catalog_failed = [m for m in failed_from_checker if m not in catalog_models]
print(f"  ✅ Still in catalog: {len(in_catalog_failed)}")
print(f"  ❌ Not in catalog: {len(not_in_catalog_failed)}")

print()
print("=== Recommendation ===")
print()
print(f"Use these {len(in_catalog_working)} verified working models:")
for m in sorted(in_catalog_working)[:10]:
    print(f"  - {m}")
if len(in_catalog_working) > 10:
    print(f"  ... and {len(in_catalog_working) - 10} more")

#!/usr/bin/env python3
"""
Create Hermes fallback config based on working models from model-checker.
This will update the hermes config.yaml to use only verified working models.
"""
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

# Working models from model-checker-report.md (the ones that passed)
WORKING_MODELS = [
    # AG (14 working)
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
    
    # Gemini (5 working)
    "gemini/gemini-3.1-flash-lite-preview",
    "gemini/gemini-3.5-flash-lite",
    "gemini/gemma-4-31b-it",
    "gemini/gemini-3-flash-preview",
    "gemini/gemini-3.6-flash",
    
    # GH (15 working - subset)
    "gh/copilot-search-a",
    "gh/copilot-search-b",
    "gh/copilot-search-c",
    "gh/exec-agent-a",
    "gh/exec-agent-c",
    "gh/gpt-3.5-turbo-0613",
    "gh/gpt-4o-mini-2024-07-18",
    
    # KR (5 working)
    "kr/minimax-m2.5",
    "kr/claude-haiku-4.5",
    "kr/claude-sonnet-4.5",
    "kr/minimax-m2.1",
    "kr/auto",
]

# Read current config
config_path = Path.home() / ".hermes" / "config.yaml"
config_content = config_path.read_text()

print("=== Current Hermes Config ===")
print()

# Show current model config
for line in config_content.splitlines():
    if 'model:' in line or 'provider:' in line or 'default:' in line or 'fallback' in line:
        print(line)

print()
print("=== Recommended Changes ===")
print()
print("Based on model-checker results, here are the verified working models:")
print()

# Categorize by use case
fast_models = [m for m in WORKING_MODELS if 'flash' in m.lower() or 'lite' in m.lower()]
reasoning_models = [m for m in WORKING_MODELS if 'opus' in m.lower() or 'pro' in m.lower()]
coding_models = [m for m in WORKING_MODELS if 'coder' in m.lower()]

print(f"**Fast models ({len(fast_models)}):**")
for m in fast_models[:5]:
    print(f"  - {m}")

print(f"\n**Reasoning models ({len(reasoning_models)}):**")
for m in reasoning_models[:5]:
    print(f"  - {m}")

print(f"\n**Coding models ({len(coding_models)}):**")
for m in coding_models:
    print(f"  - {m}")

print()
print("=== Next Steps ===")
print()
print("To update Hermes config, run:")
print("  hermes config set model.provider 9router")
print("  hermes config set model.default ag/gemini-3.5-flash-extra-low")
print()
print("Or edit ~/.hermes/config.yaml manually:")
print("  model:")
print("    provider: 9router")
print("    default: ag/gemini-3.5-flash-extra-low")

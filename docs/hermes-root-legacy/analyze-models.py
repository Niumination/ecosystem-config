#!/usr/bin/env python3
"""
Check which provider each model comes from and disable failing ones.
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

# Fetch all models
url = "http://localhost:20128/api/models"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode())

models = data['models']
print(f"Total models in catalog: {len(models)}")
print()

# Categorize by provider
providers = {}
for m in models:
    provider = m.get('provider', 'unknown')
    if provider not in providers:
        providers[provider] = []
    providers[provider].append(m['fullModel'])

print("=== Models by Provider ===")
for provider, model_list in sorted(providers.items()):
    print(f"\n{provider}: {len(model_list)} models")
    for m in sorted(model_list)[:10]:
        print(f"  - {m}")
    if len(model_list) > 10:
        print(f"  ... and {len(model_list) - 10} more")

# Find models with problematic patterns
problematic_patterns = ['thinking', 'agentic', '-high', '-pro-preview', 'trajectory', 'oswe', 'mai-code', 'gpt-4', 'gpt-5', 'gpt-3.5']
problematic_models = []

for m in models:
    model_id = m['fullModel']
    if any(pattern in model_id.lower() for pattern in problematic_patterns):
        problematic_models.append(model_id)

print(f"\n=== Potentially Problematic Models ({len(problematic_models)}) ===")
for m in sorted(problematic_models)[:20]:
    print(f"  - {m}")

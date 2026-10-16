#!/usr/bin/env python3
"""Explore 9router models API structure."""
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

# Fetch models
url = "http://localhost:20128/api/models"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode())

print("=== 9Router Models API Structure ===")
print()

# Check top-level keys
print("Top-level keys:", list(data.keys())[:20])
print()

# Check if there's a models list
if 'models' in data:
    print(f"Total models: {len(data['models'])}")
    # Show first model structure
    if data['models']:
        print("\nFirst model structure:")
        print(json.dumps(data['models'][0], indent=2)[:500])
elif 'data' in data:
    print(f"Total models: {len(data['data'])}")
    if data['data']:
        print("\nFirst model structure:")
        print(json.dumps(data['data'][0], indent=2)[:500])

# Check for disabled models field
if 'disabledModels' in data or 'disabled' in data:
    print("\nDisabled models found!")
    print(json.dumps(data.get('disabledModels', data.get('disabled', [])), indent=2)[:500])

# Save full response for analysis
with open("/tmp/9router-models.json", "w") as f:
    json.dump(data, f, indent=2)
print("\nFull response saved to /tmp/9router-models.json")

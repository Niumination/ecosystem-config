#!/usr/bin/env python3
"""Explore 9router API structure to find model disable endpoint."""
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

# Try different endpoints
endpoints = [
    "/api/models",
    "/api/v1/models",
    "/api/provider-nodes",
    "/api/providers",
    "/api/connections",
    "/api/settings",
]

print("=== Exploring 9router API Endpoints ===")
print()

for ep in endpoints:
    try:
        url = f"http://localhost:20128{ep}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode()
            print(f"✅ {ep}: {resp.status}")
            if len(data) < 500:
                print(f"   Response: {data[:200]}")
            else:
                print(f"   Response length: {len(data)} chars")
    except Exception as e:
        print(f"❌ {ep}: {e}")

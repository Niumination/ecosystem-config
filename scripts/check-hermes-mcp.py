#!/usr/bin/env python3
"""Read Hermes config and check for MCP entries."""
import os

hermes_dir = os.path.expanduser('~/.hermes')
config_path = os.path.join(hermes_dir, 'config.yaml')

# Check if MCP dir exists
mcp_dir = os.path.join(hermes_dir, 'mcp')
if os.path.isdir(mcp_dir):
    print(f'MCP dir exists: {mcp_dir}')
    for f in os.listdir(mcp_dir):
        print(f'  {f}')
else:
    print(f'MCP dir not found at {mcp_dir}')

# Read config
with open(config_path) as f:
    content = f.read()
    print(f'\nConfig file ({len(content)} bytes)')
    
# Show mcp-related sections
for line in content.split('\n'):
    if 'mcp' in line.lower() or 'uacc' in line.lower():
        print(f'  {line}')

# Check for MCP config in other locations
opencode_mcp = os.path.expanduser('~/.config/opencode/opencode.json')
if os.path.isfile(opencode_mcp):
    import json
    with open(opencode_mcp) as f:
        oc = json.load(f)
    if 'mcp' in oc:
        print(f'\nOpenCode MCP config: {json.dumps(oc["mcp"], indent=2)}')

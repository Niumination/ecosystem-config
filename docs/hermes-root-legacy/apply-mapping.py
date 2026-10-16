#!/usr/bin/env python3
"""Apply new model mapping to config.yaml."""
from pathlib import Path
import yaml

config_path = Path.home() / '.hermes' / 'config.yaml'
config = yaml.safe_load(config_path.read_text())

# 1. Update DM main model to huancheng/auto
config['model'] = {
    'provider': 'huancheng',
    'default': 'auto',
    'base_url': 'https://api.hcnsec.cn/v1',
    'api_mode': 'codex_responses'
}

# 2. Update thread overrides
config['platforms']['telegram']['channel_overrides'] = {
    '1': {
        'model': 'ag/gemini-3.5-flash-low',
        'provider': '9router'
    },
    '802': {
        'model': 'ag/gemini-3-flash-agent',
        'provider': '9router'
    },
    '803': {
        'model': 'gh/gpt-4o-mini',
        'provider': '9router'
    },
    '804': {
        'model': 'ag/gemini-3.7-flash-low',
        'provider': '9router'
    },
    '1172': {
        'model': 'gemini/gemma-4-31b-it',
        'provider': '9router'
    }
}

# 3. Update fallback chain
config['fallback_providers'] = [
    {'provider': '9router', 'model': 'ag/gemini-3.5-flash-low'},
    {'provider': '9router', 'model': 'ag/gemini-3-flash-agent'},
    {'provider': 'opencode-zen', 'model': 'hy3-free'}
]

# Save
config_path.write_text(yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False))
print("✅ Config updated successfully!")
print("\nNew mapping:")
print(f"  DM: huancheng/auto")
print(f"  Thread 1: ag/gemini-3.5-flash-low (9router)")
print(f"  Thread 802: ag/gemini-3-flash-agent (9router)")
print(f"  Thread 803: gh/gpt-4o-mini (9router)")
print(f"  Thread 804: ag/gemini-3.7-flash-low (9router)")
print(f"  Thread 1172: gemini/gemma-4-31b-it (9router)")
print(f"\nFallback: 9router/gemini-3.5-flash-low → 9router/gemini-3-flash-agent → opencode-zen/hy3-free")

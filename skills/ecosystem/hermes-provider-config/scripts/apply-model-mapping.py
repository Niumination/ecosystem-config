#!/usr/bin/env python3
"""
Apply model mapping to hermes config.yaml.
Updates: DM model, thread channel_overrides, fallback chain.
"""
from pathlib import Path
import yaml
import sys

def main():
    config_path = Path.home() / '.hermes' / 'config.yaml'

    # Backup first
    import shutil
    from datetime import datetime
    backup_path = config_path.parent / f'config.yaml.bak-before-model-mapping-{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    shutil.copy2(config_path, backup_path)
    print(f"Backup: {backup_path}")

    # Load
    config = yaml.safe_load(config_path.read_text())

    # 1. DM model → huancheng/auto
    config['model'] = {
        'provider': 'huancheng',
        'default': 'auto',
        'base_url': 'https://api.hcnsec.cn/v1',
        'api_mode': 'codex_responses'
    }

    # 2. Thread overrides
    config['platforms']['telegram']['channel_overrides'] = {
        '1': {'model': 'ag/gemini-3.5-flash-low', 'provider': '9router'},
        '802': {'model': 'ag/gemini-3-flash-agent', 'provider': '9router'},
        '803': {'model': 'gh/gpt-4o-mini', 'provider': '9router'},
        '804': {'model': 'ag/gemini-3.7-flash-low', 'provider': '9router'},
        '1172': {'model': 'gemini/gemma-4-31b-it', 'provider': '9router'}
    }

    # 3. Fallback chain
    config['fallback_providers'] = [
        {'provider': '9router', 'model': 'ag/gemini-3.5-flash-low'},
        {'provider': '9router', 'model': 'ag/gemini-3-flash-agent'},
        {'provider': 'opencode-zen', 'model': 'hy3-free'}
    ]

    # Save
    config_path.write_text(yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False))

    print("✅ Config applied!")
    print("\nNew mapping:")
    print(f"  DM: {config['model']['provider']}/{config['model']['default']}")
    for tid, conf in config['platforms']['telegram']['channel_overrides'].items():
        print(f"  Thread {tid}: {conf['provider']}/{conf['model']}")
    print("\nFallback:")
    for i, fb in enumerate(config['fallback_providers'], 1):
        print(f"  L{i}: {fb['provider']}/{fb['model']}")

if __name__ == '__main__':
    main()

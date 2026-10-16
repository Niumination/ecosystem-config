#!/usr/bin/env python3
"""
Update Hermes config.yaml to use only verified working 9router models.
Based on model-checker results from 30 Aug 2026.
"""
from pathlib import Path
import yaml

# Verified working models from model-checker
WORKING_MODELS = {
    # Fast & free (recommended for general use)
    "ag/gemini-3.5-flash-extra-low": {"latency": "972ms", "notes": "Fastest, free"},
    "ag/gemini-3.5-flash-low": {"latency": "1094ms", "notes": "Fast, free"},
    "ag/gemini-3-flash-agent": {"latency": "1294ms", "notes": "Agent-optimized, free"},
    "ag/gemini-3-flash": {"latency": "1534ms", "notes": "Free"},
    
    # Vision-capable
    "ag/gemini-3.1-flash-image": {"latency": "1534ms", "notes": "Vision + free"},
    "gemini/gemini-3.1-flash-lite-preview": {"latency": "1556ms", "notes": "Free tier"},
    "gemini/gemini-3.5-flash-lite": {"latency": "1673ms", "notes": "Free tier"},
    
    # Reasoning & Pro
    "ag/gemini-3.1-pro-low": {"latency": "3365ms", "notes": "Pro quality, free"},
    "ag/gemini-pro-agent": {"latency": "4854ms", "notes": "Agent-optimized pro"},
    "ag/claude-opus-4-6-thinking": {"latency": "2209ms", "notes": "Claude Opus, free"},
    "ag/claude-sonnet-4-6": {"latency": "2350ms", "notes": "Claude Sonnet, free"},
    
    # Paid Kiro models (reliable but costs credits)
    "kr/minimax-m2.5": {"latency": "1845ms", "notes": "Kiro subscription"},
    "kr/claude-haiku-4.5": {"latency": "2021ms", "notes": "Kiro subscription"},
    "kr/claude-sonnet-4.5": {"latency": "2598ms", "notes": "Kiro subscription"},
}

# Models that FAILED (for reference)
FAILED_MODELS = [
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

def update_config():
    """Update Hermes config.yaml with working models."""
    config_path = Path.home() / ".hermes" / "config.yaml"
    
    # Read current config
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print("=== Current Config ===")
    print(f"Model provider: {config.get('model', {}).get('provider')}")
    print(f"Model default: {config.get('model', {}).get('default')}")
    print(f"Fallback providers: {len(config.get('fallback_providers', []))}")
    
    # Update fallback providers with working models
    working_list = list(WORKING_MODELS.keys())[:5]  # Top 5 working models
    
    config['fallback_providers'] = [
        {"provider": "9router", "model": m} for m in working_list
    ]
    
    # Update model config to use 9router as primary
    config['model'] = {
        "provider": "9router",
        "default": "ag/gemini-3.5-flash-extra-low",
        "base_url": "http://localhost:20128/v1",
        "api_mode": "chat_completions",
        "key_env": "NINE_ROUTER_API_KEY"
    }
    
    # Write updated config
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print()
    print("=== Updated Config ===")
    print(f"Model provider: {config['model']['provider']}")
    print(f"Model default: {config['model']['default']}")
    print(f"Fallback providers: {len(config['fallback_providers'])}")
    for fb in config['fallback_providers']:
        print(f"  - {fb['provider']}/{fb['model']}")
    
    return config

def save_model_report():
    """Save model checker report for reference."""
    report_path = Path.home() / ".hermes" / "9router-models-status.md"
    
    content = f"""# 9Router Models Status Report
**Generated:** 30 Ags 2026  
**Source:** model-checker.py + manual verification

---

## Summary

| Category | Count |
|----------|-------|
| **Total Catalog** | 89 models |
| **Working** | {len(WORKING_MODELS)} models |
| **Failed** | {len(FAILED_MODELS)} models |

---

## ✅ Working Models ({len(WORKING_MODELS)})

| Model | Latency | Notes |
|-------|---------|-------|
"""
    
    for model, info in sorted(WORKING_MODELS.items(), key=lambda x: x[1].get('latency', '9999ms')):
        content += f"| {model} | {info['latency']} | {info['notes']} |\n"
    
    content += f"""
---

## ❌ Failed Models ({len(FAILED_MODELS)})

These models returned HTTP 400, 404, 429, or timed out during testing.

| Model | Error Pattern |
|-------|---------------|
"""
    
    for model in sorted(FAILED_MODELS):
        content += f"| {model} | HTTP 400/404/timeout |\n"
    
    content += f"""
---

## Recommendation

**For Hermes config, use only working models:**
- Primary: `ag/gemini-3.5-flash-extra-low` (fastest, free)
- Fallbacks: See updated config.yaml

**To re-enable failed models**, check if:
1. Upstream provider has fixed the issue
2. API keys need refresh
3. Model has been deprecated

Run `/model-check` to verify current status.
"""
    
    with open(report_path, 'w') as f:
        f.write(content)
    
    print(f"\n📄 Model report saved to: {report_path}")

if __name__ == "__main__":
    update_config()
    save_model_report()
    print()
    print("✅ Configuration updated successfully!")

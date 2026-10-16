# Summary — Model Mapping Update 29 Ags 2026

## Changes Applied
1. DM default: agentrouter/glm-5.3 → huancheng/auto
2. Thread 1: gemini-3.5-flash-lite → ag/gemini-3.5-flash-low (729ms)
3. Thread 802: gc/gemini-2.5-pro → ag/gemini-3-flash-agent (966ms)
4. Thread 803: cf/deepseek-r1-distill-qwen-32b → gh/gpt-4o-mini (930ms)
5. Thread 804: cf/glm-4.7-flash → ag/gemini-3.7-flash-low (2483ms)
6. Thread 1172: gemini/gemma-4-31b-it (UNCHANGED)
7. Fallback: opencode-zen single → 9router×2 + opencode-zen×1

## Test Results
- All recommended models: 10/10 burst success
- 9router: PRIMARY (fastest + most stable)
- huancheng: DM only (auto resolves to agnes-2.5-flash)
- opencode-zen: LIMITED (only hy3-free stable)

## Files Updated
- ~/.hermes/config.yaml (applied)
- ~/.hermes/skills/autonomous-ai-agents/telegram-router-orchestration/SKILL.md (patched)
- ~/.hermes/skills/ecosystem/hermes-provider-config/references/provider-sweep-2026-08-29.md (new)
- ~/.hermes/skills/ecosystem/hermes-provider-config/references/model-mapping-report-2026-08-29.md (new)

## Backup
- ~/.hermes/config.yaml.bak-before-model-mapping-20260829_*.yaml

## Next Actions
- Monitor thread performance 24-48h
- Re-test monthly or if quota changes
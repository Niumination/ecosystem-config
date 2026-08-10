# OmniRoute — Reference Study

**Repo:** https://github.com/diegosouzapw/OmniRoute
**Stars:** 44.9k | **Forks:** 6k | **License:** MIT | **Contributors:** 500+

## What It Is
Free MIT AI gateway: one endpoint, 290+ providers (90+ free), 500+ models. Works with Claude Code, Codex, Cursor, OpenCode, Cline & Copilot.

## Core Features
- **Quota-aware auto-fallback** — rotates across providers when one hits limit
- **RTK + Caveman compression** — saves 15-95% tokens
- **MCP/A2A support** — agent protocol compatibility
- **Desktop/PWA** — GUI + CLI
- **Sticky round-robin combos** — consistent routing

## Supported Providers (partial)
Kimi, Claude, GPT, OpenAI, Gemini, GLM, DeepSeek, MiniMax, and 290+ more

## Architecture Pattern
- providers/ : 290+ provider adapters
- routes/ : quota-aware routing
- compression/ : RTK + Caveman
- mcp/ : MCP server integration
- a2a/ : Agent-to-Agent protocol
- desktop/ : Electron/PWA GUI

## Relevance to Our Ecosystem
- **Model routing**: quota-aware auto-fallback = exactly what we need for 9Router + huancheng multi-provider setup
- **Compression**: RTK+Caveman token savings could extend our limited context windows
- **MCP/A2A**: standardized agent protocols = future-proofing Hermes integration
- **One endpoint**: simplifies client code — same pattern as our base_url abstraction in Hermes config
- **Open source + MIT**: can self-host instead of relying on commercial gateway

## Status
Reference only. High potential for replacing/improving our current 9Router routing layer.

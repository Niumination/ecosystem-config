# Agent Reach — Reference Study

**Repo:** https://github.com/Panniantong/Agent-Reach
**Stars:** 70.2k | **Forks:** 5.9k | **License:** MIT

## What It Is
Open-source **capability layer** that gives AI agents internet access — read/search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, Facebook, Instagram via one CLI, zero API fees.

## Core Value Proposition
- Solves the "agent can't reach the internet" problem
- Each platform = ordered primary + fallback backend list
- Auto doctor/health-check per channel
- Cookie/auth only stored locally, never uploaded
- Compatible with Claude Code, OpenClaw, Cursor, Windsurf

## Architecture Pattern
```
Agent Reach CLI
  ├── channels/           # Platform modules
  │   ├── web.py          → Jina Reader
  │   ├── twitter.py      → twitter-cli ▸ OpenCLI ▸ bird
  │   ├── youtube.py      → yt-dlp
  │   ├── github.py       → gh CLI
  │   ├── bilibili.py     → bili-cli ▸ OpenCLI
  │   ├── reddit.py       → OpenCLI ▸ rdt-cli
  │   ├── facebook.py     → OpenCLI
  │   ├── instagram.py    → OpenCLI
  │   └── xiaohongshu.py  → OpenCLI/MCP/cookie
  ├── lib/                # Core routing + probe
  ├── config/             # Per-channel backend override
  └── SKILL.md            # Agent-readable skill doc
```

## Key Design Decisions
1. **Capability layer, not wrapper** — Agent calls upstream tools directly; no middleman
2. **Ordered backend routing** — swap implementations without code changes
3. **doctor --json** — proactive health check before acting
4. **Local-only cookies** — privacy-first auth model
5. **SKILL.md trigger-first** — written for agents to read, not humans

## Relevance to Our Ecosystem
- **Research agent feeds**: Mission Control research thread (802) can use this for web/social intelligence
- **Data mining**: Pemdi operational data can be enriched from public sources
- **Content automation**: Agency output layer can pull from YouTube/Reddit/Twitter
- **Pattern reuse**: ordered backend routing = same pattern we could use for model/provider fallbacks

## Status
Reference only — no integration planned yet. File saved for future architecture review.

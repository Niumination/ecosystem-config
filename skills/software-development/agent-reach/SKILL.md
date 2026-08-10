---
name: agent-reach
description: "Internet capability layer for AI agents. Use when the agent needs to read/search web pages, YouTube, GitHub, RSS, or other platforms. Trigger words: search the web, read this URL, check GitHub repo, get YouTube transcript, monitor RSS, internet research."
version: "1.0.0"
---

# Agent Reach — Internet Capability Layer

## When to Use
- User asks to read/check a web page or URL
- User asks to search the internet
- User asks about YouTube video content/transcript
- User asks to check GitHub repo/issues/PRs
- User asks to monitor RSS feeds
- Research task needs current internet data

## Commands

### web
Read any web page and return clean markdown text.
```bash
agent-reach web <url>
```

### youtube
Get transcript/summary from YouTube video.
```bash
agent-reach youtube <url>
```

### github
Read GitHub repo info, issues, PRs.
```bash
agent-reach github <owner/repo>
# or with specific query:
agent-reach github <owner/repo> --issues
agent-reach github <owner/repo> --prs
```

### rss
Read RSS/Atom feed and return items.
```bash
agent-reach rss <feed-url>
```

## Output Format
All commands return JSON to stdout:
```json
{
  "platform": "web|youtube|github|rss",
  "url": "<input>",
  "status": "ok|error|timeout",
  "data": {
    "title": "...",
    "content": "...",
    "summary": "..."
  },
  "raw": "...",
  "meta": {
    "backend": "jina|yt-dlp|gh|feedparser",
    "latency_ms": 1234
  }
}
```

## Fallback Chain
If `agent-reach` CLI fails:
1. **Web**: `curl -s "https://r.jina.ai/<url>"`
2. **YouTube**: `yt-dlp --dump-json <url>`
3. **GitHub**: `gh repo view <owner/repo>` or `gh search repos <query>`
4. **RSS**: `python3 -c "import feedparser; ..."`

## Error Handling
- CLI not found → tell user to run `agent-reach install --env=auto`
- Timeout > 30s → return partial data with `status: "timeout"`
- Platform error → return `status: "error"` with message + suggest fallback
- Network error → return `status: "error"` with message

## Notes
- Zero-config platforms only: web, YouTube, GitHub, RSS
- Login-required platforms (Twitter, Reddit, etc.) are NOT configured yet
- Agent should parse JSON output and present results to user in natural language
- For long content, summarize key points rather than dumping full text

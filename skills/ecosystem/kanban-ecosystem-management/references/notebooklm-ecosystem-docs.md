# NotebookLM Ecosystem Documentation

Use **Google NotebookLM** as an AI-augmented documentation surface for the Niumination ecosystem. Notebooks give you a queryable knowledge base from source documents — useful for rapid research, cross-referencing, and onboarding.

## Workflow

1. **Create notebook** — `nlm notebook create --title "Niumination Ecosystem"`
2. **Add 3 core source groups** to cover the ecosystem comprehensively:

   | Source type | What to add | Examples |
   |-------------|-------------|----------|
   | Project guidelines | AGENTS.md local file | `file:///Users/zaryu/Desktop/Niumination/AGENTS.md` |
   | Master backlog | BACKLOG.md local file | `file:///Users/zaryu/Desktop/Niumination/BACKLOG.md` |
   | Live URLs | Deployed project pages | kune-ya.com, PemdiAcehTengah.pages.dev, etc. |

3. **Source addition via nlm CLI:**
   ```bash
   # File sources (text/PDF)
   nlm notebook add-source <notebook-id> --file /path/to/file.md

   # URL sources (web pages, YouTube)
   nlm notebook add-source <notebook-id> --url https://example.com

   # URL sources that fail via CLI may work via the GitHub README URL
   # (e.g. https://github.com/Niumination/<repo> index page)
   ```

4. **Query the notebook** for cross-project insights, status summaries, or research.

## Source Selection Heuristics

| If user wants... | Add these sources |
|-----------------|-------------------|
| Full ecosystem overview | AGENTS.md + BACKLOG.md + top 8 live URLs |
| Specific domain project | That project's GitHub README + live URL |
| Cross-project research | All projects in that domain + AGENTS.md guidelines |
| New notebook for a pair of projects | AGENTS.md excerpt (relevant section) + both projects' URLs + BACKLOG.md excerpt |

## CLI Tips

- **File path must be absolute** — `nlm` resolves relative to CWD, but the MCP tool sends absolute. Use `read_file` to verify content first.
- **URL source can fail** — Some sites (GH Pages, SPA apps) return HTML that NotebookLM can't parse. Fallback: add the GitHub repo's README page URL instead of the live deploy URL.
- **Duplicates** — Adding the same URL twice creates duplicate sources. Check `nlm notebook get <id>` before re-adding.
- **Processing wait** — Large files (AGENTS.md, BACKLOG.md) take 5-15 seconds to process. `--wait` flag blocks until ready. Without it, verify readiness before querying.

## Known Limitations

- **YouTube URLs** — Must be public (unlisted works). Private videos fail silently.
- **GH Pages SPAs** — Single-page apps that load content via JS may only capture the index.html shell. Prefer the GitHub repo README URL for these.
- **Rate limits** — NotebookLM has undocumented rate limits on queries. If you get a 429 or timeout, wait 30s and retry with a shorter query.

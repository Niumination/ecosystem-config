# Alternative Project Management Tools (Niumination Ecosystem)

When the Hermes kanban DB is corrupt, unavailable, or you want a persistent project tracker outside the agent's ephemeral DB, these alternatives exist in the current toolchain:

## 1. Linear (skill: `linear`)

**Type:** Issue tracker / project management (GraphQL API via curl)

| Aspect | Detail |
|--------|--------|
| **Strength** | Fast, keyboard-driven, great for software projects |
| **Weakness** | Requires Linear account + API key; Niumination doesn't have one yet |
| **Setup** | `LINEAR_API_KEY` in env → curl-based tooling works |
| **Use case** | Sprint tracking for active coding projects (TEDEO, kune-ya.com) |

## 2. Airtable (skill: `airtable`)

**Type:** Spreadsheet-database hybrid (REST API via curl)

| Aspect | Detail |
|--------|--------|
| **Strength** | Flexible schema, kanban/spreadsheet/gallery views, can embed in dashboards |
| **Weakness** | API rate limits on free tier; requires Airtable base setup |
| **Setup** | `AIRTABLE_API_KEY` + base ID in env |
| **Use case** | Portfolio register (all 66 repos + metadata) — better than kanban for filtering/sorting |

## 3. Notion (skill: `notion` + `ntn` CLI)

**Type:** All-in-one workspace with databases

| Aspect | Detail |
|--------|--------|
| **Strength** | Rich databases, linked views, mobile access, already familiar |
| **Weakness** | Notion API rate limits; `ntn` CLI needs token setup |
| **Setup** | `NOTION_TOKEN` in env + page/database IDs |
| **Use case** | Living project portfolio with status, timeline, and notes — AGENTS.md replacement |

## 4. Obsidian / brain/ (existing vault)

**Type:** Local markdown vault with git sync

| Aspect | Detail |
|--------|--------|
| **Strength** | Already exists at `~/Desktop/Niumination/brain/`, dataview queries, git-tracked |
| **Weakness** | No native API; requires Obsidian plugin setup for automation |
| **Setup** | Already configured — add dataview queries |
| **Use case** | Personal task tracking that survives USB disconnects and Hermes reset |

## 5. Niu-Kanban Dash rebuild (custom)

**Type:** Self-hosted React dashboard

| Aspect | Detail |
|--------|--------|
| **Strength** | Full control, already has the code base, can switch data source |
| **Weakness** | Requires maintenance; current DB corrupt |
| **Setup** | Change `server.js` DB source from corrupt kanban.db to JSON/YAML files or Supabase |
| **Use case** | Visual dashboard that always works — switch to file-based persistence |

## Decision Matrix

| Criteria | Linear | Airtable | Notion | Obsidian | Niu-Dash |
|----------|--------|----------|--------|----------|----------|
| Already configured | ❌ | ❌ | ❌ | ✅ | ✅ |
| Survives Hermes reset | ✅ | ✅ | ✅ | ✅ | ❌ (tied to DB) |
| Mobile accessible | ✅ | ✅ | ✅ | ✅ (sync) | ❌ |
| API available | ✅ | ✅ | ✅ | ❌ (plugin) | ✅ |
| SQL-like query | ❌ | ✅ | ❌ | ✅ (dataview) | ❌ |
| Visual kanban | ✅ | ✅ | ✅ | ✅ | ✅ |

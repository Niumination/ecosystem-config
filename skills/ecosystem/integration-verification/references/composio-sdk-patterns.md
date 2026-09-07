# Composio SDK Patterns — Verified
**Date:** 2026-09-04  
**SDK:** `composio` Python package v0.21.0  
**Auth:** Bearer API key via `vault/composio-key.md`  
**Org:** `zhallbay28-5351b229` (`6d073d32-...`)

## Verified Patterns

### Init
```python
from composio import Composio
with open('vault/composio-key.md') as f:
    api_key = f.readline().strip().split('=',1)[1]
c = Composio(api_key=api_key)
```

### List connected accounts
```python
accounts = c.connected_accounts.list()
for a in accounts.items:
    print(a.toolkit.slug, a.status)
```
- Returns `ConnectedAccountListResponse`
- Status values: `ACTIVE`, `EXPIRED`
- `toolkit` is `ItemToolkit(slug=..., name=...)`

### Create session
```python
session = c.sessions.create(user_id='afrizal_munthe')
print(session.session_id)
```
- Returns `ToolRouterSession`
- Session ID starts with `trs_`
- Keyword is `user_id`, not `toolkit`

### List tools for workflow
```python
tools = session.tools()
for t in tools:
    fn = t.get('function', {})
    print(fn.get('name'))
```
- Returns `list[dict]`
- Each dict has `function.name` and `function.description`
- Available tool names include:
  - `COMPOSIO_SEARCH_TOOLS`
  - `COMPOSIO_MULTI_EXECUTE_TOOL`
  - `COMPOSIO_GET_TOOL_SCHEMAS`
  - `COMPOSIO_MANAGE_CONNECTIONS`
  - `COMPOSIO_REMOTE_BASH_TOOL`
  - `COMPOSIO_REMOTE_WORKBENCH`

### Discover Gmail tools
```python
# Search first
result = session.execute('COMPOSIO_SEARCH_TOOLS', {
    'queries': [{'use_case': 'fetch Gmail emails'}],
    'session': {'id': session.session_id}
})
# Then get schemas
session.execute('COMPOSIO_GET_TOOL_SCHEMAS', {
    'tool_slugs': ['GMAIL_SEARCH_EMAILS'],
    'session': {'id': session.session_id}
})
```

## Gotchas
- `c.toolkits.list()` returns `ToolkitListResponse`; use `.items` for iteration.
- `len(toolkits)` fails; use `len(toolkits.items)`.
- `c.toolkits.get_tools(toolkit='gmail')` raises `AttributeError`; use session tools instead.
- Direct `session.execute` requires correct tool_slug from search results.

# Hermes Log Cleanup — 2026-09-02

**Operator:** Afrizal Munthe  
**Gateway restart:** 2026-09-02 15:34 WIB (PID 46480/46481)  
**Status:** ✅ Verified post-restart

## 1. Masalah
- `errors.log` 2.757 warning/error (5.674 baris), 46% = `niu-fence.py: command not found`, 15% = `MCP hermes-* / time Connection closed`
- Penyebab: sisa konstitusi ekosistem (hook di `/Volumes/HermesAgent/...` yang sudah tidak ada) + MCP server tanpa backend

## 2. Fix diterapkan
| Area | Before | After | File |
|------|--------|-------|------|
| hooks | 3 command `/Volumes/.../niu-*.py` | `hooks: {pre_tool_call: [], pre_llm_call: [], on_session_end: []}` | `~/.hermes/config.yaml:454` |
| hooks_auto_accept | true | true (tetap) | — |
| mcp_servers.hermes-postgres | enabled: true | **enabled: false** | `~/.hermes/config.yaml:592` |
| mcp_servers.hermes-sqlite | enabled: true | **enabled: false** | `~/.hermes/config.yaml:597` |
| mcp_servers.time | enabled: true | **enabled: false** | `~/.hermes/config.yaml:602` |
| mcp_servers.filesystem/github/context7 | enabled: true | tetap true | — |

Validasi: `hermes config check` → Config version: 38 ✓

## 3. Verifikasi post-restart
- `tail -100 errors.log | grep "shell hook failed"` → 0
- MCP errors after 15:34 → 0 (3 baris di tail -200 semua timestamp 15:32, sebelum restart)
- Gateway: `ai.hermes.gateway.plist` supervised, PID 46481

## 4. Rotasi log
- `errors.log` (814K, 6.184 baris) → `errors.log.archive-2026-09-02-pre-fix`
- `errors.log` baru 0B per 15:37 WIB (gateway akan isi otomatis)

## 5. Sisa warning (expected, bukan error config)
- `InternalServerError 500` opencode-free/muse-spark-1.2 — upstream
- `Unknown browser engine 'local'` → fallback auto
- `env passthrough blocked` → GHSA-rhgp protection

## Bukti
```
grep -A5 "^hooks:" ~/.hermes/config.yaml
# hooks:
#   pre_tool_call: []
#   pre_llm_call: []
#   on_session_end: []

grep -A4 "hermes-postgres:\|hermes-sqlite:\|  time:" ~/.hermes/config.yaml
# enabled: false (ketiganya)
```

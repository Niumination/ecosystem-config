# 05 — Dependency Map Hermes Ecosystem

> Peta dependensi antar komponen Hermes — untuk memastikan urutan migrasi yang benar.

---

## Layer Dependency (Top → Bottom)

```
┌─────────────────────────────────────────────────────────┐
│                     TELEGRAM GATEWAY                      │
│  (user-facing — tergantung semua layer di bawahnya)      │
├─────────────────────────────────────────────────────────┤
│                    HERMES AGENT CLI                       │
│  (hermes command — tergantung config + state)            │
├─────────────────────────────────────────────────────────┤
│                    CONFIGURATION                          │
│  config.yaml ──→ .env ──→ auth.json ──→ SOUL.md          │
│  │                                                       │
│  ├── providers (API keys dari .env)                      │
│  ├── mcp_servers (paths ke binary/script)                │
│  ├── cron (script paths)                                 │
│  ├── plugins (nama plugin)                               │
│  └── skills (direktori skills/)                          │
├─────────────────────────────────────────────────────────┤
│                       STATE LAYER                        │
│  state.db ──── kanban.db ──── sessions/ ──── memories/   │
│  │                                                       │
│  ├── state.db: session history, user prefs, agent state  │
│  ├── kanban.db: tasks, lanes, dispatch queue             │
│  ├── sessions/: individual session transcripts           │
│  └── memories/: MEMORY.md + USER.md                      │
├─────────────────────────────────────────────────────────┤
│                    RUNTIME LAYER                          │
│  scripts/ ──── plugins/ ──── bin/ ──── lsp/              │
│  │                                                       │
│  ├── scripts/: 12 custom cron scripts                    │
│  ├── plugins/: spotify, rtk-rewrite, achievements        │
│  ├── bin/tirith: security policy engine                  │
│  └── lsp/: language server support                       │
├─────────────────────────────────────────────────────────┤
│                    EXTERNAL LAYER                         │
│  MCP servers ──── Homebrew ──── npm global ──── pip      │
│  │                                                       │
│  ├── mcp-server-time (pip binary)                        │
│  ├── server-github (npx package)                         │
│  ├── mcp-server-filesystem (brew/homebrew)               │
│  ├── mcp-server-sqlite.py (custom script)                │
│  ├── mcp-server-postgres.sh (custom script)              │
│  └── ponytail (Node.js MCP, di Niumination repo)         │
└─────────────────────────────────────────────────────────┘
```

---

## Dependency Matrix

| Komponen | Bergantung Pada | Dipakai Oleh |
|----------|----------------|--------------|
| **Gateway** | config.yaml, state.db, .env, auth.json | Telegram user |
| **CLI** | config.yaml, skills/, MCP servers | Gateway, Terminal |
| **config.yaml** | .env (API keys), _config_version | Semua layer |
| **.env** | — (file independen) | providers, MCP, gateway |
| **auth.json** | — (file independen) | Layanan eksternal |
| **state.db** | — (SQLite file) | Session, memories, history |
| **kanban.db** | — (SQLite file) | Task management |
| **sessions/** | state.db (index) | Session history |
| **memories/** | state.db (index) | Memory injection |
| **skills/** | SKILL.md files | Agent behavior |
| **scripts/** | PATH config | Cron jobs, codebase intelligence |
| **codebase/** | scripts/codebase/*.py | Graphify + Serena for agent code understanding |
| **plugins/** | Hermes plugin API | Agent toolsets |
| **bin/tirith** | Binary file | Security enforcement |
| **MCP servers** | Python/Node/Brew | Agent tools |
| **cron jobs** | scripts/, skills/ | Scheduled tasks |
| **home/** | — (runtime cache) | node_modules, pip cache |

---

## Migration Order (Topological Sort)

Berdasarkan dependency map di atas, urutan migrasi yang benar:

```
STEP 1:  Install Hermes binary (native)                ← independent
STEP 2:  Copy config.yaml + .env + auth.json           ← independent files
STEP 3:  Copy state.db + kanban.db                     ← independent DB files
STEP 4:  Copy memories/                                ← depends on state.db
STEP 5:  Copy skills/ + scripts/ + codebase/ + plugins/ ← independent
STEP 6:  Copy sessions/ + checkpoints/                 ← nice-to-have
STEP 7:  Update paths di config.yaml                   ← depends on STEP 1-2
STEP 8:  Install/verify MCP servers                    ← depends on STEP 2,7
STEP 9:  Test CLI (hermes command)                     ← depends on STEP 1-8
STEP 10: Test MCP servers                              ← depends on STEP 8-9
STEP 11: Start gateway                                 ← depends on STEP 1-10
STEP 12: Test Telegram                                 ← depends on STEP 11
```

**Kesalahan umum:** Memulai gateway (STEP 11) sebelum MCP server path diupdate (STEP 7-8) → MCP error.

---

## Circular Dependencies (⚠️ Perhatian)

Tidak ada circular dependency dalam Hermes sendiri. Tapi ada **runtime coupling**:

```
state.db ──→ sessions/ ──→ state.db
```
Sessions diindex di state.db, tapi file session disimpan di sessions/. Jika salah satu corrupt, session history bisa broken tapi agent tetap bisa jalan.

```
config.yaml ──→ cron ──→ scripts/ ──→ config.yaml
```
Cron job path mengacu ke scripts/. Script path di config HARUS match dengan direktori.

---

## Komponen yang Bisa Di-Skip Saat Migrasi

| Komponen | Size | Alasan Skip |
|----------|------|-------------|
| `home/` | 12 GB | Cache + node_modules — recreate otomatis |
| `lsp/node_modules/` | ~350 MB | Auto-install by Hermes LSP |
| `kanban/` (workers) | 1.3 GB | Worker logs — restart workers |
| `logs/` | 34 MB | Rotate otomatis — history lama ga kritis |
| `cache/` | 96 KB | Auto-populate |
| `sandboxes/` | — | Auto-create |
| `audio_cache/` | — | Auto-populate |
| `image_cache/` | — | Auto-populate |

---

## Port Dependencies

| Service | Port | Dipakai Untuk |
|---------|------|---------------|
| Gateway API | 5199 | Kanban server dashboard |
| Kanban server | 5199 | (sama) |
| (none other) | — | Gateway tidak expose port lain |

Jika gateway pindah native, port 5199 tetap sama — tidak ada konflik dengan portable karena portable akan dimatikan.

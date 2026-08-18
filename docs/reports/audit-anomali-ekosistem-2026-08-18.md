# 🔍 Audit Anomali Ekosistem — Niumination + Hermes

| Field | Nilai |
|---|---|
| **Tanggal** | 18 Agustus 2026 (WIB) |
| **Metode** | Scan 45 repo git, secret scan, proses/port, cron, config YAML, MCP, skill plane, deploy canary, filesystem |
| **Status** | Laporan hanya — TIDAK ada perubahan yang dilakukan |

---

## Ringkasan

**22 anomali** ditemukan dalam 4 kategori: 4 kritis (P0), 8 tinggi (P1), 7 sedang (P2), 3 info.

---

## 🔴 KRITIS (P0)

| # | Anomali | Bukti |
|---|---------|-------|
| A1 | **Mission Control `:5200` DOWN** — tidak ada plist launchd, tidak ada KeepAlive, `server.py` ada (65 KB) tapi tidak jalan | port probe `000` |
| A2 | **Cron `agent-reach-watch` ERROR** — unpinned, config drift (`custom`→`opencode-zen`), fail-closed menolak jalan | `c6ec80ed633f` last run error |
| A3 | **3 launchd service GAGAL exit 127** — `kanban-sync`, `health-checker`, `changelog-writer` → script path MISSING (`/Volumes/HermesAgent/HermesAgentUSB/data/scripts/*.sh` tidak ada) | launchctl exit=127 |
| A4 | **Credential Supabase di config** — `SUPABASE_PG_URL` (postgres://postgres:***@...) tercantum di config + MCP `hermes-postgres` jalan dengan password di command line | ps + config |

## 🟠 TINGGI (P1)

| # | Anomali | Bukti |
|---|---------|-------|
| A5 | **UACC MCP rusak** — `command: .venv/bin/python` tapi `.venv` MISSING → 20x error `unrecognized arguments: --connect` | mcp-stderr 1267 error |
| A6 | **Ponytail MCP rusak** — `index.js` ada tapi `node_modules/@modelcontextprotocol/sdk` MISSING → 175x `ERR_MODULE_NOT_FOUND` | mcp-stderr |
| A7 | **`motion` MCP phantom** — dikonfigurasi tapi `motion-bridge.py` MISSING → 189x FileNotFoundError loop | mcp-stderr 295 Traceback |
| A8 | **Windows PATH di proses** — `Error: Cannot find module 'F:\Users\zaryu\...'` — sisa config dari Windows machine | mcp-stderr line 284 |
| A9 | **Fallback chain terbalik** — `juan-router` (401) di posisi #1, 9router (LIVE) di #2-3 | config |
| A10 | **Skill plane split** — bank 47 vs USB 231 (bukan 213!) vs HOME 2 vs Jcode MISSING | scan |
| A11 | **`agentrouter` dead config** — terdaftar tapi tidak di chain, tidak dipakai | config |
| A12 | **Ghost plugins** — `hermes-achievements`, `orca-status`, `telegram_router` folder ada, tidak enabled | plugins dir |

## 🟡 SEDANG (P2)

| # | Anomali | Detail |
|---|---------|--------|
| A13 | **`kune-ya.com` DOWN** (HTTP 000 timeout) | canary |
| A14 | **`niu-vermilion` 307 redirect** | perlu verifikasi |
| A15 | **Auxiliary vision provider=9router model=`Qwen3.5-397B-A17B`** — kemungkinan model tidak ada di 9router (perlu test) | config |
| A16 | **`notebooklm-mcp`:8124** — terdaftar enabled tapi TIDAK ADA proses (down) | config + lsof |
| A17 | **state.db 732 MB di ExFAT USB** — risiko korupsi + `integrity_check` timeout 30s | fs |
| A18 | **LSP node_modules 409 MB** di USB — waste | du |
| A19 | **mcp-stderr 1.5 MB / 24k lines, 1267 error-ish** — noise MCP loop | log |

## 🟢 INFO

| # | Catatan |
|---|---------|
| A20 | `Mac Win` 95% penuh (3.8 Gi sisa), `Niumination` NTFS 75% — bukan blocker |
| A21 | OpenAI Codex / MiniMax / xAI OAuth belum login — normal, tidak dipakai |
| A22 | 9router: launchd `com.9router` ✅ running; gateway `ai.hermes.gateway` ✅ running (PID 11393) |

---

## Detail Scan

### Git (45 repo)
- ✅ Semua clean & pushed (setelah update 18 Ags), kecuali camofox-browser & ponytail (keputusan: lokal)
- ✅ Tidak ada secret di tracked files
- ✅ Tidak ada remote aneh/token di URL

### Proses & Port
- ✅ Gateway PID 11393 running, Telegram connected
- ✅ 9router :20128 LISTENING (launchd com.9router)
- ⚠️ MC :5200 DOWN
- ⚠️ notebooklm :8124 DOWN

### Perangkat service launchd
| Service | Status |
|---|---|
| ai.hermes.gateway | ✅ running (PID 11393) |
| com.9router | ✅ running (PID 580) |
| com.niumination.kanban-sync | ❌ exit 127 (script missing) |
| com.niumination.health-checker | ❌ exit 127 (script missing) |
| com.niumination.changelog-writer | ❌ exit 127 (script missing) |

### Config (config.yaml)
- Model: opencode-zen / big-pickle (valid)
- Providers: 9router, agentrouter, juan-router, huancheng
- Fallback: juan-router(401) → 9router → 9router — **urutan salah**
- Plugins enabled: rtk-rewrite saja

### MCP servers (9 terdaftar, semuanya enabled)
| Server | Status |
|---|---|
| filesystem | ✅ |
| github | ✅ |
| hermes-postgres | ⚠️ credential di cmdline |
| hermes-sqlite | ✅ |
| notebooklm-mcp | ❌ down |
| ponytail | ❌ sdk missing |
| time | ✅ |
| uacc | ❌ .venv missing |
| context7 | ✅ |

### Skill plane
| Store | Count |
|---|---|
| Bank pusat (SoT) | 47 SKILL.md (manifest 47, fileCount 267) |
| Hermes USB | 231 SKILL.md |
| Hermes HOME | 2 SKILL.md |
| Jcode | MISSING |

### Deploy canary
| Target | HTTP |
|---|---|
| PemdiAcehTengah | 200 ✅ |
| kune-ya.com | 000 ❌ |
| niu-vermilion | 307 ⚠️ |
| niu-dash GH Pages | 301 ✅ |
| Niu-LKH GH Pages | 301 ✅ |
| ecosystem-config GH Pages | 301 ✅ |
| 9router | 200 ✅ |
| MC :5200 | 000 ❌ |

### Disk / RAM
- Internal Data: 39 Gi free (65%)
- HermesAgent USB: 17 Gi free (40%)
- Mac Win: 3.8 Gi free (95%!) — ExFAT
- Niumination NTFS: 44 Gi free (75%)
- RAM: 16 GB, pages free 275k (~1 GB) — **ketat**
- state.db: 732 MB di USB

---

*Laporan disusun 2026-08-18, scan menyeluruh 45 repo + proses + config + MCP + skill + deploy.*
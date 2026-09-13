# MC Bridge Migration — Opsi C Detail (2026-09-07)

## Konteks
`modules/hermes_bridge.py` dan `swarm/` (agents.py, bus.py, worker.py) dihapus
saat refactor ke apex-ui Next.js (commit `7044e8f`).
`server.py` crash: `ModuleNotFoundError: No module named 'swarm'`

## Recovery Original Source
```bash
git log --all --oneline -- modules/hermes_bridge.py
# → 7044e8f feat: migrate to apex-ui (last known good)
git show 7044e8f^:modules/hermes_bridge.py  # tampilkan source lengkap
```

## Opsi C: Reimplementasi ke TypeScript (dipilih)
Alasan pilih TS over pulihkan Python:
- server.py FastAPI butuh `swarm/` seluruhnya (bus, worker, agents) — recovery besar
- apex-ui sudah jalan di :5200 — tidak ada ruang untuk FastAPI di port yang sama
- TS route lebih maintainable dengan stack Next.js yang ada

## File yang Dibuat

### `apex-ui/lib/bridge.ts`
Modul TypeScript, 3 fungsi ekspor:
```typescript
sendChat(text: string, topicId: string = '1')
  → execFileAsync(HERMES_CLI, ['send', '-t', `telegram:${CHAT_ID}:${topicId}`, text])
  → returns { status: 'sent'|'error', message: string }

runTerminal(cmd: string, timeout: number = 15)
  → ALLOWED_COMMANDS Set, DANGEROUS_PATTERNS block
  → execFileAsync dengan shell: false
  → returns { status, output, exit_code }

runAgentTurn(prompt, sessionId, model?, provider?, timeout = 300)
  → execFileAsync(HERMES_CLI, ['-z', prompt, '--resume', sessionId, ...])
  → returns { status: 'done'|'error', output?, message? }
```

### DB Layer (`db_manager.py` + `data/init.sql`)
```sql
-- init.sql — tambah tabel
CREATE TABLE IF NOT EXISTS dispatches (
    id TEXT PRIMARY KEY,
    target_topic TEXT NOT NULL,
    message TEXT NOT NULL,
    source_agent TEXT DEFAULT 'general',
    status TEXT DEFAULT 'pending',
    error TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

```python
# db_manager.py — 3 fungsi baru
add_dispatch(target_topic, message, source_agent='general') → dict
update_dispatch_status(dispatch_id, status, error=None) → bool
get_dispatches(limit=20) → list
```

CLI query handler di `if __name__ == '__main__'`:
```python
elif query == 'add_dispatch':   print(json.dumps(add_dispatch(*params)))
elif query == 'update_dispatch_status': ...
elif query == 'get_dispatches': ...
```

### API Routes Baru (`apex-ui/app/api/mc/`)
```
dispatch/route.ts          POST {to, message, source} — validasi topic 1/802/803/804/1172
dispatches/route.ts        GET  ?limit=20 — riwayat
telegram/send/route.ts     POST {message, topic_id} — kirim via hermes send CLI
tasks/update/route.ts      POST {task_id, status, result} — overwrite GET route lama
```

## Validasi
```bash
cd apex-ui && npx next build
# Semua route harus muncul di tabel build output sebagai ƒ (Dynamic)

curl -s -X POST http://localhost:5200/api/mc/dispatch \
  -H "Content-Type: application/json" \
  -d '{"to":"803","message":"test","source":"general"}'
# Expected: {"id":"d...","status":"pending","target":"803",...}

curl -s -X POST http://localhost:5200/api/mc/dispatch \
  -H "Content-Type: application/json" \
  -d '{"to":"999","message":"invalid"}'
# Expected: 400 {"error":"Invalid target. Must be one of: 1, 802, 803, 804, 1172"}
```

## Topic Map (Hermes channel_overrides)
| Topic | Agent | Model |
|-------|-------|-------|
| 1 | chief | explabs/gpt-5.4-mini |
| 802 | research | explabs/claude-haiku-4.5 |
| 803 | programmer | explabs/gpt-4o-mini |
| 804 | qa | explabs/claude-sonnet-4.6 |
| 1172 | creator | explabs/gemma-4-31b |

## Pitfall Ditemukan
- `server.py` FastAPI tidak bisa dijalankan lagi (modul `swarm/` hilang, `modules/` hilang)
- Jangan coba pulihkan `server.py` tanpa juga pulihkan `swarm/agents.py`, `swarm/bus.py`, `swarm/worker.py`, `modules/skill_monitor.py` — semua saling dependen
- `hermes send -t telegram:CHAT_ID:TOPIC_ID` — CLI path di macOS: `/Users/zaryu/src/hermes-agent/.venv/bin/hermes`
- Tabel `dispatches` harus di-migrate (jalankan `python3 db_manager.py` ulang agar `init.sql` ter-apply via `executescript`)

# /api/mc/* — bentuk respons (verified 2026-08-15)

Semua endpoint ini punya bentuk yang TIDAK intuitif. Selalu cek shape via `curl -s localhost:5200/api/mc/...` sebelum render, atau pakai parser yang toleran dua bentuk.

| Endpoint | Bentuk | Catatan |
|---|---|---|
| `/api/mc/directive` | `{"threads":[{thread_id, model, directive, context_tokens, context_max, context_pct, updated_at}]}` | **LAMBAT** (8+ detik — baca sessions.json + config tiap call). Fetch timeout ≥ 20s. Thread id: "1","802","803","804","1172" (STRING, bukan int) |
| `/api/mc/agents` | `{"agents":[{id, name, role, status, color}]}` | BUKAN array polos! `status` ∈ idle/active/running. id: chief, research, programmer, qa, konten-kreator |
| `/api/mc/system` | `{uptime, cpu_percent, cpu_count, cpu_freq_mhz, memory:{total_gb, used_gb, available_gb, percent}, disk:{total_gb, free_gb, percent}, hostname, platform, os_release}` | `uptime` = **STRING** ("1h 37m") bukan detik. Disk pakai `disk.percent` & `disk.free_gb` — TIDAK ada `disk_percent` di root |
| `/api/mc/logs` | `{"logs":[{timestamp, level, agent_id, message}]}` | `level` uppercase (INFO/WARN/ERROR); `timestamp` ISO → slice(11,19) untuk HH:MM:SS |
| `/api/mc/send-telegram` | POST body `{message}` → kirim ke #General (topic 1) | Dipakai voice command fusion; MC log mencatat "Telegram Topic 1" |

## Pola render aman (dipakai mission panel fusion)

```js
const [res, sys] = await Promise.all([jget('/api/mc/agents'), jget('/api/mc/system')]);
const agents = (res && Array.isArray(res.agents)) ? res.agents : (Array.isArray(res) ? res : null);
// uptime string langsung dipakai: const upStr = sys.uptime || '—';
// disk: disk.percent != null ? disk.percent+'%' : '—'
```

## Health check

`GET /health` → `{"status":"ok","version":"2.6.x","database":"ok"}`. Server mati = curl gagal / browser ERR_CONNECTION_REFUSED. Restart: `terminal(background=true)` + `./venv/bin/python server.py` di `services/niu-mission-control/`.

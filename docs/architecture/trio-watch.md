# Trio Awareness — Hermes × JCode × OpenCode

**Tujuan:** Hermes (primary) aware aktivitas JCode (ke-2) & OpenCode-CLI (ke-3) secara passif — tanpa kontrol, spawn, atau delegasi. Cegah bentrok (2 tool garap repo sama) & ketinggalan info.

**Paradigma:** Hermes = konduktor. JCode/OpenCode = eksekutor mandiri. Hermes hanya **memantau → memberi tahu → mencatat ke shared memory**.

---

## 📍 Cara Pakai

```bash
# di Hermes — lihat JCode + OpenCode
bash scripts/up-eco.sh --from hermes

# di terminal JCode — lihat Hermes + OpenCode
bash scripts/up-eco.sh --from jcode

# di terminal OpenCode — lihat Hermes + JCode
bash scripts/up-eco.sh --from opencode
```

Bisa langsung: `bash scripts/trio-watch.sh --from hermes`

---

## 🧠 Shared Memory: `core/runtime/trio-status.json`

Overwrite tiap run. Struktur:
```json
{
  "updated_at": "2026-08-22T12:00:00Z",
  "called_from": "hermes",
  "tools": {
    "hermes":   { "sessions": 84, "last_session": "...", "model": "...", "git_dirty": [...] },
    "jcode":    {
      "sessions": 3,
      "active_sessions": 3,
      "total_sessions": 146,
      "last_session": "tiger",
      "live_summaries": [
        {"session": "tiger", "summary": "Project services/cc-acehtengah..."}
      ],
      "pid": "1101",
      "git_dirty": [...]
    },
    "opencode": {
      "sessions": 0,
      "active_sessions": 0,
      "last_session": "idle",
      "git_dirty": [...]
    }
  },
  "conflicts": [],
  "gaps": [ { "type":"undocumented", "repo":"/...", "commit":"daec180...", "desc":"..." } ]
}
```

---

## ⚙️ Deteksi Aktivitas (read-only)

| Tool | Sumber aktif | Total | last_session |
|---|---|---|---|
| Hermes | count `~/.hermes/sessions/*.json` | N/A | file JSON terakhir |
| JCode | `pgrep -x jcode` + `~/.jcode/sessions/*.json` mtime<5m | `~/.jcode/cache/session-picker-list-v2.json` | `compaction.summary_text` (fallback: `messages[role=user]`) |
| OpenCode | `pgrep -x opencode` | `opencode session list` | title terakhir dari list |

### JCode ringkasan aktivitas
- **Primary:** `~/.jcode/sessions/<name>/compaction.summary_text` → deskripsi project (e.g. "Project services/cc-acehtengah (Next.js...) butuh perbaikan AI").
- **Fallback:** scan `messages[]` sampai ketemu `role == user` (bukan `system-reminder`).
- **Multiple live session:** semua ditampilkan (↳ sedang: ...).

### OpenCode idle
- `pgrep -x opencode` kosong → **"tidak aktif (idle)"**, skip `opencode session list` (hemat 5s).

---

## 🛠️ File

| File | Peran |
|---|---|
| `scripts/trio-watch.sh` | Collector read-only → `core/runtime/trio-status.json` |
| `scripts/up-eco.sh` | Arg parser `--from` + Phase 9a panggil trio-watch |
| `core/runtime/trio-status.json` | Shared memory (overwrite tiap run) |

## 🔒 Safety

- Read-only → hanya overwrite `core/runtime/trio-status.json` (cache).
- Tidak ada spawn/delegasi (Hukum #11).
- Tidak ganti model (#2).
- Tidak sentuh `core/FREEZE.list` (#4).
- Tidak ada cron tambahan — hanya jalan via `up-eco` on-demand.

# Anomaly Audit Playbook — Niumination Ecosystem

> Verified 18-Ags-2026. User prompt: "periksa seluruh anomali yang ada di ekosistem, jangan melewatkan satu pun".
> Deliverable: laporan terstruktur per severity (🔴 KRITIS / 🟠 TINGGI / 🟡 SEDANG / 🟢 INFO), TANPA fix apa pun (user belum minta).

## Golden rules
1. **Rejections only when asked** — audit produces a report; fixes happen only after user says "fix/gas/kerjakan".
2. **Tidak pernah edit config.yaml langsung** — jalur tulis sah: `hermes config set` / `hermes fallback` / `hermes cron`.
3. Scan ALL 45 repos — jangan sampel. os.walk discovery (lihat bug di bawah).
4. Redact credentials di output laporan (`postgresql://user:***@host`).

## Layer 1 — Git (45 repo)
```python
import subprocess, os
NIU = "/Users/zaryu/Desktop/Niumination"
SKIP_DIRS = ('node_modules','venv','__pycache__','.venv','dist','build','venv3','.cache','.obsidian','.git')
repos = []
for root, dirs, files in os.walk(NIU):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]   # filter dulu...
    if '.git' in dirs:                                   # ...baru cek .git (BUG jika terbalik: 0 repo ditemukan)
        repos.append(root)
```
Per repo: `branch`, `git status --porcelain` (dirty count), `rev-list --count origin/<branch>..HEAD` (unpushed), `git remote -v` (kepemilikan), `git stash list`, `git ls-files` (untuk secret scan). Anomali: dirty, unpushed, remote non-Niumination, remote mengandung token, stash, branch non-main/master, submodule.

## Layer 2 — Secret scan (tracked files)
Regex catching: `sk-...`, `ghp_`, `gho_`, `xoxb`, `AIza`, `AKIA`, `BEGIN PRIVATE KEY`, JWT (`eyJ...`), `api_key=`/`token=`/`password=`/`secret=` assignments. Skip binary/large files (>500KB). **Filter false positives:** path mengandung test/fixture/example/sample/mock/placeholder.
Hasil 18-Ags: 0 hit — tapi temuan terpisah di Layer 4 (`SUPABASE_PG_URL` plaintext di config).

## Layer 3 — Proses & port
`ps aux | grep -E 'hermes|server.py|9router|mission|watchdog|mcp-server|tailscale'`; `lsof -i :5200` (MC) & `lsof -i :20128` (9router); `launchctl list | grep niu/hermes/9router/mission`. Anomali nyata 18-Ags: MC `:5200` DOWN tanpa plist, 9router UP via `com.9router`, 5 watchdog MCP duplikat.

## Layer 4 — Config (~/.hermes/data/config.yaml)
```bash
grep -A5 "^providers:" config.yaml
hermes cron list | grep -E "Name:|Schedule:|Last run:"
```
Cek: YAML parse OK, providers terdaftar vs base_url/key_env, **urutan fallback_providers vs health probe** (401 di depan = salah urut), plugins.enabled vs folder plugins/, auxiliary.* provider/model, terminal.backend.
Anomali nyata: fallback #1 `juan-router` 401 padahal 9router 200 LIVE; `agentrouter` dead config (terdaftar, tidak dipakai); 3 ghost plugins; `SUPABASE_PG_URL` plaintext + MCP jalan dengan password di command line.

## Layer 5 — MCP crash-loop diagnosis (mcp-stderr.log)
`/Volumes/HermesAgent/HermesAgentUSB/data/logs/mcp-stderr.log` — file bisa 1.5MB/24k baris. Klasifikasi error:
```python
from collections import Counter
errs = [l.strip() for l in lines if any(k in l.lower() for k in ('error','traceback','not found','cannot','failed'))]
Counter(...)  # 295x Traceback, 176x FileNotFoundError, 175x ERR_MODULE_NOT_FOUND, 100x HTTP 400...
```
Lalu cek ROOT CAUSE per jenis — cek file yang diklaim: `.venv/bin/python` MISSING (uacc), `node_modules/@modelcontextprotocol/sdk` MISSING (ponytail), `motion-bridge.py` MISSING (motion phantom), path Windows `F:\...` (sisa config mesin lain). Catatan: MCP server terdaftar di config 9 (filesystem, github, hermes-postgres, hermes-sqlite, notebooklm-mcp, ponytail, time, uacc, context7) — cek `lsof -i` untuk yang remote (notebooklm :8124 down = anomali).

## Layer 6 — Launchd & failing services
`launchctl print gui/501/<label>` → `last exit code`, `program`. Exit **127** = program/script path hilang. 18-Ags: `kanban-sync`, `health-checker`, `changelog-writer` semuanya 127 karena script di `/Volumes/HermesAgent/HermesAgentUSB/data/scripts/*.sh` MISSING (path mengarah USB, file tidak ada).

## Layer 7 — Skill plane drift
Hitung SKILL.md per store: bank `/Users/zaryu/Desktop/Niumination/skills` (47), USB `/Volumes/HermesAgent/HermesAgentUSB/data/skills` (231 — BUKAN 213, berubah!), HOME `~/.hermes/skills` (2), Jcode `~/.jcode/skills` (MISSING). Cek manifest.json skillCount vs real count; INDEX.md count vs real. 18-Ags: manifest 47 = real 47 (bank OK), tapi USB 231 = 4.9× bank (hub-dump, bukan mirror) + Jcode MISSING.

## Layer 8 — Deploy canary
```bash
for u in "https://pemdi-aceh-tengah.vercel.app" "https://kune-ya.com" "https://niu-vermilion.vercel.app" \
         "https://niumination.github.io/niu-dash" "https://niumination.github.io/Niu-LKH" \
         "https://niumination.github.io/ecosystem-config" "http://localhost:20128/v1/models" "http://127.0.0.1:5200/"; do
  curl -sS -o /dev/null -w "%{http_code}\n" -m 8 "$u"
done
```
Arti: 000 = timeout/connection (kune-ya DOWN, MC DOWN), 301 = GH Pages OK, 307 = redirect (niu-vermilion perlu verifikasi).

## Layer 9 — DB & disk
`state.db` 732MB di ExFAT USB — `sqlite3 PRAGMA integrity_check` TIMEOUT 30s (ExFAT lambat) → pakai timeout 60-120s atau skip; laporkan sebagai risiko korupsi, bukan error definitif. `du -sh` folder besar (LSP node_modules 409MB = waste).

## Output format
Tabel per severity, setiap baris: ID unik (A1..An) + anomali + bukti (nilai probe). JANGAN assert fix — tutup laporan dengan "Mau saya eksekusi fix untuk kategori tertentu, atau simpan laporan ini dulu?"
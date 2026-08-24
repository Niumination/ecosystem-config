# Ecosystem Audit: Config & System Comparison

Teknik audit komprehensif untuk membandingkan **kondisi Hermes config dan ekosistem "sebelum vs sesudah"** perubahan besar (reorganisasi root proyek, migrasi, upgrade).

## Trigger

Gunakan workflow ini ketika user meminta:
- "Buat laporan lengkap konfig hermes dan ekosistem kondisi saat ini"
- "Perbandingan dengan konfigurasi sebelumnya"
- "Apa yang berubah setelah reorganisasi/migrasi?"

## Data Points yang Harus Dikumpulkan

### 1. Hermes Config — Live State
**Sumber:** `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml`

Baca seluruh file. Catat key sections:
- `model:` — main model + provider
- `fallback_providers:` — fallback chain
- `delegation:` — max_concurrent_children, max_spawn_depth, orchestrator_enabled
- `discord:` — enabled?
- `telegram:` — allowed_chats, allowed_topics, channel_skill_bindings
- `plugins:` — enabled list + directories
- `mcp_servers:` — list of enabled servers
- `session_reset:` — mode
- `auxiliary:` — vision, compression providers
- `_config_version`

### 2. Hermes Config — Sebelumnya (Backup)
**Sumber:** `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml.bak.*`

```bash
ls -la /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml.bak*
# Pilih backup terdekat sebelum perubahan
```

Bandingkan section-by-section dengan `diff` atau per-baris:

```bash
diff <(grep -n -E "^(discord|telegram|plugins|delegation|gateway|model:|provider:)" config.yaml) \
     <(grep -n -E "^(discord|telegram|plugins|delegation|gateway|model:|provider:)" config.yaml.bak.TANGGAL)
```

### 3. Gateway State — Cek DUA Lokasi

**Penting:** Ada dua file `gateway_state.json` yang mungkin berbeda:

| Lokasi | Fungsi |
|--------|--------|
| `~/.hermes/gateway_state.json` | State lama — kadang **stale** |
| `/Volumes/HermesAgent/HermesAgentUSB/data/gateway_state.json` | State **aktual** dari USB data |

```bash
echo "--- ~/.hermes ---"
cat ~/.hermes/gateway_state.json
echo "--- USB data ---"
cat /Volumes/HermesAgent/HermesAgentUSB/data/gateway_state.json
```

Jika berbeda, laporan harus mencatat **mana yang akurat** (cross-check dengan proses aktual via `ps aux | grep hermes`).

### 4. Proses & Layanan

```bash
# Proses Hermes
ps aux | grep -i hermes | grep -v grep

# Port listener (kecuali noise sistem)
lsof -i -P | grep LISTEN | grep -v -E "rapportd|ControlCe|WindowSe|sharingd|WiFi" | awk '{print $1, $3, $9}' | sort -u

# Launchd service
launchctl list | grep hermes
```

### 5. Cron Jobs

```bash
python3 -c "
import sys, json
d = json.load(open('/Volumes/HermesAgent/HermesAgentUSB/data/cron/jobs.json'))
for j in d['jobs']:
    print(f\"{j['id'][:8]} | {j.get('name','?')} | enabled={j.get('enabled')} | schedule={j['schedule']['display']} | last={j.get('last_status','?')}\")
"
```

### 6. Kanban Stats

```bash
curl -s --max-time 5 localhost:5199/api/stats 2>/dev/null | python3 -m json.tool
```

Catat: total tasks, byStatus breakdown, recentDone items, oldestTodo.

### 7. Git Health — Root & Projects

```bash
# Root ecosystem repo
cd /Users/zaryu/Desktop/Niumination
git status --short
git log --oneline -3

# Project counts
echo "Production:" && ls Production/ | wc -l
echo "projects:" && ls projects/ | wc -l
echo "incubator:" && ls incubator/ | wc -l
```

### 8. Kanban Server Health

```bash
curl -s --max-time 3 localhost:5199/api/stats 2>/dev/null && echo "🟢 Running" || echo "🔴 Unreachable"
curl -s --max-time 3 localhost:5200 2>/dev/null && echo "🟢 MC Dashboard running" || echo "⏹️ MC Dashboard stopped"
```

## Template Laporan

Gunakan struktur berikut untuk laporan final:

```markdown
# 📊 Laporan Lengkap: [Judul]

## 🕐 Kondisi: [Tanggal + Waktu]

---

## BAGIAN 1 — KONFIGURASI HERMES SAAT INI

### 🧠 Model AI
| Item | Nilai |
...

### 🔁 Fallback Chain
...

### 🤖 Delegasi Subagent
| Parameter | Nilai |
...

### 🌐 Platform — Telegram
...

### 🧩 Topic → Skill Bindings
...

### 🔌 MCP Servers Aktif
...

### 🧩 Plugins Terinstall
...

---

## BAGIAN 2 — STATUS LAYANAN

### 🌐 Gateway
| Komponen | Status |
...

### 🖥️ Server & Port
...

### ⏰ Cron Jobs
...

### 🗄️ Kanban Stats
...

---

## BAGIAN 3 — EKOSISTEM PROYEK

### 📁 Struktur Root
...

### 🐙 GitHub Repos
...

### 📦 Project Highlight
...

---

## BAGIAN 4 — PERBANDINGAN: SEBELUM vs SESUDAH

### 🔄 Perubahan Signifikan
| Aspek | **SEBELUM** | **SESUDAH** |
|-------|-------------|-------------|
...

### ⚙️ Perubahan Konfigurasi Detail
| Parameter | Sebelum | Sesudah | Keterangan |
...

### ⚠️ Masih Perlu Perhatian
| Item | Severity | Catatan |
...
```

## Pitfalls

1. **Gateway state file ganda** — Selalu cek dua lokasi. State di `~/.hermes/` bisa stale berminggu-minggu.
2. **Config backup bisa banyak** — Pilih backup dengan timestamp terdekat SEBELUM perubahan. Jangan pakai backup yang corrupt (.corrupt.bak).
3. **AGENTS.md root terlewat** — File di root repo `ecosystem-config` sering tidak ikut di-commit. Selalu `git status` di root setelah reorganisasi.
4. **Port listener noise** — Filter port sistem (rapportd, sharingd, WiFi, dll) agar laporan fokus ke port aplikasi (5199, 5200, MCP servers).
5. **Procses baru setelah restart** — PID gateway berubah setiap restart. Jangan hardcode PID — baca dari `gateway_state.json` atau `ps`.

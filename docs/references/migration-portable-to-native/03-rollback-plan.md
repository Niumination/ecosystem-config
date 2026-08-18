# 03 — Rollback Plan: Jika Migrasi Gagal

## Prinsip Golden Rule

> **JANGAN hapus source (USB portable) sampai native confirmed working minimal 3 hari.**
> Selama periode itu, USB tetap bisa dipakai sebagai fallback.

---

## Skenario Kegagalan & Recovery

### 🔴 SCENARIO 1: Gateway Error "Config invalid" after migrate

**Gejala:** `hermes gateway run` error — config.yaml tidak kompatibel
**Penyebab:** Format YAML berubah, path absolut salah, atau field missing

**Recovery:**
```bash
# 1. Cek error detail
hermes doctor --fix

# 2. Bandingkan dengan config asli
diff ~/.hermes/config.yaml /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml

# 3. Jika tidak bisa diperbaiki dalam 5 menit → ROLLBACK
# Hapus native config
rm -rf ~/.hermes

# Kembali ke portable
export HERMES_HOME=/Volumes/HermesAgent/HermesAgentUSB/data
hermes gateway run
```

---

### 🔴 SCENARIO 2: state.db Corrupt

**Gejala:** `hermes doctor --check-db` error, atau session history hilang
**Penyebab:** Copy file tidak sempurna (USB eject saat copy), atau versi SQLite mismatch

**Recovery:**
```bash
# 1. Cek integritas
sqlite3 ~/.hermes/state.db "PRAGMA integrity_check;"

# 2. Jika corrupt → restore dari backup
cp /Volumes/HermesAgent/HermesAgentUSB/data.backup.YYYYMMDD/state.db ~/.hermes/state.db

# 3. Jika masih gagal → gunakan source USB lagi
export HERMES_HOME=/Volumes/HermesAgent/HermesAgentUSB/data
```

---

### 🔴 SCENARIO 3: API Keys Tidak Terbaca

**Gejala:** Provider error "401 Unauthorized" atau "403 Forbidden"
**Penyebab:** .env tidak tercopy, atau permission berbeda

**Recovery:**
```bash
# 1. Cek .env ada dan terbaca
ls -la ~/.hermes/.env
chmod 600 ~/.hermes/.env

# 2. Cek env_passthrough di config
grep env_passthrough ~/.hermes/config.yaml

# 3. Cek apakah HERMES_HOME override bikin env nggak ke-load
# Solusi: unset HERMES_HOME dan biarkan default ~/.hermes
unset HERMES_HOME
```

---

### 🔴 SCENARIO 4: MCP Server Gagal Start

**Gejala:** Tool error "Failed to initialize MCP server"
**Penyebab:** Path binary salah (masih pointing ke portable venv)

**Recovery:**
```bash
# 1. Cek path MCP di config
grep -A3 "mcp_servers:" ~/.hermes/config.yaml

# 2. Update path ke native venv
# Cari lokasi mcp-server-time baru:
which mcp-server-time 2>/dev/null || find ~/.local ~/.hermes -name "mcp-server-time" 2>/dev/null

# 3. Jika tidak ditemukan → install npm package
npm install -g @modelcontextprotocol/server-github @anthropic/mcp-server-time
```

---

### 🔴 SCENARIO 5: Cron Jobs Tidak Berjalan

**Gejala:** Job tidak muncul di `cronjob list`, atau error "script not found"
**Penyebab:** SCRIPTS_PATH berubah, atau cron DB path berbeda

**Recovery:**
```bash
# 1. Cek cron job masih ada
hermes cron list

# 2. Jika hilang → restore kanban.db (cron job disimpan di state.db/kanban.db)
cp /Volumes/HermesAgent/HermesAgentUSB/data.backup.YYYYMMDD/kanban.db ~/.hermes/kanban.db

# 3. Jika script path salah → update manual
hermes cron update <job_id> --script ~/.hermes/scripts/<script_name>
```

---

### 🔴 SCENARIO 6: Telegram Gateway Duplicate (Dual Gateway)

**Gejala:** Pesan terduplikasi, agent menjawab dua kali
**Penyebab:** Gateway portable masih jalan + gateway native jalan — competing for Telegram bot token

**Recovery:**
```bash
# 1. Matikan gateway portable
pkill -f "hermes.*gateway.*run"

# 2. Verifikasi PID mati
ps aux | grep hermes | grep gateway

# 3. Restart native gateway
hermes gateway run
```

---

## Complete Rollback Procedure (30 menit)

Jika lebih dari 2 skenario gagal dalam 1 sesi → **rollback total:**

```bash
# 1. STOP native gateway
pkill -f "hermes.*gateway" 2>/dev/null

# 2. HAPUS direktori native
rm -rf ~/.hermes

# 3. KEMBALIKAN environment variable
export HERMES_HOME=/Volumes/HermesAgent/HermesAgentUSB/data
echo 'export HERMES_HOME=/Volumes/HermesAgent/HermesAgentUSB/data' >> ~/.zshrc

# 4. RESTART portable gateway
cd /Volumes/HermesAgent/HermesAgentUSB/data
hermes gateway run &

# 5. VERIFIKASI dari Telegram
# Kirim "test" — pastikan response dari portable gateway
```

---

## Decision Matrix: Rollback or Fix?

| Gejala | Action | Deadline |
|--------|--------|----------|
| Config error | Fix path/config | 10 menit → rollback |
| state.db corrupt | Restore from backup | 5 menit → rollback |
| API keys error | Fix .env/permission | 5 menit → rollback |
| MCP server error | Update binary path | 15 menit → rollback |
| Cron jobs error | Re-register jobs | 10 menit → rollback |
| Dual gateway | Kill one | Langsung fix |
| Gateway crash loop | Rollback | Langsung rollback |

---

## Pre-Rollback Checklist

Sebelum memutuskan rollback, pastikan:

- [ ] Sudah mencoba `hermes doctor --fix`?
- [ ] Sudah cek diff config dengan portable?
- [ ] Sudah coba restore dari backup (copy ulang)?
- [ ] Ada error message spesifik yang bisa di-search?
- [ ] Waktu sudah > 20 menit sejak mulai troubleshooting?

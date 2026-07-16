# 02 — Migration Steps: Portable → Native macOS

## Strategi

**Dua Skenario:**

| Skenario | Kapan | Keuntungan | Risiko |
|----------|-------|------------|--------|
| **A: Migrasi dulu, upgrade nanti** | Saat ini (v0.16→v0.16 native) | Versi sama, config minimal berubah | Pekerjaan dobel (migrasi lalu upgrade) |
| **B: Upgrade dulu, migrasi setelahnya** | Setelah ekosistem matang | Sekali jalan: langsung mendarat di v0.18 native | Lebih banyak variable, potensi kegagalan |

**Rekomendasi:** Skenario A — migrasi v0.16.0 → v0.16.0 native dulu. Setelah native stabil, baru upgrade ke v0.18.0.

---

## Phase 0: Persiapan (Waktu: ~30 menit)

### 0.1 — Cek Persyaratan
```bash
# Cek disk space di Mac internal
df -h / | head -2
# Harus ≥ 20 GB free (15 GB data + overhead)

# Cek versi Hermes yang akan diinstall
hermes --version
# Harus ≥ 0.16.0

# Pastikan pip/uv tersedia
which uv
```

### 0.2 — Backup Total Portable Hermes
```bash
# STOP gateway dulu
hermes gateway stop
# atau
pkill -f "hermes gateway"

# Backup full
cp -a /Volumes/HermesAgent/HermesAgentUSB/data \
      /Volumes/HermesAgent/HermesAgentUSB/data.backup.$(date +%Y%m%d)

# Backup venv (opsional — bisa recreate)
cp -a /Users/zaryu/.hermes-portable/venv \
      /Users/zaryu/.hermes-portable/venv.backup.$(date +%Y%m%d)
```

### 0.3 — Prepare Target Directory
```bash
# Native Hermes home standard
mkdir -p ~/.hermes

# Ekosistem Niumination tetap di Desktop (tidak dipindah)
ls /Users/zaryu/Desktop/Niumination/
```

---

## Phase 1: Install Hermes Native (Waktu: ~10 menit)

### 1.1 — Install Hermes via pip/uv (native, bukan portable)
```bash
# Instal langsung di sistem python (atau venv baru)
uv tool install hermes-agent
# atau
pip install hermes-agent
```

### 1.2 — Verifikasi Instalasi Native
```bash
# Cek apakah hermes terdeteksi dari PATH global
which hermes
# Output harus: /usr/local/bin/hermes atau ~/.local/bin/hermes
# BUKAN: /Users/zaryu/.hermes-portable/venv/bin/hermes

hermes --version
# Harus: v0.16.0 (sama dengan portable)
```

**PENTING:** Pastikan versi native sama dengan portable (v0.16.0) agar format state.db kompatibel.

---

## Phase 2: Migrasi Data (Waktu: ~15 menit)

### 2.1 — Stop Gateway & Proses
```bash
# Pastikan gateway portable benar-benar mati
pkill -f "hermes gateway" 2>/dev/null
sleep 2

# Verifikasi state file tidak terkunci
! ls /Volumes/HermesAgent/HermesAgentUSB/data/*.lock 2>/dev/null && echo "No locks" || echo "LOCKED — tunggu proses mati"
```

### 2.2 — Copy Data Inti (Wajib)
```bash
# DEFINED_HERMES_HOME akan kita set dari config nanti
# Tapi default native Hermes home adalah ~/.hermes

mkdir -p ~/.hermes

# Copy file konfigurasi inti
cp /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml ~/.hermes/config.yaml
cp /Volumes/HermesAgent/HermesAgentUSB/data/.env ~/.hermes/.env
cp /Volumes/HermesAgent/HermesAgentUSB/data/auth.json ~/.hermes/auth.json
cp /Volumes/HermesAgent/HermesAgentUSB/data/SOUL.md ~/.hermes/SOUL.md

# Copy state DB (PALING KRITIS — 239 MB)
cp /Volumes/HermesAgent/HermesAgentUSB/data/state.db ~/.hermes/state.db

# Copy kanban DB
cp /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db ~/.hermes/kanban.db

# Copy memories
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/memories ~/.hermes/memories

# Copy skills
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/skills ~/.hermes/skills

# Copy scripts (12 custom scripts)
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/scripts ~/.hermes/scripts
```

### 2.3 — Copy Data Non-Kritis (Opsional)
```bash
# Sessions (histori chat)
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/sessions ~/.hermes/sessions

# Checkpoints
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/checkpoints ~/.hermes/checkpoints

# Cron output
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/cron ~/.hermes/cron

# Plugins
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/plugins ~/.hermes/plugins

# Logs (untuk referensi)
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/logs ~/.hermes/logs

# Tirith binary
cp -r /Volumes/HermesAgent/HermesAgentUSB/data/bin ~/.hermes/bin

# Cache files
cp /Volumes/HermesAgent/HermesAgentUSB/data/models_dev_cache.json ~/.hermes/models_dev_cache.json
cp /Volumes/HermesAgent/HermesAgentUSB/data/channel_directory.json ~/.hermes/channel_directory.json
```

### 2.4 — SKIP data yang bisa recreates
```bash
# TIDAK USAH di-copy:
# - home/ (12GB — cache/node_modules, recreate aja)
# - kanban/ (1.3GB — worker logs, bisa restart)
# - lsp/ (380MB — auto-install)
# - sandboxes/, images/, audio_cache/, image_cache/
# - cache/ (auto-populate)
```

---

## Phase 3: Konfigurasi Ulang Path (Waktu: ~20 menit)

### 3.1 — Update config.yaml: Replace Path Absolut

Semua path yang mengandung `/Volumes/HermesAgent/HermesAgentUSB/data/` harus diubah ke `~/.hermes/`.

**Minimal ganti:**
```yaml
# Di terminal.env_passthrough — HAPUS HERMES_HOME dari passthrough
# (karena native tidak perlu override)

# Di cron.script paths — update ke ~/.hermes/scripts/
# Di mcp_servers — update path ke venv native
```

### 3.2 — Update MCP Server Paths

| Server | Old Path | New Path |
|--------|----------|----------|
| `time` | `/Users/zaryu/.hermes-portable/venv/bin/mcp-server-time` | `<new-venv>/bin/mcp-server-time` |
| `hermes-sqlite` | `/Users/zaryu/.local/share/hermes-mcp/mcp-server-sqlite.py` | ✅ Sama (tidak perlu ganti) |
| `hermes-postgres` | `/Users/zaryu/.local/share/hermes-mcp/mcp-server-postgres.sh` | ✅ Sama |
| `ponytail` | `/Users/zaryu/Desktop/Niumination/tools/ponytail/...` | ✅ Sama (relatif ke Niumination) |

### 3.3 — Update .env HERMES_HOME
```bash
# Native: HERMES_HOME tidak perlu diset — default ke ~/.hermes
# HAPUS baris HERMES_HOME dari .env native
```

### 3.4 — Set HERMES_HOME Environment
```bash
# Tambahkan ke ~/.zshrc
echo 'export HERMES_HOME="$HOME/.hermes"' >> ~/.zshrc

# Load
source ~/.zshrc
```

---

## Phase 4: Verifikasi (Waktu: ~15 menit)

### 4.1 — Cek Konfigurasi
```bash
# Test config parsing
hermes config show model.default
# Harus: big-pickle

# Test provider
hermes config show providers

# Test env vars
hermes config show env
```

### 4.2 — Cek Database
```bash
# Cek state.db tidak corrupt
hermes doctor --check-db

# Cek memories terbaca
hermes memory list

# Cek skills terdaftar
hermes skills list | wc -l
# Harus 28+
```

### 4.3 — Test Gateway
```bash
# Start gateway di mode test (tanpa Telegram)
hermes gateway run --no-platforms --test

# Cek state
cat ~/.hermes/gateway_state.json

# Stop
hermes gateway stop
```

---

## Phase 5: Cutover (Waktu: ~5 menit)

### 5.1 — Set Native sebagai Default

Buat symlink atau alias:
```bash
# Hapus portable dari PATH
# Caranya: hapus ~/.hermes-portable/venv/bin dari PATH di ~/.zshrc

# Pastikan native hermes yang terpanggil
which hermes
# → /usr/local/bin/hermes atau ~/.local/bin/hermes
```

### 5.2 — Start Gateway Produksi
```bash
hermes gateway run
```

### 5.3 — Test dari Telegram
Kirim pesan "test" dari Telegram — pastikan response datang dari native gateway.

---

## Phase 6: Cleanup (Setelah Semua Verified)
```bash
# Baru hapus portable setelah 3-7 hari native stabil
# rm -rf /Users/zaryu/.hermes-portable/venv
# rm -rf /Volumes/HermesAgent/HermesAgentUSB/data.backup.YYYYMMDD
```

**JANGAN hapus USB portable sampai native confirmed working minimal 3 hari.**

---

## Timeline Estimasi (Total: ~1.5 jam)

```
Phase 0: Persiapan + Backup ─── 30 menit
Phase 1: Install native    ─── 10 menit
Phase 2: Copy data         ─── 15 menit (tergantung USB speed)
Phase 3: Konfigurasi path  ─── 20 menit
Phase 4: Verifikasi        ─── 15 menit
Phase 5: Cutover           ───  5 menit
                              ─────────
                    Total   ~1 jam 35 menit
```

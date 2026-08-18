# 04 — Post-Migration Verification

> **Gunakan checklist ini SETELAH migrasi selesai.**
> Jangan nyatakan migrasi berhasil sampai semua item ✅.

---

## ✅ Day 0 — Langsung Setelah Migrasi

### Config & Environment
- [ ] `hermes --version` → v0.16.0 (sama dengan portable)
- [ ] `hermes config show model.default` → `big-pickle`
- [ ] `hermes config show providers` → semua provider terdaftar
- [ ] `echo $HERMES_HOME` → `/Users/zaryu/.hermes`
- [ ] `.env` terbaca (test: kirim prompt, cek response dari model)

### Database Integrity
- [ ] `sqlite3 ~/.hermes/state.db "PRAGMA integrity_check;"` → `ok`
- [ ] `sqlite3 ~/.hermes/kanban.db "PRAGMA integrity_check;"` → `ok`
- [ ] `hermes doctor --check-db` → ✅

### Skills & Memory
- [ ] `hermes skills list \| wc -l` → 29+ (harus sama dengan portable, realitas: 29 direktori, 107 file SKILL.md)
- [ ] `hermes skills list` → nama-nama skill familiar
- [ ] `hermes memory list` → MEMORY.md + USER.md terbaca
- [ ] Test: minta agent pakai skill tertentu → response sesuai skill

### Cron Jobs
- [ ] `hermes cron list` → 1 job aktif (memory-checkpoint) — brain-daily-capture DIHAPUS 5 Agu 2026
- [ ] Script path: `checkpoint.py` → file exists di data/scripts/
- [ ] Test run job: `hermes cron run 663b902a9ce5` → sukses

### MCP Servers
- [ ] `hermes tools` atau `hermes mcp list` → 6 servers connected:
  - [ ] time
  - [ ] github
  - [ ] filesystem
  - [ ] hermes-sqlite
  - [ ] hermes-postgres
  - [ ] ponytail

### Telegram Gateway
- [ ] `hermes gateway run` → start tanpa error (mode test dulu)
- [ ] `cat ~/.hermes/gateway_state.json` → `"gateway_state":"running"`, `"platforms.telegram.state":"connected"`
- [ ] Kirim "test ping" dari Telegram → response datang dalam 10 detik
- [ ] Tidak ada duplicate response (pastikan portable gateway sudah mati)

---

## ✅ Day 1 — 24 Jam Setelah Migrasi

### Stability
- [ ] Gateway masih running (cek `gateway_state.json`)
- [ ] Tidak ada crash dalam 24 jam
- [ ] Semua cron job berjalan sesuai jadwal (cek cron output)
- [ ] Telegram responses normal, tidak ada error rate-limit aneh

### Performance
- [ ] Response time terasa lebih cepat dari USB? (I/O NVMe vs USB)
- [ ] Gateway startup time (dari sleep → siap) lebih cepat?

### Data Integrity
- [ ] Session history masih utuh (cek dengan `session_search(query="...")`)
- [ ] Memories masih akurat
- [ ] Auth token masih valid (Tavily, GitHub, Telegram)

---

## ✅ Day 7 — Satu Minggu Setelah Migrasi

### Confirmation
- [ ] Semua workflow normal berjalan (coding, research, cron)
- [ ] Tidak ada error kritis di logs (`~/.hermes/logs/errors.log`)
- [ ] Semua MCP servers stabil (tidak ada reconnect loop)
- [ ] Kanban board masih intact (tasks, lanes)
- [ ] Ekosistem Niumination masih sync (ecosystem-status.json)

### Cleanup (Setelah Confirmed)
- [ ] Hapus backup di USB: `rm -rf /Volumes/HermesAgent/.../data.backup.YYYYMMDD`
- [ ] Hapus portable venv: `rm -rf /Users/zaryu/.hermes-portable/venv`
- [ ] Update PATH di ~/.zshrc (hapus portable path)
- [ ] Update BACKLOG.md — status migrasi ✅ done
- [ ] Update AGENTS.md — path Hermes baru
- [ ] Archive folder `docs/migration-portable-to-native/` → tandai complete

---

## ✅ Extended — Upgrade ke v0.18.0 (Setelah Migrasi Stabil)

Setelah native confirmed working minimal 1 minggu:

- [ ] Backup native config: `cp -r ~/.hermes ~/.hermes.backup.pre-v018`
- [ ] Upgrade: `uv pip install --upgrade hermes-agent`
- [ ] `hermes config migrate` → auto-fix format config
- [ ] `hermes doctor --fix` → fix detected issues
- [ ] Cek: `hermes --version` → v0.18.0
- [ ] Test: kirim prompt dari Telegram → response OK
- [ ] Cek semua MCP servers masih connect
- [ ] Cek semua cron jobs masih jalan
- [ ] Cek memories & sessions masih utuh
- [ ] Jika gagal → rollback: `cp -a ~/.hermes.backup.pre-v018/* ~/.hermes/`

## 📐 Master Direction Protocol — Phase 0 (Foundation ✅)

### Apa itu?
Protocol ini adalah kerangka eksekusi master untuk seluruh ekosistem Niumination. Semua keputusan dan tindakan HERMES harus selaras dengan protocol ini.

### Prinsip Utama
1. **MASTERPLAN.md adalah blueprint final** — semua fase tereksekusi sesuai urutan, tidak ada shortcut
2. **Auto-sync wajib no_agent=true** — script mekanis, bukan LLM, untuk kendali biaya
3. **Format BACKLOG wajib parseable** — `- [STATUS] **Title** — Desc — @project`
4. **Credential cron di .env profile** — bukan di localStorage atau file proyek
5. **Setiap cron wajib workdir + profile** — path absolut, profile opencode
6. **mkdir-based lock** — bukan flock (macOS tidak punya flock)
7. **Pre-flight wajib** — gitleaks, gh auth, jq, sqlite3 sebelum fase baru

### Status Fase
| Fase | Deskripsi | Status |
|------|-----------|:------:|
| 0 | Foundation (14/14) — gitleaks, hooks, creds, dll | ✅ Done |
| 1 | Tier 1 Setup — 10 proyek AGENTS.md + BACKLOG.md | ✅ Done |
| 2.1 | health-checker.sh (script) | ✅ Done — script ada, TIDAK dijadwalkan |
| 2.2 | daily-heartbeat.sh (script) | ✅ Done — script ada, TIDAK dijadwalkan |
| 2.3 | remote-poller.sh (script) | ✅ Done — script ada, TIDAK dijadwalkan |
| 2.4 | changelog-writer.sh (script) | ✅ Done — script ada, TIDAK dijadwalkan |
| 2.5 | kanban-sync.sh + divergence detection (script) | ✅ Done — script ada, TIDAK dijadwalkan |
| 2.7 | gitleaks-weekly.sh (script) | ✅ Done — script DIHAPUS 5 Agu (CPU 721%) |
| 2.8 | Ecosystem page — Vanilla HTML + React (port 5199) | ✅ Done |
| 2.6 | issue-bridge.sh — BACKLOG→GitHub Issues sync | ✅ Done — script DIHAPUS 5 Agu |
| 2.9 | Skill Hermes ekosistem-scaffold | ✅ Done |
| 2.10 | Divergence detection (in kanban-sync.sh) | ✅ Done |
| 2.11 | generate-ecosystem-json.sh — Niu-Dash data source | ✅ Done |
| 3 | Phase 3 — Hardening validasi (6/7 ✅, 1 ⏩ skip) | ✅ Done |
| 🎯 | **Goal Besar — TEDEO T1-T4** (4 critical bugs ✅ ALL FIXED 24 Jun) | ✅ Done — committed & pushed |

> 📌 **Update Scheduler — 5 Agu 2026:** Semua launchd agents `com.niumation.*` (8 plist) **dihapus** — gitleaks (CPU overload), brain-daily-capture (file kosong), eco-collect (LOCK macet), kanban-server & mission-control (mati EX_CONFIG), health-checker/kanban-sync/changelog-writer (duplikat). Scheduler yang AKTIF sekarang:
> 1. **Cron Hermes** — `memory-checkpoint` (tiap 6 jam) → backup BACKLOG.md
> 2. **Crontab macOS** — `skills/sync-to-agents.sh` (tiap 6 jam) → sync skill bank ke Jcode + Hermes + USB
> 3. **GitHub Actions** — `update-activity.yml` (harian 08:00 UTC), `generate-readme.yml` (Senin 09:00 UTC)
>
> Script lain (`health-checker.sh`, `kanban-sync.sh`, `changelog-writer.sh`, `daily-heartbeat.sh`, `remote-poller.sh`, `eco-collect.py`) **masih ada di `scripts/` dengan path sudah diupdate** ke struktur baru, tapi **tidak terjadwal** — siap dipasang ulang jika dibutuhkan. (`gitleaks-weekly.sh` & `issue-bridge.sh` dihapus.)

### Eksekusi Selanjutnya
1. **TEDEO — ✅ T1-T4 ALL FIXED + ✅ Web deployed: https://tedeo-web.vercel.app** (13 Jul)
2. **TEDEO next** — test plan, deploy backend, mobile dev
3. **GitHub push** — ✅ niumination-workspace, niu-kanban-dash, orchestrator, Ultra
4. **Ekosistem** — ✅ eco-manifest updated (30 git + 9 non-git = 39), Niu-Dash ecosystem-status.json regenerated + pushed
5. **Pro...[truncated]
| **Phase 3 sisa** — ✅ issue-bridge (cron every 6h), cron failure simulation (⏩ skip)
| **Audit Fixes (20 Jun)** — ✅ status parsing [~], pre-commit DOX check, .gitleaks.toml custom, niu-vermilion DOX, health checker 10 Tier 1 |
4. **Scoreboard update** — sync BACKLOG scoreboard dengan realita

---

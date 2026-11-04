# Roadmap Pekerjaan — MIRAI & Ekosistem Niumination

Tanggal: 2026-11-04
Basis: audit MIRAI + BACKLOG.md + eco-guard verify + cron status

## Ringkasan Audit MIRAI

| Aspek | Status | Detail |
|---|---|---|
| Server :8800 | 🟢 Running | Python 3.9 stdlib, LaunchAgent aktif |
| Health | 🟢 20/20 PASS | CPU 45.8%, load 4.3/5.7/4.5 |
| Memory display | ⚠️ 0.0 GB | Bug display, bukan masalah fungsional |
| Agents | 11 ready | Semua status ready |
| Threads | 12 aktif | Termasuk Orkestrator (13902) |
| Cron jobs | 24 active, 0 paused | Semua model → combo-delegasi (9router) |
| A2A peer | 🟢 Online | cloud @ 100.65.20.34:9900 |
| Skill bank | 253 skills | 0 mismatch |
| Disk | 26% used, 34 GB free | Post-cleanup |

## Roadmap Prioritas

### P1 — Eksekusi Segera (1-3 hari)

| # | Pekerjaan | Owner | Thread | Status |
|---|---|---|---|---|
| 1 | **Edu Content Phase 2** — quiz (SurveyJS), bab 2-3, deploy Cloudflare Pages | ED | 12707 | 4/4 bab selesai, deploy pending |
| 2 | **sapa-ai dev→main promotion** — 7 butir lanjutan (P8-P16) | AS | 8853 | dev 0.2.0-dev siap, gerbang hijau |
| 3 | **asn-admin skill build** — 5 skill asn-* [TO BUILD] | AS | 8853 | Jalur A DOCX+PDF berfungsi |
| 4 | **niu-oss-dashboard fase 4 go-live** | BD | — | landing + dashboard OSS 91 repo ready |
| 5 | **DR Snapshot repair** — fix build L1 (aset Release terenkripsi) | CR | 12595 | Script error, 2 failures |

### P2 — Jangka Pendek (1-2 minggu)

| # | Pekerjaan | Owner | Detail |
|---|---|---|---|
| 6 | **cc-acehtengah reactivation** — restore dari hiatus | AS | Repo archived, folder lokal dihapus |
| 7 | **hypr-rust M3** — keyboard-first batch tiling | BD | M1+M2 merged, native verify PASS |
| 8 | **niu-cast v3.6.0** — Mac Connect Bridge | BD | Active |
| 9 | **uacc** — Universal AI Computer Control MCP | BD | Active |
| 10 | **didong-code** — Electron ADE Gayo | BD | Active |
| 11 | **Skill bank audit detail** — 253 skills, cek duplikat/stale | QA | Pending |
| 12 | **Eco-guard findings** — 13 perhatian (state.db prune, uv cache, request_dump, vault encrypt) | CR | Scheduled |

### P3 — Jangka Menengah (2-4 minggu)

| # | Pekerjaan | Detail |
|---|---|---|
| 13 | **niu-oss-dashboard CVE hardening** — CVE-2025-66478 tertutup, fase 4 go-live |
| 14 | **landing-web-id deploy** — niumination.web.id (Vercel ready) |
| 15 | **spatial-vision** — Rust/WASM 3D vision |
| 16 | **mata-aihackfest-2026** — Watchdog akuntabilitas pengadaan |
| 17 | **TEDEO-Kanban** — 95% selesai |
| 18 | **niu-flow** — remote only |

### Blocked / Perlu Keputusan Owner

| # | Item | Alasan | Tindakan |
|---|---|---|---|
| B1 | MIRAI memory display 0.0 GB | Bug display | Fix di server.py |
| B2 | Hermes state.db 421 MB | Perlu prune manual | `hermes sessions prune --older-than 90d` |
| B3 | uv cache 871 MB | Perlu approval | `eco-guard.sh prune --apply` |
| B4 | vault/ 13 artefak tanpa enkripsi | Perlu passphrase | Enkripsi dengan age |
| B5 | Screen Recording agent-desktop | TCC granted tapi internal check false | Mac restart |
| B6 | 2 open PRs | Perlu review/merge | Review manual |

## Delegasi Orkestrasi — Siap Pakai

| Mekanisme | Status | Keterangan |
|---|---|---|
| Orkestrator (13902) | 🟢 Ready | Memecah → delegasikan → verifikasi → lapor |
| Delegate Task | ✅ | Subagent isolated context |
| A2A (Mac↔Cloud) | ✅ Verified | lightvela online |
| Kanban | ✅ | Task tracking |
| Cron delivery | ✅ 24 active | Output → thread 12595 |
| Thread scoping | ✅ 12 thread | Persona + model per thread |

## Rekomendasi Eksekusi Pertama

1. **Mulai dari Edu Content Phase 2** (ED thread 12707) — paling dekat selesai, tinggal quiz + deploy.
2. **sapa-ai promotion** (AS thread 8853) — dev siap, gerbang hijau, tinggal eksekusi.
3. **asn-admin skills** (AS thread 8853) — 5 skill [TO BUILD], format sudah siap.
4. **niu-oss-dashboard go-live** (BD) — fase 4 pending, stack siap.
5. **DR Snapshot repair** (CR thread 12595) — perbaiki build L1, jalankan manual.

Mau saya eksekusi salah satu? (sebut nomor atau "gas")
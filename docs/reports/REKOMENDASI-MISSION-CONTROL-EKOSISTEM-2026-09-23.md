# Rekomendasi Perbaikan Ekosistem Mission Control — 23 Sep 2026

**Penulis:** Researcher (thread 802)
**Status:** Laporan rekomendasi — belum dieksekusi
**Cakupan:** Kondisi real Niu-MissionControl + sintesis riset internet (multi-agent architecture, fallback routing, observability, Telegram multi-agent, launchd)

---

## 1. Ringkasan Kondisi Real (diagnosis 23 Sep 2026)

| Area | Status | Bukti |
|---|---|---|
| Server MC port 5200 | ❌ DOWN | `curl` HTTP 000, tidak ada proses `next start`/`server.py` |
| LaunchAgent MC | ❌ tidak terdaftar | `launchctl print gui/501/com.niumination.missioncontrol` → "Could not find service" |
| Penyebab terakhir down | `EADDRINUSE` | `mc.stderr.log`: "listen EADDRINUSE: address already in use 0.0.0.0:5200" |
| DB `swarm_state.db` | ✅ utuh (53 KB, 7 Sep) | yang dibutuhkan server tersimpan |
| Gateway Hermes | 🟢 PID 893 | dari `~/src/hermes-agent/` |
| 9router | 🟢 PID 1663, 718 model | catalog 104 KB JSON |
| Config.yaml vs runtime | ⚠️ KONFLIK | config masih nous lama, runtime pakai model lain |
| Thread 804 (QA) | 💤 idle 11 hari | terakhir 12 Sep (`gpt-6-astra`) |
| Thread 803 (Builder) | 💤 idle 13 hari | terakhir 10 Sep (`deepseek-v4-flash-free`) |

**Probe live 9router (23 Sep):**
- `opencode-combo` → HTTP 200 (1.44s) — resolve ke `big-pickle`
- `deepseek-v4.1-flash` → HTTP 200 (0.88s)
- `Atria-Dawn-Preview` → HTTP 404 "No active credentials for provider: openai"
- `sensenova-6.8-flash-lite` → HTTP 404 (sama)

> ⚠️ 404 pada Atria/sensenova = false negative (routing internal eksperimental `explabs/`, bukan provider nyata — pitfall skill `model-status-checker`).

---

## 2. Sintesis Riset Internet (sumber di bagian 4)

### 2.1 Multi-agent architecture
- **Supervisor pattern (orchestrator-worker)** — central coordinator menugaskan specialist, linier coordination overhead, deterministik, paling cocok untuk workflow dengan batas tugas jelas. **MC sudah menerapkan pola ini** (thread 1 = supervisor; 802/803/804/1172 = specialist).
- ⚠️ Riset Google: multi-agent **degrade 39–70%** pada sequential reasoning karena komunikasi memecah alur pikir. Multi-agent menang hanya pada tugas paralel.
- Multi-agent production gagal karena: quadratic coordination overhead + error propagation antar chain.
- Rekomendasi umum: bounded autonomy — aksi berisiko butuh approval manusia (sudah jadi hard rule di SOUL).

### 2.2 Fallback & routing model
- **LiteLLM** = open-source default (33.8k stars, 100+ model, priority fallback + cooldown); **Portkey** = observability (tampilkan model yang dicoba + alasan gagal + cost); **Bifrost** = performance (Go, ~11µs).
- 4 strategi routing: priority-based (default), latency-based, cost-optimized (tugas mudah → model murah), quality-aware.
- **Pola fallback yang benar (urut by cost):** primary → same-provider cheap → cross-provider cheap → cross-provider premium → local.
- **Circuit breaker:** ~5 kegagalan → trip, 60s cooldown, baru uji recovery.
- **Operasional:** review chain tiap kuartal; alert jika fallback menangani >5% traffic = sinyal primary bermasalah.
- **Model tiering** hemat 40–60% cost: model murah/cepat untuk triage/routing, model capable untuk reasoning kompleks.

### 2.3 Observability agent
- OpenTelemetry kini punya **GenAI semantic conventions** (`gen_ai.*`) — standar lintas framework.
- Tool agent tracing 2026: Langfuse (self-hosted gratis), Arize Phoenix, Laminar, Langtrace, Uptrace.
- 4 pilar agent observability: **Monitoring, Tracing, Evaluation, Governance**.
- Data Hermes `state.db` (sessions: model, tokens, cost, latency) sudah merupakan fondasi telemetry — tanpa tool tambahan.

### 2.4 Telegram multi-agent
- Telegram menjadi "front door" default untuk AI agents (baca: `pub.towardsai.net` + Hermes issue #10452).
- **Session isolation** = kritis: tiap agent/persona punya lane & state sendiri (OpenClaw docs) — MC threads 1/802/803/804/1172 sudah mengikuti pola ini.
- Komunikasi antar-agent via dispatch endpoint = SPOF saat MC down; Hermes issue #10452 menyarankan kanban/task-board layer.

### 2.5 macOS launchd
- `KeepAlive` = restart otomatis saat proses mati, TAPI **tidak ada health-check port bawaan** — perlu watchdog eksternal untuk service HTTP (Apple docs + apple.stackexchange).

---

## 3. Rekomendasi Perbaikan (urut prioritas)

### P0 — Kendalikan kerusakan (satu sesi)
1. **Perbaiki start MC — guard `EADDRINUSE`.**
   Ubah `services/niu-mission-control/start.sh`: sebelum `next start`, jalankan `lsof -ti :5200 | xargs kill` (atau `pkill -f "next start"`). Ini akar penyebab down terakhir — proses lama masih pegang port, start baru gagal.
2. **Daftarkan ulang LaunchAgent** `com.niumination.missioncontrol` + tambah `KeepAlive=true` + `ThrottleInterval` secukupnya (mis. 10s) agar auto-restart crash tidak jadi restart-loop. Pastikan plist memakai `start.sh` yang sudah di-guard (P0-1).
3. **Tambah watchdog health-check** (cron tiap 5 menit): `curl -sf http://localhost:5200/api/mc/health` → jika gagal, jalankan start.sh. launchd tidak bisa cek port; watchdog inilah yang menutup celahnya.

### P1 — Selaraskan model mapping (config = sumber kebenaran)
4. **Refresh `config.yaml` channel_overrides** sesuai runtime aktual yang sudah terverifikasi HTTP 200, kecuali user memilih model lain. Saat ini config masih menunjuk `nous/*` lama padahal runtime 802=opencode-combo, 1172=sensenova-6.8-flash-lite, 1=Atria-Dawn-Preview.
5. **Batasi mapping ke active namespaces** (`explabs/`, `ag/`, `claude-combo`) — jangan `gh/`, `kr/`, `gemini/`, `experimentallabs/` (skill `9router-model-mapping` rule 3).
6. **Fallback chain urut by cost + lintas quota:** primary → same-namespace cheap → cross-provider cheap. Pastikan tidak ada dua model berbagi quota backend yang sama di chain (rule 9router-model-mapping checklist).
7. **Probe ulang mapping tiap pemakaian** dengan `scripts/stress-test-models.py` (8x request, parser SSE) — jangan andalkan data probe lama.

### P2 — Observability tanpa tambahan framework (ponytail: pakai yang sudah ada)
8. **Jadikan `state.db` + `swarm_state.db` sebagai telemetry source.** Dashboard MC sudah punya endpoint `/api/mc/cost`, `/api/mc/agents`, `/api/mc/hermes/sessions` — cukup pastikan server hidup, lalu tambah panel "model drift" (config vs runtime) + "cost per thread" dari data yang sudah tersedia.
9. **Alert fallback/downtime:** hitung error rate dari `data/logs/errors.log` + `state.db` (sudah ada pola endpoint `/api/mc/errors` di `server.py`).

### P3 — Operasional & governance
10. **Hidupkan kembali thread 804 (QA) & 803 (Builder)** atau tandai sengaja idle. 11–13 hari tanpa aktivitas menandakan role tidak terpakai — konfirmasi ke user: pertahankan atau ubah mapping-nya.
11. **Simulasi outage bulanan** (chaos engineering) — matikan provider utama sengaja, verifikasi fallback berfungsi. Dari riset: jangan tunggu outage nyata untuk tahu fallback patah.
12. **Aktifkan git hook secret-scan** di repo: `git config core.hooksPath .githooks` (rule DOX root; mencegah insiden 16 Sep terulang).

### P4 — Pilihan jangka menengah (opsional, bukan sekarang)
13. **Cross-agent dispatch tanpa SPOF:** ganti/dukung endpoint HTTP `/api/mc/dispatch` dengan task-board SQLite yang di-poll agent (blackboard pattern) — tetap satu DB, tapi tidak bergantung server HTTP hidup. Hanya jika dispatch jadi kebutuhan rutin.
14. **Framework orchestration (LangGraph/CrewAI/OpenAI Agents SDK)** — **TIDAK direkomendasikan sekarang.** 5 agent dengan peran tetap sudah pas dengan supervisor pattern manual + Telegram threads. Framework menambah state management & checkpointing yang belum dibutuhkan (skala kecil, koordinasi sederhana). Evaluasi ulang jika agent >10 atau workflow branching kompleks.
15. **OTel/Langfuse** — tunda. Telemetry dari state.db cukup untuk scale ini; tambahkan hanya jika butuh trace lintas tool/provider yang tidak bisa direkonstruksi dari SQLite.

---

## 4. Sumber Riset

1. **Openlayer** — Multi-agent system architecture guide (Mar 2026): supervisor/hierarchical/P2P/blackboard/swarm pattern, koordinasi overhead, bounded autonomy. https://www.openlayer.com/blog/multi-agent-system-architecture-guide
2. **GuruSup** — Best multi-agent frameworks 2026: LangGraph/CrewAI/OpenAI Agents SDK/Google ADK/Claude SDK; model tiering hemat 40–60%. https://gurusup.com/blog/best-multi-agent-frameworks-2026
3. **BuildMVPFast** — LLM Fallback Strategies 2026: pola fallback urut cost, circuit breaker (5 failure/60s), alert fallback >5%, LiteLLM/Portkey/Bifrost. https://www.buildmvpfast.com/blog/llm-fallback-strategies-primary-model-secondary-model-2026
4. **Braintrust** — Best LLM routers 2026: OpenRouter fallback limitations, Portkey circuit breakers. https://www.braintrust.dev/articles/best-llm-routers-2026
5. **Langfuse** — Open-Source AI Agent Framework comparison (Jul 2026): tabel 13 framework, observability integration. https://langfuse.com/blog/2025-03-19-ai-agent-comparison
6. **OpenTelemetry** — GenAI Observability (Mei 2026): `gen_ai.*` semantic conventions. https://opentelemetry.io/blog/2026/genai-observability/
7. **Uptrace** — OTel for AI Systems: agent observability metrics. https://uptrace.dev/blog/opentelemetry-ai-systems
8. **Confident AI** — Best AI agent observability tools 2026. https://www.confident-ai.com/knowledge-base/compare/best-ai-agent-observability-tools-2026
9. **OpenClaw Docs** — Multi-agent routing & session isolation. https://docs.openclaw.ai/concepts/multi-agent
10. **Hermes Agent issue #10452** — Multi Telegram bots routing: session isolation, kanban/role routing layer. https://github.com/NousResearch/hermes-agent/issues/10452
11. **Towards AI** — Telegram as default front door for AI agents. https://pub.towardsai.net/telegram-is-quietly-becoming-the-default-front-door-for-ai-agents-e0ba57a5b681
12. **Apple Developer** — Creating Launch Daemons and Agents: `KeepAlive` behavior. https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
13. **Apple StackExchange** — Restart launchd service when port stops responding (watchdog pattern). https://apple.stackexchange.com/questions/467724

---

## 5. Bukti Diagnosis di Mesin

```bash
# Server MC down
curl -s -o /dev/null -w "HTTP %{http_code}\n" --max-time 10 http://localhost:5200/api/mc/health
# → HTTP 000 (connection refused)

# LaunchAgent tidak terdaftar
launchctl print gui/501/com.niumination.missioncontrol
# → Bad request. Could not find service

# Akar penyebab dari log
tail -20 ~/Desktop/Niumination/brain/ops/mc.stderr.log
# → Error: listen EADDRINUSE: address already in use 0.0.0.0:5200

# Probe 9router live
curl -s http://localhost:20128/v1/chat/completions -H "Authorization: Bearer $NINE_ROUTER_API_KEY" -d '{"model":"opencode-combo","messages":[{"role":"user","content":"OK"}],"max_tokens":1}'
# → HTTP 200 (opencode-combo), HTTP 404 (Atria-Dawn-Preview, sensenova-6.8-flash-lite)

# Runtime model per thread (state.db, last 7d)
# 802=opencode-combo (22:52), 1=Atria-Dawn-Preview (22:52), 1172=sensenova-6.8-flash-lite (22:46),
# 804=gpt-6-astra (12 Sep), 803=deepseek-v4-flash-free (10 Sep)
```

---

## 6. Langkah Eksekusi yang Diminta Approval

| # | Aksi | Risiko |
|---|---|---|
| 1 | Edit `start.sh` + guard kill port | Rendah — file lokal, reversible |
| 2 | Daftarkan ulang LaunchAgent MC | Rendah — service lokal |
| 3 | Tambah watchdog cron health-check | Rendah — cron baca saja |
| 4 | Refresh `config.yaml` channel_overrides | Sedang — mapping aktif berubah, perlu backup |
| 5 | Probe ulang model mapping | Rendah — read-only |
| 6 | Aktifkan git hook secret-scan | Rendah — `.githooks` ada di repo |

Status: MENUNGGU approval owner ("gas"/"kerjakan") sebelum eksekusi.
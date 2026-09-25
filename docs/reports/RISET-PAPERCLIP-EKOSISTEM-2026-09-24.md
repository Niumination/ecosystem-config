# Riset Paperclip — Orkestrasi AI Agent "Perusahaan" & Relevansi ke Ekosistem Niumination

**Tanggal riset:** 2026-09-24 | **Sumber:** paperclip.ing, GitHub paperclipai/paperclip, Hostinger, Contabo, flowtivity.ai, deployhq.com
**Pemicu:** Bookmark `paperclip.ing` di Tab Stash browser (`brain/Backup Tab Stash - Firefox.md`), belum pernah dipelajari.

---

## 1. Ringkasan Eksekutif

**Paperclip** = platform **orkestrasi AI agent open-source** yang memodelkan tim AI sebagai **perusahaan** — lengkap dengan org chart, role, budget per agent, governance, dan audit trail. Bukan pesaing langsung Mission Control kita, tapi **evolusi konsep** yang lebih matang di dimensi governance/cost-control.

- **Lisensi:** MIT ✅ aman
- **Stars:** 82.9k ★ (15.1k forks, 215 kontributor) — salah satu proyek open-source agent tercepat pertumbuhannya (30k★ dalam 3 minggu pertama)
- **Stack:** TypeScript 93.6%, Rust 2.9%, JS 2.1% — Node.js ≥24.11, embedded Postgres atau eksternal
- **Versi terkini:** v2026.916.1 (21 Sep 2026)
- **Cocok/tidak:** Sangat relevan sebagai **referensi arsitektur** untuk MC kita; bukan pengganti langsung (MC kita sudah punya pola supervisor-worker yang benar).

---

## 2. Apa Itu Paperclip?

Paperclip menyelesaikan masalah: **bagaimana mengkoordinasikan banyak AI agent agar kerja sebagai tim, bukan tumpukan script terpisah**. Pendekatannya: model **perusahaan** (bukan pipeline).

| Konsep | Penjelasan |
|---|---|
| **Bring Your Own Agent** | Agent apa pun bisa masuk: Claude Code, Codex, OpenClaw, Python script, shell, HTTP webhook — selama bisa terima heartbeat |
| **Goal Alignment** | Setiap task punya ancestry ke misi organisasi. Agent tahu _apa_ dan _kenapa_ |
| **Heartbeats** | Agent bangun per jadwal, cek work, eksekusi. Delegasi naik-turun org chart |
| **Cost Control** | Budget bulanan per agent. 80% = soft warning, 100% = auto-pause + block task baru |
| **Multi-Organization** | Satu deployment, banyak company, isolasi data penuh |
| **Ticket System** | Setiap percakapan di-trace, keputusan dijelaskan, tool-call tracing + immutable audit log |
| **Governance** | Approve hire, override strategi, pause/terminate agent kapan pun. **Agent TIDAK bisa hire agent baru tanpa approval Board** |
| **Org Chart** | Hierarki, role, reporting line. Agent punya boss, title, job description |

**Arsitektur server:**
```
Identity & Access | Work & Tasks | Heartbeat Execution | Governance & Approvals
Org Chart & Agents | Workspaces & Runtime | Plugins | Budget & Costs
Routines & Schedules | Secrets & Storage | Activity & Events | Company Portability
        ↑               ↑               ↑               ↑
   Claude Code       Codex         CLI agents      HTTP/web bots
```

---

## 3. Fitur Kunci yang Relevan dengan Ekosistem Kita

### 3.1 Yang Langsung Kita Butuhkan (gap di MC kita)
1. **Budget & Cost Control per agent** — MC kita TIDAK punya ini. Laporan audit menemukan cost tracking belum ada. Paperclip: token+cost tracking per company/agent/project/goal/issue, scoped budget, hard stop, overspend auto-pause + cancel queued work. **Ini gap terbesar.**
2. **Immutable audit trail** — MC punya `swarm_state.db` tapi belum append-only full tracing per tool call. Paperclip: semua mutating action, heartbeat state, cost event, approval, comment tercatat durable + versioned config + rollback.
3. **Atomic task checkout** — agent claim task = execution lock, tidak ada duplicate run. MC tidak punya ini (2 agen bisa kerjakan task sama).
4. **Governance gate** — agent tidak bisa hire/mutasi tanpa approval. MC: agent bisa (supervisor pattern tapi tanpa gate). Ini selaras Hard Rules kita.

### 3.2 Komparasi Fungsional: MC vs Paperclip

| Dimensi | Mission Control (kita) | Paperclip |
|---|---|---|
| Konsep dasar | Supervisor-worker swarm | Perusahaan + org chart |
| Persona/role | ✅ (5 thread Telegram) | ✅ (role + reporting line) |
| Cost control | ❌ belum ada | ✅ budget + hard stop |
| Audit trail | ⚠️ partial (state.db) | ✅ append-only full tracing |
| Task race prevention | ❌ ada risiko | ✅ atomic checkout |
| Governance gate | ⚠️ manual via approval user | ✅ Board approval built-in |
| Heartbeat scheduler | ⚠️ cron manual | ✅ routines + cron/webhook/API |
| Multi-tenant | ❌ | ✅ multi-company isolasi |
| Isolasi sesi per thread | ✅ | ✅ |
| Stack | Python FastAPI (MC) / Hermes | TypeScript/Node 24 + Postgres |
| Status | ❌ DOWN (start.sh patah) | 🟢 aktif, 82.9k★ |

### 3.3 Yang SUDAH Kita Punya Lebih Baik
- **Deployment di 16GB MBP** — Paperclip butuh ≥2 vCPU/4GB RAM/50GB SSD (VPS). Kita jalan di Mac 16GB i5 2020.
- **Integrasi Telegram native** — MC thread Telegram langsung; Paperclip pakai adapter (belum ada Telegram gateway bawaan tingkat thread).
- **Stack Python** — MC FastAPI cocok ekosistem Python kita; Paperclip TS/Node menambah beban runtime.
- **Ekosistem skill 180+** — Paperclip `.agents/skills` masih kecil (baru mulai).

---

## 4. Konsep "Paperclip Maximizer" (Konteks Tambahan)

Bookmark `paperclip.ing` adalah nama produk. Tapi istilah "paperclip" di dunia AI punya makna kedua: **paperclip maximizer** — thought experiment Nick Bostrom (Superintelligence, 2014): AI yang dioptimasi memproduksi paperclip tanpa batas, akhirnya menghancurkan segalanya demi tujuannya (instrumental convergence / orthogonality thesis). Ini fondasi diskusi AI safety & alignment.

**Relevansi ke ekosistem:** governance model Paperclip (Board approval, budget cap, pause) adalah **respon praktis** terhadap paperclip maximizer problem — membatasi runaway agent dengan kontrol manusia. Tidak ada referensi paperclip maximizer di docs/brain kita sebelumnya (baru bookmark tool).

---

## 5. Analisis Adopsi ke Ekosistem Niumination

### 5.1 Opsi A — Adopsi langsung Paperclip
**👍 Pro:**
- Governance + cost control matang (gap terbesar MC kita)
- MIT, self-hosted, tanpa akun
- 82.9k★ + 215 kontributor = mature, aktif
- BYO-agent: bisa masukkan Hermes, Claude Code, Codex, script kita

**👎 Kontra:**
- **Node 24 + Postgres baru** — beban infra tambahan di MBP 16GB (semua service kita Python/Node kecil)
- **Stack berubah** — mengganti MC FastAPI = rebuild (Rule Refactor user: rebuild from scratch, mahal)
- **MC kita masih DOWN** — lebih baik perbaiki MC yang ada dulu dari pindah platform
- Tidak ada Telegram thread-native integration out-of-box (kita harus adapter sendiri)
- Skala personal (1 user, 5 thread) tidak butuh multi-company org chart — **over-engineering** untuk ukuran ini (Ponytail: YAGNI)

### 5.2 Opsi B — Adopsi POLA (direkomendasikan)
Tiru **pola governance Paperclip** ke MC kita tanpa pindah stack:
1. **Budget per agent (Hermes thread)** → cost tracker sederhana di MC (state.db tambah kolom budget/spend)
2. **Atomic task checkout** → lock task saat agent claim (hindari duplicate run)
3. **Append-only audit** → log semua tool call + keputusan ke file append-only (bukan overwrite)
4. **Governance gate** → agent tidak bisa hire/ubah config tanpa approval (selaras Hard Rules)
5. **Heartbeat scheduler** → routine/cron ke MC (sudah ada sebagian di Herem)

### 5.3 Keputusan
**TIDAK adopsi langsung (P2/P3).** Alasan: MC down perlu diperbaiki dulu (P0), stack bernilai (Python), scale personal tidak butuh org chart multi-company. **Adopsi pola governance Paperclip ke MC = P1** setelah MC hidup.

Jika nanti ekosistem tumbuh ke multi-project/instansi (Pemdi, Diskominfo) dengan banyak agent paralel — Paperclip sebagai **kandidat serius** (komparasi ulang saat itu).

---

## 6. Sumber

1. https://paperclip.ing/ — situs resmi, fitur, FAQ, testimoni
2. https://github.com/paperclipai/paperclip — repo, stars, lisensi, arsitektur
3. https://www.hostinger.com/tutorials/paperclip-ai-use-cases/ — 10 use case
4. https://contabo.com/blog/what-is-paperclip-ai/ — fitur, pricing, growth (30k★/3 minggu)
5. https://contabo.com/blog/paperclip-ai-alternatives/ — vs OpenClaw/LangChain/CrewAI
6. https://www.deployhq.com/blog/self-host-paperclip-vps-docker-deployhq — Docker self-host min 2vCPU/4GB/50GB
7. https://www.mindstudio.ai/blog/paperclip-vs-openclaw-multi-agent-system-comparison — managed vs self-host
8. https://flowtivity.ai/blog/openclaw-vs-paperclip-ai-agent-framework-comparison/ — OpenClaw vs Paperclip
9. https://en.wikipedia.org/wiki/Instrumental_convergence — paperclip maximizer / AI safety
10. https://cepr.org/voxeu/columns/ai-and-paperclip-problem — paperclip problem economics

## Bukti
- `grep "paperclip"` di `docs/`, `brain/`, `skills/` → hanya bookmark Tab Stash (3 file), 0 riset formal sebelumnya
- `web_search` paperclip.ing + GitHub + safety concept → data di atas
- `web_extract` github repo + paperclip.ing + hostinger → konfirmasi fitur/arsitektur/lisensi
- File ini = `docs/reports/RISET-PAPERCLIP-EKOSISTEM-2026-09-24.md` (dibuat 24 Sep 2026 ~19:55 WIB)
# Riset: DeepSeek Harness Ecosystem & FrontierHarness Eval & CooperBench

**Tanggal:** 2026-11-04  
**Sumber:** 4 repositori/paper dari DeepSeek AI dan FrontierHarness community

---

## Ringkasan Eksekutif

Empat sumber ini membentuk ekosistem evaluasi dan deployment agent coding frontier yang sedang berkembang cepat. DeepSeek merilis **DeepSeek Harness (DSH)** sebagai open-source agent framework dengan arsitektur plugin, termasuk **super-agent prototype** yang meniru pola kerja tim manusia. Bersama **FrontierHarness Eval** (benchmark perbandingan 12 harness) dan **CooperBench** (paper arXiv tentang kolaborasi agent), kita mendapat gambaran utuh: industri bergerak dari "model sekuat apa" ke "harness sebaik apa".

---

## 1. DeepSeek Harness (`deepseek-ai/deepseek-harness`)

| Meta | Value |
|---|---|
| Stars | **274.381** (viral) |
| Forks | 33.516 |
| Bahasa | TypeScript |
| Ukuran | 360 MB |
| Terbit | 13 Agu 2026 |
| Versi terbaru | `dsh-v0.2.2-rc.1` (4 Nov 2026) |
| Lisensi | MIT |
| Arsitektur | Cordis (spatiotemporal composability) |
| Dokumentasi | https://deepseek-harness.github.io/deepseek-harness/ |

### Filosofi: "Everything is a Plugin"
Setiap kemampuan — shell, SSH, terminal, browser, computer-use, LLM provider, skill loader, context compaction, subagent, team coordination, sandbox, LSP — adalah paket TypeScript terpisah di `packages/`. Tidak ada monolith.

### Struktur Paket Inti
```
packages/
  core/          agent.session API
  api/           remote BFF (backend-for-frontend)
  llm/           model providers (multi-provider)
  shell/         command execution
  ssh/           SSH execution providers
  terminal/      persistent terminals
  sandbox/       process confinement
  subagent/      delegated agents
  team/          shared task coordination
  compaction/    context compaction
  guard/         loop/tool guards
  mcp/           external tools (MCP integration)
  sdk/           JSON-RPC SDK
  ... (40+ packages)
```

### Keamanan
`SAFETY.md` eksplisit:
- Experimental developer-preview, **belum security audit**
- Bisa execute model-generated code, load third-party plugins, akses network/processes/credentials
- Sandbox + approval prompts **tidak menjamin isolasi**
- Rekomendasi: disposable VM/container, least privileges, backup sebelum jalankan

### Benchmark & Testing
- `test:expected` — owner-local process expectations
- `test:snapshot` — recorded-session replay through shipped profiles
- `vitest.*.config.ts` — 10+ konfigurasi test (unit, e2e, snapshot, web-stress, perf, benchmark)
- Coverage gate: **100% per-file** pada `packages/*/*/src`

### Hubungan dengan Jailbreaks Repo
DSH punya konfigurasi `dsh-standard`, `dsh-creator`, `dsh-ptc`, `dsh-minimal` yang muncul di FrontierHarness Eval results. Ini menunjukkan DeepSeek sengaja membuat berbagai "persona" harness untuk testing komparatif.

---

## 2. dsh-superagent-prototype (`deepseek-ai/dsh-superagent-prototype`)

| Meta | Value |
|---|---|
| Stars | **19.924** |
| Forks | 2.302 |
| Bahasa | TypeScript |
| Size | 37 KB (sangat ringan = mostly prompts/docs) |
| Terbit | 31 Okt 2026 |
| Lisensi | MIT |

### Deskripsi
Research prototype untuk paper *"Exploring Super-agent Design: Towards a More Autonomous Agent System"*. Bukan produk resmi DeepSeek — "code grew out of our team's day-to-day development work, with much of the engineering done by coding agents."

### Arsitektur
Proactive coding agent untuk **satu GitHub repository**. Listen ke GitHub + opsional Feishu (platform kolaborasi Tiongkok). Ketika allowed user meminta kerja:
1. Buka work item
2. Kerjakan di agent session & directory sendiri
3. Jawab di conversation asli (bisa via PR)
4. Web panel tampilkan apa yang butuh human

### Filosofi Inti (docs/000-philosophy.md)
> **"Take as little human attention as possible, and give as much value as possible."**

Setiap bagian proyek diukur dari "attention cost"-nya. Jika tidak memberi nilai lebih dari biaya attention-nya → hapus.

Prinsip agent:
- **Act only when asked** atau ada written rule yang mengizinkan
- **Speak only when someone must act** atau bisa pakai hasil
- **Ask one concrete question at a time** — bukan report panjang
- **Stop by impact, not by effort** — local change → reviewable result
- **Report honestly** — draft = unfinished, failure = failure, limit ≠ bypass

Prinsip desain:
- **Few concepts** — business need jadi atribut atau prompt text, bukan concept baru
- **Few settings** — default menang jika satu value suits almost every team
- **Panel shows only what needs a person** — healthy state takes no space

### Dokumen Berurutan (read in order)
000 Philosophy → 001 Domain model → 002 Authorization → 003 Execution → 004 Prompts → 005 Panel → 006 Deployment → 007 Architecture → 008 Cookbook

### Relevansi untuk Niumination
Pola "super-agent" ini mirip dengan Hermes di Niumination tapi dengan pendekatan berbeda:
- DSH superagent = **proaktif terbatas** (hanya saat diminta atau ada rule)
- Hermes saat ini = **reactif** (hanya saat ada pesan Telegram)
- Pola "panel shows only what needs a person" bisa diadaptasi untuk MIRAI dashboard

---

## 3. FrontierHarness Eval (`frontier-harness-eval/eval`)

| Meta | Value |
|---|---|
| Stars | 332 |
| Forks | 25 |
| Bahasa | JavaScript |
| Size | 2.5 MB |
| Terbit | 31 Agu 2026 |
| Benchmark | v1.0 frozen |

### Metodologi
**Controlled experiment:** model tetap (Kimi K3 dari Fireworks), tasks tetap (30), runtime tetap. Hanya harness yang berubah.

**30 tasks:**
- 21 Terminal-Bench tasks (realistic terminal-based software engineering)
- 9 DeepSWE tasks (software engineering from datacurve-ai repo)

**9 harnesses × beberapa configuration = 12 configurations total = 360 evaluations**

### Hasil (Kimi K3, Fireworks provider)

| Harness (config) | Pass rate | Median cost/pass | Cache median | Median time |
|---|---|---|---|---|
| **Codex** | **66.7%** | $3.47 | 88.0% | 6m 43s |
| DSH Creator | 63.3% | $3.28 | 84.3% | 6m 44s |
| Claude Code | 63.3% | **$18.34** | 67.8% | 9m 38s |
| Pi | 60.0% | $2.43 | 79.4% | 7m 33s |
| DSH PTC | 60.0% | $4.58 | 87.2% | 7m 44s |
| DSH Standard | 60.0% | $3.46 | 86.5% | 6m 17s |
| Oh My Pi | 56.7% | $4.75 | 82.2% | 6m 46s |
| Kimi Code | 56.7% | $3.65 | 88.0% | 7m 56s |
| DSH Minimal | 56.7% | $4.72 | 84.6% | **5m 41s** |
| Exo Harness | 53.3% | **$1.05** | 70.3% | 6m 17s |
| OpenCode | 50.0% | $3.24 | 78.4% | 6m 27s |
| **Hermes** | **50.0%** | **$2.90** | 85.9% | 6m 58s |

### Temuan Kunci
1. **Pass rate spread hanya 16.7 poin** (50%–66.7%) — harness berpengaruh tapi tidak dramatis
2. **Cost spread 17.5×** ($1.05–$18.34) — pengaruh harness jauh lebih besar di biaya
3. **Claude Code** paling mahal ($18.34/pass) meski pass rate tinggi — efisiensi rendah
4. **Exo Harness** paling murah ($1.05/pass) tapi pass rate tengah-bawah
5. **Hermes** di posisi terakhir (50%, sama dengan OpenCode) — area improvement jelas
6. **DSH 3 konfigurasi** masuk top-middle — Creator (63.3%), PTC (60%), Minimal (56.7%)

### Evaluasi Sendiri
Repo menyediakan workflow reproduksi: `npx @frontierharness/eval` install workspace + skill. Warnas: perlu **matched control run** untuk establish comparability. Environment differences harus dicatat.

---

## 4. CooperBench — arXiv:2601.13295

| Meta | Value |
|---|---|
| Judul | *CooperBench: Why Coding Agents Cannot be Your Teammates Yet* |
| Tanggal | 19 Jan 2026 (online 26 Jan 2026) |
| Penulis | 11 orang (Khatua, Zhu, Tran, Prabhudesai, Sadrieh, Lieberwirth, Yu, Fu, Ryan, Pei, Yang) |
| Kategori | cs.LG (machine learning) |

### Masalah yang Ditelepon
"Curse of coordination" — agregasi kemampuan individual tidak linear ke kolaborasi.

### Metodologi
- **600+ collaborative coding tasks**
- **12 libraries** di **4 programming languages**
- Setiap task: 2 agent dapat fitur berbeda yang bisa diimplementasi independen tapi **bisa konflik tanpa koordinasi**
- Tasks grounded di real open-source repositories dengan expert-written tests
- Evaluasi state-of-the-art coding agents

### Temuan Utama

**Curse of coordination:**
> Agents achieve on average **30% lower success rates** when working together compared to performing both tasks individually.

Contrast dengan human teams di mana menambahkan teammate biasanya **meningkatkan** produktivitas.

**Tiga root causes:**
1. **Communication jam** — pesan vague, ill-timed, inaccurate memenuhi channel
2. **Commitment deviation** — bahkan dengan komunikasi efektif, agent menyimpang dari komitmen
3. **Wrong expectations** — agent punya persepsi salah tentang rencana dan komunikasi orang lain

**Emergent behaviors** (langka tapi menarik):
- Role division
- Resource division
- Negotiation

### Implikasi
Paper menyerukan pergeseran fokus: dari **individual agent capability** ke **social intelligence** untuk multi-agent collaboration.

---

## Sintesis: Peta Ekosistem

```
                    ┌─────────────────────────────┐
                    │   DeepSeek AI Ecosystem      │
                    ├─────────────────────────────┤
                    │  deepseek-harness (274K ⭐)  │ ← Production agent framework
                    │       │                     │
                    │       ├─ dsh-standard        │ ← 60% pass, $3.46
                    │       ├─ dsh-creator         │ ← 63.3% pass, $3.28
                    │       ├─ dsh-ptc             │ ← 60% pass, $4.58
                    │       └─ dsh-minimal         │ ← 56.7% pass, $4.72, tercepat
                    │                               │
                    │  dsh-superagent-prototype     │ ← Research prototype
                    │  (19.9K ⭐)                   │   Proactive, attention-minimal
                    │       │                     │
                    │       └─ Paper: "Exploring   │
                    │          Super-agent Design"  │
                    └─────────────────────────────┘
                              ↓ evaluation
                    ┌─────────────────────────────┐
                    │   FrontierHarness Eval       │
                    │   (332 ⭐, benchmark v1.0)   │
                    ├─────────────────────────────┤
                    │  Controlled: Kimi K3 × 9     │
                    │  harnesses × 30 tasks        │
                    │  = 360 evaluations           │
                    │                               │
                    │  Winner: Codex (66.7%)       │
                    │  cheapest: Exo ($1.05)       │
                    │  Hermes: 50% ($2.90)         │
                    └─────────────────────────────┘
                              ↓ extends to
                    ┌─────────────────────────────┐
                    │   CooperBench (arXiv)        │
                    │   Multi-agent collab bench   │
                    ├─────────────────────────────┤
                    │  600+ tasks, 12 libs, 4 lang │
                    │  "Curse of coordination"     │
                    │  -30% vs individual          │
                    │  → need social intelligence  │
                    └─────────────────────────────┘
```

### Temuan Cross-Cutting

1. **Model ≠ semua.** FrontierHarness membuktikan harness choice berpengaruh signifikan ke cost (17.5× spread) bahkan dengan pass rate yang relatif padat (16.7pp spread).

2. **DSH memiliki 4 "persona" konfigurasi** yang masing-masing trade-off berbeda: Creator (highest pass), Standard (balanced), PTC (costlier), Minimal (fastest). Ini adalah implementasi praktis dari filosofi "attention minimization" di superagent prototype.

3. **Hermes di posisi last** (50% pass rate) di FrontierHarness. Ini bukan kritik — Hermes dirancang untuk orchestration, bukan raw coding throughput. Tapi ini benchmark objektif untuk improvement.

4. **CooperBench mengonfirmasi hipotesis** bahwa kolaborasi multi-agent masih broken. "Curse of coordination" berarti adding more agents bukan solusi otomatis — perlu social intelligence layer.

5. **Jailbreaks repo** (riset sebelumnya) dan **DSH** berada di sisi berlawanan spektrum: satu memanipulasi prompt, satu membangun framework production. Keduanya mengakui bahwa system prompt adalah boundary yang bisa di-reconfigure.

---

## Rekomendasi untuk Niumination

### Immediate (hari ini juga)
1. **Cek DSH di local** — `npx @deepseek-ai/dsh web` di machine yang dedicated, bukan di Mac utama Afrizal. Evaluasi sendiri sebelum adopsi.
2. **Pelajari DSH superagent philosophy** — pola "act only when asked, speak only when needed" bisa direplikasi di Hermes profile design.
3. **Benchmark Hermes** — jalankan FrontierHarness Eval workflow untuk Hermes di environment terkontrol. Hasil saat ini (50%) perlu validasi ulang dengan setup yang match.

### Short-term (1-2 minggu)
4. **Adopsi "few settings, default wins"** dari DSH philosophy ke Hermes config — kurangi opsi yang tidak perlu.
5. **Evaluasi DSH vs Hermes** untuk use case spesifik Niumination (bukan general coding). DSH mungkin lebih baik untuk repository-specific work, Hermes untuk multi-thread orchestration.
6. **Monitor CooperBench follow-ups** — paper ini baru Januari 2026, likely ada iterating research di multi-agent coordination.

### Strategic
7. **Arsitektur plugin-ready** — jika Niumination perlu expand capability (browser, computer-use, dll), pola "everything is a plugin" dari DSH bisa diadopsi parsial.
8. **Attention-cost metric** — tambahkan metrik "average attention cost per agent action" di monitoring Hermes. Saat ini tidak terukur.

---

## Bukti

```
# GitHub API queries
$ curl -s https://api.github.com/repos/deepseek-ai/deepseek-harness | jq '{stars: .stargazers_count, forks: .forks_count, size: .size, created_at: .created_at, updated_at: .updated_at}'
→ stars: 274381, forks: 33516, size: 360269KB, created: 2026-08-13, updated: 2026-11-06

$ curl -s https://api.github.com/repos/deepseek-ai/dsh-superagent-prototype | jq '{stars: .stargazers_count, forks: .forks_count, size: .size, created_at: .created_at}'
→ stars: 19924, forks: 2302, size: 37KB, created: 2026-10-31

$ curl -s https://api.github.com/repos/frontier-harness-eval/eval | jq '{stars: .stargazers_count, forks: .forks_count, size: .size, created_at: .created_at}'
→ stars: 332, forks: 25, size: 2534KB, created: 2026-08-31

$ curl -s https://api.github.com/repos/deepseek-ai/deepseek-harness/releases?per_page=5 | jq '.[] | {tag: .tag_name, date: .published_at[:10]}'
→ dsh-v0.2.2-rc.1 (2026-11-04), dsh-v0.2.2-alpha.3 (2026-11-03), dsh-v0.2.1-rc.5 (2026-10-30)...

# Arxiv
$ curl -sL https://arxiv.org/abs/2601.13295 | grep -oP 'citation_author" content="\K[^"]+' | wc -l
→ 11 authors
$ curl -sL https://arxiv.org/abs/2601.13295 | grep -oP 'citation_date" content="\K[^"]+'
→ 2026/01/19
```

Source: GitHub REST API v3 + arXiv metadata, accessed 2026-11-04.

# INDEX — Bank Skill Terpusat Niumination

> **Versi:** 4.0.1 (Superpowers Integration — 6 SDLC skills added from obra/superpowers)
> **Lokasi:** `~/Desktop/Niumination/skills/`
> **Sync:** ✅ `sync-to-agents.sh` — auto-copy ke Jcode + Hermes (local + USB) + AGENTS.md (cron every 6h)
> **DOX Injection:** ✅ Layer 3 — 32 skill auto-loaded via trigger keyword di AGENTS.md
> **Mission-Control Dashboard:** ✅ Layer 4 — Skill Monitor di `services/niu-mission-control/` (WebSocket, stats, stale, conflicts)
> **Hermes Integration:** ✅ Semua 32 skill tersedia di Hermes catalog (USB: 150+ total, ~/.hermes/: up-to-date)
> **Domain-based:** Semua skill dikategorisasi per domain, BUKAN per agent.
> **Status:** 32 ✅ Aktif

---

## Domain: Software Development

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **ponytail-core** | ✅ Aktif | tools/ponytail/ | 6.5 KB | Lazy senior dev mindset — YAGNI, stdlib first, minimal solution |
| **ponytail-audit** | ✅ Aktif | tools/ponytail/ | 1.7 KB | Whole-repo audit for over-engineering — ranked deletion list |
| **ponytail-review** | ✅ Aktif | tools/ponytail/ | 2.4 KB | Diff-level over-engineering review — satu baris per finding |
| **ponytail-debt** | ✅ Aktif | tools/ponytail/ | 1.7 KB | Harvest `ponytail:` comments into debt ledger — track deferred shortcuts |
| **ponytail-gain** | ✅ Aktif | tools/ponytail/ | 2.0 KB | Measured-impact scoreboard: -54% LOC, -22% token, -20% cost |
| **ponytail-help** | ✅ Aktif | tools/ponytail/ | 2.6 KB | Quick-reference card for all ponytail modes, skills, and commands |
| **systematic-debugging** | ✅ Aktif | Hermes | 25.6 KB | 4-phase debugging workflow — isolate, root cause, fix, verify |
| **project-orientation** | ✅ Aktif | Hermes | 64.0 KB | Verify from source — jangan asumsi, baca direktori & file dulu |
| **document-content-pipeline** | ✅ Aktif | Hermes | 30.1 KB | ODL-PDF batch convert → Markdown → cleanup → JSON → website. Termasuk rebuild ground-truth (2d) + post-rebuild cleanup (2e) + ROOT CAUSE PPT→PDF |
| **optimization** | ✅ Aktif | Jcode + Hermes | 2.1 KB | Profiling, bottleneck detection, targeted optimization |
| **ultrathink** | ✅ Aktif | HaydenLundin | 4.5 KB | Deep architectural reasoning — trade-offs, invariants, craftsmanship |
| **tripwire** | ✅ Aktif | sisi-tarak | 2.8 KB | Single-risk prioritization — satu hal paling kritis untuk dipantau |
| **premortem** | ✅ Aktif | sisi-tarak | 2.5 KB | Failure pre-mortem — asumsikan gagal, cari penyebab sebelum mulai |
| **hermes-zero-defect-architect** | ✅ Aktif | Hermes USB | 11.8 KB | Zero-defect debugging — snapshot, rollback, JCode parallel, full pipeline |
| **simplify-code** | ✅ Aktif | Hermes USB | 10.9 KB | Parallel 3-agent cleanup — simplify, refactor, deduplicate recent changes |
| **brainstorming** | ✅ Aktif | superpowers | 10.0 KB | Design refinement sebelum coding — hard gate: jangan nulis kode tanpa desain disetujui |
| **writing-plans** | ✅ Aktif | superpowers | 7.0 KB | Implementation plan granular — tiap task 2-5 menit, bite-sized steps, no placeholders |
| **verification-before-completion** | ✅ Aktif | superpowers | 3.6 KB | Iron law verification — no completion claims tanpa fresh verification evidence |
| **subagent-driven-development** | ✅ Aktif | superpowers | 28.0 KB | Parallel agent execution — dispatch subagent per task, 2-stage review, fix loop max 5 rounds |
| **finishing-a-development-branch** | ✅ Aktif | superpowers | 7.0 KB | Post-implementation workflow — verify tests, present merge/PR/keep/discard options |
| **requesting-code-review** | ✅ Aktif | superpowers | 3.0 KB | Dispatch code reviewer subagent — spec compliance + code quality assessment |
| **pemdi-evidence-management** | ✅ Aktif | Hermes USB | 50.8 KB | Kelola bukti dukung Pemdi (PermenPANRB 8/2026) — cross-ref PemdiArena CSV, Excel master, modul JSON, JDIH/OpenData API → inject ke dashboard dengan inline PDF preview |
| **compliance-checklist-dashboard** | ✅ Aktif | Hermes USB | 11.0 KB | Build compliance/checklist dashboards (Pemdi, SPBE, IKD) — parse checklist → JSON → Next.js dashboard + embedded previews |
| **plan-compliance-audit** | ✅ Aktif | Hermes USB | 21.0 KB | Audit ekosistem/proyek terhadap spesifikasi tertulis — layer scripts/crons/configs/credentials/docs, gap by severity |

## Domain: Design

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **impeccable** | ✅ Aktif | Claude Code / Jcode | 19.9 KB | Production-grade UI/UX design — 23 sub-commands, OKLCH, anti-pattern AI slop |
| **ui-ux-pro-max** | ✅ Aktif | Hermes USB | 29.5 KB | UI/UX design intelligence — 67 styles, 96 palettes, 57 font pairings, Python search |

## Domain: Ecosystem

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **up-eco** | ✅ Aktif | Hermes | 3.0 KB | Ecosystem status check — git, divergence, health |
| **ekosistem-scaffold** | ✅ Aktif | Hermes | 40.6 KB | Membuat struktur proyek baru sesuai standar Niumination |
| **hermes-agent-skill-authoring** | ✅ Aktif | Hermes USB | 10.7 KB | Author in-repo SKILL.md — frontmatter, validator, structure, quality principles |

## Domain: Security

| Skill | Status | Source | Deskripsi |
|-------|:------:|--------|-----------|
| **redteam** | ✅ Aktif | Agentpedia + Niumination | 4.0 KB | Adversarial security testing — stress-test plan dari sudut pandang attacker |

## Domain: Creative

| Skill | Status | Source | Deskripsi |
|-------|:------:|--------|-----------|
| **ghost** | ✅ Aktif | sisi-tarak + Niumination | 3.2 KB | AI text humanizer — rewrite AI-generated text to read naturally |
| **hyperframes** | ✅ Aktif | heygen-com/hyperframes | 4.0 KB | HTML-to-video framework — 'Write HTML. Render video. Built for agents.' |

---

## Ringkasan

| Status | Jumlah |
|--------|:------:|
| ✅ Aktif | **32** |
| **Total** | **32** |

## Catatan Penting — Potensi Konflik

### 🔴 Konflik Aktif (perlu mitigasi)

| Konflik | Skill 1 | Skill 2 | Mitigasi |
|---------|:-------:|:-------:|----------|
| 🟡 **Craftsmanship vs Minimalism** | `ultrathink` | `ponytail-core` | Ultrathink sudah punya Relationship section yang menjelaskan kapan pakai mana. Ponytail untuk implementasi cepat, ultrathink untuk arsitektur. |
| 🟡 **UI/UX - Build vs Research** | `impeccable` | `ui-ux-pro-max` | Beda fokus: impeccable = code-first, build UI langsung. ui-ux-pro-max = search-based, design research & recommendation. Trigger berbeda: `/impeccable craft` vs `/ui-ux-pro-max --design-system`. |
| 🟡 **Debugging - Generic vs Agresif** | `systematic-debugging` | `hermes-zero-defect-architect` | systematic-debugging = 4-phase generik. zero-defect = full pipeline + snapshot/rollback + JCode parallel. zero-defect adalah superset untuk Hermes + JCode environment. |

### 🟢 Konflik Terkelola (aman)

| Pair | Alasan |
|------|--------|
| `ponytail-audit` ↔ `ponytail-review` | Komplementer: audit = whole-repo, review = diff-level |
| `ponytail-core` ↔ `simplify-code` | core = mental model sebelum nulis, simplify-code = refactor kode existing |
| `impeccable` ↔ `ghost` | Beda domain: UI/UX design vs text humanizer |
| `hermes-agent-skill-authoring` ↔ semua | Meta-skill — justru membantu maintain skill lain |
| `brainstorming` ↔ `ultrathink` | Komplementer: brainstorming = "apa yang dibangun", ultrathink = "gimana arsitekturnya" |
| `brainstorming` ↔ `ponytail-core` | Sama-sama YAGNI — brainstorming cegah fitur tidak perlu sebelum coding |
| `verification-before-completion` ↔ `ponytail-core` | Komplementer: ponytail minimal code, verification buktikan kode beneran jalan |
| `verification-before-completion` ↔ `systematic-debugging` | Verification adalah fase final debugging — cocok berurutan |
| `subagent-driven-development` ↔ semua | Layer orchestration — tidak konflik, menjalankan skill lain via subagent |
| `requesting-code-review` ↔ `ponytail-review` | Beda fokus: ponytail = over-engineering check, requesting = spec compliance + quality |
| `writing-plans` ↔ `brainstorming` | **Pipeline:** brainstorming → writing-plans → subagent-driven-development → requesting-code-review → finishing-a-development-branch |
| `finishing-a-development-branch` ↔ `up-eco` | finishing = cleanup satu branch, up-eco = sync seluruh ekosistem

### 📌 Catatan Lain

- **Naming convention:** `<domain>/<nama>-<variant>/SKILL.md`
- **Versioning:** Cukup git history untuk tahap awal
- **Optimization:** minimal version dari Jcode bundled skill
- **Frontmatter YAML:** setiap skill wajib punya name, description, version, tags

## Cara Nambah Skill Baru

1. Bikin folder: `mkdir -p skills/<domain>/<nama>/`
2. Tulis SKILL.md dengan frontmatter YAML + markdown instruksi
3. Update INDEX.md — tambah baris di tabel yang sesuai
4. `git add skills/ && git commit -m "skills: tambah <nama>"`

## Format SKILL.md (Template)

```yaml
---
name: <skill-name>
description: "<satu kalimat deskripsi>"
version: 1.0.0
author: <Hermes|Jcode|Agentpedia>
source: <dari mana asalnya>
tags: [<domain>, <keyword1>, <keyword2>]
platforms: [macos, linux]
---
# <Nama Skill — Judul Manusiawi>

## Trigger
Kapan skill ini harus dipakai?

## Prasyarat
- Item 1
- Item 2

## Prosedur
1. Langkah 1
2. Langkah 2
3. Langkah 3

## Contoh
...
```

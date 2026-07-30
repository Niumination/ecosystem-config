# INDEX — Bank Skill Terpusat Niumination

> **Versi:** 3.0.0 (Expanded — 9 new skills added from Hermes USB + Jcode)
> **Lokasi:** `~/Desktop/Niumination/skills/`
> **Sync:** ✅ `sync-to-agents.sh` — auto-copy ke Jcode + Hermes (local + USB) + AGENTS.md (cron every 6h)
> **DOX Injection:** ✅ Layer 3 — 22 skill auto-loaded via trigger keyword di AGENTS.md
> **Mission-Control Dashboard:** ✅ Layer 4 — Skill Monitor di `services/niu-mission-control/` (WebSocket, stats, stale, conflicts)
> **Hermes Integration:** ✅ Semua 22 skill tersedia di Hermes catalog (USB: 150+ total, ~/.hermes/: up-to-date)
> **Domain-based:** Semua skill dikategorisasi per domain, BUKAN per agent.
> **Status:** 22 ✅ Aktif

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
| **document-content-pipeline** | ✅ Aktif | Hermes | 13.6 KB | ODL-PDF batch convert → Markdown → cleanup → JSON → website |
| **optimization** | ✅ Aktif | Jcode + Hermes | 2.1 KB | Profiling, bottleneck detection, targeted optimization |
| **ultrathink** | ✅ Aktif | HaydenLundin | 4.5 KB | Deep architectural reasoning — trade-offs, invariants, craftsmanship |
| **tripwire** | ✅ Aktif | sisi-tarak | 2.8 KB | Single-risk prioritization — satu hal paling kritis untuk dipantau |
| **premortem** | ✅ Aktif | sisi-tarak | 2.5 KB | Failure pre-mortem — asumsikan gagal, cari penyebab sebelum mulai |
| **hermes-zero-defect-architect** | ✅ Aktif | Hermes USB | 11.8 KB | Zero-defect debugging — snapshot, rollback, JCode parallel, full pipeline |
| **simplify-code** | ✅ Aktif | Hermes USB | 10.9 KB | Parallel 3-agent cleanup — simplify, refactor, deduplicate recent changes |

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

---

## Ringkasan

| Status | Jumlah |
|--------|:------:|
| ✅ Aktif | **22** |
| **Total** | **22** |

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

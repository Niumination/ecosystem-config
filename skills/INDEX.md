# INDEX — Bank Skill Terpusat Niumination

> **Versi:** 2.0.0 (Layers 1-4 ✅ ALL COMPLETE — Hermes integration verified)
> **Lokasi:** `~/Desktop/Niumination/skills/`
> **Sync:** ✅ `sync-to-agents.sh` — auto-copy ke Jcode + Hermes (local + USB) + AGENTS.md (cron every 6h)
> **DOX Injection:** ✅ Layer 3 — 13 skill auto-loaded via trigger keyword di AGENTS.md
> **Mission-Control Dashboard:** ✅ Layer 4 — Skill Monitor di `services/niu-mission-control/` (WebSocket, stats, stale, conflicts)
> **Hermes Integration:** ✅ Semua 13 skill tersedia di Hermes catalog (USB: 150 total, ~/.hermes/: up-to-date)
> **Domain-based:** Semua skill dikategorisasi per domain, BUKAN per agent.
> **Status:** 13 ✅ Aktif

---

## Domain: Software Development

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **ponytail-core** | ✅ Aktif | tools/ponytail/ | 6.5 KB | Lazy senior dev mindset — YAGNI, stdlib first, minimal solution |
| **ponytail-audit** | ✅ Aktif | tools/ponytail/ | 1.7 KB | Ponytail variant untuk audit kode — review diff, deteksi over-engineering |
| **systematic-debugging** | ✅ Aktif | Hermes | 25.6 KB | 4-phase debugging workflow — isolate, root cause, fix, verify |
| **project-orientation** | ✅ Aktif | Hermes | 64.0 KB | Verify from source — jangan asumsi, baca direktori & file dulu |
| **document-content-pipeline** | ✅ Aktif | Hermes | 13.6 KB | ODL-PDF batch convert → Markdown → cleanup → JSON → website |
| **optimization** | ✅ Aktif | Jcode + Hermes | 2.1 KB | Profiling, bottleneck detection, targeted optimization |
| **ultrathink** | ✅ Aktif | HaydenLundin | 4.5 KB | Deep architectural reasoning — trade-offs, invariants, craftsmanship |
| **tripwire** | ✅ Aktif | sisi-tarak | 2.8 KB | Single-risk prioritization — satu hal paling kritis untuk dipantau |
| **premortem** | ✅ Aktif | sisi-tarak | 2.5 KB | Failure pre-mortem — asumsikan gagal, cari penyebab sebelum mulai |

## Domain: Ecosystem

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **up-eco** | ✅ Aktif | Hermes | 3.0 KB | Ecosystem status check — git, divergence, health |
| **ekosistem-scaffold** | ✅ Aktif | Hermes | 40.6 KB | Membuat struktur proyek baru sesuai standar Niumination |

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
| ✅ Aktif | **13** |
| **Total** | **13** |

## Catatan

- ✅ **13 SKILL.md terisi penuh** — 8 existing + 5 baru
- ✅ **redteam & ghost** — sudah diporting dari placeholder ke konten mature
- ✅ **3 skill baru** — ultrathink, tripwire, premortem dari eksternal
- ✅ **Frontmatter YAML** — setiap skill punya name, description, version, tags
- 📌 **Optimization** — minimal version dari Jcode bundled skill
- ⚡ **Potensi konflik:** ultrathink ↔ ponytail-core (craftsmanship vs minimalism) — sudah ada section Relationship di ultrathink
- 📌 **Naming convention:** `<domain>/<nama>-<variant>/SKILL.md` — suffix untuk variant
- 📌 **Versioning:** Cukup git history untuk tahap awal

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

# INDEX — Bank Skill Terpusat Niumination

> **Versi:** 1.1.0 (terisi)
> **Lokasi:** `~/Desktop/Niumination/skills/`
> **Domain-based:** Semua skill dikategorisasi per domain, BUKAN per agent.
> **Pengisian oleh Hermes:** ✅ 7/8 skill aktif terisi. 1 (optimization) diisi Hermes + Jcode.

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

## Domain: Ecosystem

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **up-eco** | ✅ Aktif | Hermes | 3.0 KB | Ecosystem status check — git, divergence, health |
| **ekosistem-scaffold** | ✅ Aktif | Hermes | 40.6 KB | Membuat struktur proyek baru sesuai standar Niumination |

## Domain: Security

| Skill | Status | Source | Deskripsi |
|-------|:------:|--------|-----------|
| **redteam** | ⏳ Future | Agentpedia | 32 agen adversarial untuk security pentest (porting manual) |

## Domain: Creative

| Skill | Status | Source | Deskripsi |
|-------|:------:|--------|-----------|
| **ghost** | ⏳ Future | Agentpedia | AI text humanizer — bypass AI detection untuk konten publikasi |

---

## Ringkasan

| Status | Jumlah |
|--------|:------:|
| ✅ Aktif | **8** |
| ⏳ Future | **2** |
| **Total** | **10** |

## Catatan

- ✅ **8 SKILL.md terisi** — dari Hermes (6) + tools/ponytail/ (2)
- ✅ **Frontmatter YAML** — setiap skill punya name, description, version, tags
- 📌 **Optimization** — minimal version dari Jcode bundled skill
- ⏳ **Future skills** (redteam, ghost) butuh porting manual dari Agentpedia
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

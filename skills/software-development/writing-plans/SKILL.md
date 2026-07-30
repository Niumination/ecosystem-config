---
name: writing-plans
description: "Use when you have a spec or requirements for a multi-step task, BEFORE touching code. Creates detailed implementation plans with bite-sized tasks."
domain: software-development
subdomain: sdlc
tags: [planning, implementation, tasks, spec, execution, sdlc]
version: "1.0"
author: obra/superpowers + Niumination
source: superpowers
license: MIT
---

# Writing Plans

> **Sumber:** Diadaptasi dari `obra/superpowers` (MIT).

Tulis implementation plan komprehensif dengan asumsi engineer memiliki nol konteks tentang codebase. Setiap task adalah bite-sized (2-5 menit). DRY. YAGNI. TDD.

**Integrasi Niumination:** Jembatan antara `brainstorming` (desain) dan `subagent-driven-development` (eksekusi). Plan yang baik mencegah waste yang dicegah `ponytail-core`.

**Announce:** "Saya menggunakan writing-plans skill untuk membuat implementation plan."
**Simpan plans ke:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## Scope Check

Jika spec mencakup multiple independent subsystems, pecah jadi beberapa plan — satu per subsystem. Setiap plan harus produce working, testable software sendiri.

## File Structure

Sebelum mendefinisikan task, petakan file yang akan dibuat/dimodifikasi:
- Setiap file punya satu responsibility jelas
- Prefer smaller focused files
- Files yang berubah bersama harus hidup bersama
- Di existing codebase, ikuti pola yang ada

## Task Right-Sizing

Task adalah unit terkecil yang punya test cycle sendiri dan layak di-review sendiri. Setiap task berakhir dengan deliverable yang bisa di-test secara independen.

## Bite-Sized Task Granularity

**Setiap step adalah SATU action (2-5 menit):**
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

## Struktur Plan Document

Setiap plan WAJIB mulai dengan header ini:

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence]
**Architecture:** [2-3 sentences]
**Tech Stack:** [Key technologies]

## Global Constraints

[Project-wide requirements — version floors, dependency limits, etc.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `path/to/file.py`
- Modify: `path/to/existing.py:123-145`
- Test: `path/to/test.py`

**Interfaces:**
- Consumes: [from earlier tasks]
- Produces: [for later tasks]

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Write minimal implementation**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit**
````

## No Placeholders

Setiap step WAJIB berisi actual content. Plan failures:
- "TBD", "TODO", "implement later"
- "Add appropriate error handling" (tanpa spesifik)
- "Write tests for the above" (tanpa test code)
- Referensi ke function yang tidak didefinisikan di task mana pun

## Self-Review

Setelah menulis plan:
1. **Spec coverage:** Setiap requirement di spec punya task?
2. **Placeholder scan:** Ada "TBD"?
3. **Type consistency:** Signatures konsisten antar task?

## Execution Handoff

Setelah plan tersimpan, tawarkan eksekusi:

**"Plan selesai. Dua opsi eksekusi:**
**1. Subagent-Driven (recommended)** — dispatch fresh subagent per task + review
**2. Inline Execution** — execute tasks di session ini dengan checkpoints"

## Integrasi Ekosistem

| Skill | Hubungan |
|-------|----------|
| `brainstorming` | **Input:** spec/desain dari brainstorming |
| `subagent-driven-development` | **Output:** plan dieksekusi via SDD |
| `executing-plans` | **Output alternatif:** plan dieksekusi inline |
| `ponytail-core` | YAGNI — plan harus minimal, tidak over-engineered |

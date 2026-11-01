# Spec-Driven Development (SDD) Workflow — EGM Adoption

> Adopted from Google's Elephant-Goldfish Model (EGM, Apache 2.0).
> Basis: docs/designs/architecture.md, docs/getting_started.md

## Filosofi
EGM memisahkan development menjadi dua peran:
- **Elephant** (deep-context): explore requirements, draft design
- **Goldfish** (zero-context): review design secara adversarial

## 6 Fase Workflow

### Fase 1: Ideasi Upstream (`/egm-brainstorm`)
- Elephant interview developer → anchor core hypothesis
- Spawn 6-lens Goldfish swarm → shoot down flawed assumptions
- Output: `concepts_brief.md`

### Fase 2: Authoring Spec (`/egm-draft`)
- Convert concepts brief → formal design doc di `docs/designs/<feature>.md`
- **Semantic Boundary Discovery**: pisahkan `FeatureRange` (arsitektur high-level) vs `DetailedRange` (implementasi detail)
- Output: design doc dengan batas semantik yang jelas

### Fase 3: Review (`/egm-review` + `/egm-review-loop`)
- Goldfish swarm zero-context mengevaluasi draft
- 7 persona: Comprehension, Critic, Tech Lead, Codebase Auditor, Structural Validator, Style Editor, Zoom Out Architect
- Output: deficiency report (flat, tanpa bias)

### Fase 4: Resolve (`/egm-resolve`)
- Triage findings: PROPOSE FIX vs NEGOTIATE
- Apply automated fixes via UI multiple-choice gates
- Output: resolved design doc

### Fase 5: Implementasi
- Coding agent implementasi sesuai approved design doc
- Tidak perlu Skill.md tambahan (spec sudah lengkap)

### Fase 6: Drift Monitoring (`/egm-drift-report`)
- Jalankan periodik (mingguan) untuk deteksi divergensi spec vs code
- Output: drift report (Matched/Drifted/Orphaned/Missing)

## Kapan pakai
- Fitur baru yang kompleks (multi-file, multi-component)
- Perubahan arsitektur signifikan
- Onboarding repo baru

## Kapan TIDAK pakai
- Bug fix sederhana (one-shot)
- Perubahan kosmetik
- Task yang sudah jelas scope-nya

## Integrasi dengan ekosistem Niumination
- Fase 1-2 → `writing-plans` skill + `brainstorming` skill
- Fase 3-4 → `requesting-code-review` + `egm-*` Goldfish personas
- Fase 5 → `test-driven-development` + `verification-before-completion`
- Fase 6 → `documentation-reconciliation` + `egm-drift-report`
- Living specs → `docs/designs/` (baru) + `docs/registry/` (existing)
- Drift check → `eco-guard.sh verify` (existing) + `egm-drift-report` (baru)

## Semantic Boundary Discovery
Pemisahan antara:
- **FeatureRange**: arsitektur high-level, tujuan, batas komponen, user journey
- **DetailedRange**: implementasi detail, API, data model, algoritma

Tujuan: memungkinkan review targeted (Goldfish hanya review FeatureRange atau DetailedRange, bukan keduanya sekaligus).

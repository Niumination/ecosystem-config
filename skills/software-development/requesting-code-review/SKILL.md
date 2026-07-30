---
name: requesting-code-review
description: "Use when completing tasks, implementing major features, or before merging to verify work meets requirements — dispatches code reviewer with precise context."
domain: software-development
subdomain: sdlc
tags: [review, code-quality, pr, verification, qa]
version: "1.0"
author: obra/superpowers + Niumination
source: superpowers
license: MIT
---

# Requesting Code Review

> **Sumber:** Diadaptasi dari `obra/superpowers` (MIT).

Dispatch code reviewer subagent untuk catch issues sebelum cascade. Reviewer mendapat precisely crafted context — bukan session history.

**Core principle:** Review early, review often.

**Integrasi Niumination:** Melengkapi `ponytail-review` (over-engineering focus) dengan review spek compliance + code quality penuh. `ponytail-review` fokus ke "apa yang bisa didelete", skill ini fokus ke "apa yang benar dan lengkap".

## When to Request Review

**Wajib:**
- Setelah setiap task di subagent-driven-development
- Setelah selesai major feature
- Sebelum merge ke main

**Opsional:**
- When stuck (fresh perspective)
- Sebelum refactoring (baseline check)
- Setelah fixing complex bug

## How to Request

**1. Dapatkan git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code reviewer:**

Dispatch subagent dengan template berikut:
- **DESCRIPTION:** Ringkasan apa yang dibangun
- **REQUIREMENTS:** Plan atau spec yang harus dipenuhi
- **BASE_SHA:** Starting commit
- **HEAD_SHA:** Ending commit

**3. Act on feedback:**
- Critical issues → fix segera
- Important issues → fix sebelum proceed
- Minor issues → catat untuk nanti
- Push back jika reviewer salah (dengan reasoning teknis)

## Red Flags — Never

- Skip review karena "it's simple"
- Ignore Critical issues
- Proceed dengan unfixed Important issues
- Argue dengan valid technical feedback

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just review the diff myself" | Coordinator reviewing inline burns context window. Dispatch subagent. |
| "The reviewer needs my whole session history" | Hand it precisely crafted context, not history. |

## Integrasi Ekosistem

| Skill | Hubungan |
|-------|----------|
| `ponytail-review` | **Complement:** fokus over-engineering check |
| `subagent-driven-development` | Review adalah bagian dari SDD loop |
| `verification-before-completion` | Review findings harus diverifikasi |
| `finishing-a-development-branch` | Review selesai sebelum branch di-finish |

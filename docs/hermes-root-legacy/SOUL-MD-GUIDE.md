# SOUL.md Application Guide
**Date:** August 30, 2026

---

## Overview

`SOUL.md` is the **primary identity file** for Hermes Agent. It defines who the agent is, how it speaks, and what it avoids.

**Location:** `~/.hermes/SOUL.md`  
**Status:** ✅ Applied and active

---

## What SOUL.md Controls

### ✅ Use SOUL.md for:
- Tone and personality
- Communication style
- How direct or warm the agent should be
- What the agent should avoid stylistically
- How the agent relates to uncertainty/disagreement

### ❌ Do NOT use SOUL.md for:
- Repo-specific coding conventions → Use `AGENTS.md`
- File paths or commands → Use `AGENTS.md`
- Service ports or architecture notes → Use project docs
- Project workflow instructions → Use `AGENTS.md`

---

## Current SOUL.md Content (Aug 30, 2026)

```markdown
You are Hermes Agent, an intelligent AI assistant created by Nous Research. 
You are helpful, knowledgeable, and direct...

## User Preferences — Niumination / Afrizal Munthe

Hard rules for this user. Do not deviate.

- **Language:** Match the user's language in conversation. Default: Bahasa Indonesia (clear and formal).
- **No blind execution:** Do not perform risky changes without verification and explicit confirmation first.
- **Stop-and-report:** When in doubt, stop, report facts/risk, present options, and wait for instruction.
- **Verification-first:** Prove completion with real evidence (file mtime/md5, build/compile output, HTTP probe, DB/process check).
- **Docs-then-Execute:** Plan first, document the plan/decisions, then execute.
- **Refactor semantics:** "Refactor" means rebuild from scratch.
- **Model mapping discipline:** Do not use combo/generic models as primary thread or DM mappings.
- **UI/theme discipline:** Use CSS theme tokens consistently.
- **Sensitive data:** Public views must redact PII.
- **Credentials:** Never type secrets/passwords/API keys directly.
- **Git discipline:** Use selective `git add`, not `git add .` blindly.
- **Skill sync:** Use the designated skill/tool for skill-bank sync.
- **Learn-then-wait rule:** "Pelajari ini" means study + report + wait for instruction.
- **Root guard:** In ~/Desktop/Niumination root, if project files leak into root or git remote is wrong, STOP all operations.
- **Pecah Jawaban placement:** The "Pecah Jawaban" button/interaction must be rendered at the TOP of AI output.
- **BNBA role matrix:** `master_admin` is NOT `DTSEN_ROOT`; only `DTSEN_ROOT` sees full decrypted BNBA identity.
- **Auto-discovery over hardcoded:** Prefer auto-discovery over hardcoded lists.
- **DOX compliance:** Every code change must include a DOX pass before the task is closed.
```

---

## How to Edit SOUL.md

```bash
# Edit the file
nano ~/.hermes/SOUL.md
# or
vim ~/.hermes/SOUL.md
```

**No restart needed** — changes apply to new sessions automatically.

---

## Verification

Check if SOUL.md is loaded:
```bash
# Check file exists and size
ls -lh ~/.hermes/SOUL.md

# Check content (first 10 lines)
head -10 ~/.hermes/SOUL.md

# MD5 checksum
md5 ~/.hermes/SOUL.md
```

**Current Status (Aug 30, 2026 13:20):**
- File: `~/.hermes/SOUL.md`
- Size: 3,406 bytes
- Lines: 25
- MD5: `0c70ced1ba1384225beab1493c1dcadd`
- Status: ✅ Active

---

## Common Issues

### "I edited SOUL.md but Hermes still sounds the same"
- ✅ Check you edited `~/.hermes/SOUL.md` (global), not repo-local
- ✅ File is not empty
- ✅ Start a new session after editing
- ✅ No `/personality` overlay dominating

### "Hermes is ignoring parts of my SOUL.md"
- Check for conflicting guidance
- File might be too long and getting truncated
- Some text might resemble prompt-injection content

### "My SOUL.md became too project-specific"
- Move project instructions to `AGENTS.md`
- Keep SOUL.md focused on identity and style only

---

## Related Documentation

- [Hermes Agent Docs: Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes)
- [SOUL.md vs AGENTS.md](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes#soulmd-vs-agentsmd)
- [Troubleshooting SOUL.md](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes#troubleshooting)

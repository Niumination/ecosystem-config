---
name: ecosystem-recovery
description: Full ecosystem recovery after delete or up-eco failures.
tags: [ecosystem, recovery, up-eco, skill-bank, stow, dotfiles, vercel, splp, health-check]
version: 1.0.0
last_updated: "2026-08-28"
---

# Ecosystem Recovery — Full Health Luar-Dalam

Class-level recovery workflow that turns a 9-recommendation red `/up-eco` into a 4-recommendation HOLD (non-blocking) in one session. Validated 28 Aug 2026.

## Trigger

- `bash scripts/up-eco.sh` shows: manifest mismatch + Jcode 0/68 + root dirty + trash files + Vercel env stale
- Post mass-delete / `setup.sh` / Stow bulk incident
- `opencode --version` / `jcode --version` fail after config wipe
- SPLP key rotated or Bapokting chip disabled
- User says: "recover full", "periksa ulang", "pastikan sehat luar dalam", "up-eco rusak?"

## Workflow — Ordered (do not reorder)

### 1. Thermal + Hermes quick check (read-only)

```bash
osx-cpu-temp; sh ~/Desktop/Niumination/scripts/thermal-status.sh 2>&1 | head
cat ~/.hermes/gateway_state.json | head; ls -lh ~/.hermes/.env; cat ~/Desktop/Niumination/vault/secrets.zsh | head
jcode --version; opencode --version
jcode run "say PONG" 2>&1 | head  # should be hy3-free free tier
```

`64°C` + `gateway 5.7%` = healthy. `opencode/hy3-free` must answer PONG.

### 2. Dependency audit (read-only)

```bash
ls ~/Desktop/Niumination/services/cc-acehtengah/node_modules | head
npx --prefix ~/Desktop/Niumination/services/cc-acehtengah prisma --version
for t in starship fzf zoxide bat rg fd eza thefuck tmux stow; do command -v $t && echo OK || echo MISSING; done
# OPTIONAL: lazygit, gh, nvim — missing is not fatal
```

- `cc-acehtengah/node_modules` must exist (prisma 6.19.3)
- `~/.config/opencode/node_modules` → `@opencode-ai/plugin`
- `apps/niu-dash` Vanilla HTML `node_modules` MISSING is EXPECTED (no build)

### 3. Skill Bank regenerate (MUST be before sync)

```bash
python3 scripts/skill-manifest.py              # generate
python3 scripts/skill-manifest.py --check      # should be 0 mismatch, 68 skill/348 file
```

3 mismatches (`telegram-router-orchestration`, `hermes-provider-config`, `up-eco`) → regenerate fixes. Never sync with stale manifest.

### 4. Brew deps — exact fix for optional tools

```bash
brew install lazygit          # 0.64.1
brew install olets/tap/zsh-abbr  # NOT `abbr` — zsh-abbr is a zsh function
zsh -c 'source ~/.zshrc && type abbr'  # → shell function from zsh-abbr.zsh
```

Don't capture `abbr: command not found` (bash) as a skill rule — it's a shell-function by design.

### 5. Trash cleanup (non-destructive)

```bash
rm -f photorec.se2                          # TestDisk artifact (~40KB)
rm -f scripts/.thermal-guardian.{err,log,out}
rm -rf .agents .claude                      # empty stub dirs (6 skills each, failed agent)
git status --short
```

Check `.gitignore` before deleting; `photorec.se2` is never committed.

### 6. Selective git add + commit

```bash
git add skills/manifest.json skills/autonomous-ai-agents/telegram-router-orchestration/SKILL.md \
        skills/ecosystem/hermes-provider-config/SKILL.md \
        docs/references/model-mapping-post-rollback.md skills-lock.json
git commit -m "chore(eco): full recover — manifest + skill sync + cleanup"
```

Do NOT `git add .` — trash would be committed.

### 7. Skill sync (full-folder, all targets)

```bash
bash skills/sync-to-agents.sh
# expected:
# Jcode: 68 skill disinkronkan → ✅ verifikasi hash LULUS
# Hermes: 68 skill disinkronkan → 1 mismatch simplify-code/SKILL.md is warning-only
```

If Hermes `simplify-code` mismatch persists: `rm -rf ~/.hermes/skills/simplify-code && bash skills/sync-to-agents.sh`.

### 8. AGENTS.md registry commit (separate)

Sync bumps `_Last sync: <timestamp>` + 2 blank lines → always 1 dirty file after sync:

```bash
git add AGENTS.md
git commit -m "chore(skill): sync registry — 68 skill -> Jcode/Hermes"
```

This dirty state is EXPECTED, not a regression.

### 9. Push via token (restore URL after)

```bash
source ~/.hermes/.env
git remote set-url origin "https://oauth2:${GITHUB_TOKEN}@github.com/Niumination/ecosystem-config.git"
git push origin main
git remote set-url origin git@github.com:Niumination/ecosystem-config.git
```

Verify `0 ahead` after push.

### 10. Vercel env + service chip (when SPLP/Bapokting changed)

```bash
# SPLP key: same JWT invalid across services — Bapokting (bahan-pokok-penting) ≠ DTSEN (dtsen-aceh-tengah)
# app 6617 key → Bapokting 200 OK (76 komoditas) but DTSEN 401 Invalid Credentials → need separate key
# Update fallback in src/lib/bapokting-client.ts + Vercel env SPLP_API_KEY, then:
vercel --prod
sleep 3; curl -s https://cc-acehtengah.vercel.app/api/health | head
# expect: 200 healthy, sapa:ok, ai:nemotron-3-ultra-free

# Bapokting chip activation in src/components/QueryBar.tsx:
# chips disabled (query:'') → active queries matching orchestrator regex \b(harga|komoditas|beras|minyak|bawang)\b
# Hint: 'menunggu sumber data' → 'SPLP API 76 komoditas'
# Verify: node -e "const r=/\b(harga|komoditas|beras|minyak|bawang)\b/; console.log(r.test('berapa harga beras'))"
```

### 11. Final verify

```bash
bash scripts/up-eco.sh
# 9 → 5 → 4 recommendations remaining (all HOLD):
# gh auth login, MC :5200 offline, audit 32 findings (URL allowlist), Broker Phase B HOLD
```

`MC :5200` (Mission Control) offline is non-blocking. Offer to start: `cd services/niu-mission-control && python3 server.py`.

## Service-Specific Pitfalls

- **SPLP one-key-per-service**: same `AuthorizationSPLP: Bearer <JWT>` tested against `bahan-pokok-penting` (200) vs `dtsen-aceh-tengah` (401) — proves JWT is service-scoped. Request separate `dtsen-aceh-tengah/1.0` key from portal `api-splp.layanan.go.id`.
- **Chip query must match orchestrator regex** in `src/services/ai-orchestrator.ts`: `harga|komoditas|beras|minyak|bawang|bahan pokok`. Empty `query: ''` disables chip; wrong keyword → `fetchLatestBapoktingPrices()` never called.
- **zsh-abbr binary confusion**: `abbr` not found in bash is correct — it's a zsh function loaded via `~/.zshrc`.
- **Vanilla projects**: `apps/niu-dash` is single-file HTML, `node_modules` missing is expected.
- **AGENTS.md dirty after sync**: registry timestamp bump, not a failure.

## Verification

- `bash scripts/up-eco.sh` → 0 mismatch, Jcode 68/68, root 0 dirty, 0 ahead
- `jcode run "say PONG"` → PONG (hy3-free)
- `https://cc-acehtengah.vercel.app/api/health` → 200 healthy + Bapokting live
- `git -C ~/Desktop/Niumination status --short` → clean after AGENTS.md commit

## Remediation workflow: PII/credential cleanup in git
- **Branching rule**: affected branch stays untouched; create a new branch from it for remediation work
- **Rewrite history only on the new branch** using `git filter-repo --force --replace-text <map>`; do not force-push `main` or other shared branches
- **Verification**: after filter-repo, confirm affected strings no longer appear in the new branch's reachable history
- **Deploy path**: open a PR from the remediation branch; merge through GitHub rather than force-pushing shared branches
- **Why**: minimizes disruption to collaborators while still producing a cleaned history for future merges

## References

- `references/full-recover-2026-08-28.md` — full transcript (up-eco 02:05→02:11, Vercel 2 redeploys, Bapokting 76 komoditas)
- `references/splp-bapokting-chip-2026-08-28.md` — SPLP key service-scoping + QueryBar chip activation detail
- `docs/ECOSYSTEM-STATUS-2026-08-27.md` + `docs/references/model-mapping-post-rollback.md`
- `skills/ecosystem/up-eco/SKILL.md` Phase 9c (Credential Broker HOLD)

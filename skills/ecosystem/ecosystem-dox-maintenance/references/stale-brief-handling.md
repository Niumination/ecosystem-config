# Stale Brief/Prototype Handling

## Decision rule
When a project ships a zip or instruction bundle that describes work, compare that bundle against the live branch state first.

- If live already exceeds the brief → remove the obsolete bundle from the repo. Do not rewrite historical docs to match new reality unless user explicitly asks.
- If live is missing pieces → patch only the gaps.

## Merge strategy for hotfix release
If `hotfix/meeting-ready` is the agreed release state and `main` is stale, prefer:
1. `git checkout main`
2. `git reset --hard origin/hotfix/meeting-ready`
3. `git push origin main --force`

instead of resolving large merge conflicts that mainly reintroduce stale files or old paths.

## Verification after cleanup
- Confirm removed directories no longer exist.
- Run `npx tsc --noEmit`, `npx vitest run --reporter=dot`, `bash scripts/pii-gate.sh .`.
- Re-check live health endpoint before declaring clean.

---
name: vercel-feature-activation
description: "Use when activating a dormant feature on a Vercel app."
version: 1.0.0
metadata:
  hermes:
    tags: [vercel, activation, env, postgres, cms, auth, verification]
    category: devops
---

# Activating a dormant feature on a live Vercel app

Some features ship fully coded but stay dark until infrastructure exists — a CMS behind `DATABASE_URL`, shared-password auth behind `*_RAHASIA`/`*_SANDI_*`, a queue behind a broker. Turning one on is **configuration, not code**: the risk is not breaking the app, it is declaring victory on a status page that reports only "an env var is set" and never proving a write landed.

## When to Use

- A feature exists in the codebase but every entry point returns read-only, 503, or "not configured".
- The owner says "turn it on", "activate it", "make the CMS/admin/AI work", or hands you a vendor activation guide.
- You are adding or rotating env vars on a deployed app and must prove they took effect.

NOT for: writing the feature's code, or pure env rotation of an already-working feature (see the env-rotation skill if one exists).

## Rule 0 — read the source before the console

Before touching the dashboard or CLI, read four things in the repo:

1. **`.env.example`** — exact var names, and which are declared optional.
2. **The auth/session module** — what each secret is used for and any length or format constraint (a signing secret may require ≥32 chars; an account password may require nothing).
3. **The activation guide** if the vendor shipped one in the repo or with the release — follow its order, it is the author's own verified sequence.
4. **The status/health endpoint** — find the one that reports per-subsystem booleans; that is what you will verify against.

Never invent var names from the feature's UI. A wrong name is invisible: the app keeps returning its old "not configured" response and you cannot tell whether the env or the code is at fault.

## Procedure

1. **Inventory what already exists.** `vercel env ls` in the project dir. If a database URL is already present, that database is provisioned and connected — reuse it. Do not create a second database; ask the owner before creating one, and if they already made one, find it rather than duplicating.
2. **Classify each required secret:**
   - *Account credentials* (human-typed passwords) — a temporary value from the owner is acceptable for a trial, but say plainly in your report that it must be replaced.
   - *Machine secrets* (HMAC/session signing keys, webhook secrets, encryption keys) — always generate with `openssl rand`; a guessable signing secret lets anyone forge sessions, which is strictly worse than a guessable password. Never substitute an owner-supplied password here.
3. **Generate machine secrets locally**, write to a temp file with `umask 077`, consume via `"$(cat file)"`, then `shred -u`. Never echo a secret into the terminal, chat, a report, or a commit.
4. **Set env vars non-interactively:**
   ```bash
   vercel env add NAME production --sensitive --value "$VALUE" -y
   vercel env add NAME production --sensitive --force --value "$VALUE" -y   # rotation
   ```
   Scope deliberately: `production` only, or add `preview` when you intend to test on a preview URL. `--sensitive` for anything secret. Confirm with `vercel env ls` (values stay `Hidden`).
5. **Redeploy — env is build/deploy-scoped.** `vercel --prod --yes`. Then confirm the new deployment actually owns the production domain: `vercel inspect <url>` and read the `Aliases` block. A successful deploy does not always take over the domain; when it did not, `vercel promote <url>`.
6. **Verify against the app's own status endpoint** and require explicit booleans per subsystem. `{"cmsAktif":true,"dbAktif":true}` is evidence; a page returning 200 is not.
7. **Exercise the real path end-to-end** (see `references/api-authz-verification.md`): read current state → write → read back → confirm the new value is visible on the public/read path → confirm the audit trail recorded the action.
8. **Prove the authorization matrix**, not just the happy path: anonymous, wrong role, right role on a forbidden field, right role on an allowed field. A feature that only ever demonstrated success has not been verified.
9. **Revert test writes from the source of truth.** Before writing, read the original value out of the authoritative file (the seed JSON, not your memory of it) and write exactly that back afterwards. Delete temp cookie/credential files.
10. **Update the project DOX** with: which storage is connected, which env vars exist, that any temporary password is temporary, the verification results, and every integration gotcha discovered — those gotchas are the entire value of the exercise for the next session.

## Pitfalls

- **A "feature active" boolean is not proof the schema exists.** Such flags are usually derived from the presence of a connection string, which says nothing about whether the tables were created. The first real write is the only probe that counts.
- **A 403 on a write endpoint can be an identifier-shape mismatch, not a permissions denial.** Handlers frequently resolve the caller's target with a multi-shape lookup (`String(x.id) === input || x.singkat === input || x.nama === input`) before the ownership check; when the handler's real matching key is a numeric id and you sent a slug or a lowercase abbreviation, the ownership check fails and returns the same 403 an under-privileged caller would get. Read the handler's lookup expression and send the exact shape the UI sends — the UI's own source is the authoritative answer.
- **Guess field names from the validator's error, not from intuition.** A 400 naming the constraint is the cheapest possible probe; each guess costs a round-trip and risks writing to the wrong key.
- **Env edits without a redeploy silently do nothing**, and a redeploy that does not take the domain looks exactly like a successful activation. Check aliases, not just exit codes.
- **Never retry a blocked protected-file edit through another tool or path.** If an approval gate for a DOX or agent-instruction file times out, state the intended edits, ask once, and batch all of them into the single approved pass.
- **Confirm each file edit landed before the next step depends on it** — check `git status --porcelain` or `ls -la` after any write performed through a wrapper, then build on that confirmation.
- **Leave unrelated stale env vars alone** unless the owner asks; note them as an observation so removing them stays a deliberate decision.
- **Report what you could not do.** Browser-only steps (clicking through the UI, real-device checks) and anything needing other people remain open items with the exact command or click-path the owner must run.

## Verification

- `vercel env ls` shows every required var with the intended environment scope and `Hidden`/`Sensitive` values.
- The status endpoint reports every subsystem boolean `true`, individually named.
- One write returned success, the value reads back equal, the change is visible on the end-user path, and the audit log contains the action.
- Each authorization cell returned the expected status code — expected failures were observed, not assumed.
- Test data restored; temp credential files gone (`ls` returns nothing).
- `git status --porcelain` shows exactly the intended DOX/doc files.

## References

- `references/api-authz-verification.md` — exercising and proving a live write API, the authorization matrix, and the identifier-shape trap.
- `references/env-and-db-provisioning.md` — env var commands, secret generation, database reuse vs creation, redeploy/promote, rotation recipe.

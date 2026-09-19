# Vercel: build failure vs deploy block

Local `npm run build` green but the deployment shows `● Error` — the two causes
look identical in the dashboard and need different fixes. Read the **tail** of
the build log first.

## Symptom → cause → move

| Tail of `vercel inspect <url> --logs` | Meaning | Move |
|---|---|---|
| Error inside compile / type check / `Collecting page data` | Build failure; platform-specific env is the usual trigger | Reproduce locally with the platform's env shape (below), fix code |
| `Build Completed in /vercel/output` + `Deploying outputs...` then `Vulnerable version of Next.js detected` | Platform refuses the artefact (framework CVE) | Upgrade `next` within the same major line, regen lockfile, push |
| `Build Completed` + alias/`Can't find the deployment` on `vercel inspect` | Wrong identifier passed to `inspect` | Use the deployment URL from `vercel ls`, not the project alias |
| `npm ci` fails: lockfile out of sync | Dependency change not committed | Regenerate `package-lock.json`, commit it with the bump |

## Evidence commands

```bash
vercel project ls                                   # project + latest production URL
vercel ls <project>                                 # Status per push, with age
vercel inspect <deployment-url> --logs | tail -60    # build log, newest last
```

`vercel link --yes --project <name>` makes CLI commands work from the project
dir; it writes `.vercel/` and `.env.local`, and appends an `.env*` line to the
project `.gitignore`. Expect those three working-tree changes and report them.

A failed deployment does not stop the next push from deploying: the newest
failed deployment is often from the *older* commit, so match the commit hash in
the log header (`Cloning github.com/<org>/<repo> (Branch: main, Commit: <sha>)`)
before concluding your fix did not work.

## Empty-string env vars: mechanism and probe

`process.env.X ?? 'default'` — `??` fires only for `undefined`/`null`. A variable
created on the platform but left blank yields `''`, which then reaches
`new URL('')` / `fetch('')` at module scope and throws during page-data
collection (`ERR_INVALID_URL`, `input: ''`). Unset locally ⇒ green locally.

```bash
# replicate the platform condition
SITE_URL= npm run build

# prove the mechanism without a full build
node -e "function t(v,l){process.env.X=v; const b=process.env.X ?? 'd'; const o=(process.env.X?.trim()||'d'); const r=x=>{try{return new URL(x).href}catch(e){return e.code}}; console.log(l, r(b), r(o))}"
```

Rule: an env var whose empty value must be tolerated needs `?.trim() || default`
(or an explicit `if (!v) return fallback`), never bare `??`. Env values captured
by `vercel env pull` show as `[SENSITIVE]` when the variable is sensitive-type,
so emptiness must be inferred from the build crash, not from the pull.

## Framework CVE deploy block

Vercel hard-stops deployments whose Next.js build carries RSC vulnerabilities
(React2Shell, CVE-2025-66478). Patched releases published for the affected line:
15.0.5 · 15.1.9 · 15.2.6 · 15.3.6 · 15.4.8 · 15.5.7 · 16.0.7 (plus canaries
15.6.0-canary.58 / 16.1.0-canary.12).

Procedure:

1. `npm view next@<line> version` — pick the highest patch in the current line.
2. `npm install next@<that version>`; commit `package.json` + `package-lock.json`.
3. `npm test` · `npm run typecheck` · `npm run build` locally.
4. `SITE_URL= npm run build` again to keep the platform condition covered.
5. Push, then `vercel ls <project>` until `Ready` — a green GitHub Actions run
   says nothing about the Vercel deploy, they are separate gates.

Keep the jump minimal inside the major line; escalate to the next major only
with owner approval (React/App Router migration risk).

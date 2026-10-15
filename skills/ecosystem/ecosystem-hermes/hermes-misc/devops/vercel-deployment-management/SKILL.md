---
name: vercel-deployment-management
description: Manage Vercel deployments — status, deploys, pause/unpause.
---

# Vercel Deployment Management

## Always-On Rules

1. **CLI has no `unpause` command** — Vercel CLI does not support unpausing a project. Triggering a production deployment creates a new deployment but does NOT unpause the production domain. Unpause requires dashboard action or API call with appropriate token.

2. **Pause is project-level, not deployment-level** — A paused project returns 503 with `x-vercel-error: DEPLOYMENT_PAUSED` on the production domain. New deployments are still created and accessible via their direct URL, but the production alias remains paused.

3. **Check deployment status before declaring success** — Use `vercel inspect <url> --wait` to check deployment status. A 302 redirect means the deployment is ready. A 503 with `DEPLOYMENT_PAUSED` means the project is paused.

4. **Production deployment command** — `vercel --prod --yes` from the project directory. This creates a new production deployment but does not unpause a paused project.

5. **Project inspection** — `vercel project inspect <name>` shows project settings including framework, root directory, and build command.

6. **First deploy of a never-deployed project is allocated production automatically** — `vercel deploy --yes` on a fresh project gets a production allocation; the `.vercel.app` URL serves either way, but the production alias points at this deployment. Confirm intent before running it.

7. **`vercel link` writes `.vercel/` and `.env.local` (OIDC token)** — right after linking, prove they are ignored before the next commit: `git check-ignore -v .env.local .vercel`.

8. **Verify a live deployment by GET-ing the routes users hit**, not just the root: `curl -s -o /dev/null -w '%{http_code}' https://<url>/<route>` per route (SSG pages, API, gated/verify pages). A deploy reports Ready while a subroute still 404s or 500s.

9. **A 200 on a per-deployment URL is not proof your app served it.** With Deployment Protection (Vercel Authentication) on — the default for new projects — `https://<project>-<hash>-<team>.vercel.app` answers **200 with Vercel's own sign-in page** on every route. Verify identity from the response body, not the status code: read `<title>` (Vercel's SSO page titles `Login – Vercel`) or grep for a string only your app renders. Probe the **stable alias** (`<project>-<team>.vercel.app`, `<project>.vercel.app`) or the custom domain, never the hash URL, when the question is "is the app live".

10. **`vercel env` targets the project by cwd.** A `vercel env add` run from the wrong directory writes into a different team's project and exits 0. Pass `workdir=<project-dir>` on the terminal call (an `os.chdir()` inside `execute_code` does not carry over) and confirm the project name the CLI prints before trusting the write.

## Workflow: Unpause a Paused Project

1. Check current status: `curl -sI https://<domain>.vercel.app | head -5`
2. If 503 with `DEPLOYMENT_PAUSED`, the project is paused
3. Trigger production deployment: `vercel --prod --yes` (from project directory)
4. Wait for deployment to complete: `vercel inspect <deployment-url> --wait`
5. Check if production domain is now live: `curl -sI https://<domain>.vercel.app | head -5`
6. If still 503, the pause is a project-level setting that requires dashboard action:
   - User must open https://vercel.com/<team>/project/settings
   - Find "Deployment Paused" or "Pause Production Traffic" section
   - Click "Unpause" or toggle off pause
7. After unpause, verify: `curl -sI https://<domain>.vercel.app | head -5` should return 200 or 302

## Workflow: Check Deployment Status

1. List recent deployments: `vercel ls --prod`
2. Inspect specific deployment: `vercel inspect <url> --wait`
3. Check production domain: `curl -sI https://<domain>.vercel.app | head -5`

## Workflow: Deploy to Production

1. From project directory: `vercel --prod --yes`
2. Wait for deployment: `vercel inspect <deployment-url> --wait`
3. Verify: `curl -sI https://<domain>.vercel.app | head -5`

## Pitfalls

- **CLI timeout** — `vercel --prod --yes` can take 2-5 minutes. Use `timeout=120` or higher, or run in background.
- **Auth token** — Vercel CLI uses `~/.vercel/auth.json`. If missing, run `vercel login` first.
- **Project scope** — Vercel projects are scoped to a team. Use `vercel project inspect <name>` to find the correct team.
- **Exit code 0 does not prove a deployment happened** — the CLI can print an unknown-option error and still exit 0. `--no-env` is not a flag. Success = a deployment URL in the output or `vercel ls` showing the new entry; verify before reporting.
- **`vercel env add` exit 1 with a warning is not failure** — when adding `NEXT_PUBLIC_*` vars the CLI warns "can be seen by anyone visiting your site" and returns RC 1 *after saving*. Verify with `vercel env ls` rather than treating RC 1 as "not set".
- **`vercel deploy` targets the project by cwd, not by flag** — running it from the home directory (or after a `chdir` that didn't persist) silently deploys to a different team's project (observed: `cc-acehtengah` instead of `kelas`). Always run with `workdir=<project-dir>` on the terminal call, or `cd <project-dir> &&` inside one command string. Confirm the linked project with `vercel project inspect` before trusting the deploy URL.
- **`os.chdir()` in execute_code does not persist across calls** — the kernel may be reused or reset between calls. Never rely on it to set cwd for CLI tools; pass `workdir` explicitly on every terminal call.
- **The hash deployment URL sits behind Deployment Protection; the stable alias does not.** `vercel ls <project> --prod` lists hash URLs that all return 200 — with Vercel's login page. Get the aliases that actually serve the app from `vercel alias ls | grep <project>` (shape: `<project>-<team>.vercel.app`, `<project>.vercel.app`, `<project>-git-main-<team>.vercel.app`, plus custom domains). Smoke-test an alias or the domain and confirm the body is your app before recording a status anywhere — a "200 OK" captured from a protected URL is a false green that later has to be retracted.
- **`vercel deploy --yes --prod` may stop to ask "You are deploying your home directory. Do you want to continue?"** and exit 0 without deploying when stdin is not interactive. Pipe `echo y |` or, better, fix the cwd with `workdir` — the prompt itself is the signal that the CLI is not in the project root.
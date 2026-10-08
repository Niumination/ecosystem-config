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
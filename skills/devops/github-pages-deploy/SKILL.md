---
name: github-pages-deploy
description: Deploy static HTML to GitHub Pages via clean branch.
tags: [deploy, github-pages, static-site, branch]
---

# GitHub Pages Deploy (Static HTML)

## Overview

Deploy single-file or small static HTML sites to GitHub Pages via the `gh-pages` branch.

## The Iron Law

```
Jekyll build FAILS when checkout errors occur → use CLEAN orphan branch, not source-based build.
```

## API Constraints (learn these once, stop re-discovering them)

- **Pages source path is RESTRICTED to `/` or `/docs`.** You cannot point Pages at an arbitrary
  subfolder: `-F 'source[path]=snapshot'` → `422 ... is not a possible value. Must be one of the
  following: /, /docs.` Consequence: to publish files that live in `snapshot/`, deploy a dedicated
  branch whose **ROOT** holds the files — copy them up out of the subfolder. Do not try to teach
  Pages a subfolder.
- **Nested fields use bracket syntax with `-F`, never a JSON string.**
  `-f source='{"branch":"gh-pages","path":"/"}'` → `422 Invalid property /source: "..." is not of
  type object.` Use `-F 'source[branch]=gh-pages' -F 'source[path]=/'`.
- **The publishing branch must exist before Pages can build it.** Setting a source branch that does
  not exist → `422 The gh-pages branch must exist before GitHub Pages can be built.` Create it first:
  `gh api --method POST /repos/{owner}/{repo}/git/refs -F ref=refs/heads/gh-pages -F "sha=$(git rev-parse <rev>)"`
- **Branch creation needs the FULL 40-char SHA.** A short SHA → `422 At least 40 characters are
  required`. Always resolve first: `-F "sha=$(git rev-parse <short-or-ref>)"`. `gh api` has no
  `--sha` flag.
- **`POST /pages` on an already-enabled site** → `409 GitHub Pages is already enabled.` Harmless.
  Read state with `GET /repos/{owner}/{repo}/pages` (fields: `status`, `cname`, `source`, `html_url`,
  `https_enforced`, `pending_domain_unverified_at`) instead of re-POSTing.
- **The Pages workflow has NO `workflow_dispatch` trigger.**
  `gh workflow run pages-build-deployment` → `422 Workflow does not have 'workflow_dispatch' trigger`.
  You cannot force a rebuild manually — push a new commit to the publishing branch.
- **Workflow LOGS need admin rights** (`403 Must have admin rights to Repository`). To find which
  step actually failed, use the jobs endpoint rather than the logs endpoint:
  `gh api /repos/{owner}/{repo}/actions/runs/<id>/jobs --jq '.jobs[] | .name, (.steps[] | .name, .conclusion)'`
  A `build` job failing at `Checkout` = the branch content is unpublishable (LFS pointers,
  submodules, or a full repo mirror). Fix the branch content, not the workflow.

## Pre-Execution Checklist

1. **Check if Pages already deployed** → `gh api /repos/{owner}/{repo}/pages` (status, source)
2. **Check if gh-pages branch exists** → `gh api /repos/{owner}/{repo}/git/refs/heads/gh-pages`
3. **Verify file exists in repo** → `gh api /repos/{owner}/{repo}/contents/<path>` (download_url)
4. **Check existing build status** → `gh api /repos/{owner}/{repo}/actions/runs` (last 3 runs)

### Step 0 (Optional): Custom domain setup

If deploying to a custom domain (e.g., `watchdog-mata.niumination.web.id`):

1. **Create CNAME file** in the gh-pages branch:
   ```bash
   echo 'watchdog-mata.niumination.web.id' > CNAME
   git add CNAME && git commit --amend --no-edit
   git push -f origin gh-pages
   ```
2. **Add custom domain via GitHub API**:
   ```bash
   gh api --method POST /repos/{owner}/{repo}/pages \
     -F 'source[branch]=gh-pages' \
     -F 'source[path]=/'
   ```
3. **Update DNS in Cloudflare**: Replace the existing A record for the domain with a CNAME record pointing to `niumination.github.io` (proxy ON). If using a subdomain, ADD a CNAME record (no conflict with existing A records for the apex domain).
4. **Wait for DNS propagation** (~5 min) before expecting GitHub Pages to activate the custom domain.

Note: GitHub Pages auto-configures HTTPS via Cloudflare once the CNAME record resolves. No manual certificate setup needed.

### Step 1: Create clean gh-pages branch

The publishing branch must hold ONLY the deployables — no submodules, no LFS pointers, no full-repo
mirror. That is exactly what makes the Jekyll `Checkout` step fail.

```bash
git checkout main && git reset --hard origin/main
git branch -D gh-pages 2>/dev/null || true    # refuses while gh-pages is the checked-out branch
git checkout -b gh-pages <full-sha-of-main>   # start from a commit, then rewrite the tree
git rm -rf -- .                               # clears the INDEX *and* the working tree
git checkout main -- snapshot/                # restore the deployable subset from the source branch
git add snapshot/
git commit -m "gh-pages: static snapshot <description>"
git push -f origin gh-pages
```

Branch-surgery hazards (each one costs a round trip):

- `git checkout -b <new> --orphan <other>` → `fatal: '-b', '-B', and '--orphan' cannot be used
  together`. For a true orphan, use `git checkout --orphan <name>` alone.
- `git branch -D <branch>` refuses while that branch is checked out — switch away first.
- `git rm -rf -- .` deletes the files from disk as well as from the index, so the following
  `git add <path>` dies with `pathspec did not match any files` until the path is restored with
  `git checkout <source-branch> -- <path>`.
- After a mass `git rm`, `git add <tracked-path>` can answer *"nothing to commit, but untracked files
  present"* while the commit is in fact only the deletions. Confirm what is staged with
  `git ls-files <path>` / `git show --stat`, never from the status wording.
- Switching one checkout back and forth between `main` and the publishing branch in a repo carrying
  submodules/LFS leaves residue (`unable to rmdir 'assets/media': Directory not empty`) and stray
  untracked dirs. Do publishing-branch work in a `git worktree` when the primary checkout must stay
  clean.

### Step 1b: Add one more artifact to an existing publishing branch

Do NOT rebuild the branch to publish another file — pull just that file across and push:

```bash
git checkout gh-pages
git checkout main -- snapshot/<new-artifact>.html
git add snapshot/<new-artifact>.html
git commit -m "gh-pages: add <artifact>"
git push origin gh-pages
```

### Step 2: Commit with minimal content

```bash
git add <needed-files/>
git commit -m "gh-pages: static snapshot <description>"
git push -f origin gh-pages
```

### Step 3: Enable Pages

```bash
# Pages is auto-enabled when gh-pages branch exists with HTML files.
# Force a rebuild:
gh api --method POST /repos/{owner}/{repo}/pages \
  -F 'source[branch]=gh-pages' \
  -F 'source[path]=/'
```

If Pages already enabled → you'll get 409 (conflict). That's fine.

### Step 4: Verify deployment

```bash
# Wait 60-120s for build
sleep 60
curl -sI https://<username>.github.io/<repo>/<path> | head -n 1
# Expected: HTTP/2 200

# Check build status
gh api /repos/{owner}/{repo}/actions/runs --jq '.workflow_runs[0].status, .workflow_runs[0].conclusion'
```

### Step 5: Verify custom domain (if applicable)

```bash
# Check DNS resolves
curl -sI https://<custom-domain>/ | head -n 1
# Expected: HTTP/2 200 (not "Could not resolve host")

# Check GitHub Pages status
gh api /repos/{owner}/{repo}/pages --jq '.status'
# Expected: "built"
```

## Pitfalls

1. **Jekyll checkout failure** — The automatic `pages-build-deployment` workflow uses `actions/checkout@v4` which fails on repos with LFS or submodules. Fix: use clean orphan branch approach (Step 1 clean-slate).

2. **Root path 404** — If `source[path]=/` and no `index.html` at root, you get 404. Put files in a subdirectory (e.g., `/snapshot/`) and access via `/<repo>/snapshot/file.html`.

3. **LFS files not served** — GitHub Pages doesn't serve LFS files directly. Ensure HTML files are NOT LFS-tracked. Check `.gitattributes` for `*.html filter=lfs` and remove if present.

4. **Build takes >2 min** — First build can take 2-3 min. Poll with `sleep 60 && curl` twice.

5. **Force push required** — `git push -f origin gh-pages` because gh-pages branch needs to be rewritten to contain only the deployed files.

6. **Custom domain DNS must be updated BEFORE adding to GitHub** — If the domain points to a dead VPS (e.g., Cloudflare A record to old IP), GitHub Pages custom domain won't activate. DNS must resolve to `niumination.github.io` first. In Cloudflare: replace A record with CNAME `subdomain` → `niumination.github.io` (proxied ON). GitHub Pages auto-enables HTTPS via Cloudflare once DNS propagates (~5 min).

7. **macOS DNS cache stale after CNAME change** — `dig` resolves correctly but `curl` fails with "Could not resolve host" because macOS `mDNSResponder` cache is stale. Fix: `sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder`. If still failing, use `curl --resolve <domain>:443:<cloudflare-ip>`. See `references/dns-cloudflare.md` for full troubleshooting.

8. **DNS cannot have both A and CNAME for same name** — Cloudflare (and DNS generally) rejects coexisting A + CNAME for the same hostname. To use a custom domain, REPLACE the existing A record — don't add alongside it. Alternatively, use a subdomain (e.g., `watchdog-mata.niumination.web.id`) — additive, non-destructive, and the safest option when the apex record still matters to someone else.

9. **CNAME file must be in gh-pages branch** — Create a `CNAME` file at the root of the publishing branch containing the custom domain name. This tells GitHub Pages to accept the custom domain. Commit and force-push to the branch.

10. **Enabling Pages BEFORE the custom domain is wired** — the domain shows as the site's `html_url`
    while `https_enforced` stays `false`. That is the normal intermediate state behind a Cloudflare
    proxy, not an error. Confirm with `curl --resolve` at the edge rather than assuming it failed.

11. **Root `/` 404 with the files in a subfolder** — the root needs its own entry point. Either add
    an `index.html` that redirects to the file, or replace the root with a small picker page listing
    the available artifacts. A picker beats a blind auto-redirect when there is more than one
    artifact and the audience must know which one is authoritative.
    Build it as ONE self-contained file — no CDN fonts, no external CSS/JS, no JS at all when plain
    links suffice — and label which artifact is authoritative (the one submitted/graded) versus newer
    work. When proposing the choice, describe or sketch what the visitor will see: naming it
    "halaman pemilih" alone does not convey the change, so the user has to stop and ask what it means.

12. **`status` lags the live site** — the Pages API can keep reporting `building` for minutes while
    the artifact already answers `200` at its URL. Verify the artifact with `curl` first; treat only
    a failing `curl` as a failed deploy, and re-read `status` afterwards to confirm it flipped.

## Verification

Do not wait for the local resolver: after a CNAME change the edge already serves the site while
`curl <domain>` still says "Could not resolve host". Verify against the edge IP directly, then
re-check the plain hostname later to confirm propagation.

```bash
dig <domain> +short          # Cloudflare edge IPs for the new CNAME
curl --resolve <domain>:443:<edge-ip> -o /dev/null -w '%{http_code} %{size_download}\n' https://<domain>/<path>
```

- `curl -sI https://<user>.github.io/<repo>/<file>` → HTTP 200
- `gh api /repos/{owner}/{repo}/pages --jq '.status'` → "built" (not "building" or "failed")
- `gh api /repos/{owner}/{repo}/actions/runs` → conclusion: success (not failure)

## GitHub CLI Auth

```bash
gh auth status  # verify logged in
gh api /repos/{owner}/{repo} --jq '.html_url'  # verify repo access
```
Requires `repo` scope token.

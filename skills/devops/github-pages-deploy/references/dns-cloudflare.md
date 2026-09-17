# Custom domain on GitHub Pages behind Cloudflare

Ordered procedure — doing it out of order leaves Pages stuck on "domain not verified".

## 1. Publish the branch content first

`CNAME` file at the ROOT of the publishing branch, containing the bare hostname (no scheme, no
path, trailing newline fine):

```bash
echo 'sub.domain.tld' > CNAME
git add CNAME && git commit -m "publish: CNAME for sub.domain.tld"
git push -f origin gh-pages
```

Without this file GitHub Pages will not claim the domain, no matter what the API says.

## 2. Point DNS at the Pages hostname

Cloudflare DNS → the record for the subdomain:

- Type `CNAME`, name = the subdomain label, target `<owner>.github.io`, **Proxy ON**.
- Keep it **DNS-only vs proxied** in mind: proxied gives Cloudflare's cert + IPs on `dig`; that is
expected and fine. `dig <domain> +short` returns Cloudflare edge IPs, not GitHub IPs.

### Apex vs subdomain — the conflict rule

DNS forbids an A record and a CNAME **for the same name**. Two ways out:

- **Replace** the existing A record with the CNAME (destructive: whatever the A pointed at stops
  being reachable — only do this once the old origin is confirmed dead/retired).
- **Add a NEW subdomain** CNAME (additive, zero risk to existing services). Prefer this whenever the
  apex still serves something else, and always prefer it when the old target might come back.

## 3. Register the domain in GitHub Pages

```bash
gh api /repos/{owner}/{repo}/pages --jq '.cname, .status, .https_enforced, .pending_domain_unverified_at'
```

`pages-build-deployment` is a GitHub-managed dynamic workflow: it has **no** `workflow_dispatch`, so
it cannot be triggered by hand. It re-runs when the publishing branch gets a new commit.

## 4. Verify before propagation completes

A stale local resolver will report `Could not resolve host` for minutes after the edge is already
serving. Do not read that as failure:

```bash
dig <domain> +short                                        # edge IPs
dig <domain> CNAME +short                                  # confirm the CNAME chain
curl --resolve <domain>:443:<edge-ip> -o /dev/null -w '%{http_code}\n' https://<domain>/
```

macOS resolver flush (needs an interactive shell for sudo; if it is unavailable, just use
`--resolve` and move on):

```bash
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder
```

## States you will see and what they mean

| Signal | Meaning | Action |
|---|---|---|
| `status: building` for minutes | Build queued/running | Poll; the build is not instant |
| `status: built`, domain still unresolvable | DNS propagation lag | Verify via `--resolve`, wait |
| `https_enforced: false` | Normal behind a Cloudflare proxy | Nothing; do not chase a cert |
| `pending_domain_unverified_at` set | GitHub has not claimed the domain yet | Confirm the `CNAME` file is in the branch root and DNS resolves |
| `422 The gh-pages branch must exist...` | Source branch missing | Create the branch, then set the source |

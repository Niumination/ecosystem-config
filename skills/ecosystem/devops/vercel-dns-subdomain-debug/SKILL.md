---
name: vercel-dns-subdomain-debug
category: devops
description: >-
  Use when Vercel domain shows red/invalid config. Debug www.
---

# Vercel DNS Subdomain Debug

## When to use

Vercel dashboard shows a domain (especially `www`) as red/"Invalid Configuration" or "Third Party" despite:
- The site responding HTTP 200
- The cert being valid (Let's Encrypt CN=www)
- The apex domain being green/Verified

## Root causes (in order of likelihood)

1. **Mixed nameservers at registrar** — registrar still has idwebhost NS alongside vercel-dns NS → Vercel classifies as "Third Party"
2. **CNAME pointing to generic `cname.vercel-dns.com`** instead of project-specific `<hash>.vercel-dns-017.com`
3. **Local DNS cache stale** — resolver (1.1.1.1, 9.9.9.9) still caches old NS, but global DNS already propagated; causes misleading `NXDOMAIN` locally while the domain works globally
4. **Domain not attached to project** — www added to account but not to specific project

## Diagnostic procedure

### Step 1 — Check what Vercel sees
```bash
vercel domains verify www.example.com 2>&1 | grep -E '"status"|"domainStatus"|"current"|nameservers' | head -15
```
Key fields:
- `domainStatus: "invalid-configuration"` → proceed
- `domainStatus: "configured-correctly"` → Vercel happy; problem is only dashboard cache, refresh
- `current.nameservers` → what Vercel's resolver sees for NS

### Step 2 — Confirm global DNS state via DoH (bypasses local cache)
```bash
# NS check
curl -s --max-time 10 "https://dns.google/resolve?name=example.com&type=NS" > /tmp/ns.json
cat /tmp/ns.json | python3 -c "import sys,json; d=json.load(sys.stdin); [print(r.get('data'), 'TTL', r.get('TTL')) for r in d.get('Answer', [])]"

# www A check
curl -s --max-time 10 "https://dns.google/resolve?name=www.example.com&type=A" > /tmp/www.json
cat /tmp/www.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('Status:', d.get('Status')); [print(r.get('type'), r.get('data'), 'TTL', r.get('TTL')) for r in d.get('Answer', [])]"
```
- If NS = `ns1/ns2.vercel-dns.com` globally but Vercel still shows mixed → wait TTL seconds (check TTL field)
- If NS still mixed globally → fix at registrar panel (idwebhost: replace all NS entries with only ns1/ns2.vercel-dns.com)

### Step 3 — Check project attachment
```bash
vercel domains add www.example.com <project> 2>&1 | head -8
```
- `domain_already_assigned` → attached correctly
- `project_required_for_subdomain` → was added without project; www requires explicit project name

### Step 4 — Check and fix CNAME record
```bash
vercel dns ls example.com 2>&1 | grep -i www
```
Vercel recommends a **project-specific** CNAME like `d0a001efa465354b.vercel-dns-017.com`, NOT generic `cname.vercel-dns.com`.

If wrong CNAME is present:
```bash
# Remove old CNAME (get ID from dns ls output)
vercel dns rm <rec_ID> --yes

# Add project-specific CNAME (get correct value from vercel domains verify, 'recommended' field)
vercel dns add example.com www CNAME <hash>.vercel-dns-017.com
```

### Step 5 — Force re-verify
```bash
vercel domains verify www.example.com 2>&1 | grep -E '"domainStatus"|"ok"'
```
Expected: `"domainStatus": "configured-correctly"`, `"ok": true`

## Pitfalls

- **`vercel domains rm www.example.com` fails "Domain not found"** when www is project-level, not account-level. Use `vercel domains add www.example.com <project>` to re-attach.
- **`nslookup` NXDOMAIN but HTTP 200 works**: local resolver cache is stale. Use DoH (`dns.google/resolve`) for true global state — never diagnose from local `nslookup`/`dig` when UDP 53 is firewalled or cached.
- **`sudo dscacheutil -flushcache` needs interactive terminal**: agent cannot run it. User must run in Terminal manually.
- **TTL NS = 21600s (6 hours)**: 1.1.1.1 may cache old NS up to 6h even after local flush. 8.8.8.8 often expires sooner. Check TTL field in DoH response.
- **`vercel domains verify` mixes human text + JSON**: pipe to `grep` for fields, not `python3 json.load(sys.stdin)` — non-JSON prefix lines break the parser.
- **`vercel dns rm` syntax**: `vercel dns rm <rec_ID> --yes` (ID only). `vercel dns rm <domain> <ID>` = "Invalid number of arguments".
- **Generic vs project-specific CNAME**: `cname.vercel-dns.com` = account-level = triggers "Third Party". Always use project-specific hash CNAME from `vercel domains verify` recommended field.
- **`vercel domains ls` shows apex only**: www subdomain assignments are per-project. Use `vercel domains inspect www.example.com` for per-subdomain status.

## Verify TLS independently of DNS
```bash
# Test cert + HTTP via IP directly, bypassing DNS
echo | openssl s_client -connect <vercel_ip>:443 -servername www.example.com 2>&1 | grep -E "subject|issuer"
curl -s -o /dev/null -w "HTTP: %{http_code}\n" \
  --resolve www.example.com:443:<vercel_ip> \
  "https://www.example.com"
```
HTTP 200 + valid cert here = site works globally. "Invalid configuration" is purely Vercel CLI/dashboard resolver cache, not a real outage.

## Vercel IP addresses (as of Sep 2026)
- `216.198.79.1` / `64.29.17.1` (apex A records)
- `216.198.79.65` / `64.29.17.65` (www, may differ)

## Final state confirmation
Dashboard turns green once `vercel domains verify` returns `configured-correctly`. If site works (HTTP 200, cert valid) but dashboard still red: wait TTL, or test from a different network that already sees the new NS.

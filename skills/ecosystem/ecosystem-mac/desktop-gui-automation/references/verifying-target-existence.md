# Verifying a named target actually exists

A "pelajari X" request names a target that may not exist. Search engines return
same-name results for unrelated things (a makeup artist, a different tool, a
parked domain) — none of which is the target. Confirm existence with a direct
probe BEFORE studying anything, and report a target that does not resolve as
unverifiable rather than substituting a lookalike.

## Probe the exact name first

```bash
dig +short TARGET.sh A                 # empty = no A record
curl -sI -m 8 -o /dev/null -w 'HTTP=%{http_code}\n' https://TARGET.sh
whois TARGET.sh | grep -iE 'registrar|creation date|status'
```

Then widen only across plausible variants of the same name, not to unrelated
hits:

```bash
for d in TARGET.sh www.TARGET.sh TARGET.dev TARGET.ai TARGETd.sh; do
  printf '%-24s ' "$d"
  dig +short "$d" A | tr '\n' ' '; echo
done
```

Empty `dig` plus `HTTP=000` is a solid negative. `whois` showing
`status: ACTIVE` with no registrar or creation data means the name is
registered-but-not-resolving (or a registry that withholds data) — report
that distinction, it is not the same as "does not exist".

## A negative result is a real deliverable

When the target does not resolve, say so plainly and stop. Do not fill the gap
with the best-matching unrelated search result — that manufactures a study of
something the user never asked about. Ask for the full URL, repo, or a
screenshot instead.

A single unverified name inside a multi-target request is a normal outcome;
report it per-target and complete the ones that did verify.

## When the only trace is social media

Platforms like Instagram refuse automated extraction. A name that appears only
in influencer posts has no auditable source — no license, no source code, no
security posture to assess. State the trace, state that it could not be
verified, and request the direct source. Do not infer a product's contents from
a post caption.

## Foreign characters in generated prose

Long generated documents can pick up stray CJK or Cyrillic characters in
otherwise-Indonesian sentences. They are invisible on a casual read and ship
straight into the repo. After writing, scan and repair before committing:

```python
import re
s = open(path, encoding='utf-8').read()
print(set(re.findall(r'[\u4e00-\u9fff\uac00-\ud7af\u0400-\u04ff]', s)))  # {} == clean
```

Re-run until the set is empty. Fix with targeted replacements, not a blanket
rewrite, so real content is preserved.

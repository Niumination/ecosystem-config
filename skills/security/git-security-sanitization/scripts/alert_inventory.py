#!/usr/bin/env python3
"""Account-wide open secret-scanning alert inventory — masked by construction.

Usage:
    python3 alert_inventory.py <owner> [--limit 200]

Answers "what is exposed across this account right now?" BEFORE triaging any single repo:
  * groups open alerts by secret type and repository visibility
  * prints file, first-seen date, validity, and publicly_leaked per alert
  * lists, separately, the repos where secret scanning is DISABLED

A `404 Secret scanning is disabled on this repository` is NOT "zero alerts": the guard is off, so
that repo can leak silently. Report that class on its own.

The alert API returns no secret value (type, locations, validity only), so this script cannot print
one even by accident. Requires `gh` authenticated for the owner.
"""
import json
import subprocess
import sys
from collections import defaultdict


def gh(path):
    p = subprocess.run(["gh", "api", path, "--paginate"], capture_output=True, text=True)
    if p.returncode != 0:
        return None, (p.stderr.strip() or p.stdout.strip())
    try:
        return json.loads(p.stdout or "null"), None
    except json.JSONDecodeError:
        return None, "unparseable gh output"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    owner = sys.argv[1]
    limit = 200
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    p = subprocess.run(["gh", "repo", "list", owner, "--limit", str(limit),
                        "--json", "name,visibility"], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"gh repo list failed: {p.stderr.strip()}")
        return 1
    repos = json.loads(p.stdout or "[]")
    if not repos:
        print(f"no repositories listed for {owner}")
        return 1

    visibility = {r["name"]: r.get("visibility", "?") for r in repos}
    groups = defaultdict(lambda: {"n": 0, "repos": set(), "validity": set()})
    per_repo = defaultdict(list)
    disabled, errored = [], []

    for name in sorted(visibility):
        alerts, err = gh(f"repos/{owner}/{name}/secret-scanning/alerts?state=open&per_page=100")
        if alerts is None:
            (disabled if "disabled" in (err or "").lower() else errored).append((name, err))
            continue
        for a in alerts:
            tipe = a.get("secret_type_display_name") or a.get("secret_type") or "?"
            loc = a.get("first_location_detected") or {}
            key = (tipe, visibility[name])
            groups[key]["n"] += 1
            groups[key]["repos"].add(name)
            groups[key]["validity"].add(str(a.get("validity")))
            per_repo[name].append((tipe, loc.get("path"), a.get("created_at"),
                                   a.get("validity"), a.get("publicly_leaked"), loc.get("blob_sha")))

    total = sum(g["n"] for g in groups.values())

    for name in sorted(per_repo):
        print(f"\n{name} ({visibility[name]}) — {len(per_repo[name])} open alert(s)")
        for tipe, path, created, validity, pub, blob in per_repo[name]:
            print(f"  - {tipe}")
            print(f"      file: {path or '(unknown)'} | first seen: {created}")
            print(f"      validity: {validity} | publicly_leaked: {pub} | blob: {blob}")

    print(f"\n=== SUMMARY — {total} open alert(s) across {len(per_repo)} repo(s) ===")
    for (tipe, vis), g in sorted(groups.items(), key=lambda kv: (-kv[1]["n"], kv[0][0])):
        val = ", ".join(sorted(g["validity"])) or "?"
        print(f"  {g['n']:3}x  {tipe}  [{vis}]")
        print(f"        repos: {', '.join(sorted(g['repos']))}")
        print(f"        validity: {val}  (unknown == treat as live)")

    if disabled:
        print(f"\n=== SECRET SCANNING DISABLED ({len(disabled)} repo) — can leak silently ===")
        for name, _ in disabled:
            print(f"  {name} ({visibility.get(name, '?')})")
    if errored:
        print(f"\n=== could not query ({len(errored)}) ===")
        for name, err in errored:
            print(f"  {name}: {err[:120]}")

    print("\nNext: enumerate distinct values per alert, then probe each one read-only (see "
          "references/leaked-credential-blast-radius.md).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Scan a repo's ENTIRE history (every blob in every ref) for given secret values.

Usage:
    python3 history_secret_scan.py <repo-path> <source-file-with-secrets>

Secrets come from <source-file-with-secrets>: one per line, either a bare value or KEY=value
(the value after the first '='). Comments (#) and blank lines are skipped; values shorter than
8 chars are ignored. Values are NEVER printed - findings report the blob path, which form
matched, and the value index. Exit 1 on any finding, 0 when clean, 2 on usage error.

Why this exists: "0 hits in tracked files" is not evidence of safety. A blob removed from
tracking two commits later still answers on the host, and a scan that skips large blobs or
separator-formatted variants silently exempts them.
"""
import re
import subprocess
import sys
from pathlib import Path


def load_secrets(path: Path):
    out = []
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        val = line.split("=", 1)[1].strip() if "=" in line else line
        val = val.strip('"').strip("'")
        if len(val) >= 8:
            out.append(val)
    return out


def git(repo, *args, text=True):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=text)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    repo, src = sys.argv[1], Path(sys.argv[2])
    if not (Path(repo) / ".git").exists():
        print(f"not a git repo: {repo}")
        return 2

    secrets = load_secrets(src)
    print(f"secrets loaded: {len(secrets)} (values not printed)")
    if not secrets:
        return 2

    # plain form + separator-tolerant form (1994-07-27 / 1994 07 27 / 1994.07.27)
    patterns = [(re.compile(re.escape(s)),
                 re.compile(r"[\s\-\.\u2013\u2014]*".join(map(re.escape, s))))
                for s in secrets]

    blob_to_path = {}
    for line in git(repo, "rev-list", "--objects", "--all").stdout.splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            blob_to_path.setdefault(parts[0], parts[1])

    listing = git(repo, "cat-file", "--batch-all-objects",
                  "--batch-check=%(objecttype) %(objectname) %(objectsize)").stdout
    blobs = [l.split() for l in listing.splitlines() if l.startswith("blob ")]
    total = sum(int(b[2]) for b in blobs)
    print(f"blobs: {len(blobs)}  total {total / 1e6:.1f} MB  (no size cap)")

    findings = []
    for _, sha, _size in blobs:
        content = git(repo, "cat-file", "blob", sha, text=False).stdout
        txt = content.decode("utf-8", errors="ignore")
        for idx, (plain, sep) in enumerate(patterns, 1):
            if plain.search(txt):
                findings.append((blob_to_path.get(sha, "(unknown path)"), idx, "plain"))
            elif sep.search(txt):
                findings.append((blob_to_path.get(sha, "(unknown path)"), idx, "separator"))

    print(f"\nfindings: {len(findings)}")
    for path, idx, form in sorted(set(findings)):
        print(f"  secret[{idx}] {form:10} {path}")

    if findings:
        print("\n=> LEAK STILL IN HISTORY - history rewrite required "
              "(see references/history-rewrite-dry-run.md)")
        return 1
    print("=> clean: no secret found in any blob of any ref")
    return 0


if __name__ == "__main__":
    sys.exit(main())

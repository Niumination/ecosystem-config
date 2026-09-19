#!/usr/bin/env python3
"""Scan every blob reachable from every ref of a repo for secret-shaped patterns.

Usage:
    python3 blob_history_pattern_scan.py <repo-path>

Why this exists: a name sweep proves whether a credential FILE existed and a tracked-file sweep only
sees the current checkout. Both miss the case that actually ships -- a secret in a file version that is
no longer in HEAD. This walks git objects directly, so the plaintext value is never needed as input and
is never printed: findings show the blob prefix, the path, the pattern class, and a masked sample
(first 6 characters + character count).

Exit: 0 clean, 1 any credential-class finding, 2 usage error.
"""

import re
import subprocess
import sys
from collections import defaultdict

# Credential classes -- a hit here is a finding (exit 1).
SECRET_PATTERNS = {
    "telegram_bot_token": re.compile(rb"\b\d{8,12}:[A-Za-z0-9_\-]{30,}\b"),
    "openai_style_key": re.compile(rb"\bsk-[A-Za-z0-9_\-]{20,}"),
    "github_pat": re.compile(rb"\b(?:ghp_|github_pat_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9_]{20,}"),
    "aws_key": re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    "jwt": re.compile(rb"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
    "private_key_block": re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer": re.compile(rb"[Bb]earer\s+[A-Za-z0-9._\-]{20,}"),
    "secret_assignment": re.compile(
        rb"(?i)\b(?:API_KEY|TOKEN|SECRET|PASSWORD)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{12,}"
    ),
    "nik_16digit": re.compile(rb"\b\d{16}\b"),
}

# Informational only -- reported as counts, never as a finding.
INFO_PATTERNS = {
    "ipv4_public": re.compile(
        rb"\b(?!10\.|127\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    ),
}


def mask(value: bytes) -> str:
    """Never reveal the value: first 6 characters plus its length."""
    return f"{value[:6].decode('utf-8', 'replace')}\u2026[MASKED {len(value)} chars]"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    repo = sys.argv[1]

    def git(args, stdin=None):
        proc = subprocess.run(["git", "-C", repo] + args, input=stdin, capture_output=True)
        return proc.stdout

    listing = git(["rev-list", "--all", "--objects"]).decode("utf-8", "replace")
    paths = defaultdict(set)
    shas = set()
    for line in listing.splitlines():
        parts = line.split(" ", 1)
        shas.add(parts[0])
        paths[parts[0]].add(parts[1] if len(parts) > 1 else "(no path)")

    # git rev-list --objects also emits trees and commits; keep blobs only.
    check = git(["cat-file", "--batch-check"], stdin="\n".join(sorted(shas)).encode()).decode()
    blobs = [line.split()[0] for line in check.splitlines() if " blob " in line]
    print(f"unique objects: {len(shas)} | blobs: {len(blobs)}")

    totals = defaultdict(int)
    samples = defaultdict(list)
    for sha in blobs:
        data = git(["cat-file", "blob", sha])
        for label, rx in {**SECRET_PATTERNS, **INFO_PATTERNS}.items():
            found = rx.findall(data)
            if not found:
                continue
            totals[label] += len(found)
            if label in SECRET_PATTERNS:
                for value in found[:2]:
                    samples[label].append((sha[:10], sorted(paths[sha])[0][:70], mask(value)))

    print("\n=== findings per pattern (all refs, history included) ===")
    for label in sorted(totals, key=lambda k: -totals[k]):
        kind = "FINDING" if label in SECRET_PATTERNS else "info"
        print(f"  {label:22} {totals[label]:6} occurrence(s)   [{kind}]")

    if samples:
        print("\n=== locations (values masked) ===")
        for label in sorted(samples):
            for sha, path, masked in samples[label]:
                print(f"  {label:20} blob {sha}  {path}\n{'':22}\u2192 {masked}")

    findings = sum(totals[label] for label in SECRET_PATTERNS if totals[label])
    print("\n=== values never printed ===")
    if findings:
        print(f"VERDICT: {findings} credential-class occurrence(s) — locate the introducing commit, "
              "report exposure anonymously, then follow the remediation ladder.")
        return 1
    print("VERDICT: no credential-class pattern in any blob of any ref.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

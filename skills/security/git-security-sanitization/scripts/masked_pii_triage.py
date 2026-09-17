#!/usr/bin/env python3
"""List credential/PII pattern hits in a repo with the matched value MASKED.

Usage:
    python3 masked_pii_triage.py [repo] [--untracked]

Scans `git ls-files` (or untracked paths with --untracked) and prints file, line, pattern
label, and +/-55 chars of surrounding context with the match replaced by [MASKED].
The value itself is never printed, so the output is safe to paste into a report or chat.

Exit 1 when hits exist (usable as a gate), 0 when clean.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PATTERNS = {
    "telegram_token": r"\b\d{8,12}:[A-Za-z0-9_\-]{30,}\b",
    "api_key_sk": r"\bsk-[A-Za-z0-9_\-]{20,}",
    "github_pat": r"\b(?:ghp_|github_pat_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9_]{20,}",
    "aws_key": r"\bAKIA[0-9A-Z]{16}\b",
    "jwt": r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}",
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "bearer": r"[Bb]earer\s+[A-Za-z0-9._\-]{20,}",
    "env_assignment": r"(?i)\b(?:API_KEY|TOKEN|SECRET|PASSWORD)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{12,}",
    # Indonesian NIK/KK. High false-positive rate (share/reel IDs, fixtures) - triage by context.
    "digit16": r"\b\d{16}\b",
}

SKIP_SUFFIX = (
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".tgz", ".db", ".sqlite",
    ".woff", ".woff2", ".ico", ".mp4", ".mov", ".xlsx", ".docx",
)
SELF = "masked_pii_triage.py"
CONTEXT = 55
MAX_BYTES = 2_000_000


def listing(repo: Path, untracked: bool) -> list[str]:
    if untracked:
        out = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain"],
            capture_output=True, text=True, check=True,
        ).stdout
        return [line[3:] for line in out.splitlines() if line.startswith("??")]
    out = subprocess.run(
        ["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True,
    ).stdout
    return [line for line in out.splitlines() if line]


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    untracked = "--untracked" in sys.argv
    repo = Path(args[0] if args else ".").resolve()
    hits = 0
    for rel in listing(repo, untracked):
        path = repo / rel
        if path.name == SELF or path.name.startswith("._") or path.suffix.lower() in SKIP_SUFFIX:
            continue
        if ".env" in path.name or not path.is_file() or path.stat().st_size > MAX_BYTES:
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for label, pattern in PATTERNS.items():
            for match in re.finditer(pattern, text):
                line = text[: match.start()].count("\n") + 1
                left = text[max(0, match.start() - CONTEXT): match.start()].replace("\n", " ")
                right = text[match.end(): match.end() + CONTEXT].replace("\n", " ")
                print(f"{rel}:L{line} [{label}] ...{left}[MASKED]{right}...")
                hits += 1
    print(f"\n=== {hits} hit(s) - values masked, output safe to share ===")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())

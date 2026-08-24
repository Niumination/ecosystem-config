#!/usr/bin/env python3
"""
niu-prime-context.py — AI Priming: baca notes relevan sebelum output (no-agent).

Konsep (dari ai-memory-vault): sebelum agen mulai tugas baru, baca notes
relevan dari brain/ supaya output berkualitas, bukan ngawang.

Cara pakai:
  python3 niu-prime-context.py <kata-kunci> [<kata-kunci> ...] [--limit 5]

Output: JSON [{"file":..., "score":..., "snippet":...}] → agen baca dan pakai.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BRAIN_DIR = Path("/Users/zaryu/Desktop/Niumination/brain")

# Berat kata kunci vs noise
STOP = {
    "dan", "atau", "yang", "di", "ke", "dari", "untuk", "dengan", "ini",
    "itu", "adalah", "pada", "akan", "tidak", "sudah", "juga", "saya",
    "kamu", "kami", "mereka", "harus", "bisa", "agar", "supaya", "the",
    "and", "for", "with", "from", "this", "that", "are", "was", "were",
}


def score_text(text: str, keywords: list[str]) -> int:
    low = text.lower()
    score = 0
    for kw in keywords:
        if kw in STOP:
            continue
        score += low.count(kw) * 2
    return score


def main() -> int:
    ap = argparse.ArgumentParser(description="AI Priming — baca notes relevan")
    ap.add_argument("keywords", nargs="+", help="kata kunci tugas")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--max-chars", type=int, default=800)
    args = ap.parse_args()

    if not BRAIN_DIR.is_dir():
        sys.stderr.write(f"ERROR: brain dir tidak ada: {BRAIN_DIR}\n")
        return 1

    results: list[dict] = []
    for md in BRAIN_DIR.rglob("*.md"):
        if any(seg.startswith(".") for seg in md.parts):
            continue
        try:
            text = md.read_text(errors="ignore")
        except Exception:
            continue
        score = score_text(text, args.keywords)
        if score <= 0:
            continue
        snippet = text[: args.max_chars].replace("\n", " ")
        results.append(
            {
                "file": str(md.relative_to(BRAIN_DIR)),
                "score": score,
                "snippet": snippet,
            }
        )

    results.sort(key=lambda r: -r["score"])
    print(json.dumps(results[: args.limit], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
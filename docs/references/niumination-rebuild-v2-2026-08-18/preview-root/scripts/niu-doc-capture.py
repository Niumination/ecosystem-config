#!/usr/bin/env python3
"""Tangkap jejak kerja ke ledger — tanpa LLM.

Mengambil: git status/diffstat di root NIU, STATE.yaml mtime, fence, ukuran AGENTS.md.
Ini pengganti 'model yang janji akan menulis dokumentasi'.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from niu_corelib import (  # noqa: E402
    append_session_ledger,
    core_dir,
    niu_root,
    now_iso,
    read_fence,
)


def git(args: list[str], cwd: Path) -> str:
    try:
        r = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        return (r.stdout or "").strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--note", default="")
    p.add_argument("--session-id", default="manual")
    args = p.parse_args()

    niu = niu_root()
    agents = niu / "AGENTS.md"
    entry = {
        "ts": now_iso(),
        "event": "doc-capture",
        "session_id": args.session_id,
        "note": args.note[:500],
        "cwd": str(niu),
        "git_status": git(["status", "--porcelain"], niu)[:2000],
        "git_diffstat": git(["diff", "--stat"], niu)[:2000],
        "git_head": git(["rev-parse", "--short", "HEAD"], niu),
        "agents_md_bytes": agents.stat().st_size if agents.is_file() else None,
        "fence": read_fence(),
        "core_exists": core_dir().is_dir(),
    }
    path = append_session_ledger(entry)
    day = entry["ts"][:10]
    md = core_dir() / "ledger" / f"{day}.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    header = f"# ledger {day}\n\n"
    line = (
        f"- `{entry['ts']}` capture head=`{entry['git_head']}` "
        f"dirty=`{bool(entry['git_status'])}` {args.note[:80]}\n"
    )
    if not md.exists() or md.stat().st_size == 0:
        md.write_text(header + line, encoding="utf-8")
    else:
        with md.open("a", encoding="utf-8") as fh:
            fh.write(line)
    print(str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

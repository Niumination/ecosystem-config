#!/usr/bin/env python3
"""Tulis / arsipkan / turunkan fence HANDOFF. Tanpa LLM."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from niu_corelib import (  # noqa: E402
    clear_fence,
    fence_path,
    handoff_path,
    read_fence,
    set_fence,
    write_handoff,
)


def main() -> int:
    p = argparse.ArgumentParser(description="Niumination handoff / fence")
    p.add_argument("--from-model", default="unknown")
    p.add_argument("--to-model", default="unknown")
    p.add_argument("--reason", default="manual")
    p.add_argument("--task", default="UNKNOWN")
    p.add_argument("--write", action="store_true", help="tulis HANDOFF + nyalakan fence")
    p.add_argument("--clear", action="store_true", help="turunkan fence (hanya manusia)")
    p.add_argument("--status", action="store_true")
    args = p.parse_args()

    if args.status or (not args.write and not args.clear):
        fence = read_fence()
        print(f"fence.active = {bool(fence.get('active'))}")
        print(f"fence.file   = {fence_path()}")
        print(f"handoff      = {handoff_path()} exists={handoff_path().is_file()}")
        if fence:
            print(fence)
        return 0

    if args.clear:
        clear_fence()
        print("fence diturunkan")
        return 0

    write_handoff(
        from_model=args.from_model,
        to_model=args.to_model,
        reason=args.reason,
        task_open=args.task,
    )
    set_fence(args.reason, args.from_model, args.to_model)
    print(f"HANDOFF ditulis: {handoff_path()}")
    print("fence AKTIF")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

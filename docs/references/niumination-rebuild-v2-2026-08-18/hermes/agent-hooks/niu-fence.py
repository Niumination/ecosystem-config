#!/usr/bin/env python3
"""Hermes shell hook — pre_tool_call. Baca JSON stdin, tulis block/allow ke stdout."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# izinkan import pustaka dari scripts/
ROOT_CANDIDATES = [
    Path("/Users/zaryu/Desktop/Niumination/scripts"),
    Path.home() / "niumination-rebuild" / "scripts",
]
HERE = Path(__file__).resolve()
for p in (
    HERE.parents[2] / "scripts",  # repo paket
    Path("/Users/zaryu/Desktop/Niumination/scripts"),
):
    if p.is_dir():
        sys.path.insert(0, str(p))
        break

from niu_corelib import decide_pre_tool  # noqa: E402


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        ev = json.loads(raw)
    except json.JSONDecodeError:
        return 0
    extra = ev.get("extra") if isinstance(ev.get("extra"), dict) else {}
    model = extra.get("model") or ev.get("model")
    tool = ev.get("tool_name") or ""
    tin = ev.get("tool_input") or {}
    decision = decide_pre_tool(str(tool), tin, model=model)
    if decision:
        sys.stdout.write(json.dumps(decision, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

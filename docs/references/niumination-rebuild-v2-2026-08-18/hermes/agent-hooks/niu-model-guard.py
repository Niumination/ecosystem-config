#!/usr/bin/env python3
"""Hermes shell hook — pre_llm_call. Suntik konteks + aktifkan fence jika model berganti."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
for p in (
    HERE.parents[2] / "scripts",
    Path("/Users/zaryu/Desktop/Niumination/scripts"),
):
    if p.is_dir():
        sys.path.insert(0, str(p))
        break

from niu_corelib import pre_llm_context  # noqa: E402


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        ev = json.loads(raw)
    except json.JSONDecodeError:
        return 0
    extra = ev.get("extra") if isinstance(ev.get("extra"), dict) else {}
    session_id = str(ev.get("session_id") or extra.get("session_id") or "unknown")
    model = extra.get("model") or ev.get("model")
    is_first = bool(extra.get("is_first_turn") or ev.get("is_first_turn"))
    ctx = pre_llm_context(session_id, model, is_first)
    if ctx:
        sys.stdout.write(json.dumps({"context": ctx}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

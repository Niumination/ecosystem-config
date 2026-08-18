#!/usr/bin/env python3
"""Hermes shell hook — on_session_end / on_session_finalize. Ledger tanpa LLM."""
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

from niu_corelib import append_session_ledger, now_iso, normalize_model_id  # noqa: E402


def main() -> int:
    raw = sys.stdin.read() or "{}"
    try:
        ev = json.loads(raw)
    except json.JSONDecodeError:
        return 0
    extra = ev.get("extra") if isinstance(ev.get("extra"), dict) else {}
    append_session_ledger(
        {
            "ts": now_iso(),
            "event": ev.get("hook_event_name") or "on_session_end",
            "session_id": ev.get("session_id") or extra.get("session_id"),
            "model": normalize_model_id(extra.get("model") or ev.get("model")),
            "platform": extra.get("platform") or ev.get("platform"),
            "completed": extra.get("completed"),
            "interrupted": extra.get("interrupted"),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

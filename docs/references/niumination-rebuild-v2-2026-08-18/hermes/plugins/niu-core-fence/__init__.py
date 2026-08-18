"""Plugin Hermes: niu-core-fence.

Harus di-enable eksplisit:
  hermes config set  →  plugins.enabled += niu-core-fence
Tidak mendaftarkan tool baru (model lemah tidak perlu tool tambahan).
"""
from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = [
    Path("/Users/zaryu/Desktop/Niumination/scripts"),
    Path(__file__).resolve().parents[3] / "scripts",
]
for p in _SCRIPTS:
    if p.is_dir():
        sys.path.insert(0, str(p))
        break

from niu_corelib import (  # noqa: E402
    append_session_ledger,
    decide_pre_tool,
    now_iso,
    normalize_model_id,
    pre_llm_context,
)


def register(ctx):
    def on_pre_tool(**kwargs):
        tool_name = kwargs.get("tool_name") or ""
        tool_input = kwargs.get("tool_input") or kwargs.get("params") or {}
        model = kwargs.get("model")
        decision = decide_pre_tool(str(tool_name), tool_input, model=model)
        return decision

    def on_pre_llm(**kwargs):
        session_id = str(kwargs.get("session_id") or "unknown")
        model = kwargs.get("model")
        is_first = bool(kwargs.get("is_first_turn"))
        ctx_txt = pre_llm_context(session_id, model, is_first)
        if ctx_txt:
            return {"context": ctx_txt}
        return None

    def on_end(**kwargs):
        append_session_ledger(
            {
                "ts": now_iso(),
                "event": "on_session_end",
                "session_id": kwargs.get("session_id"),
                "model": normalize_model_id(kwargs.get("model")),
                "platform": kwargs.get("platform"),
                "completed": kwargs.get("completed"),
                "interrupted": kwargs.get("interrupted"),
            }
        )

    ctx.register_hook("pre_tool_call", on_pre_tool)
    ctx.register_hook("pre_llm_call", on_pre_llm)
    ctx.register_hook("on_session_end", on_end)

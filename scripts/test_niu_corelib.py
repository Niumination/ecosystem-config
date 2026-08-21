#!/usr/bin/env python3
"""Uji pagar core — harus lulus tanpa mesin zaryu."""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import niu_corelib as C  # noqa: E402


def setup_tmp() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="niu-core-"))
    core = tmp / "core"
    core.mkdir(parents=True)
    (core / "runtime").mkdir()
    (core / "ledger" / "sessions").mkdir(parents=True)
    (core / "ledger" / "handoffs").mkdir(parents=True)
    (core / "CONSTITUTION.md").write_text("# hukum\n", encoding="utf-8")
    (core / "FREEZE.list").write_text(
        "core/CONSTITUTION.md\ncore/VISION.md\nvault/\n/Volumes/Niumination\n",
        encoding="utf-8",
    )
    os.environ["NIU"] = str(tmp)
    os.environ["NIU_CORE"] = str(core)
    return tmp


def assert_true(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"FAIL: {msg}")
    print(f"  ok  {msg}")


def main() -> int:
    setup_tmp()
    print("== classify_model ==")
    assert_true(C.classify_model("opencode-zen/nemotron-3-ultra-free") == "allowed", "nemotron allowed")
    assert_true(C.classify_model("nemotron-3-ultra-free") == "allowed", "bare nemotron allowed")
    assert_true(C.classify_model("opencode-zen/hy3-free") == "allowed", "hy3 allowed")
    assert_true(C.classify_model("hy3-free") == "allowed", "bare hy3 allowed")
    assert_true(C.classify_model("opencode-zen/nemotron-3.5-lightning-free") == "allowed", "lightning allowed")
    assert_true(C.classify_model("laguna-s-2.1-free") == "allowed", "laguna (bare -free) allowed")
    assert_true(C.classify_model("opencode-zen/big-pickle") == "allowed", "big-pickle re-allowed (D-0004)")
    assert_true(C.classify_model("big-pickle") == "allowed", "bare big-pickle allowed")
    assert_true(C.classify_model("deepseek-v4-flash-free") == "allowed", "deepseek-v4-flash-free allowed (zen free tier)")
    assert_true(C.classify_model("opencode-zen/deepseek-v4-flash") == "foreign", "paid zen (no -free) foreign")
    assert_true(C.classify_model("stepfun/step-3.7-flash:free") == "allowed", "nous :free allowed")
    assert_true(C.classify_model("upstage/solar-pro4:free") == "allowed", "nous :free allowed (2)")
    assert_true(C.classify_model("nous/stepfun/step-3.7-flash:free") == "allowed", "nous-prefixed :free allowed")
    assert_true(C.classify_model("anthropic/claude-opus-5") == "foreign", "nous paid (no :free) foreign")
    assert_true(C.classify_model("nous/anthropic/claude-opus-5") == "foreign", "nous paid foreign (2)")
    assert_true(C.classify_model("9router/gratislonggar") == "foreign", "gratislonggar foreign")
    assert_true(C.classify_model("gemini/gemini-3.x") == "foreign", "gemini foreign")
    assert_true(C.classify_model("juan-router/agnes-2.0-flash") == "foreign", "juan foreign")
    assert_true(C.classify_model("9router/big-pickle") == "foreign", "pickle via 9router foreign")
    assert_true(C.classify_model("9router/nemotron-3-ultra-free") == "foreign", "nemotron via 9router foreign")

    print("== freeze paths ==")
    niu = Path(os.environ["NIU"])
    assert_true(C.is_frozen_path(str(niu / "core" / "CONSTITUTION.md")), "constitution frozen")
    assert_true(C.is_frozen_path("/Volumes/Niumination/foo"), "ntfs trap frozen")
    assert_true(C.is_frozen_path(str(niu / "vault" / "x")), "vault frozen")
    assert_true(not C.is_frozen_path(str(niu / "brain" / "ops" / "a.md")), "brain/ops not frozen")

    print("== block frozen write ==")
    d = C.decide_pre_tool(
        "write_file",
        {"path": str(niu / "core" / "CONSTITUTION.md"), "content": "hack"},
        model="opencode-zen/nemotron-3-ultra-free",
    )
    assert_true(d is not None and d.get("action") == "block", "block write constitution")

    print("== allow normal write when no fence ==")
    d = C.decide_pre_tool(
        "write_file",
        {"path": str(niu / "brain" / "ops" / "note.md"), "content": "ok"},
        model="opencode-zen/nemotron-3-ultra-free",
    )
    assert_true(d is None, "allow brain/ops write")

    print("== foreign model cannot mutate ==")
    d = C.decide_pre_tool(
        "write_file",
        {"path": str(niu / "brain" / "ops" / "note.md"), "content": "no"},
        model="9router/gratislonggar",
    )
    assert_true(d is not None and d.get("action") == "block", "foreign blocked")

    print("== same-provider switch does NOT fence ==")
    ctx = C.pre_llm_context("sess-1", "opencode-zen/nemotron-3-ultra-free", True)
    assert_true("Hukum" in ctx or "hukum" in ctx.lower() or "CONSTITUTION" in ctx, "first turn inject")
    ctx2 = C.pre_llm_context("sess-1", "opencode-zen/hy3-free", False)
    assert_true("provider" in ctx2.lower(), "same-provider switch note")
    assert_true(not C.read_fence().get("active"), "no fence after same-provider switch")
    assert_true(not C.handoff_path().is_file(), "no handoff after same-provider switch")

    print("== nous→nous switch does NOT fence ==")
    C.clear_fence()
    C.pre_llm_context("sess-n1", "stepfun/step-3.7-flash:free", True)
    ctxn = C.pre_llm_context("sess-n1", "upstage/solar-pro4:free", False)
    assert_true(not C.read_fence().get("active"), "no fence nous→nous")
    assert_true(not C.handoff_path().is_file(), "no handoff nous→nous")

    print("== cross-provider (zen→nous) switch fences ==")
    C.clear_fence()
    C.pre_llm_context("sess-x1", "opencode-zen/nemotron-3-ultra-free", True)
    C.clear_fence()
    ctxc = C.pre_llm_context("sess-x1", "stepfun/step-3.7-flash:free", False)
    assert_true(C.read_fence().get("active") is True, "fence on cross-provider switch")
    assert_true(C.handoff_path().is_file(), "handoff on cross-provider switch")
    C.clear_fence()

    print("== foreign switch raises fence ==")
    ctx3 = C.pre_llm_context("sess-2", "9router/gratislonggar", True)
    assert_true("BUKAN otak" in ctx3, "foreign model inject")
    assert_true(C.read_fence().get("active") is True, "fence on after foreign switch")
    assert_true(C.handoff_path().is_file(), "handoff written after foreign switch")

    print("== foreign→allowed keeps fence ==")
    ctx4 = C.pre_llm_context("sess-2", "opencode-zen/hy3-free", False)
    assert_true("fence" in ctx4.lower() or "HANDOFF" in ctx4, "return-to-allowed warns fence")
    assert_true(C.read_fence().get("active") is True, "fence stays active on return to allowed")

    print("== same-provider switch with active fence warns ==")
    ctx5 = C.pre_llm_context("sess-5", "opencode-zen/nemotron-3-ultra-free", True)
    ctx6 = C.pre_llm_context("sess-5", "opencode-zen/hy3-free", False)
    assert_true("provider" in ctx6.lower(), "same-provider switch note (fence still on)")
    assert_true("fence" in ctx6.lower(), "same-provider switch notes active fence")

    d = C.decide_pre_tool(
        "write_file",
        {"path": str(niu / "core" / "STATE.yaml"), "content": "x"},
        model="opencode-zen/hy3-free",
    )
    assert_true(d is not None and d.get("action") == "block", "fence blocks core mutate")

    print("== shell freeze ==")
    d = C.decide_pre_tool(
        "terminal",
        {"command": "echo pwned >> core/CONSTITUTION.md"},
        model="opencode-zen/nemotron-3-ultra-free",
    )
    assert_true(d is not None and d.get("action") == "block", "shell rewrite constitution blocked")

    print("\nALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

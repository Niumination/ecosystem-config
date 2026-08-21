#!/usr/bin/env python3
"""Pustaka inti Niumination — tanpa LLM.

Dipakai hook Hermes, plugin, dan CLI. Gagal-aman: jika ragu, BLOCK.
"""
from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Iterable

WIB = timezone(timedelta(hours=7))

DEFAULT_NIU = "/Users/zaryu/Desktop/Niumination"
ALLOWED_MODELS = (
    "nemotron-3-ultra-free",
    "hy3-free",
    "nemotron-3.5-lightning-free",
    "mimo-v2.5-free",
)
ALLOWED_PROVIDER = "opencode-zen"
# Teks tampilan untuk pesan enforcement (satu sumber, hindari drift antar string)
ALLOWED_MODELS_TEXT = (
    "opencode-zen/nemotron-3-ultra-free · opencode-zen/nemotron-3.5-lightning-free · "
    "opencode-zen/hy3-free · opencode-zen/mimo-v2.5-free"
)

WRITE_TOOLS = {
    "write_file",
    "write",
    "edit_file",
    "edit",
    "str_replace",
    "apply_patch",
    "create_file",
    "delete_file",
    "remove_file",
    "move_file",
    "rename_file",
    "patch",
    "notebook_edit",
}

SHELL_TOOLS = {"terminal", "bash", "shell", "execute", "run_command", "command"}

SHELL_WRITE_HINT = re.compile(
    r"(>>?|tee\b|sed\s+-i|perl\s+-i|rm\s|mv\s|cp\s|chmod\s|chown\s|"
    r"truncate\b|unlink\b|rsync\s|install\s)",
    re.I,
)

FROZEN_BASENAMES = {
    "constitution.md",
    "vision.md",
    "model.policy.yaml",
    "freeze.list",
    "scope.md",
    "soul.md",
    ".gitleaks.toml",
}


def now_iso() -> str:
    return datetime.now(WIB).strftime("%Y-%m-%dT%H:%M:%S+07:00")


def niu_root() -> Path:
    return Path(os.environ.get("NIU", DEFAULT_NIU)).expanduser()


def core_dir() -> Path:
    override = os.environ.get("NIU_CORE")
    if override:
        return Path(override).expanduser()
    return niu_root() / "core"


def runtime_dir() -> Path:
    p = core_dir() / "runtime"
    p.mkdir(parents=True, exist_ok=True)
    return p


def fence_path() -> Path:
    return runtime_dir() / "fence.json"


def handoff_path() -> Path:
    return runtime_dir() / "HANDOFF.md"


def session_model_path() -> Path:
    return runtime_dir() / "session-models.json"


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_freeze_patterns() -> list[str]:
    path = core_dir() / "FREEZE.list"
    if not path.is_file():
        return [
            "core/CONSTITUTION.md",
            "core/VISION.md",
            "core/MODEL.policy.yaml",
            "core/FREEZE.list",
            "vault/",
            "/Volumes/Niumination",
        ]
    out: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out


def expand_pattern(pat: str) -> str:
    if pat.startswith("~/"):
        return str(Path.home() / pat[2:])
    return pat


def norm(p: str | Path) -> str:
    s = str(p)
    if s.startswith("~/"):
        s = str(Path.home() / s[2:])
    try:
        return os.path.normpath(s)
    except Exception:
        return s


def path_matches(candidate: str, pattern: str) -> bool:
    c = norm(candidate)
    pat = expand_pattern(pattern)
    if pat.endswith("/**"):
        root = norm(pat[:-3])
        return c == root or c.startswith(root + os.sep)
    if pat.endswith("/") or pat.endswith(os.sep):
        root = norm(pat)
        return c == root or c.startswith(root + os.sep)
    if "*" in pat:
        # glob sederhana di basename atau suffix
        import fnmatch

        return fnmatch.fnmatch(c, norm(pat)) or fnmatch.fnmatch(os.path.basename(c), pat)
    p = norm(pat)
    return c == p or c.startswith(p + os.sep) or os.path.basename(c) == os.path.basename(p)


def is_frozen_path(candidate: str) -> bool:
    if not candidate:
        return False
    base = os.path.basename(norm(candidate)).lower()
    if base in FROZEN_BASENAMES:
        return True
    rel_try = candidate
    niu = str(niu_root())
    cn = norm(candidate)
    if cn.startswith(niu + os.sep):
        rel_try = cn[len(niu) + 1 :]
    for pat in load_freeze_patterns():
        if path_matches(candidate, pat) or path_matches(rel_try, pat):
            return True
    return False


def is_core_mutate_path(candidate: str) -> bool:
    """True jika path di bawah core/ (kecuali runtime handoff + ledger append)."""
    cn = norm(candidate)
    core = str(core_dir())
    if not (cn == core or cn.startswith(core + os.sep)):
        # relative
        if candidate.replace("\\", "/").startswith("core/"):
            cn2 = str(niu_root() / candidate)
            return is_core_mutate_path(cn2)
        return False
    rel = cn[len(core) + 1 :] if len(cn) > len(core) else ""
    if rel in {"runtime/HANDOFF.md", "runtime/fence.json", "runtime/session-models.json"}:
        return False
    if rel.startswith("ledger/"):
        return False
    return True


def extract_paths_from_obj(obj: Any) -> list[str]:
    found: list[str] = []

    def walk(x: Any, key: str | None = None) -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, str(k))
        elif isinstance(x, list):
            for i in x:
                walk(i, key)
        elif isinstance(x, str) and x:
            kl = (key or "").lower()
            if kl in {"path", "file", "filepath", "file_path", "target", "dest", "destination", "to"}:
                found.append(x)
            elif "/" in x or x.endswith((".md", ".yaml", ".yml", ".py", ".json", ".toml")):
                if len(x) < 400:
                    found.append(x)

    walk(obj)
    return found


def extract_command(tool_input: Any) -> str:
    if isinstance(tool_input, dict):
        for k in ("command", "cmd", "script", "code"):
            v = tool_input.get(k)
            if isinstance(v, str):
                return v
    if isinstance(tool_input, str):
        return tool_input
    return ""


def classify_model(model: str | None) -> str:
    """allowed | same-family handled by caller | foreign | unknown"""
    if not model:
        return "unknown"
    m = model.lower().strip()
    # normalize provider/model
    name = m.split("/")[-1]
    has_zen = "opencode-zen" in m or m.startswith("zen/")
    if name in ALLOWED_MODELS:
        # if provider explicitly something else, foreign
        if "9router" in m or "juan" in m or "huancheng" in m or "agentrouter" in m:
            return "foreign"
        return "allowed"
    if has_zen and name in ALLOWED_MODELS:
        return "allowed"
    return "foreign"


def normalize_model_id(model: str | None) -> str:
    if not model:
        return "unknown"
    m = model.strip()
    name = m.split("/")[-1]
    if name in ALLOWED_MODELS:
        return f"{ALLOWED_PROVIDER}/{name}"
    return m


def read_fence() -> dict[str, Any]:
    data = load_json(fence_path(), {})
    if not isinstance(data, dict):
        return {"active": False}
    return data


def set_fence(reason: str, frm: str, to: str) -> dict[str, Any]:
    data = {
        "active": True,
        "reason": reason,
        "from": frm,
        "to": to,
        "ts": now_iso(),
    }
    save_json(fence_path(), data)
    return data


def clear_fence() -> None:
    save_json(fence_path(), {"active": False, "cleared": now_iso()})


def remember_session_model(session_id: str, model: str) -> tuple[str | None, bool]:
    """Return (previous_model, switched)."""
    db = load_json(session_model_path(), {})
    if not isinstance(db, dict):
        db = {}
    prev = db.get(session_id)
    db[session_id] = model
    # keep small
    if len(db) > 200:
        keys = list(db.keys())[:-80]
        for k in keys:
            db.pop(k, None)
    save_json(session_model_path(), db)
    switched = bool(prev) and normalize_model_id(prev) != normalize_model_id(model)
    return (prev, switched)


def write_handoff(
    *,
    from_model: str,
    to_model: str,
    reason: str,
    task_open: str = "UNKNOWN",
    extra: str = "",
) -> Path:
    body = (
        f"# HANDOFF\n\n"
        f"```yaml\n"
        f"ts: {now_iso()}\n"
        f"from_model: {from_model}\n"
        f"to_model: {to_model}\n"
        f"reason: {reason}\n"
        f"task_open: {task_open}\n"
        f"files_touched: []\n"
        f"last_goal_one_line: UNKNOWN\n"
        f"done: UNKNOWN\n"
        f"not_done: UNKNOWN\n"
        f"do_not_repeat: jangan lanjut tugas seolah model tidak berganti\n"
        f"next_human_or_same_family: tunggu zaryu atau {ALLOWED_MODELS_TEXT} setelah fence turun\n"
        f"```\n\n"
        f"{extra}\n"
    )
    dest = handoff_path()
    dest.write_text(body, encoding="utf-8")
    archive = core_dir() / "ledger" / "handoffs"
    archive.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(WIB).strftime("%Y%m%d-%H%M%S")
    shutil.copy2(dest, archive / f"{stamp}.md")
    return dest


def tool_is_mutating(tool_name: str) -> bool:
    t = (tool_name or "").lower()
    if t in WRITE_TOOLS or t in SHELL_TOOLS:
        return True
    if any(x in t for x in ("write", "edit", "patch", "delete", "remove", "move")):
        return True
    return False


def decide_pre_tool(tool_name: str, tool_input: Any, model: str | None = None) -> dict[str, Any] | None:
    """Return block dict or None (allow)."""
    tname = (tool_name or "").lower()
    paths = extract_paths_from_obj(tool_input)
    cmd = extract_command(tool_input)
    fence = read_fence()
    fence_on = bool(fence.get("active"))
    klass = classify_model(model) if model else "unknown"

    # always block frozen paths
    for p in paths:
        if is_frozen_path(p):
            return {
                "action": "block",
                "message": f"NIU-FENCE: dilarang menyentuh file beku: {p}",
            }

    if cmd and SHELL_WRITE_HINT.search(cmd):
        # scan freeze names inside command
        low = cmd.lower()
        for marker in (
            "constitution.md",
            "vision.md",
            "model.policy.yaml",
            "freeze.list",
            "soul.md",
            "/volumes/niumination",
            "vault/",
        ):
            if marker in low:
                return {
                    "action": "block",
                    "message": f"NIU-FENCE: perintah shell menyentuh wilayah beku ({marker})",
                }

    if klass == "foreign" and tool_is_mutating(tname):
        return {
            "action": "block",
            "message": (
                f"NIU-FENCE: model ini bukan otak yang diizinkan (hanya {ALLOWED_MODELS_TEXT}). "
                "Jangan mutasi file. Tulis HANDOFF jika belum, tunggu manusia."
            ),
        }

    if fence_on and tool_is_mutating(tname):
        # allow handoff / ledger only
        allowed = True
        if paths:
            allowed = all(
                (not is_frozen_path(p))
                and (
                    "runtime/HANDOFF.md" in norm(p)
                    or "/ledger/" in norm(p).replace("\\", "/")
                    or not is_core_mutate_path(p)
                )
                for p in paths
            )
            # if any path is core mutate (except runtime/ledger) block
            if any(is_core_mutate_path(p) or is_frozen_path(p) for p in paths):
                allowed = False
        else:
            # mutating without path (likely shell) — block if looks like write
            if tname in SHELL_TOOLS and SHELL_WRITE_HINT.search(cmd or ""):
                allowed = False
            elif tname in WRITE_TOOLS:
                allowed = False
        if not allowed:
            return {
                "action": "block",
                "message": (
                    "NIU-FENCE aktif setelah ganti model. "
                    "Jangan mutasi core. Baca core/runtime/HANDOFF.md. "
                    "Manusia menurunkan fence: python3 scripts/niu-handoff.py --clear"
                ),
            }

    return None


def pre_llm_context(session_id: str, model: str | None, is_first_turn: bool) -> str:
    bits: list[str] = []
    klass = classify_model(model)
    mid = normalize_model_id(model)
    prev, switched = remember_session_model(session_id or "unknown", mid)

    if klass == "foreign":
        write_handoff(
            from_model=str(prev or "unknown"),
            to_model=mid,
            reason="foreign_model",
        )
        set_fence("foreign_model", str(prev or "unknown"), mid)
        bits.append(
            f"[NIU] Kamu BUKAN otak yang diizinkan. Hanya {ALLOWED_MODELS_TEXT}. "
            "Jangan menulis file. Baca core/runtime/HANDOFF.md. Tunggu manusia."
        )
    elif switched:
        prev_klass = classify_model(prev)
        if prev_klass == "allowed" and klass == "allowed":
            # Sesama keluarga (nemotron/lightning/hy3/mimo): bebas lanjut, tanpa fence.
            bits.append(
                f"[NIU] Model berganti dalam keluarga {prev} → {mid}. "
                "Tidak ada fence. Lanjutkan sesuai Hukum & Scope."
            )
        else:
            # Kembali ke keluarga dari model asing: tanpa fence baru
            # (fence dari kejadian asing tetap aktif sampai manusia menurunkan).
            bits.append(
                f"[NIU] Model berganti {prev} → {mid}. Lanjutkan sesuai Hukum & Scope."
            )

    fence = read_fence()
    if fence.get("active") and not switched and klass != "foreign":
        bits.append(
            f"[NIU] Fence masih aktif ({fence.get('reason')}). "
            "Boleh baca dan mengisi HANDOFF. Jangan mengubah file beku atau core lain."
        )

    if is_first_turn:
        bits.append(
            "[NIU] Hukum: core/CONSTITUTION.md. Scope: core/SCOPE.md. "
            f"Otak: {ALLOWED_MODELS_TEXT}. Chat bukan arsip."
        )

    # keep tiny — weak models drown
    return "\n".join(bits)


def append_session_ledger(entry: dict[str, Any]) -> Path:
    day = datetime.now(WIB).strftime("%Y-%m-%d")
    folder = core_dir() / "ledger" / "sessions"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{day}.jsonl"
    line = json.dumps(entry, ensure_ascii=False)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return path

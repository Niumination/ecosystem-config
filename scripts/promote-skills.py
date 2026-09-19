#!/usr/bin/env python3
"""promote-skills.py — promosi KONSERVATIF skill lokal dari target Hermes ke bank pusat.

KEPUTUSAN PEMILIK (19 Sep 2026)
-------------------------------
D1: promosi otomatis HANYA untuk skill lokal BARU; konflik masuk karantina untuk ditinjau.
D3: TIDAK auto-commit - bank dibiarkan kotor agar ditinjau manusia.

ATURAN (semua harus terpenuhi)
------------------------------
1. folder skill ada di target dan punya SKILL.md dengan frontmatter `name` + `description`;
2. nama skill (folder atau `name:`) TIDAK ada di bank  -> tidak pernah menimpa apa pun;
3. bukan skill bawaan Hermes (`.bundled_manifest`);
4. bukan hasil instal hub (`.hub/lock.json` -> `installed`);
5. tidak ada di ledger tombstone (pernah sengaja dihapus dari bank) -> cegah "resurrect";
6. isinya tidak memuat pola kredensial.

Skill yang ADA di bank tetapi isinya berbeda TIDAK disentuh di sini - itu urusan
`sync-guard.py` (karantina, jangan timpa) sesuai keputusan D2.

Ledger: skills/.promotion-ledger.json  (promoted / ignored-bundled / ignored-hub /
tombstone / rejected) -> membuat proses idempoten dan dapat diaudit.

Usage:
  python3 scripts/promote-skills.py [--dry-run] [--json]
Exit: 0 selalu (kecuali error teknis).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import sys
from datetime import datetime, timezone

# Path bisa di-override lewat env agar skrip dapat diuji di sandbox (tanpa menyentuh data nyata).
BANK = pathlib.Path(os.environ.get("NIU_BANK", "/Users/zaryu/Desktop/Niumination/skills"))
TARGET = pathlib.Path(os.environ.get("NIU_TARGET", pathlib.Path.home() / ".hermes" / "skills"))
LEDGER = BANK / ".promotion-ledger.json"
SKIP_FILES = {".DS_Store"}
SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".pytest_cache"}
PLACEHOLDER_MARKS = ("...", "<", ">", "{{", "${", "xxxx", "XXXX", "REDACTED", "PLACEHOLDER", "YOUR_", "EXAMPLE", "abc")

SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9_\-]{16,}", "openai-style key"),
    (r"ghp_[A-Za-z0-9]{20,}", "github token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "github pat"),
    (r"AIza[0-9A-Za-z_\-]{20,}", "google api key"),
    (r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}", "jwt"),
    (r"postgres(?:ql)?://[^\s\"']+:[^\s\"']+@", "db url with password"),
    (r"xox[baprs]-[A-Za-z0-9\-]{10,}", "slack token"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"(?i)service_role_key\s*[:=]\s*[\"']?[A-Za-z0-9_\-\.]{20,}", "supabase service role"),
    (r"(?i)(password|passwd|secret)\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']", "hardcoded password"),
]


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_json(p: pathlib.Path, default):
    try:
        return json.loads(p.read_text())
    except Exception:
        return default


def frontmatter(md: pathlib.Path) -> tuple[str, str] | None:
    try:
        text = md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = re.match(r"^---\n(.*?)\n---", text, re.S) or re.search(r"\n---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    n = re.search(r"^name:\s*(.+)$", fm, re.M)
    d = re.search(r"^description:\s*(>|\|)?\s*(.*)$", fm, re.M)
    if not n or not d:
        return None
    name = n.group(1).strip().strip("\"'")
    desc = d.group(2).strip().strip("\"'")
    if not name or not desc:
        return None
    return name, desc


def secret_hit(skill_dir: pathlib.Path) -> str | None:
    for f in sorted(skill_dir.rglob("*")):
        if not f.is_file() or f.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat, label in SECRET_PATTERNS:
            for m in re.finditer(pat, text):
                tok = m.group(0)
                # Placeholder/bait (mis. "sk-abc...6789") bukan rahasia nyata: token berisi
                # ellipsis, kurung template, atau kata penanda contoh. Tanpa aturan ini,
                # fixture self-test scanner (bait-*.sh) akan selalu ditolak false-positive.
                if any(mark in tok for mark in PLACEHOLDER_MARKS):
                    continue
                return f"{label} di {f.relative_to(skill_dir)}"
    return None


def bundled_names() -> set[str]:
    p = TARGET / ".bundled_manifest"
    out = set()
    if p.exists():
        for line in p.read_text(errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                out.add(line.split(":")[0])
    return out


def hub_names() -> set[str]:
    d = load_json(TARGET / ".hub" / "lock.json", {})
    inst = d.get("installed", {}) if isinstance(d, dict) else {}
    out = set(inst.keys()) if isinstance(inst, dict) else set()
    if isinstance(inst, dict):
        for v in inst.values():
            ip = (v or {}).get("install_path")
            if ip:
                out.add(pathlib.PurePosixPath(ip).name)
    return out


def bank_names() -> set[str]:
    out = set()
    for md in BANK.rglob("SKILL.md"):
        parts = md.relative_to(BANK).parts
        if any(x.startswith(".") for x in parts):
            continue
        out.add(md.parent.name)
        fm = frontmatter(md)
        if fm:
            out.add(fm[0])
    return out


def target_skills() -> dict[str, pathlib.Path]:
    out = {}
    for md in sorted(TARGET.rglob("SKILL.md")):
        parts = md.relative_to(TARGET).parts
        if any(x.startswith(".") for x in parts):
            continue
        out[md.parent.name] = md.parent
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    ledger = load_json(LEDGER, {"version": 1, "promoted": {}, "ignored": {}, "tombstones": []})
    ledger.setdefault("promoted", {})
    ledger.setdefault("ignored", {})
    ledger.setdefault("tombstones", [])

    bank = bank_names()
    bundled = bundled_names()
    hub = hub_names()
    tombstones = set(ledger["tombstones"])
    now = datetime.now(timezone.utc).isoformat()

    promoted, ignored, rejected = [], [], []
    for name, sdir in target_skills().items():
        if name in bank:
            continue                                     # sudah ada di bank - bukan urusan promosi
        if name in tombstones:
            ignored.append((name, "tombstone"))
            continue
        if name in bundled:
            ignored.append((name, "bundled"))
            continue
        if name in hub:
            ignored.append((name, "hub"))
            continue

        fm = frontmatter(sdir / "SKILL.md")
        if not fm:
            rejected.append((name, "frontmatter tidak valid (name/description)"))
            continue
        hit = secret_hit(sdir)
        if hit:
            rejected.append((name, f"pola kredensial: {hit}"))
            continue

        rel = sdir.relative_to(TARGET)
        domain = rel.parts[0] if len(rel.parts) > 1 else "."
        key = name if domain == "." else f"{domain}/{name}"
        dest = BANK / domain / name
        if dest.exists():
            rejected.append((name, f"tujuan sudah ada: {dest.relative_to(BANK)}"))
            continue

        if a.dry_run:
            promoted.append((name, key, "DRY-RUN"))
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(sdir, dest)
        files = {f.relative_to(dest).as_posix(): sha(f)
                 for f in sorted(dest.rglob("*")) if f.is_file() and f.name not in SKIP_FILES}
        ledger["promoted"][key] = {
            "name": name, "domain": domain, "files": len(files),
            "bundleHash": hashlib.sha256(
                "\n".join(f"{k}:{v}" for k, v in sorted(files.items())).encode()).hexdigest(),
            "source": str(sdir), "promotedAt": now,
        }
        promoted.append((name, key, f"{len(files)} berkas"))

    for name, why in ignored:
        ledger["ignored"][name] = {"reason": why, "checkedAt": now}
    for name, why in rejected:
        ledger["ignored"][name] = {"reason": f"rejected: {why}", "checkedAt": now}
    if not a.dry_run:
        ledger["updatedAt"] = now
        LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")

    if a.json:
        print(json.dumps({"promoted": promoted, "ignored": ignored, "rejected": rejected,
                          "dry_run": a.dry_run}, indent=2))
        return 0

    mode = "DRY-RUN" if a.dry_run else "dipromosikan"
    print(f"[promosi] {mode}: {len(promoted)} · diabaikan: {len(ignored)} · ditolak: {len(rejected)}")
    for n, d, extra in promoted:
        print(f"  + {n} → {d} ({extra})")
    for n, why in ignored[:5]:
        print(f"  = diabaikan {n}: {why}")
    for n, why in rejected:
        print(f"  ! ditolak {n}: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""promote-skills.py — Two-Way Convergence: serap skill, berkas pendukung, dan update dari target Hermes ke bank pusat.

FUNGSI:
-------
1. Promosi skill BARU di target (autoskills, clone, session creation).
2. Promosi berkas pendukung BARU (target_only: references/, scripts/, templates/) pada skill yang sudah ada di bank.
3. Penyerapan update/patch (reverse-sync): file yang dimodifikasi di target diserap balik ke bank.
4. Tetap memvalidasi format, anti-tombstone, dan audit rahasia (secret-scan).

Ledger: skills/.promotion-ledger.json
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

BANK = pathlib.Path(os.environ.get("NIU_BANK", "/Users/zaryu/Desktop/Niumination/skills"))
TARGET = pathlib.Path(os.environ.get("NIU_TARGET", pathlib.Path.home() / ".hermes" / "skills"))
LEDGER = BANK / ".promotion-ledger.json"
SKIP_FILES = {".DS_Store"}
SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".pytest_cache"}
PLACEHOLDER_MARKS = ("...", "<", ">", "{{", "${", "xxxx", "XXXX", "REDACTED", "PLACEHOLDER", "YOUR_", "EXAMPLE", "abc", "***")

SECRET_PATTERNS = [
    (r"\bsk-[A-Za-z0-9_\-]{16,}", "openai-style key"),
    (r"\bghp_[A-Za-z0-9]{20,}", "github token"),
    (r"\bgithub_pat_[A-Za-z0-9_]{20,}", "github pat"),
    (r"\bAIza[0-9A-Za-z_\-]{20,}", "google api key"),
    (r"\beyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}", "jwt"),
    (r"postgres(?:ql)?://[^\s\"']+:[^\s\"']+@", "db url with password"),
    (r"\bxox[baprs]-[A-Za-z0-9\-]{10,}", "slack token"),
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


def file_secret_hit(f: pathlib.Path) -> str | None:
    try:
        text = f.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    for pat, label in SECRET_PATTERNS:
        for m in re.finditer(pat, text):
            tok = m.group(0)
            if any(mark in tok for mark in PLACEHOLDER_MARKS):
                continue
            return label
    return None


def secret_hit(skill_dir: pathlib.Path) -> str | None:
    for f in sorted(skill_dir.rglob("*")):
        if not f.is_file() or f.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        hit = file_secret_hit(f)
        if hit:
            return f"{hit} di {f.relative_to(skill_dir)}"
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


def bank_skills_map() -> dict[str, pathlib.Path]:
    """Kembalikan map {nama_skill: path_folder_di_bank}"""
    out = {}
    for md in BANK.rglob("SKILL.md"):
        parts = md.relative_to(BANK).parts
        if any(x.startswith(".") for x in parts):
            continue
        out[md.parent.name] = md.parent
        fm = frontmatter(md)
        if fm:
            out[fm[0]] = md.parent
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

    bank_map = bank_skills_map()
    bundled = bundled_names()
    hub = hub_names()
    tombstones = set(ledger["tombstones"])
    now = datetime.now(timezone.utc).isoformat()

    promoted_skills = []
    promoted_files = []
    updated_files = []
    ignored = []
    rejected = []

    # 1. SCAN TARGET SKILLS (Skill baru atau pembaruan skill yang ada)
    for name, sdir in target_skills().items():
        if name in tombstones:
            ignored.append((name, "tombstone"))
            continue
        if name in bundled and name not in bank_map:
            ignored.append((name, "bundled"))
            continue
        if name in hub and name not in bank_map:
            ignored.append((name, "hub"))
            continue

        # Kasus A: Skill SUDAH ADA di bank -> Periksa berkas tambahan atau modifikasi
        if name in bank_map:
            bdir = bank_map[name]
            for tf in sorted(sdir.rglob("*")):
                if not tf.is_file() or tf.name in SKIP_FILES:
                    continue
                if any(part in SKIP_DIRS for part in tf.parts):
                    continue
                frel = tf.relative_to(sdir)
                bf = bdir / frel

                hit = file_secret_hit(tf)
                if hit:
                    rejected.append((f"{name}/{frel}", f"pola kredensial: {hit}"))
                    continue

                if not bf.exists():
                    # Berkas baru di skill yang sudah ada (target_only)
                    if not a.dry_run:
                        bf.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(tf, bf)
                    promoted_files.append((name, str(frel)))
                else:
                    # Berkas ada di kedua sisi -> cek apakah berbeda
                    th = sha(tf)
                    bh = sha(bf)
                    if th != bh:
                        # Target berbeda dari bank -> reverse-sync (target lebih kaya/baru)
                        if not a.dry_run:
                            shutil.copy2(tf, bf)
                        updated_files.append((name, str(frel), f"{bf.stat().st_size}B → {tf.stat().st_size}B"))
            continue

        # Kasus B: Skill BARU (belum ada di bank)
        fm = frontmatter(sdir / "SKILL.md")
        if not fm:
            rejected.append((name, "frontmatter tidak valid (name/description)"))
            continue
        hit = secret_hit(sdir)
        if hit:
            rejected.append((name, f"pola kredensial: {hit}"))
            continue

        rel = sdir.relative_to(TARGET)
        domain = rel.parts[0] if len(rel.parts) > 1 else "ecosystem"
        key = f"{domain}/{name}"
        dest = BANK / domain / name
        if dest.exists():
            rejected.append((name, f"tujuan sudah ada: {dest.relative_to(BANK)}"))
            continue

        if a.dry_run:
            promoted_skills.append((name, key, "DRY-RUN"))
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
        promoted_skills.append((name, key, f"{len(files)} berkas"))

    for name, why in ignored:
        ledger["ignored"][name] = {"reason": why, "checkedAt": now}
    for name, why in rejected:
        ledger["ignored"][name] = {"reason": f"rejected: {why}", "checkedAt": now}

    if not a.dry_run and (promoted_skills or promoted_files or updated_files):
        ledger["updatedAt"] = now
        LEDGER.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n")

    if a.json:
        print(json.dumps({
            "promoted_skills": promoted_skills,
            "promoted_files": promoted_files,
            "updated_files": updated_files,
            "ignored": ignored,
            "rejected": rejected,
            "dry_run": a.dry_run
        }, indent=2))
        return 0

    mode = "DRY-RUN" if a.dry_run else "konvergen"
    print(f"[promosi] {mode}: {len(promoted_skills)} skill baru · {len(promoted_files)} berkas baru · {len(updated_files)} update diserap · {len(rejected)} ditolak")
    for n, d, extra in promoted_skills:
        print(f"  + skill baru: {n} → {d} ({extra})")
    for n, f in promoted_files:
        print(f"  + berkas baru: {n} :: {f}")
    for n, f, sz in updated_files:
        print(f"  ↺ update diserap: {n} :: {f} ({sz})")
    for n, why in rejected:
        print(f"  ! ditolak {n}: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

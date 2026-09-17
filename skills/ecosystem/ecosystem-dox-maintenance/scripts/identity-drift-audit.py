#!/usr/bin/env python3
"""One-pass identity/config drift audit: symlinks, tracked status, hash uniformity, stale paths.

Usage:
    python3 identity-drift-audit.py [--eco ~/Desktop/Niumination] [--home ~/.hermes]
                                    [--name SOUL.md] [--name AGENTS.md] [--stale docs/reference/]

Checks:
  1. Hermes home: every symlink - its target and whether the target exists
  2. Each requested identity/config filename under the ecosystem: tracked status via the nearest
     enclosing repo (catches orphans living inside a gitignored folder such as dotfiles/)
  3. Hash uniformity across every copy of that filename plus the active symlink
  4. Residue of a retired path string in live config/scripts (web cache and archives ignored)

Read-only. Exit 1 when it finds an orphan, a hash drift, or stale-path residue.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

MAX_BYTES = 2_000_000
SCAN_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".sh", ".py", ".txt", ""}
SKIP_PARTS = ("/node_modules/", "/.git/", "/cache/", "/archive/", "/.venv/")


def sha(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except OSError:
        return "ERR"


def nearest_repo(path: Path) -> Path | None:
    cur = path.parent if path.is_file() else path
    while cur != cur.parent:
        if (cur / ".git").exists():
            return cur
        cur = cur.parent
    return None


def tracked_by(path: Path) -> tuple[Path | None, bool]:
    repo = nearest_repo(path)
    if not repo:
        return None, False
    try:
        rel = path.relative_to(repo)
    except ValueError:
        return repo, False
    res = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--error-unmatch", str(rel)],
        capture_output=True, text=True,
    )
    return repo, res.returncode == 0


def main() -> int:
    argv = sys.argv[1:]

    def opt(flag: str, default: str) -> str:
        return argv[argv.index(flag) + 1] if flag in argv else default

    eco = Path(os.path.expanduser(opt("--eco", "~/Desktop/Niumination")))
    home = Path(os.path.expanduser(opt("--home", "~/.hermes")))
    names = [argv[i + 1] for i, a in enumerate(argv) if a == "--name"] or ["SOUL.md"]
    stale = opt("--stale", "")
    problems = 0

    print("1) Hermes home: symlinks & targets")
    for item in sorted(home.iterdir()):
        if item.is_symlink():
            target = os.readlink(item)
            ok = Path(target).exists()
            problems += 0 if ok else 1
            print(f"   symlink {item.name:22} -> {target} [{'OK' if ok else 'TARGET MISSING'}]")

    for name in names:
        print(f"\n2) {name} across the ecosystem: tracked or orphan?")
        copies = [p for p in sorted(eco.rglob(name))
                  if not any(part in str(p) for part in SKIP_PARTS)]
        for path in copies:
            repo, tracked = tracked_by(path)
            problems += 0 if tracked else 1
            print(f"   {'TRACKED' if tracked else 'ORPHAN (untracked)'}  sha {sha(path)}  {path}"
                  f"  repo: {repo.name if repo else '(no repo)'}")

        print(f"\n3) {name}: hash uniformity (canonical vs snapshots vs active)")
        active = home / name
        group = copies + ([active] if active.exists() else [])
        hashes = {str(p): sha(p) for p in group}
        for value, path in hashes.items():
            print(f"   {value}  {path}")
        distinct = set(hashes.values())
        if len(distinct) > 1:
            problems += 1
            print(f"   => DRIFT: {len(distinct)} different versions")
        elif group:
            print("   => SERAGAM (identical)")

    if stale:
        print(f"\n4) Residue of retired path '{stale}' in live config/scripts")
        roots = [home, eco / "scripts", eco / "skills"]
        hits = 0
        for root in roots:
            files = [root] if root.is_file() else [f for f in root.rglob("*") if f.is_file()]
            for path in files:
                if path.suffix not in SCAN_SUFFIXES or any(p in str(path) for p in SKIP_PARTS):
                    continue
                try:
                    if path.stat().st_size > MAX_BYTES:
                        continue
                    text = path.read_text(errors="ignore")
                except OSError:
                    continue
                for lineno, line in enumerate(text.splitlines(), 1):
                    if stale in line:
                        print(f"   {path}:{lineno}")
                        hits += 1
        problems += hits
        print(f"   => {hits} hit(s)" + (" (clean)" if hits == 0 else ""))

    print(f"\n=== {problems} problem(s) found ===")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

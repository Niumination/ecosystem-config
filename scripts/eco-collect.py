#!/usr/bin/env python3
"""
eco-collect.py — Ecosystem Manifest Collector v2
Auto-discover git repos + non-git dirs, detect changes.
Part of ecosystem-auto-sync pipeline (cron every 15m + launchd RunAtLoad).

Usage:
  python3 eco-collect.py           # normal: compare + output
  python3 eco-collect.py --force   # force output full manifest
  python3 eco-collect.py --save    # save state only (launchd), no stdout

Output:
  - "NO_CHANGES" or manifest with diff summary → stdout
  - Writes state to brain/logs/eco-manifest.json
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

NIUMINATION = Path("/Users/zaryu/Desktop/Niumination")
STATE_FILE = NIUMINATION / "brain" / "logs" / "eco-manifest.json"
LOCK_FILE = Path("/tmp/eco-collect.lock")
TIMEOUT = 10  # seconds per git command

# Non-git dirs to track (relative to NIUMINATION)
NON_GIT_DIRS = [
    "PI",
    "archive",
    "labs",
    "dotfiles",
    "Belum disentuh",
    "Production",
    "scripts",
    "projects/aistudio-google",
    "projects/arena.ai",
]


def run_git(cwd, args):
    """Run git command safely, return stdout or None."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def scan_git_repo(path):
    """Scan a single git repository."""
    git_dir = path / ".git"
    if not git_dir.exists():
        return None

    rel = path.relative_to(NIUMINATION)

    # Get current branch
    branch = run_git(path, ["rev-parse", "--abbrev-ref", "HEAD"])
    # Get HEAD commit
    head = run_git(path, ["rev-parse", "--short", "HEAD"])
    # Check for dirty
    dirty_output = run_git(path, ["status", "--porcelain"])
    dirty = bool(dirty_output and dirty_output.strip())
    # Check remote
    remote_url = run_git(path, ["remote", "get-url", "origin"])
    has_remote = remote_url is not None
    # Last commit date
    last_commit = run_git(
        path, ["log", "-1", "--format=%ci", "--date=short"]
    )
    # Get version tag
    version = run_git(path, ["describe", "--tags", "--abbrev=0"])

    return {
        "name": path.name,
        "path": str(rel),
        "head": head or None,
        "branch": branch or None,
        "dirty": dirty,
        "remote": has_remote,
        "remote_url": remote_url,
        "version": version or None,
        "last_commit": last_commit or None,
    }


def auto_discover_git_repos():
    """Auto-discover all git repos under Niumination root."""
    repos = []
    # Scan root-level dirs (brain/, etc.) + projects/ subdirs
    scan_dirs = [d for d in NIUMINATION.iterdir() if d.is_dir() and not d.name.startswith(".")]
    scan_dirs += sorted(NIUMINATION.glob("projects/*"))
    scan_dirs += sorted(NIUMINATION.glob("Production/*"))
    seen = set()
    for d in scan_dirs:
        if d in seen:
            continue
        seen.add(d)
        if d.is_dir() and (d / ".git").exists():
            info = scan_git_repo(d)
            if info:
                repos.append(info)
    return repos


def count_files(path):
    """Count files in a directory (shallow)."""
    try:
        return sum(1 for _ in path.rglob("*") if _.is_file())
    except (OSError, PermissionError):
        return 0


def scan_non_git(path, rel_path):
    """Scan a non-git directory."""
    if not path.exists() or not path.is_dir():
        return None
    return {
        "name": path.name,
        "path": str(rel_path) if rel_path != Path(".") else path.name,
        "file_count": count_files(path),
    }


def build_manifest():
    """Build current ecosystem manifest."""
    git_repos = auto_discover_git_repos()
    non_git = []
    for rel in NON_GIT_DIRS:
        p = NIUMINATION / rel
        if p.exists() and p.is_dir():
            info = scan_non_git(p, Path(rel))
            if info:
                non_git.append(info)

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "git_repos": git_repos,
        "non_git": non_git,
        "total_git": len(git_repos),
        "total_non_git": len(non_git),
        "total_items": len(git_repos) + len(non_git),
    }


def format_diff(old, new):
    """Compare old vs new manifest, return human-readable diff."""
    lines = []

    old_git = {r["path"]: r for r in old.get("git_repos", [])}
    new_git = {r["path"]: r for r in new.get("git_repos", [])}
    old_ng = {r["path"]: r for r in old.get("non_git", [])}
    new_ng = {r["path"]: r for r in new.get("non_git", [])}

    added = []
    removed = []
    changed = []

    # Detect added/removed/changed git repos
    for path, repo in new_git.items():
        if path not in old_git:
            added.append(f"  + Added repo: {path} ({repo['name']}, git)")
        elif old_git[path] != repo:
            o = old_git[path]
            if o["dirty"] != repo["dirty"]:
                changed.append(f"  ~ {path}: dirty {o['dirty']}→{repo['dirty']}")
            if o["branch"] != repo["branch"]:
                changed.append(f"  ~ {path}: branch {o['branch']}→{repo['branch']}")
            if o["head"] != repo["head"]:
                changed.append(
                    f"  ~ {path}: HEAD {o['head'][:8] or '?'}→{repo['head'][:8] or '?'}"
                )

    for path in old_git:
        if path not in new_git:
            removed.append(f"  - Missing repo: {path}")

    # Non-git changes
    for path, d in new_ng.items():
        if path not in old_ng:
            added.append(f"  + New dir: {path}")
        elif old_ng[path].get("file_count") != d.get("file_count"):
            changed.append(
                f"  ~ {path}: {old_ng[path]['file_count']}→{d['file_count']} files"
            )

    for path in old_ng:
        if path not in new_ng:
            removed.append(f"  - Missing dir: {path}")

    if not added and not removed and not changed:
        return None

    lines.append(f"CHANGED ITEMS ({len(added) + len(removed) + len(changed)}):")
    lines.extend(added)
    lines.extend(removed)
    lines.extend(changed)
    lines.append(
        f"  ~ Total items: {old.get('total_items', '?')} → {new.get('total_items', '?')}"
    )

    return "\n".join(lines)


def main():
    force = "--force" in sys.argv
    save_only = "--save" in sys.argv

    # Acquire lock
    try:
        lock_fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_RDWR)
    except FileExistsError:
        # Check if lock is stale (>5 min)
        try:
            age = time.time() - os.path.getmtime(LOCK_FILE)
            if age > 300:
                os.unlink(LOCK_FILE)
                lock_fd = os.open(
                    str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_RDWR
                )
            else:
                if not save_only:
                    print("LOCKED", flush=True)
                return
        except OSError:
            return

    try:
        # Build current manifest
        current = build_manifest()

        # Read old manifest
        old = {}
        if STATE_FILE.exists():
            try:
                old = json.loads(STATE_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                old = {}

        # Save current state
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(
            json.dumps(current, indent=2, default=str)
        )

        if save_only:
            return

        if old and not force:
            diff = format_diff(old, current)
            if diff is None:
                print("NO_CHANGES", flush=True)
                return

            # Output manifest + diff for agent
            print("=== Ecosystem Manifest ===", flush=True)
            print(
                f"Timestamp: {current['timestamp']}",
                flush=True,
            )
            print("", flush=True)
            print(diff, flush=True)
            print("", flush=True)
            print("FULL MANIFEST:", flush=True)
            print(
                json.dumps(current, indent=2, default=str),
                flush=True,
            )
        else:
            # Force or first run — output full manifest
            print("=== Ecosystem Manifest ===", flush=True)
            print(
                f"Timestamp: {current['timestamp']}",
                flush=True,
            )
            print("", flush=True)
            print("FULL MANIFEST:", flush=True)
            print(
                json.dumps(current, indent=2, default=str),
                flush=True,
            )

    finally:
        os.close(lock_fd)
        os.unlink(LOCK_FILE)


if __name__ == "__main__":
    main()

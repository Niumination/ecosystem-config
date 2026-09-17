#!/usr/bin/env python3
"""Scan a repo tree for container-relevant signals (containerization readiness audit).

Prints a JSON array (one row per active repo) plus a TOTAL line. Each row: category, project, stack,
existing docker artifacts, deploy target, DB hints, long-running service hints.
Read alongside SKILL.md's verdict table.

Usage: python3 scan_docker_need.py [root]
"""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "~/Desktop/Niumination").expanduser()
SKIP_TOP = {"archive", "node_modules", "brain", "vault", ".git"}
CATEGORIES = ["apps", "services", "sites", "desktop", "agents", "labs", "sandbox", "tools"]

DB_HINTS = {
    "postgresql": "postgres", "psycopg": "postgres", "pg": "postgres",
    "mysql": "mysql", "mariadb": "mysql",
    "redis": "redis", "ioredis": "redis",
    "mongodb": "mongo", "mongoose": "mongo", "pymongo": "mongo",
    "sqlite": "sqlite", "better-sqlite3": "sqlite", "aiosqlite": "sqlite",
    "supabase": "supabase(cloud)", "prisma": "prisma",
    "chromadb": "chroma", "qdrant": "qdrant", "weaviate": "weaviate",
    "elasticsearch": "elastic",
}
SRV_HINTS = ("fastapi", "flask", "uvicorn", "gunicorn", "express", "next", "vite",
             "django", "aiohttp", "websocket", "socket.io", "celery", "playwright",
             "selenium", "puppeteer", "torch", "tensorflow", "ollama", "vllm")


def read(p: Path, limit=200_000) -> str:
    try:
        return p.read_text(errors="replace")[:limit]
    except Exception:
        return ""


def deps_of(d: Path) -> str:
    txt = ""
    for name in ("package.json", "requirements.txt", "pyproject.toml", "Pipfile",
                 "Cargo.toml", "go.mod", "docker-compose.yml", "compose.yaml"):
        f = d / name
        if f.exists():
            txt += read(f, 120_000).lower()
    return txt


def stack_of(d: Path) -> str:
    s = []
    if (d / "package.json").exists():
        s.append("node")
    if any((d / f).exists() for f in ("requirements.txt", "pyproject.toml", "Pipfile")):
        s.append("python")
    if (d / "Cargo.toml").exists():
        s.append("rust")
    if (d / "go.mod").exists():
        s.append("go")
    return ",".join(s) or "?"


def deploy_of(d: Path) -> str:
    out = set()
    if (d / "vercel.json").exists() or any(d.glob("**/vercel.json")):
        out.add("vercel")
    if (d / "netlify.toml").exists():
        out.add("netlify")
    if (d / "fly.toml").exists():
        out.add("fly")
    if (d / "render.yaml").exists():
        out.add("render")
    wf = d / ".github" / "workflows"
    if wf.is_dir():
        for f in wf.glob("*.y*ml"):
            t = read(f, 40_000).lower()
            if "pages" in t:
                out.add("gh-pages")
            if "docker" in t:
                out.add("gh-action-docker")
    # systemd unit / launchd plist / bootstrap script => self-hosted runtime
    for pat in ("deploy/*.service", "**/*.service", "*.plist", "setup_vps.sh", "docker-compose.yml"):
        if list(d.glob(pat)):
            out.add("self-host")
            break
    return ",".join(sorted(out)) or "-"


def docker_artifacts(d: Path) -> str:
    a = []
    if list(d.glob("Dockerfile*")):
        a.append("Dockerfile")
    if list(d.glob("docker-compose*")) or list(d.glob("compose.y*ml")) or list(d.glob("**/docker-compose*")):
        a.append("compose")
    if (d / ".devcontainer").is_dir():
        a.append("devcontainer")
    return ",".join(a) or "-"


def main() -> None:
    rows = []
    for cat in CATEGORIES:
        cdir = ROOT / cat
        if not cdir.is_dir():
            continue
        for d in sorted(cdir.iterdir()):
            if not d.is_dir() or d.name in SKIP_TOP or d.name.startswith("."):
                continue
            if not (d / ".git").exists():
                continue
            deps = deps_of(d)
            rows.append({
                "cat": cat,
                "proj": d.name,
                "stack": stack_of(d),
                "deploy": deploy_of(d),
                "docker": docker_artifacts(d),
                "db": ",".join(sorted({v for k, v in DB_HINTS.items() if k in deps})) or "-",
                "needs_svc": ",".join(sorted({h for h in SRV_HINTS if h in deps})) or "-",
            })
    print(json.dumps(rows, indent=1))
    print("\nTOTAL REPOS: %d" % len(rows))


if __name__ == "__main__":
    main()

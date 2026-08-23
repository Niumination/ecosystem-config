#!/usr/bin/env python3
# generate-ecosystem-json.py — Generate ecosystem-status.json for Niu-Dash
# Cron: (idealnya dipanggil health-checker.sh)
# Output: apps/niu-dash/public/data/ecosystem-status.json
# Data source: BACKLOG.md parsing + kanban.db query

import json
import os
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone, timedelta

WIB = timezone(timedelta(hours=7))
NIUMINATION = "/Users/zaryu/Desktop/Niumination"
BACKLOG = os.path.join(NIUMINATION, "BACKLOG.md")
# DB path: env HERMES_HOME (gateway), fallback lokal, lalu USB. None jika tidak ada.
_db_env = os.environ.get("KANBAN_DB") or os.path.join(
    os.environ.get("HERMES_HOME", "/Users/zaryu/.hermes"), "kanban.db")
DB = _db_env
if not os.path.isfile(DB):
    for _cand in ("/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db",
                  "/Users/zaryu/Desktop/Niumination/data/kanban.db"):
        if os.path.isfile(_cand):
            DB = _cand
            break
    else:
        DB = None  # kanban.db unavailable → BACKLOG-only mode
OUTPUT = os.path.join(NIUMINATION, "apps/niu-dash/public/data/ecosystem-status.json")

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

# Parse task counts from BACKLOG
with open(BACKLOG) as f:
    content = f.read()

tasks = re.findall(r'^- \[(.)\]', content, re.MULTILINE)
total = len(tasks)
done = sum(1 for t in tasks if t == 'x')

# Count P1/P2/P3 by matching lines with P-level tags
p1 = len(re.findall(r'^- \[.\] .*P1', content, re.MULTILINE))
p2 = len(re.findall(r'^- \[.\] .*P2', content, re.MULTILINE))
p3 = len(re.findall(r'^- \[.\] .*P3', content, re.MULTILINE))

# Parse kanban counts from DB
kanban = {"active": 0, "todo": 0, "done": 0, "archived": 0}
if DB is not None:
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        for status in ["in_progress", "todo", "done", "cancelled"]:
            cur.execute("SELECT COUNT(*) FROM tasks WHERE status=?", (status,))
            count = cur.fetchone()[0] or 0
            if status == "in_progress":
                kanban["active"] = count
            elif status == "cancelled":
                kanban["archived"] = count
            else:
                kanban[status] = count
        conn.close()
    except Exception:
        pass

# Generate timestamp
timestamp = datetime.now(WIB).strftime("%Y-%m-%dT%H:%M:%S+07:00")

# Build JSON
data = {
    "version": 2,
    "generated_at": timestamp,
    "total_tasks": total,
    "kanban": kanban,
    "backlog": {
        "total": total,
        "p1": p1,
        "p2": p2,
        "p3": p3,
    },
    "projects": [
        {
            "name": "TEDEO",
            "tier": 1,
            "status": "in_progress",
            "priority": "P1",
            "git": "Niumination/TEDEO",
            "dox": True,
            "desc": "Delivery Service — T1-T4 critical bugs fixed, butuh deploy test",
        },
        {
            "name": "kune-ya.com",
            "tier": 1,
            "status": "in_progress",
            "priority": "P1",
            "git": "Niumination/kune-ya.com",
            "dox": True,
            "desc": "AI Chat RAG — analytics & rate limiting",
        },
        {
            "name": "PemdiAcehTengah",
            "tier": 1,
            "status": "in_progress",
            "priority": "P1",
            "git": "Niumination/PemdiAcehTengah",
            "dox": True,
            "desc": "Portal Pemda Aceh Tengah — 52 OPD, 70 pages",
        },
        {
            "name": "niu-vermilion",
            "tier": 1,
            "status": "in_progress",
            "priority": "P1",
            "git": "Niumination/Niu-Vermilion",
            "dox": True,
            "desc": "Second Brain — V1-V5 auth fixed",
        },
        {
            "name": "Niu-Flow",
            "tier": 1,
            "status": "in_progress",
            "priority": "P2",
            "git": "Niumination/Niu-Flow",
            "dox": True,
            "desc": "JCode bridge — pipeline paralel, 5 commits",
        },
        {
            "name": "niu-dash",
            "tier": 1,
            "status": "in_progress",
            "priority": "P2",
            "git": "Niumination/niu-dash",
            "dox": True,
            "deployUrl": "https://niumination.github.io/niu-dash",
            "desc": "Ecosystem dashboard — v2.16.8, 27/27 audit ✅",
        },
        {
            "name": "Niu-LKH",
            "tier": 1,
            "status": "done",
            "priority": "P2",
            "git": "Niumination/Niu-LKH",
            "dox": True,
            "deployUrl": "https://niumination.github.io/Niu-LKH",
            "desc": "Laporan Kegiatan Harian — v3.1.1 ✅ 100%",
        },
        {
            "name": "Flame-ADE",
            "tier": 1,
            "status": "in_progress",
            "priority": "P2",
            "git": "Niumination/Flame-ADE",
            "dox": True,
            "desc": "Tauri/Rust v1.3.0 — AI-native terminal",
        },
        {
            "name": "niu-cast",
            "tier": 1,
            "status": "in_progress",
            "priority": "P2",
            "git": "Niumination/niu-cast",
            "dox": True,
            "desc": "Android ADB Tool & Screen Mirror v1.1.1",
        },
        {
            "name": "brain",
            "tier": 1,
            "status": "in_progress",
            "priority": "P2",
            "git": "Niumination/brain",
            "dox": True,
            "desc": "Obsidian Vault — 14 inbox daily",
        },
        {
            "name": "niumination-workspace",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/niumination-workspace",
            "dox": True,
            "desc": "Next.js 16 workspace — 4 commits pushed, 110 proyek sync",
        },
        {
            "name": "niu-kanban-dash",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/niu-kanban-dash",
            "dox": False,
            "desc": "Vite/React kanban dashboard — pushed to GitHub",
        },
        {
            "name": "orchestrator",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/orchestrator",
            "dox": False,
            "desc": "Python multi-agent — pushed to GitHub",
        },
        {
            "name": "Ultra",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/ultra-automation",
            "dox": True,
            "desc": "Puppeteer browser automation — pushed to GitHub",
        },
        {
            "name": "x-downloader",
            "tier": 1,
            "status": "in_progress",
            "priority": "P1",
            "git": "Niumination/x-downloader",
            "dox": True,
            "desc": "v2.0 FastAPI+Next.js 16+Three.js+Tauri 2 — published to GitHub",
        },
        {
            "name": "mac-web-dashboard",
            "tier": 1,
            "status": "in_progress",
            "priority": "P2",
            "git": "Niumination/mac-web-dashboard",
            "dox": False,
            "desc": "macOS Dashboard v1.0.0 — under development, 10 dirty",
        },
        {
            "name": "JHermUSB-portable",
            "tier": 1,
            "status": "done",
            "priority": "P2",
            "git": "Niumination/JHermUSB-portable",
            "dox": False,
            "desc": "Hermes Agent portable — 652K",
        },
        {
            "name": "ai-first-os",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/AI-First-OS",
            "dox": False,
            "desc": "Arch Linux ISO builder — v1.0.0",
        },
        {
            "name": "arch-web-dashboard",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/arch-web-dashboard",
            "dox": False,
            "desc": "Arch Linux Dashboard v1.0.0",
        },
        {
            "name": "ai-file-manager-android",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/ai-file-organizer-android",
            "dox": False,
            "desc": "Android Kotlin — AI File Organizer, Gemini OCR",
        },
        {
            "name": "TEDEO-Kanban",
            "tier": 2,
            "status": "done",
            "priority": "P2",
            "git": "Niumination/TEDEO-Kanban",
            "dox": False,
            "desc": "Kanban board untuk TEDEO — pushed to GitHub",
        },
        {
            "name": "AuditTI-AT",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/AuditTI-AT",
            "dox": False,
            "deployUrl": "https://niumination.github.io/AuditTI-AT",
            "desc": "Audit TI Aceh Tengah — GH Pages live",
        },
        {
            "name": "niuterm",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/niu-term",
            "dox": True,
            "desc": "Tauri terminal tool",
        },
        {
            "name": "terax-ai",
            "tier": 2,
            "status": "done",
            "priority": "P3",
            "git": "Niumination/terax-ai",
            "dox": True,
            "desc": "Lightweight ADE fork (TS)",
        },
    ],
}

with open(OUTPUT, "w") as f:
    json.dump(data, f, indent=2)

path = os.path.relpath(OUTPUT, NIUMINATION)
print(f"✅ Generated ecosystem-status.json ({os.path.getsize(OUTPUT)} bytes)")
print(f"   {path}")

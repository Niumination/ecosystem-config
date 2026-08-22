#!/usr/bin/env bash
# =============================================================================
# trio-watch.sh — Read-only Trio Awareness (Hermes · JCode · OpenCode)
# =============================================================================
# Pemanggil: up-eco.sh --from <hermes|jcode|opencode>
# Tujuan : Memberi tahu 2 tool lain tanpa kontrol/span/delegasi apa pun.
# Output : core/runtime/trio-status.json  (overwrite tiap run, shared memory)
# Batasan: READ-ONLY. Tidak mutate core, tidak spawn sub-agent, tidak ganti model.
# =============================================================================

set -euo pipefail
NIUMINATION="/Users/zaryu/Desktop/Niumination"
HERMES_HOME="${HOME}/.hermes"
STATUS_FILE="$NIUMINATION/core/runtime/trio-status.json"

# ── Parse --from arg ──
FROM=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from) FROM="$2"; shift 2;;
    --from=*) FROM="${1#*=}"; shift;;
    *) break;;
  esac
done
FROM="${FROM:-hermes}"

NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ── helpers ──────────────────────────────────────────────────────────────────
section() { printf "\n\033[1;36m◆ %s\033[0m\n" "$1"; }
pass()    { printf "  \033[32m✅ %s\033[0m\n" "$1"; }
warn()    { printf "  \033[33m⚠️  %s\033[0m\n" "$1"; }
info()    { printf "  \033[36mℹ️  %s\033[0m\n" "$1"; }

# ── Build status JSON via python3 (read-only filesystem access only) ─────────
python3 - "$FROM" "$NIUMINATION" "$HERMES_HOME" "$STATUS_FILE" "$NOW" <<'PYEOF'
import json, os, sys, glob, subprocess, re

caller, nium, hermes_home, status_file, now = sys.argv[1:6]
tools = {}

# ── Hermes ───────────────────────────────────────────────────────────────────
def hermes_status():
    s = {"sessions": 0, "last_session": "", "model": "", "git_dirty": []}
    sess_dir = os.path.join(hermes_home, "sessions")
    if os.path.isdir(sess_dir):
        files = sorted(glob.glob(f"{sess_dir}/*.json"))
        s["sessions"] = len(files)
        if files:
            s["last_session"] = os.path.basename(files[-1])
    # model terakhir
    model_file = os.path.join(hermes_home, "session-models.json")
    if os.path.exists(model_file):
        try:
            import json as _j
            mm = _j.load(open(model_file))
            if mm:
                last_key = sorted(mm.keys())[-1]
                s["model"] = mm[last_key]
        except Exception:
            pass
    # git dirty di ekosistem root
    try:
        out = subprocess.run(["git", "-C", nium, "status", "--porcelain"],
                             capture_output=True, text=True, timeout=10).stdout
        if out.strip():
            s["git_dirty"] = [l for l in out.strip().splitlines()[:5]]
    except Exception:
        pass
    return s

# ── JCode ────────────────────────────────────────────────────────────────────
def jcode_status():
    s = {"sessions": 0, "active_sessions": 0, "total_sessions": 0,
         "last_session": "", "pid": "", "git_dirty": []}
    cache = os.path.expandvars("$HOME/.jcode/cache/session-picker-list-v2.json")
    sessions_dir = os.path.expandvars("$HOME/.jcode/sessions")
    goals_dir = os.path.expandvars("$HOME/.jcode/goals")
    import subprocess as _sp
    import time as _time
    import glob as _glob

    # proses hidup? (server daemon = PID hidup = JCode siap pakai)
    pgrep = _sp.run(["pgrep", "-x", "jcode"], capture_output=True, text=True)
    pids = [p for p in pgrep.stdout.strip().split("\n") if p]
    s["pid"] = pids[0] if pids else ""
    jcode_running = bool(pids)  # proses hidup = aktif

    # ── aktivitas: pgrep hidup = aktif, scan session terbaru untuk ringkasan ──
    active_sessions = 0
    last_session_name = ""
    live_summaries = []  # ringkasan aktivitas tiap session live
    if jcode_running:
        active_sessions = 1  # pgrep hidup = JCode siap pakai
    if os.path.isdir(sessions_dir):
        try:
            json_files = [f for f in _glob.glob(f"{sessions_dir}/*.json") if os.path.isfile(f)]
            json_files.sort(key=os.path.getmtime)
            # ambil 3 file terbaru untuk ringkasan (live atau stale, asal ada)
            for jf in reversed(json_files[-3:]):
                try:
                    d2 = json.load(open(jf))
                    sn = d2.get("short_name") or d2.get("title", "")[:50]
                    wdir = d2.get("working_dir", "")
                    # 🎯 PRIMARY: compaction.summary_text
                    summary = ""
                    comp = d2.get("compaction", {})
                    if isinstance(comp, dict):
                        raw_summary = comp.get("summary_text", "")
                        if raw_summary:
                            summary = raw_summary.replace("**Context:** ", "").strip()[:120]
                    # fallback: scan sampai ketemu user prompt asli
                    if not summary and d2.get("messages"):
                        for idx in range(min(5, len(d2["messages"]))):
                            mb = d2["messages"][idx]
                            if not isinstance(mb, dict): continue
                            if mb.get("role") != "user": continue
                            content = mb.get("content", "")
                            if isinstance(content, list):
                                for item in content:
                                    if isinstance(item, dict) and item.get("type") == "text":
                                        txt = item.get("text", "")
                                        if txt and "system-reminder" not in txt:
                                            summary = txt[:120]; break
                                    elif isinstance(item, str) and item != "system-reminder":
                                        summary = item[:120]; break
                            elif isinstance(content, str) and "system-reminder" not in content:
                                summary = content[:120]
                            if summary: break
                    # tambah project/repo jika ada di working_dir
                    extra = ""
                    if wdir and "services/" in wdir:
                        import re as _re
                        m = _re.search(r"services/([a-zA-Z0-9_-]+)", wdir)
                        if m: extra = f"[{m.group(1)}]"
                    if not summary and sn: summary = sn
                    summary = f"{extra} {summary}".strip()[:90] if extra else summary[:90]
                    live_summaries.append({"session": sn, "summary": summary})
                    if not last_session_name:
                        last_session_name = sn
                except Exception:
                    pass
        except Exception:
            pass
    s["live_summaries"] = live_summaries

    # ── total session dari cache ──
    total_sessions = 0
    if os.path.exists(cache):
        try:
            d = json.load(open(cache))
            ext = d.get("external_sessions", [])
            sg = d.get("server_groups", [])
            orphans = d.get("orphan_sessions", [])
            if not isinstance(ext, list): ext = []
            if not isinstance(sg, list): sg = []
            if not isinstance(orphans, list): orphans = []
            total_sessions = len(orphans + ext + [ss for grp in sg for ss in grp.get("sessions", [])])
        except Exception:
            pass

    # ── goals count ──
    s["goals_count"] = 0
    if os.path.isdir(goals_dir):
        try:
            s["goals_count"] = len(os.listdir(goals_dir))
        except Exception:
            pass

    s["active_sessions"] = active_sessions
    s["total_sessions"] = total_sessions
    s["sessions"] = active_sessions
    s["last_session"] = last_session_name or "idle"
    s["generated_at"] = str(_time.strftime("%Y-%m-%dT%H:%M:%SZ", _time.gmtime(os.path.getmtime(cache)))) if os.path.exists(cache) else ""
    # git dirty
    try:
        out = subprocess.run(["git", "-C", nium, "status", "--porcelain"],
                             capture_output=True, text=True, timeout=10).stdout
        if out.strip():
            s["git_dirty"] = [l for l in out.strip().splitlines()[:5]]
    except Exception:
        pass
    return s


# ── OpenCode ─────────────────────────────────────────────────────────────────
def opencode_status():
    s = {"sessions": 0, "active_sessions": 0, "last_session": "", "git_dirty": []}
    sessions_total = 0
    sessions = []
    # cek proses hidup via pgrep (reliable untuk active count)
    import subprocess as _sp
    pgrep = _sp.run(["pgrep", "-x", "opencode"], capture_output=True, text=True)
    opencode_running = bool(pgrep.stdout.strip())
    # OPTIMASI: kalau opencode tidak jalan, skip `opencode session list` (hemat ~14s)
    sessions_total = 0
    sessions = []
    prev_status = os.path.exists(status_file) and json.load(open(status_file)).get("tools",{}).get("opencode",{})
    if not opencode_running:
        s["sessions"] = 0
        s["active_sessions"] = 0
        s["last_session"] = "idle"
        # ambil total dari cache trio-status.json sebelumnya (jika ada)
        if prev_status:
            sessions_total = prev_status.get("total_sessions", 0)
        s["sessions"] = sessions_total
    else:
        # ambil daftar total + last via opencode session list
        try:
            out = subprocess.run(["opencode", "session", "list"],
                                 capture_output=True, text=True, timeout=25).stdout
            lines = out.strip().splitlines()[2:]  # skip header 2 lines
            for ln in lines:
                parts = ln.split(None, 2)
                if len(parts) >= 3:
                    sessions.append({"id": parts[0], "title": parts[1], "updated": parts[2]})
            sessions_total = len(sessions)
            s["last_session"] = sessions[-1].get("title", "") if sessions else ""
        except Exception as e:
            s["error"] = str(e)
    # active = proses hidup
    s["sessions"] = sessions_total
    s["active_sessions"] = 1 if opencode_running and sessions_total > 0 else 0
    # git dirty
    try:
        out = subprocess.run(["git", "-C", nium, "status", "--porcelain"],
                             capture_output=True, text=True, timeout=10).stdout
        if out.strip():
            s["git_dirty"] = [l for l in out.strip().splitlines()[:5]]
    except Exception:
        pass
    return s

tools["hermes"]   = hermes_status()
tools["jcode"]    = jcode_status()
tools["opencode"] = opencode_status()

# ── Detector konflik (tanpa window) ─────────────────────────────────────────
conflicts = []
gaps = []

# cari repo/project name yang muncul di >1 tool via git log author atau session title
repo_pattern = re.compile(r"^(?:commit|repo):\s*(.+)", re.I)

# scan git log terbaru per tool (simple: cek author)
def recent_tool_activity(repo):
    """Return set of tools active in repo via git log authors in last 10 commits"""
    found = set()
    try:
        log = subprocess.run(
            ["git", "-C", repo, "log", "-15", "--pretty=format:%an|%ae|%s"],
            capture_output=True, text=True, timeout=10).stdout
        for ln in log.splitlines():
            parts = ln.split("|")
            if len(parts) >= 2:
                author = parts[0].lower()
                email = parts[1].lower()
                if "jcode" in author or "jcode" in email:
                    found.add("jcode")
                if "opencode" in author or "open" in email:
                    found.add("opencode")
                if "hermes" in author or "hermes" in email:
                    found.add("hermes")
    except Exception:
        pass
    return found

# Check conflict: 2+ tools active in same repo
for repo in [nium,
             f"{nium}/services/cc-aceh-tengah",
             f"{nium}/services/niu-mission-control"]:
    if os.path.isdir(repo) and os.path.isdir(f"{repo}/.git"):
        active = recent_tool_activity(repo)
        if len(active) >= 2:
            conflicts.append({
                "type": "overlap",
                "repo": repo.replace(nium, ""),
                "tools": sorted(active),
                "desc": f"⚠️ {', '.join(sorted(active))} pernah aktif di repo yang sama"
            })

# Gap: commit terbaru ada tapi belum di BACKLOG
backlog_path = f"{nium}/BACKLOG.md"
for repo in [nium, f"{nium}/services/cc-aceh-tengah"]:
    if not os.path.isdir(repo):
        continue
    try:
        last_commit = subprocess.run(
            ["git", "-C", repo, "log", "-1", "--pretty=format:%h %s"],
            capture_output=True, text=True, timeout=10).stdout.strip()
        if last_commit and os.path.exists(backlog_path):
            h = last_commit.split()[0]
            if h not in open(backlog_path).read():
                rel = repo.replace(f"{nium}/", "")
                gaps.append({
                    "type": "undocumented",
                    "repo": rel,
                    "commit": last_commit[:60],
                    "desc": f"ℹ️ commit terbaru {h} di {rel} belum tercatat di BACKLOG.md"
                })
    except Exception:
        pass

result = {
    "updated_at": now,
    "called_from": caller,
    "tools": tools,
    "conflicts": conflicts,
    "gaps": gaps,
    "note": "Read-only watcher. Hermes hanya pantau, tidak kontrol."
}

with open(status_file, "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# ── Print summary ───────────────────────────────────────────────────────────
print(f"\n🔗 TRIO AWARENESS (called_from: {caller})")
for name, data in tools.items():
    if name == caller:
        prefix = "  YOU"
    elif name == "hermes":
        prefix = "  🤖 Hermes"
    elif name == "jcode":
        prefix = "  🟢 JCode"
    else:
        prefix = "  🟣 OpenCode"
    sess = data.get("sessions", 0)
    active = data.get("active_sessions", sess)
    total = data.get("total_sessions", sess)
    last = data.get("last_session", "") or "-"
    model = f" | model: {data.get('model','')}" if data.get("model") else ""
    # tampilkan "X aktif (Y total)" bila ada active_sessions terpisah
    if "active_sessions" in data and total != active:
        sess_str = f"{active} aktif ({total} total)"
    else:
        sess_str = f"{sess} sessions"
    # untuk open-code jika tidak aktif → pesan idle
    if name == "opencode" and active == 0:
        sess_str = "tidak aktif (idle)"
    print(f"{prefix}: {sess_str} | last: {last[:40]}{model}")
    # ringkasan live sessions (jika ada)
    live_summaries = data.get("live_summaries", [])
    for ls in live_summaries:
        smry = ls.get("summary", "")
        if smry:
            print(f"     ↳ sedang: {smry}  (session: {ls.get('session','')})")

if conflicts:
    print(f"\n  ⚠️  {len(conflicts)} conflict(s) terdeteksi:")
    for c in conflicts:
        print(f"     → {c['desc']}")
else:
    print(f"\n  ✅ Tidak ada overlap aktivitas antar-tool")

if gaps:
    print(f"\n  ℹ️  {len(gaps)} gap dokumentasi:")
    for g in gaps:
        print(f"     → {g['desc']}")

print(f"\n  💾 Status disimpan: {status_file}")
PYEOF

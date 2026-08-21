#!/usr/bin/env python3
import sqlite3, os, re, sys
from pathlib import Path
from datetime import datetime

try:
    import yaml
except Exception:
    yaml = None

import os as _os
# Prefer env HERMES_HOME (set by gateway/Hermes), fallback to local ~/.hermes,
# then USB mount. Hardcoding USB broke status when USB not mounted.
HERMES_HOME = _os.environ.get("HERMES_HOME") or _os.path.expanduser("~/.hermes")
if not _os.path.exists(f"{HERMES_HOME}/state.db"):
    for cand in ["/Volumes/HermesAgent/HermesAgentUSB/data",
                 _os.path.expanduser("~/.hermes-portable/data")]:
        if _os.path.exists(f"{cand}/state.db"):
            HERMES_HOME = cand
            break
state_db = f"{HERMES_HOME}/state.db"
error_log = f"{HERMES_HOME}/logs/gateway.error.log"
threads = ["1", "802", "803", "804", "1172"]

routing = {}
sessions = {}
errors = {}
overrides = {}

if os.path.exists(state_db):
    try:
        con = sqlite3.connect(state_db)
        cur = con.cursor()
        cur.execute("SELECT session_key, updated_at FROM gateway_routing WHERE session_key LIKE 'agent:main:telegram:group:%' ORDER BY session_key;")
        for skey, updated in cur.fetchall():
            tid = skey.split(":")[-1]
            routing[tid] = updated
        cur.execute("SELECT id, session_key, message_count FROM sessions WHERE session_key LIKE 'agent:main:telegram:group:%' ORDER BY session_key;")
        for sid, skey, msgs in cur.fetchall():
            tid = skey.split(":")[-1]
            sessions[tid] = (sid, msgs)
        con.close()
    except Exception as e:
        pass

if os.path.exists(error_log):
    for tid in threads:
        pat = re.compile(rf"thread=.*:{tid}([^0-9]|$)")
        matches = []
        with open(error_log, "r", errors="ignore") as f:
            for line in f:
                if pat.search(line) and "summary=" in line:
                    m = re.search(r"summary=([^\n|]{0,50})", line)
                    if m:
                        matches.append(m.group(1))
        if matches:
            errors[tid] = matches[-1]

if yaml:
    try:
        cfg = yaml.safe_load(open(f"{HERMES_HOME}/config.yaml"))
        for tid in threads:
            ov = cfg.get("platforms", {}).get("telegram", {}).get("channel_overrides", {}).get(tid, {})
            overrides[tid] = (ov.get("provider", "-"), ov.get("model", "-"))
    except Exception:
        pass

print(f"  {'Thread':<8} {'Status':<12} {'Model':<18} {'Provider':<10} {'Pesan':<8} Last Error")
print(f"  {'-------':<8} {'------':<12} {'-----':<18} {'--------':<10} {'-----':<8} ----------")
for tid in threads:
    if tid in routing:
        status = "Active"
        provider, model = overrides.get(tid, ("-", "-"))
        sid, msgs = sessions.get(tid, ("?", 0))
    else:
        status = "Inactive"
        provider, model = ("default", "default")
        msgs = 0
    err = errors.get(tid, "")[:50]
    model_disp = model[:15] + "..." if len(model) > 18 else model
    print(f"  {tid:<8} {status:<12} {model_disp:<18} {provider:<10} {str(msgs):<8} {err}")

print("")
print("  Last Activity (5 thread)")
for tid in threads:
    if tid in routing:
        ts = routing[tid]
        try:
            human = datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M")
        except Exception:
            human = ts
        _, msgs = sessions.get(tid, ("?", 0))
        print(f"  Thread {tid}: {msgs} pesan | aktif terakhir {human}")
    else:
        print(f"  Thread {tid}: tidak aktif / belum ada session")

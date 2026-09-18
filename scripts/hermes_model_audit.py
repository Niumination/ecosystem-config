#!/usr/bin/env python3
"""
Hermes Runtime Model Audit Tool
Reads state.db to report ACTIVE models per channel/session.
Source of truth: ~/.hermes/state.db sessions table.
"""

import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

STATE_DB = Path.home() / ".hermes" / "state.db"

def main():
    if not STATE_DB.exists():
        print(f"ERROR: {STATE_DB} not found")
        return
    
    conn = sqlite3.connect(STATE_DB)
    conn.row_factory = sqlite3.Row
    
    rows = conn.execute("""
        SELECT session_key, chat_id, thread_id, display_name, model, model_config, last_activity_at
        FROM sessions
        WHERE last_activity_at > (strftime('%s', 'now') - 86400 * 7)
          AND archived = 0
        ORDER BY last_activity_at DESC
    """).fetchall()
    
    print("=" * 70)
    print("🔍 HERMES RUNTIME MODEL AUDIT")
    print(f"⏰ Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"📁 Source: {STATE_DB} (sessions table, last 7 days)")
    print("=" * 70)
    print()
    
    dm_sessions = []
    group_sessions = []
    
    for row in rows:
        entry = {
            "session_key": row["session_key"],
            "chat_id": row["chat_id"],
            "thread_id": row["thread_id"],
            "display_name": row["display_name"] or "",
            "model": row["model"] or "(default)",
            "model_config": row["model_config"],
            "last_active": datetime.fromtimestamp(row["last_activity_at"], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC') if row["last_activity_at"] else "never"
        }
        
        if row["chat_id"] and row["chat_id"].startswith("-100"):
            group_sessions.append(entry)
        elif row["chat_id"]:
            dm_sessions.append(entry)
    
    if dm_sessions:
        print("📱 DM (Direct Messages):")
        print("-" * 50)
        for s in dm_sessions:
            print(f"  • {s['chat_id']:<15} {s['model']:<40} {s['last_active']}")
        print()
    
    if group_sessions:
        print("👥 Group Channels:")
        print("-" * 50)
        for s in group_sessions:
            thread = f"thread:{s['thread_id']}" if s['thread_id'] else "main"
            print(f"  • {s['display_name']:<25} {thread:<10} {s['model']:<40} {s['last_active']}")
        print()
    
    all_models = set()
    for s in dm_sessions + group_sessions:
        if s["model"] and s["model"] != "(default)":
            all_models.add(s["model"])
    
    print("=" * 70)
    print(f"📊 SUMMARY: {len(all_models)} unique models active in last 7 days")
    print()
    for m in sorted(all_models):
        print(f"  • {m}")
    
    # Config comparison
    config_file = Path.home() / ".hermes" / "config.yaml"
    if config_file.exists():
        try:
            import yaml
            with open(config_file) as f:
                config = yaml.safe_load(f)
            config_default = config.get("model", {}).get("default", "unknown")
            print()
            print(f"📄 Config default: {config_default}")
            uses_default = [s for s in dm_sessions + group_sessions if s["model"] == "(default)"]
            if uses_default:
                print(f"  ⚠️ {len(uses_default)} session(s) using config default")
        except:
            pass
    
    conn.close()

if __name__ == "__main__":
    main()

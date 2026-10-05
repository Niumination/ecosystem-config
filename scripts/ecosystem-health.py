#!/usr/bin/env python3
"""Ecosystem Health Check — single script, cron every 2h, deliver to thread 12595.
Checks: gateway, relay, cron, disk, system, Tailscale.
Reads tokens from ~/.hermes/.env (never prints them).
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

HERMES_HOME = Path.home() / ".hermes"
ENV_FILE = HERMES_HOME / ".env"
CRON_JOBS = HERMES_HOME / "cron" / "jobs.json"
THREAD_ID = "12595"
CHAT_ID = "-1004204696417"


def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except Exception as e:
        return str(e), -1


def parse_launchctl(label):
    """Parse launchctl list output for PID and LastExitStatus."""
    out, _ = run(f"launchctl list {label} 2>/dev/null")
    pid = "?"
    exit_code = "?"
    if '"PID"' in out:
        m = re.search(r'"PID"\s*=\s*(\d+)', out)
        if m:
            pid = m.group(1)
    if '"LastExitStatus"' in out:
        m = re.search(r'"LastExitStatus"\s*=\s*(\d+)', out)
        if m:
            exit_code = m.group(1)
    return pid, exit_code


def check_gateway(env):
    lines = []
    pid, exit_code = parse_launchctl("ai.hermes.gateway")
    if pid != "?":
        lines.append(f"Gateway: PID {pid}, last_exit={exit_code}")
    else:
        lines.append("Gateway: NOT RUNNING")
    # A2A bind
    out, _ = run("lsof -i :9900 2>/dev/null | head -3")
    if out:
        lines.append("A2A: listening on :9900")
    else:
        lines.append("A2A: NOT listening on :9900")
    # E2E
    a2a_host = env.get("A2A_HOST", "")
    a2a_token = env.get("A2A_BEARER_TOKEN", "")
    if a2a_host and a2a_token:
        try:
            req = urllib.request.Request(
                f"http://{a2a_host}:9900/health",
                headers={"Authorization": f"Bearer {a2a_token}"},
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                lines.append(f"E2E: {r.status} OK")
        except Exception as e:
            lines.append(f"E2E: FAIL ({e})")
    else:
        lines.append("E2E: no A2A_HOST or token")
    return lines


def check_relay(env):
    lines = []
    pid, exit_code = parse_launchctl("com.niumination.office-relay")
    if pid != "?":
        lines.append(f"Relay: PID {pid}, last_exit={exit_code}")
    else:
        lines.append("Relay: NOT RUNNING")
    # Presence — office server is on cloud, not localhost
    office_token = env.get("OFFICE_MAC_TOKEN", "")
    cloud_ip = "100.65.20.34"
    if office_token:
        try:
            req = urllib.request.Request(
                f"http://{cloud_ip}:7333/presence",
                headers={"Authorization": f"Bearer {office_token}"},
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                agents = data.get("agents", {})
                mac = agents.get("mac", {})
                cloud = agents.get("cloud", {})
                lines.append(f"Presence: mac={mac.get('online', '?')} cloud={cloud.get('online', '?')}")
        except Exception as e:
            lines.append(f"Presence: FAIL ({e})")
    else:
        lines.append("Presence: no OFFICE_MAC_TOKEN")
    # Log errors
    err_log = Path.home() / "Library/Logs/office-relay.err.log"
    if err_log.exists():
        size = err_log.stat().st_size
        lines.append(f"Relay err log: {size} bytes")
    else:
        lines.append("Relay err log: none")
    return lines


def check_cron():
    lines = []
    if not CRON_JOBS.exists():
        return ["Cron: jobs.json not found"]
    try:
        data = json.loads(CRON_JOBS.read_text())
        jobs = data.get("jobs", data) if isinstance(data, dict) else data
        active = [j for j in jobs if j.get("enabled", True)]
        lines.append(f"Cron: {len(active)} active jobs")
        for j in active:
            name = j.get("name", j.get("id", "?"))[:30]
            last = j.get("last_run_at", j.get("last_run", "never"))
            status = j.get("last_status", "?")
            lines.append(f"  {name}: last={str(last)[:16]} status={status}")
    except Exception as e:
        lines.append(f"Cron: FAIL ({e})")
    return lines


def check_disk():
    lines = []
    out, _ = run("df -h / | tail -1")
    if out:
        parts = out.split()
        if len(parts) >= 5:
            lines.append(f"Disk: {parts[2]} / {parts[1]} ({parts[4]})")
    return lines


def check_system():
    lines = []
    out, _ = run("uptime | awk -F'load averages:' '{print $2}'")
    if out:
        lines.append(f"Load:{out}")
    out, _ = run("ps -Ao pid,%cpu,command -r 2>/dev/null | head -4 | tail -3")
    if out:
        lines.append("Top CPU:")
        for line in out.splitlines():
            lines.append(f"  {line[:80]}")
    return lines


def check_tailscale():
    lines = []
    out, _ = run("tailscale ip -4 2>/dev/null")
    if out:
        lines.append(f"Tailscale IP: {out}")
    else:
        lines.append("Tailscale: not connected")
    out, _ = run("tailscale status 2>/dev/null | grep -E '100\\.65\\.|vm-6-34' | head -1")
    if out:
        lines.append(f"Peer cloud: {out.split()[1] if len(out.split()) > 1 else '?'}")
    else:
        lines.append("Peer cloud: not found")
    return lines


def main():
    env = load_env()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = [f"Niumination Health Check — {now}", ""]
    report += check_gateway(env)
    report.append("")
    report += check_relay(env)
    report.append("")
    report += check_cron()
    report.append("")
    report += check_disk()
    report.append("")
    report += check_system()
    report.append("")
    report += check_tailscale()
    text = "\n".join(report)
    print(text)


if __name__ == "__main__":
    main()

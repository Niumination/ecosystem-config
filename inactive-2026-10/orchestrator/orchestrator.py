#!/usr/bin/env python3
import argparse
import json
import os
import sys

from .utils.logger import setup_logger
from .utils.opencode_bridge import OpenCodeBridge
from .utils.scheduler import Scheduler
from .tasks.daily_brief import DailyBriefTask
from .tasks.daily_news import DailyNewsTask
from .tasks.vault_organize import VaultOrganizeTask
from .tasks.summarize import SummarizeTask

ORCHESTRATOR_DIR = os.path.dirname(os.path.abspath(__file__))

TASK_REGISTRY = {
    "daily_brief": DailyBriefTask(),
    "daily_news": DailyNewsTask(),
    "vault_organize": VaultOrganizeTask(),
    "summarize": SummarizeTask(),
}

def load_config():
    cfg_path = os.path.join(ORCHESTRATOR_DIR, "config.json")
    if not os.path.exists(cfg_path):
        print("✗ config.json not found in Orchestrator/")
        sys.exit(1)
    with open(cfg_path) as f:
        return json.load(f)

def build_runtime_config(config, log):
    runtime = dict(config)
    runtime["_log"] = log
    runtime["_bridge"] = OpenCodeBridge(
        opencode_path=config.get("opencode_path", "opencode"),
        logger=log
    )
    return runtime

def cmd_list(config, log):
    log.info("Available tasks:")
    for name, task in TASK_REGISTRY.items():
        log.info("  %-16s %s", name, task.description)

def cmd_status(config, log):
    from .utils.vault_state import VaultState
    vault = VaultState(config["vault_root"])
    stats = vault.get_stats()
    structure = vault.scan()
    log.info("Vault: %s", config["vault_root"])
    log.info("  Files: %d", stats["total_files"])
    log.info("  Size:  %s", stats["total_size_mb"])
    log.info("  Folders:")
    for f in structure["folders"]:
        log.info("    %-20s (%d files)", f["name"], f["file_count"])
    log.info("  Root files:")
    for f in structure["files"]:
        log.info("    %s", f["name"])

def run_task(task_name, runtime_config, log):
    if task_name not in TASK_REGISTRY:
        log.error("Unknown task: %s", task_name)
        log.info("Use 'list' to see available tasks")
        return False
    task = TASK_REGISTRY[task_name]
    log.info("🚀 Starting task: %s", task_name)
    log.info("   %s", task.description)
    try:
        result = task.run(runtime_config)
        log.info("✅ Task '%s' completed", task_name)
        return True
    except Exception as e:
        log.error("❌ Task '%s' failed: %s", task_name, str(e))
        import traceback
        log.debug(traceback.format_exc())
        return False

def main():
    parser = argparse.ArgumentParser(
        prog="orchestrator",
        description="AI Agent Orchestrator — Automate vault management tasks"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="list",
        choices=["list", "status", "daily-routine", "daily_brief", "daily_news",
                 "vault_organize", "summarize", "daemon", "schedule-install",
                 "vault-organize", "daily-brief", "daily-news"],
        help="Task to run"
    )
    parser.add_argument(
        "--config", "-c",
        default=None,
        help="Path to config file (default: Orchestrator/config.json)"
    )
    parser.add_argument(
        "--schedule",
        default=None,
        help="Path to schedule file (default: Orchestrator/schedule.json)"
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=60,
        help="Daemon check interval in seconds (default: 60)"
    )
    args = parser.parse_args()
    config = load_config()
    log_dir = os.path.join(ORCHESTRATOR_DIR, config.get("log_dir", "logs"))
    log = setup_logger("orchestrator", log_dir)
    cmd = args.command.replace("-", "_")
    if cmd == "list":
        cmd_list(config, log)
    elif cmd == "status":
        cmd_status(config, log)
    elif cmd == "daily_routine":
        tasks = config.get("daily_routine_tasks", ["daily_brief", "daily_news", "vault_organize"])
        runtime = build_runtime_config(config, log)
        for t in tasks:
            run_task(t, runtime, log)
    elif cmd in TASK_REGISTRY:
        runtime = build_runtime_config(config, log)
        run_task(cmd, runtime, log)
    elif cmd == "daemon":
        schedule_path = args.schedule or os.path.join(ORCHESTRATOR_DIR, "schedule.json")
        runtime = build_runtime_config(config, log)
        scheduler = Scheduler(schedule_path, TASK_REGISTRY, runtime, log)
        scheduler.daemon_loop(interval=args.interval)
    elif cmd == "schedule_install":
        log.info("To run daemon in background, use:")
        log.info("  nohup python3 -m Orchestrator.orchestrator daemon &")
        log.info("Or add to crontab:")
        log.info("  @reboot cd %s && nohup python3 -m Orchestrator.orchestrator daemon &",
                 os.path.dirname(ORCHESTRATOR_DIR))

if __name__ == "__main__":
    main()

import json
import os
import time
import subprocess
from datetime import datetime

class Scheduler:
    def __init__(self, schedule_path, task_registry, config, logger):
        self.schedule_path = schedule_path
        self.task_registry = task_registry
        self.config = config
        self.log = logger
        self._last_run = {}

    def load_schedule(self):
        if not os.path.exists(self.schedule_path):
            self.log.warning(f"Schedule file not found: {self.schedule_path}")
            return {}
        with open(self.schedule_path) as f:
            return json.load(f)

    def check(self):
        now = datetime.now()
        schedule = self.load_schedule()
        triggered = []
        for task_name, rule in schedule.items():
            if not rule.get("enabled", True):
                continue
            if rule["hour"] == now.hour and rule["minute"] == now.minute:
                last = self._last_run.get(task_name)
                if last is None or (now - last).total_seconds() > 60:
                    triggered.append(task_name)
                    self._last_run[task_name] = now
        return triggered

    def daemon_loop(self, interval=60):
        self.log.info("Scheduler daemon started (check every %ss)", interval)
        self.log.info("Press Ctrl+C to stop")
        try:
            while True:
                triggered = self.check()
                for task_name in triggered:
                    self.log.info("⏰ Scheduled: %s", task_name)
                    if task_name in self.task_registry:
                        task = self.task_registry[task_name]
                        task.run(self.config)
                    else:
                        self.log.warning("Unknown task: %s", task_name)
                time.sleep(interval)
        except KeyboardInterrupt:
            self.log.info("Scheduler daemon stopped")

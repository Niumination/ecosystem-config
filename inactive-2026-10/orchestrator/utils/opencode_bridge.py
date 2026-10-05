import subprocess
import sys
import shlex

class OpenCodeBridge:
    def __init__(self, opencode_path="opencode", logger=None):
        self.opencode_path = opencode_path
        self._log = logger

    def log(self, msg, level="info"):
        if self._log:
            getattr(self._log, level, print)(msg)

    def call_skill(self, skill_name):
        cmd = [self.opencode_path, "run", "skill", skill_name]
        self.log(f"  → opencode skill: {skill_name}")
        return self._run(cmd)

    def call_prompt(self, prompt):
        cmd = [self.opencode_path, shlex.quote(prompt)]
        self.log(f"  → opencode prompt: {prompt[:80]}...")
        return self._run(cmd)

    def _run(self, cmd):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.stdout:
                self.log(result.stdout.strip()[:200])
            if result.returncode != 0:
                self.log(f"  ⚠ exit code {result.returncode}", "warning")
                if result.stderr:
                    self.log(f"  stderr: {result.stderr.strip()[:200]}", "warning")
            return result
        except FileNotFoundError:
            self.log(f"  ✗ opencode not found at: {self.opencode_path}", "error")
            return None
        except subprocess.TimeoutExpired:
            self.log(f"  ✗ opencode timed out (300s)", "error")
            return None

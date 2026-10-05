from .base import Task
from ..utils.vault_state import VaultState

class DailyBriefTask(Task):
    name = "daily_brief"
    description = "Generate daily brief with calendar, weather, and priorities"

    def run(self, config):
        log = config.get("_log")
        bridge = config.get("_bridge")
        vault = VaultState(config["vault_root"])
        stats = vault.get_stats()
        structure = vault.scan()
        if log:
            log.info("📊 Vault: %d files (%s)", stats["total_files"], stats["total_size_mb"])
            log.info("📁 Folders: %s", ", ".join(f["name"] for f in structure["folders"]))
        if bridge:
            log.info("Running daily-brief skill via OpenCode...")
            result = bridge.call_skill("daily-brief")
            if result and result.returncode == 0:
                log.info("✅ Daily brief generated")
            else:
                log.warning("⚠️ Daily brief skill returned non-zero")
        return {"status": "done", "stats": stats}

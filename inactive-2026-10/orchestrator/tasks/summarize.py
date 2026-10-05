from .base import Task
from ..utils.vault_state import VaultState

class SummarizeTask(Task):
    name = "summarize"
    description = "Summarize new clips and read-it-later items"

    def run(self, config):
        log = config.get("_log")
        bridge = config.get("_bridge")
        sources = config.get("summarize_sources", [])
        vault = VaultState(config["vault_root"])
        items = vault.get_unprocessed(sources)
        if not items:
            log.info("No unprocessed items to summarize")
            return {"status": "done", "summarized": 0}
        log.info("Found %d item(s) to summarize", len(items))
        for item in items:
            log.info("  %s (%s)", item["name"], item["path"])
        if bridge:
            for item in items:
                prompt = f"summarize the content at {item['name']}"
                bridge.call_prompt(prompt)
        log.info("✅ All items processed")
        return {"status": "done", "summarized": len(items)}

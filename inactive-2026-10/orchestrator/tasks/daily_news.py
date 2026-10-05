from .base import Task
from ..utils.news_fetcher import NewsFetcher
from datetime import datetime
from pathlib import Path

class DailyNewsTask(Task):
    name = "daily_news"
    description = "Hasilkan ringkasan berita harian dari RSS — anime, youtube, tech, bisnis, sains, dunia"

    def run(self, config):
        log = config.get("_log")
        log.info("Fetching news from RSS sources...")
        fetcher = NewsFetcher(logger=log)
        digest = fetcher.fetch_all()
        if not any(s["items"] for s in digest.values()):
            log.warning("All RSS feeds failed — falling back to OpenCode bridge")
            bridge = config.get("_bridge")
            if bridge:
                bridge.call_skill("daily-news")
            return {"status": "fallback", "digest": digest}
        markdown = fetcher.generate_markdown(digest)
        news_dir = Path(config["vault_root"]) / "01 Updates"
        news_dir.mkdir(parents=True, exist_ok=True)
        news_path = news_dir / "Harini.md"
        news_path.write_text(markdown, encoding="utf-8")
        log.info("✅ Ringkasan harian selesai: 01 Updates/Harini.md")
        for topic, section in digest.items():
            count = len(section["items"])
            if count > 0:
                log.info("  %s: %d stories", section["label"], count)
                for i, item in enumerate(section["items"][:2]):
                    log.info("    %s", item["title"][:80])
        return {"status": "done", "digest": {t: len(s["items"]) for t, s in digest.items()}}

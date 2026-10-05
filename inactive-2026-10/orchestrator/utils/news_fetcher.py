import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from html import unescape
import re

USER_AGENT = "ZMP-Orchestrator/1.0"

RSS_SOURCES = {
    "anime_donghua": [
        ("Anime News Network", "https://www.animenewsnetwork.com/news/rss.xml"),
        ("MyAnimeList", "https://myanimelist.net/rss/news.xml"),
    ],
    "youtube": [
        ("YouTube - IGN", "https://www.youtube.com/feeds/videos.xml?channel_id=UCKy1dAqELo0zrOtPkf0eTMw"),
        ("YouTube - Fireship", "https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA"),
    ],
    "technology": [
        ("Hacker News", "https://hnrss.org/frontpage?count=5"),
        ("TechCrunch", "https://techcrunch.com/feed/"),
    ],
    "business": [
        ("Google News Business", "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB"),
        ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ],
    "science": [
        ("ScienceDaily", "https://www.sciencedaily.com/rss/all.xml"),
        ("Nature", "https://www.nature.com/nature.rss"),
    ],
    "world": [
        ("BBC News", "https://feeds.bbci.co.uk/news/rss.xml"),
        ("NPR", "https://feeds.npr.org/1001/rss.xml"),
    ],
}

TOPIC_LABELS = {
    "anime_donghua": "🎌 Anime & Donghua",
    "youtube": "🎥 YouTube",
    "technology": "Technology & AI",
    "business": "Business & Finance",
    "science": "Science & Health",
    "world": "World News",
}

class NewsFetcher:
    def __init__(self, logger=None):
        self._log = logger

    def log(self, msg, level="info"):
        if self._log:
            getattr(self._log, level, print)(msg)

    def fetch_feed(self, url, timeout=10):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            root = ET.fromstring(raw)
            items = []
            for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
                title = entry.findtext("{http://www.w3.org/2005/Atom}title", "")
                link_el = entry.find("{http://www.w3.org/2005/Atom}link")
                link = link_el.get("href", "") if link_el is not None else ""
                summary = entry.findtext("{http://www.w3.org/2005/Atom}summary", "")
                items.append({"title": unescape(title.strip()), "link": link.strip(), "summary": unescape(summary.strip())})
            for item in root.iter("item"):
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                desc = item.findtext("description", "")
                if title:
                    items.append({"title": unescape(title.strip()), "link": link.strip(), "summary": unescape(re.sub(r"<[^>]+>", "", desc).strip())})
            return items[:10]
        except Exception as e:
            self.log(f"  ⚠ RSS feed failed: {url[:60]}... ({e})", "warning")
            return []

    def fetch_all(self):
        digest = {}
        for topic, sources in RSS_SOURCES.items():
            label = TOPIC_LABELS.get(topic, topic)
            self.log(f"  Fetching {label}...")
            all_items = []
            for name, url in sources:
                items = self.fetch_feed(url)
                for it in items:
                    it["source"] = name
                all_items.extend(items)
            all_items.sort(key=lambda x: len(x.get("summary", "")), reverse=True)
            seen_titles = set()
            unique = []
            for it in all_items:
                t = it["title"].lower()[:60]
                if t not in seen_titles:
                    seen_titles.add(t)
                    unique.append(it)
            digest[topic] = {"label": label, "items": unique[:5]}
        return digest

    def generate_markdown(self, digest, date_str=None):
        if date_str is None:
            date_str = datetime.now().strftime("%A, %d %B %Y")
        lines = [
            "---",
            "type: daily-news",
            f"date: {datetime.now().strftime('%Y-%m-%d')}",
            "---",
            "",
            f"# Harini — {date_str}",
            "",
        ]
        for topic in ["anime_donghua", "youtube", "technology", "business", "science", "world"]:
            section = digest.get(topic)
            if not section or not section["items"]:
                continue
            lines.append(f"## {section['label']}")
            lines.append("")
            for i, item in enumerate(section["items"]):
                title = item["title"]
                link = item["link"]
                summary = item.get("summary", "") or item.get("description", "")
                source = item.get("source", "")
                if i == 0:
                    lines.append(f"**[{title}]({link}**)")
                    if source:
                        lines.append(f"*{source}*")
                    if summary:
                        lines.append(summary[:300])
                    lines.append("")
                else:
                    lines.append(f"- [{title}]({link}) — {summary[:150]}")
                    lines.append("")
        lines.append("---")
        lines.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M')}*")
        lines.append("")
        return "\n".join(lines)

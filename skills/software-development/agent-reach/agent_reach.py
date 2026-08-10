#!/usr/bin/env python3
"""
Agent Reach wrapper for Hermes Agent.
Falls back to direct tools if agent-reach CLI is not installed.
"""
import json
import subprocess
import sys
import os
import time
from urllib.parse import urlparse

PLATFORM = sys.argv[1] if len(sys.argv) > 1 else "help"
ARGS = sys.argv[2:] if len(sys.argv) > 2 else []


def run(cmd, timeout=30):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return out.stdout, out.stderr, out.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", 124
    except Exception as e:
        return "", str(e), 1


def agent_reach_available():
    out, _, _ = run(["agent-reach", "--version"])
    return out.strip().startswith("agent-reach")


def call_agent_reach(platform, args):
    cmd = ["agent-reach", platform] + args
    out, err, code = run(cmd)
    return out, err, code


def fallback_web(url):
    # Jina Reader
    out, err, code = run(["curl", "-s", "--max-time", "20", f"https://r.jina.ai/{url}"])
    if code == 0 and out:
        return {
            "platform": "web",
            "url": url,
            "status": "ok",
            "data": {"title": "", "content": out[:5000], "summary": ""},
            "raw": out[:2000],
            "meta": {"backend": "jina-reader", "latency_ms": 0},
        }
    return {
        "platform": "web",
        "url": url,
        "status": "error",
        "data": {},
        "raw": err or "No output",
        "meta": {"backend": "none", "latency_ms": 0},
    }


def fallback_youtube(url):
    out, err, code = run(["yt-dlp", "--dump-json", "--no-warnings", url], timeout=60)
    if code == 0 and out:
        try:
            data = json.loads(out.split("\n")[0])
            return {
                "platform": "youtube",
                "url": url,
                "status": "ok",
                "data": {
                    "title": data.get("title", ""),
                    "content": data.get("description", "")[:5000],
                    "summary": "",
                },
                "raw": out[:2000],
                "meta": {"backend": "yt-dlp", "latency_ms": 0},
            }
        except Exception:
            pass
    return {
        "platform": "youtube",
        "url": url,
        "status": "error",
        "data": {},
        "raw": err or out[:500] or "yt-dlp failed",
        "meta": {"backend": "none", "latency_ms": 0},
    }


def fallback_github(repo):
    out, err, code = run(["gh", "repo", "view", repo, "--json", "url,description,name,owner"], timeout=20)
    if code == 0 and out:
        try:
            data = json.loads(out)
            return {
                "platform": "github",
                "url": f"https://github.com/{repo}",
                "status": "ok",
                "data": {
                    "title": data.get("name", repo),
                    "content": data.get("description", ""),
                    "summary": "",
                },
                "raw": out[:2000],
                "meta": {"backend": "gh-cli", "latency_ms": 0},
            }
        except Exception:
            pass
    return {
        "platform": "github",
        "url": f"https://github.com/{repo}",
        "status": "error",
        "data": {},
        "raw": err or out[:500] or "gh failed",
        "meta": {"backend": "none", "latency_ms": 0},
    }


def fallback_rss(url):
    # Try feedparser if available
    try:
        import feedparser
        feed = feedparser.parse(url)
        if feed.entries:
            items = []
            for entry in feed.entries[:10]:
                items.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": (entry.get("summary", "") or "")[:200],
                })
            return {
                "platform": "rss",
                "url": url,
                "status": "ok",
                "data": {"items": items, "count": len(items)},
                "raw": json.dumps(items[:2]),
                "meta": {"backend": "feedparser", "latency_ms": 0},
            }
    except ImportError:
        pass
    return {
        "platform": "rss",
        "url": url,
        "status": "error",
        "data": {"error": "feedparser not installed"},
        "raw": "feedparser not installed. Install with: pip install feedparser",
        "meta": {"backend": "none", "latency_ms": 0},
    }


def main():
    if PLATFORM in ("help", "--help", "-h"):
        print(json.dumps({
            "commands": ["web <url>", "youtube <url>", "github <owner/repo>", "rss <url>"],
            "fallbacks": ["jina-reader", "yt-dlp", "gh-cli", "feedparser"]
        }, indent=2))
        return

    if agent_reach_available():
        out, err, code = call_agent_reach(PLATFORM, ARGS)
        if code == 0 and out.strip():
            print(out)
            return
        # Fall through to fallback if agent-reach fails

    if PLATFORM == "web" and ARGS:
        print(json.dumps(fallback_web(ARGS[0]), indent=2, ensure_ascii=False))
    elif PLATFORM == "youtube" and ARGS:
        print(json.dumps(fallback_youtube(ARGS[0]), indent=2, ensure_ascii=False))
    elif PLATFORM == "github" and ARGS:
        print(json.dumps(fallback_github(ARGS[0]), indent=2, ensure_ascii=False))
    elif PLATFORM == "rss" and ARGS:
        print(json.dumps(fallback_rss(ARGS[0]), indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": "Usage: agent_reach.py <platform> <args>"}, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Firefox Tab Stash Extractor & Categorizer
Extracts Tab Stash bookmarks (even when Firefox is running via temp copy)
and categorizes URLs automatically.
"""

import os
import sys
import shutil
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime

PROFILE_DIR = Path.home() / "Library/Application Support/Firefox/Profiles/3setc0jl.default-release"
PLACES_DB = PROFILE_DIR / "places.sqlite"
TEMP_DB = Path("/tmp/places_copy.sqlite")
OUTPUT_DIR = Path.home() / "Desktop/Niumination/vault/tab-stash"
BRAIN_INBOX = Path.home() / "Desktop/Niumination/brain/inbox"

# Category rules based on URL / Title keywords
CATEGORIES = {
    "AI & Machine Learning": [r"ai", r"gpt", r"claude", r"llm", r"openai", r"huggingface", r"anthropic", r"gemini", r"nous", r"model", r"deepseek", r"ollama", r"vllm"],
    "Development & GitHub": [r"github\.com", r"gitlab", r"stackoverflow", r"npm", r"pypi", r"python", r"react", r"nextjs", r"typescript", r"docker", r"vercel"],
    "Government & Diskominfo": [r"go\.id", r"acehtengah", r"kominfo", r"pemda", r"bkn", r"ekinerja", r"dtsen", r"bappeda"],
    "Productivity & Tools": [r"notion", r"airtable", r"trello", r"kanban", r"figma", r"excalidraw", r"drive\.google", r"docs\.google"],
    "News & Knowledge": [r"medium\.com", r"dev\.to", r"wikipedia", r"arxiv", r"submstack", r"youtube\.com", r"youtu\.be"]
}

def categorize_url(url, title):
    combined = f"{url} {title}".lower()
    for cat, patterns in CATEGORIES.items():
        for pat in patterns:
            if re.search(pat, combined):
                return cat
    return "Uncategorized & General"

def extract_tabs():
    if not PLACES_DB.exists():
        print(f"Error: {PLACES_DB} does not exist.")
        return []

    # Copy to temp to prevent SQLite lock if Firefox is running
    shutil.copy2(PLACES_DB, TEMP_DB)
    if (PROFILE_DIR / "places.sqlite-wal").exists():
        shutil.copy2(PROFILE_DIR / "places.sqlite-wal", Path("/tmp/places_copy.sqlite-wal"))

    conn = sqlite3.connect(str(TEMP_DB))
    cursor = conn.cursor()

    # Find Tab Stash parent folder ID(s)
    cursor.execute("SELECT id, title FROM moz_bookmarks WHERE title LIKE '%stash%' OR title LIKE '%Tab Stash%'")
    stash_folders = cursor.fetchall()

    stashed_tabs = []

    def get_bookmarks_recursive(parent_id, current_path=""):
        cursor.execute("""
            SELECT b.id, b.title, b.type, b.dateAdded, h.url
            FROM moz_bookmarks b
            LEFT JOIN moz_places h ON b.fk = h.id
            WHERE b.parent = ?
            ORDER BY b.dateAdded DESC
        """, (parent_id,))
        rows = cursor.fetchall()
        for b_id, title, b_type, date_added, url in rows:
            dt_str = datetime.fromtimestamp(date_added / 1000000).strftime("%Y-%m-%d %H:%M:%S") if date_added else "Unknown"
            if b_type == 2:  # Folder
                sub_path = f"{current_path} / {title}" if current_path else title
                get_bookmarks_recursive(b_id, sub_path)
            elif b_type == 1 and url:  # Bookmark
                stashed_tabs.append({
                    "title": title or "Untitled",
                    "url": url,
                    "date_added": dt_str,
                    "folder": current_path or "Root Stash",
                    "category": categorize_url(url, title or "")
                })

    for folder_id, folder_title in stash_folders:
        get_bookmarks_recursive(folder_id, folder_title)

    conn.close()
    
    # Cleanup temp
    if TEMP_DB.exists():
        os.remove(TEMP_DB)
    if Path("/tmp/places_copy.sqlite-wal").exists():
        os.remove(Path("/tmp/places_copy.sqlite-wal"))

    return stashed_tabs

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BRAIN_INBOX.mkdir(parents=True, exist_ok=True)

    tabs = extract_tabs()
    print(f"Extracted {len(tabs)} tabs from Tab Stash.")

    # Save JSON
    json_path = OUTPUT_DIR / "tab-stash-categorized.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tabs, f, indent=2, ensure_ascii=False)

    # Save Markdown Report in Vault
    md_path = OUTPUT_DIR / "tab-stash-categorized.md"
    
    # Group by category
    by_category = {}
    for t in tabs:
        cat = t["category"]
        by_category.setdefault(cat, []).append(t)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 🔖 Tab Stash Categorized Summary\n\n")
        f.write(f"**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Total Stashed Tabs:** {len(tabs)}\n\n")
        f.write("---\n\n")

        for cat, items in by_category.items():
            f.write(f"## {cat} ({len(items)})\n\n")
            for item in items:
                f.write(f"- **[{item['title']}]({item['url']})**\n")
                f.write(f"  - *Folder:* `{item['folder']}` | *Added:* {item['date_added']}\n")
            f.write("\n")

    # Also write a copy to Brain Inbox for Second Brain integration
    brain_copy = BRAIN_INBOX / "tab-stash-latest.md"
    shutil.copy2(md_path, brain_copy)

    print(f"✅ Categorized JSON saved to {json_path}")
    print(f"✅ Markdown report saved to {md_path}")
    print(f"✅ Second Brain copy saved to {brain_copy}")

if __name__ == "__main__":
    main()

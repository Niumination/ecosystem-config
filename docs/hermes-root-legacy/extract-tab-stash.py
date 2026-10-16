#!/usr/bin/env python3
"""Extract Tab Stash data from Firefox places.sqlite"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Firefox profile path
profile_dir = Path.home() / "Library/Application Support/Firefox/Profiles/3setc0jl.default-release"
places_db = profile_dir / "places.sqlite"
output_dir = Path.home() / "Desktop/Niumination/vault/tab-stash"

# Create output directory
output_dir.mkdir(parents=True, exist_ok=True)

# Connect to database
conn = sqlite3.connect(str(places_db))
cursor = conn.cursor()

print("🔍 Scanning for Tab Stash bookmarks...")

# Find Tab Stash folder
cursor.execute("""
    SELECT id, title, type FROM moz_bookmarks 
    WHERE title LIKE '%stash%' OR title LIKE '%Tab Stash%'
""")
stash_folders = cursor.fetchall()

print(f"Found {len(stash_folders)} Tab Stash folders")

if not stash_folders:
    print("No Tab Stash folders found. Checking all bookmark folders...")
    cursor.execute("""
        SELECT id, title, type FROM moz_bookmarks 
        WHERE parent = 6 ORDER BY dateAdded DESC LIMIT 20
    """)
    all_folders = cursor.fetchall()
    print(f"Recent folders: {all_folders}")
else:
    # Process each Tab Stash folder
    all_stashes = []
    
    for folder_id, folder_title, folder_type in stash_folders:
        print(f"\n📁 Processing: {folder_title} (ID: {folder_id})")
        
        # Get all bookmarks in this folder
        cursor.execute("""
            SELECT b.id, b.title, b.dateAdded, b.lastModified, h.url
            FROM moz_bookmarks b
            LEFT JOIN moz_places h ON b.fk = h.id
            WHERE b.parent = ?
            ORDER BY b.dateAdded
        """, (folder_id,))
        
        bookmarks = cursor.fetchall()
        print(f"   Found {len(bookmarks)} tabs")
        
        for bm_id, title, date_added, last_modified, url in bookmarks:
            if date_added:
                dt = datetime.fromtimestamp(date_added / 1000000)
                date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                date_str = "Unknown"
            
            all_stashes.append({
                'title': title,
                'url': url,
                'date_added': date_str,
                'folder': folder_title
            })
    
    # Save to JSON
    output_file = output_dir / "tab-stash-export.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_stashes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Exported {len(all_stashes)} tabs to: {output_file}")
    
    # Save as Markdown for readability
    md_file = output_dir / "tab-stash-summary.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Tab Stash Export\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Tabs:** {len(all_stashes)}\n\n")
        f.write("---\n\n")
        
        # Group by folder
        folders = {}
        for stash in all_stashes:
            folder = stash['folder']
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(stash)
        
        for folder, tabs in folders.items():
            f.write(f"## {folder}\n\n")
            for tab in tabs:
                f.write(f"- **{tab['title']}** ({tab['date_added']})\n")
                f.write(f"  - {tab['url']}\n\n")
    
    print(f"✅ Summary saved to: {md_file}")

conn.close()
print("\n✨ Done!")

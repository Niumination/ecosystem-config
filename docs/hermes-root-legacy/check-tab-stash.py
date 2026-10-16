#!/usr/bin/env python3
"""Check Tab Stash bookmarks in Firefox profile."""
import json
import os
from pathlib import Path
from datetime import datetime

profile_dir = Path.home() / "Library/Application Support/Firefox/Profiles/3setc0jl.default-release"

# Try to read bookmarks.html
bookmarks_file = profile_dir / "bookmarks.html"
if bookmarks_file.exists():
    content = bookmarks_file.read_text(encoding='utf-8', errors='ignore')
    
    # Look for Tab Stash related bookmarks
    stash_lines = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if 'tab-stash' in line.lower() or 'stash' in line.lower() or 'Tab Stash' in line:
            # Get context around the match
            start = max(0, i-2)
            end = min(len(lines), i+5)
            stash_lines.extend(lines[start:end])
    
    if stash_lines:
        print("Found Tab Stash references in bookmarks.html:")
        print('\n'.join(stash_lines[:50]))
    else:
        print("No Tab Stash references found in bookmarks.html")
        
    # Count total lines
    print(f"\nTotal lines in bookmarks.html: {len(lines)}")
else:
    print("bookmarks.html not found")

# Check for DMP (Data Migration Platform) files
dmp_files = list(profile_dir.glob("*.jsonlz4"))
if dmp_files:
    print(f"\nFound {len(dmp_files)} JSONLZ4 files:")
    for f in dmp_files:
        print(f"  - {f.name}")

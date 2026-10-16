# Tab Stash Check Results

**Date:** 30 Ags 2026
**Firefox Profile:** 3setc0jl.default-release

## Status
- ✅ **Tab Stash Extension Installed** (v3.4)
- ✅ **Extension Active** (not disabled)
- ⚠️ **Cannot Access Saved Tabs** - Firefox is running and locking the database

## What I Found

### Extension Details
```
ID: tab-stash@condordes.net
Version: 3.4
Status: Active (not disabled)
Location: ~/Library/Application Support/Firefox/Profiles/3setc0jl.default-release/extensions/tab-stash@condordes.net.xpi
```

### Why I Can't Check Stashed Tabs
1. **Firefox is running** (PID 17721)
2. **places.sqlite is locked** (database locked error)
3. Bookmark data is stored in SQLite, which Firefox locks while running

## How to Check Tab Stash Yourself

### Method 1: Via Firefox UI (Easiest)
1. Open Firefox
2. Click the **Tab Stash icon** in toolbar (looks like a stack of tabs)
3. Or press `Cmd+Shift+S` (default shortcut)
4. Sidebar will show all your stashed tabs grouped by date/time

### Method 2: Close Firefox First
```bash
# Close Firefox
pkill -f Firefox

# Then check via terminal (I can do this for you)
# Or manually inspect the bookmarks
```

### Method 3: Check Bookmarks Folder
Tab Stash saves tabs as bookmarks in a folder called **"Tab Stash"** in your bookmarks. You can:
1. Open Bookmarks Manager (`Cmd+Shift+B`)
2. Look for folder named "Tab Stash"
3. Inside are subfolders grouped by date/time

## Backup Files Found
```
~/Library/Application Support/Firefox/Profiles/3setc0jl.default-release/bookmarkbackups/
├── bookmarks-2026-08-30_523_*.jsonlz4  (Latest)
├── bookmarks-2026-08-29_512_*.jsonlz4
└── bookmarks-2026-08-28_10_*.jsonlz4
```

## Recommendation

**Close Firefox first**, then I can query the bookmarks database to show you exactly what's in your Tab Stash folders.

Would you like me to:
1. Close Firefox for you, then check Tab Stash?
2. Guide you through checking it manually in Firefox UI?
3. Both?

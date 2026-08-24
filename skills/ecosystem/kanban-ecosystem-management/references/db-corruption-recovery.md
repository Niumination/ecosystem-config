# Kanban DB Corruption Recovery

## Quick Detection

If `hermes kanban list` or `hermes kanban stats` fails with:

```
Error: file is not a database: invalid SQLite header
```

Or if the Niu-Kanban Dash dashboard shows 0 tasks when tasks exist:

### 1. Check the DB file size

```bash
file /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db
ls -la /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db
```

A healthy SQLite DB starts at ~4KB+ (3+ pages). A 1-byte file is corrupt — likely truncated during an unclean shutdown (USB disconnect, crash, power loss while Hermes was writing).

### 2. Check for automatic backups

Hermes creates `.corrupt.*.bak` files automatically on detection:

```bash
ls -la /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db.corrupt.*.bak
ls -la /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db.corrupt.current*
```

Some may have WAL/SHM companions (`.bak-wal`, `.bak-shm`) that hold committed but un-checkpointed transactions.

### 3. Attempt backup restoration

```bash
cd /Volumes/HermesAgent/HermesAgentUSB/data

# Try each backup by size (largest = most data)
for bak in kanban.db.corrupt.*.bak; do
  sz=$(wc -c < "$bak" 2>/dev/null || echo 0)
  echo "$sz bytes  $bak"
done | sort -rn

# Try largest one:
cp kanban.db.corrupt.XXXX.bak kanban.db.test
sqlite3 kanban.db.test ".tables" 2>/dev/null || echo "Still corrupt"
```

### 4. If all backups are also corrupt

If every backup is also 0-1 bytes or fails SQLite validation, the corruption is systemic — the DB was already empty when the corruption was recorded. Options:

- **Rebuild from AGENTS.md + BACKLOG.md** — the project catalog in AGENTS.md has all 55+ projects with categories, priorities, and status. Use that as the base data for a fresh kanban board.
- **Check the `boards/` directory** — `/Volumes/HermesAgent/HermesAgentUSB/data/kanban/boards/` may have board-specific backups.
- **Check `state.db`** — `/Volumes/HermesAgent/HermesAgentUSB/data/state.db` or the profile-level `state.db` may contain cached task metadata.

### 5. Prevention (after recovery)

- Ensure the USB drive is safely ejected before disconnecting
- Consider running kanban on the internal SSD (symlink from USB) for write reliability
- Regular `hermes kanban stats` snapshots in BACKLOG.md as a secondary record

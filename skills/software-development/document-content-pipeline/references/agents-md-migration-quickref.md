# Quick Reference: AGENTS.md Migration Checklist

Use when root AGENTS.md references stale directory paths (v3.0 → v4.0 migration).

## Detection (30 seconds)

```bash
# 1. Root structure
ls -d /Users/zaryu/Desktop/Niumination/*/
# If DOX says Production/ but reality says apps/ → stale

# 2. DOX Chain claims
for claim in "brain/AGENTS.md" "apps/Niu-LKH/AGENTS.md" "services/niu-cast/AGENTS.md" "agents/orchestrator/AGENTS.md"; do
  test -f "/Users/zaryu/Desktop/Niumination/$claim" && echo "✅ $claim" || echo "❌ $claim"
done

# 3. App/services contents
for dir in apps services sites desktop agents labs sandbox; do
  echo "$dir/: $(ls -d \"/Users/zaryu/Desktop/Niumination/$dir/\"*/ 2>/dev/null | wc -l | tr -d ' ') projects"
done
```

## Common v3.0 → v4.0 Path Changes

| Old (v3.0) | New (v4.0) |
|------------|------------|
| `Production/<proj>/` | `apps/<proj>/` |
| `projects/<proj>/` | → `services/` or `sites/` or `desktop/` or `labs/` or `sandbox/` |
| `PI/` | `vault/` |
| `rekap/` | `dotfiles/` |
| `Niumination/` (in root) | `agents/profile/` |

## Fix Sequence

1. **Bump DOX Version** in header (3.0 → 4.0)
2. **Replace** entire Directory Structure tree — not individual lines
3. **Fix** every path in Project Catalog tables (20+ rows)
4. **Fix** DOX Chain list — remove nonexistent, add missing
5. **Update** Quick Links + Footer
6. **Commit separately** — reversible if migration causes issues

See also: `references/agents-md-migration-case-study.md` for full walkthrough with 15+ corrections and detection methodology.

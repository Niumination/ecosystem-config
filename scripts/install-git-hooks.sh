#!/bin/sh
# install-git-hooks.sh — Install pre-commit hooks ke seluruh repo Niumination
# Menggunakan git init (re-initialize) untuk meng-copy hooks dari templateDir
#
# Usage: ./scripts/install-git-hooks.sh [--dry-run]

set -e

ROOT="/Users/zaryu/Desktop/Niumination"
DRY_RUN=false

if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
    echo "🏁 DRY-RUN mode — no changes will be made"
fi

echo "🔍 Scanning for git repositories under $ROOT..."
echo ""

# Cari semua .git directories (max depth 4 untuk mencakup root + projects/)
repos=$(find "$ROOT" -name ".git" -maxdepth 4 -type d 2>/dev/null | sort)

count=0
fail=0

for gitdir in $repos; do
    repo="$(dirname "$gitdir")"
    relpath="${repo#$ROOT/}"
    if [ "$relpath" = "$repo" ]; then
        relpath="(root)"
    fi

    count=$((count + 1))

    if $DRY_RUN; then
        echo "   [$count] Would install hook: $relpath"
    else
        echo "   [$count] Installing hook: $relpath"
        (cd "$repo" && git init >/dev/null 2>&1)
        ec=$?
        if [ $ec -eq 0 ]; then
            # Verify hook was installed
            if [ -f "$gitdir/../.git/hooks/pre-commit" ]; then
                echo "     ✅ pre-commit hook active"
            else
                echo "     ⚠️  hook not found after init — checking templateDir"
                fail=$((fail + 1))
            fi
        else
            echo "     ❌ git init failed (exit $ec)"
            fail=$((fail + 1))
        fi
    fi
done

echo ""
echo "═══════════════════════════════════════"
echo "   Total repos scanned: $count"
echo "   Failures: $fail"
echo "═══════════════════════════════════════"

if $DRY_RUN; then
    echo "   Jalankan tanpa --dry-run untuk instalasi sesungguhnya."
fi

exit $fail

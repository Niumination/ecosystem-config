#!/usr/bin/env python3
"""Scan text for glyphs from scripts that don't belong in Indonesian/English docs.

Niumination docs are Indonesian or English. A CJK, Cyrillic, Hangul, or Greek
word sitting inside an Indonesian sentence is a generation artifact — it reads as
corruption and hides meaning. Commit 787548f shipped four of those on 2026-10-02.

Deliberately narrow. Emoji (✅ ⚠️ ⏳ ❌ ⭐), box-drawing (├── ── └──), typography
(— – ’ “ ” …), math (−20 dB, ≤, ×), and Latin diacritics (é ü ç ñ) are all
intentional in this corpus and must NOT be reported. An earlier version of this
script flagged all of them and produced 52 false positives on clean files.

Usage:
    python3 scripts/scan-stray-glyphs.py                # scan staged files
    python3 scripts/scan-stray-glyphs.py <path> [...]   # scan given paths
Exit 0 clean, 1 when something needs a human look.
"""
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

# Scripts that cannot legitimately appear in an Indonesian/English technical doc.
# Keyed on the FIRST WORD of the Unicode character name, because stdlib has no
# script property. For a CJK ideograph the name is "CJK UNIFIED IDEOGRAPH-XXXX",
# for a Cyrillic letter it is "CYRILLIC SMALL LETTER KA" — both expose the script
# as the leading token.
#
# GREEK is deliberately absent. Letters like π, Ω, α, β are used as math symbols
# and appear in level/loudness/geometry notes in this corpus, so flagging the
# whole script produced false positives. The artifacts actually observed
# (commit 787548f, 2026-10-02) were CJK, Cyrillic, and Hangul only.
FOREIGN_SCRIPTS = frozenset({
    "CJK", "HIRAGANA", "KATAKANA", "HANGUL", "CYRILLIC",
    "ARABIC", "HEBREW", "THAI", "DEVANAGARI", "BENGALI", "TAMIL",
    "TELUGU", "KANNADA", "MALAYALAM", "GUJARATI", "GURMUKHI",
    "ARMENIAN", "GEORGIAN", "ETHIOPIC", "CHEROKEE", "MONGOLIAN",
    "TIBETAN", "MYANMAR", "KHMER", "LAO", "SINHALA",
})

# Documentation ABOUT text corruption has to quote the corruption. A skill
# cataloguing bad-output shapes, or the scanner's own test, would otherwise be
# permanently un-committable. Fenced code blocks and these two files are exempt.
FENCE = re.compile(r"^\s*(?:```|~~~)")
SELF_TEST_PATH = "test-scan-stray-glyphs.py"


def _in_fenced_block(lines, index):
    """True when lines[index] sits inside a ``` or ~~~ fenced block."""
    openers = 0
    for i in range(index):
        if FENCE.match(lines[i]):
            openers += 1
    return openers % 2 == 1

BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz",
              ".tgz", ".mp4", ".mov", ".woff", ".woff2", ".ttf",
              ".mp3", ".m4a", ".webm", ".enc", ".jks", ".sqlite", ".db",
              ".pyc", ".mo"}


def foreign_glyphs(path: Path):
    """Return (lineno, char, script, context) for glyphs in a foreign script."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    lines = text.splitlines()
    hits = []
    for lineno, line in enumerate(lines, 1):
        if _in_fenced_block(lines, lineno - 1):
            continue
        for ch in set(line):
            if ord(ch) < 128:
                continue
            try:
                script = unicodedata.name(ch).split()[0].upper()
            except (ValueError, IndexError):
                continue
            if script in FOREIGN_SCRIPTS:
                hits.append((lineno, ch, script, line.strip()[:100]))
    return hits


def staged_files():
    out = subprocess.run(
        ["git", "-c", "core.quotepath=false", "diff", "--cached",
         "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True).stdout
    return [Path(f) for f in out.splitlines() if f.strip()]


def main(argv):
    files = ([Path(a) for a in argv[1:]] if len(argv) > 1 else staged_files())
    files = [f for f in files if f.is_file() and f.suffix.lower() not in BINARY_EXT]
    # The scanner's own test must quote the corruption it detects, so exempt it.
    files = [f for f in files if f.name != SELF_TEST_PATH]
    if not files:
        print("[stray-glyphs] tidak ada berkas teks untuk dipindai")
        return 0

    total = 0
    for f in files:
        for lineno, ch, script, ctx in foreign_glyphs(f):
            total += 1
            print(f"  {f}:{lineno}  U+{ord(ch):04X}  {script}  {unicodedata.name(ch, '?')}")
            print(f"      {ctx}")

    if total:
        print(f"\n[stray-glyphs] {total} glif dari skrip asing di {len(files)} berkas.")
        print("              Perbaiki di tempatnya, lalu jalankan ulang.")
        return 1

    print(f"[stray-glyphs] bersih — {len(files)} berkas, 0 glif skrip asing")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
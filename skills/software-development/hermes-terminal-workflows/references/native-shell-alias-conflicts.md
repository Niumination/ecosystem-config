# Native-shell aliases break text utilities

On this machine `grep` and `cat` are shell functions/aliases that dispatch to a
ripgrep-backed implementation. Tooling that assumes GNU semantics then fails in
ways that look like the data is malformed rather than the tool being different.

## Recognisable symptoms

- `grep -P ...` / `grep -iE ...` → error about an unknown *encoding*, naming the
  pattern as if it were a charset. This is the tell: the `-E` or `-P` flag is
  being parsed as a different option entirely.
- `cat -A file` → "illegal option". The `-A` flag (`--show-all`) is not supported.
- `cat file` on a large file → behaves like a search tool, not a pager.

## What to do

- Prefer `rg` directly over `grep` — it is what is actually being invoked, so
  there is no translation layer to disagree with.
- For byte/line-ending inspection, use Python rather than fighting flags:

```python
import unicodedata
for i, line in enumerate(open(path).read().splitlines(), 1):
    odd = [c for c in line if ord(c) > 0x2100 and c not in '\u2014\u2192']
    if odd:
        print(i, [(c, unicodedata.name(c, '?')) for c in odd])
```

  Codepoint-plus-name is strictly better for spotting stray characters in
  prose: it names the character, so you can tell an intentional emoji from a
  mangled CJK glyph without guessing from a hex value.

- To run the real binaries, invoke them by absolute path, not by name.

## Pasting output from a piped command

`cmd | head -5` reports the **last** command's exit status, so a failing `cmd`
shows as success. When a probe's output looks wrong, re-run it unpiped and read
the actual exit code before concluding anything about the data.

## Structured extraction beats whitespace parsing

A fixed-column table that looks parseable with `awk '{print $1, $2}'` is not:
column widths shift with content length. When a command's table output needs
parsing, use Python and parse on the header, or use the tool's own JSON output
flag. Do not build a regex around column positions.

## Cache invalidation when redirecting to a file

Redirecting a command to a file and reading it in the same session can return a
stale or empty file depending on how the shell handles the write. If a captured
file comes back with zero bytes while the command exits 0, capture the output
through the tool interface instead of a shell redirect.

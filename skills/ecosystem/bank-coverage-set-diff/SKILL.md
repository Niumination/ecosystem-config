---
name: bank-coverage-set-diff
description: Use when a scanner total may not cover every skill.
version: 1.0.0
---

# Bank coverage set-diff

A scanner that prints "N skills scanned" proves only that it iterated something.
Coverage is proven by a symmetric difference between the keys the scanner
discovers and the keys the manifest declares. Run this before quoting any
finding count.

## The check

```python
import importlib.util, json
from pathlib import Path

spec = importlib.util.spec_from_file_location("sa", "scripts/skill-audit.py")
sa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sa)

bank = Path("skills")
found = {f"{d}/{n}" for d, n, _p in sa.iter_skills(bank)}
declared = set(json.load(open(bank / "manifest.json"))["skills"])

print("declared:", len(declared), "discovered:", len(found))
print("missing from scanner:", sorted(declared - found))
print("extra on disk:", sorted(found - declared))
```

`discovered == declared` with empty symmetric difference is the gate. Anything
else means the scanner's counts are lower bounds, not totals, and its findings
list is incomplete.

Load the scanner with `importlib.util.spec_from_file_location`, not
`sys.path.insert` plus `import <name>`: the audit script's filename is
hyphenated, so the plain import never resolves and the failure looks like a
missing module rather than a naming problem.

## Reading the diff to locate the bug

- `missing` clustered under one top-level domain → the scanner is keying on a
  directory object's name instead of its path relative to the bank root, so all
  nested subtrees collapse to the same key. Use
  `parent.relative_to(bank).as_posix()`.
- `missing` entries that are bare names with no domain → `SKILL.md` sits
  directly in a top-level domain folder, which a two-level walk never yields.
  Check the domain folder itself and emit a bare-name key.
- `extra` entries under a dotted directory → a retired-skill folder is being
  scanned. Skip dotted directories (`.git`, `.archive`) rather than hardcoding
  names; a hardcoded plain name like `archive` will swallow a live domain if one
  is ever added.

After fixing, re-run until the diff is empty, then re-count findings. A count
recomputed on a fixed walker is the only count worth reporting.

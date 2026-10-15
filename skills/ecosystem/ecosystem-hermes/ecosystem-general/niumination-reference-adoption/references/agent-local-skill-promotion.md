# Promoting Hermes-local skills into the Niumination bank

Use when the bank and an agent target have diverged because skills were created in `~/.hermes/skills/` and never backported.

## 1. Classify (never promote bundled or hub skills)

```python
import json, pathlib
HSK = pathlib.Path.home() / ".hermes/skills"
bundled = {l.split(":")[0] for l in (HSK/'.bundled_manifest').read_text().splitlines() if l.strip()}
hub = set((json.loads((HSK/'.hub/lock.json').read_text()).get('installed') or {}))
bank = {p.parent.name for p in pathlib.Path.home().joinpath('Desktop/Niumination/skills').glob('*/*/SKILL.md')}
hermes = {p.parent.name: p for p in list(HSK.glob('*/SKILL.md')) + list(HSK.glob('*/*/SKILL.md'))}
candidates = {s: p for s, p in hermes.items() if s not in bundled | hub | bank}
```

`.bundled_manifest` is `name:md5` per line; `.hub/lock.json` is `{"version":…, "installed": {…}}`. Both are flat text/JSON — no CLI needed. Skip anything under `.archive/`.

## 2. Back up, then verify the backup by NAME

```bash
tar czf /tmp/hermes-skills-backup-$(date +%Y%m%d-%H%M).tgz <relative dirs...>
# verify coverage by name, not by count — a count can look plausible while a dir is missing
tar tzf <tarball> | grep "SKILL.md$" | awk -F/ '{print $(NF-1)}' | sort > /tmp/tar-names.txt
comm -23 /tmp/expected-names.txt /tmp/tar-names.txt   # empty = complete
```

## 3. Copy into the bank

- Preserve the existing domain directory when Hermes already groups the skill (`ecosystem/`, `software-development/`, `devops/`, `github/`, `productivity/`, `research/`).
- Top-level Hermes skills need an explicit domain mapping; pick the closest bank domain and stay consistent (`niu-9router-maintain` → `ecosystem`, `macos-launchd-services`/`env-doctor` → `devops`, refactor/branch skills → `software-development`).
- Copy the whole folder (`SKILL.md` + `references/` + `scripts/` + `templates/`), excluding `.DS_Store`.
- A bank dir that exists but has lost its `SKILL.md` (leftover `references/` only) is a broken entry: `up-eco` will not count it, but the manifest may still be "consistent" because it was regenerated after the loss. Restore the file from the target copy during promotion.

## 4. Update `skills/INDEX.md`

Rows are `| **name** | ✅ Aktif | Source | Ukuran KB | Deskripsi |`; insert after the last data row of the matching `## Domain: X` section, and add a new section for a new domain. Keep the file's own counters in step (status line, Hermes-integration line, `## Ringkasan` totals).

`up-eco.sh` counts rows with `^\| \*\*[^*]+\*\* \| ✅ Aktif \|`. Looser patterns break: `^\| \*\*[a-z]` misses digit-leading names (`9router-model-mapping`) and `[A-Za-z0-9]` also matches the `| **Total** |` row in Ringkasan. Either mistake produces a false "INDEX.md mismatch" warning — fix the regex, not the skill name.

## 5. Verify

```bash
python3 scripts/skill-manifest.py            # regenerate after any add
grep -cE '^\| \*\*[^*]+\*\* \| ✅ Aktif \|' skills/INDEX.md
ls skills/*/*/SKILL.md | wc -l               # must equal the INDEX count
bash skills/sync-to-agents.sh
bash scripts/up-eco.sh                       # evidence: folder/dir, manifest, INDEX all ✅
```

## Pitfalls

- **Bank-wins sync does not delete.** After promotion the old target path (e.g. a top-level `~/.hermes/skills/<skill>/`) still exists alongside the new `~/.hermes/skills/<domain>/<skill>/`, so the Hermes catalog lists the same skill twice. Remove the superseded copy (backup first) after the sync — `sync-to-agents.sh` has no `--delete` by design.
- **`rsync -u` silently froze divergence.** With `-u`, a target file whose mtime is newer wins forever: verify reports `[ubah]` but sync can never repair it. The bank is the source of truth — copy without `-u`; if a target-side edit is genuinely better, backport it into the bank before syncing.
- **Counts are not proof.** Verify bulk copies with an explicit name-set diff (`comm`), and re-list from a fresh process after deleting anything remote-side.

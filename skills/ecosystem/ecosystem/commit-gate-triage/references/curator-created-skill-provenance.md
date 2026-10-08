# Curator-Created Skill Provenance

Load when a skill you did not create appears in the bank, or when a commit is refused because a
skill exists on disk but not in the manifest.

## An unexpected skill is NOT automatically another agent's work

The autonomous curator creates skills from the CURRENT session's transcript. A skill that appears
mid-session — with a plausible name, matching the work you just did — is usually the curator
extracting your own findings, not a foreign thread writing into your tree.

Getting this wrong is expensive: treating it as foreign makes you refuse to touch it, leave your
work uncommitted, and escalate a non-problem to the user.

## Check the ledger before concluding anything

```bash
grep '<skill-name>' ~/.hermes/skills/.curator_ledger.jsonl | tail -3
```

Each entry carries `actor`, `action`, and `evidence.session_id`. Compare that session id with the
session you are in:

- **same session id** → curator extracted it from your own work. It is yours to extend, and the
  manifest gate is legitimately stale.
- **different session id** → genuinely foreign. Do not touch it; report and let its owner commit.
- **no entry** → hand-written or installed by other means. Treat as user-owned.

Cross-check the timestamp: ledger entries are UTC, so convert before comparing against file mtimes
(a local-time mtime will look hours later than the ledger line).

## Resolving the manifest gate once provenance is confirmed

A gate that refuses a commit because a skill is on disk but absent from the manifest is telling
you the manifest is stale — not that the commit is wrong. Regenerate, verify, then commit:

```bash
python3 scripts/skill-manifest.py            # rewrites manifest.json
python3 scripts/skill-manifest.py --check    # must report 0 mismatch
bash skills/sync-to-agents.sh                # sync bank -> target + registry
```

The skill count in the regenerated manifest should equal the previous count plus the number of new
skills. A count that jumps by more than you added means something else landed at the same time —
investigate before committing.

## If you edit a skill and the bank does not change

Skill edits land in the **sync target** (`~/.hermes/skills/`) first. The bank is the source of
truth. Promote explicitly, then confirm by hash:

```bash
cp <target-file> <bank-file>
shasum -a 256 <target-file> <bank-file>   # hashes must match
python3 scripts/skill-manifest.py         # then regenerate + --check
```

Committing without the promotion silently loses the edit on the next sync, which overwrites the
target from the bank.

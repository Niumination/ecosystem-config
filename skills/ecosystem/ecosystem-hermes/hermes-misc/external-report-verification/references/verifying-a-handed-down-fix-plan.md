# Verifying a handed-down fix plan

A report arrives naming a root cause and prescribing a fix. Verifying the *claim* is only half
the job — the claim can be true while the prescribed fix does nothing. Check all three layers
before executing anything.

## The three checks

| Layer | Question | Fails when |
|---|---|---|
| **Mechanism** | Does the code path the report blames actually exist in the target branch? | The blamed file/function was never present there, so it cannot be the cause |
| **Remedy** | Does the prescribed action change the failing behaviour? | The merge/cherry-pick/patch lands code that has no bearing on the symptom |
| **Executability** | Can the prescribed action even run? | The file imports a package absent from the target branch |

A plan that passes only the first check must not be executed. Report the gap instead.

## Worked shape

Symptom: a generated shim pointed at a Python the project excluded.

```bash
# 1. MECHANISM — is the blamed machinery in the branch we would change?
git grep -c "stage_launcher" main              # 0 → main never had it
#    The shim was written while a DIFFERENT branch was checked out.
#    Reflog dates it: shim mtime sits between the other branch's last commit
#    and the checkout back to main.
git reflog --date=iso | head -20

# 2. REMEDY — would the proposed action change the symptom?
git show upstream/main:<file> | grep -c "version_info"   # 0 → no guard anywhere
#    The newest upstream still picks the same unwanted interpreter, so merging
#    cannot fix it. The proposed remedy is inert.

# 3. EXECUTABILITY — does the file survive on its own in the target?
git show <branch>:<file> | grep -n "^from <pkg>"        # imports a package
git ls-tree main -- <pkg>/ | wc -l                      # 0 → package absent
#    A single-file cherry-pick raises ModuleNotFoundError on import.
```

## Rules

- **A branch's copy of a file can be OLDER than upstream's.** Compare blob sizes and diff
  against upstream before treating "it exists in the other branch" as "it is the good
  version": `git cat-file -s <blob>` on both, then `git diff upstream/main <branch> -- <file>`.
- **A branch that was rebased days ago is stale by however much upstream moved since.**
  `git rev-list --count <base>..upstream/main` before proposing a merge; a merge of a stale
  branch imports stale code, including files upstream has since fixed.
- **Do not execute a plan whose remedy is inert, even when its premise is true.** State which
  of the three checks failed and what would actually change the behaviour.
- **Prefer the fix at the layer that owns the bug.** If the unwanted value comes from a
  generated facts/state file read without validation, the durable fix is validation or the
  source of the value — not moving the reader to another branch.
- **Say what is unverified.** If a diagnostic command is blocked, report the finding as
  provisional and name the one command that would settle it, rather than picking a fix by
  elimination.

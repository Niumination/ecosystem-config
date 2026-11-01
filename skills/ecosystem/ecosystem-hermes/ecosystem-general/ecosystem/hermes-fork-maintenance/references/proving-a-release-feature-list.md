# Proving a Release's Feature List

A release note is marketing copy, not an inventory. Before telling the owner "vX ships feature
Y", show the code that implements Y — the note names a behaviour, not a file.

## Procedure

1. **Resolve the checkout to the tag under discussion.** A source tree on `main` is *ahead* of
   the tag and can contain work the release never shipped.
   ```bash
   git show <tag>:path/to/file.py | grep -c '<symbol>'
   git ls-tree -r <tag> --name-only | grep -iE '<feature-slug>'
   ```
   Use the tag ref, never the working tree, when answering "does this release have it".

2. **Grep the SOURCE tree, not the docs tree.** Release notes live in a website/ directory; a
   hit there proves nothing about the code.

3. **Resolve a greppable symbol per feature.** Map each note item to its mechanism name:

   | Feature in the note | Symbol to grep |
   |---|---|
   | pluggable delegation backends | `register_delegation_provider`, `delegation_backends.py` |
   | plugin slash commands pick an option | `ask_choice` |
   | sign-in flow change | `auth_device_flow.py` |
   | local LLM one-click | `llama_app_latest` in `pm/packages.py` |
   | desktop framework bump | the pinned version in `package.json` |
   | backend moved out of core | whether the file still exists in core |

4. **Prefer the commit log when you need the whole window.** One query lists every change:
   ```bash
   git log --oneline <prev-tag>..<tag> --no-merges --grep='<feature>' -i
   git log --oneline <prev-tag>..<tag> --no-merges | head -40
   ```
   Match each grep to a release-note item. A `--grep` that returns nothing usually means the
   note's vocabulary differs from the commit vocabulary — widen the term, do not conclude the
   feature is absent.

5. **Read the tag's pinned version when the claim is a version number.** A note saying
   "Electron 44" is disproved by the checkout pinning a different minor — but only at that tag,
   and only if the file is not installed elsewhere (a workspace dep list can pin a floor, not the
   runtime).

6. **Report a table: verified (commit + file) / unverified (note claim only).** Never state
   "feature X exists" from a release note alone, and never state "X is absent" from one failed
   grep either — an unverified row is an *uncertainty*, not a negative finding.

## Pitfalls

- **A "0 references" grep is not proof of absence.** Feature notes and code use different
  vocabulary; a wider grep of the commit log often finds the feature under a name you did not try.
- **Checking the working tree instead of the tag conflates released and unreleased work.**
- **A version claim in the note can be off by a patch release.** Pin the exact version and quote
  it; "bumped to 44" is not "44.9.3".
- **A backend "moved out of core" is proven only by the file's absence in core at that tag**, not
  by the note's wording.

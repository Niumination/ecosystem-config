# Offsite destination: staging, fetching and authenticating

The backup has to leave the machine, and the destination has a size budget and an auth model that both bite in
predictable ways. Decide these while planning.

## Large archives: release assets, not commits

Committing a 100 MB+ archive on a schedule grows the repo by that amount per commit (a daily cadence crosses the
host's soft ceiling within weeks, and undoing it needs a history rewrite). Split the storage by lifetime:

- **In git**: scripts, `README`/`MANIFEST`, path maps, patch files, checksums — small, reviewable, versioned.
- **As release assets**: the archive and its parts, dated/tagged per backup. Assets can be replaced or deleted
  without touching commit history — that is the whole point of choosing them.
- **Encrypted credential blobs** (kilobyte-scale ciphertext) may live in git next to the scripts that use them.

Consequence to state in the plan: the restore **must** fetch assets (`gh release download <tag> --repo … --dir …`),
and the verifier has to check that it did.

```bash
gh release create <tag> --repo <owner>/<repo> --title '<label>' --notes '<what changed>'
gh release upload  <tag> part-* --repo <owner>/<repo>
gh release download <tag> --repo <owner>/<repo> --dir /tmp/fetch
cat /tmp/fetch/part-* > backup.zip && shasum -a 256 backup.zip   # compare with the recorded checksum
gh release upload  <tag> part-aa --repo <owner>/<repo> --clobber  # replaces a same-named asset
gh release delete-asset <tag> <name> --repo <owner>/<repo> --yes
```

- **A repo needs at least one commit before it can hold a release** — `gh release create` on an empty repo fails with
  *"Repository is empty"*. Order: create repo → commit the scripts and `README` → tag and upload assets.
- **Always pass `--repo`.** Omitting it makes `gh` act on the repo of the current working directory; a script that
  derives the target implicitly will one day write to whatever directory it was started from.
- Verify the round trip once per destination (upload → download into a clean dir → reassemble → compare checksums),
  and keep the checksum in the repo so a restore can prove the fetch.

## Authentication in unattended contexts

The CLI login that works by hand is not available to a background job:

- **Keychain-backed logins are unreachable from non-interactive processes.** A sync job started by a scheduler gets
  `HTTP 401` on operations that succeed in the terminal; the job must carry a token in its environment instead.
- **The environment token must actually be valid.** A stale token exported into the environment overrides a healthy
  keychain login and breaks every call for that process (and for any tool that sources the same env file). Probe it
  before trusting it: `gh api user --jq .login` must return a name, not an error payload.
- Debug order for a 401 that appears in scripts but not in the terminal: run it with the env token unset, then with it
  set, and compare. That distinguishes "permissions" from "bad credential" in one step.
- Treat credential validation as its own check in the drill — presence and validity are different findings, and only
  the second one decides whether the restore is actually usable.

## Hygiene at the destination

- Fetch into a temporary directory, reassemble, verify checksums, and delete the plaintext working copy once
  coverage is confirmed: the archive holds `.env` and DB dumps, so every stray copy is another place the secret
  lives.
- Keep test artefacts out of real repos: rehearse destination behaviour against a throwaway private repo, then delete
  it, and verify the cleanup (`releases` count back to 0, tag gone).

# Ignored-Path Sweep — what only exists on this machine

Purpose: enumerate the files a `git clone` will not bring back, then cut that list down to the ones that
actually hurt. Run it per repo; the Hermes home is not a repo, so there classify its top-level entries the
same way.

## 1. Enumerate

```bash
git -C <repo> ls-files --others --ignored --exclude-standard   # ignored + untracked, repo-relative
```

No manual `.gitignore` parsing, no walking `.git`. Combine with `git -C <repo> status --porcelain` when you
need to separate "never tracked" from "locally modified".

## 2. Filter the rebuildable majority

Expect tens of thousands of hits and only a handful of real candidates. Drop anything matching dependencies,
build output, caches and generated schemas:

```
node_modules/  .venv/  venv/  site-packages/  __pycache__/  *.pyc  *.egg-info/
.next/  dist/  build/  out/  .build/  target/  vendor/  Pods/  .gradle/  .dart_tool/
.angular/  .svelte-kit/  .nuxt/  .output/  .expo/  .turbo/  .cache/  .parcel-cache/
coverage/  .pytest_cache/  .mypy_cache/  .ruff_cache/  .swiftpm/  DerivedData/
.terraform/  .serverless/  gen/schemas/  tsconfig.tsbuildinfo  next-env.d.ts
.DS_Store  logs/  *.log  tmp/
```

Also drop third-party checkouts and extracted archives (an extracted APK tree, an upstream clone, a browser
profile cache): they are re-downloadable, and where a browser profile does hold value it is the logged-in
session, which a re-login restores.

## 3. Triage the survivors, in this order

1. **Irreplaceable small binaries** — signing keystores (`.jks`, `.keystore`), certificates (`.pem`, `.cer`),
   licence / provisioning files. Kilobyte-scale, absent from every repo, unrecreatable: losing an app
   signing key permanently blocks publishing updates for that app, including updates to builds already live.
2. **Credentials and deploy wiring** — `.env`, `.env.local`, `.env.production`, `.vercel/project.json`,
   `.vercel/env`, provider config, token files, `vault/`-style trees.
3. **State and authored data** — project DBs (`*.db`, `*.sqlite`), `data/*.json`, swarm/kanban state, raw
   source datasets, locally authored skill or plugin trees that have no upstream.
4. **Everything else** — decide explicitly per file. Never sweep it in "just in case"; an unexamined
   allowlist entry is how a backup silently becomes a second copy of a secret.

## 4. Size, before promising coverage

- Git hosts reject large single files (GitHub: 100 MB hard, 50 MB warning) and degrade on multi-GB repos.
  A 200 MB+ state DB must be compressed and split, or reduced to the tables that matter — a SQLite file of
  structured records usually compresses several-fold. Decide this while planning, not on the first push.
- Ask of each candidate: *if this vanished, would I rebuild it or mourn it?* Mostly-cache data belongs in
  the reduce step, not the backup.
- For a home-directory layer, expect roughly half the total to be rebuildable — language servers and tool
  binaries are re-downloaded, logs and caches regenerate, checkpoint and profile trees cost convenience,
  not capability. Report the surviving size, not the directory size.

## 5. Output

A flat **allowlist of paths** for the sync script, grouped by destination (config repo vs encrypted data
repo) — never a blind `git add -A`. Each entry must be defensible as "cannot be rebuilt", which is the
parent skill's rule 6.

## 6. Package the allowlist, then verify it end to end

Archive and encrypt the allowlist, then prove it by restoring into a clean directory and comparing **per-file
hashes against the live sources** — presence is not evidence.

```bash
tar -czf l2.tar.gz -C staging .                      # staging holds the allowlist with its structure
openssl enc -aes-256-cbc -pbkdf2 -salt -in l2.tar.gz -out l2.tar.gz.enc -pass pass:<...>
openssl enc -d -aes-256-cbc -pbkdf2 -in l2.tar.gz.enc -out l2.dec -pass pass:<...>
mkdir -p restore && tar -xzf l2.dec -C restore
sqlite3 restore/eco/<project>.db "PRAGMA integrity_check;"    # per restored DB
```

Measured on the reference host — allowlist of 28 objects / **73 files / 72 MB**:

| Stage | Size |
|---|---|
| staged sources | 72 MB |
| `tar.gz` | 19 MB |
| encrypted | 19 MB |
| verification | 73/73 hashes match, 0 differing, 0 missing; both project DBs `ok` |

What that changes in the plan:

- **L2 usually lands far below the git file limits** (credentials and datasets are text, and CSV/ZIP compress ~4x),
  so it can ship as an ordinary encrypted file in the private repo. Reserve archives-with-split — or release assets —
  for the measured item that actually exceeds the threshold, rather than assuming the whole plan needs them.
- **`tar` carries the permission bits.** A `0600` SSH key and a `0700` secrets directory keep their modes through
  archive → encrypt → restore, so the credential layer needs no extra `chmod` recipe. Confirm it in the restore
  output anyway — a mode that silently widened is a leak.
- **Print skipped entries.** An allowlist entry that no longer exists is dropped with a visible note; silently
  skipping it lets a renamed or moved credential disappear from coverage without anyone noticing.
- **Delete the staging tree and the decrypted intermediate** once hashes match — they are plaintext copies of every
  secret in the allowlist, and the encrypted archive already proved itself.

## 7. Re-run cadence

Re-run when a project gains a service, a deployment target, or a binary/signing asset — those are the moments
new ignored-but-critical files appear. Diff the fresh list against the stored allowlist; every new entry is
a deliberate decision, not an automatic addition.

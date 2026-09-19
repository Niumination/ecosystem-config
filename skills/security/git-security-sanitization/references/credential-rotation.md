# Credential Rotation — replace a secret without leaving a live alias

Use when a key, password, or token must be replaced (suspected exposure, age, an open security item in the backlog). The failure this prevents: rotating the variable everyone looks at while an alias the code still reads keeps the old value one unset-variable away from coming back.

## 1. Read the auth code before touching the console

- Find **every** variable the check reads, including `||` chains and dev defaults: `password = process.env.ADMIN_PASSWORD || process.env.ADMIN_TOKEN`. **Every alias is a rotation target.** Rotating `A` while `B` still holds the old value leaves a latent bypass that reactivates the moment `A` is unset — and no test you run today will fail.
- Confirm the control **fails closed**: no configured secret must mean "reject all", never "fall back to a default". Read the guard, do not assume it.
- Probe the live endpoint with an obvious default (`Bearer admin`, `Bearer test`, `admin/admin`) and expect 401/403. Do this *before* recommending rotation: it finds a real hole, or clears a suspected one, in one request — the difference between "rotate to be tidy" and "rotate because this is open". Do not print the response body of an admin endpoint; it can carry user data.

## 2. Rotate

- Generate the new value **on the owner's machine**, never through the chat: `openssl rand -hex 32`. The value must not enter your context, a doc, a commit message, or a log — the owner pastes it straight into the provider.
- Update the provider's environment variables for **every** environment (production and preview), then rotate or delete the alias variables from step 1.
- **Serverless env changes need a new deployment.** Editing an env var does not change the running deployment; say this explicitly or the owner will conclude the rotation failed and revert it.

## 3. Verify with a pair, not a single check

- Old value → expect 401/403.
- New value → expect 200.
- Record *who* ran the check. If the owner ran it, the project doc line says so ("checked by owner"), not "verified".

## 4. Housekeeping that outlives the rotation

- Store the new value only in the vault/env store; remove the old one from every place it was echoed (host secrets, `.env`, CI variables, docs).
- Delete dead credential entries from your own env store when a stored URL is rejected (rotated password, retired project). A dead credential that still looks authoritative costs the next session a debugging detour — it can hide the fact that you simply cannot verify that provider from here.

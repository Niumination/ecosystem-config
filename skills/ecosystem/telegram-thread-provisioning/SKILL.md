---
name: telegram-thread-provisioning
description: "Use when adding a Telegram persona thread to a forum group."
tags: [telegram, hermes, config, persona, thread, model-mapping, ecosystem, niumination]
last_updated: "2026-09-25"
version: 1.0.0
---

# Telegram Thread Provisioning

Adding a NEW persona thread to a Telegram forum group (Mission Control) — a distinct job from
*tuning* an existing thread's model. Tuning = change `channel_overrides`. Provisioning = the
group, the topic, the persona, the model, the skills, and the proof it works.

## Trigger
User asks for a new thread/topic/persona in a Telegram forum group, or a new specialized worker
(for a job role, a project, a client). Also fires when a thread exists but is not routed yet.

## Order of operations

### Step 1 — Read the LIVE config, never the skill's tables
`~/.hermes/config.yaml` is the only source of truth. Model-mapping tables inside skills go stale
routinely and will name dead models. Read `platforms.telegram` → `channel_overrides`,
`extra.channel_prompts`, `extra.channel_skill_bindings` and see what is actually running.

```bash
grep -n -A 25 "channel_overrides" ~/.hermes/config.yaml
```

Also check what the gateway really routed (this is truth, config is intent):

```bash
python3 - <<'PY'
import sqlite3, pathlib
con = sqlite3.connect(str(pathlib.Path.home()/'.hermes'/'state.db'))
for (skey,) in con.execute(
    "select session_key from gateway_routing where session_key like '%telegram:group:%'"):
    print(skey)
PY
```

`gateway_routing` lives in `state.db` (SQLite), NOT in a `sessions.json`. Columns are
`scope, session_key, entry_json, updated_at` — the metadata JSON is in `entry_json`, and the
thread id is the last `:`-segment of `session_key`. Selecting a column named `key` fails.

### Step 2 — The topic must be created by the human, in Telegram
An agent can call `create_forum_topic`, but it has no bot token to authenticate that call, and
the bot API has no "list topics" call. So the human creates the topic (`/newtopic`) and **sends
one message in it**. Until that message lands, no routing row exists and any config you write
for the thread id is unfalsifiable — you cannot confirm you targeted the right id.

Do not ask the user to "give me the thread id" as the first step. Ask them to create the topic and
post once; then read the id yourself from `gateway_routing`. That way the id is verified, not
transcribed.

### Step 3 — Vet the model THROUGH the gateway, not with raw curl
A provider section may have no `key_env`, in which case the gateway holds a built-in key that is
absent from `~/.hermes/.env`. Raw curl then returns 401 and you will wrongly conclude the model is
dead. Probe the way the thread will actually call it:

```bash
cd ~/src/hermes-agent && source .venv/bin/activate
hermes chat -q "Balas persis: OK" -m "<model>" --provider <provider> -Q
```

Reading the result:
- **200 with content** → model alive.
- **404 "no longer free"** → the `:free` slug was retired upstream. Real, and it catches models
  that other threads are still pointing at. Do not adopt it; do not report it as "provider down".
- **401 from curl but 200 here** → missing `key_env` in config, not a broken model.

**`:free` slugs are not durable.** A slug can be free today and paywalled tomorrow with no config
change on our side. Re-probe before assigning a model to a new thread, and when you find a dead
one, report every thread that still references it.

**Then stress-test before adopting.** One 200 hides rate limits. Send ~8 quick requests with
representative, multi-word content **in the language the thread will work in** — relays filter on
content, so ASCII "ping" probes pass where real traffic gets blocked. Only adopt a candidate that
survives the burst.

Pick the model by evidence, not by "it looks good": reuse a model another live thread already
runs (proven in production for this exact load) unless the thread's work needs something else.
Never assign a combo/auto slug as a thread's primary — auto may resolve to a provider with no
credentials and fail the whole thread.

### Step 4 — Write the persona prompt in the house shape
Mirror the blocks existing threads use, in the same order: role sentence + scope, evidence rule
("read the file before concluding, cite the source"), output format, escalation path, then the
standing document and credential rules. Consistency across threads is the point — a thread whose
prompt invents its own conventions will drift from the rest.

Keep it under ~2 KB. It is prepended to every turn in that thread forever.

### Step 5 — Apply the config change by script, never by hand
`config.yaml` is large and shared. Hand-editing risks a malformed file that breaks every platform.
Use `scripts/install-thread.py`: it takes a backup, mutates all three fields, re-parses to
confirm, and rolls the backup back on any failure.

```bash
THREAD_ID=<id> python3 scripts/install-thread.py
```

Two shape facts it handles, both of which bite when hand-editing:
- `channel_skill_bindings` is a **JSON string**, not a YAML mapping. Adding a thread means
  `json.loads` → insert key → `json.dumps`, or you corrupt the value.
- `channel_prompts` values contain single quotes (`'{...'}` JSON examples) — naive shell quoting
  mangles them. Python string handling avoids the whole class of bug.

Script location: keep it inside this skill, not in the ecosystem repo — Hermes config is machine
state, not a repo deliverable. Backups land in `~/.hermes/config-backups/`.

### Step 6 — Prove it end to end, in this order
1. Config parses and the new keys are present.
2. Gateway has a routing row for the thread id.
3. The model answers through the gateway (same command as step 3).
4. A message actually arrives: `hermes send --to "telegram:<chat_id>:<thread_id>" "<konfirmasi>"`.
5. Ask the thread who it is, and confirm the persona is in force — not merely that the transport
   works.
6. Session message count climbs in `state.db` → proof a real turn used it.

An unverified thread is indistinguishable from a misconfigured one until it takes a message.

### Step 7 — Record it
Write the thread to the ecosystem registry row (persona, model, provider, skill bindings, why that
model) and commit. An unrecorded thread is invisible to the next session and gets re-diagnosed
from scratch.

## Pitfalls

- **Never trust a model-mapping table inside a skill.** Those tables age into fiction; config
  drifts from them silently and nothing warns you. Read `config.yaml` first, every time.
- **A 401 from a hand-rolled curl is not a dead model.** The gateway may hold a key the shell does
  not have. Probe through `hermes chat` so the test matches production's call path.
- **Probing with "ping"/"OK" is not a real probe.** Content filters let trivial ASCII through and
  block real multi-word non-English traffic. Stress-test with the thread's actual language.
- **A configured thread is not a working thread.** Config writes succeed against an id that has
  never received a message, and the failure surfaces only when the user talks to it. Verify the
  routing row, then send.
- **Do not `git add -f` config or token files into the ecosystem repo.** Shared machine state,
  git-ignored secrets, same rule that keeps real tokens out of public history.
- **Read the group's own thread status tooling before hardcoding thread lists.** Status scripts
  that enumerate a fixed set of ids go stale the moment a thread is added, and the new thread
  looks inactive forever. Derive the list from data, never from a literal.

## Support files
- `scripts/install-thread.py` — backup + mutate + validate + rollback installer for one thread.
- `references/config-shape.md` — exact YAML/JSON shapes, the probes, and the verification queries.

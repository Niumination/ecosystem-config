# Editing per-thread channel prompts (Hermes gateway)

Use when a standing rule must reach Telegram threads — "semua thread MC harus ..." — for example after a
doc-path regression caused by a thread inventing its own folder. Each thread's prompt lives in
`platforms.telegram.extra.channel_prompts`: a `{ "<thread_id>": "<prompt>" }` map in
`~/.hermes/config.yaml`. **There is no shared prompt.** A rule that must apply to every thread has to be
appended to every entry — and to the repo's root `AGENTS.md` as well, because the prompt governs the
thread while `AGENTS.md` governs every agent, including ones outside Telegram.

## Procedure

1. Back up before touching config:
   ```bash
   cp ~/.hermes/config.yaml /tmp/config.yaml.bak-$(date +%Y%m%d-%H%M%S)
   ```
2. Read → modify → write back inside one script, passing the JSON as a single argv element. Shell
   quoting of one large JSON string is where this goes wrong; an argv list has no quoting layer.

   **Read the value from `config.yaml`, not from `hermes config get`.** Once any previous `config set`
   has run, `config get` prints a **Python-dict repr** (`'1': 'Kamu adalah …`), so `json.loads` raises
   `JSONDecodeError` and the edit script aborts before writing anything. Parsing the file is the path
   that works in every state:
   ```python
   KEY = "platforms.telegram.extra.channel_prompts"
   d = yaml.safe_load(open("/Users/zaryu/.hermes/config.yaml", encoding="utf-8"))
   prompts = d["platforms"]["telegram"]["extra"]["channel_prompts"]
   prompts = json.loads(prompts) if isinstance(prompts, str) else prompts   # {thread_id: prompt}
   MARKER = "ATURAN DOKUMEN"                       # idempotency guard
   for k, v in prompts.items():
       if MARKER not in v:
           prompts[k] = v.rstrip() + RULE
   subprocess.run(["hermes", "config", "set", KEY, json.dumps(prompts, ensure_ascii=False)])
   ```
3. Verify three ways — a `config set` exit code is not evidence the agent will read it.
   - Parse the file with the Hermes venv python and assert the marker in **every** entry:
     ```python
     d = yaml.safe_load(open("/Users/zaryu/.hermes/config.yaml"))
     v = d["platforms"]["telegram"]["extra"]["channel_prompts"]
     v = json.loads(v) if isinstance(v, str) else v
     assert all(MARKER in p for p in v.values())
     ```
   - Call the production resolver — the same function the gateway uses, so this is the strongest check
     short of sending a live message:
     ```python
     from hermes_cli.config import load_config_readonly
     from gateway.platforms.base import resolve_channel_prompt
     cfg = load_config_readonly()
     resolve_channel_prompt(cfg["platforms"]["telegram"]["extra"], "1")
     ```
   - Re-read `hermes config get` only as a hint: after a `set` it can print a **Python-dict repr**, not
     JSON, so `json.loads` on it fails — cosmetic, not a broken config.
4. No restart needed. The config cache is keyed on `(st_mtime_ns, st_size)` (`hermes_cli/config.py`), so
   editing the file invalidates the merged cache and the prompt is live on the next turn. Do not restart
   the gateway to "apply" a prompt edit.
5. Report the diff: which threads gained the text, characters before/after, and the added sentence
   verbatim — the user should be able to read the rule that now governs those threads.

## Pitfalls

- **A rule added to the DM/default prompt does nothing for threads.** Resolve per thread id; the five
  Mission Control threads are `1, 802, 803, 804, 1172`.
- **Topics inherit the parent prompt.** `resolve_channel_prompt` falls back to `parent_id`, so a topic
  with no prompt of its own still picks up its group's — a stale parent rule reaches every topic under it.
- **Grep lies about long prompts.** YAML line folding can wrap the phrase being searched, so raw
  `grep -c` undercounts. Count on the parsed value.
- **State the doc layout in the prompt itself.** A thread with no layout rule invents paths; the failure
  mode is recreating a folder that was deliberately deleted. Name the target (`docs/reports/` for
  reports/plans/strategy, `docs/registry/` for live registries, `docs/references/` for archives) and say
  explicitly not to create new folders under `docs/`.
- **Keep the value one YAML scalar.** `channel_prompts` is stored as a single JSON string; keep it
  single-line with `ensure_ascii=False`.

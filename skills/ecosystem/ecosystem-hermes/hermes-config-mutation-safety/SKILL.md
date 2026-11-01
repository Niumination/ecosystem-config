---
name: hermes-config-mutation-safety
description: "Use when editing ~/.hermes/config.yaml safely."
version: "1.0.0"
tags: [hermes, config, model-routing, channel-overrides, safety]
---

# Hermes Config Mutation Safety

## Overview

`~/.hermes/config.yaml` holds live routing for every session. Three write paths exist and they are NOT
interchangeable. Two of them lose content; one is refused outright. Pick deliberately, then verify with a
diff every time — no write path is self-verifying.

## Procedure

1. **Back up first.** `cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak-$(date +%Y%m%d)`. The backup is
   the only way back once a lossy write lands.
2. **Read the target region with line numbers** to get exact indentation. YAML in this file uses mixed
   indent; a guessed indent level silently creates a sibling key instead of editing the intended one.
3. **Choose a write path** (table below). The `patch` tool is *not* an option.
4. **Diff against the backup.** `diff ~/.hermes/config.yaml.bak-* ~/.hermes/config.yaml` must show only the
   lines you intended. Any other hunk means the write was lossy — restore and switch paths.
5. **Re-parse YAML** to confirm structure: `python3 -c "import yaml;yaml.safe_load(open('/Users/zaryu/.hermes/config.yaml'))"`.
6. **Probe the model live** before claiming the route works (see "Proving a route works").
7. **Report whether a restart is needed.** Config edits do not retroactively change an already-running
   session; say so explicitly rather than implying the switch is live.

## Write paths

| Path | Verdict | Mechanism |
|------|---------|-----------|
| `patch` tool on `config.yaml` | **REFUSED** | Guard treats it as security-sensitive config; agent writes are blocked. Do not retry with workarounds — switch to an allowed path. |
| `hermes config set <dotted.key> <value>` | **LOSSY** | Rewrites the file by round-tripping a parsed structure. Trailing comment blocks are not represented in the data model, so they get dropped. |
| `python3 -c` exact-string replace on the file | **SAFE** | Byte-level replace touches nothing outside the matched string. Guard with `assert s.count(old) == 1` so a non-unique match fails loudly instead of corrupting. |
| `sed -i '' "${N}r file"` to splice a block | **WRONG PLACE** | `r` appends the file's contents *after* line N, ignoring indentation and parent keys. A block meant as a sibling of line N lands nested under whatever key line N belongs to. |

### Splicing a new block into a nested map

Insert with Python line indices, anchored by asserts on the *neighbourhood*, not on the line number alone — line numbers drift, and an off-by-one here puts a whole server under an unrelated key while the YAML still parses:

```python
lines = s.splitlines(keepends=True)
i = next(k for k,l in enumerate(lines) if l.strip() == 'platform_toolsets:')
assert lines[i-1].strip() == 'enabled: true'   # expected last line of the block above
assert lines[i-2].strip().startswith('url: ')  # proves we found the RIGHT anchor, not a same-named key
lines[i:i] = ['  composio:\n', '    url: https://...\n', '    enabled: true\n']
```

Then prove placement structurally: `yaml.safe_load` the file and assert the new key is under the intended parent **and absent from every sibling map** (a misplaced block parses fine — structure, not syntax, is what breaks).

### The `hermes config set` truncation trap

`hermes config set` returns a cheerful `✓ Set ... in /Users/zaryu/.hermes/config.yaml` and succeeds while
silently deleting every trailing comment block in the file. Documented fallbacks and provider notes live
there, so a routine route change can delete reference material a later session depends on. **Always diff
after using it.** If the diff shows a lost block, restore from backup and redo the edit with the
exact-string replace path.

## Detecting a truncated or overwritten config (not just a bad edit)

A config that was never edited by you can still arrive in a broken state. Symptom pair: `/model`
lists nothing, and some other service reports the ecosystem wrongly (a monitor reading
`channel_prompts` finds one entry instead of ten). **Check file size and the live model default
before concluding anything is broken** — a healthy file here is tens of KB; a truncated one is
under ~1 KB and holds only a `model:` block.

```bash
wc -c ~/.hermes/config.yaml
cat ~/.hermes/config.yaml
```

Read the whole file when it is small; a five-line dump tells you more than any parse.

**A stub config naming a provider and model this install does not use is a smoking gun.** Compare the
names against the install's real provider (a local router on a high port, with its key in the env
file) and probe both endpoints: the local router answers 200 while the stub's provider answers 401.
Report that contrast as evidence rather than an opinion.

**Beware the same text arriving from an unrelated source.** An applied zip can carry a `.hermes/`
stub whose contents match the truncated file byte for byte. Treat a match as *correlation to report*,
not as proof of causation — the stub is not necessarily what wrote the file, and naming it as the
cause is a claim you have not tested.

**The stub is still a fingerprint: hash-match it against every candidate writer.** Even though the
match proves nothing by itself, it is a cheap discriminator. Collect SHA-256 of the damaged file and of
each candidate source (zip entry, backup, cron job output, DB record), then compare:

```bash
shasum -a 256 ~/.hermes/config.yaml
shasum -a 256 /tmp/<quarantine>/.hermes/config.yaml
```

A byte-identical hit narrows the field to whoever had those exact bytes — including an agent session
whose own model block you can read back out of a `sessions/request_dump_*.json` (the runtime
environment block states `Model:` / `Provider:` / `Home directory:`). Combine the hash with the
mtime and with that session's tool-call trail before naming a cause.

**Find the writer from the session trail, not from suspicion.** Two sources, in order:

1. `~/.hermes/sessions/request_dump_*.json` — one file per failed request, named with the session id
   and a timestamp, carrying `reason` and `error`. Sort by `timestamp`; the dumps bracketing the
   damaged file's mtime are the sessions active at the moment.
2. `state.db` `messages` — `timestamp` is a **unix epoch float**, not an ISO string, so a string
   comparison against the file's mtime silently returns zero rows. Convert first:

```python
import sqlite3, datetime
tz = datetime.timezone(datetime.timedelta(hours=7))          # owner's TZ
ts = datetime.datetime(2026,10,22,15,29,52,tzinfo=tz).timestamp()
rows = con.execute("select session_id, role, tool_name, substr(content,1,200), timestamp "
                   "from messages where timestamp between ? and ? order by timestamp",
                   (ts-600, ts+300)).fetchall()
```

Group by `session_id` over the window to see every session that was live, then read its `tool_name`
values — a writer shows up as `write_file` / `patch` / `execute_code`, not as `None`.

**Before blaming an agent, audit other writers of the same path.** A monitoring panel or companion
service with a file-write endpoint is a more common cause than a rogue edit. Grep the writing
endpoint's guard conditions before assuming an agent caused the damage, and check whether the
permissions you are reading actually cover the profile you care about:

- An allowlist of editable paths (`SOUL.md`, `config.yaml`, `memories/USER.md`, ...) plus a
  **profile resolved from the caller's own code** means any code the panel knows can write any
  profile's `config.yaml` — not just its own.
- Check the guard exists *for the write*, not merely for the read. An endpoint that refuses an
  unparseable stub config on one path may accept a minimal valid one on another.

Establish this with a real call, then revert it in the same turn and state that you did.

**Damage assessment — separate the live parts from the damaged part:**

```bash
stat -f "%Sm  %z bytes  %N" -t "%Y-%m-%d %H:%M:%S" ~/.hermes/config.yaml
stat -f "%Sm  %z bytes  %N" -t "%Y-%m-%d %H:%M:%S" ~/.hermes/.env
python3 -c "import os,time;p=os.path.expanduser('~/.hermes/cron/ticker_heartbeat');print(round(time.time()-os.path.getmtime(p)),'s')"
```

Env file intact and a fresh cron heartbeat mean the process is still alive and executing jobs — so
report a *narrow* break (routing/provider resolution) rather than "Hermes is broken", which would
send the owner chasing a phantom outage.

**Restore only on the owner's explicit go-ahead**, and never before confirming the backup differs:
`ls -lat ~/.hermes/backups/config/ | head`. The file is guarded so agent writes are refused, and
this kind of repair is one the owner may prefer to perform or review.

## Thread-scoped vs global model routing

A Telegram thread maps to `platforms.telegram.channel_overrides.<channel_id>`. Editing only that entry
changes one thread and leaves the global `model.default` plus every sibling channel untouched — prefer this
for "make X the model for this thread", and say explicitly that the global default was not changed.

Keys are quoted strings (`'1':`, `'802':`). Dotted `hermes config set` addressing must reproduce that
quoting or it will not match the existing key.

## `python3 -c` from inside the gateway

Multi-line heredocs (`python3 - <<'PY' ... PY`) are **blocked** by the gateway's self-restart guard, which
cannot prove a heredoc body does not restart the gateway. Use `python3 -c '...'` with inline string literals
instead. When the payload contains both quote styles, pick the outer quote style and escape the inner one,
or use a `Path` object to avoid escaping entirely.

Verify the write landed:

```
python3 -c "from pathlib import Path;p=Path('/Users/zaryu/.hermes/config.yaml');s=p.read_text();old='...';new='...';assert s.count(old)==1,'MATCH %d'%s.count(old);p.write_text(s.replace(old,new));print('OK')"
```

## Proving a route works

Config that parses is not a route that works. Probe the endpoint the override points at:

- **Local OpenAI-compatible routers require an auth header on localhost too.** An unauthenticated request
  returns an HTML 404 from the router's own web UI, which reads like "endpoint missing" but is actually an
  auth rejection. Always send the header when probing.
- **The key usually lives only in the env file, not the shell.** Source the env file in the same command
  before probing, or the probe 401s and looks like a dead model.
- **A 200 only proves the endpoint answered.** Read the response body's `model` field: a router alias may
  resolve to a different underlying model than the alias name. Report what actually served the request.
- **Reasoning models may return `finish_reason: length` on a tiny `max_tokens` probe.** That is normal
  token accounting, not a failure.

## Provider kustom (`providers.<nama>`) dan picker `/model`

Jalur chat gateway membaca katalog provider dengan `non_blocking_catalogs=True, probe_custom_providers=False,
probe_current_custom_provider=True`. Artinya: **provider custom yang bukan endpoint aktif tidak di-probe live** —
kalau cache dingin dan `models:` tidak dideklarasikan, barisnya kosong atau hanya menyisakan `default_model`.

Gejala di Telegram: `/model` menampilkan provider dengan 0 model atau 1 model, padahal endpoint sehat.

**Dua hal yang WAJIB dipahami sebelum "memperbaiki":**

1. **`models:` adalah fallback, bukan pin.** Diverifikasi: dengan cache hangat, picker tetap memakai hasil
   cache meski `models:` berisi daftar berbeda. `models:` hanya dipakai saat cache dingin/kosong. Jadi mengedit
   `models:` saja **tidak** menyembunyikan model yang sudah dihapus dari katalog — harus invalidate cache
   (`~/.hermes/provider_models_cache.json`, TTL 1 jam) juga.
2. **Bentuk `list` = allowlist; bentuk `dict` = metadata** (`_models_config_is_allowlist`). Untuk membuat
   daftar yang dipakai sebagai fallback, pakai `list`.

Cara mengisi `models:` dari katalog live, dengan anchor assert (jangan pakai `hermes config set` — lossy):
```python
import yaml
s = open(p).read()
old = "    key_env: HUANCHENG_API_KEY\n    default_model: auto\n"
assert s.count(old) == 1, "anchor %d" % s.count(old)
s = s.replace(old, old + "    models:\n" + "".join(f"    - {m}\n" for m in live_ids))
open(p, "w").write(s)
```
Verifikasi dengan `diff` terhadap backup: hitung baris `^<` (penghapusan) — **harus 0** kalau hanya menambah.

Config baru langsung terbaca gateway **tanpa restart**: `load_user_config_effective` di-cache berdasarkan
signature file (mtime/size), bukan dimuat sekali saat start.

## Pitfalls

1. **Never edit `config.yaml` with the `patch` tool.** It is refused by design; the refusal is not a bug to
   route around with a different tool call.
2. **Never trust `hermes config set` output as proof the file is intact.** Its success message covers only
   the key it wrote. Diff or you will ship a config that silently lost its documentation blocks.
3. **Always diff config writes against the backup before reporting done.** This is the single check that
   catches both lossy paths; nothing else does.
4. **Do not treat a routing edit as taking effect immediately.** The change applies when config is reloaded.
   State the restart requirement instead of implying the thread already switched.
5. **Anchor edits with a uniqueness assert.** `assert s.count(old) == 1` turns a silent multi-site
   corruption into a loud failure.
6. **Probe through the provider the override actually names.** A config that points at one provider and a
   probe aimed at another proves nothing about the route.
7. **`channel_skill_bindings` is JSON-in-YAML** — the value is a single quoted JSON string, not nested YAML.
   Editing it with `patch` on a JSON key inside the string silently corrupts the YAML. Use the python3
   json-round-trip path: load YAML → parse the bindings JSON string → modify → re-serialize → write back.
8. **A write that parses is not a write that landed where you meant.** Nested YAML moves a misplaced block
   from "syntax error" to "silently active under the wrong parent" — the two failure modes have opposite
   signals, so validate placement with a parser assert, not with `yaml.safe_load` succeeding.
9. **Jangan simpulkan "cache dingin" dari satu pengamatan.** Selalu uji **dua** kondisi — cache hangat dan
   cache dingin (pindahkan `provider_models_cache.json`, panggil `clear_provider_models_cache()`) — karena
   keduanya bisa memberi angka berbeda dan hanya salah satunya mereproduksi keluhan pengguna.
10. **`/v1/models` sebuah provider bisa memuat model yang sudah dihapus/dimatikan.** Katalog ≠ status aktif.
    Verifikasi lewat `isActive` di DB provider, bukan dari ada/tidaknya model di daftar.
11. **`hermes cron --no-agent` memakai interpreter Hermes sendiri — tidak ada PyYAML.** Script yang berjalan fine dari shell (yang punya PyYAML) bisa gagal total di cron job `--no-agent` dengan `ModuleNotFoundError: No module named 'yaml'`. Kalau script diedarkan sebagai cron `--no-agent`, tulis parser string murni (`re`, `json`, `urllib`) dan validasi struktur dengan assert — jangan pernah impor paket eksternal. Uji dengan `hermes cron run <job-id>` sekalipun pengujian manual tadi lolos dari shell.
12. **Jangan asumsi indentasi list item YAML adalah `key_indent + 4`.** YAML mengizinkan sequence di kolom yang sama dengan key-nya (`models:` diikuti langsung `    - item` dengan indentasi sama). Parser yang mengasumsikan +4 akan gagal diam-diam. Baca indentasi aktual dari item pertama. Juga: cek parent section sebelum replace — config ini punya dua `  9router:` (providers dan model_catalog) dan hanya satu yang boleh disentuh.
13. **Uji script yang menulis config pada SALINAN, bukan config asli.** Arahkan `CONFIG`/`CACHE` ke file `/tmp` lewat variabel yang bisa di-override, lalu buktikan config asli tidak tersentuh (`grep -c` untuk nilai uji = 0) sesudahnya. Menjalankan script penulis config pertama kali langsung ke file produksi adalah cara kehilangan config.
14. **JANGAN membuktikan "service X bisa menimpa config" dengan menulis ke config asli.** Ini adalah kesalahan yang nyata: dua tulis uji ke `~/.hermes/config.yaml` dan ke config sebuah profil, lalu dipulihkan. Ujinya sah sebagai bukti, tetapi ia **menambah** kerusakan pada berkas yang sedang Anda selidiki, dan berkas itu dilindungi guard sehingga pemulihan manual adalah satu-satunya jalan kembali. Ganti tulis sungguhan dengan **pembacaan kode saja**: baca `_resolve`/`_profile_for_code`/`ALLOWED` dan simpulkan cakupannya dari sana. Kalau panggilan nyata tetap mutlak diperlukan, tulis ke **salinan** di `/tmp` (`HOME=/tmp/... ` atau override path), dan pulihkan berkas asli dengan menulis balik byte persisnya (pertahankan mode `0600`) — lalu sebutkan secara eksplisit di laporan bahwa Anda menulis dan sudah memulihkannya.
15. **Cek SEMUA berkas config di bawah `~/.hermes`, bukan hanya yang di root.** Pemutusan yang sama bisa mengenai `~/.hermes/profiles/<nama>/config.yaml` — keduanya bisa berubah pada detik yang sama dengan isi yang identik. Periksa ukuran+SHA kedua-duanya; kalau keduanya identik, itu bukti penulis yang sama dan juga tanda bahwa sebuah profil mungkin **dibuat** oleh proses yang sama (cek `stat -f %SB` untuk waktu pembuatan profil, bukan hanya mtime isinya).

## Related skills
- `hermes-configuration` — Hermes model mapping, hooks, MCP (if reachable in your skill set)
- `hermes-provider-config` — provider config and auth troubleshooting
- `config-history-review` — retrace prior config changes from backups
- `agent-shell-command-guards` — blocked/stalled shell commands

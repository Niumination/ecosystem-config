#!/usr/bin/env python3
"""Keep Hermes's `models:` list for a provider in sync with its live catalog.

Why this exists (verified 2026-10-11):
  * The `/model` Telegram picker reads provider catalogs cache-only
    (non_blocking_catalogs=True, probe_custom_providers=False), so a cold
    cache plus an undeclared `models:` row shows an empty or 1-model list.
  * `models:` in providers.<name> is a FALLBACK, not a pin: a warm cache
    WINS over it. Editing `models:` alone does nothing to a picker that
    already holds a cache entry.
  * Therefore a change requires BOTH: rewrite `models:` AND drop the
    provider_models_cache.json entry.

Only 9router is synced. `huancheng` is stable and `atria` declares a single
default model; add a PROVIDERS entry when their catalogs start moving.

Anchor-based replacement is used instead of `hermes config set`, which
round-trips the whole file and silently drops trailing comment blocks.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

CONFIG = os.path.expanduser("~/.hermes/config.yaml")
CACHE = os.path.expanduser("~/.hermes/provider_models_cache.json")

# Run under `hermes cron --no-agent`, which uses Hermes's own interpreter: no PyYAML,
# no third-party imports. The file is read, structurally rewritten and checked with
# these two helpers instead.
_ITEM_RE = re.compile(r"^(\s*)- (.*)$")


def _parse_models(lines, section):
    """Return (start_index, end_index_exclusive) of the `models:` list under `providers.<section>`.

    Raises AssertionError when the block is absent or empty, so a malformed config fails
    loudly instead of being silently rewritten.
    """
    hdr = None
    for i, line in enumerate(lines):
        if line.strip() != f"{section}:" or line.lstrip().startswith("#"):
            continue
        if _parent_key(lines, i) in ("providers", ""):
            hdr = i
            break
    if hdr is None:
        raise AssertionError(f"section 'providers.{section}' not found")
    indent = len(lines[hdr]) - len(lines[hdr].lstrip())

    key = " " * (indent + 2) + "models:"
    start = None
    for j in range(hdr + 1, len(lines)):
        if not lines[j].strip():
            continue
        if len(lines[j]) - len(lines[j].lstrip()) <= indent:
            break
        if lines[j] == key:
            start = j
            break
    if start is None:
        raise AssertionError(f"no 'models:' key under {section!r}")

    item_indent = None
    first = None
    last = None
    for k in range(start + 1, len(lines)):
        m = _ITEM_RE.match(lines[k])
        if m:
            if item_indent is None:
                item_indent = len(m.group(1))
            if len(m.group(1)) == item_indent:
                if first is None:
                    first = k
                last = k
            continue
        if not lines[k].strip():
            if first is not None:
                break
            continue
        if len(lines[k]) - len(lines[k].lstrip()) <= indent:
            break
        if first is not None:
            break
    if first is None:
        raise AssertionError(f"empty models list under {section!r}")
    return first, last + 1


def _read_models(path, section):
    with open(path) as fh:
        lines = fh.read().split("\n")
    first, last = _parse_models(lines, section)
    return [m.group(2) for m in map(_ITEM_RE.match, lines[first:last])]


def _replace_models(text, section, new_models):
    """Rewrite the `models:` sequence under `providers.<section>`; nothing else moves."""
    lines = text.split("\n")
    first, last = _parse_models(lines, section)
    item_indent = len(lines[first]) - len(lines[first].lstrip())
    lines[first:last] = [" " * item_indent + "- " + m for m in new_models]
    return "\n".join(lines)


def _check_models_list(path, section, expected_count):
    """Independent re-read: prove the list on disk really holds what we meant to write."""
    got = _read_models(path, section)
    assert len(got) == expected_count, \
        f"{section}: config holds {len(got)} models, expected {expected_count}"
    return got

# section name -> base URL. Extend here when another provider's catalog moves.
PROVIDERS = {
    "9router": "http://127.0.0.1:20128/v1",
}
ENV_KEYS = {"9router": "NINE_ROUTER_API_KEY"}


def api_key(section: str) -> str:
    env_name = ENV_KEYS.get(section, f"{section.upper()}_API_KEY")
    with open(os.path.expanduser("~/.hermes/.env")) as fh:
        for line in fh:
            if line.startswith(env_name + "="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def live_models(base_url: str, key: str) -> list[str]:
    req = urllib.request.Request(f"{base_url}/models",
                                 headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return sorted(m["id"] for m in json.load(resp)["data"])


def stable_live_models(base_url: str, key: str, attempts: int = 3, delay: float = 3.0) -> list[str] | None:
    """Return the catalog only when two consecutive reads agree.

    Measured 2026-10-11: 9router's aggregate catalog flapped 168 <-> 126 within
    seconds (a whole provider drops out when its upstream errors, then returns).
    Writing on a single sample made this job rewrite config on every wobble and
    post a Telegram message each time. Two agreeing reads filter that out; a
    still-moving catalog returns None so the caller can stay silent and let the
    next scheduled run catch the settled value.
    """
    previous = None
    for i in range(attempts):
        try:
            current = live_models(base_url, key)
        except (urllib.error.URLError, OSError, ValueError):
            return None
        if previous is not None and current == previous:
            return current
        previous = current
        if i < attempts - 1:
            time.sleep(delay)
    return None


def _parent_key(lines: list[str], index: int) -> str | None:
    """Name of the mapping that directly contains `lines[index]`, or None at top level."""
    indent = len(lines[index]) - len(lines[index].lstrip())
    for j in range(index - 1, -1, -1):
        line = lines[j]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cur = len(line) - len(line.lstrip())
        if cur < indent and line.rstrip().endswith(":"):
            return line.strip().rstrip(":")
        # An empty parent name means a top-level key, e.g. `providers:` —
        # it has no colon inside the key token, so it never matches above.
        if cur < indent and not line.strip().endswith(":"):
            return ""
    return None




def drop_cache_entries(base_url: str) -> int:
    if not os.path.exists(CACHE):
        return 0
    with open(CACHE) as fh:
        data = json.load(fh)
    doomed = [k for k in data if base_url.split("/v1")[0] in k]
    for k in doomed:
        del data[k]
    with open(CACHE, "w") as fh:
        json.dump(data, fh, indent=2)
    return len(doomed)


def main() -> int:
    if not os.path.exists(CONFIG):
        print(f"ERROR: {CONFIG} not found", file=sys.stderr)
        return 1

    text = open(CONFIG).read()
    notes = []
    changed = 0
    written = {}

    for section, base_url in PROVIDERS.items():
        key = api_key(section)
        if not key:
            print(f"ERROR: {section}: api key not found", file=sys.stderr)
            return 1
        live = stable_live_models(base_url, key)
        if live is None:
            # Catalog still moving (or unreachable): stay silent, do not write.
            # The next scheduled run catches the settled value.
            continue

        declared = _read_models(CONFIG, section)
        if live == declared:
            continue

        text = _replace_models(text, section, live)
        changed += 1
        written[section] = len(live)
        dropped = drop_cache_entries(base_url)
        notes.append(f"{section}: {len(declared)} -> {len(live)} models, "
                     f"cache entries dropped: {dropped}")

    if not changed:
        # Nothing to say: stay silent so a 30-minute job does not post
        # "unchanged" to Telegram 48 times a day.
        return 0

    open(CONFIG, "w").write(text)

    # Verify the bytes on disk against the SAME snapshot that drove the write.
    # Re-fetching the catalog here made the check race a flapping endpoint
    # (9router measured 168 <-> 126 within seconds) and failed a healthy job.
    try:
        for section, expected in written.items():
            got = _check_models_list(CONFIG, section, expected)
            notes.append(f"{section}: verified {len(got)} models on disk")
    except AssertionError as exc:
        print(f"ERROR: verification failed, config may be inconsistent: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"ERROR: config failed to parse after edit: {exc}", file=sys.stderr)
        return 1

    print("; ".join(notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())

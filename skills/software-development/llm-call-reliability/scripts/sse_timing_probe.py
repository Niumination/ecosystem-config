#!/usr/bin/env python3
"""Time SSE events from an LLM-backed endpoint: first token vs total.

Usage:
    python3 sse_timing_probe.py <stream-url> "query one" "query two" ...

Why: a stalled connection (no first token ever arrives) and slow generation
(early first token, long tail) need opposite remedies. Measure before changing
any timeout, retry, or model setting. Point this at the SAME path the real
client uses, so the pipeline under test is the pipeline in production.

Reads: event: status / token / result / error  (data: lines).
Prints per query: verdict, total seconds, seconds to first token, token count,
and the result/error payload.
"""
import json
import sys
import time
import urllib.request


def probe(url: str, query: str, timeout: float = 180.0):
    req = urllib.request.Request(
        url,
        data=json.dumps({"query": query}).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    tokens = 0
    t_first = None
    akhir = ""
    ev = ""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line:
                    continue
                dt = time.time() - t0
                if line.startswith("event:"):
                    ev = line[6:].strip()
                elif line.startswith("data:"):
                    data = line[5:].strip()
                    if ev == "token":
                        tokens += 1
                        if t_first is None:
                            t_first = dt
                    elif ev in ("result", "error"):
                        akhir = f"{ev}|{data}"
    except Exception as e:  # noqa: BLE001 - in a probe every failure IS the data
        akhir = f"EXC|{e}"
    total = round(time.time() - t0, 1)
    return total, (round(t_first, 1) if t_first is not None else None), tokens, akhir


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    url, queries = sys.argv[1], sys.argv[2:]
    ok = 0
    gagal = 0
    for q in queries:
        total, first, tokens, akhir = probe(url, q)
        sukses = akhir.startswith("result")
        if sukses:
            ok += 1
        else:
            gagal += 1
        # first=None with tokens=0 on a failure is the stall signature: nothing ever came.
        print(f"{'OK ' if sukses else 'GAGAL'} {total:>6}s pertama={first} token={tokens} | {akhir[:120]}")
    print(f"\nRINGKASAN: {ok} berhasil, {gagal} gagal dari {len(queries)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

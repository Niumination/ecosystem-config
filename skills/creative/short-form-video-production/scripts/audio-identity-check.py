#!/usr/bin/env python3
"""audio-identity-check.py - does this file/segment carry exactly this audio source?

Answers a different question from scripts/audio-similarity.py. That one asks "how close are these two?".
This one asks "is the audio here the take I intended to mux?" - the gate to run after every mux.

Why correlation and not the other metrics: in a real session timbre could not separate the correct take
from a wrong one (0.0047 vs 0.0022) and median f0 landed between the two candidates (113.6 Hz against
105.3 and 120.3). Lag-aligned waveform correlation separated them immediately: 0.9991 vs 0.1569.

Interpretation:
    ~0.95-1.00  same source (re-encode, gain change, or a lossy mux container)
    ~0.10-0.30  same voice, different take / different text
    ~0.00-0.05  unrelated audio

Usage:
    python3 audio-identity-check.py VIDEO --start 0.5 --dur 4.3 --cand vo3/S1.mp3 --cand vo2/S1.mp3
    python3 audio-identity-check.py a.mp3 --cand b.mp3

--start/--dur select the segment to probe; without them the whole file is used (truncated to the
shortest input). Exit 1 when no candidate reaches --threshold, or when the top two are within --margin
(too close to call). A few seconds per candidate: the lag sweep is sample-wise.

Requires: ffmpeg on PATH, numpy.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

import numpy as np

SR = 16000


def pcm(path: str, start: float | None = None, dur: float | None = None) -> np.ndarray:
    """Decode to mono float32 at SR. Explicit decode so headerless or odd containers cannot slip through."""
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", str(start)]
    if dur is not None:
        cmd += ["-t", str(dur)]
    cmd += ["-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]
    raw = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def best_corr(a: np.ndarray, b: np.ndarray, max_lag_s: float) -> tuple[float, int]:
    """Max Pearson correlation over +/- max_lag (aligns the two starts), and that lag in samples."""
    n = min(len(a), len(b))
    if n < SR:  # need at least a second of overlap to say anything
        return 0.0, 0
    a, b = a[:n], b[:n]
    lag_max = int(max_lag_s * SR)
    best, best_lag = -1.0, 0
    for lag in range(-lag_max, lag_max + 1):
        if lag >= 0:
            x, y = a[lag:], b[: n - lag]
        else:
            x, y = a[: n + lag], b[-lag:]
        if len(x) < SR:
            continue
        x = x - x.mean()
        y = y - y.mean()
        den = float(np.linalg.norm(x) * np.linalg.norm(y))
        if den == 0.0:
            continue
        c = float(np.dot(x, y) / den)
        if c > best:
            best, best_lag = c, lag
    return max(best, 0.0), best_lag


def main() -> int:
    ap = argparse.ArgumentParser(description="Prove which audio source a file/segment carries.")
    ap.add_argument("target", help="file to probe (video or audio)")
    ap.add_argument("--cand", action="append", required=True, help="candidate source, repeatable")
    ap.add_argument("--start", type=float, default=None, help="segment start in the target (s)")
    ap.add_argument("--dur", type=float, default=None, help="segment length in the target (s)")
    ap.add_argument("--max-lag", type=float, default=0.35, help="alignment search window in s")
    ap.add_argument("--threshold", type=float, default=0.5, help="minimum to count as a match")
    ap.add_argument("--margin", type=float, default=0.25, help="top-two gap required to call a winner")
    a = ap.parse_args()

    probe = pcm(a.target, a.start, a.dur)
    if len(probe) < SR:
        print(f"FATAL: segment too short ({len(probe) / SR:.2f}s) - check --start/--dur and that the "
              f"target decoded at all", file=sys.stderr)
        return 1
    if a.start is None and a.dur is None:
        print(f"probe: {a.target} (whole file, {len(probe) / SR:.2f}s)")
    else:
        print(f"probe: {a.target} @ {a.start or 0.0}s + {a.dur or 0.0}s ({len(probe) / SR:.2f}s)")

    rows = []
    for cand in a.cand:
        other = pcm(cand)
        if len(other) < SR:
            print(f"  SKIP {cand}: decoded to {len(other) / SR:.2f}s (0s means the decode produced no "
                  f"audio - the whole comparison would be noise)")
            continue
        c, lag = best_corr(probe, other, a.max_lag)
        rows.append((c, lag, cand))

    if not rows:
        print("FATAL: no candidate could be decoded", file=sys.stderr)
        return 1

    rows.sort(reverse=True)
    print(f"\n{'correlation':>12}  {'lag':>8}  candidate")
    for c, lag, cand in rows:
        print(f"{c:>12.4f}  {lag / SR * 1000:>+7.0f}ms  {cand}")

    top = rows[0]
    if top[0] < a.threshold:
        print(f"\nVERDICT: no match (best {top[0]:.4f} < {a.threshold}) - the probe does not carry any "
              f"of these sources; check for a stale intermediate or a wrong take")
        return 1
    if len(rows) > 1 and (top[0] - rows[1][0]) < a.margin:
        print(f"\nVERDICT: too close to call ({top[0]:.4f} vs {rows[1][0]:.4f}, margin {a.margin}) - "
              f"lengthen the probe or compare single-scene files")
        return 1
    print(f"\nVERDICT: MATCH -> {top[2]} ({top[0]:.4f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

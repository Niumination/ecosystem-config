---
name: measure-before-write
description: "Write figures only from command output, else UNCHECKED."
---

# Measure Before Writing a Number

This ecosystem is built on verification, and numbers are where it usually
breaks. A plausible figure quoted from memory, an earlier session, or a
document written before the facts were known gets treated as established
once it lands in a doc or template — and it is far cheaper to check it now
than to unwind it after a future session builds on it.

Every number in a doc, template, registry, or report must come from a
command's output in this session. If it does not, label it `UNCHECKED` with
the reason rather than rounding it to something plausible.

## The checks

**Duration and timing.** Run it.

**Sample rate, channels, bitrate.**
`ffprobe -show_entries stream=sample_rate,channels -of default=noprint_wrappers=1 <file>`.

**Loudness (LUFS, true peak, LRA).** One-pass loudnorm prints every figure
it computes and uses — read them back instead of assuming the targets
applied:
```
ffmpeg -i vo.mp3 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
```
`input_i` is before, `output_i` is after. `normalization_type` tells you
whether dynamic range was actually forced or only requested.

**CLI flag meaning.** Read `--help` for the installed version, not the
version in the docs or in memory. Short flags are aliases and aliasing
changes between major releases; a flag that meant quality in one release
may mean verbosity in the next, and the parse failure is silent.

**Version and provenance of a file.** `grep -m1 '^version:'` on the file
itself, not the version a summary or report attributes to it.

**Whether a function is reachable.** Count call sites, not text matches.
A grep for `name(` counts the `def name(...)` line too, so a match count of
1 is usually the definition, not a live call. Confirm the containing
function is itself reachable — and know what the entry point is actually
called before grepping for it.

## When the source document disagrees with what you measured

The document is wrong. Fix the sentence that states the bad figure in place
— do not append "UPDATE: actually..." underneath, which leaves both figures
live for a reader who stops at the first one. Note the correction in the
commit message, because the reader who wrote the original number needs to
see it retracted, not quietly replaced.

A number being wrong twice in different directions means the first removal
was also wrong. If you removed a figure because its justification was
absent and you later measure it and it checks out, restore the figure with
the justification attached. The figure was never the problem; the missing
evidence was.

## What not to write

- A figure you inferred because the exact one was inconvenient.
- A figure a source states, when your measurement says otherwise — the
  source loses, and you fix the source.
- A causal explanation for a setting you only observed, not tested. If you
  kept a flag or a value because it worked and never varied it, say the
  reason is `UNCHECKED`. Writing a confident mechanism for an untested
  setting is the cheapest way to make a wrong claim sound validated.
- A number that reads as authoritative when the measurement was conditional.
  If a tool reported a figure as a request rather than an achieved target,
  record both the request and the achieved value.

## Why this matters

The cost of a plausible-looking wrong number is not the number. It is that
it stops being questioned: a future session reads it as settled and builds
on it, and the error is now load-bearing rather than cosmetic. Measuring
costs seconds and produces a figure that survives contact with reality.

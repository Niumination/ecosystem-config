---
name: short-form-video-production
description: "Make ready-to-post vertical video (Reels) at zero cost."
version: 1.4.0
author: Hermes (curator)
tags: [creative, video, reels, short-form, hyperframes, ffmpeg, tts, free-tier, content]
platforms: [macos]
---

# Short-Form Video Production (9:16, zero cost)

Pipeline for turning an idea into a **ready-to-post vertical video** using only local, free tooling:
HyperFrames (HTML/CSS/JS → MP4) + ffmpeg + local TTS. No stock footage, no licensed music, no paid
render cloud, no subscription schedulers.

Runtime-side basics of HyperFrames (init, preview, block catalog) live in the ecosystem skill
`hyperframes`; free-tier channel limits live in `references/free-toolchain-verification.md` here.
This skill carries the production loop, the design corrections, and the verification gates.

## Non-negotiables

- **Work outside the ecosystem repo.** Scaffold in `~/Downloads/<project>/`. A video project inside
  `~/Desktop/Niumination/` breaks the 15-folder structure and has been rejected before. Final MP4 is
  copied out; the render project stays outside.
- **Total cost must be Rp 0.** Every added dependency must be free (local binary, vendored OSS lib,
  free TTS endpoint). If a step would need a paid asset, drop the step and note it, don't silently add cost.
- **Any number or claim shown on screen must be verified the same day** from the ecosystem itself
  (counts, HTTP 200s, registry entries) or from the official source page. A wrong number on a public
  post is the worst failure mode here.
- **Point the call-to-action at something reachable today, and verify it before it goes on screen.** Confirm
  the target responds (a public repo: HTTP 200 from the host API, not just a local clone). When a project's
  own site does not resolve yet, the CTA names the repo that *is* public and the caption says it is coming —
  presenting an unshipped surface as live is the same class of error as a wrong number.
- **Deliverable lands in the owner's output folder** (`~/Movies/Posting - Instagram/`), named
  `<date>-reels-NN-<slug>.mp4`; the package (script, caption, hashtags, repro commands, verification)
  is written to `docs/reports/` in the ecosystem repo — never to a new folder under `docs/`.
- **Never ship a render you have not looked at.** Frame inspection is a gate, not a nicety
  (see step 5). A plain-HTML render with no timeline and no layout work was previously rejected outright.
- **Fix a quality complaint at its own level: engine first, text second.** When a take sounds worse than
  the reference, research the synthesizer landscape and agree the target with the owner before writing any
  text layer. Layering normalization onto a mid-tier engine makes the take worse, not better, and every
  rule then has to be unwound. State the intended target (what "good" means here, judged by the owner's
  ear) before implementing anything. Generalise it: when the owner flags quality, the first deliverable is a
  researched direction — references, a named target, the real options compared — not a patch. Prefer
  removing a layer over adding one. A round that answers "this is worse" by adding rules, a dictionary, or
  another transform reads as going in circles even while every test is green, because the tests measure the
  layer and the owner measures the result.

- **Choose the concept, format, and hook from current performance data before authoring anything.** What
  formats are working now, what a hook has to achieve in the first three seconds, and what makes a piece
  *shareable* are inputs to the script, not afterthoughts. See `references/content-strategy-and-hooks.md`.
  Research sources outside the ecosystem as well as inside it — an idea list drawn only from our own repos
  is a catalogue, not a strategy.

## Pipeline

### 1. Scaffold outside the repo

```bash
mkdir -p ~/Downloads/niu-konten && cd ~/Downloads/niu-konten
npx --no-install hyperframes init reels-001 --example blank
```

`init` can stall on npm/network chatter **after** it has already written the project files. Check the
project directory on disk before re-running; if `index.html`, `hyperframes.json`, `meta.json` exist,
just continue. Use `npx --no-install hyperframes <cmd>` everywhere so npx never tries to fetch.

### 2. Vendor the animation library (no CDN at render time)

```bash
cd ~/Downloads/niu-konten/reels-001 && mkdir -p assets
curl -sS -L -o assets/gsap.min.js https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js
```

Reference it locally (`<script src="./assets/gsap.min.js">`). HyperFrames forbids network fetches in
compositions, and a CDN tag makes renders fail or silently lose all animation when the network is flaky.

### 3. Author the composition

Start from `templates/reels-9x16-composition.html` (known-good: inner-wrapper pattern, hard kills,
vendored GSAP, brand bar, progress bar). Structure that works:

- root `<div id="root" data-composition-id="<id>" data-start="0" data-duration="<sec>"
  data-width="1080" data-height="1920" data-fps="30">`
- one `<section class="clip" data-start data-duration>` per scene, **each containing a single
  `<div class="inner" id="sNin">` that owns all layout**
- one paused master timeline registered as `window.__timelines["<composition-id>"]`
- supported animated props only: `opacity, x, y, scale, scaleX, scaleY, rotation, width, height, visibility`
  (no color/clip-path tweens)
- 6 scenes × 5–8 s ≈ 35–40 s is the sweet spot: hook → problem → proof → public value → how it works → CTA

### 4. Lint — and fix exits correctly

```bash
npx --no-install hyperframes lint --verbose
```

Exit tweens are the one recurring failure. The framework owns visibility of `.clip` elements, so an
`opacity` fade on the clip itself is flagged `gsap_exit_missing_hard_kill`. Fix it the intended way:

```js
tl.to("#s1in",  { opacity: 0, duration: 0.4 }, 4.6);   // tween the inner wrapper
tl.set("#s1in", { opacity: 0 }, 5.0);                  // hard kill, at the next scene's clip start
```

Zero errors before rendering. Warnings must be read, not ignored.

### 5. Draft render, then MANDATORY frame QA

```bash
npx --no-install hyperframes render --resolution=portrait --fps=30 --quality=draft \
  -o "$PWD/../reels-001-draft.mp4"
```

Draft is ~2× faster than `--quality=high` (≈1m15s vs ≈2m for 38 s / 1140 frames) — iterate on draft,
render final once. Then extract scene midpoints, build a contact sheet, and **look at it**:

```bash
scripts/reels-qa.sh ~/Downloads/niu-konten/reels-001-draft.mp4
```

The script prints ffprobe facts, extracts frames, tiles them into sheets, and reports audio levels.
Inspect the sheets with the vision tool and judge: text legible, nothing clipped, no unintended overlap,
**no large dead space**. Fix the composition and re-render the draft until the sheets look good.

### 6. Final render + free voice-over + mux

```bash
npx --no-install hyperframes render --resolution=portrait --fps=30 --quality=high \
  -o ~/Downloads/niu-konten/reels-001-final-silent.mp4
```

Narration quality is decided by the **engine first**, then by the script pass and per-scene delivery
settings — text work cannot lift a mid-tier synthesizer, and normalizing text for an engine that never
needed it makes the take worse (short, uniform, chopped fragments). Pick the engine before writing any
normalization, and read `references/voiceover-delivery.md` before synthesizing anything — section 0 covers
engine selection and hosted LLM TTS, section 0c how to prove a rule is needed. The minimum bar is:

1. **Humanize the VO script first** (skill `ghost`): short standalone sentences, spoken register, varied
   rhythm, every number and claim unchanged. TTS speaks exactly what is written — a flat script stays
   flat in any voice.
2. **Send the script AS WRITTEN — spell nothing by hand.** Do not spell digits as words, do not expand
   acronyms into letters, do not strip symbols, and do not carry the `<en>…</en>` span trick over. An
   LLM-based engine reads numbers, dates, acronyms and mixed Indonesian–English natively; the pre-spelled
   form is what makes a take sound chopped. The spell-out layer in reference section 2 is
   **classic-endpoint only** — apply it when the engine is edge-tts, and only the rules reference
   section 0c proves that engine actually needs.
3. **Direction goes in the prompt, never in the text.** Supply audio profile / scene / performance /
   context, open with a synthesize-speech preamble, and put the spoken lines under `#### TRANSCRIPT` —
   without the preamble and the delimiter the model reads the direction aloud. Audio tags stay in English
   even for an Indonesian script, sit exactly where the change should land, and must never be adjacent to
   each other. The ecosystem engine implementing all of this is the skill `creative/gemini-vo-narration`
   (`scripts/gemini_vo.py`, presets `narator`/`pengumuman`/`edukasi`/`story`, voices
   `algenib`/`charon`/`sadaltager`); its ladder is hosted LLM TTS → edge-tts (per-scene rate/pitch table in
   reference section 3) → the owner's own recording.
4. **One request per video, not per scene.** The hosted free tier counts requests per model per day, so a
   per-scene loop burns the budget for nothing; send the whole script and recover the scene split from the
   audio. Recover it from the **energy profile, not `silencedetect`**: cut the audio into 50 ms frames, take
   the median dB, mark frames below `median-18 dB`, keep runs ≥0.5 s, then choose the five gaps that best
   match the boundaries predicted by each scene's share of the script's characters — taking the combination
   whose midpoints are monotonic and whose total error is smallest. Report the residual: a good fit lands
   under ~1 s and its picks are the longest gaps, which are the ones the `[short pause]` tags created. Drive
   the composition from those numbers (`data-start`/`data-duration`) so the visuals follow the voice rather
   than the voice being nudged to fit a guessed timeline.
5. **Audition before producing**: render the *same* script with several candidates at identical settings,
   include a no-direction control, and send the owner one comparison file with spoken markers. Their ear is
   the verdict on quality — and a take that is *correct* can still be *unnatural*, so a clean pronunciation
   check is never evidence that the delivery is good. The approved voices are already locked (`algenib`,
   `charon`, `sadaltager`, kept for variation between pieces) — vary among them instead of re-running an
   audition from scratch every time.
6. **The quality ceiling is the owner reading it themselves** — offer the per-scene recording kit
   (script, filenames, mux that adapts scene length) before calling a synthesized take final.

Using the Hermes `text_to_speech` tool with `provider="edge"` (free; `id-ID-ArdiNeural` in this
environment) is the fallback path — it accepts only a global speed, so per-scene rate/pitch needs the CLI.
Keep each line shorter than its scene window — measure first:

```bash
for f in vo/vo*.ogg; do printf '%s ' "$f"; ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"; done
```

Place each line with `adelay` (scene start + ~0.5 s), mix with `amix=normalize=0`, normalise to −16 LUFS,
then mux without re-encoding video:

```bash
ffmpeg -y -i vo/vo1.ogg -i vo/vo2.ogg -i vo/vo3.ogg -filter_complex \
"[0:a]adelay=600|600[a0];[1:a]adelay=5600|5600[a1];[2:a]adelay=11600|11600[a2];\
[a0][a1][a2]amix=inputs=3:normalize=0:dropout_transition=0[mix];[mix]loudnorm=I=-16:TP=-1.5:LRA=11[out]" \
-map "[out]" -t <total-sec> -ar 48000 -ac 2 vo_mix.wav
ffmpeg -y -i reels-001-final-silent.mp4 -i vo_mix.wav -c:v copy -c:a aac -b:a 192k -shortest reels-001-final.mp4
```

### 7. Verify, deliver, document

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate \
  -show_entries format=duration,size -of default=noprint_wrappers=1 reels-001-final.mp4
ffmpeg -hide_banner -i reels-001-final.mp4 -af volumedetect -f null - 2>&1 | grep -E 'mean_volume|max_volume'
mkdir -p ~/Movies/"Posting - Instagram" && cp reels-001-final.mp4 ~/Movies/"Posting - Instagram"/<date>-reels-NN-<slug>.mp4
md5 -q reels-001-final.mp4 ~/Movies/"Posting - Instagram"/<date>-reels-NN-<slug>.mp4   # must match
```

Then write the package doc to `docs/reports/` (scene table, script, verified-claims table, toolchain,
caption + hashtags ready to paste, free posting steps, repro commands, verification results) and commit
docs only — never the MP4. Finish by confirming the ecosystem still has only its standard top-level
folders (`ls -d */`).

## Locking a result as the standard

When the owner says a delivered take is what they want and it should hold for all future content, that is a
promotion, not a compliment. Do all four, in order:

1. **Write the standard where the next session loads it** — a skill carrying the engine, voices, presets,
   and the binding rules; plus one final report in `docs/reports/`. Procedure belongs in the skill body;
   the report is the record, the skill is the instruction.
2. **Sync through the bank tooling** (`scripts/skill-manifest.py`, then `skills/sync-to-agents.sh`) and
   confirm the hash verification passes; a standard nobody's next session can load is not locked.
3. **Re-point every superseded document.** Put a banner at the top of an older report whose approach is now
   abandoned, naming the current standard — do not leave it reading as current, and do not rewrite its
   every section.
4. **Delete the superseded scratch; keep what regenerates the result.** Project source, the silent master,
   and the locked audition file stay. What is reproducible from source does not need archiving. State in
   the final report what was removed so the deletion is traceable.

## Design rules for 9:16 (these are corrections, not taste)

- Put content in the **upper-middle safe zone**: vertical centering via
  `.inner { display:flex; flex-direction:column; justify-content:center; padding: 210px 96px 230px; }`.
  Top-weighted layouts leave the bottom half empty; bottom-heavy ones collide with Instagram's caption
  and action rail.
- Fill space with **designed density**: stat cards, chips, a value plate, and a large translucent scene
  number watermark — not with bigger text alone.
- One accent colour plus a near-black gradient background and a 120 px grid overlay reads as "designed"
  at thumbnail size; keep the kicker (uppercase, letter-spaced) → headline → rule → sub hierarchy per scene.
- Silent video + in-app trending audio is normal and free. When a voice-over exists, tell the owner to
  lower the added track to ~10–20% so narration stays intelligible.
- Reuse one template for follow-ups: swap scenes 3–5, keep the frame, timing rhythm, and CTA.

## Pitfalls

- `-v error` suppresses ffmpeg's own analysis filters — `volumedetect` **and** `silencedetect` log at info
  level, so a grepped run comes back empty and reads as "no audio" or "no silence" when the file is fine.
  Use `-hide_banner` on its own, and re-run before concluding anything from an empty result.
- `text_to_speech` with `provider="edge"` writes **`.ogg`** even when `output_path` ends in `.mp3`; use the
  returned `file_path`, not the requested extension.
- In `set -euo pipefail` helper scripts, never leave a bare `grep` whose zero-match case is legal
  (e.g. a silent video has no volume lines) — guard every such pipe with `|| true`.
- Do not depend on capturing live site screenshots for B-roll: fetching external URLs and browser
  capture can require owner approval and stall the run. Build the visuals with CSS/SVG, or ask first and
  keep the composition renderable without them.
- Music/footage licensing: skipping licensed audio is what keeps the "Rp 0" claim true. Do not add a
  track you cannot prove is free.
- One global rate/pitch for every scene is the tell of a rushed take: number-heavy scenes read too fast
  to follow and the opening drags. Set delivery per scene (see the reference).
- Batch media work (renders, multi-file TTS) can hit an approval gate mid-run. If a generation command is
  blocked, stop and ask for consent — never rephrase it into a different command to get the same effect.
- **Never identify a voice with median f0.** Pitch estimated per file is unusable as evidence: within a
  single file the median moves 40–55 Hz depending only on where the file is cut, so "different f0 per
  scene" reads as several voices when there is one. Use the timbre metric (`--timbre`) with its text
  control instead, and never conclude "the generator picked a voice per scene" from f0.
- **Assert the decoded duration before trusting any audio comparison.** Some TTS endpoints return
  headerless raw PCM (e.g. `audio/L16;codec=pcm;rate=24000`); writing those bytes to `.mp3`/`.wav` yields an
  unreadable file, and every distance computed from it is garbage that reads as a confident "engine
  eliminated". Decode explicitly (`ffmpeg -f s16le -ar <rate> -ac 1 -i pipe:0`) and drop any candidate
  whose probe produced a 0 s duration.
- **GSAP uses absolute time — changing scene boundaries alone does not fix sync.** GSAP timelines in
  HyperFrames compositions use absolute frame times (`tl.fromTo(..., 5.55)`), not relative to `data-start`.
  When you correct a scene's `data-start`, you **must** rewrite every GSAP timing inside that scene to
  match the new boundary. Changing only the `data-start` attributes while leaving GSAP times untouched
  produces exactly the sync bug seen in reels-003 v4 (VO sounded faster than the visuals).
  Write the scene boundaries and GSAP timeline in the same pass, not sequentially.
- **Pin HyperFrames version to match the reference project.** Version 0.8.62 produces 6 lint warnings
  (text_not_painted on watermark `.wnum`, contrast errors) that are inherent to the composition pattern,
  not regressions. Pin `npx --yes hyperframes@0.8.30` in the project's `package.json` scripts to match
  the reference project (reels-002) — this gives 0 errors, 0 warnings. Do not assume the global install
  version is correct; always pin the version in the project's `package.json`.
- **Use `--low-memory-mode` when disk space is tight.** With 1628 frames at 1080×1920, `--workers 2`
  needs ~13.5 GB temp space. If available disk is under 15 GB, use `--low-memory-mode --workers 1`
  which streams frames instead of writing them all to disk. This is slower (~5m vs ~4m for 1600 frames)
  but prevents disk-full failures.
- **Loudness: match the reference take, do not pick a target number from memory.** There is no LUFS
  standard written anywhere in this ecosystem — no SKILL.md, no report, no config. The value `-14` is
  not sourced from anything here. The approved takes measure differently from the number people tend to
  quote: the owner-approved VO files sit near **-19.6 LUFS** (reels-002 `vo_utuh.mp3` = -19.58,
  reels-003 `vo_charon.mp3` = -19.85, both LRA 4.5–5.1), and the reels-003 v4.1 final delivered at
  **-15.40 LUFS / TP -1.17 / LRA 3.70** and was accepted by the owner. Measure the accepted reference
  with `ffmpeg -af loudnorm=print_format=json` and match it, rather than applying a target you remember.
  If you do push toward -14, expect roughly 5 dB of gain over the approved VO and have the owner
  confirm, because normalisation is not free loudness here — it changes how the take sits against
  in-app trending audio.
- **After changing scene boundaries, ALWAYS render and vision-check each scene.** Extract a frame at
  each scene's midpoint and verify with vision_analyze that the correct scene content appears. A scene
  that shows the wrong content at its boundary time means the GSAP timeline was not rewritten to match
  the new `data-start` values.
- **Read the project's own handoff doc before running audio forensics.** A `VOICE.md`-style doc names the
  voice, the per-scene settings, and often states which tooling held it — that answers the question
  directly. Forensics is the last resort, not the first step.
- **Swapping to a slower/longer voice re-opens every scene window.** Re-measure all lines, and **shorten
  the line** to fit rather than only raising rate — faster delivery destroys the character you picked the
  voice for. Test a small (text × rate) matrix and keep the shortest line that preserves the meaning.
- **Retract in place, never append.** If an earlier report carried a conclusion drawn from a metric that
  had no calibration control, correct that conclusion inside the document; an "UPDATE: actually …" line
  under a wrong finding leaves the wrong finding standing.
- **Re-point every intermediate path when deriving a mux script from an earlier version, and delete stale
  intermediates before rendering.** A copy made by substituting the output filename kept reading the
  *previous* take's mix WAV, so the delivered "new voice" file carried the old voice — the substitution
  looked complete because only the final name had been changed.
- **Settle audio identity with lag-aligned waveform correlation, never with timbre or median f0.** Both
  weaker metrics failed on a real mix: timbre scored the correct take `0.0047` and the wrong one `0.0022`
  (no separation), and f0 fell between the two candidates; correlation returned `0.9991` for the correct
  source and `0.1569` for the wrong one. Run `scripts/audio-identity-check.py` after every mux.
- **Never verify a text transformation with a checker that reuses the transformation's own logic.** A
  harness calling the same helper the production path calls reports "clean" while the emitted string is
  visibly mangled — it was green on 26 of 33 cases during a run whose raw output was wrong. Write
  hand-written expected strings per case (a golden test) and assert the production path against those; the
  checker's verdict is operator convenience, never evidence.
- **Run the changed transform over the project's real scripts and diff before/after.** That diff is what
  proves working text was not regressed — and it is how a self-introduced regression surfaces: a
  punctuation-tidying rule silently collapsed the ellipses that carry deliberate dramatic pauses, and only
  the corpus diff showed it.
- **An A/B comparison must re-implement the OLD behaviour, not just toggle the new switch.** When both
  sides run through the patched helper, the "before" side already contains the fix and the comparison
  reports "same" for exactly the cases that changed most. Require every case to differ; treat an all-equal
  result as a harness bug before believing it.
- **Text-layer verification is the gate for pronunciation; the owner's ear is the verdict.** Duration is
  not a proxy (short utterances come back padded to a fixed floor, so spelled and unspelled forms measure
  within 0.1 s) and a speech-to-text round trip is a language model decoding its own prior, not a
  phoneme measurement. Verify the emitted string deterministically, then send the owner an A/B file with
  spoken markers.
- **Prove the engine mishandles the input before writing code to fix it.** Render the line as written and
  the same line pre-spelled, same voice, and compare. Building a normalization layer against an assumed
  engine failure is how a working take regresses — measure first, keep only the rules the measurement
  supports, and treat a single sample as a hypothesis.
- **Read a transcription; never pattern-match it.** Every ASR normalises while it writes: spoken "tiga miliar
  seratus tujuh belas juta" returns as `Rp 3.117.360.000.`, and a spelled acronym returns compressed. A
  keyword check therefore reports failures that never happened, while a term that really is mangled hides in
  the same noise. Read the whole transcript before fixing or clearing anything, then fix only the term that
  is demonstrably wrong — and leave a near-miss alone (`Next.js` read as "Next JS" is correct, not a defect).
- **Transcribe with the hosted LLM already in hand rather than downloading a local speech model.** A small
  local model hallucinates on Indonesian ("es ka pe de" came back as "Eskapi diri"); an accurate one costs
  ~1.5 GB and minutes per clip on a CPU-only machine, and it re-introduces files you may have just been told
  to delete. Send the audio to the hosted model instead — its quota is separate from the TTS quota — asking
  for a verbatim transcript with numbers and abbreviations left as spoken, and assert only a handful of
  required terms. This is how two apparent failures were retired as measurement artifacts; it is still
  weaker than the owner's ear, and a brand name two systems render the same unlikely way is exactly the case
  to hand back to the owner rather than respell on your own judgement.
- **Reload an edited Python module before re-testing it inside the persistent code kernel.** The kernel
  keeps imported modules in memory, so a patched file appears to have no effect and the fix reads as a
  failure; call `importlib.reload(<module>)` (or re-exec the file) after each edit before evaluating it,
  and re-run the check in a fresh process when the result gates a claim.
- **Reading a source project's docs is a step, not the answer.** Handoff docs state intent and often
  describe tooling that never shipped with the archive — verify the named helper files exist before
  repeating a reproducibility claim, and treat an internal label (`voice-NN`) as a name, not a voice any
  CLI can be handed.
- **Before adopting a different TTS engine, probe its voices one at a time with a real sentence in the
  target language and transcribe each.** Viability varies *per voice inside one engine*: a provider
  returned audio for four voices and only one survived a transcription check — the rest mangled ordinary
  Indonesian words ("91 W E P O P P U B L I C"). A single working voice is a fallback, not an engine
  migration. Call the endpoint repeatedly before planning volume work on it: an engine that answers one
  health check can still hang or time out back-to-back.
- **A provider's model catalogue is not a statement of access.** Probing capacity is a readiness question
  (see `content-pipeline-readiness`); the production consequence is that no pipeline should be designed on
  a model you have not successfully called once.

## Verification checklist

1. `hyperframes lint --verbose` → 0 errors, 0 warnings.
2. `ffprobe` → expected codec, 1080×1920, fps, duration, size; audio stream present when VO was added.
3. `volumedetect` → mean roughly −14…−22 dB, max below 0 dB (no clipping).
4. Contact sheets inspected visually for every scene; nothing clipped or cramped; no half-empty frames.
5. md5 of the delivered copy equals the working master — **and**, when a VO was muxed, the narration
   itself is identity-checked against the intended scene file (`scripts/audio-identity-check.py`). A
   matching md5 proves the copy, not which take was mixed into it.
6. Every on-screen figure traced to a same-day source.
7. Package doc committed in `docs/reports/`; work project outside the repo.

## Support files

- `templates/reels-9x16-composition.html` — known-good starter composition (inner wrappers + hard kills).
- `scripts/reels-qa.sh` — frame extraction, contact sheets, ffprobe + audio-level report, md5.
- `scripts/audio-similarity.py` — voice/engine comparison with two calibrated modes: DTW log-mel for
  same-text pairs, `--timbre` for cross-text questions ("is this set one voice?", "which candidate is
  closest?"). Both print their controls; read the verdicts, never the raw ranking.
- `scripts/audio-identity-check.py` — lag-aligned waveform correlation; answers "does this file carry
  exactly this audio source?" (the post-mux gate). Use it instead of timbre or f0 to prove which take
  landed in a delivered video.
- `templates/pronunciation-golden-test.py` — starter golden test for a pronunciation layer: hand-written
  expected strings, a determinism check, an A/B assertion that every case differs from the old behaviour,
  and a corpus diff over the project's real scripts. Copy it and fill the expectations by hand; never paste
  the layer's own output back in as the expectation.
- `references/content-strategy-and-hooks.md` — pre-production layer: what the platform rewards
  (shareability over likes, format split, hashtag decay, the authenticity-vs-polish penalty), hook
  requirements and benchmark numbers, the 5-part script skeleton, 5 script templates, 20 hook formulas in
  five families, borrowable concept formats, the testing cadence, the open tension with our own design
  rules, and how strongly each source should be trusted.
- `references/free-toolchain-verification.md` — how to verify free tiers from official pages, plus the
  channel limits that decide which free tool can actually publish video.
- `references/voiceover-delivery.md` — the VO delivery layer: **engine selection and hosted LLM TTS
  (Gemini) with its per-model free-tier quota and batch-per-video consequence**, prompt-and-audio-tag
  direction (tag mechanics, why mid-sentence code-switching must stay unsplit), humanize-then-synthesize,
  spoken-form numbers and acronyms, the pronunciation normalization layer (case-insensitive dictionary with
  a measured exception list; structured formats — dates, clock times, versions, phone/NIK, ranges,
  ordinals, emails, URLs, file extensions, official abbreviations) plus how to verify that layer, per-scene
  rate/pitch table, punctuation-as-pauses, voice audition (with its no-direction control), the self-serve
  renderer package, how to resolve an unidentifiable reference voice, human-recording mode, and where the
  ecosystem's worked VO pipeline lives.

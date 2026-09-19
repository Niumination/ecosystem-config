# Voice-over delivery for short-form video

Narration quality is decided by the **engine**, then by the **script** and the **per-scene delivery
settings** — in that order. A mid-tier synthesizer cannot be lifted by better text: script and delivery
work prevents a flat, uniform read, but it does not change the class of voice you get. Treat "this take
sounds worse than the reference" as an engine question first (section 0), and only afterwards as a script
or normalization question. The failure this file exists to prevent is reaching for more text processing
when the synthesizer was the ceiling.

Quality ceiling, stated once: the best-sounding narration available at zero cost is **a person reading
the script**, one file per scene. TTS is the fallback, not the equal. Offer the recording kit (section 6)
before presenting a synthesized take as final.

## 0. Engine first — choose the synthesizer before touching the script

Quality **class** separates takes more than any text-layer tweak. In published blind-preference
comparisons the proprietary LLM-based synthesizers (Gemini, GPT-4o, ElevenLabs) sit around MOS 4.2–4.3,
while the classic free endpoints and small open models sit below. What that means here:

- **Classic free endpoint** (edge-tts) — zero dependency, no key, no quota, always available. Serviceable,
  not studio. Correct default when nothing better is reachable.
- **Hosted LLM TTS** — the step up, and the first thing to research when the reference take sounds better
  than the local one.
- **Open-weight models** — mostly a dead end for Indonesian (Kokoro and Qwen3-TTS do not cover it;
  Chatterbox added it late) and the capable ones want a GPU, which a CPU-only laptop does not have.

### 0a. Hosted LLM TTS — verified shape (Gemini TTS)

Verified against the live API in this environment:

- Enumerate model ids with `GET /v1beta/models` before assuming any exists. TTS ids seen:
  `gemini-3.1-flash-tts-preview`, `gemini-2.5-flash-preview-tts`, `gemini-2.5-pro-preview-tts`.
- **Indonesian is generally available** (Javanese too).
- **30 preset voices**, each with a character descriptor — `Charon` *Informative*, `Sadaltager`
  *Knowledgeable*, `Algenib` *Gravelly*, `Gacrux` *Mature*, `Iapetus` *Clear*. Shortlist by descriptor, then
  decide by audition (section 4); descriptors are a hint, not a ranking.
- **Output is headerless PCM**: `audio/L16;codec=pcm;rate=24000`, mono. Decode explicitly with
  `ffmpeg -f s16le -ar 24000 -ac 1 -i pipe:0 out.mp3`. Writing the returned bytes straight into a `.mp3`
  or `.wav` produces an unreadable file and every measurement taken from it is noise.
- **The free tier is small and counted per model, not per account** — 10 requests/day for a TTS model, with
  a separate bucket per model, so a second TTS model keeps answering after the first is exhausted. Read the
  real limit out of the 429 body (`quotaValue`, `quotaId`) rather than trusting a docs table, and treat an
  exhausted model as a rotation signal, not a dead end.
- **Consequence for this pipeline: one request per video, not per scene.** One request accepts a whole
  short-form script, which turns a 10/day ceiling into ten videos instead of one and a half; the per-scene
  split is then recovered from the audio (silence detection) rather than bought with one call per scene.
  *The batch-then-split path is the intended approach but has not been exercised end-to-end here — prove it
  on one video and check every recovered scene boundary before depending on it.*

### 0b. Direct delivery in natural language instead of mangling the text

An LLM-based synthesizer takes direction, so prosody is steered from the prompt. Two documented failure
modes to design around:

- Without an explicit **synthesize-speech preamble plus a transcript delimiter**, the model reads the
  direction aloud — it must decide what is stage direction and what is speech. State the preamble first and
  put the lines under `#### TRANSCRIPT`.
- **Keep punctuation natural.** Practitioner guidance is explicit that period-separated fragments sound
  chopped, so a text layer that splits a script into many short pieces buys pronunciation at the cost of
  the delivery. Prefer commas between tagged clauses.
- Delivery tags stay in **English even for a non-English transcript** (`[warmly]`, `[thoughtfully]`,
  `[very slow]`), and the transcript's writing style should match the direction being given.

Audio-tag mechanics — each one fails silently if ignored:

- The documented shape is `[pacing tag] text [expressive tag] text [pause tag] text`: put each tag exactly
  where the change should land. Pacing (`[slow]`, `[fast]`), pauses (`[short pause]`, `[long pause]`) and
  non-verbal tags (`[whispers]`, `[laughs]`, `[sighs]`) are the usual working set.
- **Never place two tags next to each other** — separate them with text or punctuation. Adjacent tags raise
  a system error.
- **An accent comes from the style prompt, not from a language setting.** Passing a language code does not
  produce an accent; describe the accent in the direction block instead.
- **Do not carry the `<en>…</en>` span-splitting trick over to an LLM synthesizer.** It handles
  mid-sentence code-switching natively and rates well at it, so splitting a mixed Indonesian–English line
  into per-language spans is itself what makes the delivery chopped — leave the mixed line intact and let
  the style prompt cover the technical vocabulary. The span trick is still correct for the classic-endpoint
  renderer package in section 8, which routes exactly one voice per language.

### 0c. Prove the engine is wrong before normalizing for it

The layer in section 2 exists for engines that do not understand their input. Do not build it on an
assumption — measure, per rule:

1. Render a line **as written** and the same line **pre-spelled**, same voice, and compare the emitted
   string and its duration. If both land within a fraction of a second, that engine is already handling the
   raw form and the rule is unnecessary noise.
2. Expect a mixed answer, and treat every single measurement as a hypothesis rather than a finding — one
   sample is not a calibration. In the one spell-out test run here, the spelled acronym form measured
   longer than the raw form (raw was likely read as one invented word), while URL and symbol rewriting
   mostly added artefacts.
3. Keep only the rules that survive step 1 for the engine actually in use, and park the rest behind the
   engine that needs them. A normalization layer is engine-specific, not universal.

Normalizing for an engine that did not need it is the most reliable way to make a take sound **worse**:
individual phonemes improve while the prosody collapses into short uniform fragments.

**Fallback ladder:** hosted LLM TTS → classic free endpoint → local offline engine → owner's own recording.
Only the last one raises the quality ceiling; the rest trade availability against class.

## 1. Script layer — humanize BEFORE synthesis

Run the VO script through the humanizer rules (skill `ghost`) first:

- short sentences that can stand alone ("Tiga belas kali lipat.")
- spoken register, not written-official ("kamu bisa tanya langsung", not "Anda dapat bertanya")
- cut hedges and chain every `dan`; break one long sentence into two where the second is the punch
- vary rhythm deliberately — a 3-word sentence between two long ones
- abstract claim → concrete detail ("Ambang dan rumusnya terbuka", not "Aturannya transparan")
- **never change a number or a factual claim** while humanizing; the script pass is style only

Why it matters mechanically: TTS reads what is written. Uniform, medium-length sentences produce
uniform, medium-length speech no matter which voice is selected.

## 2. Numbers and symbols

Apply this section **only as far as section 0c proves the chosen engine needs it** — with a hosted
LLM synthesizer, most of it is unnecessary and some of it is actively harmful. With a classic endpoint,
assume it is all needed.

- Spell numbers as words: "dua ratus dua puluh sembilan juta rupiah", not `229.391.668`. Indonesian
  voices mis-group digits and insert wrong pauses.
- **Expand acronyms into their spoken letters** with a dictionary you keep beside the script
  (`SKPD → es ka pe de`, `KPK → ka pe ka`, `D4 → de empat`, `VPS → ve pe es`). An unlisted acronym is read
  as one invented word — this, not numbers, is the most common source of wrong pronunciation. An acronym
  with a real pronunciation belongs in the dictionary too (`JSON → jason`, `uptime → ap taim`). A term
  pronounced differently per language needs both forms (`IDwebhost → id web host` / `I D web host`).
- Audit the script for acronyms missing from the dictionary before synthesizing, not after listening.
- Remove characters that are never spoken: `/`, `%`, parentheses.

### 2b. Match the dictionary case-insensitively — with a measured exception list

Prose writes acronyms in lowercase as often as uppercase (`skpd`, `laporan.pdf`, `data.csv`), and a
case-sensitive dictionary silently skips every one of them. Widen the match to case-insensitive, then
**carve out the entries whose lowercase form is an ordinary word**, because those must not be rewritten:
`API` must become "a pe i" while `api` ("fire") stays `api`; the same applies to `pa`, `ram`, `rt`, `rw`,
`lan`, `dak`, `tik`, `pad`, `ai`. Keep that exception list in the dictionary data (e.g. a
`_peka_huruf_besar` key), not in the code, so it is edited alongside the terms it protects.

Do **not** guess the list. Grep a real corpus of the target language's prose for every dictionary key,
count case-sensitive versus case-insensitive hits, and put every key whose lowercase form actually occurs
into the exception list. Leave the rest case-insensitive — file extensions in particular must stay
insensitive, or `laporan.pdf` keeps its raw letters.

### 2c. Structured formats the digit speller does not cover

A renderer that spells digits correctly still mangles anything *structured*, and the failure is silent —
the output reads like ordinary prose while the audio is wrong. Normalize these **before** the digit pass:

| Input | Spoken form | What breaks otherwise |
|---|---|---|
| `19/09/2026` | "sembilan belas September dua ribu dua puluh enam" | the slashes survive into the audio |
| `09:30` | "jam sembilan tiga puluh" | the colon survives |
| `14.00` | "jam empat belas tepat" | read as a decimal |
| `v4.1.0`, `3.2` | "versi empat titik satu titik nol" | digits split around a stray dot |
| `0812-3456-7890`, 16-digit NIK | digit by digit ("nol delapan satu dua …") | grouped as thousands |
| `5-10`, `2024-2026` | "lima sampai sepuluh" | the hyphen survives |
| `ke-3` | "ketiga" | the hyphen survives |
| `admin@host.web.id` | "admin at host titik web titik id" | `@` and the dots survive |
| `mata.niumination.web.id` | "mata titik niumination titik web titik id" | the dots survive |
| `data.csv` | "data se es ve" | the dot survives |
| `dll. dgn sbb. a.n. u.p.` | "dan lain-lain, dengan, sebagai berikut, atas nama, untuk perhatian" | read as invented words |
| `A & B (urgent) = 5/6` | "A dan B urgent sama dengan lima per enam" | symbols are skipped or misread |

Rules that keep the layer safe:

- **Detect a URL only by a recognised TLD.** A loose "word.word" pattern swallows `laporan.pdf`, and the
  file extension then comes out as a domain name.
- **Order the steps:** file extensions → email → URL → date → time → version → phone → range → ordinal →
  abbreviations → symbols → digit spelling. Each step assumes the earlier ones consumed their patterns.
- **Require a number pattern to end on a digit**, or it eats the sentence-final period and the take loses
  its closing pause.
- **Never collapse an ellipsis.** `...` is a deliberate dramatic pause in narration; a "tidy repeated
  punctuation" rule destroys it silently.
- **Do not duplicate the digit speller.** Emit text for the existing speller to finish ("19 September
  2026"), instead of carrying a second number-to-words implementation that will drift out of sync.
- **Tag brands and foreign terms for the other voice automatically** (`<en>Instagram</en>`, `Zoom`,
  `GitHub`, `deadline`, `webinar`) — and protect tags that already exist, or the tagger nests
  `<en><en>…</en></en>` and the closing tag is read aloud as "per en".

Before/after for the layer, same voice and same rate on both sides:

```
skpd ke bpkp                         → es ka pe de ke be pe ka pe
0812-3456-7890                       → nol delapan satu dua … sembilan nol
19/09/2026 pukul 09:30               → sembilan belas September … pukul sembilan tiga puluh
laporan (urgent) 10 GB               → laporan urgent sepuluh gigabita
dll. dengan OPD & BPKP, sbb. 14.00   → dan lain-lain dengan o pe de dan be pe ka pe,
                                       sebagai berikut jam empat belas tepat
v4.1.0 butuh 8 MB                    → versi empat titik satu titik nol butuh delapan megabita
```

### 2d. Verify the layer at the TEXT level; the owner's ear is the verdict

Two popular audio-side proxies for pronunciation are traps, and a keyword check against a transcript is
structurally wrong:

- **Duration is not a proxy.** Short utterances come back padded to a fixed floor (≈1.87 s for every
  sample under about three syllables), so "SKPD" and "es ka pe de" measure within 0.1 s of each other and
  the comparison proves nothing.
- **A speech-to-text round trip is not a measuring instrument — and a keyword check against its transcript
  is structurally wrong.** A base-size model transcribes spelled letters as words of its own invention
  ("es ka pe de" → "Eskapi diri") — it is decoding a language model's prior, not measuring phonemes.
  Separately, the recognizer applies **inverse text normalization**: a number spoken as words comes back as
  digits ("tiga miliar seratus tujuh belas juta tiga ratus enam puluh ribu rupiah" → `Rp 3.117.360.000.`).
  So a check of the form "the transcript must contain the word *miliar*" reports failure on a take that
  pronounced the amount perfectly — in one run most cases "failed" for this reason alone while the audio
  was correct. That is a measurement bug, not a synthesis bug, and blaming the engine for it is how a
  working take gets regressed.
- If a transcript is used at all, restrict it to two jobs: accept **either** the word or the digit form as a
  pass, and answer the one question text-level checks cannot — **did the model read its own direction
  aloud?** Scan the opening of the transcript for the profile/scene/performance wording; if any of it
  appears, the prompt lost the preamble or the `#### TRANSCRIPT` delimiter and the take is unusable.

So verify what is deterministic — the **string handed to the synthesizer** — with hand-written expected
values per case asserted against the production code path, and use the audio only to confirm the take
actually changed (lag-aligned correlation against a re-render control; see the skill's
`scripts/audio-identity-check.py`). Then send the owner an A/B file: per case, a spoken marker, the old
take, the new take. They judge pronunciation; nothing else does.

Regression rule: run the changed layer over the project's real scripts and diff the emitted strings
before/after. Expect a handful of intended improvements and **zero unexplained changes** — and expect to
find at least one self-introduced regression, because a formatting rule that is obviously right in
isolation is usually wrong somewhere in real prose.

### 2e. Checking what was actually heard — hand the audio back to the hosted model

An audio-side check does exist and it needs no local speech model: send the rendered file back to the
hosted LLM **as audio input** and read the transcript. Verified working, and it is the cheapest way to
catch the one failure that only the audio shows.

- **Recipe.** One request: an instruction, then the audio inline (base64, `audio/mp3` or `audio/wav`;
  keep the file under ~18 MB or split it). Ask for a verbatim transcript and tell the model to write
  numbers, acronyms, names and URLs **exactly as they are spoken** — spelled letters as letters, a number
  read as a quantity as that quantity. A working implementation is `scripts/periksa_vo.py` in the engine
  skill `creative/gemini-vo-narration`; it takes `--unsur` and reports which expected strings appeared.
- **It costs nothing on disk and nothing from the synthesis budget.** No download, no model file, and the
  transcription quota sits on a different model than the TTS quota — so a spent TTS day still allows
  verification.
- **It is far better at Indonesian than a small local ASR.** A full mixed Indonesian–English narration came
  back clean and correctly cased, including acronyms, a phone number, an email and a version string.
- **Use it for the one question the text layer cannot answer:** did the model read its own direction aloud?
  Read the opening of the transcript. If it starts with the profile/scene/performance wording instead of
  the first spoken line, the preamble or the `#### TRANSCRIPT` delimiter was lost and the take is unusable.
  This check is worth running on its own, before any pronunciation question.

Limits — both bite, and confusing them for engine faults is how a good take gets regressed:

- **It rewrites numerals anyway.** A rupiah amount spoken as words returns as `3 miliar 117 juta` or as
  digits depending on the phrasing, so accept either form and read the transcript rather than asserting a
  pattern. This is the same inverse-text-normalization effect as below, from a second system.
- **It normalises unusual proper nouns toward familiar words.** A brand name came back with the same
  substitute spelling from two *independent* transcribers — which is a hint that the name may be unclear in
  the audio, **not proof that the engine mispronounced it**. Agreement between transcribers is not a
  pronunciation verdict. When a name matters and two systems agree against you, listen to it yourself
  before changing anything, and fix it in the style prompt rather than by mangling the script text.

A local ASR adds nothing on either path: a small local model hallucinates on Indonesian (spelled letters
come back as invented words), an accurate one is ~1.5 GB and minutes per clip on a CPU-only laptop, and
its transcript is still subject to the same normalisation. **Nothing in production or verification needs a
local speech model** — the render path shells out to `curl`, `ffmpeg` and `ffprobe` only. Confirm that with
a dependency grep before proposing a download.

## 3. Per-scene rate and pitch (free edge-tts has no SSML)

Free edge-tts rejects `<break>` / `<emphasis>`, so **pauses exist only in punctuation**: period = full
pause, comma = short, em-dash `—` = dramatic. Write the pauses into the script.

Set rate and pitch **per scene** through the edge-tts CLI, never one value for the whole video:

| Scene type | rate | pitch | Reason |
|---|---|---|---|
| opening / hook | `+10%` | `-2Hz` | fast, slightly heavier read |
| plain narrative | `+2%` | `+0Hz` | neutral |
| number-heavy / proof | `-4%` | `-3Hz` | figures must slow down to be absorbed |
| process / energy | `+6%` | `+0Hz` | forward motion |
| closing / CTA | `-4%` | `-2Hz` | calm landing |

```bash
~/.venv-mata/bin/edge-tts --voice <Voice> --rate=+10% --pitch=-2Hz \
  --text "<line>" --write-media vo/S1.mp3
```

The Hermes `text_to_speech` tool exposes only a global speed for the edge provider, so per-scene
rate/pitch requires the CLI. Call the CLI from a venv that already has edge-tts installed rather than
installing into a project folder.

Always measure each line against its scene window before mixing — a line that overruns spills into the
next scene's audio and destroys sync:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 vo/S1.mp3
```

**When a line overruns its window, shorten the text — do not just raise the rate.** Switching to a slower
voice (a male narrator reads noticeably longer than a female one at identical settings) re-opens every
window at once, and the fastest fix looks like pushing the rate up, which is exactly what destroys the
character the voice was chosen for. Instead, render a small matrix of candidates — a few shortened text
variants × two or three rates — print the durations, and keep the shortest line that still carries the
meaning. Re-measure *every* scene afterwards, not only the one that overflowed.

## 4. Choose the voice by audition, not by default

- Render **the same line** with several candidates at identical rate/pitch, concatenate with labels, and
  send the owner one comparison file. They pick.
- Multilingual narrator voices (`en-US-AndrewMultilingualNeural`, `en-US-BrianMultilingualNeural`,
  `de-DE-FlorianMultilingualNeural`) read Indonesian with more warmth and authority than the plain
  `id-ID-*` pair; the Indonesian male/female pair is serviceable but noticeably flatter for storytelling.
- **Write the audition script as real narration, not as a bench of one-off examples.** A script that reads
  as plausible content while carrying the hard cases — mixed Indonesian/English technical vocabulary,
  agency acronyms, a long rupiah amount, a date, a clock time, a phone number, an email, a version string —
  lets the owner judge delivery in context instead of judging isolated tokens. Every candidate renders the
  *same* script text so the comparison stays apples-to-apples.
- **Include a no-direction control: the same voice, same script, without the style prompt and without audio
  tags.** A styled take comes back noticeably longer (the requested pauses and slower pace), which proves
  the direction was applied — it does **not** prove it helped. Only the owner's ear settles that, and the
  control is what gives them something to compare against. Say plainly that the control exists so they can
  reject the prompt layer outright.
- Keep the numbering identical across auditions of the same candidate set (`1 Algenib · 2 Sadaltager ·
  3 Charon …`) so a choice made in one round still maps to a name in the next.
- Never ship a voice the owner has not heard at least once.

## 5. Identify what an existing recording used

**Ask first.** The owner usually knows how the reference was produced, and one question costs less than
any forensic run. Open an investigation only when they say they do not know — and then stop at the first
discriminating answer instead of pursuing the engine to the end.

Escalation order:

0. **Read the source project's own documentation first.** A `VOICE.md`-style handoff doc names the voice
   (often as an internal label, not a vendor voice name) and states which tooling held it — that alone can
   close the question. Two cautions: a doc that *references* helper files (`uji-*.mp3`, a `vo_bebas.py`)
   does not mean those files shipped with the archive — check existence before accepting its
   reproducibility claim; and an internal label like "voice-00" is not a voice any CLI can be handed.
1. **Container properties** (`ffprobe` → sample rate, bitrate, `TAG:encoder`). An `Lavf*` encoder tag means
   the file was re-encoded by ffmpeg, not raw engine output. 24 kHz mono is shared by several TTS backends,
   so it narrows little on its own — but it does rule out "never processed".
2. **Duration fingerprint** — voices read the same text at measurably different lengths: re-synthesize the
   reference text per candidate at the same rate/pitch and compare. The right voice lands within a few
   hundred milliseconds; a published per-voice duration table in the source project is a cross-check.
3. **Calibrated audio similarity** — `scripts/audio-similarity.py`. Pick the mode by question, because the
   two metrics are calibrated for different things:
   - **Same text on both files** (a re-render of the same line) → default DTW log-mel mode, read against its
     self / re-render / re-encode controls.
   - **Different text** (does this set hold one voice? which candidate is nearest?) → `--timbre` mode, which
     averages the log-mel spectrum over voiced frames so tempo and line breaks cannot distort it. It has no
     meaning without the **same-voice-different-text control**; the script demands it for exactly that
     reason.

**Is the reference set even one voice?** Answer this with timbre, never with f0. Rough calibration from a
real set: identical file `0.0000` · one voice at a 22 % different rate `0.0002` · one voice reading
*different* text `~0.001` · different scenes of one voice `0.007–0.015` · a genuinely different voice
`0.027+`. The `~0.001` text control is what makes the cross-file numbers readable: without it, a distance
of `0.02` looks "close" when it is in fact clearly another voice. Median f0 per file is **not** evidence —
within one file it swings 40–55 Hz purely by where the file is cut, so it manufactures "several voices"
out of a single one. It is a hint for hand-picking a candidate, nothing more.

Traps that produce confident wrong answers:

- **Never conclude "this is the owner's own recording" from a failed match.** A non-match means the engine
  is unknown, nothing more — a set of purely synthesized files has already been mislabelled that way, by
  inferring "human voice" from a `vo-manual/`-style folder name and a zero correlation. Report "engine
  unidentified", and ask again holding the specific file.
- **A candidate you could not actually probe is not an eliminated candidate.** If an endpoint returned
  headerless raw PCM and the probe wrote those bytes to a media container, the resulting file has no
  duration and every distance from it is noise. Verify each probe decoded to a non-zero duration, and
  re-open any earlier "eliminated" verdict whose probe took that path.
- **State the metric's limits in the report.** DTW distance between files reading *different* text has no
  calibration: a large number there is not evidence of a different voice. Also separate what was measured
  from what was inferred — "not edge-tts / not gTTS" is measured, "the engine is X" usually is not.

Stop condition: this work exists to answer the owner's question, not to satisfy curiosity. Once the owner
can name the tool, or one free voice is close enough, stop analysing and send the audition file — stating
plainly what was ruled out, what stayed unidentified, and what the free alternative is.

### Expected resolution: a hosted-session-only voice

The likely answer, and the one to aim for, is that the reference was synthesized by the **TTS engine of a
hosted agent session** and carries only an internal handle (`voice-NN`) — not a vendor voice name any CLI
can be given. Two consequences decide the whole response:

- **It is not reproducible locally, and it is not re-obtainable later either.** The voice lives in that
  session's engine; a new session has to re-audition and may land on a different timbre. Say this plainly
  instead of implying the reference can be re-rendered on demand.
- **Use the replacement settings the producer's documentation already calibrated**, not a re-derivation. A
  handoff doc that names the closest free voice usually names the exact rate and pitch for it as well; that
  pair was tuned against the reference, and re-deriving it burns a session to arrive somewhere worse.

Once this answer lands, stop the forensics. If an earlier report concluded "the generator chose a voice per
scene" from a per-file pitch comparison, retract that conclusion in place — the set being one voice is
typically the truth.

## 6. Human-recording mode (highest quality, still zero cost)

When the owner records the narration themselves:

1. Deliver a script **per scene** plus a timing/beat sheet (which scene each line belongs to and how long
   its window is).
2. Fix a filename convention that mirrors the composition scene ids (`S1.mp3` … `S6.mp3`, `R1.mp3` … for
   a reels cut) and keep one file per scene — no single 40-second take.
3. Make the mux **adapt scene length to the recording** (pad the visual, extend the scene) instead of
   forcing the recording into a fixed window; match filenames case-insensitively and fail fast with a
   list of missing files rather than silently falling back to TTS.

## 7. Read the worked example before designing a new VO

The MATA video pipeline is packaged in this ecosystem at
`labs/mata-aihackfest-2026/assets/media/pipeline/hermes-video-pipeline.zip`. Inside:

- `VOICE.md` — the delivery table, before/after humanization examples, edge-tts limits, and the
  human-recording procedure
- `naskah_short.json` / `naskah_vo.json` — per-scene `rate`, `pitch`, `voice`, and both `vo_lama` and
  humanized `vo` fields to diff
- `tts.py` — one code path for manual VO files and one for edge-tts, with the manual path deliberately
  never touching the network
- `audio/voice-samples/` — the audition set (one hook line rendered per candidate voice)

Read `VOICE.md` first; re-deriving the rules from scratch is how the flat-take failure recurs.

## 8. Prefer the self-serve renderer package over a hand-rolled TTS loop

**Scope: classic endpoint only.** With an LLM synthesizer the production path is the engine skill
(`creative/gemini-vo-narration`), where the script is sent as written and the direction lives in the prompt
— the package described below was retired when the owner locked that engine, so treat this section as the
edge-tts fallback rather than the default, and do not go looking for its files.

A per-line `edge-tts` CLI loop (section 3) works, but it re-implements — worse — what a purpose-built
renderer package already does. When the pipeline ships one (a `hermes-tts/` directory holding the renderer
script plus `suara.json` and `kamus_pelafalan.json`), that is the production path:

- **Plain numbers are spelled automatically** per language: write `Rp 3.117.360.000` and the renderer
  emits "tiga miliar seratus tujuh belas juta …", so the manual spelling pass in section 2 stops being
  needed for digits (dictionary acronyms still are). This covers *whole amounts only* — the speller does
  not understand structured values, and it will happily read `0812-3456-7890` as "delapan ratus dua belas
  ribu …". Add the normalization layer from section 2c rather than hand-spelling the script.
- **Acronyms come from the dictionary**, and the built-in checker reports any acronym it does not know —
  the audit from section 2 runs itself.
- **Language routing per span**: wrap a phrase in `<en>…</en>` to read it with the English voice while the
  rest stays Indonesian, and prefix a line with `@en` to switch a whole block. Each language maps to its
  own voice in the voice map. Mixed-language lines are the case a single-voice loop cannot get right.
- **Cost guards ride along**: a hard per-run call ceiling, existing files skipped (a re-run costs nothing),
  a process lock so two runs cannot interleave, a per-call timeout, and bounded retries.
- **Output contract matches the pipeline** — 44.1 kHz stereo 192 kbps, lead 0.60 s, tail 0.80 s, plus a
  `durations.json` — so files drop straight into the renderer's scene windows without a conversion step.

Verify it by **running it**, in this order, before quoting anything the package says about itself:

```bash
python3 hermes-tts/tts_hermes.py <naskah.txt> --cek                # free, no network: script + acronym audit
python3 hermes-tts/tts_hermes.py <naskah.txt> --keluar vo_test    # one scene is enough to prove it
ffprobe -v error -show_entries stream=sample_rate,channels,bit_rate \
        -show_entries format=duration -of csv=p=0 vo_test/S1.mp3
```

The check mode is the cheap gate: it reports digits still written as digits, symbols that are not spoken,
over-long sentences, and unknown acronyms, all without touching the network. Then confirm the emitted file
actually matches the output contract above. A package's own status line ("last tested: …") describes the
*producer's* environment — reproduce the check locally rather than repeating its claim as your evidence.
### Per-scene delivery on a per-language renderer

A renderer package maps **language → voice + rate + pitch** in its voice map, so it ships one delivery
setting for a whole script, while section 3's delivery layer needs it **per scene**. Bridge the two
without editing the package:

1. Back up the voice map once (`cp suara.json suara.json.orig`).
2. Per scene, write the map with that scene's rate/pitch for the script's language, invoke the renderer for
   that one line, then restore the original on exit (`trap 'cp -f suara.json.orig suara.json' EXIT`) and
   confirm the restore with `diff` at the end of the run.
3. Drive the loop from a single table — `tag|rate|pitch|scene-start|window|text` — printing per scene the
   measured duration, the computed end, and OK/overrun. That table, not the audio, is the artifact to keep
   when a voice has to be swapped later.

Run `--tanpa-jeda` (or the package's equivalent) so its lead/tail padding is off: your mux already places
lines with `adelay`, and leaving both on makes every line land late.

Gotchas that cost a run the first time:

- **The renderer ignores scene labels.** A single-block script emits `S1.mp3` no matter which label the
  block carries, so the driver must rename each result to its scene tag — and must test for the file
  **after** the rename. Checking the final name before renaming makes every scene report failure while the
  renders actually succeeded.
- **Only the free check mode reports which dictionary entries fired.** The render pass does not print them,
  so capture the dictionary hits from a `--cek` invocation per line if the scene table should record them.
- **Extend the dictionary for this project before rendering.** Acronyms specific to the video's domain are
  routinely absent from a shipped map even when the script uses them; add them and re-run the check, then
  keep the additions in the project copy rather than the package original.
- **The package's own configured rate/pitch is a starting point, not the delivery layer.** It is tuned for
  continuous narration; a short-form cut still wants the per-scene table from section 3.

If no such package exists in the ecosystem, section 3's loop is the fallback; if the network is
unavailable, the local offline engine is the fallback; and a provider key unlocks an SSML engine for
precise pauses when that precision is genuinely needed.

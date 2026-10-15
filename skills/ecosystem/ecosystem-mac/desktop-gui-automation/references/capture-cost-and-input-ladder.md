# Capture cost discipline and the input ladder

`computer_use` is slow when captures are unscoped and repeated. Both are
avoidable. Measured on a messaging-app task: 3 unscoped captures burned
~5-7k tokens each and six vision round trips for zero progress.

## 1. Scope every capture to the app

```
computer_use(action="capture", app="WhatsApp", mode="ax")
```

Without `app=`, the capture walks the global accessibility tree and the
macOS menu bar dominates: on a 144-element capture, 139 elements (96%) were
`AXMenuBar`/`AXMenuBarItem`/`AXMenuItem`. The useful app content was 5
elements.

**WHY it costs you twice** — the token cost, and a privacy cost: menu-bar
labels carry the user's recent-file list (document names, media filenames)
straight into the conversation. `app=` drops a typical capture from ~144
elements / ~21KB to ~37 elements / ~7KB.

## 2. Pick the cheapest mode that answers the question

| mode | returns | costs a vision round trip? |
| --- | --- | --- |
| `ax` | AX tree text only | no |
| `som` | screenshot + numbered overlays + AX tree | yes |
| `vision` | plain screenshot | yes |

Use `ax` to confirm structure, labels, and which element exists. Reach for
`som`/`vision` only when the decision genuinely needs pixels.

## 3. Re-capture only when state may have changed

Every capture is a tool call plus (for pixel modes) a vision model call. Read
the returned verdict before spending another:

- `verdict.decision: "done"` — the driver read the value back. Stop; a
  re-capture proves nothing new.
- `effect: "confirmed"` (often with `evidence: value_readback`) — verified.
- `effect: "unverifiable"` — delivered but unproven. One fresh capture decides
  it; do not re-send the input on an escalation hint alone.
- `effect: "suspected_noop"` or a structured `refusal` — climb the ladder.

Element indices are only valid for the capture that produced them; the tree is
re-enumerated every capture and indices shift.

## 4. When element clicks are refused, go to the keyboard

A refusal such as `bare element_index is not accepted; pass element_token, or
snapshot_id together with element_index` means the driver wants a per-snapshot
token the caller may not hold. Do not grind through retries.

The reliable path is keyboard navigation, which needs no element identity and
returns a read-back verdict:

```
computer_use(action="key",     app=APP, delivery_mode="foreground", keys="cmd+f")
computer_use(action="type",    app=APP, delivery_mode="foreground", text="QUERY")
computer_use(action="key",     app=APP, delivery_mode="foreground", keys="down")
computer_use(action="key",     app=APP, delivery_mode="foreground", keys="return")
```

Delivery often fails in background mode with `escalation.reason:
"delivery_failed"`; that verdict is the signal to re-issue the same action
with `delivery_mode="foreground"`. The foreground route returned
`effect: "confirmed"` with `value_readback`, which background never did.

Escalation order when a click does not land: element → fresh verify → pixel
coordinate → foreground. Re-issue the *same* action one rung up; never repeat
a confirmed action, and never guess the rung from the app being
Electron/Chromium.

## 5. Treat a rejected arg as a fallback cue, not a puzzle

If a coordinate array fails schema validation through the tool bridge, do not
burn turns re-encoding it. Switch to the keyboard ladder, which needs no
coordinates. Array-shaped args can be flattened by the bridge into a wrapper
the validator rejects — a transport artifact, not a wrong value.

## 6. Send captures to the user deliberately

Save screenshots you use only for control out of the reply. Only attach one
via `MEDIA:` when the user asked to see it — a capture of an app the user is
actively using can contain their own private content.

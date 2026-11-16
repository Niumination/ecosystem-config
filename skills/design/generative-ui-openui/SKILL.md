---
name: generative-ui-openui
description: Use when building Generative UI (interfaces composed by a model from your own components) with OpenUI Lang. Covers when to choose it over static components or JSON, defining components with Zod, streaming rendering, and the Gateway/Autofix split.
license: MIT (upstream thesysdev/openui)
metadata:
  author: thesysdev/openui
  upstream: https://github.com/thesysdev/openui
  version: "1.1"
source: riset ekosistem 2026-11-16 — docs/reports/RISET-OPENUI-2026-11-16.md
---

# Generative UI with OpenUI

Generative UI means the model composes the interface itself: it picks and configures components from a
library you control, per request. OpenUI is one open standard for this; its output format is
**OpenUI Lang**, a compact line-oriented DSL that streams.

## When to use — and when not to

Use OpenUI when the interface must **adapt to the conversation**: a dashboard assembled from live data,
a form shaped to the request, a multi-tab report. Do NOT use it for UI that is the same every time —
there a normal component is cheaper, simpler, and easier to test.

| Need | Pick |
| --- | --- |
| Fixed layout, known data | Plain component (optionally via `pick-ui-library` for the right package) |
| Structured payload, model just returns data | JSON / schema-constrained output |
| Interface composed by the model, context-driven | **OpenUI Lang** |

Rule of thumb: if you find yourself writing `if (intent === …)` to swap between hand-built screens,
that is the signal to let the model compose instead.

## Mechanics

```
Your components (Zod schemas) → system prompt → model → OpenUI Lang stream → Renderer → live UI
```

1. **Define components** — each gets a Zod schema. The **order of keys** in the schema defines the
   positional argument order in OpenUI Lang.
2. **Generate the prompt** — OpenUI turns the component library into model instructions.
3. **Call the model** — via Gateway (recommended: validates and repairs while streaming) or your own
   provider + Autofix for invalid output.
4. **Render** — `<Renderer />` parses each line as it arrives and maps it to your components.

Syntax:

```text
root = Stack([header, table])
header = Header("Laporan", "Per kuartal")
table = Table({ columns: ["Kuartal", "Pendapatan"], rows: data })
```

- One statement per line: `identifier = Expression`. First statement must be `root`.
- Values: component call, string, number, boolean, null, array, object, identifier reference.
- **Hoisting**: an identifier may be referenced before it is defined — the renderer shows a skeleton,
  then swaps in the real component when the definition lands. Keep the stream top-down
  (layout → components → data) for perceived performance.
- Trailing optional arguments may be omitted.
- Invalid lines are dropped by the parser; the rest still renders.

## Minimal React wiring

```bash
npm install @openuidev/react-lang @openuidev/react-headless
```

Define the library with Zod, hand the generated prompt to the model, stream the text back, and feed the
accumulated text to the renderer:

```tsx
import { Renderer } from '@openuidev/react-lang'

const library = createLibrary({
  Stack: z.object({ children: z.array(z.any()) }),
  Header: z.object({ title: z.string(), subtitle: z.string().optional() }),
  Table:  z.object({ columns: z.array(z.string()), rows: z.any() }),
})

// stream the model response, then:
<Renderer library={library} code={accumulatedText} />
```

For a full chat surface (threads, streaming messages, tool activity) use `@openuidev/react-ui` /
`react-headless` instead of wiring `<Renderer />` by hand.

## Model layer

- **Gateway** (`https://api.thesys.dev/v1/embed`, `THESYS_API_KEY`) — OpenAI-compatible Chat
  Completions and Responses endpoints, automatic provider failover, and OpenUI Lang repair during
  streaming. Simplest path, but a paid third-party hop.
- **Direct provider + Autofix** — keep your own provider and keys. After generation, validate with the
  parser; on failure send generation + component spec + conversation to Autofix and use the corrected
  OpenUI Lang.
- **Runtime only** — use `lang-core`/renderers with a model you already call. No Gateway, no Autofix.
  Preferred when the model provider must stay in-house.

## Pitfalls

- **Model compliance is not guaranteed.** Without Gateway/Autofix, a malformed stream only partially
  renders. Budget for that; never treat a partial render as success without validating.
- **Every component needs a Zod schema.** That is the real cost — schema authoring and keeping prop
  order stable. Renaming a key silently changes the positional mapping.
- **Sandbox the component set.** The model can only use what you register, so register deliberately;
  never hand it a raw HTML/URL-rendering component.
- **Telemetry.** `lang-core` and the CLI write install telemetry (hashed project id, atomic writes).
  Check it before use on sensitive or government networks.
- **Vendor lock-in.** Gateway/Autofix are SaaS. If the project must stay provider-neutral, use the
  runtime-only path.
- **Do not confuse this with `pick-ui-library`.** That skill selects a static UI package; this one
  decides whether the model should compose the UI at all.

## Provenance

Adopted from `thesysdev/openui` (MIT, ★15.2k, spec 1.1, active 2026-11). Study:
`docs/reports/RISET-OPENUI-2026-11-16.md`. No official agent skill ships upstream — this bank entry is
our own guide, not a copy.

---
name: provider-model-verification
description: "Verify an AI provider/model before relying on it."
version: "1.0.0"
author: Hermes Agent
metadata:
  hermes:
    tags: [provider, model, verification, free-tier, probe]
---

# Provider / Model Verification

Determine whether a provider's *listed* model actually produces output with your credentials — before planning work on it — and whether a free tier is reachable through any path at all.

## When to use
- "periksa provider ...", "cek model X bisa dipakai?", "kenapa model Y error rate limit"
- Adding a new provider/model to Hermes or to a local router

## Workflow

1. **Treat `/v1/models` as a catalog, not proof of access.** Fetch it for names, but never conclude usability from its size — some providers answer 200 on the models endpoint with dozens of entries and still reject every chat call.
2. **Probe each intended model once** with a minimal chat completion (`max_tokens` ~8). Classify by HTTP status + body hint:
   - `200` + content → usable.
   - `500` + "no available channel for this model" / "不存在" → **listed but NOT provisioned for your key** (common on aggregator keys: 20+ advertised, zero wired to your account).
   - curl timeout / HTTP `000` → registered but backend unresponsive (unusable for production).
   - `401`/`403` → auth-tier or free-tier policy.
3. **Probe the capabilities you'll actually consume, not just chat** — if vetting a production partner, test the use domain (e.g. TTS intelligibility back-to-text). Working chat does not imply working TTS/ASR.
4. **For a free-tier claim, verify two independent paths** before proposing any client-side bridge:
   a. REST directly (curl the chat endpoint).
   b. The vendor's own CLI with its logged-in session (e.g. `opencode run --model opencode/<model>`).
   If the console rejects with "<app>'s free tier can only be used from within <app>", the block is **upstream session-provenance enforcement**. No proxy pool, custom header, or session-UUID trick bridges it — the console verifies request provenance, not the network path. A proxy/relay only helps an IP/routing cause, never a session-entitlement cause.
5. **Timebox to a verdict.** When the conclusion is already formed or probes stop converging (a few sequential timeouts carry the signal of a full sweep), stop and report the evidence + verdict — do not widen the test matrix to burn budget confirming a reached conclusion.
6. **Re-probe live before trusting old notes.** A header/session-forging trick written down in an earlier session may be patched or never verified; confirm it with a live call before building on it.

## Pitfalls
- **Listed-model count ≠ accessible-model count.** A provider can return 200 on `/v1/models` with dozens of models yet reject every chat call (500 no-channel / timeout). Allocate work on probed results only, never on the catalog.
- **App-only free tiers defeat every client-side bridge.** The "can only be used from within <app>" error means the console verifies request provenance; headers, proxies, and forged session UUIDs do not change it. Distinguish IP/routing (proxy fixes) from session-entitlement (nothing client-side fixes) before recommending a relay.
- **"The CLI lists the free model" ≠ "the CLI can use it."** A vendor CLI can show free models yet time out when actually run — verify with real output, not listing appearance.

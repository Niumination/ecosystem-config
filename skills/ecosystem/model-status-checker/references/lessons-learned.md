# Model Status Checker — Lessons Learned

## Why Hybrid Approach?

Direct probing (sending a request to every model) was the naive approach. It failed:
- 88 models × ~10 tokens = ~880 tokens per run
- ~26K tokens/month — wasteful
- Most models returned 503/timeout/404 due to capacity, not because they were broken
- **False negatives**: Models behind 9router internal routing (Nous Portal, `explabs/` namespace) returned 404/401 but WORKED in production

## The Breakthrough

User challenged: "pastikan dulu script ini dapat menghasilkan tujuan yang diinginkan dengan tepat dan benar, baru impelementasikan ke cron"

Translation: **Test the script first, verify it produces correct results, THEN implement as cron job.**

This seems obvious but is a common failure mode: agents build automation on top of broken assumptions.

## What We Learned

1. **OpenRouter publishes pricing metadata** — `pricing.prompt == "0" && pricing.completion == "0"` = free model. 24 free models available as fallback.
2. **9router does NOT publish pricing** — all 88 models look identical in the catalog
3. **`explabs/` namespace** = Hermes internal routing. Cannot probe directly. Skip.
4. **`provider: nous`** in config.yaml = routed through 9router at localhost:20128, NOT direct Nous Portal URL
5. **`inclusionai/ling-3.0-flash-fin:free`** returns 404 when probed directly at 9router but WORKS in production because 9router routes it to Nous Portal internally
6. **HTTP 401 via direct Nous URL** = expected. `NINE_ROUTER_API_KEY` is for 9router, not Nous Portal.
7. **Cron provider auth** — Default Hermes provider (nous) sometimes unreachable from cron sessions. Set cron job to use `9router` with base_url `http://localhost:20128/v1`.

## The Cron Provider Problem

Original job failed with: `HTTP 404: No active credentials for provider: openai-compatible-chat-e63f76a7-...`

Root cause: Cron sessions don't inherit `NINE_ROUTER_API_KEY` from `.env` the same way main sessions do.

Fix: Set cron job provider to `9router` (local, no external API key needed for basic operation) with explicit base_url.

But: `cronjob_manage` action=update sometimes doesn't persist provider/model fields. Always verify with `hermes cron list` after update.

## Test Results (17-Sep-2026)

| Source | Result |
|--------|--------|
| OpenRouter | 24 free models identified, 444 total |
| 9router | 88 models, 4 namespaces (gh:33, gemini:8, kr:34, cf:13) |
| Hermes config | 6 critical models detected |
| Probe | 0 OK, 1 false negative (ling-3.0-flash-fin:free), 5 skipped (explabs/) |

## What Still Needs Improvement

1. **Recognize active model as OK** — If a model is the current default and we're actively using it, mark as OK regardless of probe result
2. **Persist cron provider config** — The cronjob_manage tool doesn't always save provider/model fields; sometimes needs recreate instead of update
3. **Cross-reference OpenRouter free list** — Show which of the 9router models are confirmed free via OpenRouter pricing metadata

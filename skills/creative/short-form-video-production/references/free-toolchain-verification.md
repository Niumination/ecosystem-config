# Verifying "free" tooling before it goes into a content plan

Applies whenever a plan, catalogue, or caption promises a tool is free. The rule is short: **a free
tier is a fact you read off the vendor's own page, never a fact you remember.** Marketing pages,
blog listicles, and older copies of our own registry drift within months.

## Method

1. Open the vendor's **pricing page** (and the help-centre article for the specific feature) and read
   the clause that states the limit. Search snippets are not evidence.
2. Record the **source URL next to the number** in the catalogue, and keep a `Status` column so anything
   not yet checked is visibly unverified rather than silently trusted.
3. Numbers and structure both matter: a quota figure without its qualifier is a false promise.
   Typical qualifiers to hunt for:
   - does a free plan exist **at all** (vs a 7-day trial marketed as free)
   - post/send/credit caps, refill behaviour, and "per channel" vs "per account"
   - **scheduling window** (how many days ahead content can be queued)
   - **media-type restriction** (image-only free tiers cannot publish video/reels)
   - account/brand/seat caps, and whether a card is required
   - API access and request limits
   - divergence between the **cloud** product and the **self-hosted** build of the same project
   - feature placed behind a paid plan even though the free plan looks generous (e.g. the design tool
     is free but *scheduling to social* is a paid feature)
4. When a figure changes, **fix the sentence in place** — do not append "update: actually …" underneath.
   Keep one home per list and have the plan document point at it instead of copying rows.
5. Treat anything unverified older than roughly a quarter as stale: re-check before it becomes a promise
   to a client or the public.

## Failure shapes that recur

| Shape | What it looks like | Why it bites |
|---|---|---|
| "Free forever" but media-restricted | scheduler free tier that publishes still images only | reels cannot ship through it; the plan silently has no video path |
| Cloud vs self-host split | hosted version has **no** free plan (trial only), self-hosted build is free | deploying the hosted version costs money immediately |
| Generous design tool, paid distribution | design/carousel tool free; publishing or scheduling gated to Pro | export is free, posting is manual |
| Trial labelled as free | "every plan starts with a free trial" | the plan assumes a permanent free path that does not exist |
| Window shorter than the calendar | 30-day content calendar vs a 29-day scheduling window | the last planned item can never be queued |
| Unlimited-sounding native tool | native suite described as "unlimited" | scheduling window and per-post media caps still apply |

## Publishing video at zero cost — what the checks decide

- **Native platform scheduler**: free, per-day post cap, ~30-day look-ahead, supports reels; requires a
  public/business account. Usually the cheapest first channel.
- **Free tier of a multi-channel scheduler**: limited channels × queued posts per channel; automatic
  publishing to a platform normally needs a business/creator account there.
- **Self-hosted open-source scheduler**: no quota, full feature set, but needs a server you maintain —
  that is the price of "unlimited free".
- **Automation platforms on free plans**: credit caps plus a limit on *simultaneously active* scenarios
  and a minimum interval between runs — fine for a trial, not for a daily publishing pipeline.
- Licensed music/footage is never free: keep renders silent and let the platform's own audio be added at
  upload, or the "zero cost" claim in the content becomes false.

## Where the results live

Catalogue goes in the ecosystem registry (`docs/registry/`) with a per-row source URL and a verification
column; plans and content docs reference it by pointer instead of duplicating the table. Update the
catalogue the moment a figure is disproved, and state which downstream plan decisions changed.

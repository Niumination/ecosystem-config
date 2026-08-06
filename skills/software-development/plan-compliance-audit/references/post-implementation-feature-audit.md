# Post-Implementation Feature Compliance Audit

**Use case:** After finishing a sprint/fase of feature implementation (e.g., "selesaikan P4-P5"), verify that the code matches the MASTERPLAN and TECHSPEC.

**Difference from runtime ecosystem audit:** This audit checks **implemented features against specification documents**, not running configs/crons/hooks against operational requirements. The unit of analysis is a feature/section in the spec, not a script or cron job.

## When to Use

- User says "selesaikan [fase], lalu pastikan semua sesuai masterplan dan dox"
- User says "cek apakah semua udah sesuai dengan masterplan" after implementation
- You've just implemented features from a phased roadmap and need to close the compliance loop
- A multi-tab dashboard project where each tab corresponds to a spec requirement

## Methodology

### Phase 1: Read Both Spec Documents

Every full-feature project has at least a MASTERPLAN (roadmap) and TECHSPEC (implementation contract). Read BOTH start-to-finish:

```text
MASTERPLAN.md  → What should exist, phase breakdown, priority matrix
TECHSPEC.md    → How it should work: API contracts, data models, directory structure
```

**Extract from MASTERPLAN:**
- Phase/task tables — each row is a claim: "this feature exists"
- Feature descriptions — what each tab/screen should show and do
- Priority matrix — which features were "baru" vs "existing"

**Extract from TECHSPEC:**
- API contracts — request/response shapes for every endpoint
- Data models — what each DB table should contain
- Directory structure — what files should exist
- Tab descriptions — what each HTML page should render

### Phase 2: Map Implementation vs Spec Claims

For each spec claim, determine the **actual** state:

| Spec Claim | Reality Check | Method |
|------------|---------------|--------|
| "X feature/fase is ✅ selesai" | Does the code exist? | `search_files`, `ls` |
| "API Y returns JSON with fields Z" | Run it and check | `curl` endpoint |
| "Tab Z shows [specific data]" | Serve the HTML, check JS logic | `read_file`, verify `fetch` URLs & rendering |
| "Data model has columns A, B, C" | Check DB schema | `sqlite3 .schema` |
| "Feature works by doing X" | Trace the code path | Read handler + frontend JS |

### Phase 3: Identify Three Types of Deviation

Not all deviations are bugs. Classify each mismatch:

| Type | Definition | Action |
|------|------------|--------|
| **🔴 Bug** | Feature exists but doesn't work as spec describes (e.g., chat POST doesn't send body) | Fix immediately |
| **🟡 Spec drift** | Implementation differs from spec but is FUNCTIONALLY EQUIVALENT or BETTER (e.g., SPA routing instead of multi-page TABS dict) | Update spec documents to match reality |
| **⬜ Missing** | Spec says feature exists but code doesn't implement it (e.g., Tailscale not installed) | Flag as pending — may need sudo/user action |

**Common spec drift patterns in web dashboard projects:**

1. **nav.html** — MASTERPLAN says create a separate `nav.html` component. Reality: navigation is inline in `index.html` (SPA model). This is BETTER — no HTTP request per nav click, works offline. **Document the actual architecture in AGENTS.md, don't create nav.html.**

2. **TABS dict vs SPA routing** — MASTERPLAN says use a Python `TABS` dict to serve tab pages. Reality: All routes serve `index.html` and JS reads the URL path to switch tabs. This is BETTER — preserves scroll state, enables client-side routing. **Update server.py documentation comment.**

3. **Three.js vs CSS fallback** — MASTERPLAN says build Three.js 3D office. Reality: CSS towers are lighter, render instantly, no CDN dependency. **Document the rationale in TIMELINE.md.**

### Phase 4: Verify Smoke Tests

Run a comprehensive smoke test that covers ALL claims from the spec:

```bash
# API endpoints (from TECHSPEC)
for ep in aggregated system agents cron projects gateway activity "activity/stats" tokens content; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:5200/api/mc/$ep")
  echo "[$status] /api/mc/$ep"
done

# Try POST endpoints
curl -s -X POST http://localhost:5200/api/mc/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"ping","topic_id":"1"}' | head -c 200

# All tabs serve 200
for tab in overview agents office chat tasks content schedule projects docs; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:5200/$tab")
  echo "[$status] /$tab"
done
```

**Important:** Run smoke tests AFTER applying fixes, not just at the start. The spec compliance check itself may uncover bugs that need fixing → re-testing.

### Phase 5: Update Spec Documents

After verification, synchronize the spec documents to match reality:

1. **TIMELINE.md** — Update phase status: `✅` for completed, note actual completion date
2. **TESTING.md** — Update acceptance criteria checkboxes: `☐` → `✅` for verified items
3. **MASTERPLAN.md** — If spec drift was identified and accepted, document the deviation rationale
4. **TECHSPEC.md** — If API contracts changed during implementation, update the response examples

Apply the "update first, then commit" rule: doc updates are part of the compliance fix, not a separate cleanup task.

### Phase 6: Flag Blockers

Some gaps can't be closed by code changes:

| Blocker | Example | Action |
|---------|---------|--------|
| **Needs sudo** | `brew install --cask tailscale` | Document install command, say "needs sudo" |
| **Needs external account** | Tailscale auth, Vercel deploy | Document steps, user handles |
| **Needs hardware** | GPU for Three.js | Fallback to CSS alternative |

Separate these from code bugs in your report so the user knows what requires their action vs what's already fixed.

## Example: Dashboard Feature Compliance

When auditing a multi-tab dashboard project against its MASTERPLAN:

| Check | Technique |
|-------|-----------|
| Tab exists | `ls dashboard/tabs/<tab>.html` |
| Tab loads | `curl http://localhost:5200/<tab>` → 200 |
| Tab has content | Read HTML — does it reference real API endpoints? |
| Tab JS works | Read `<script>` — are `fetch`/`fetchJSON` URLs correct? |
| API endpoint matches spec | `curl` → check JSON shape against TECHSPEC contracts |
| POST works | Does the handler parse the correct body fields? |
| DB schema matches | `sqlite3 data/agent_log.db ".schema"` |
| Data folders exist | `ls -la data/contents/{builder,pengawas,...}` |

## Pitfalls

### ❌ Only checking if files exist, not if they work
A file exists but may have bugs: chat.html sending `fetchJSON(url)` instead of `fetch(url, {method:'POST', body})`. Always read the JS logic and test the actual endpoint.

### ❌ Assuming spec is correct
Sometimes the MASTERPLAN describes an architecture that was intentionally improved upon during implementation. If the implementation is BETTER, don't "fix" it to match the spec — update the spec instead.

### ❌ Skipping doc updates
After verifying all features, leaving TIMELINE.md and TESTING.md with old ⏳/☐ markers means the docs don't reflect reality. This creates confusion in future sessions. Always sync the doc checkboxes.

### ❌ Ignoring API_BASE / URL hardcodes
A common pattern: API_BASE is hardcoded to `'http://localhost:5200'` but the spec requires remote access via Tailscale. Fix to `window.location.origin` before marking "Tailscale compatible" as done.

### ❌ Not tracing the full data flow
A POST endpoint may work in isolation but not log to the database. Always trace: frontend → POST handler → module function → database → readback.

## When to Use plan-compliance-audit vs This Reference

| Use | Skill | 
|-----|-------|
| Auditing runtime config, cron schedules, hooks, scripts against a spec | `plan-compliance-audit` (main) |
| Auditing freshly implemented features/code against a MASTERPLAN roadmap | This reference (sub-type) |
| Finding bugs in existing code by reading every source file | `codebase-audit` (related) |

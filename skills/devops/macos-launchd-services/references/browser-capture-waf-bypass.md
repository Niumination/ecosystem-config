# Browser Capture for WAF-Blocked Endpoints (Jalur G2)

Some government/industry endpoints (e.g., `data.inaproc.id`) reject datacenter IP ranges at the network/ASN layer. A headless browser on a VPS still fails. The bypass: run the browser on a **laptop (residential IP)** while the agent orchestrates via SSH.

## When to use
- `curl` from VPS returns empty or WAF block page
- Playwright/CDP capture on VPS yields 0 responses
- Endpoint requires residential IP reputation

## Tool
`scripts/rup_browser_collect.py` (Playwright-based, project-specific path: `mata/scripts/`)

## Workflow
1. **One-time setup (laptop):**
   ```bash
   pip install playwright
   python3 -m playwright install chromium
   ```
2. **First run (verify data is visible):**
   ```bash
   python3 scripts/rup_browser_collect.py \
     --url "https://data.inaproc.id/realisasi?tahun=2026&jenis_klpd=4&instansi=D6" \
     --wait 35 --screenshot --headed
   ```
   If data is server-rendered (not XHR/fetch), the script captures 0 JSON responses — `--headed` confirms whether the page actually shows data.
3. **Headless capture (after verifying data is visible):**
   ```bash
   python3 scripts/rup_browser_collect.py \
     --url "https://data.inaproc.id/realisasi?tahun=2026&jenis_klpd=4&instansi=D6" \
     --wait 35 --screenshot
   ```
4. **Push to VPS (optional, if `/api/edge-push` exists):**
   ```bash
   python3 scripts/rup_browser_collect.py \
     --url "..." --wait 35 \
     --push --url-vps https://HOST-VPS:8080 --token <edge.push_token>
   ```

## Output
- JSON lines: `mata/data/edge_capture.jsonl` (one object per captured XHR/fetch response)
- Screenshot: `mata/data/edge_screenshot_<unix_ts>.png`

## Pitfalls
- **Server-rendered data** (HTML table, not JSON API) → Playwright captures 0 responses. Use the website's "Download CSV" or HTML scraping instead.
- **Login wall** → first `--headed` run must complete manual login; the session persists in `mata/data/browser_profile/` for subsequent headless runs.
- **0 responses does not mean failure** — it means the page renders server-side. Check the screenshot to confirm data is visible.

#!/usr/bin/env python3
"""Verify a static dashboard snapshot actually works: stub endpoints answer, key data is present,
zero JS errors.

Usage:
    python3 verify_snapshot.py <url> [--expect TEXT]... [--forbid TEXT]... [--json-out FILE]

Example:
    python3 verify_snapshot.py https://example.github.io/repo/snapshot/dash.html \\
        --expect 662 --expect ANANDA --forbid '127.0.0.1:8181/api'

Why it is shaped this way:
  * Asserts against page.content() (FULL DOM), not inner_text -- dashboards that hide sections in
    collapsed panels/popups keep data in the DOM but out of visible text, which makes rendered-text
    checks report false failures.
  * Calls the injected fetch stub from the page context. That is the snapshot's actual contract:
    fetch must resolve without a backend. Existence of a stub <script> proves nothing.
  * Reports pageerror + console errors, because a snapshot can look rendered while a script threw.

Exit code 0 = PASS, 1 = FAIL.
"""

import argparse
import json
import sys

from playwright.sync_api import sync_playwright

PROBE_JS = """
async () => {
  const out = {};
  for (const ep of ['/api/status', '/api/flags', '/api/analisis']) {
    try {
      const r = await fetch(ep);
      if (!r.ok) { out[ep] = {__error: 'HTTP ' + r.status}; continue; }
      const ct = (r.headers.get('content-type') || '').toLowerCase();
      out[ep] = ct.includes('json') ? await r.json() : {__bytes: (await r.text()).length};
    } catch (e) {
      out[ep] = {__error: String(e)};
    }
  }
  return out;
}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--expect", action="append", default=[],
                    help="substring that MUST be in the DOM (repeatable)")
    ap.add_argument("--forbid", action="append", default=[],
                    help="substring that must NOT be in the DOM (repeatable)")
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args()

    errors, console_errors = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: console_errors.append(m.text)
                if m.type == "error" else None)
        page.goto(args.url, wait_until="load", timeout=60000)
        page.wait_for_timeout(4000)  # let on-load rendering settle

        dom = page.content()
        title = page.title()
        stub = page.evaluate(PROBE_JS)
        counts = {
            "tables": page.evaluate("document.querySelectorAll('table').length"),
            "scripts": page.evaluate("document.querySelectorAll('script').length"),
            "dom_chars": len(dom),
        }
        browser.close()

    status = stub.get("/api/status") or {}
    flags = stub.get("/api/flags")

    checks = {
        "stub_status_responds": isinstance(status, dict) and not status.get("__error"),
        "stub_status_not_degraded": isinstance(status, dict) and bool(status.get("ok", True)),
        "stub_flags_responds": isinstance(flags, list) and len(flags) > 0,
        "zero_js_errors": not errors,
        "zero_console_errors": not console_errors,
    }
    for text in args.expect:
        checks[f"dom_has[{text[:28]}]"] = text in dom
    for text in args.forbid:
        checks[f"dom_lacks[{text[:28]}]"] = text not in dom

    report = {
        "url": args.url,
        "title": title,
        "stub": stub,
        "counts": counts,
        "js_errors": errors,
        "console_errors": console_errors,
        "checks": checks,
    }

    print("TITLE:", title)
    print("STUB:", json.dumps(stub, ensure_ascii=False)[:400])
    print("COUNTS:", counts)
    for name, ok in checks.items():
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")
    if errors:
        print("JS_ERRORS:", errors[:3])
    if console_errors:
        print("CONSOLE_ERRORS:", console_errors[:3])

    passed = all(checks.values())
    print("RESULT:", "PASS" if passed else "FAIL")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

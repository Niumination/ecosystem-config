#!/usr/bin/env python3
"""Verify a landing/picker page: every relative link resolves, cards render, hints are present,
zero JS errors. A rendered-but-dead-link landing page otherwise passes a visual glance.

Usage: python3 verify_landing_links.py <url> [expected_card_count]
Exits 0 on PASS, 1 on FAIL. Screenshot lands at /tmp/landing-page.png for the layout check.
"""
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]
expect_cards = int(sys.argv[2]) if len(sys.argv) > 2 else None
base = url.rsplit("/", 1)[0]
errors = []

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(url, wait_until="load", timeout=45000)
    pg.wait_for_timeout(600)

    title = pg.title()
    headings = pg.eval_on_selector_all("h2", "els => els.map(e => e.innerText)")
    cards = pg.evaluate("document.querySelectorAll('.card').length")
    links = pg.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")

    # resolve internal links against the served base - this is the real check
    resolved = {}
    for href in links:
        if href.startswith("http") or href.startswith("#"):
            continue
        resolved[href] = pg.request.get(base + "/" + href.lstrip("./")).status

    pg.screenshot(path="/tmp/landing-page.png", full_page=True)
    b.close()

checks = {
    "has_title": bool(title.strip()),
    "cards_rendered": cards > 0 and (expect_cards is None or cards == expect_cards),
    "headings_present": bool(headings) and all(h.strip() for h in headings),
    "all_relative_links_200": bool(resolved) and all(v == 200 for v in resolved.values()),
    "zero_js_errors": not errors,
}

print("TITLE:", title)
print("H2:", headings)
print("CARDS:", cards, "(expected %s)" % (expect_cards if expect_cards else "any"))
print("LINKS:", resolved)
for k, v in checks.items():
    print("  %s %s" % ("OK " if v else "FAIL", k))
print("JS_ERRORS:", len(errors), errors[:3])
ok = all(checks.values())
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)

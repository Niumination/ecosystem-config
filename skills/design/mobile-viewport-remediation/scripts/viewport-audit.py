#!/usr/bin/env python3
"""Audit mobile satu URL di beberapa lebar viewport via camofox REST.

Pakai: python3 viewport-audit.py https://contoh.app [/rute /rute2 ...]
Butuh camofox di 127.0.0.1:9377. Kalau belum jalan, start sesuai skill `camofox-browser`.

Per rute x lebar dicetak: tinggi halaman (px + setara layar), tinggi per blok utama, lebar anak
kartu pertama, jumlah kontrol <44px, keadaan deret chip, dan elemen sticky/fixed.
"""
import json, sys, time, urllib.request

BASE = "http://127.0.0.1:9377"
KEY = "hermes-camofox-2026"
USER = "viewport-audit"
WIDTHS = [390, 360, 320]

PROBE = r"""
(() => {
  const nm = e => e.tagName.toLowerCase() + (e.className ? '.' + e.className.toString().trim().split(/\s+/)[0] : '');
  const small = [];
  for (const e of document.querySelectorAll('a, button, [role=button], select, summary')) {
    const r = e.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 && r.height < 44) small.push({ el: nm(e), h: Math.round(r.height), txt: ((e.innerText || '') + '').trim().replace(/\s+/g, ' ').slice(0, 20) });
  }
  const cards = [...document.querySelectorAll('.service-card, .card')];
  const c = cards[0];
  const anak = c ? [...c.children].map(e => { const r = e.getBoundingClientRect(); return { el: nm(e), w: Math.round(r.width), h: Math.round(r.height), disp: getComputedStyle(e).display }; }) : [];
  const chips = document.querySelector('[class*=tags], [class*=chip]');
  const blocks = [...(document.querySelector('main') || document.body).children]
    .map(e => ({ el: nm(e), h: Math.round(e.getBoundingClientRect().height) })).filter(o => o.h > 60);
  const st = [...document.querySelectorAll('body *')]
    .filter(e => ['sticky', 'fixed'].includes(getComputedStyle(e).position) && e.getBoundingClientRect().height > 20).map(nm);
  return JSON.stringify({
    vw: innerWidth, tinggi: document.body.scrollHeight,
    layar: Math.round(document.body.scrollHeight / innerHeight),
    kartu: c ? { w: Math.round(c.getBoundingClientRect().width), h: Math.round(c.getBoundingClientRect().height), display: getComputedStyle(c).display, anak } : null,
    kartuRata: cards.length ? Math.round(cards.reduce((a, x) => a + x.getBoundingClientRect().height, 0) / cards.length) : null,
    kontrolKecil: { n: small.length, contoh: small.slice(0, 5) },
    chips: chips ? { wrap: getComputedStyle(chips).flexWrap, scrollable: chips.scrollWidth > chips.clientWidth, tinggi: Math.round(chips.getBoundingClientRect().height) } : null,
    blok: blocks.slice(0, 8), stickyFixed: st.slice(0, 6)
  });
})()
"""


def call(method, path, body=None, timeout=120):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None, method=method)
    req.add_header("Authorization", "Bearer " + KEY)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            try:
                return json.loads(raw)
            except Exception:
                return raw
    except Exception as e:
        return {"error": str(e)}


def ev(tab, expr, timeout=120):
    res = call("POST", f"/tabs/{tab}/evaluate", {"userId": USER, "expression": expr}, timeout)
    if not isinstance(res, dict):
        return res
    v = res.get("result", res)
    if isinstance(v, str):
        try:
            return json.loads(v)
        except Exception:
            return v
    return v


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    base = sys.argv[1].rstrip("/")
    routes = sys.argv[2:] or ["/"]
    tab = call("POST", "/tabs", {"userId": USER, "sessionKey": "audit", "url": base + routes[0]})
    tid = tab.get("tabId") if isinstance(tab, dict) else None
    if not tid:
        print("gagal membuka tab:", str(tab)[:200])
        print("pastikan camofox jalan di", BASE)
        sys.exit(1)
    for route in routes:
        for w in WIDTHS:
            call("POST", f"/tabs/{tid}/viewport", {"userId": USER, "width": w, "height": 844})
            call("POST", f"/tabs/{tid}/navigate", {"userId": USER, "url": base + route})
            time.sleep(3)
            ev(tid, "(() => { window.scrollTo(0, 400); return 1 })()")
            time.sleep(0.8)
            r = ev(tid, PROBE)
            if not isinstance(r, dict):
                print(f"  {route} @{w}: data tidak terbaca ({str(r)[:80]})")
                continue
            print(f"\n=== {route} @{w}px — tinggi {r['tinggi']}px (~{r['layar']} layar) ===")
            if r.get("kartu"):
                k = r["kartu"]
                print(f"  kartu {k['w']}x{k['h']}px display={k['display']} (rata-rata {r['kartuRata']}px)")
                for a in k["anak"][:6]:
                    print(f"     {a['w']:>5}px lebar  {a['h']:>4}px  {a['disp']:<12} {a['el'][:30]}")
            print(f"  kontrol <44px: {r['kontrolKecil']['n']}  {r['kontrolKecil']['contoh']}")
            if r.get("chips"):
                print(f"  chips: wrap={r['chips']['wrap']} scrollable={r['chips']['scrollable']} tinggi={r['chips']['tinggi']}px")
            print(f"  blok: {[(b['el'][:22], b['h']) for b in r['blok']]}")
            print(f"  sticky/fixed: {r['stickyFixed']}")
    call("DELETE", f"/sessions/{USER}")


if __name__ == "__main__":
    main()

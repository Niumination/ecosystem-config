#!/usr/bin/env python3
"""Audit akses model 9router — disable provider yang 0 model OK.

Usage: python3 audit_models.py
"""
import json, os, sqlite3, urllib.request, urllib.error
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor as cf

ROUTER = "http://localhost:20128/v1"
DB = os.path.expanduser("~/.9router/db/data.sqlite")
KEY = os.environ.get("NINE_ROUTER_API_KEY", "")

def get_models():
    req = urllib.request.Request(f"{ROUTER}/models", headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return [m["id"] for m in json.load(r)["data"]]

def test_model(mid):
    body = json.dumps({"model": mid, "messages": [{"role": "user", "content": "x"}], "max_tokens": 5}).encode()
    req = urllib.request.Request(f"{ROUTER}/chat/completions", data=body,
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return mid, r.status
    except urllib.error.HTTPError as e:
        return mid, e.code
    except Exception:
        return mid, 0

def main():
    print("=== 9router model audit ===")
    try:
        ids = get_models()
    except Exception as e:
        print(f"❌ 9router mati: {e}")
        print("   Restart: launchctl kickstart -k gui/$(id -u)/com.9router.autostart")
        return
    print(f"total model: {len(ids)}")

    res = {}
    with cf(max_workers=8) as ex:
        for mid, st in ex.map(test_model, ids):
            res[mid] = st == 200

    ok = [m for m, v in res.items() if v]
    fails = [(m, res[m]) for m in res if not res[m]]
    print(f"OK: {len(ok)} | FAIL: {len(fails)}")

    # group by provider
    by_prov = defaultdict(lambda: [0, 0])  # [ok, total]
    for m in ids:
        p = m.split("/")[0]
        by_prov[p][1] += 1
        if res[m]:
            by_prov[p][0] += 1

    print("\n=== per provider ===")
    disable = []
    for p, (o, t) in sorted(by_prov.items()):
        flag = "❌ DISABLE" if o == 0 else "✅"
        print(f"  {flag} {p}: {o}/{t} ok")
        if o == 0:
            disable.append(p)

    if disable:
        print(f"\nDisabling providers: {disable}")
        con = sqlite3.connect(DB)
        for p in disable:
            n = con.execute("UPDATE providerConnections SET isActive=0 WHERE provider=?", (p,)).rowcount
            print(f"  {p}: {n} connection(s) → isActive=0")
        con.commit()
        con.close()
        print("\nRestart server: launchctl kickstart -k gui/$(id -u)/com.9router.autostart")
    else:
        print("\nSemua provider punya model OK — tidak ada yang di-disable.")

if __name__ == "__main__":
    main()

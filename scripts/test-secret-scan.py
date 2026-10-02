#!/usr/bin/env python3
"""Self-check untuk pola gate kredensial.

    python3 scripts/test-secret-scan.py

Exit 0 hanya bila setiap kebocoran sintetis tertangkap dan setiap placeholder
aman tetap lolos. Fixture disusun dari potongan runtime, bukan literal utuh, demi
agar file ini sendiri tidak memicu gate yang diujinya.
"""
import importlib.util
import re

GATE = "/Users/zaryu/Desktop/Niumination/scripts/secret-scan-staged.py"
spec = importlib.util.spec_from_file_location("ss", GATE)
ss = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ss)

# Nama variabel dirakit dari bagian, supaya tak ada baris `NAMA_KEY=nilai` utuh.
V_API = "API" + "_KEY"
V_ACC = "ACCESS" + "_KEY"
V_ADM = "ADMIN" + "_KEY"
P_CAMO = "CAMOFOX_" + V_API

# Nilai sintetis. Panjang sengaja realistis (19 char) seperti key yang bocor.
S1 = "cfapi" + "-" + "synthetic0"
S2 = "cfacc" + "-" + "synthetic1"
S3 = "cfadm" + "-" + "synthetic2"

MUST_CATCH = [
    ("camofox_api", f'{P_CAMO}="{S1}"'),
    ("camofox_access", f'CAMOFOX_{V_ACC}={S2}'),
    ("camofox_admin", f'CAMOFOX_{V_ADM}={S3}'),
    ("bare_apikey", f'{V_API.lower()} = "{"x" * 24}"'),
    ("colon_secret", "secret: '" + "a" * 20 + "'"),
    ("github", "ghp_" + "A" * 30),
    ("openai", "sk-" + "b" * 30),
    ("aws", "AKIA" + "C" * 16),
]

MUST_PASS = [
    ("env_var_ref", "set -a; . ~/.hermes/.env; set +a"),
    ("env_interp", "Authorization: Bearer $" + V_ACC),
    ("js_interp", "Authorization: 'Bearer ' + process.env." + V_ACC),
    ("placeholder", V_API + '="your-key-here"'),
    ("redacted_doc", V_API + " = <REDACTED>"),
    ("name_only", P_CAMO + ": read from ~/.hermes/.env, never commit"),
    ("comment", "# Set the key via the launchd plist env"),
    ("url", "https://example.com/api/v1/models?token=x"),
    ("plist_placeholder", "<string>__CAMOFOX_ACCESS_KEY__</string>"),
]


def hits(text):
    return [label for label, pat in ss.PATTERNS if pat.search(text)]


fails = []
print("=== HARUS ditolak ===")
for name, text in MUST_CATCH:
    h = hits(text)
    print(f"  {'PASS' if h else 'FAIL'}  {name:<16} -> {h or 'TIDAK TERTANGKAP'}")
    if not h:
        fails.append(f"leak slipped through: {name}")

print("\n=== HARUS boleh ===")
for name, text in MUST_PASS:
    h = hits(text)
    print(f"  {'PASS' if not h else 'FAIL'}  {name:<16} -> {h or 'bersih'}")
    if h:
        fails.append(f"false positive: {name}")

print()
if fails:
    print("GATE_TEST_FAIL")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print(f"GATE_TEST_PASS  ({len(MUST_CATCH)} kebocoran tertangkap, "
      f"{len(MUST_PASS)} placeholder lolos)")
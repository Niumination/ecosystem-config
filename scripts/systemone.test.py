#!/usr/bin/env python3
"""
systemone.test.py — Self-check untuk scripts/systemone.py
=============================================================
Hanya menguji gate AMAN (tidak butuh jaringan / tidak biayai). Semua uji yang
menyentuh endpoint --allow sengaja DILEWATI supaya check ini gratis & idempoten.

Jalankan:  python3 scripts/systemone.test.py
Exit:      0 = semua lolos, 1 = ada yang gagal
"""
import os, pathlib, subprocess, sys

SCRIPT = pathlib.Path(__file__).parent / "systemone.py"
DISABLE_FILE = pathlib.Path.home() / ".hermes/systemone.disabled"
fails = []


def run(args, env_extra=None, expect_fail=False):
    env = {**os.environ, **(env_extra or {})}
    p = subprocess.run([sys.executable, str(SCRIPT), *args],
                       capture_output=True, text=True, env=env, timeout=60)
    if expect_fail and p.returncode == 0:
        fails.append(f"{' '.join(args)[:60]}: diharapkan GAGAL tapi exit 0")
    if not expect_fail and p.returncode != 0:
        fails.append(f"{' '.join(args)[:60]}: exit {p.returncode} — {p.stderr[:80]}")
    return p


# 1. kill switch ENV harus menolak, walau --allow diberikan
p = run(["--q", "t::tes?", "--noul", "--allow"], {"SYSTEMONE_DISABLED": "1"}, expect_fail=True)
assert "SYSTEMONE_DISABLED" in (p.stderr + p.stdout), "kill switch env tidak.message jelas"

# 2. kill switch FILE harus menolak
DISABLE_FILE.parent.mkdir(parents=True, exist_ok=True)
DISABLE_FILE.touch()
try:
    p = run(["--q", "t::tes?", "--noul", "--allow"], expect_fail=True)
    assert "Kill switch" in (p.stderr + p.stdout), "kill switch file tidak.message jelas"
finally:
    DISABLE_FILE.unlink(missing_ok=True)

# 3. budget 0 / negatif harus ditolak (fail-closed)
for b in ["0", "-1"]:
    run(["--q", "t::tes?", "--noul", "--budget", b], expect_fail=True)

# 4. cap kecil harus menolak SEBELUM request
p = run(["--q", "t::tes?", "--noul", "--budget", "0.000000001", "--allow"], expect_fail=True)
assert "cap" in (p.stderr + p.stdout), "budget cap tidak menolak"

# 5. batas atas pertanyaan
run(["--q", "a::t", "--noul", "--q", "b::t", "--noul", "--q", "c::t", "--noul",
     "--q", "d::t", "--noul", "--q", "e::t", "--noul", "--q", "f::t", "--noul",
     "--q", "g::t", "--noul", "--q", "h::t", "--noul", "--q", "i::t", "--noul",
     "--q", "j::t", "--noul", "--q", "k::t", "--noul"], expect_fail=True)

# 6. choice tanpa --crit harus ditolak
p = run(["--q", "t::tes?"], expect_fail=True)
assert "crit" in (p.stderr + p.stdout), "choice tanpa crit tidak ditolak"

# 7. format --q salah harus ditolak
run(["--q", "tanpa-pemisah"], expect_fail=True)

# 8. tanpa pertanyaan = usage error
run([], expect_fail=True)

# 9. dry-run TIDAK boleh mengirim request — harus tampil rancangan
p = run(["--q", "isi::Apa ini?", "--crit", "a::desc", "--crit", "b::desc"])
out = p.stdout
assert "DRY-RUN" in out, "dry-run tidak ditandai"
assert "questions" in out, "dry-run tidak menampilkan body"
assert "Bearer" not in out and "NINE_ROUTER" not in out, "dry-run bocorkan key"

# 10. secret tidak pernah muncul di output mana pun
p = run(["--q", "t::tes?", "--noul", "--json"], expect_fail=False)  # dry-run
assert "sk-" not in p.stdout, "prefix key bocor ke stdout"

print(f"\n{'FAIL' if fails else 'PASS'} — {len(fails)} masalah")
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)

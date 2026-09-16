#!/usr/bin/env python3
"""niu-health-probe.py — detak jantung no-agent untuk Niumination.

Tidak memanggil LLM. Tidak mencetak nilai secret. Tidak menulis ke NTFS.
Exit code (lihat laporan §4.3):
    0  semua sinyal wajib hijau
   10  Mission Control down (usaha restart sudah dicoba jika --heal)
   11  9router down
   12  Hermes Gateway down
   13  cron c6ec80ed633f masih ERROR / unpinned
   20  skill-plane drift
   30  canary deploy gagal (tidak men-trigger restart)
   40  RAM kritis
   2   preflight path salah (bukan mesin zaryu)

Contoh:
    python3 niu-health-probe.py
    python3 niu-health-probe.py --heal
    python3 niu-health-probe.py --loop --interval 120 --heal
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NIU_DEFAULT = "/Users/zaryu/Desktop/Niumination"
MC_PORT = int(os.environ.get("NIU_MC_PORT", "5200"))
NINE_PORT = int(os.environ.get("NINE_PORT", "20128"))
JOB_ID = os.environ.get("JOB", "c6ec80ed633f")
BANK_EXPECTED = 47
ALERT_THREAD = os.environ.get("NIU_ALERT_THREAD", "1172")

EXIT_OK = 0
EXIT_MC = 10
EXIT_NINE = 11
EXIT_GW = 12
EXIT_CRON = 13
EXIT_SKILL = 20
EXIT_CANARY = 30
EXIT_RAM = 40
EXIT_PREFLIGHT = 2


def now_wib() -> str:
    # Asia/Jakarta = UTC+7, tanpa dependensi zoneinfo opsional
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def http_probe(url: str, timeout: float = 4.0, headers: dict[str, str] | None = None) -> tuple[int, float, str]:
    started = time.monotonic()
    req = urllib.request.Request(url, method="GET", headers=headers or {"User-Agent": "niu-health-probe/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = time.monotonic() - started
            return int(resp.status), elapsed, ""
    except urllib.error.HTTPError as exc:
        elapsed = time.monotonic() - started
        return int(exc.code), elapsed, str(exc.reason)
    except Exception as exc:  # noqa: BLE001 — probe harus tahan semua gagal jaringan
        elapsed = time.monotonic() - started
        return 0, elapsed, type(exc).__name__


def port_open(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def run(cmd: list[str], timeout: float = 15.0) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"{cmd[0]} not found"
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def pgrep_first(pattern: str) -> str | None:
    code, out, _ = run(["pgrep", "-f", pattern], timeout=5)
    if code == 0 and out:
        return out.splitlines()[0].strip()
    return None


def free_ram_mb() -> int | None:
    # macOS: pages free+speculative+inactive * page size
    code, out, _ = run(["vm_stat"], timeout=5)
    if code != 0:
        return None
    page = 4096
    keys = {"Pages free": 0, "Pages speculative": 0, "Pages inactive": 0}
    for line in out.splitlines():
        for key in list(keys):
            if line.startswith(key):
                num = line.split(":")[-1].strip().rstrip(".").replace(".", "")
                try:
                    keys[key] = int(num)
                except ValueError:
                    pass
        if "page size of" in line:
            try:
                page = int(line.split("page size of")[-1].split()[0])
            except ValueError:
                pass
    total_pages = sum(keys.values())
    return int(total_pages * page / (1024 * 1024))


def count_skill_md(root: Path) -> int:
    if not root.is_dir():
        return -1
    return sum(1 for p in root.rglob("SKILL.md") if p.is_file())


def append_ops_log(niu: Path, payload: dict[str, Any]) -> None:
    ops = niu / "brain" / "ops"
    try:
        ops.mkdir(parents=True, exist_ok=True)
        day = datetime.now().strftime("%Y-%m-%d")
        path = ops / f"{day}.md"
        line = f"- `{payload.get('ts')}` probe exit={payload.get('exit')} signals={json.dumps(payload.get('signals'), ensure_ascii=False)}\n"
        with path.open("a", encoding="utf-8") as fh:
            if path.stat().st_size == 0:
                fh.write(f"# ops {day}\n\n")
            fh.write(line)
        # JSON machine-readable rolling
        jpath = ops / "probe-last.json"
        jpath.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError:
        pass


def try_heal_mc(niu: Path) -> None:
    uid = os.getuid()
    label = f"gui/{uid}/niu.missioncontrol"
    code, _, _ = run(["launchctl", "kickstart", "-k", label], timeout=8)
    if code == 0:
        return
    server = niu / "services" / "niu-mission-control" / "server.py"
    if not server.is_file():
        return
    ops = niu / "brain" / "ops"
    ops.mkdir(parents=True, exist_ok=True)
    stdout = ops / "mc.stdout.log"
    stderr = ops / "mc.stderr.log"
    # jangan dobel-spawn jika sudah ada
    if pgrep_first("niu-mission-control/server.py"):
        return
    with stdout.open("a") as so, stderr.open("a") as se:
        subprocess.Popen(
            [sys.executable, str(server)],
            cwd=str(server.parent),
            stdout=so,
            stderr=se,
            start_new_session=True,
        )


def try_heal_launchd(label_suffix: str) -> None:
    uid = os.getuid()
    run(["launchctl", "kickstart", "-k", f"gui/{uid}/{label_suffix}"], timeout=8)


def probe_once(args: argparse.Namespace) -> int:
    niu = Path(args.niu)
    signals: dict[str, Any] = {"ts": now_wib()}
    worst = EXIT_OK

    if not niu.is_dir():
        print(f"[PREFLIGHT] root tidak ada: {niu}", file=sys.stderr)
        return EXIT_PREFLIGHT

    trap = Path("/Volumes/Niumination")
    signals["ntfs_trap_mounted"] = trap.exists()
    usb = Path("/Volumes/HermesAgent")
    signals["usb_mounted"] = usb.exists()

    # RAM
    ram = free_ram_mb()
    signals["free_ram_mb"] = ram
    if ram is not None and ram < 800:
        print(f"[RAM] kritis free={ram}MB")
        worst = max(worst, EXIT_RAM)
    elif ram is not None and ram < 1536:
        print(f"[RAM] degradasi free={ram}MB")

    # Mission Control
    mc_code, mc_ms, mc_err = http_probe(f"http://127.0.0.1:{MC_PORT}/", timeout=3.0)
    signals["mc"] = {"http": mc_code, "s": round(mc_ms, 3), "err": mc_err}
    if mc_code == 0:
        print(f"[MC] DOWN :{MC_PORT} ({mc_err})")
        if args.heal:
            try_heal_mc(niu)
            time.sleep(2)
            mc_code, mc_ms, mc_err = http_probe(f"http://127.0.0.1:{MC_PORT}/", timeout=3.0)
            signals["mc_after_heal"] = {"http": mc_code, "s": round(mc_ms, 3)}
        if mc_code == 0:
            worst = max(worst, EXIT_MC)
        else:
            print(f"[MC] pulih HTTP {mc_code} in {mc_ms:.2f}s")
    else:
        print(f"[MC] HTTP {mc_code} in {mc_ms:.2f}s")

    # 9router — SPOF Telegram
    nine_url = f"http://127.0.0.1:{NINE_PORT}/v1/models"
    nine_code, nine_ms, nine_err = http_probe(nine_url, timeout=3.0)
    signals["nine"] = {"http": nine_code, "s": round(nine_ms, 3), "err": nine_err}
    if nine_code == 0:
        print(f"[9router] DOWN :{NINE_PORT} ({nine_err})")
        if args.heal:
            try_heal_launchd("niu.ninerouter")
        worst = max(worst, EXIT_NINE)
    else:
        print(f"[9router] HTTP {nine_code} in {nine_ms:.2f}s")

    # OpenCode Zen — jangan kirim key ke stdout
    zen_code, zen_ms, zen_err = http_probe("https://opencode.ai/zen/v1/models", timeout=8.0)
    signals["zen"] = {"http": zen_code, "s": round(zen_ms, 3), "err": zen_err}
    print(f"[zen] HTTP {zen_code} in {zen_ms:.2f}s")

    # Gateway
    gw_pid = pgrep_first("[h]ermes.*gateway") or pgrep_first("[H]ermes")
    signals["gateway_pid"] = gw_pid
    if gw_pid:
        print(f"[gateway] pid {gw_pid}")
    else:
        print("[gateway] PID tidak ketemu")
        if args.heal:
            try_heal_launchd("ai.hermes.gateway")
        worst = max(worst, EXIT_GW)

    # Cron job pin / status (best-effort)
    if shutil.which("hermes"):
        code, out, err = run(["hermes", "cron", "status"], timeout=20)
        blob = (out + "\n" + err).lower()
        signals["cron_status_rc"] = code
        if JOB_ID.lower() in blob or JOB_ID in (out + err):
            snippet = "\n".join(
                line for line in (out + "\n" + err).splitlines() if JOB_ID in line or "agent-reach-watch" in line.lower()
            )
            signals["cron_snippet"] = snippet[:500]
            if "error" in snippet.lower() or "blocked_config" in snippet.lower() or "unpinned" in snippet.lower():
                print(f"[cron] {JOB_ID} masih bermasalah")
                worst = max(worst, EXIT_CRON)
            else:
                print(f"[cron] {JOB_ID} terlihat di status")
        else:
            print(f"[cron] job {JOB_ID} tidak terlihat di `hermes cron status`")
    else:
        print("[cron] binary hermes tidak di PATH — dilewati")

    # Skill plane
    bank = niu / "skills"
    bank_n = count_skill_md(bank)
    signals["skills_bank"] = bank_n
    home_candidates = [
        Path.home() / ".hermes" / "skills",
        Path.home() / ".hermes" / "hermes-agent" / "skills",
    ]
    home_n = next((count_skill_md(p) for p in home_candidates if p.is_dir()), -1)
    signals["skills_home"] = home_n
    usb_n = count_skill_md(usb) if usb.exists() else -2
    signals["skills_usb"] = usb_n
    jcode = usb / ".cache" / "unix-home" / ".jcode" / "skills"
    jcode_ok = jcode.is_dir()
    signals["jcode_dir"] = jcode_ok if usb.exists() else "usb-unmounted"
    print(f"[skills] bank={bank_n} (expect {BANK_EXPECTED}) home={home_n} usb={usb_n} jcode={signals['jcode_dir']}")
    if bank_n != BANK_EXPECTED and bank_n >= 0:
        print("[skills] DRIFT: bank != 47")
        worst = max(worst, EXIT_SKILL)
    if usb.exists() and not jcode_ok and args.heal:
        try:
            jcode.mkdir(parents=True, exist_ok=True)
            print(f"[skills] mkdir {jcode}")
        except OSError as exc:
            print(f"[skills] gagal mkdir Jcode: {exc}")

    # Canary — tidak menaikkan worst di atas 30, dan tidak heal
    canaries = {
        "kune-ya": os.environ.get("NIU_CANARY_KUNEYA", "https://kune-ya.com"),
        "pemdi": os.environ.get("NIU_CANARY_PEMDI", "https://pemdi-aceh-tengah.vercel.app"),
    }
    canary_fail = False
    signals["canary"] = {}
    for name, url in canaries.items():
        c, ms, err = http_probe(url, timeout=10.0)
        signals["canary"][name] = {"http": c, "s": round(ms, 3), "err": err}
        print(f"[canary] {name} HTTP {c} in {ms:.2f}s")
        if c == 0:
            canary_fail = True
    if canary_fail and worst == EXIT_OK:
        worst = EXIT_CANARY

    payload = {
        "ts": signals["ts"],
        "exit": worst,
        "alert_thread": ALERT_THREAD,
        "signals": signals,
        "heal": bool(args.heal),
    }
    append_ops_log(niu, payload)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    return worst


def main() -> int:
    parser = argparse.ArgumentParser(description="Niumination health probe (no-agent)")
    parser.add_argument("--niu", default=os.environ.get("NIU", NIU_DEFAULT))
    parser.add_argument("--heal", action="store_true", help="kickstart MC/gateway/9router + mkdir Jcode")
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--interval", type=int, default=120)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.loop:
        return probe_once(args)

    last = EXIT_OK
    while True:
        try:
            last = probe_once(args)
        except KeyboardInterrupt:
            return last
        except Exception as exc:  # noqa: BLE001
            print(f"[probe] crash: {type(exc).__name__}: {exc}", file=sys.stderr)
            last = max(last, EXIT_MC)
        time.sleep(max(15, args.interval))


if __name__ == "__main__":
    sys.exit(main())

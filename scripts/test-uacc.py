#!/usr/bin/env python3
"""Test UACC MCP server langsung — test tools dasar."""
import json
import subprocess
import sys
import time

def test_uacc():
    print("=" * 55)
    print("  🖥️  UACC v1.1.0 — Tool Test Suite")
    print("=" * 55)

    p = subprocess.Popen(
        ["/Users/zaryu/.hermes-portable/venv/bin/python", "-m", "uacc.mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    msg_id = 0

    def call(method, params=None):
        nonlocal msg_id
        msg_id += 1
        req = json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "method": method,
            "params": params or {},
        })
        p.stdin.write(req + "\n")
        p.stdin.flush()

    def read(timeout=5):
        deadline = time.time() + timeout
        resp_lines = []
        while time.time() < deadline:
            import select
            r, _, _ = select.select([p.stdout], [], [], 0.3)
            if r:
                line = p.stdout.readline()
                if line:
                    line = line.strip()
                    if line:
                        resp_lines.append(line)
        return resp_lines

    # 1. Initialize
    print("\n[1/5] Initialize MCP...")
    call("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "jcode-test", "version": "1.0"},
    })
    time.sleep(2)
    resp = read(3)
    if resp:
        print("  ✅ Connected — UACC MCP server running")
    else:
        print("  ⚠️  No init response, trying tools/list anyway")

    # 2. List tools
    print("\n[2/5] List tools...")
    call("tools/list")
    time.sleep(2)
    resp = read(5)
    tools = []
    for r in resp:
        try:
            data = json.loads(r)
            if "result" in data and "tools" in data["result"]:
                tools = data["result"]["tools"]
        except:
            pass

    if tools:
        print(f"  ✅ {len(tools)} tools registered")
        # Group by category
        cats = {}
        for t in tools:
            name = t["name"]
            prefix = name.split("_")[0] if "_" in name else name
            cats.setdefault(prefix, []).append(name)
        for cat, names in sorted(cats.items()):
            print(f"     {cat}: {len(names)} tools")
    else:
        print(f"  ⚠️  No tools found in response")
        # Show raw responses
        for r in resp:
            print(f"     {r[:200]}")

    # 3. Test get_system_info
    print("\n[3/5] System info...")
    call("tools/call", {"name": "get_system_info", "arguments": {}})
    time.sleep(3)
    resp = read(5)
    for r in resp:
        try:
            data = json.loads(r)
            if "result" in data:
                for c in data["result"].get("content", []):
                    if "text" in c:
                        txt = c["text"]
                        # Parse key info
                        for line in txt.split("\n"):
                            if any(k in line.lower() for k in ["platform", "system", "python", "host", "os", "version", "cpu", "memory", "arch"]):
                                print(f"     {line.strip()}")
                        break
        except:
            pass

    # 4. Test list_monitors
    print("\n[4/5] Monitor info...")
    call("tools/call", {"name": "list_monitors", "arguments": {}})
    time.sleep(3)
    resp = read(5)
    for r in resp:
        try:
            data = json.loads(r)
            if "result" in data:
                for c in data["result"].get("content", []):
                    if "text" in c:
                        print(f"     {c['text'][:300]}")
        except:
            pass

    # 5. Test get_mouse_position
    print("\n[5/5] Mouse position...")
    call("tools/call", {"name": "get_mouse_position", "arguments": {}})
    time.sleep(3)
    resp = read(5)
    for r in resp:
        try:
            data = json.loads(r)
            if "result" in data:
                for c in data["result"].get("content", []):
                    if "text" in c:
                        print(f"     {c['text'][:200]}")
        except:
            pass

    # Cleanup
    p.terminate()
    print("\n" + "=" * 55)
    print("  ✅ UACC Test Complete")
    print("=" * 55)

if __name__ == "__main__":
    test_uacc()

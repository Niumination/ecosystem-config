#!/usr/bin/env python3
"""
test-vision-endpoint.py — verifikasi model vision hidup di endpoint OpenAI-compatible
SEBELUM menulis config auxiliary.vision (atau fallback). Baca key dari data/.env.

Pakai:
  python3 test-vision-endpoint.py --base-url http://localhost:20128/v1 \
      --model gemini/gemini-3.7-flash --key-env NINE_ROUTER_API_KEY
  python3 test-vision-endpoint.py --base-url https://api.hcnsec.cn/v1 \
      --model DeepSeek-V4-Flash --key-env HUANCHENG_API_KEY

Keluar: 0 = vision OK, 1 = gagal. Print status + cuplikan respons.
Deteksi SSE: sebagian relay (9router/gratislonggar) balas `data: {...}` chunks walau
stream=false — parser ini menangani dua bentuk (JSON penuh atau SSE).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_ENV = "/Volumes/HermesAgent/HermesAgentUSB/data/.env"


def load_env_value(key_env: str, env_path: str) -> str:
    if not key_env:
        return ""
    # 1. lingkungan sudah ada
    v = os.environ.get(key_env, "")
    if v:
        return v
    # 2. baca dari file .env (format KEY=value / export KEY=value)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            line = line.lstrip("export ")
            k, _, val = line.partition("=")
            if k.strip() == key_env:
                return val.strip().strip('"').strip("'")
    return ""


def parse_response(raw: str) -> str:
    """Kembalikan teks dari JSON penuh atau SSE data: chunks."""
    if not raw.strip():
        return "(empty response)"
    if "data:" in raw:
        content_parts = []
        for chunk in raw.split("\n"):
            chunk = chunk.strip()
            if not chunk.startswith("data:"):
                continue
            data = chunk[5:].strip()
            if data == "[DONE]":
                break
            try:
                obj = json.loads(data)
                delta = obj.get("choices", [{}])[0].get("delta", {})
                content_parts.append(delta.get("content", ""))
            except json.JSONDecodeError:
                continue
        return "".join(content_parts) or "(SSE received, no content delta)"
    try:
        obj = json.loads(raw)
        return (obj.get("choices", [{}])[0].get("message", {})).get("content", json.dumps(obj)[:200])
    except json.JSONDecodeError:
        return raw[:300]


def main() -> int:
    ap = argparse.ArgumentParser(description="Test vision chat-completion terhadap endpoint")
    ap.add_argument("--base-url", required=True, help="mis. http://localhost:20128/v1")
    ap.add_argument("--model", required=True, help="model ID exact (case-sensitive!)")
    ap.add_argument("--key-env", default="", help="nama env var key (dibaca dari .env)")
    ap.add_argument("--env-path", default=DEFAULT_ENV)
    ap.add_argument("--image", default="", help="path PNG lokal untuk diuji (default: screenshot terakhir Hermes)")
    ap.add_argument("--timeout", type=int, default=90)
    args = ap.parse_args()

    img_path = args.image
    if not img_path:
        cache = Path("/Volumes/HermesAgent/HermesAgentUSB/data/cache/screenshots")
        shots = sorted(cache.glob("browser_screenshot_*.png"))
        if shots:
            img_path = str(shots[-1])
    if not img_path or not Path(img_path).is_file():
        print("ERR: tidak ada gambar untuk diuji (--image)")
        return 1

    key = load_env_value(args.key_env, args.env_path)
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"

    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    payload = {
        "model": args.model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Jawab singkat: OK."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                ],
            }
        ],
        "max_tokens": 50,
        "stream": False,
    }

    req = urllib.request.Request(
        args.base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode(),
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as r:
            raw = r.read().decode(errors="replace")
        print(f"STATUS {r.status} — model '{args.model}' vision OK")
        print("RESP:", parse_response(raw)[:300])
        return 0
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        print(f"HTTP {e.code} — model '{args.model}' GAGAL")
        print(body)
        return 1
    except Exception as e:
        print(f"ERR: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
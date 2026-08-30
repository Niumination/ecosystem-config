#!/usr/bin/env python3
"""
Model Checker — ekosistem Niumination
Cek semua model yang tersedia, test aksesibilitas, kategorikan gratis vs berbayar.
Hasil: laporan markdown + data JSON.
"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
ROUTER_URL = "http://127.0.0.1:20128"
ROUTER_MODELS = f"{ROUTER_URL}/v1/models"
ROUTER_CHAT = f"{ROUTER_URL}/v1/chat/completions"
DB_PATH = os.path.expanduser("~/.9router/db/data.sqlite")
REPORT_PATH = os.path.expanduser("~/Desktop/Niumination/scripts/model-checker-report.md")
DATA_PATH = os.path.expanduser("~/Desktop/Niumination/scripts/model-checker-data.json")

# ── helpers ──────────────────────────────────────────────────────────────────
def get_key():
    """Ambil NINE_ROUTER_API_KEY dari env atau .env."""
    key = os.environ.get("NINE_ROUTER_API_KEY", "")
    if not key:
        try:
            with open(os.path.expanduser("~/.hermes/.env")) as f:
                for line in f:
                    if line.startswith("NINE_ROUTER_API_KEY="):
                        key = line.strip().split("=", 1)[1]
                        break
        except:
            pass
    return key

def fetch_models():
    """Fetch model list dari 9router."""
    key = get_key()
    if not key:
        print("❌ NINE_ROUTER_API_KEY tidak ditemukan")
        sys.exit(1)
    req = urllib.request.Request(ROUTER_MODELS,
        headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.load(r)
    return [m["id"] for m in data["data"]]

def test_model(model_id, key, timeout_s=15):
    """
    Test model dengan request non-streaming.
    Handle response biasa (JSON) dan SSE (data: lines).
    """
    body = json.dumps({
        "model": model_id,
        "messages": [{"role": "user", "content": "x"}],
        "max_tokens": 5,
        "stream": False
    }).encode()
    req = urllib.request.Request(ROUTER_CHAT, data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {key}"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            raw = r.read().decode()
            elapsed = round((time.time() - t0) * 1000)
            # Cek apakah ini SSE
            if raw.startswith("data:"):
                # SSE format — parse chunks
                chunks = []
                for line in raw.split("\n"):
                    if line.startswith("data: ") and line != "data: [DONE]":
                        try:
                            chunk = json.loads(line[6:])
                            delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta:
                                chunks.append(delta)
                        except:
                            pass
                content = "".join(chunks)
                return {"ok": True, "latency_ms": elapsed, "content": content[:20],
                        "error": None, "stream": True, "chunks": len(chunks)}
            else:
                resp = json.loads(raw)
                content = resp.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {"ok": True, "latency_ms": elapsed, "content": content[:20],
                        "error": None, "stream": False, "chunks": 0}
    except urllib.error.HTTPError as e:
        elapsed = round((time.time() - t0) * 1000)
        return {"ok": False, "latency_ms": elapsed, "content": "",
                "error": f"HTTP {e.code}", "stream": False, "chunks": 0}
    except Exception as e:
        elapsed = round((time.time() - t0) * 1000)
        return {"ok": False, "latency_ms": elapsed, "content": "",
                "error": str(e)[:50], "stream": False, "chunks": 0}

# ── kategorisasi model ───────────────────────────────────────────────────────
def categorize_model(model_id, is_ok, latency_ms, error):
    """
    Kategorikan model berdasarkan provider dan status.
    Gratis/free: gemini (AI Studio free), github (Copilot free), ag (Antigravity free tier)
    Berbayar/kuota: kiro (Kiro subscription), nvidia (NIM paid)
    """
    prov = model_id.split("/")[0]

    # Status dasar
    if not is_ok:
        return {"category": "not_accessible", "reason": error or "gagal"}

    # Provider-based categorization
    if prov == "gemini":
        # Google AI Studio: gratis dengan kuota harian (gemini-3.5-flash-lite paling stabil)
        if "lite" in model_id:
            return {"category": "free", "tier": "gratis", "notes": "AI Studio free, kuota harian 무제한"}
        return {"category": "free", "tier": "gratis_dengan_kuota", "notes": "AI Studio free, ada batas kuota"}

    if prov == "github":
        # GitHub Copilot free tier: ada batas penggunaan harian
        return {"category": "free", "tier": "gratis_copilot", "notes": "GitHub Copilot free tier"}

    if prov == "ag":
        # Antigravity: gratis via OAuth, ada kuota
        return {"category": "free", "tier": "gratis_antigravity", "notes": "Antigravity gratis via OAuth"}

    if prov == "kr":
        # Kiro: subscription-based (mungkin ada free tier terbatas)
        if "qwen3" in model_id or "deepseek" in model_id:
            return {"category": "free_tier", "tier": "gratis_terbatas", "notes": "Kiro — model tertentu gratis terbatas"}
        return {"category": "paid", "tier": "berbayar", "notes": "Kiro subscription"}

    if prov == "nvidia":
        return {"category": "paid", "tier": "berbayar_nim", "notes": "NVIDIA NIM — berbayar"}

    if prov == "ollama":
        return {"category": "unknown", "tier": "tidak_diketahui", "notes": "Ollama cloud"}

    if prov == "kimi":
        return {"category": "free", "tier": "gratis_kimi", "notes": "Kimi — gratis tapi sering error"}

    return {"category": "unknown", "tier": "tidak_diketahui", "notes": "provider tidak dikenal"}

# ── main ─────────────────────────────────────────────────────────────────────
def main():
    print("═" * 72)
    print("  🌟 MODEL CHECKER — Ekosistem Niumination")
    print(f"  {datetime.now().strftime('%d %b %Y %H:%M')} WIB")
    print("═" * 72)
    print()

    # Step 1: Fetch models
    print("📡 Step 1: Fetch model list dari 9router...")
    try:
        models = fetch_models()
    except Exception as e:
        print(f"❌ Gagal fetch: {e}")
        sys.exit(1)
    print(f"   Dapat {len(models)} model IDs")
    print()

    # Step 2: Test all models
    print("🧪 Step 2: Testing semua model...")
    key = get_key()
    results = {}
    for i, mid in enumerate(models):
        r = test_model(mid, key)
        results[mid] = r
        prov = mid.split("/")[0]
        status = "✅" if r["ok"] else "❌"
        lat = r["latency_ms"]
        error = r["error"] or ""
        print(f"  [{i+1:02d}/{len(models):02d}] {status} {mid:45s}  {lat:5d}ms  {error}")

    # Step 3: Kategorisasi
    print()
    print("📊 Step 3: Kategorisasi model...")
    categories = {"free": [], "free_tier": [], "paid": [], "not_accessible": [], "unknown": []}
    for mid, r in results.items():
        cat = categorize_model(mid, r["ok"], r["latency_ms"], r["error"])
        cat["model_id"] = mid
        cat["latency_ms"] = r["latency_ms"]
        cat["error"] = r["error"]
        cat["stream"] = r["stream"]
        categories.setdefault(cat["category"], []).append(cat)

    # Step 4: Report
    print()
    print("📝 Step 4: Membuat laporan...")
    report_lines = []
    report_lines.append(f"# Model Checker Report — {datetime.now().strftime('%d %b %Y %H:%M')} WIB")
    report_lines.append("")
    report_lines.append(f"Server: 9router (127.0.0.1:20128)")
    report_lines.append(f"Total model di catalog: {len(models)}")
    report_lines.append(f"Model accessible: {sum(1 for r in results.values() if r['ok'])}")
    report_lines.append(f"Model inaccessible: {sum(1 for r in results.values() if not r['ok'])}")
    report_lines.append("")

    # Per-provider summary
    by_prov = {}
    for mid, r in results.items():
        prov = mid.split("/")[0]
        by_prov.setdefault(prov, []).append((mid, r))

    report_lines.append("## Per Provider Summary")
    report_lines.append("")
    for prov in sorted(by_prov):
        entries = by_prov[prov]
        ok = [e for e in entries if e[1]["ok"]]
        fail = [e for e in entries if not e[1]["ok"]]
        lats = [e[1]["latency_ms"] for e in ok]
        avg = round(sum(lats)/len(lats)) if lats else 0
        report_lines.append(f"### {prov.upper()} ({len(entries)} models)")
        report_lines.append(f"- **OK:** {len(ok)} | **FAIL:** {len(fail)}")
        if lats:
            report_lines.append(f"- Latency: min={min(lats)}ms, avg={avg}ms, max={max(lats)}ms")
        report_lines.append("")

    # Model gratis / free tier
    report_lines.append("## 🆓 Model GRATIS / Free Tier (bisa dipakai tanpa biaya)")
    report_lines.append("")
    free_models = sorted(categories.get("free", []) + categories.get("free_tier", []),
                         key=lambda c: c["latency_ms"])
    if free_models:
        report_lines.append("| Model | Provider | Latency | Keterangan |")
        report_lines.append("|-------|----------|---------|------------|")
        for m in free_models:
            report_lines.append(f"| {m['model_id']} | {m['model_id'].split('/')[0]} | {m['latency_ms']}ms | {m.get('notes', '')} |")
        report_lines.append("")
        report_lines.append(f"**Total:** {len(free_models)} model gratis")
    else:
        report_lines.append("*Tidak ada model gratis yang accessible*")
    report_lines.append("")

    # Model berbayar / kuota besar
    report_lines.append("## 💰 Model Berbayar / Kuota Besar")
    report_lines.append("")
    paid_models = sorted(categories.get("paid", []), key=lambda c: c["latency_ms"])
    if paid_models:
        report_lines.append("| Model | Provider | Latency | Keterangan |")
        report_lines.append("|-------|----------|---------|------------|")
        for m in paid_models:
            report_lines.append(f"| {m['model_id']} | {m['model_id'].split('/')[0]} | {m['latency_ms']}ms | {m.get('notes', '')} |")
        report_lines.append("")
        report_lines.append(f"**Total:** {len(paid_models)} model berbayar")
    else:
        report_lines.append("*Tidak ada model berbayar yang accessible*")
    report_lines.append("")

    # Model tidak accessible
    report_lines.append("## ❌ Model Tidak Accessible")
    report_lines.append("")
    fail_models = sorted(categories.get("not_accessible", []), key=lambda c: c["model_id"])
    if fail_models:
        report_lines.append("| Model | Provider | Error |")
        report_lines.append("|-------|----------|-------|")
        for m in fail_models:
            report_lines.append(f"| {m['model_id']} | {m['model_id'].split('/')[0]} | {m.get('error', 'unknown')} |")
        report_lines.append("")
        report_lines.append(f"**Total:** {len(fail_models)} model gagal")
    report_lines.append("")

    # Rekomendasi
    report_lines.append("## 🎯 Rekomendasi (berdasarkan latency + ketersediaan)")
    report_lines.append("")
    all_ok = sorted([c for c in categories.get("free", []) + categories.get("free_tier", []) +
                     categories.get("paid", [])], key=lambda c: c["latency_ms"])
    report_lines.append("### Cepat (< 1000ms)")
    report_lines.append("")
    for m in all_ok[:5]:
        report_lines.append(f"- **{m['model_id']}** ({m['latency_ms']}ms) — {m.get('notes', '')}")
    report_lines.append("")
    report_lines.append("### Vision-capable (bisa proses gambar)")
    report_lines.append("")
    vision_ok = [c for c in all_ok if c['model_id'].startswith(('ag/gemini', 'gemini/gemini', 'gh/gpt-4o', 'gh/gpt-4.1', 'kr/claude'))]
    for m in sorted(vision_ok, key=lambda c: c["latency_ms"])[:5]:
        report_lines.append(f"- **{m['model_id']}** ({m['latency_ms']}ms)")
    report_lines.append("")

    # Write report
    report_text = "\n".join(report_lines)
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        f.write(report_text)
    print(f"   Laporan tersimpan: {REPORT_PATH}")

    # Save JSON data
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "router": ROUTER_URL,
        "total_models": len(models),
        "results": {mid: {
            "ok": r["ok"],
            "latency_ms": r["latency_ms"],
            "error": r["error"],
            "stream": r["stream"],
            "category": categorize_model(mid, r["ok"], r["latency_ms"], r["error"])
        } for mid, r in results.items()}
    }
    with open(DATA_PATH, "w") as f:
        json.dump(json_data, f, indent=2)
    print(f"   Data JSON tersimpan: {DATA_PATH}")
    print()

    # Print summary ke stdout
    print("═" * 72)
    print("  📋 RINGKASAN")
    print("═" * 72)
    print()
    print(f"Total model: {len(models)}")
    print(f"✅ Accessible: {sum(1 for r in results.values() if r['ok'])}")
    print(f"❌ Inaccessible: {sum(1 for r in results.values() if not r['ok'])}")
    print()
    print("Kategori:")
    for cat in ["free", "free_tier", "paid", "not_accessible", "unknown"]:
        count = len(categories.get(cat, []))
        label = {"free": "Gratis", "free_tier": "Free Tier", "paid": "Berbayar",
                 "not_accessible": "Tidak Accessible", "unknown": "Tidak Diketahui"}[cat]
        print(f"  {label}: {count}")
    print()
    print(f"Laporan lengkap: {REPORT_PATH}")
    print("═" * 72)

if __name__ == "__main__":
    main()

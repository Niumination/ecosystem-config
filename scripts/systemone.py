#!/usr/bin/env python3
"""
systemone.py — Pemanggil Opinion-based Decision Model (Jev) via 9router /systemone
===============================================================================
Klasifikasi keputusan (choice / noul). BUKAN agen, BUKAN eksekutor.

DESIGN KESELAMATAN (baca sebelum dipakai):
  1. Tidak ada jalur eksekusi. Satu-satunya efek samping = HTTP POST ke
     /systemone (klasifikasi) + 1 baris audit log lokal. Tidak bisa beli tiket,
     tidak bisa main game, tidak bisa jalankan perintah.
  2. Fail-closed. Kill switch, disable file, dan budget cap di chilly:
     gate yang gagal = tidak jadi memanggil, bukan meloloskan.
  3. Tidak ada auto-trigger. Tidak ada daemon, tidak terdaftar cron, tidak
     dipanggil Hermes secara otomatis. Hanya jalan bila manusia memanggil
     dengan tangan.
  4. Rahasia tidak pernah dicetak. API key dibaca dari env, hanya dipakai
     sebagai header, tidak masuk argumen/log/output.
  5. Cost cap per panggilan. Di-ATAS cap = tolak sebelum request.

Exit code: 0 = ok, 1 = error/ditolak, 2 = usage salah.

Mode:
  (default)            Klasifikasi satu pertanyaan (dry-run: hanya prints)
  --q KLABEL::TEKS     Tambah pertanyaan (boleh berulang, 1 request)
  --noul               Pertanyaan tipe noul (ya/tidak) untuk --q terakhir
  --crit K::DESKRIPSI  Opsi + deskripsi untuk mode choice (boleh berulang)
  --context TEKS       Konteks tambahan (state.messages)
  --file PATH          Ambil teks pertanyaan dari file/stdin ("-")
  --budget USD         Cap biaya 1 panggilan (default 0.01)
  --json               Output JSON mentah
  --health             Cek endpoint + model + provider, tanpa memanggil
  --allow              WAJIB. Tanpa flag ini skrip hanya menampilkan rancangan.

  --allow              Wajib untuk benar-benar memanggil. Tanpa itu: dry-run.

Kill switch (berprioritas dari atas):
  export SYSTEMONE_DISABLED=1        # matikan total
  ~/.hermes/systemone.disabled        # file kill switch (isi bebas)
"""
import json, os, pathlib, re, sys, time, urllib.error, urllib.request

BASE = os.environ.get("NINE_ROUTER_URL", "http://localhost:20128")
MODEL = os.environ.get("SYSTEMONE_MODEL", "openrouter/typesafe/jev-1.13")
MAX_Q = 10          # abuse: jangan bombardedir endpoint
MAX_CHARS = 8000    # abuse: jangan kirim dokumen penuh ke pihak ketiga
DISABLE_FILE = pathlib.Path.home() / ".hermes/systemone.disabled"
LOG = pathlib.Path.home() / ".hermes/logs/systemone-audit.log"

DEFAULT_BUDGET = 0.01
# Harga jev-1.13 (usageHistory 2026-09-26: 386 tok = 0.0000162 USD).
# Dipakai hanya sebagai patokan保守 refuse, bukan penagihan.
COST_PER_1K_IN = 0.00005
COST_PER_1K_OUT = 0.00020


def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def gate():
    """Semua gate安全. Gagal = TOLAK (fail-closed), bukan lolos."""
    # 1. Kill switch env
    if os.environ.get("SYSTEMONE_DISABLED", "").strip() not in ("", "0", "false"):
        die("SYSTEMONE_DISABLED aktif — skrip dimatikan.")
    # 2. Kill switch file
    if DISABLE_FILE.exists():
        die(f"Kill switch aktif: {DISABLE_FILE} ada. Hapus file itu untuk mengaktifkan.")
    # 3. Opt-in eksplisit
    if "--allow" not in sys.argv:
        return False
    return True


def load_key():
    env = pathlib.Path.home() / ".hermes/.env"
    if not env.exists():
        die("~/.hermes/.env tidak ada.")
    for line in env.read_text().splitlines():
        if line.startswith("NINE_ROUTER_API_KEY="):
            k = line.split("=", 1)[1].strip().strip('"').strip("'")
            if k:
                return k
    die("NINE_ROUTER_API_KEY tidak ada di ~/.hermes/.env.")


def read_text(path):
    if path == "-":
        return sys.stdin.read()
    p = pathlib.Path(path).expanduser()
    if not p.exists():
        die(f"file tidak ada: {p}")
    if p.stat().st_size > MAX_CHARS * 4:
        die(f"file terlalu besar ({p.stat().st_size} B). Maks {MAX_CHARS * 4} B.")
    return p.read_text()


def build_questions(qs, crits, noul_flags):
    questions = {}
    for i, (label, text) in enumerate(qs):
        if noul_flags[i]:
            questions[label] = {"type": "noul", "instructions": text}
        else:
            if not crits:
                die(f"'{label}' mode choice butuh --crit K::DESKRIPSI minimal 1.")
            questions[label] = {
                "type": "choice",
                "instructions": text,
                "criteria": {k: v for k, v in crits},
            }
    return questions


def budget_refuse(state_text, n_questions):
    est_in = (len(state_text) // 4) + 50
    est_out = 60 * n_questions
    est = est_in / 1000 * COST_PER_1K_IN + est_out / 1000 * COST_PER_1K_OUT
    return est, est_in


def audit(line, ok):
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} ok={ok} {line}\n")
        os.chmod(LOG, 0o600)
    except Exception:
        pass


def call(body, key):
    req = urllib.request.Request(
        f"{BASE}/systemone",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]
    except Exception as e:
        return 0, f"{type(e).__name__}: {str(e)[:200]}"


def health(key):
    print(f"endpoint : {BASE}/systemone")
    print(f"model    : {MODEL}")
    print(f"kill sw  : env={'MATI' if os.environ.get('SYSTEMONE_DISABLED') else 'nyala'}"
          f" file={'MATI' if DISABLE_FILE.exists() else 'tidak ada'}")
    try:
        with urllib.request.urlopen(f"{BASE}/v1/models", timeout=10) as r:
            ms = [m["id"] for m in json.loads(r.read()).get("data", [])]
        hit = [m for m in ms if "jev" in str(m)]
        print(f"katalog  : {len(ms)} model, jev={'ADA ' + str(hit) if hit else 'TIDAK ADA'}")
    except Exception as e:
        print(f"katalog  : GAGAL {type(e).__name__}: {str(e)[:100]}")
    st, resp = call({
        "model": MODEL,
        "state": {"messages": [{"role": "user", "content": "ping"}]},
        "questions": {"ping": {"type": "noul", "instructions": "Apakah ini hidup?"}},
    }, key)
    print(f"probe    : HTTP {st}")
    if st == 200 and isinstance(resp, dict):
        a = resp.get("answers", {}).get("ping", {})
        audit(f"HEALTH cost={resp.get('usage', {}).get('cost')}", True)
        print(f"jawaban  : noul skor={a.get('noul')}, cost={resp.get('usage', {}).get('cost')}")
        return 0
    audit(f"HEALTH-FAIL http={st}", False)
    print(f"detail   : {str(resp)[:250]}")
    return 1


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)

    live = gate()  # fail-closed; False = dry-run

    key = load_key()  # validasi key ada, tidak pernah dicetak

    if "--health" in argv:
        sys.exit(health(key))

    qs, crits, noul_flags = [], [], []
    context, budget, as_json, src = [], DEFAULT_BUDGET, False, None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--q":
            val = argv[i + 1] if i + 1 < len(argv) else ""
            if "::" not in val:
                die("format --q = KLABEL::TEKS")
            lbl, txt = val.split("::", 1)
            if src:
                txt = read_text(src) + "\n\n" + txt
            qs.append((lbl, txt)); noul_flags.append(False)
        elif a == "--noul":
            if not noul_flags:
                die("--noul harus setelah --q")
            noul_flags[-1] = True
        elif a == "--crit":
            val = argv[i + 1] if i + 1 < len(argv) else ""
            if "::" not in val:
                die("format --crit = OPSI::DESKRIPSI")
            k, v = val.split("::", 1)
            crits.append((k, v))
        elif a == "--context":
            context.append(argv[i + 1] if i + 1 < len(argv) else "")
        elif a == "--file":
            src = argv[i + 1] if i + 1 < len(argv) else ""
        elif a == "--budget":
            budget = float(argv[i + 1]) if i + 1 < len(argv) else DEFAULT_BUDGET
        elif a == "--json":
            as_json = True
        i += 1

    if not qs:
        die("tidak ada pertanyaan. Contoh: --q 'label::apa isi pesan ini?' --crit a::desc --crit b::desc --allow")

    # Gate abuse
    if len(qs) > MAX_Q:
        die(f"terlalu banyak pertanyaan ({len(qs)}). Maks {MAX_Q}.")
    if len(crits) > 20:
        die(f"terlalu banyak opsi ({len(crits)}). Maks 20.")
    try:
        if budget <= 0:
            die("budget harus > 0.")
    except ValueError:
        die("budget harus angka.")

    msgs = [{"role": "user", "content": c} for c in context] + \
           [{"role": "user", "content": t} for _, t in qs]
    body = {"model": MODEL, "state": {"messages": msgs}, "questions": build_questions(qs, crits, noul_flags)}

    est, est_in = budget_refuse(json.dumps(body), len(qs))
    if est > budget:
        audit(f"REFUSE est={est:.6f} cap={budget}", False)
        die(f"estimasi biaya {est:.6f} USD > cap {budget} USD. Tolak (fail-closed). Naikkan --budget bila memang mau.")

    if not live:
        print("DRY-RUN — tidak ada request terkirim. Tambahkan --allow untuk memanggil.")
        print(f"  model    : {MODEL}")
        print(f"  pertanyaan: {len(qs)} ({sum(noul_flags)} noul, {len(qs)-sum(noul_flags)} choice)")
        print(f"  estimasi  : {est:.6f} USD (cap {budget})")
        print(f"  body      : {json.dumps(body, ensure_ascii=False)[:400]}")
        return 0

    st, resp = call(body, key)
    if st == 200 and isinstance(resp, dict):
        audit(f"OK q={len(qs)} in~{est_in} cost={resp.get('usage', {}).get('cost')}", True)
        if as_json:
            print(json.dumps(resp, ensure_ascii=False, indent=2))
        else:
            for lbl, a in resp.get("answers", {}).items():
                print(f"\n{lbl}:")
                if a.get("type") == "noul" or ("noul" in a and "choice" not in a):
                    # noul balik SKOR float 0..1 (bukan choice/confidence)
                    n = a.get("noul")
                    print(f"  skor noul: {n}  (ya={float(n or 0) >= 0.5})")
                else:
                    print(f"  pilihan   : {a.get('choice')}")
                    print(f"  confidence: {a.get('confidence')}")
                    print(f"  probabilitas: {json.dumps(a.get('probabilities', {}), ensure_ascii=False)}")
            u = resp.get("usage", {})
            print(f"\n  token: in={u.get('input_tokens')} out={u.get('output_tokens')} cost={u.get('cost')} USD")
        return 0

    audit(f"FAIL http={st}", False)
    die(f"HTTP {st}: {str(resp)[:300]}", 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Gate penulis `.env` — menolak skrip yang menimpa credential store tanpa backup.

    python3 scripts/scan-env-writers.py [path ...]
    python3 scripts/scan-env-writers.py --self-test

Latar (3 Okt 2026): `rotate.py` menulis ulang `~/.hermes/.env` untuk mengganti 3
kunci CamoFox, lalu MENYIMPAN ULANG hanya kunci yang disebut dalam tuple KEYS.
23 kunci lain (Telegram, 9router, Vercel, OpenRouter, ...) hilang tanpa satu
pesan pun. Verifikasi skrip hanya membandingkan 3 kunci itu, jadi lolos. File
file hasilnya hanya berisi 4 kunci; gateway crash-loop 61x karena
`TELEGRAM_BOT_TOKEN` hilang.

Self-check skrip rotasi hanya membandingkan kunci yang SEDANG DIROTAASI — bukan
"tidak ada yang hilang". Gate ini menangkap kelas yang lebih luas: file yang
MENULIS `.env` tanpa mengambil salinan lebih dulu.

Exit 0 = aman. Exit 1 = ditolak. Nilai kredensial tidak pernah dicetak.
"""
import re
import subprocess
import sys
from pathlib import Path

# ── apa yang dianggap "menulis" ────────────────────────────────────────────────
# Sengaja sempit: hanya mode yang menimpa/menambah isi, bukan `set -a; . .env`
# (membaca) maupun redirection ke file .env.example / template / .bak / .dist.
WRITE_PATTERNS = [
    # open(...).write  /  open(..., 'w'|'a')
    ("python_open_write", re.compile(r"open\s*\(\s*[^\n]{0,80}?\.env\b[^\n]{0,40}?['\"][wa]['\"]")),
    ("python_write_text", re.compile(r"\.write_text\s*\(\s*[^\n]{0,60}?\.env")),
    # shell/heredoc: > atau >> ke path .env
    ("shell_redirect", re.compile(r"(?<![0-9])>>?\s*[\"']?[^\n\"'|>]{0,80}?\.env(?![.\w'\"])[\"']?")),
    # cp / mv yang menimpa sumber lain ke .env
    ("cp_to_env", re.compile(r"\b(?:cp|mv|install)\b[^\n]{0,120}?\.env(?![.\w])")),
    # tee
    ("tee_to_env", re.compile(r"\btee\b[^\n]{0,120}?\.env(?![.\w])")),
]

# ── apa yang dianggap "sudah aman" ───────────────────────────────────────────
# Suatu file aman bila DI DALAMNYA ada operasi yang jelas mengambil salinan
# sebelum menulis. Cukup satu; tidak perlu membuktikan urutan (POSIX tak punya
# analisis aliran di gate ini) — pesan error menyebut beide.
BACKUP_MARKERS = re.compile(
    r"""(
        \.bak                       # suffix .bak (milik repo)
      | backup                    # kata backup / pre-ghtoken / hermes\.env\.bak
      | mktemp                    # pola add-gh-token.sh: tulis ke tmp lalu cp
      | shutil\.copy
      | Path\(.*\)\.read_text    # baca-semua-lalu-tulis ulang (rotate.py safe)
    )""",
    re.IGNORECASE | re.VERBOSE,
)

# Path yang TIDAK pernah boleh dianggap credential store ikut-raster (False positive killer)
READ_ONLY_HINT = re.compile(
    # Baris yang MEMBACA .env sah saja: `set -a; . .env` (memuat ke env), dan
    # `open(path)` tanpa mode (default 'r'). Modus 'w'/'a' tidak ikut cocok
    # karena pola `open\s*\([^)]*['"]?[wa]['"]?\)` di bawah mensyaratkan REITANG.
    r"""(
        set\s+-a\s*;\s*\.\s+\S
      | \bopen\s*\(\s*[^\n)]*\.env[^\n)]*\)        # open('...env') — tanpa mode
      | \.read_text\s*\(
      | \bgrep\b
      | \bcat\b
      | ^\s*\.\s+\S
    )""",
    re.VERBOSE | re.IGNORECASE,
)

# Pass 2 (target tak langsung): berkas menyebut credential store secara literal
# DAN menulis ulang seluruh isi file. Dua fakta itu harus sama-sama ada -- satu
# saja terlalu longgar (dokumen yang menyebut `.env` adalah file yang sicher).
ENV_LITERAL = re.compile(r"""[~$/"']*\.hermes/\.env\b|\bHERMES_HOME\b[^\n]{0,20}/\.env\b""")
WHOLE_FILE_WRITE = re.compile(
    # WAJIB re.VERBOSE: pola ini punya komentar inline, dan tanpa flag itu `#`
    # diperlakukan sebagai literal yang harus cocok -- sehingga tiap alternatif
    # gagal. BACKUP_MARKERS di atas tidak tersentuh karena sudah memakai flag.
    # Tanda kutip opsional DI LUAR kelas: `['"][wa]['"]` salah -- '[' dibaca
    # sebagai anggota kelas sehingga `open(V, 'w')` tak pernah cocok.
    r"""(
        open\s*\(\s*[A-Za-z_][A-Za-z0-9_.]*\s*,\s*['"]?[wa]['"]?   # open(VAR, 'w')
      | \.write_text\s*\(                                        # Path(VAR).write_text
      | >{1,2}\s*['"]?\$[A-Za-z_][A-Za-z0-9_]*['"]?               # > "$ENV_FILE"
      | tee\s[^\n]{0,40}['"]?\$[A-Za-z_][A-Za-z0-9_]*['"]?
    )""",
    re.VERBOSE,
)

# Menentukan bahwa variabel yang ditulis ITU credential store. Dua bukti harus
# sama-sama ada: (a) variabel di-assign dari path .env, (b) namanya env-ish.
# Tanpa keduanya, singkatan seperti REPORT_PATH / output_file bukan credential
# store -- tiga skrip di repo ini hanya MEMBACA .env lalu menulis laporan, dan
# pola longgar akan menandai semuanya (52 FP pada scan-stray-glyphs v1).
ENV_VAR_ASSIGNED_FROM_ENV = re.compile(
    r"""^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*[furb]{0,2}['"][^\n]{0,40}?\.hermes/\.env""",
    re.MULTILINE,
)
ENVISH_NAME = re.compile(r"(?i)^(env|env_?file|dotenv|hermes_?env|cred_?file|credentials?_?file|envpath|env_path)$")


def _env_targets(text: str):
    """Variable names assigned from the credential-store path."""
    return {m.group(1) for m in ENV_VAR_ASSIGNED_FROM_ENV.finditer(text)}


def _writes_via(text: str, targets: set) -> bool:
    """True when a whole-file write targets one of those variables."""
    for t in targets:
        pats = [
            rf"open\s*\(\s*{re.escape(t)}\s*,\s*['\"]?[wa]['\"]?",
            rf"{re.escape(t)}\s*\)?\.write_text\s*\(",
            rf">{{1,2}}\s*['\"]?\$\{{?{re.escape(t)}\b",
            rf"\btee\b[^\n]{{0,40}}['\"]?\$\{{?{re.escape(t)}\b",
            rf"\b(?:cp|mv|install)\b[^\n]{{0,120}}['\"]?\$\{{?{re.escape(t)}\b",
        ]
        for p in pats:
            if re.search(p, text):
                return True
    return False


def WRITE_VIA_ENV_TARGET(text: str) -> bool:  # noqa: N802 — dipanggil seperti konstanta pola
    return _writes_via(text, {t for t in _env_targets(text) if ENVISH_NAME.match(t)})

SUFFIXES = (".sh", ".py", ".bash", ".zsh", ".bashrc", ".zshrc", ".profile")

# Direktori yang isinya bukan skrip milik kita. Tanpa pengecualian, rglob mengitra
# node_modules/.venv dan repo anak; scan penuh repo root jadi >400 detik.
SKIP_DIRS = {
    "node_modules", ".git", ".venv", "venv", "dist", "build", ".next",
    "__pycache__", ".cache", "target", "vendor", ".tox", "coverage",
    "credentials", "l2-data", "archive", "sandbox", "inactive-2026-09",
}


def looks_like_write(text: str):
    """Return the label of a credential-store write, or None.

    Two passes, because the 3 Okt incident wrote through a VARIABLE
    (`ENV = f'{HOME}/.hermes/.env'` then `open(ENV, 'w')`) -- a literal-path
    pattern alone sees no target there and the whole-file rewrite slips through.
    """
    # Pass 1: target literal (shell redirection, tee, cp/mv ke .env, open(...,'w')).
    for label, pat in WRITE_PATTERNS:
        for m in pat.finditer(text):
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.end())
            line = text[line_start:line_end if line_end != -1 else len(text)]
            # redirection ke .env.example / .template / .sample / .dist / .bak bukan write
            if re.search(r"\.env\.(example|sample|template|dist|bak|new|tmp)", line):
                continue
            # Baris yang jelas membaca .env (bukan menulisnya) bukan temuan.
            if READ_ONLY_HINT.search(line) and not re.search(r">{1,2}\s*|\btee\b|\bcp\b|\bmv\b", line):
                continue
            return label

    # Pass 2: target tak langsung. Berkas ini menyebut credential store secara literal
    # DAN melakukan write seluruh-isi ke suatu target; destination-nya
    # bisa berupa variabel, jadi hanya gabungan dua fakta yang boleh menandai.
    if not ENV_LITERAL.search(text):
        return None
    if not WHOLE_FILE_WRITE.search(text):
        return None
    # '\.write_text(' / 'open(VAR,'w')' bisa menunjuk file OUTPUT lain (laporan,
    # data cache). Kalau satu-satunya cara skrip menyentuh .env adalah MEMBACANYA,
    # skrip itu bukan penulis credential store -- biarkan lewat.
    if not WRITE_VIA_ENV_TARGET(text):
        return None
    return "indirect_target_whole_file_write"


def scan(path: Path):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    label = looks_like_write(strip_comments_and_docs(text))
    if not label:
        return None
    if BACKUP_MARKERS.search(text):
        return None
    return label


# ── pisahkan kode dari komentar & docstring ─────────────────────────────────
# Gate ini hanya boleh menilai PERILAKU. Contoh yang nyata: docstring
# `probe-tool-calling.py` memuat contoh shell `set -a; . ~/.hermes/.env`
# sebagai teks; tanpa pemisahan ini ia terbaca sebagai skrip pembaca yang
# entah menulis -- false positive ke-4 yang ditemukan saat scan repo penuh.
def strip_comments_and_docs(src: str) -> str:
    """Blank comments and bare-string statements; keep inline strings visible.

    Yang diblokir: komentar, dan string yang berdiri sendiri sebagai pernyataan
    (docstring modul/fungsi). Yang SENGAJA dibiarkan: string di dalam baris
    kode -- terutama f-string path seperti `f'{HOME}/.hermes/.env'`. Bila string
    inline ikut diblokir, `rotate.py` (file yang caused insiden) tak akan pernah
    terdeteksi karena target tulisnya justru sebuah string.
    """
    import io
    import tokenize

    lines = src.splitlines(keepends=True)
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError):
        # Python rusak / bukan Python (sh) — biarkan apa adanya; gate ini hanya
        # mengurangi false positive, tak boleh jadi penghalang parsing.
        return src

    significant = [t for t in toks
                   if t.type not in (tokenize.NL, tokenize.NEWLINE,
                                     tokenize.INDENT, tokenize.DEDENT,
                                     tokenize.COMMENT, tokenize.ENCODING)]
    for tok in toks:
        if tok.type == tokenize.COMMENT:
            pass
        elif tok.type == tokenize.STRING and _is_standalone_string(toks, tok, significant):
            pass
        else:
            continue
        for lineno in range(tok.start[0], tok.end[0] + 1):
            line = lines[lineno - 1]
            a = tok.start[1] if lineno == tok.start[0] else 0
            b = tok.end[1] if lineno == tok.end[0] else len(line)
            lines[lineno - 1] = line[:a] + " " * max(0, b - a) + line[b:]
    return "".join(lines)


def _is_standalone_string(toks, tok, significant) -> bool:
    """True when the string is a whole statement (a docstring), not inline."""
    try:
        pos = significant.index(tok)
    except ValueError:
        return False
    prev = significant[pos - 1] if pos > 0 else None
    nxt = significant[pos + 1] if pos + 1 < len(significant) else None
    if prev is not None and prev.end[0] == tok.start[0]:
        return False   # ada token lain di baris yang sama -> inline
    if nxt is not None and nxt.start[0] == tok.end[0]:
        return False   # ada token lain setelahnya di baris yang sama -> inline
    return True


def self_test():
    CAMO = "CAMOFOX_" + "API" + "_KEY"
    cases = [
        # (nama, isi, harus_ditolak?)
        # Regresi 3 Okt 2026, bentuk aslinya (msg 76411). Menyeluruhkan K=V yang
        # namanya bukan dalam KEYS karena cabang `else` tak terjangkau -- 23 kunci
        # hilang. Target ditulis lewat variabel, jadi definisi ENV ikut wajib ada
        # di fixture; tanpanya pola tak bisa melihat titik tulisnya.
        ("rotate_buggy",
         """ENV = f'{HOME}/.hermes/.env'
for line in f:
    s = line.rstrip('\\n')
    if '=' in s and not s.lstrip().startswith('#'):
        k = s.split('=', 1)[0].strip()
        if k in KEYS:
            order.append(k)
            data.append((k, s.split('=', 1)[1]))
    else:
        data.append((None, s))
with open(ENV, 'w') as f:
    f.write('\\n'.join(out) + '\\n')""", True),
        ("add_gh_token_safe",
         """TMP="$(mktemp)"
grep -v '^GH_TOKEN=' "$ENV_FILE" > "$TMP" || true
cp "$TMP" "$ENV_FILE"
chmod 600 "$ENV_FILE\"""", False),
        ("read_only_source",
         "set -a; . \"$HOME/.hermes/.env\"; set +a", False),
        ("example_file", f"{CAMO}=" + "sk-your-key-here" + " > .env.example", False),
        ("redirection_no_backup",
         "printf 'FOO=1\\n' >> ~/.hermes/.env", True),
        ("cp_from_backup",
         "cp -p /tmp/hermes.env.bak /tmp/hermes.env.pre-ghtoken", False),
        ("tee_no_backup", "echo 'FOO=1' | tee -a ~/.hermes/.env", True),
        ("doc_mention_only", "# rotate writes .env then read_text to verify", False),
    ]
    ok = 0
    for name, body, should_flag in cases:
        p = Path(__file__).with_name(f"._envw_test_{name}.sh")
        try:
            p.write_text(body, encoding="utf-8")
            got = scan(p) is not None
        finally:
            p.unlink(missing_ok=True)
        status = "OK " if got == should_flag else "FAIL"
        if got == should_flag:
            ok += 1
        else:
            print(f"  {status} {name}: got flagged={got}, expected={should_flag}")
    print(f"env-writer self-test: {ok}/{len(cases)} lulus")
    return 0 if ok == len(cases) else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()

    if "--staged" in argv:
        # Hanya berkas yang akan masuk commit. Memindai seluruh working tree
        # untuk pre-commit terlalu lambat (92 detik di repo root) dan menjebak
        # commit karena skrip rusak yang belum disentuh commit ini.
        out = subprocess.run(
            ["git", "-c", "core.quotepath=false", "diff", "--cached",
             "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True).stdout
        targets = [Path(f) for f in out.splitlines()
                   if f.strip() and Path(f).suffix in SUFFIXES]
        if not targets:
            return 0
    else:
        targets = [Path(a) for a in argv[1:]] or [Path.cwd()]

    findings = []
    for t in targets:
        if t.is_dir():
            for f in sorted(t.rglob("*")):
                if SKIP_DIRS & set(f.relative_to(t).parts[:-1]):
                    continue
                if f.is_file() and (f.suffix in SUFFIXES or f.name.startswith(".")):
                    label = scan(f)
                    if label:
                        findings.append((str(f), label))
        elif t.is_file():
            label = scan(t)
            if label:
                findings.append((str(t), label))
    if not findings:
        return 0
    print("\n[env-writer] DITOLAK — skrip menulis credential store tanpa backup:\n", file=sys.stderr)
    for path, label in findings:
        print(f"  - {path}  (pola: {label})", file=sys.stderr)
    print("\nCredential store = ~/.hermes/.env (semua token ecosystem). Menimpanya tanpa"
          "\nsalinan menghapus kredensial lain secara diam-diam — gateway lalu crash-loop"
          "\ndengan 'No bot token configured' (insiden 3 Okt 2026: 23 kunci hilang)."
          "\n\nPerbaikan yang diterima: salin dulu (`.bak` / `mktemp` / `shutil.copy`),"
          "\nlalu tulis; dan verifikasi jumlah kunci SEBELUM vs SESUDAH, bukan hanya kunci"
          "\nyang sedang diubah.\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

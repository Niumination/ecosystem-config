#!/usr/bin/env python3
"""Gate kredensial untuk commit di repo ekosistem ini.

Dijalankan sebagai pre-commit hook. Menolak commit bila:
  1. ada file staged yang sebenarnya di-ignore .gitignore (indikasi `git add -f`), atau
  2. isi file staged memuat pola kredensial (nilai TIDAK pernah dicetak).

Latar: 2026-09-16 `apps/pi-app-studio-mata/server/.env` lolos ke history repo publik
lewat `git add -f`; hook ini mencegah kelas kejadian yang sama.
"""
import re
import subprocess
import sys

# Pola berisiko tinggi (false positive rendah). Urutan tidak penting.
PATTERNS = [
    ("telegram_bot_token", re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("github_token", re.compile(r"\b(ghp_|gho_|ghu_|ghs_|ghr_|github_pat_)[A-Za-z0-9_]{20,}")),
    ("aws_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.")),
    ("pi_api_key", re.compile(r"PI_API_KEY\s*[=:]\s*[\"']?[A-Za-z0-9_-]{20,}")),
    ("generic_secret_assignment", re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password|passwd|access[_-]?key)\b\s*[=:]\s*[\"'][A-Za-z0-9_\-]{24,}[\"']")),
]

# Nama file yang tidak boleh masuk repo sama sekali (contoh/template dikecualikan).
BANNED_NAMES = re.compile(r"(^|/)(\.env($|\.)|.*\.pem$|.*\.key$|credentials\.json$|api-key\.md$)")
ALLOWED_SUFFIX = re.compile(r"\.(example|sample|template)$")


def staged_files():
    out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                         capture_output=True, text=True).stdout
    return [f for f in out.splitlines() if f.strip()]


def is_ignored(path):
    # --no-index WAJIB: tanpa itu, berkas yang sudah ter-stage (mis. lewat `git add -f`)
    # dianggap tracked dan check-ignore menjawab "tidak di-ignore" — gate jadi bocor.
    r = subprocess.run(["git", "check-ignore", "--no-index", "-q", path])
    return r.returncode == 0


def staged_content(path):
    r = subprocess.run(["git", "show", f":{path}"], capture_output=True)
    return r.stdout.decode("utf-8", errors="ignore")


BINARY_EXT = (".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz", ".tgz",
              ".mp4", ".mov", ".woff", ".woff2", ".ttf", ".lock")


def main():
    files = staged_files()
    if not files:
        return 0

    problems = []
    for path in files:
        if BANNED_NAMES.search(path) and not ALLOWED_SUFFIX.search(path):
            problems.append((path, "nama file kredensial (mis. .env)"))
            continue
        if is_ignored(path):
            problems.append((path, "file ini di-ignore .gitignore (jangan `git add -f`)"))
        if path.endswith(BINARY_EXT):
            continue
        content = staged_content(path)
        for label, pattern in PATTERNS:
            if pattern.search(content):
                problems.append((path, f"pola kredensial: {label}"))
                break

    if not problems:
        return 0

    print("\n[secret-scan] COMMIT DITOLAK — {} masalah:\n".format(len(problems)), file=sys.stderr)
    for path, why in problems:
        print(f"  - {path}: {why}", file=sys.stderr)
    print("\nNilai kredensial tidak dicetak. Pindahkan rahasia ke ~/.hermes/.env, vault/, atau"
          " file yang di-ignore; commit hanya contoh (.env.example).\n"
          "Butuh melewati gate ini? Jangan — perbaiki dulu. Bila benar-benar perlu:"
          " `git commit --no-verify` (wajib dicatat di laporan).\n", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

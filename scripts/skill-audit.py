#!/usr/bin/env python3
"""
skill-audit.py — Audit konten Skill Bank (anti prompt-injection)
================================================================
Pola diadopsi dari autoskills (midudev): review konten skill sebelum agent
mengeksekusi instruksinya. Versi heuristic, deterministik, warning-only.

7 kategori (dari docs/architecture/autoskills-pattern-adoption.md PHASE 3):
  1. hidden      instruksi tersembunyi — zero-width chars, komentar HTML berisi perintah
  2. exfil       exfiltrasi — base64 blob panjang, curl|bash / wget|sh
  3. url         URL non-allowlist (di luar dokumen resmi/npm/pypi/dll)
  4. secret      pola token/secret dalam contoh kode
  5. path        path/perintah berbahaya — ~/.ssh, ~/.aws, chmod 777, rm -rf /*
  6. self-mod    instruksi self-modification — edit SKILL.md / core beku
  7. injection   frasa prompt-injection klasik

Kalibrasi false-positive (dipelajari dari baseline 68 skill):
  - `~/.config` TIDAK di-flag (umum & benign); hanya `~/.ssh|~/.aws|~/.gnupg`.
  - `secret=`/`password=` literal: tidak di-flag jika didahului `?`/`&` (query param).
  - `api_key=`/`token=`: hanya di-flag jika value-nya mengandung digit (bukan nama variabel).
  - self-mod: hanya target `SKILL.md` + file beku (CONSTITUTION/VISION/SCOPE/FREEZE),
    bukan `AGENTS.md`/`BACKLOG.md` (itu alur kerja normal ekosistem).
  - `system prompt` polos tidak di-flag (konsep yang sering dikutip wajar).

PENTING: level WARNING saja. Hasil = rekomendasi review manual, BUKAN auto-fix.
Skill di domain `security` (mis. redteam) secara sah memuat pola-pola ini sebagai
contoh — konteks menentukan. Konsisten dengan aturan "audit = saran, bukan mutasi".

Mode:
  (default)           Scan semua skill, cetak laporan terkelompok per skill
  --bank DIR          Bank skill (default: <repo>/skills — script-relative)
  --skill NAME        Hanya scan satu skill
  --count             Cetak TOTAL jumlah finding (untuk integrasi up-eco Phase 6e)
  --json              Output JSON (array finding)
  --help              Bantuan

Exit code: 0 = scan selesai (termasuk saat ada finding). 1 = error path/bank.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BANK = REPO_ROOT / "skills"

SKIP_FILES = {".DS_Store"}
SKIP_DIRS = {".git"}

# ── Allowlist URL (host resmi/dokumentasi + deploy sendiri). Non-allowlist di-flag. ──
ALLOWED_DOMAINS = {
    # git & registry
    "github.com", "githubusercontent.com", "gist.github.com", "github.io",
    "gitlab.com", "bitbucket.org",
    "readthedocs.io", "python.org", "pypi.org", "npmjs.com",
    "nodejs.org", "vercel.com", "vercel.app",
    "nextjs.org", "react.dev", "vuejs.org", "nuxt.com", "ui.nuxt.com",
    "svelte.dev", "tailwindcss.com", "astro.build", "vitejs.dev",
    "rust-lang.org", "crates.io", "go.dev", "golang.org",
    "pub.dev", "dart.dev", "riverpod.dev",
    # frontend/design docs
    "shadcn.com", "ui.shadcn.com", "heroicons.com", "uiverse.io",
    "impeccable.style", "unsplash.com",
    # mobile & web platform
    "android.com", "flutter.dev", "reactnative.dev", "expo.dev",
    "reactnavigation.org", "swmansion.com", "testing-library.com",
    # standard bodies & docs
    "w3.org", "schema.org", "sitemaps.org", "apache.org",
    "openxmlformats.org", "web.dev", "mozilla.org",
    # aksesibilitas
    "deque.com", "dequeuniversity.com", "webaim.org", "nvaccess.org", "tpgi.com",
    # AI infra (dikenal luas)
    "anthropic.com", "openai.com", "googleapis.com", "openrouter.ai",
    "agentrouter.org", "opencode.ai", "huggingface.co", "autoskills.sh",
    "arxiv.org", "doi.org", "nvidia.com", "jina.ai",
    # provider internal Niumination (9router)
    "juan.web.id", "hcnsec.cn", "aerolink.lat", "router.juan.web.id", "api.hcnsec.cn",
    # komunitas
    "discord.gg", "discord.com",
    # google & sosial
    "google.com", "gstatic.com", "twitter.com", "linkedin.com",
    # wikipedia/stackoverflow
    "wikipedia.org", "wikimedia.org", "stackoverflow.com", "stackexchange.com",
    # infra umum
    "supabase.com", "prisma.io", "postgresql.org", "sqlite.org",
    "docker.com", "kubernetes.io", "apple.com", "microsoft.com",
    "ubuntu.com", "archlinux.org",
    # video & produk sendiri
    "heygen.com", "hyperframes.dev", "kune-ya.com",
    # pemerintahan Indonesia
    "go.id",
    # contoh & loopback
    "example.com", "example.org", "example.net", "localhost", "127.0.0.1",
}


def host_allowed(host: str) -> bool:
    host = host.lower().rstrip(".")
    if host in ALLOWED_DOMAINS:
        return True
    return any(host.endswith("." + d) for d in ALLOWED_DOMAINS)


# ── Pola per kategori ────────────────────────────────────────────────────────
ZERO_WIDTH = re.compile(r"[\u200b\u200c\u200d\u200e\u200f\ufeff]")

HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.S)
INSTR_KEYWORDS = re.compile(
    r"\b(ignore|disregard|override|execute|run|install|download|"
    r"curl|wget|bypass|jailbreak|you are|system prompt|sudo|rm -rf|chmod)\b",
    re.I,
)

EXFIL_CURL_BASH = re.compile(
    r"\b(curl|wget)\b[^\n|]{0,160}\|\s*(sudo\s+)?(ba|z|fi)?sh\b", re.I
)
BASE64_BLOB = re.compile(r"\b[A-Za-z0-9+/]{200,}={0,2}\b")

URL = re.compile(r"https?://[^\s\)\]\"'<>,\u201c\u201d`]+")

SECRET_SK = re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")
# api_key/token assignment — value wajib mengandung digit (filter di scan_skill)
SECRET_APIKEY = re.compile(
    r"(api[_-]?key|apikey|access[_-]?token|auth[_-]?token)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})",
    re.I,
)
SECRET_ASSIGN = re.compile(
    r"(?<![?&])\b(secret|password|passwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.I
)
SECRET_AWS = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
SECRET_GHP = re.compile(r"\bghp_[A-Za-z0-9]{36}\b")
SECRET_PRIVKEY = re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")

PATH_SSH = re.compile(r"~/(\.ssh|\.aws|\.gnupg)(/|$)")
PATH_ETC = re.compile(r"/etc/(passwd|shadow|sudoers)")
CHMOD777 = re.compile(r"chmod\s+(-R\s+)?0?777\b")
RM_RF = re.compile(r"\brm\s+-rf\s+(/~|/\*|/\s|~|\.\.)\b")
FORKBOMB = re.compile(r":\(\)\s*\{[^}]*\|[^}]*&\s*\}[^;]*;?:")

SELF_MOD = re.compile(
    r"\b(edit|modify|overwrite|rewrite|append\s+to)\b"
    r"[^\n]{0,60}\b(SKILL\.md|CONSTITUTION\.md|VISION\.md|SCOPE\.md|FREEZE\.list)\b",
    re.I,
)

INJ_IGNORE = re.compile(
    r"\bignore\s+(all\s+)?(previous|prior|above|earlier)\s+instructions\b", re.I
)
INJ_YOUARE = re.compile(
    r"\byou\s+are\s+now\b|\byou\s+are\s+no\s+longer\b|\bpretend\s+you\s+are\b", re.I
)
INJ_DISREGARD = re.compile(r"\bdisregard\s+(all\s+)?(previous|prior|above)\b", re.I)
INJ_OVERRIDE = re.compile(
    r"\b(override|bypass|ignore)\s+(the\s+)?(system|developer|safety)\b", re.I
)
INJ_JAILBREAK = re.compile(r"\bjailbreak\b|\bdeveloper\s+mode\b|\bDAN\s+mode\b", re.I)

# (category, label, regex) — diterapkan per-baris
LINE_RULES = [
    ("hidden", "zero-width char", ZERO_WIDTH),
    ("exfil", "curl|bash / wget|sh", EXFIL_CURL_BASH),
    ("exfil", "base64 blob (>200)", BASE64_BLOB),
    ("secret", "token sk-", SECRET_SK),
    ("secret", "secret=/password= literal", SECRET_ASSIGN),
    ("secret", "AWS AKIA", SECRET_AWS),
    ("secret", "GitHub PAT ghp_", SECRET_GHP),
    ("secret", "private key block", SECRET_PRIVKEY),
    ("path", "~/.ssh ~/.aws ~/.gnupg", PATH_SSH),
    ("path", "/etc/passwd|shadow|sudoers", PATH_ETC),
    ("path", "chmod 777", CHMOD777),
    ("path", "rm -rf / | ~ | ..", RM_RF),
    ("path", "fork bomb", FORKBOMB),
    ("self-mod", "edit/append SKILL.md / core beku", SELF_MOD),
    ("injection", "ignore previous instructions", INJ_IGNORE),
    ("injection", "you are now / pretend", INJ_YOUARE),
    ("injection", "disregard previous", INJ_DISREGARD),
    ("injection", "override/bypass system", INJ_OVERRIDE),
    ("injection", "jailbreak / DAN mode", INJ_JAILBREAK),
]

CATEGORIES = ["hidden", "exfil", "url", "secret", "path", "self-mod", "injection"]


def iter_skills(bank: Path):
    """Yield (domain, skill_name, skill_dir) untuk setiap folder berisi SKILL.md."""
    if not bank.is_dir():
        return
    for domain in sorted(p for p in bank.iterdir() if p.is_dir() and p.name not in SKIP_DIRS):
        for skill_dir in sorted(p for p in domain.iterdir() if p.is_dir() and p.name not in SKIP_DIRS):
            if (skill_dir / "SKILL.md").is_file():
                yield domain.name, skill_dir.name, skill_dir


def scan_skill(skill_dir: Path, domain: str, skill: str):
    """Return list of findings untuk satu skill."""
    findings = []
    for f in sorted(skill_dir.rglob("*")):
        if not f.is_file() or f.name in SKIP_FILES:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = f.relative_to(skill_dir).as_posix()

        # URL (diekstrak sekali, per file)
        for m in URL.finditer(text):
            url = m.group(0).rstrip(".,;:!?")
            if any(t in url for t in ("...", "$(", "*")):
                continue  # placeholder/template, bukan URL nyata
            try:
                host = url.split("//", 1)[1].split("/", 1)[0].split(":")[0]
            except IndexError:
                continue
            host = host.lower().rstrip(".")
            if not host or host in {"test", "example.invalid"}:
                continue  # placeholder host
            if host_allowed(host):
                continue
            line = text.count("\n", 0, m.start()) + 1
            findings.append(_f(domain, skill, rel, line, "url", "URL non-allowlist", url[:120]))

        # Komentar HTML berisi instruksi
        for m in HTML_COMMENT.finditer(text):
            body = m.group(1)
            if INSTR_KEYWORDS.search(body):
                line = text.count("\n", 0, m.start()) + 1
                snippet = re.sub(r"\s+", " ", body).strip()[:120]
                findings.append(_f(domain, skill, rel, line, "hidden", "HTML comment berisi instruksi", snippet))

        # Pola per-baris
        for lineno, line in enumerate(text.splitlines(), 1):
            for cat, label, rx in LINE_RULES:
                for m in rx.finditer(line):
                    findings.append(_f(domain, skill, rel, lineno, cat, label, line.strip()[:120]))
            # api_key/token assignment — hanya jika value mengandung digit (hindari nama variabel)
            for m in SECRET_APIKEY.finditer(line):
                if any(c.isdigit() for c in m.group(2)):
                    findings.append(
                        _f(domain, skill, rel, lineno, "secret", "api_key=/token= (value ber-digit)", line.strip()[:120])
                    )

    return findings


def _f(domain, skill, file, line, cat, label, snippet):
    return {
        "skill": skill,
        "domain": domain,
        "file": file,
        "line": line,
        "category": cat,
        "label": label,
        "snippet": snippet,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit konten Skill Bank (anti prompt-injection)")
    ap.add_argument("--bank", metavar="DIR", default=str(DEFAULT_BANK), help="Bank skill (default: repo skills/)")
    ap.add_argument("--skill", metavar="NAME", help="Hanya scan satu skill")
    ap.add_argument("--count", action="store_true", help="Cetak total jumlah finding saja")
    ap.add_argument("--json", action="store_true", help="Output JSON (array finding)")
    args = ap.parse_args()

    bank = Path(args.bank).expanduser()
    if not bank.is_dir():
        print(f"[error] bank tidak ditemukan: {bank}", file=sys.stderr)
        return 1

    all_findings = []
    skill_count = 0
    file_count = 0
    for domain, skill, skill_dir in iter_skills(bank):
        if args.skill and skill != args.skill:
            continue
        skill_count += 1
        for f in skill_dir.rglob("*"):
            if f.is_file() and f.name not in SKIP_FILES:
                file_count += 1
        all_findings.extend(scan_skill(skill_dir, domain, skill))

    if args.count:
        print(len(all_findings))
        return 0

    if args.json:
        print(json.dumps(all_findings, indent=2, ensure_ascii=False))
        return 0

    # ── Laporan default ──────────────────────────────────────────────────────
    print(f"[audit] Bank: {bank} — {skill_count} skill, {file_count} file")
    print("[audit] skill-audit.py — heuristic, warning-only, BUKAN auto-fix")
    print()

    by_skill = {}
    for f in all_findings:
        by_skill.setdefault(f["skill"], []).append(f)

    for skill in sorted(by_skill):
        fs = by_skill[skill]
        domain = fs[0]["domain"]
        print(f"Skill: {skill} ({domain}) — {len(fs)} finding")
        for f in fs[:20]:
            print(f"  [{f['category']}] {f['file']}:{f['line']} — {f['label']}")
            print(f"      {f['snippet']}")
        if len(fs) > 20:
            print(f"  ... dan {len(fs) - 20} finding lainnya (pakai --json untuk lengkap)")
        print()

    cat_count = {c: 0 for c in CATEGORIES}
    for f in all_findings:
        cat_count[f["category"]] += 1

    print("Ringkasan:")
    print(f"  {skill_count} skill discan, {file_count} file, {len(all_findings)} finding total")
    print("  per kategori: " + ", ".join(f"{c}={cat_count[c]}" for c in CATEGORIES))
    print()
    print("⚠️  Warning-only — hasil = rekomendasi review manual. Skill di domain")
    print("    `security` (mis. redteam) sah memuat pola ini sebagai contoh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

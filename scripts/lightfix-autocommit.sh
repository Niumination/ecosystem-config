#!/usr/bin/env bash
# =============================================================================
# lightfix-autocommit.sh — commit otomatis HANYA untuk churn timestamp artefak turunan
# =============================================================================
# Kebijakan (disetujui pemilik 19 Sep 2026): lightfix TIDAK pernah commit perubahan
# konten. Satu pengecualian: skills/manifest.json dan docs/registry/skill-registry.md
# bila perubahan keduanya TERBUKTI hanya timestamp (manifest.generatedAt, baris
# "_Last sync:" di registry). Tanpa ini, setiap run cron 23:30 meninggalkan 2 berkas
# "kotor" di root hanya karena stempel waktu berubah.
#
# Bukti, bukan dugaan: versi HEAD dibandingkan dengan versi working SETELAH field/baris
# waktu dinormalisasi — isi (hash, jumlah skill, nama, deskripsi) harus identik byte-per-byte.
# Grep kata "generated" saja tidak cukup: kata itu juga muncul di deskripsi skill.
#
# MENOLAK commit (keluar senyap + alasan di log) bila:
#   - HEAD belum ada, atau repo sedang merge/rebase
#   - ada perubahan ber-stage (jangan pernah menyentuh pekerjaan sesi lain)
#   - ada berkas berubah DI LUAR allowlist
#   - perubahan konten nyata terdeteksi pada berkas allowlist
#
# Tidak pernah push. Selalu exit 0 (kecuali error tak terduga) agar tidak mematikan caller.
# Usage: bash scripts/lightfix-autocommit.sh [repo-root]
# =============================================================================
set -uo pipefail

NIUMINATION="${1:-${NIUMINATION:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}}"
ALLOW=( "skills/manifest.json" "docs/registry/skill-registry.md" )

log() { echo "[autocommit] $*"; }

cd "$NIUMINATION" 2>/dev/null || { log "tidak bisa masuk $NIUMINATION"; exit 0; }
git rev-parse --git-dir >/dev/null 2>&1 || { log "bukan repo git"; exit 0; }

# ── 1. prasyarat ──
if ! git rev-parse --verify -q HEAD >/dev/null; then
  log "HEAD belum ada (repo kosong) — dilewati"; exit 0
fi
GITDIR=$(git rev-parse --git-dir)
if [ -e "$GITDIR/MERGE_HEAD" ] || [ -e "$GITDIR/rebase-merge" ] || [ -e "$GITDIR/rebase-apply" ]; then
  log "merge/rebase sedang berlangsung — dilewati"; exit 0
fi
if ! git diff --cached --quiet 2>/dev/null; then
  log "ada perubahan ter-stage (milik sesi lain?) — dilewati"; exit 0
fi

# ── 2. apa saja yang berubah ──
changed=$(git status --porcelain -- "${ALLOW[@]}" 2>/dev/null | awk '$1=="M"{print $2}')
if [ -z "$changed" ]; then
  log "tidak ada artefak turunan yang berubah — tidak ada yang perlu di-commit"; exit 0
fi

# Berkas TERLACAK yang dimodifikasi di luar allowlist → JANGAN commit otomatis (milik
# sesi/pekerjaan lain). Berkas untracked sengaja diabaikan: `git add` di skrip ini selalu
# memakai pathspec eksplisit (dua berkas allowlist), jadi untracked tidak mungkin ikut
# ter-commit. Diabaikan tapi DICATAT agar tidak ada perubahan tersembunyi.
other=$(git status --porcelain 2>/dev/null | awk '$1!="??" && $1!="A"{print $2}' \
        | grep -vxF -e "skills/manifest.json" -e "docs/registry/skill-registry.md" || true)
if [ -n "$other" ]; then
  log "ada berkas terlacak DI LUAR allowlist berubah — tidak commit otomatis:"
  printf '%s\n' "$other" | sed 's/^/[autocommit]   - /'
  exit 0
fi
untracked=$(git status --porcelain 2>/dev/null | awk '$1=="??"{print $2}' || true)
if [ -n "$untracked" ]; then
  log "untracked diabaikan (tidak akan ikut ter-commit): $(printf '%s' "$untracked" | tr '\n' ' ')"
fi

log "artefak berubah: $(printf '%s' "$changed" | tr '\n' ' ')"

# ── 3. buktikan timestamp-saja ──
if python3 - "$NIUMINATION" <<'PY'
import json, re, subprocess, sys
from pathlib import Path

repo = Path(sys.argv[1])
META_KEYS = {"generatedat", "lastsync", "updatedat", "timestamp", "generated_at", "syncedat"}


def norm_json(text: str):
    def scrub(obj):
        if isinstance(obj, dict):
            return {k: ("<TS>" if k.lower() in META_KEYS else scrub(v)) for k, v in obj.items()}
        if isinstance(obj, list):
            return [scrub(x) for x in obj]
        return obj
    return scrub(json.loads(text))


TS_LINE = re.compile(r"^\s*[_-]{0,2}\s*(last\s*sync|generated|diperbarui|updated)\b[^|]*:", re.I)


def norm_text_lines(text: str):
    return [l for l in text.splitlines() if not TS_LINE.match(l)]


def version(rel: str) -> str | None:
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, text=True, cwd=repo)
    return r.stdout if r.returncode == 0 else None


ok = True
for rel in ("skills/manifest.json", "docs/registry/skill-registry.md"):
    head = version(rel)
    path = repo / rel
    if head is None or not path.exists():
        print(f"[autocommit]   {rel}: tidak bisa dibandingkan — anggap BUKAN timestamp-saja")
        ok = False
        continue
    cur = path.read_text(encoding="utf-8")
    try:
        if rel.endswith(".json"):
            same = norm_json(head) == norm_json(cur)
        else:
            same = norm_text_lines(head) == norm_text_lines(cur)
    except Exception as exc:                                  # JSON rusak = jangan commit
        print(f"[autocommit]   {rel}: gagal menormalkan ({exc}) — anggap BUKAN timestamp-saja")
        ok = False
        continue
    print(f"[autocommit]   {rel}: {'timestamp-saja' if same else 'ADA PERUBAHAN KONTEN'}")
    ok = ok and same
sys.exit(0 if ok else 1)
PY
then
  git add -- "${ALLOW[@]}"
  if git commit -q -m "chore(registry): sinkronkan timestamp artefak turunan (lightfix otomatis)"; then
    touched=$(git show --pretty="" --name-only HEAD 2>/dev/null | tr '\n' ' ')
    log "✓ commit timestamp-saja dibuat: $(git log -1 --pretty=%h) — tanpa push"
    log "  berkas dalam commit: $touched"
  else
    log "commit gagal — perubahan dibiarkan apa adanya"
  fi
else
  log "perubahan KONTEN nyata terdeteksi — tidak di-commit otomatis (butuh peninjauan manusia)"
fi
exit 0

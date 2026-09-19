#!/usr/bin/env python3
"""gen-skill-index.py — selaraskan skills/INDEX.md dengan bank (sumber kebenaran).

Latar: INDEX.md adalah artefak turunan yang sebelumnya TIDAK punya generator, sehingga
setiap skill baru membuatnya drift (dari sesi mana pun, termasuk thread MC grup).

Yang disentuh skrip ini:
  1. baris skill yang belum ada di tabel domain-nya  → ditambahkan (mengikuti skema kolom
     section itu: 4 kolom Path / 4 kolom Source / 5 kolom Source+Ukuran)
  2. baris skill yang foldernya sudah tidak ada di bank → dibuang (dilaporkan)
  3. section domain baru                            → dibuat sebelum bagian penutup
  4. counter: "Semua N skill tersedia", "**Status:** N ✅ Aktif", tabel Ringkasan

Yang TIDAK disentuh: blok header, tabel "featured" sebelum section pertama (kurasi manusia),
catatan konflik, panduan, template.

IDEMPOTEN — dijalankan dua kali berturut-turut, eksekusi kedua tidak mengubah apa pun.
Versi-versi sebelumnya gagal pada dua hal dan keduanya sudah diuji ulang:
  (a) parser hanya mengenali section sebelum heading non-domain pertama → heading domain di
      bagian penutup ikut diparsing ulang tiap putaran (15 section → 45 section, tidak konvergen);
  (b) penulis menulis baris 4 kolom ke section berskema 5 kolom (Source+Ukuran) → format rusak.
Sekarang skema tiap section dibaca dari baris header-nya sendiri.

Usage:
  python3 scripts/gen-skill-index.py            # perbaiki INDEX.md
  python3 scripts/gen-skill-index.py --check    # laporkan drift saja (exit 1 bila ada)
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "skills"
INDEX = BANK / "INDEX.md"
SKIP_DIRS = {".archive", ".git", "references", "templates", "scripts", "assets"}

TITLES = {
    "software-development": "Software Development", "design": "Design", "ecosystem": "Ecosystem",
    "security": "Security", "creative": "Creative", "note-taking": "Note-taking",
    "autonomous-ai-agents": "Autonomous AI Agents", "devops": "DevOps", "github": "GitHub",
    "productivity": "Productivity", "research": "Research", "development": "Development",
    "mlops": "MLOps", "smart-home": "Smart Home", "media": "Media", "apple": "Apple",
    "email": "Email", "governance": "Governance", "web": "Web",
}
ROOT_TITLE = "Standalone (root bank)"
ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|")
SEC_RE = re.compile(r"^##\s+Domain:\s*(.+?)\s*$")
HDR_RE = re.compile(r"^\|\s*Skill\s*\|(.*)\|\s*$")


def title_for(domain: str) -> str:
    return TITLES.get(domain, domain.replace("-", " ").title())


def human_size(skill_dir: Path) -> str:
    md = skill_dir / "SKILL.md"
    try:
        n = md.stat().st_size
    except OSError:
        return "—"
    return f"{n/1024:.1f} KB" if n < 1024 * 1024 else f"{n/1048576:.1f} MB"


def frontmatter(skill_dir: Path) -> tuple[str, str]:
    md = skill_dir / "SKILL.md"
    try:
        text = md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return skill_dir.name, ""
    name, desc = skill_dir.name, ""
    m = re.match(r"^---\n(.*?)\n---", text, re.S) or re.search(r"\n---\n(.*?)\n---", text, re.S)
    if m:
        mn = re.search(r"^name:\s*(.+)$", m.group(1), re.M)
        ds = re.search(r"^description:\s*(.+)$", m.group(1), re.M)
        if mn:
            name = mn.group(1).strip().strip("\"'")
        if ds:
            desc = ds.group(1).strip().strip("\"'")
    if not desc:
        body = re.sub(r"^---\n.*?\n---", "", text, count=1, flags=re.S)
        for line in body.split("\n"):
            line = line.strip()
            if line and not line.startswith(("#", ">")):
                desc = line
                break
    desc = re.sub(r"\s+", " ", desc)
    return name, (desc[:110].rstrip() + "…") if len(desc) > 112 else desc


def scan_bank() -> dict[str, list[tuple[str, str, str, str, str]]]:
    """domain → [(nama, deskripsi, path-index, ukuran, folder)] (kedalaman bebas)."""
    found: dict[str, list[tuple[str, str, str, str, str]]] = {}
    for md in sorted(BANK.rglob("SKILL.md")):
        parts = md.relative_to(BANK).parts
        if len(parts) < 2 or any(p in SKIP_DIRS for p in parts[:-1]):
            continue
        domain = parts[0] if len(parts) > 2 else "__root__"
        # Nama baris = NAMA FOLDER, bukan `name:` di frontmatter — pemeriksa up-eco
        # mencocokkan nama folder (`basename $(dirname ...)`), jadi identitas baris harus
        # sama. (Kasus nyata: ponytail-core punya frontmatter bernama lain sehingga barisnya
        # sempat dianggap hilang lalu dibuang oleh generator.)
        _fm_name, desc = frontmatter(md.parent)
        name = md.parent.name
        path = "Bank Pusat" if domain == "__root__" else f"{domain}/{md.parent.name}"
        found.setdefault(domain, []).append((name, desc, path, human_size(md.parent), md.parent.name))
    return {k: sorted(v, key=lambda x: x[0].lower()) for k, v in found.items()}


def row_for(header: str | None, name: str, desc: str, path: str, size: str) -> str:
    """Bangun baris mengikuti skema kolom section (dibaca dari baris header tabelnya)."""
    h = (header or "").lower()
    if "ukuran" in h:                       # Skill | Status | Source | Ukuran | Deskripsi
        return f"| **{name}** | ✅ Aktif | Bank Pusat | {size} | {desc} |"
    if "path" in h:                         # Skill | Status | Path | Deskripsi
        return f"| **{name}** | ✅ Aktif | {path} | {desc} |"
    if "source" in h:                       # Skill | Status | Source | Deskripsi
        return f"| **{name}** | ✅ Aktif | Bank Pusat | {desc} |"
    return f"| **{name}** | ✅ Aktif | {path} | {desc} |"


def build(text: str) -> tuple[str, list[str]]:
    bank = scan_bank()
    total = sum(len(v) for v in bank.values())
    by_title = {title_for(d): d for d in bank}
    by_title[ROOT_TITLE] = "__root__"

    lines = text.split("\n")
    log: list[str] = []
    by_title_l = by_title

    # Pindai SELURUH berkas: setiap heading "## Domain:" memulai blok, berakhir di heading
    # "## " berikutnya (domain atau bukan). Versi sebelumnya berhenti pada heading non-domain
    # pertama, sehingga blok yang ditambahkan di akhir berkas tidak ikut diparsing dan
    # ditambahkan ulang setiap putaran (tidak konvergen).
    out: list[str] = []
    seen: set[str] = set()
    idx = 0
    n = len(lines)
    while idx < n:
        m = SEC_RE.match(lines[idx])
        if not m:
            out.append(lines[idx])
            idx += 1
            continue
        title = m.group(1)
        j = idx + 1
        while j < n and not lines[j].startswith("## "):
            j += 1
        body = lines[idx + 1:j]
        out.append(lines[idx])
        domain = by_title_l.get(title)
        if domain is None:
            out.extend(body)
        else:
            seen.add(domain)
            header = next((l for l in body if HDR_RE.match(l)), None)
            wanted = {x[0] for x in bank[domain]}
            kept, present = [], set()
            for line in body:
                rm = ROW_RE.match(line)
                if rm:
                    nm = rm.group(1).strip()
                    if nm in wanted and nm not in present:
                        kept.append(line)
                        present.add(nm)
                    elif nm in present:
                        log.append(f"  - duplikat dibuang dari {title}: {nm}")
                    else:
                        log.append(f"  - buang dari {title}: {nm}")
                    continue
                kept.append(line)
            for name, desc, path, size, _folder in bank[domain]:
                if name in present:
                    continue
                at = max((k for k, l in enumerate(kept) if ROW_RE.match(l)), default=len(kept) - 1) + 1
                kept.insert(at, row_for(header, name, desc, path, size))
                log.append(f"  + tambah ke {title}: {name}")
            out.extend(kept)
        idx = j

    new_blocks: list[str] = []
    for domain in bank:                                 # section domain yang belum ada
        if domain in seen:
            continue
        t = ROOT_TITLE if domain == "__root__" else title_for(domain)
        hdr = "| Skill | Status | Source | Ukuran | Deskripsi |"
        new_blocks.append(f"## Domain: {t}")
        new_blocks.append("")
        new_blocks.append(hdr)
        new_blocks.append("|-------|:------:|--------|-------:|-----------|")
        for name, desc, path, size, _folder in bank[domain]:
            new_blocks.append(row_for(hdr, name, desc, path, size))
        new_blocks.append("")
        log.append(f"  + section baru: {t}")
    if new_blocks:                                      # sisipkan setelah blok domain terakhir
        last = max((k for k, l in enumerate(out) if SEC_RE.match(l)), default=len(out) - 1)
        end_of_last = last + 1
        while end_of_last < len(out) and not out[end_of_last].startswith("## "):
            end_of_last += 1
        out[end_of_last:end_of_last] = new_blocks

    text = "\n".join(out)
    text = re.sub(r"Semua \d+ skill tersedia", f"Semua {total} skill tersedia", text)
    text = re.sub(r"\*\*Status:\*\* \d+ ✅ Aktif", f"**Status:** {total} ✅ Aktif", text)
    text = re.sub(r"\| ✅ Aktif \| \*\*\d+\*\* \|", f"| ✅ Aktif | **{total}** |", text)
    text = re.sub(r"\| \*\*Total\*\* \| \*\*\d+\*\* \|", f"| **Total** | **{total}** |", text)
    return text, log


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not INDEX.exists():
        print(f"  ✗ {INDEX} tidak ada")
        return 2
    original = INDEX.read_text(encoding="utf-8")
    text, log = build(original)
    total = sum(len(v) for v in scan_bank().values())

    if args.check:
        if text != original:
            print(f"  ⚠️  INDEX.md drift ({len(log)} perubahan · {total} skill di bank)")
            for l in log[:15]:
                print("   " + l)
            return 1
        print(f"  ✅ INDEX.md sinkron dengan bank ({total} skill)")
        return 0

    if text != original:
        INDEX.write_text(text, encoding="utf-8")
        print(f"  ✅ diperbarui — {total} skill di bank · {len(log)} perubahan")
        for l in log:
            print("   " + l)
    else:
        print(f"  ✅ tidak ada perubahan — {total} skill di bank (idempoten)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

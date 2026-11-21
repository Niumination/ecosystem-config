#!/usr/bin/env python3
"""Build the central media library for the Niumination ecosystem.

Masters stay where they are -- each project repo keeps its own source of truth
(abstract-studio: project/<slug>/output/, govtechlab: artifacts/showreel/, ...).
Moving them would break the one-home rule and duplicate hundreds of MB.

This script therefore does two things:

  1. INDEX   -- catalogues every produced media file (video / image / audio)
     found under the known production roots into
     archive/media-lib/INDEX.md, with project, kind, bytes, mtime and SHA-256.
  2. SHELF   -- hardlinks the FINAL deliverables into
     archive/media-lib/deliverables/<project>/... so there is one door to all
     published material. Hardlinks share the inode with the master: they cost
     no extra disk and follow the master's content.

Re-run after any production run:

    python3 scripts/build-media-index.py

Stdlib only. No network, no writes outside archive/media-lib/.
"""

from __future__ import annotations

import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path

ECO = Path(__file__).resolve().parents[1]
LIB = ECO / "archive" / "media-lib"
INDEX = LIB / "INDEX.md"
SHELF = LIB / "deliverables"

VIDEO = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
IMAGE = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif", ".svg"}
AUDIO = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}
MEDIA = VIDEO | IMAGE | AUDIO

# Roots that hold production output. Everything media-shaped under these is
# catalogued. Roots are relative to the ecosystem root.
INDEX_ROOTS: dict[str, list[str]] = {
    "abstract-studio": ["apps/abstract-studio"],
    "govtechlab-aceh-tengah": ["dinas/govtechlab-aceh-tengah"],
    "hermes-showreel-engine": ["labs/hermes-showreel-engine"],
    "edu-content": ["labs/edu-content"],
    "remotion-studio": ["sandbox/remotion-studio"],
    "mata-aihackfest-2026": ["labs/mata-aihackfest-2026"],
}

# Globs (relative to ecosystem root) whose files count as FINAL deliverables
# and are hardlinked onto the shelf.
DELIVERABLE_GLOBS = [
    "apps/abstract-studio/project/*/output/*",
    "apps/abstract-studio/project/*/out/*",
    "apps/abstract-studio/output/*",
    "dinas/govtechlab-aceh-tengah/artifacts/showreel/*",
    "labs/hermes-showreel-engine/projects/*/out/*",
    "labs/edu-content/**/audio/**",
    "sandbox/remotion-studio/out/*",
]

# Never catalogue these (junk, third-party extracts, stale backups).
SKIP_PARTS = {
    "node_modules", ".git", "apk_extract", "__pycache__",
    "_backup", "data/_backup", "archive/backup",
}

# Path fragments that mark a file as working source rather than a result.
SOURCE_HINTS = ("/src/", "/assets/", "/node_modules/", "/.venv/", "/venv/")


def kind_of(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext in VIDEO:
        return "video"
    if ext in IMAGE:
        return "image"
    if ext in AUDIO:
        return "audio"
    return None


def skipped(rel: Path) -> bool:
    parts = rel.parts
    if any(p in SKIP_PARTS for p in parts):
        return True
    # archive/backup/... is a stale mirror, not live production
    if len(parts) > 1 and parts[0] == "archive" and parts[1] == "backup":
        return True
    return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n / 1:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} GB"


def collect() -> tuple[list[dict], list[Path]]:
    """Return (catalogue rows, deliverable paths)."""
    rows: list[dict] = []
    seen: set[Path] = set()

    for project, roots in INDEX_ROOTS.items():
        for root_rel in roots:
            root = ECO / root_rel
            if not root.is_dir():
                continue
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                rel = path.relative_to(ECO)
                if skipped(rel):
                    continue
                k = kind_of(path)
                if k is None:
                    continue
                if path in seen:
                    continue
                seen.add(path)
                st = path.stat()
                rows.append({
                    "project": project,
                    "rel": rel.as_posix(),
                    "kind": k,
                    "bytes": st.st_size,
                    "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d"),
                    "sha": sha256(path),
                    "deliverable": False,
                })

    # mark deliverables
    deliv: list[Path] = []
    for pattern in DELIVERABLE_GLOBS:
        for path in ECO.glob(pattern):
            if not path.is_file() or kind_of(path) is None:
                continue
            deliv.append(path)
            rel = path.relative_to(ECO).as_posix()
            for row in rows:
                if row["rel"] == rel:
                    row["deliverable"] = True
                    break

    rows.sort(key=lambda r: (r["project"], r["rel"]))
    return rows, sorted(set(deliv))


def build_shelf(deliverables: list[Path]) -> tuple[int, int]:
    """Hardlink deliverables under SHELF. Returns (linked, skipped)."""
    linked = skipped_count = 0
    for src in deliverables:
        rel = src.relative_to(ECO)
        # shelf path: deliverables/<project-root>/<rest>
        parts = rel.parts
        if parts[0] in ("apps", "dinas", "labs", "sandbox", "services", "sites"):
            project = "/".join(parts[:2])
            rest = parts[2:]
        else:
            project, rest = parts[0], parts[1:]
        dst = SHELF / project / Path(*rest)
        if dst.exists():
            skipped_count += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(src, dst)
            linked += 1
        except OSError:
            # cross-device or filesystem without hardlink support: fall back
            import shutil
            shutil.copy2(src, dst)
            linked += 1
    return linked, skipped_count


def write_index(rows: list[dict], linked: int, skipped: int) -> None:
    total_bytes = sum(r["bytes"] for r in rows)
    dels = [r for r in rows if r["deliverable"]]
    del_bytes = sum(r["bytes"] for r in dels)

    lines = [
        "# Media Library — Niumination",
        "",
        f"_Dibangkitkan `scripts/build-media-index.py` · "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')} · "
        f"jangan edit tangan._",
        "",
        "## Aturan",
        "",
        "- **Master tetap di repo proyek.** abstract-studio: `project/<slug>/output/`;",
        "  govtechlab: `artifacts/showreel/`; engine: `projects/<slug>/out/`.",
        "  Memindahkannya melanggar one-home rule dan menggandakan ratusan MB.",
        "- `deliverables/` di direktori ini adalah **hardlink** ke master — inode yang",
        "  sama, nol tambahan disk, isinya mengikuti master.",
        "- Arsip di `archive/backup/`, extract APK, dan `_backup/` **tidak** dikatalogkan.",
        "",
        "## Ringkasan",
        "",
        f"- Total berkas: **{len(rows)}** ({human(total_bytes)})",
        f"- Deliverable final: **{len(dels)}** ({human(del_bytes)}) — "
        f"hardlink {linked} baru, {skipped} sudah ada",
        "",
    ]

    by_kind: dict[str, int] = {}
    for r in rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
    lines.append("| Kind | Jumlah |")
    lines.append("|---|---|")
    for k in ("video", "image", "audio"):
        lines.append(f"| {k} | {by_kind.get(k, 0)} |")
    lines.append("")

    cur = None
    for r in rows:
        if r["project"] != cur:
            cur = r["project"]
            lines.append(f"## {cur}")
            lines.append("")
            lines.append("| | Berkas | Kind | Ukuran | Tanggal | SHA-256 (12) |")
            lines.append("|---|---|---|---|---|---|")
        flag = " **DELIVERABLE**" if r["deliverable"] else ""
        lines.append(
            f"|{flag} | `{r['rel']}` | {r['kind']} | {human(r['bytes'])} | "
            f"{r['mtime']} | `{r['sha'][:12]}` |"
        )
    lines.append("")

    LIB.mkdir(parents=True, exist_ok=True)
    INDEX.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    LIB.mkdir(parents=True, exist_ok=True)
    rows, deliverables = collect()
    linked, skipped = build_shelf(deliverables)
    write_index(rows, linked, skipped)
    dels = sum(1 for r in rows if r["deliverable"])
    print(f"[media-lib] {len(rows)} berkas dikatalogkan "
          f"({dels} deliverable), shelf +{linked} hardlink, {skipped} sudah ada")
    print(f"[media-lib] index -> {INDEX.relative_to(ECO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

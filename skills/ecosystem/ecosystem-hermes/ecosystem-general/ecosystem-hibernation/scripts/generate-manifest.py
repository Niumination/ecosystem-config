#!/usr/bin/env python3
"""
generate-manifest.py — Manifest SHA-256 untuk hibernasi proyek ke vault.

Pemakaian:
  python3 generate-manifest.py <folder_vault>              # buat MANIFEST.sha256.json
  python3 generate-manifest.py <folder_vault> --verify     # verifikasi vs manifest
  python3 generate-manifest.py <folder_vault> --root /path  # path relatif vs root lain

Keluar:
  0 = sukses / verifikasi cocok semua
  1 = argumen salah / manifest tidak ada saat --verify
  2 = MISMATCH terdeteksi (berkas berubah/hilang/tambahan)

Bagian dari skill ecosystem-hibernation (Niumination).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys
from pathlib import Path

MANIFEST_NAME = "MANIFEST.sha256.json"


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            data = fh.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def collect(folder: Path) -> list[dict]:
    entries: list[dict] = []
    for dirpath, dirnames, filenames in os.walk(folder):
        # manifest sendiri diabaikan dari checksum (dia buat setelahnya)
        dirnames[:] = [d for d in sorted(dirnames)]
        for name in sorted(filenames):
            if name == MANIFEST_NAME:
                continue
            full = Path(dirpath) / name
            entries.append(
                {
                    "path": str(full.relative_to(folder)),
                    "sha256": sha256_file(full),
                    "bytes": full.stat().st_size,
                }
            )
    entries.sort(key=lambda e: e["path"])
    return entries


def generate(folder: Path, asal: str | None) -> int:
    files = collect(folder)
    total_bytes = sum(e["bytes"] for e in files)
    manifest = {
        "arsip": f"hibernasi {folder.name}",
        "asal": asal or str(folder),
        "tanggal": _dt.date.today().isoformat(),
        "file_count": len(files),
        "total_bytes": total_bytes,
        "catatan": (
            "Backup hibernasi: berkas git-ignored (.env, data/PII, .vercel/) + source. "
            "node_modules/.next/dist TIDAK dibackup (regeneratif). "
            "Pulihkan: git clone untuk history + pulihkan folder ini + npm install."
        ),
        "files": files,
    }
    out = folder / MANIFEST_NAME
    out.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(f"manifest dibuat: {out}")
    print(f"berkas: {len(files)} · total: {total_bytes:,} bytes")
    return 0


def verify(folder: Path) -> int:
    manifest_path = folder / MANIFEST_NAME
    if not manifest_path.exists():
        print(f"ERROR: manifest tidak ada: {manifest_path}", file=sys.stderr)
        return 1
    m = json.loads(manifest_path.read_text())
    listed = {e["path"] for e in m["files"]}
    ok = miss = bad = 0
    for entry in m["files"]:
        p = folder / entry["path"]
        if not p.exists():
            miss += 1
            print(f"HILANG : {entry['path']}")
            continue
        actual = sha256_file(p)
        if actual == entry["sha256"]:
            ok += 1
        else:
            bad += 1
            print(f"RUSAK  : {entry['path']}")
            print(f"         manifest={entry['sha256'][:16]}… aktual={actual[:16]}…")

    # berkas tambahan setelah manifest dibuat (bisa jadi lightfix autocommit)
    on_disk = {str(p.relative_to(folder)) for p in folder.rglob("*") if p.is_file()}
    extra = sorted(on_disk - listed - {MANIFEST_NAME})
    for name in extra:
        print(f"TAMBAH : {name}")

    total = ok + miss + bad
    print(
        f"\ndiperiksa: {total} · cocok: {ok} · hilang: {miss} · rusak: {bad}"
        f" · tambahan: {len(extra)}"
    )
    if ok == m["file_count"] and miss == 0 and bad == 0:
        print("HASIL: UTUH ✓")
        return 0
    print("HASIL: MISMATCH ✗ — jangan hapus folder asli", file=sys.stderr)
    return 2


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Manifest SHA-256 untuk hibernasi proyek ke vault"
    )
    ap.add_argument("folder", help="folder vault hasil stage backup")
    ap.add_argument(
        "--verify",
        action="store_true",
        help="verifikasi isi vs MANIFEST.sha256.json (bukan generate)",
    )
    ap.add_argument("--root", help="path asal folder (untuk metadata asal)")
    args = ap.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        print(f"ERROR: bukan folder: {folder}", file=sys.stderr)
        return 1
    if args.verify:
        return verify(folder)
    return generate(folder, args.root)


if __name__ == "__main__":
    sys.exit(main())

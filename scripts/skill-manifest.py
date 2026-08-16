#!/usr/bin/env python3
"""
skill-manifest.py — Manifest SHA-256 untuk Skill Bank Niumination
================================================================
Pola diadopsi dari autoskills (midudev) — manifest per-file hash + bundleHash.

Mode:
  (default)           Generate skills/manifest.json dari filesystem
  --check             Verifikasi manifest vs filesystem bank (deteksi ubah/hilang/baru)
  --verify-target DIR Verifikasi salinan di target agent (Jcode/Hermes/USB) vs manifest
  --lockfile DIR      Generate skills-lock.json di target (source + bundleHash)
  --help              Bantuan

Exit code: 0 = OK, 1 = mismatch/error (detail di stdout)

Contoh:
  python3 scripts/skill-manifest.py
  python3 scripts/skill-manifest.py --check
  python3 scripts/skill-manifest.py --verify-target ~/.jcode/skills
  python3 scripts/skill-manifest.py --lockfile ~/.jcode/skills
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Path resolution (Hermes env HOME bisa beda) ─────────────────────────────
def resolve_home() -> Path:
    home = Path.home()
    if (home / "Desktop" / "Niumination" / "skills").is_dir():
        return home
    user = os.environ.get("USER", "zaryu")
    alt = Path(f"/Users/{user}")
    if (alt / "Desktop" / "Niumination" / "skills").is_dir():
        return alt
    return home

REAL_HOME = resolve_home()
BANK_DIR = REAL_HOME / "Desktop" / "Niumination" / "skills"
MANIFEST_PATH = BANK_DIR / "manifest.json"

SKIP_FILES = {".DS_Store"}
SKIP_DIRS = {".git"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_skills(bank: Path):
    """Yield (domain, skill_name, skill_dir) untuk setiap folder berisi SKILL.md."""
    if not bank.is_dir():
        return
    for domain in sorted(p for p in bank.iterdir() if p.is_dir() and p.name not in SKIP_DIRS):
        for skill_dir in sorted(p for p in domain.iterdir() if p.is_dir() and p.name not in SKIP_DIRS):
            if (skill_dir / "SKILL.md").is_file():
                yield domain.name, skill_dir.name, skill_dir


def build_skill_entry(domain: str, skill_name: str, skill_dir: Path) -> dict:
    files = {}
    for f in sorted(skill_dir.rglob("*")):
        if f.is_file() and f.name not in SKIP_FILES:
            rel = f.relative_to(skill_dir).as_posix()
            files[rel] = sha256_file(f)
    # bundleHash = SHA-256 dari gabungan "rel:hash" sorted (pola autoskills)
    bundle_src = "\n".join(f"{rel}:{h}" for rel, h in sorted(files.items()))
    bundle_hash = hashlib.sha256(bundle_src.encode()).hexdigest()
    return {
        "domain": domain,
        "bundleHash": bundle_hash,
        "files": files,
    }


def generate_manifest() -> dict:
    skills = {}
    for domain, skill_name, skill_dir in iter_skills(BANK_DIR):
        skills[skill_name] = build_skill_entry(domain, skill_name, skill_dir)
    manifest = {
        "version": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "skillCount": len(skills),
        "fileCount": sum(len(v["files"]) for v in skills.values()),
        "skills": skills,
    }
    return manifest


def write_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"[ok] manifest.json ditulis: {MANIFEST_PATH}")
    print(f"     {manifest['skillCount']} skill, {manifest['fileCount']} file")


def check_bank() -> int:
    if not MANIFEST_PATH.is_file():
        print(f"[error] manifest.json tidak ada: {MANIFEST_PATH}")
        print("        Jalankan: python3 scripts/skill-manifest.py")
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text())
    errors = []
    known_skills = set(manifest["skills"].keys())
    disk_skills = set()

    for domain, skill_name, skill_dir in iter_skills(BANK_DIR):
        disk_skills.add(skill_name)
        if skill_name not in manifest["skills"]:
            errors.append(f"  [baru] {skill_name} — ada di filesystem, TIDAK di manifest")
            continue
        entry = manifest["skills"][skill_name]
        # cek file hilang
        for rel in entry["files"]:
            if not (skill_dir / rel).is_file():
                errors.append(f"  [hilang] {skill_name}/{rel}")
        # cek hash berubah
        for rel, expected in entry["files"].items():
            p = skill_dir / rel
            if p.is_file() and sha256_file(p) != expected:
                errors.append(f"  [ubah] {skill_name}/{rel}")
        # cek file baru (tidak terdaftar)
        disk_files = {
            f.relative_to(skill_dir).as_posix()
            for f in skill_dir.rglob("*")
            if f.is_file() and f.name not in SKIP_FILES
        }
        for rel in sorted(disk_files - set(entry["files"])):
            errors.append(f"  [baru] {skill_name}/{rel} — tidak di manifest")

    # skill di manifest tapi hilang dari disk
    for skill_name in sorted(known_skills - disk_skills):
        errors.append(f"  [hilang-skill] {skill_name} — di manifest tapi tidak ada di disk")

    if errors:
        print(f"[FAIL] {len(errors)} ketidaksesuaian manifest vs filesystem:")
        for e in errors:
            print(e)
        return 1
    print("[ok] manifest sinkron dengan filesystem — 0 mismatch")
    return 0


def verify_target(target: Path, structure: str = "flat") -> int:
    if not MANIFEST_PATH.is_file():
        print("[error] manifest.json tidak ada di bank — generate dulu")
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text())
    missing = []
    mismatch = []
    checked = 0
    for skill_name, entry in manifest["skills"].items():
        if structure == "domain":
            skill_dir = target / entry["domain"] / skill_name
        else:
            skill_dir = target / skill_name
        if not skill_dir.is_dir():
            missing.append(f"  [hilang-skill] {skill_name}")
            continue
        for rel, expected in entry["files"].items():
            p = skill_dir / rel
            checked += 1
            if not p.is_file():
                missing.append(f"  [hilang] {skill_name}/{rel}")
            elif sha256_file(p) != expected:
                mismatch.append(f"  [ubah] {skill_name}/{rel}")
    if missing or mismatch:
        print(f"[FAIL] target {target} — {len(missing)} hilang, {len(mismatch)} mismatch ({checked} file dicek):")
        for e in (missing + mismatch)[:50]:
            print(e)
        if len(missing) + len(mismatch) > 50:
            print(f"  ... dan {len(missing) + len(mismatch) - 50} lainnya")
        return 1
    print(f"[ok] target {target} — {checked} file diverifikasi, 0 masalah")
    return 0


def write_lockfile(target: Path) -> int:
    if not MANIFEST_PATH.is_file():
        print("[error] manifest.json tidak ada — generate dulu")
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text())
    now = datetime.now(timezone.utc).isoformat()
    lock = {
        "version": 1,
        "updatedAt": now,
        "skills": {
            name: {
                "source": "Bank Pusat",
                "domain": entry["domain"],
                "bundleHash": entry["bundleHash"],
                "syncedAt": now,
            }
            for name, entry in sorted(manifest["skills"].items())
        },
    }
    target.mkdir(parents=True, exist_ok=True)
    lock_path = target / "skills-lock.json"
    lock_path.write_text(json.dumps(lock, indent=2) + "\n")
    print(f"[ok] skills-lock.json ditulis: {lock_path} ({len(lock['skills'])} skill)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Manifest SHA-256 Skill Bank Niumination")
    ap.add_argument("--check", action="store_true", help="Verifikasi manifest vs bank")
    ap.add_argument("--verify-target", metavar="DIR", help="Verifikasi salinan target vs manifest")
    ap.add_argument("--structure", choices=["flat", "domain"], default="flat",
                    help="Struktur target: flat=<dir>/<skill>/ (Jcode), domain=<dir>/<domain>/<skill>/ (Hermes/USB)")
    ap.add_argument("--lockfile", metavar="DIR", help="Generate skills-lock.json di target")
    args = ap.parse_args()

    if not BANK_DIR.is_dir():
        print(f"[error] bank tidak ditemukan: {BANK_DIR}")
        return 1

    if args.check:
        return check_bank()
    if args.verify_target:
        return verify_target(Path(args.verify_target).expanduser(), args.structure)
    if args.lockfile:
        return write_lockfile(Path(args.lockfile).expanduser())

    manifest = generate_manifest()
    write_manifest(manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())

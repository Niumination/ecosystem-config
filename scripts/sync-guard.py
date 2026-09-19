#!/usr/bin/env python3
"""sync-guard.py — penjaga "never clobber" untuk sinkronisasi bank -> target.

MASALAH YANG DICEGAH
--------------------
`sync-to-agents.sh` menyalin dengan `rsync -a` (tanpa --delete). Skill BARU di target aman,
tetapi suntingan pada FILE yang SUDAH ada di bank akan ditimpa tanpa peringatan.
Kasus nyata 19 Sep 2026: software-development/hermes-terminal-workflows di target 8.097 B
(lebih baru, lebih kaya) tertimpa versi bank 5.391 B - kerja hilang.

GRANULARITAS: PER-FILE (bukan per-skill)
----------------------------------------
Memblokir seluruh skill terlalu kasar: berkas pendukung yang hanya ada di target
(references/, templates/, scripts/) tidak pernah dihapus rsync tanpa --delete, jadi
tidak perlu memblokir apa pun - cukup dilaporkan sebagai kandidat promosi.
Yang benar-benar diblokir hanya FILE yang isinya berbeda dan terbukti disunting di target.

CARA MEMBEDAKAN "target disunting" vs "bank berubah"
----------------------------------------------------
Snapshot `~/.hermes/skills/.sync-state.json` mencatat hash setiap file target SESUDAH sync
terakhir. Maka untuk file yang ada di kedua sisi:
  target_hash == bank_manifest_hash          -> aman (target memang salinan bank)
  target_hash != bank, == state_hash         -> BANK berubah -> aman ditimpa sync
  target_hash != bank, != state_hash         -> TARGET disunting lokal -> KONFLIK
  tidak ada catatan state (pertama kali)     -> asal tak diketahui -> KONFLIK (konservatif)

Mode:
  --conflicts        cetak daftar "rel:file" yang HARUS DILEWATI sync (satu per baris)
  --conflicts-json   sama, dalam JSON (termasuk catatan target-only)
  --write-state      tulis/perbarui snapshot state (jalankan SESUDAH sync sukses)
  --status           ringkasan manusia

Exit: 0 selalu (kecuali error teknis) - penjaga tidak boleh mematikan caller.
Path bisa di-override lewat env NIU_BANK / NIU_TARGET untuk pengujian di sandbox.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
from datetime import datetime, timezone

BANK = pathlib.Path(os.environ.get("NIU_BANK", "/Users/zaryu/Desktop/Niumination/skills"))
TARGET = pathlib.Path(os.environ.get("NIU_TARGET", pathlib.Path.home() / ".hermes" / "skills"))
STATE = TARGET / ".sync-state.json"
MANIFEST = BANK / "manifest.json"
SKIP_FILES = {".DS_Store"}
SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".pytest_cache"}


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_json(p: pathlib.Path, default):
    try:
        return json.loads(p.read_text())
    except Exception:
        return default


def skipped(p: pathlib.Path) -> bool:
    return p.name in SKIP_FILES or any(part in SKIP_DIRS for part in p.parts)


def bank_skills() -> dict:
    man = load_json(MANIFEST, {})
    return man.get("skills", {}) if isinstance(man, dict) else {}


def scan() -> dict:
    """Kembalikan konflik (per-file) + catatan berkas yang hanya ada di target."""
    man = bank_skills()
    st = load_json(STATE, {"skills": {}}).get("skills", {})
    conflicts: dict[str, list[str]] = {}
    target_only: dict[str, list[str]] = {}
    ok = missing = 0

    for rel, entry in sorted(man.items()):
        tdir = TARGET / rel
        if not tdir.is_dir():
            missing += 1
            continue
        bank_files = entry.get("files", {}) or {}
        st_files = (st.get(rel) or {}).get("files", {}) or {}
        reasons: list[str] = []

        for frel, bhash in sorted(bank_files.items()):
            tf = tdir / frel
            if not tf.is_file():
                continue                                    # akan ditambahkan sync
            th = sha(tf)
            if th == bhash:
                continue                                    # target == bank
            prev = st_files.get(frel)
            if prev is None:
                reasons.append(f"{frel}: berbeda dari bank, asal tidak diketahui (belum ada state)")
            elif th != prev:
                reasons.append(f"{frel}: disunting di target sesudah sync terakhir")

        for tf in sorted(tdir.rglob("*")):
            if not tf.is_file() or skipped(tf):
                continue
            frel = tf.relative_to(tdir).as_posix()
            if frel not in bank_files:
                target_only.setdefault(rel, []).append(frel)

        if reasons:
            conflicts[rel] = reasons
        else:
            ok += 1

    return {"conflicts": conflicts, "ok": ok, "missing_target": missing,
            "total": len(man), "target_only": target_only}


def write_state() -> int:
    """Snapshot SESUDAH sync.

    PENTING: skill yang sedang KONFLIK tidak boleh diperbarui state-nya. Kalau hash target
    yang sudah disunting ikut direkam, run berikutnya akan membaca "target == state" dan
    menyimpulkan suntingan itu berasal dari bank - proteksi hilang tepat setelah satu siklus.
    State lama untuk skill konflik dipertahankan supaya konflik tetap terdeteksi.
    """
    man = bank_skills()
    prev = load_json(STATE, {"skills": {}}).get("skills", {})
    conflicts = set(scan()["conflicts"])
    skills = {}
    now = datetime.now(timezone.utc).isoformat()
    for rel in sorted(man):
        tdir = TARGET / rel
        if not tdir.is_dir():
            continue
        if rel in conflicts:
            if rel in prev:
                skills[rel] = prev[rel]          # pertahankan catatan lama
            continue                              # tanpa catatan baru = tetap konflik
        files = {tf.relative_to(tdir).as_posix(): sha(tf)
                 for tf in sorted(tdir.rglob("*")) if tf.is_file() and not skipped(tf)}
        skills[rel] = {"files": files, "syncedAt": now}
    STATE.write_text(json.dumps({"version": 1, "updatedAt": now, "skills": skills}, indent=2) + "\n")
    print(f"[guard] state ditulis: {STATE} ({len(skills)} skill)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--conflicts", action="store_true")
    ap.add_argument("--conflicts-json", action="store_true")
    ap.add_argument("--write-state", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()

    if a.write_state:
        return write_state()

    res = scan()
    if a.conflicts:
        for rel, files in res["conflicts"].items():
            for f in files:
                print(f"{rel}:{f.split(':')[0]}")
        return 0
    if a.conflicts_json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    n = len(res["conflicts"])
    print(f"[guard] skill bank dipantau: {res['total']} · aman: {res['ok']} · "
          f"konflik: {n} · belum ada di target: {res['missing_target']}")
    for rel, why in res["conflicts"].items():
        print(f"  KONFLIK {rel}")
        for w in why[:4]:
            print(f"      - {w}")
    tonly = res.get("target_only") or {}
    if tonly:
        total = sum(len(v) for v in tonly.values())
        print(f"  catatan: {total} berkas hanya ada di target pada {len(tonly)} skill "
              f"(tidak memblokir sync - kandidat promosi berkas pendukung)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

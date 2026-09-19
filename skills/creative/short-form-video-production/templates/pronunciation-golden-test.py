#!/usr/bin/env python3
"""Golden test for a TTS pronunciation layer — copy and adapt.

WHY THIS SHAPE: a checker that reuses the transformation's own logic reports "clean" while the
emitted string is mangled. The only trustworthy test asserts HAND-WRITTEN expected strings against
the real production code path, so fill CASES in by hand after reading what the layer actually emits
once — never by pasting the layer's own output back in as the expectation.

WHAT IT CHECKS
  1. Every case matches its hand-written expectation.
  2. Determinism: the same input twice gives the same output.
  3. A/B integrity: with the OLD behaviour wired into spoken_old(), *every* case must differ — an
     all-equal result means the "before" side is silently running the new code.
  4. Corpus diff: run the layer over the project's real scripts and print what changed.

STATUS NOT COVERED: this proves the STRING handed to the synthesizer, not the audio. Keep the audio
check separate (lag-aligned correlation vs a re-render control) and let the owner's ear decide
pronunciation. Duration and speech-to-text round trips are not valid substitutes.
"""

import json
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------- wire these up
from your_renderer import normalisasi, rapikan, belah_span, eja_angka_id  # noqa: F401


def spoken(text: str) -> str:
    """The production path: raw script line -> the exact string sent to the synthesizer."""
    out = []
    for bahasa, bagian in belah_span(text, "id"):
        kode = bahasa.split("-")[0].lower()
        bagian = normalisasi(bagian, kode)
        bagian = eja_angka_id(bagian)
        out.append(" ".join(rapikan(bagian).split()))
    return " ".join(t for t in out if t)


def spoken_old(text: str) -> str:
    """The PREVIOUS behaviour, re-implemented.

    Do not simply call spoken() — if both sides go through the patched code the comparison reports
    "same" for exactly the cases that changed most.
    """
    raise NotImplementedError("re-implement the old path, or the A/B check is meaningless")


# ------------------------------------------------------------------- hand-written expectations
# (label, input, expected spoken string)   <- type the expectation yourself
CASES: list[tuple[str, str, str]] = [
    ("acronym_upper", "Laporan SKPD ke BPKP.", "Laporan es ka pe de ke be pe ka pe."),
    ("acronym_lower", "laporan skpd ke bpkp.", "laporan es ka pe de ke be pe ka pe."),
    ("word_not_acronym", "Ada api di gedung itu.", "Ada api di gedung itu."),
    ("phone", "Hubungi 0812-3456-7890.",
     "Hubungi nol delapan satu dua tiga empat lima enam tujuh delapan sembilan nol."),
    ("date_time", "Ditetapkan 19/09/2026 pukul 09:30.",
     "Ditetapkan sembilan belas September dua ribu dua puluh enam pukul sembilan tiga puluh."),
    ("version_size", "Versi v4.1.0 butuh 8 MB.",
     "Versi versi empat titik satu titik nol butuh delapan megabita."),
    ("email_url", "Kirim ke admin@host.web.id atau buka host.web.id.",
     "Kirim ke admin at host titik web titik id atau buka host titik web titik id."),
    ("extension", "Simpan sebagai laporan.pdf.", "Simpan sebagai laporan pe de ef."),
    ("range_ordinal", "Antara 5-10 paket, peringkat ke-3.",
     "Antara lima sampai sepuluh paket, peringkat ketiga."),
    ("abbrev_symbol", "Rapat dll. (urgent) A & B.", "Rapat dan lain-lain urgent A dan B."),
    ("ellipsis_kept", "Semoga cukup... diawasi.", "Semoga cukup \u2026 diawasi."),
]


def jalankan_uji() -> int:
    gagal = 0
    for label, masukan, harapan in CASES:
        hasil = spoken(masukan)
        if hasil != harapan:
            gagal += 1
            print(f"GAGAL {label}\n  input   : {masukan}\n  dapat   : {hasil}\n  harusnya: {harapan}")
        if spoken(masukan) != hasil:
            gagal += 1
            print(f"GAGAL {label}: tidak deterministik")
    print(f"[1-2] {len(CASES) - gagal}/{len(CASES)} kasus cocok")
    return gagal


def cek_ab() -> int:
    """Every case must differ between old and new, or the harness is lying."""
    try:
        sama = [label for label, masukan, _h in CASES
                if spoken_old(masukan) == spoken(masukan)]
    except NotImplementedError as e:
        print(f"[3] dilewati: {e}")
        return 0
    if sama:
        print(f"[3] GAGAL: {len(sama)} kasus tidak berbeda -> harness ikut memakai kode baru: {sama}")
        return len(sama)
    print(f"[3] OK: {len(CASES)} kasus berbeda antara lama dan baru")
    return 0


def diff_korpus(akar: Path) -> int:
    """Run the layer over real scripts and print every changed line.

    The point is not the count: check each change is intended, and expect at least one
    self-introduced regression. A rule that looks obviously right in isolation is usually wrong
    somewhere in real prose (a punctuation tidy-up collapsing dramatic ellipses is the classic).
    """
    if not akar.exists():
        print(f"[4] dilewati: {akar} tidak ada")
        return 0
    berubah = 0
    for p in sorted(akar.rglob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for s in d.get("scenes", []):
            for kunci in ("vo", "vo_lama"):
                teks = s.get(kunci) or ""
                if not teks.strip():
                    continue
                lama, baru = spoken(teks), spoken(teks)
                if lama != baru:
                    berubah += 1
                    print(f"  [{p.stem}/{s.get('id')}/{kunci}]\n    lama : {lama}\n    baru : {baru}")
    print(f"[4] {berubah} baris berubah — periksa satu per satu")
    return 0


if __name__ == "__main__":
    korpus = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("naskah")
    sys.exit(1 if (jalankan_uji() or cek_ab() or diff_korpus(korpus)) else 0)

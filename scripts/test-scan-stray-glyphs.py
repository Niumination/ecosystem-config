#!/usr/bin/env python3
"""Self-test untuk scripts/scan-stray-glyphs.py.

    python3 scripts/test-scan-stray-glyphs.py

Gate ini hanya berguna kalau ia tidak salah menandai dokumen bersih. Dua arah
diuji: artefak skrip asing harus tertangkap, dan corpus yang sah (emoji,
box-drawing, matematika, aksen Latin, contoh berkode blok) harus tetap lolos.
"""
import importlib.util
import sys
import tempfile
from pathlib import Path

SCANNER = Path(__file__).with_name("scan-stray-glyphs.py")
spec = importlib.util.spec_from_file_location("stray", SCANNER)
if spec is None or spec.loader is None:
    raise SystemExit(f"tidak bisa memuat {SCANNER}")
stray = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stray)

CASES = [
    # (nama, teks, harapan: "CATCH" atau "clean")
    ("artifacts_cjk", "Temuan最重要的 yang harus ditetapkan", "CATCH"),
    ("artifacts_cyrillic", "berkas yang的感情 sudah memenuhi", "CATCH"),
    ("artifacts_hangul", "perlu langkah 操作 dari Windows", "CATCH"),
    ("clean_emoji", "Status: ✅ selesai ⚠️ hati-hati ⏳ tunggu ❌ gagal ⭐", "clean"),
    ("clean_boxdraw", "├── index.html\n└── package.json\n\n# ── Judul ──", "clean"),
    ("clean_math", "level −20 dB, ≤3 org, 1920×1080, ±1, √2, 3π ≈ 9.42", "clean"),
    ("clean_latin_diacritics", "café naïve Müller ç ñ é ü", "clean"),
    ("clean_quotes", "smart “quotes” and ‘apostrophes’ plus em—dash and ellipsis…", "clean"),
    # Dokumentasi tentang korupsi teks harus boleh mengutip korupsinya.
    ("doc_in_fenced_block",
     "```\ncorrect → Temuan最重要的 yang ditetapkan\n```", "clean"),
]


def main():
    failures = 0
    for name, text, expect in CASES:
        tmp = Path(tempfile.mkstemp(suffix=".md")[1])
        tmp.write_text(text, encoding="utf-8")
        hits = len(stray.foreign_glyphs(tmp))
        tmp.unlink()
        got = "CATCH" if hits else "clean"
        ok = got == expect
        failures += not ok
        print(f"  {'PASS' if ok else 'FAIL'} {name:<26} hits={hits} expect={expect}")

    print()
    if failures:
        print(f"STRAY_GLYPH_TEST_FAIL ({failures}/{len(CASES)})")
        return 1
    print(f"STRAY_GLYPH_TEST_PASS ({len(CASES)}/{len(CASES)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
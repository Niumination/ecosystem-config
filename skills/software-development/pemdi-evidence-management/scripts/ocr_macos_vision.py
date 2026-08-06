#!/usr/bin/env python3
"""OCR a rendered PNG via macOS Vision framework (pyobjc) — offline, free.

Usage:
    python3 ocr_macos_vision.py <image.png>
    # batch: render PDF pages first with pymupdf:
    #   import fitz; pix = fitz.open(pdf)[i].get_pixmap(dpi=150); pix.save(f'p{i}.png')

Verified 5 Agu 2026 on scanned Indonesian gov PDFs (SK, perbup, surat undangan).
Pitfalls baked in (do not "fix"):
  - .fast recognition level — .accurate hangs without callback on this setup
  - usesLanguageCorrection=False — correction path hangs too
  - en-US language — works fine on Indonesian text; id-ID was unnecessary
  - run in main thread (Vision needs an active runloop)
Do NOT rewrite this in swiftc — first compile takes 3+ min; pyobjc is instant.
"""
import sys
import Vision
from Foundation import NSURL


def ocr_image(path: str) -> str:
    url = NSURL.fileURLWithPath_(path)
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelFast)
    request.setUsesLanguageCorrection_(False)
    request.setRecognitionLanguages_(["en-US"])
    ok, err = handler.performRequests_error_([request], None)
    if not ok:
        raise RuntimeError(f"OCR failed: {err}")
    lines = []
    for obs in request.results() or []:
        lines.append(obs.topCandidates_(1)[0].string())
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    print(ocr_image(sys.argv[1]))

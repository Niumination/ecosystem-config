#!/usr/bin/env python3
"""
ODL-PDF Batch — Ekstrak semua PDF Modul Indikator 1-20 ke Markdown.
Output: apps/PemdiAcehTengah/docs/modul-indikator/
"""

import os, sys, glob, json, time

SOURCE_DIR = "/Users/zaryu/Documents/Modul Indikator 1-20"
OUTPUT_DIR = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/docs/modul-indikator"
HERMES_PY = "/Users/zaryu/.hermes-portable/venv/bin/python3"
JAVA_HOME = "/usr/local/Cellar/openjdk/26.0.1/libexec/openjdk.jdk/Contents/Home"

os.environ["JAVA_HOME"] = JAVA_HOME
os.environ["PATH"] = f"{JAVA_HOME}/bin:/Users/zaryu/.local/bin:{os.environ.get('PATH','')}"

def main():
    pdfs = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.pdf")))
    if not pdfs:
        print("❌ Tidak ada PDF ditemukan di", SOURCE_DIR)
        sys.exit(1)

    print(f"📄 Menemukan {len(pdfs)} file PDF:")
    for p in pdfs:
        print(f"   - {os.path.basename(p)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n📁 Output: {OUTPUT_DIR}")
    print(f"⏳ Memulai ekstraksi ke Markdown...\n")

    # Build Python code to run in Hermes venv
    pdf_list_json = json.dumps(pdfs)
    
    code = f"""
import opendataloader_pdf, json, sys, os

os.environ["JAVA_HOME"] = "{JAVA_HOME}"
os.environ["PATH"] = "{JAVA_HOME}/bin:" + os.environ.get("PATH","")

pdfs = {pdf_list_json}
output_dir = "{OUTPUT_DIR}"

print(f"Memproses {{len(pdfs)}} file...")
opendataloader_pdf.convert(
    input_path=pdfs,
    output_dir=output_dir,
    format="markdown",
    quiet=True,
    keep_line_breaks=True,
)
print("DONE")
"""

    import subprocess
    result = subprocess.run(
        [HERMES_PY, "-c", code],
        capture_output=True, text=True, timeout=600,
        env={**os.environ, "JAVA_HOME": JAVA_HOME}
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        # Filter out noisy Java warnings
        for line in result.stderr.splitlines():
            if "WARNING" in line or "Error" in line or "Exception" in line:
                print(f"⚠️  {line}")

    # Verify output
    print("\n📋 Verifikasi output:")
    md_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "*.md")))
    json_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "*.json")))
    
    if md_files:
        print(f"   ✅ {len(md_files)} file Markdown:")
        for f in md_files:
            size_kb = os.path.getsize(f) / 1024
            print(f"      - {os.path.basename(f)} ({size_kb:.1f} KB)")
    else:
        print("   ❌ Tidak ada file Markdown dihasilkan")
        
    if json_files:
        print(f"\n   📎 {len(json_files)} file JSON (metadata):")
        for f in json_files:
            size_kb = os.path.getsize(f) / 1024
            print(f"      - {os.path.basename(f)} ({size_kb:.1f} KB)")

    if "DONE" in result.stdout:
        print(f"\n✅ Selesai! Semua {len(pdfs)} PDF berhasil diekstrak.")
    else:
        print(f"\n⚠️  Mungkin ada error. Cek stdout/stderr di atas.")

if __name__ == "__main__":
    t0 = time.time()
    main()
    t = time.time() - t0
    print(f"⏱  Waktu: {t:.1f}s")

#!/usr/bin/env python3
"""
OpenDataLoader PDF — Ekstrak PDF ke Markdown/JSON via Hermes.
Usage:  python3 odl-pdf.py <input.pdf> [--format markdown,json] [--output output_dir]

Dependencies: pip install opendataloader-pdf, Java 11+
"""

import sys, os, json, argparse

HERMES_PY = "/Users/zaryu/.hermes-portable/venv/bin/python3"
JAVA_HOME = "/usr/local/Cellar/openjdk/26.0.1/libexec/openjdk.jdk/Contents/Home"

def convert_pdf(input_path, output_dir, formats="markdown,json"):
    """Convert PDF to Markdown/JSON using OpenDataLoader."""
    if not os.path.exists(input_path):
        return {"error": f"File not found: {input_path}"}
    
    os.environ["JAVA_HOME"] = JAVA_HOME
    os.environ["PATH"] = f"/Users/zaryu/.local/bin:{os.environ.get('PATH','')}"
    
    import subprocess
    code = f"""
import opendataloader_pdf, json
opendataloader_pdf.convert(
    input_path='{input_path}',
    output_dir='{output_dir}',
    format='{formats}'
)
print('DONE')
"""
    result = subprocess.run(
        [HERMES_PY, "-c", code],
        capture_output=True, text=True, timeout=120,
        env={**os.environ, "JAVA_HOME": JAVA_HOME}
    )
    
    md_file = os.path.join(output_dir, os.path.basename(input_path).replace('.pdf', '.md'))
    json_file = os.path.join(output_dir, os.path.basename(input_path).replace('.pdf', '.json'))
    
    return {
        "status": "success" if "DONE" in result.stdout else "error",
        "markdown": md_file if os.path.exists(md_file) else None,
        "json": json_file if os.path.exists(json_file) else None,
        "pages": "see json"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenDataLoader PDF - Ekstrak PDF")
    parser.add_argument("input", help="Path to PDF file")
    parser.add_argument("--format", default="markdown,json", help="Output format(s)")
    parser.add_argument("--output", default="/tmp/odl-output", help="Output directory")
    args = parser.parse_args()
    
    result = convert_pdf(args.input, args.output, args.format)
    print(json.dumps(result, indent=2))

#!/usr/bin/env python3
"""
cleanup-modul.py — Bersihkan & Normalisasi 20 file Markdown Modul Indikator
Output: folder docs/modul-indikator-clean/ (siap inject ke website)

Yang dilakukan:
  1. Hapus header/footer noise (slide header "Milik Kementerian PANRB", dll)
  2. Normalisasi heading hierarchy (H1 → H2, pastikan setiap file mulai dgn H1)
  3. Hapus baris kosong berlebihan (max 1 blank line antar blok)
  4. Frontmatter title dari nama file
  5. Rapihin list dan formatting

Usage:  python3 scripts/cleanup-modul.py [--dry-run]
"""

import os, re, sys

SRC_DIR = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/docs/modul-indikator"
DST_DIR = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/docs/modul-indikator-clean"

HEADER_NOISE = [
    r"(?i)^Milik\s*$",
    r"(?i)^Kementerian\s*$", 
    r"(?i)^PANRB\s*$",
    r"(?i)^slide\s*\d+\s*$",
    r"(?i)^halaman\s*\d+\s*$",
]

CLEAN_TITLE_MAP = {
    "1": "Pilar 1 - Regulasi & Tata Kelola Pemdi",
    "2": "Aspek 1 - Indikator 2: Manajemen Layanan Digital",
    "3": "Aspek 1 - Indikator 3: Manajemen Keamanan Informasi",
    "4": "Aspek 2 - Indikator 4: Infrastruktur Pemdi",
    "5": "Aspek 2 - Indikator 5: Aplikasi & Layanan Digital",
    "6": "Indikator 6: Berbagi Pakai Data & Informasi Geospasial",
    "7": "Indikator 7: Layanan Data Satu Pintu",
    "8": "Indikator 8: Tingkat Kematangan Perlindungan Data Pribadi",
    "9": "Indikator 9: Pusat Data Pemerintah",
    "10": "Indikator 10: Jaringan Intra Pemerintah",
    "11": "Indikator 11: Sistem Penghubung Layanan",
    "12": "Indikator 12: Smart City & Inovasi Daerah",
    "13": "Indikator 13: Transparansi & Partisipasi Publik",
    "14": "Indikator 14: Anggaran TI & Digital",
    "15": "Indikator 15: SDM Digital & Literasi",
    "16": "Indikator 16: Keamanan Siber & Resiliensi",
    "17": "Indikator 17: Kualitas Layanan Digital",
    "18": "Indikator 18: Kepuasan Pengguna",
    "19": "Indikator 19: Kapabilitas Proses Bisnis",
    "20": "Indikator 20: Evaluasi & Rekomendasi Kebijakan",
}

def get_title_from_file(fname):
    match = re.search(r'(?<!Revamp\s)(\d+)\s', fname)
    if match:
        num = match.group(1)
        if num in CLEAN_TITLE_MAP:
            return CLEAN_TITLE_MAP[num]
    return f"Modul Indikator — {fname.replace('.md','')}"

def is_header_noise(line):
    clean = line.strip()
    if not clean:
        return False
    for pattern in HEADER_NOISE:
        if re.match(pattern, clean):
            return True
    # Single-word lines that look like headers but aren't headings
    single_words = ["milik", "kementerian", "panrb", "slide", "halaman", "page"]
    if clean.lower() in single_words and len(clean.split()) == 1:
        return True
    return False

def clean_file(fpath, dry_run=False):
    """Clean a single markdown file."""
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    title = get_title_from_file(fname)
    
    # Remove BOM
    if lines and lines[0].startswith('\ufeff'):
        lines[0] = lines[0][1:]
    
    # Phase 1: Remove header noise (first few lines that are slide headers)
    cleaned = []
    noise_ended = False
    text_started = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines before text starts
        if not text_started and not stripped:
            continue
        
        if not text_started:
            text_started = True
        
        # Check for noise in first 5 non-empty lines
        if not noise_ended and i < 15:
            if is_header_noise(line):
                continue
            else:
                noise_ended = True
        
        # Check for single-word noise mixed in content (slide footers)
        if stripped and len(stripped.split()) <= 2 and i > 0:
            skip = False
            for pattern in HEADER_NOISE:
                if re.match(pattern, stripped):
                    skip = True
                    break
            # Only skip if followed by an image or empty line
            if skip:
                next_lines = lines[i+1:i+3]
                next_stripped = [l.strip() for l in next_lines if l.strip()]
                if next_stripped and not next_stripped[0].startswith('!['):
                    skip = False
            if skip:
                continue
        
        cleaned.append(line)
    
    # Re-join
    text = ''.join(cleaned)
    
    # Phase 2: Normalize headings
    has_h1 = bool(re.search(r'^# ', text, re.MULTILINE))
    if not has_h1:
        # Add frontmatter title as H1
        text = f"# {title}\n\n{text}"
    
    # Phase 3: Fix heading levels - ensure H1 is the document title, 
    # everything else shifted appropriately
    lines = text.split('\n')
    new_lines = []
    first_h1_found = False
    
    for line in lines:
        if line.startswith('# '):
            if not first_h1_found:
                # Replace first H1 with clean title
                new_lines.append(f"# {title}")
                first_h1_found = True
            else:
                # Extra H1 → H2
                new_lines.append('#' + line)
        elif line.startswith('#### '):
            # H4 → bold paragraph
            content = line[5:].strip()
            new_lines.append(f"**{content}**")
        else:
            new_lines.append(line)
    
    text = '\n'.join(new_lines)
    
    # Phase 4: Remove excessive blank lines (max 1)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Phase 5: Fix image paths - make them relative
    text = re.sub(r'!\[\]\(<([^>]+)>\)', r'![](\1)', text)
    # Remove relative path prefix from images
    text = re.sub(r'!\[\]\(.*?_images/', r'![](_images/', text)
    
    # Phase 6: Ensure file ends with newline
    text = text.strip() + '\n'
    
    if dry_run:
        # Count stats
        orig_lines = len(open(fpath, 'r').readlines())
        new_line_count = len(text.split('\n'))
        images = len(re.findall(r'!\[\]\(', text))
        h1 = len(re.findall(r'^# ', text, re.MULTILINE))
        h2 = len(re.findall(r'^## ', text, re.MULTILINE))
        return {
            "file": fname,
            "title": title,
            "original_lines": orig_lines,
            "cleaned_lines": new_line_count,
            "images": images,
            "h1": h1,
            "h2": h2,
        }
    
    # Write cleaned version
    os.makedirs(DST_DIR, exist_ok=True)
    dst_path = os.path.join(DST_DIR, fname)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    # Copy images directory
    img_dir = fpath.replace('.md', '_images')
    dst_img_dir = dst_path.replace('.md', '_images')
    if os.path.isdir(img_dir) and not os.path.isdir(dst_img_dir):
        import shutil
        shutil.copytree(img_dir, dst_img_dir, symlinks=True)
    
    return {
        "file": fname,
        "status": "cleaned",
        "size": len(text),
    }

def main():
    dry_run = '--dry-run' in sys.argv
    
    files = sorted([f for f in os.listdir(SRC_DIR) if f.endswith('.md')])
    print(f"Found {len(files)} markdown files")
    
    results = []
    for fname in files:
        fpath = os.path.join(SRC_DIR, fname)
        result = clean_file(fpath, dry_run)
        results.append(result)
        
        if dry_run:
            print(f"  {result['file']}: {result['original_lines']}→{result['cleaned_lines']} lines | {result['images']} img | H1:{result['h1']} H2:{result['h2']}")
        else:
            print(f"  ✅ {result['file']} → {result['size']:,} bytes")
    
    if dry_run:
        print(f"\nSummary: {len(results)} files")
        print(f"Total H1 headings: {sum(r['h1'] for r in results)}")
        print(f"Files without H1 (before fix): {sum(1 for r in results if r['h1'] == 0)}")
        print(f"Total images: {sum(r['images'] for r in results)}")
    else:
        print(f"\n✅ Done! Cleaned files in: {DST_DIR}")
        print(f"Total size: {sum(r['size'] for r in results):,} bytes")

if __name__ == '__main__':
    main()

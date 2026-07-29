#!/usr/bin/env python3
"""
Extract structured data from modul indikator markdowns.
Output: structured JSON for the modul-indikator page.
"""

import os, re, json, glob

MODUL_DIR = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/docs/modul-indikator"
OUTPUT = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/data/modul-indikator.json"

# Mapping modul number -> indikator ID in pemdi.json
MODUL_TO_IND = {
    1: "I1", 2: "I2", 3: "I3", 4: "I4", 5: "I5",
    6: "I6", 7: "I7", 8: "I8", 9: "I9", 10: "I10",
    11: "I11", 12: "I12", 13: "I13", 14: "I14", 15: "I15",
    16: "I16", 17: "I17", 18: "I18", 19: "I19", 20: "I20",
}

def clean_text(text):
    """Clean extraneous formatting from extracted text."""
    text = re.sub(r'!\[\]\([^)]+\)', '', text)  # Remove image refs
    text = re.sub(r'\|.*?\|', '', text)  # Remove malformed table lines
    text = re.sub(r'#{1,6}\s*', '', text)  # Remove markdown headers
    text = re.sub(r'\*\*', '', text)  # Remove bold markers
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    return text

def extract_content(md_path):
    """Extract key sections from a modul markdown file."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {
        "deskripsi": "",
        "level_kriteria": [],
        "data_dukung": []
    }
    
    lines = content.split('\n')
    current_section = None
    buffer = []
    
    # Simple section extraction
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip image-only lines
        if stripped.startswith('![]('):
            continue
            
        # Detect sections
        if stripped.startswith('### ') or stripped.startswith('## '):
            section_name = stripped.lstrip('#').strip().lower()
            
            if 'deskripsi' in section_name or 'pendahuluan' in section_name or 'latar belakang' in section_name:
                current_section = 'deskripsi'
                buffer = []
            elif 'kriteria' in section_name or 'kondisi' in section_name or 'level' in section_name:
                current_section = 'kriteria'
                buffer = []
            elif 'data dukung' in section_name or 'bukti' in section_name or 'contoh' in section_name:
                current_section = 'data_dukung'
                buffer = []
            else:
                current_section = None
                buffer = []
            continue
        
        if current_section and stripped and not stripped.startswith('|') and not stripped.startswith('!['):
            buffer.append(stripped)
    
    # Get full text for each section
    full_text = clean_text(content)
    
    # Extract deskripsi - first meaningful paragraph
    paras = [p.strip() for p in full_text.split('\n\n') if len(p.strip()) > 50]
    if paras:
        result['deskripsi'] = paras[0]
    
    # Try to find level criteria sections
    level_patterns = [
        (r'(?:Level|Tingkat)\s*1[\.:\)]?\s*(.*?)(?=(?:Level|Tingkat)\s*2|$)', 1),
        (r'(?:Level|Tingkat)\s*2[\.:\)]?\s*(.*?)(?=(?:Level|Tingkat)\s*3|$)', 2),
        (r'(?:Level|Tingkat)\s*3[\.:\)]?\s*(.*?)(?=(?:Level|Tingkat)\s*4|$)', 3),
        (r'(?:Level|Tingkat)\s*4[\.:\)]?\s*(.*?)(?=(?:Level|Tingkat)\s*5|$)', 4),
        (r'(?:Level|Tingkat)\s*5[\.:\)]?\s*(.*?)(?=(?:Level|Tingkat)\s*[1-5]|$)', 5),
    ]
    
    # Also try Kurang/Initiate, Cukup, Baik, etc pattern
    kategori_levels = [
        (r'(?:Kurang|Initiate|Nilai\s*<\s*1[.,]?5).*?(?=(?:Cukup|Sedang|Level|Tingkat|Memuaskan))', 1),
    ]
    
    found_levels = {}
    for pattern, level in level_patterns:
        m = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
        if m:
            txt = clean_text(m.group(1))
            if len(txt) > 20:
                found_levels[level] = txt[:300]
    
    for level in sorted(found_levels.keys()):
        result['level_kriteria'].append({
            "level": level,
            "kriteria": found_levels[level]
        })
    
    # Extract data dukung - lines mentioning "Data Dukung" or items
    in_data_dukung = False
    data_items = []
    for line in lines:
        s = line.strip()
        if 'data dukung' in s.lower():
            in_data_dukung = True
            continue
        if in_data_dukung and s.startswith('### '):
            break
        if in_data_dukung and s and not s.startswith('![') and not s.startswith('|'):
            cleaned = clean_text(s)
            if len(cleaned) > 10:
                data_items.append(cleaned)
    
    result['data_dukung'] = data_items[:10]
    
    return result

def main():
    modules = []
    md_files = sorted(glob.glob(os.path.join(MODUL_DIR, "*.md")))
    
    for md_path in md_files:
        basename = os.path.basename(md_path)
        
        # Extract modul number
        num_match = re.match(r'(\d+)', basename)
        if not num_match:
            continue
        
        num = int(num_match.group(1))
        indikator_id = MODUL_TO_IND.get(num, f"I{num}")
        
        content = extract_content(md_path)
        
        # Read raw content and count text vs images
        with open(md_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        
        image_count = len(re.findall(r'!\[\]\([^)]+\)', raw))
        text_lines = len([l for l in raw.split('\n') if l.strip() and not l.strip().startswith('![](')])
        
        modules.append({
            "nomor": num,
            "indikator_id": indikator_id,
            "file": basename,
            "image_count": image_count,
            "text_lines": text_lines,
            **content
        })
    
    output = {
        "total_modul": len(modules),
        "modules": modules
    }
    
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Extracted {len(modules)} modules to {OUTPUT}")

if __name__ == "__main__":
    main()

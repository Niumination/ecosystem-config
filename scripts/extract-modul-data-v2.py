#!/usr/bin/env python3
"""
Extract level criteria and evidence requirements from all 20 modul markdowns.
Since the PPT-based PDF markdown has inconsistent structure, we use multiple strategies.
"""

import os, re, json, glob

MODUL_DIR = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/docs/modul-indikator"
PEMDI_JSON = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/data/pemdi.json"
OUTPUT = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/data/modul-indikator.json"

# Load existing pemdi data for cross-reference
with open(PEMDI_JSON) as f:
    pemdi = json.load(f)

# Build lookup: indikator_id -> data from pemdi
indikator_map = {}
for aspek in pemdi['aspek']:
    for ind in aspek['indikator']:
        indikator_map[ind['id']] = {
            'aspek_nama': aspek['nama'],
            'aspek_singkat': aspek.get('singkat',''),
            'indikator': ind
        }

def extract_levels_advanced(text):
    """Extract level-based criteria from messy PPT markdown."""
    levels = {}
    
    # Strategy 1: Look for explicit level/tingkat markers
    level_headers = re.findall(
        r'(?:(?:Level|Tingkat)\s*(\d+)|(?:Nilai)\s*(?:<|>)\s*[\d,]+|'
        r'(?:Kurang/Initiate)|(?:Cukup/Emerging)|(?:Memuaskan/Leading)|'
        r'(?:Terpadu/Transformasi))',
        text, re.IGNORECASE
    )
    
    # Strategy 2: Look for paragraphs near known level keywords
    lines = text.split('\n')
    current_level = None
    level_buffer = []
    
    for line in lines:
        s = line.strip()
        if not s or s.startswith('![](') or s.startswith('|'):
            continue
            
        # Detect level indicators
        lower = s.lower()
        level_match = None
        if 'kurang' in lower and ('initiate' in lower or 'nilai' in lower):
            level_match = 1
        elif 'cukup' in lower and ('emerging' in lower or 'nilai' in lower):
            level_match = 2
        elif 'baik' in lower and ('established' in lower or 'nilai' in lower):
            level_match = 3
        elif 'sangat baik' in lower or ('memuaskan' in lower and 'leading' in lower):
            level_match = 4
        elif 'terpadu' in lower or ('transformasi' in lower):
            level_match = 5
        elif re.match(r'(?:Level|Tingkat)\s*(\d+)', s, re.IGNORECASE):
            level_match = int(re.match(r'(?:Level|Tingkat)\s*(\d+)', s, re.IGNORECASE).group(1))
        
        if level_match:
            if current_level and level_buffer:
                text_content = ' '.join(level_buffer)
                if len(text_content) > 20:
                    levels[current_level] = text_content[:500]
            current_level = level_match
            level_buffer = []
        elif current_level:
            level_buffer.append(s)
    
    # Don't forget the last level
    if current_level and level_buffer:
        text_content = ' '.join(level_buffer)
        if len(text_content) > 20:
            levels[current_level] = text_content[:500]
    
    return levels

def extract_data_dukung(text):
    """Extract evidence requirements mentioned in the modul."""
    items = []
    in_section = False
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        s = line.strip()
        if 'data dukung' in s.lower() or 'contoh bukti' in s.lower():
            in_section = True
            continue
        if in_section:
            if s.startswith('### ') or s.startswith('## '):
                if 'data dukung' not in s.lower():
                    break
            if s and not s.startswith('![](') and not s.startswith('|') and not s.startswith('---'):
                cleaned = re.sub(r'<[^>]+>', '', s).strip()
                if len(cleaned) > 15:
                    items.append(cleaned)
    
    return items[:8]

def extract_recommendations(text):
    """Extract any actionable recommendations."""
    recs = []
    # Look for patterns like "langkah", "rekomendasi", "strategi"
    lines = text.split('\n')
    for line in lines:
        s = line.strip().lower()
        if any(kw in s for kw in ['rekomendasi', 'langkah strategis', 'tahapan', 'prioritas']):
            cleaned = re.sub(r'<[^>]+>', '', line).strip()
            if len(cleaned) > 20:
                recs.append(cleaned)
    return recs

def main():
    md_files = sorted(glob.glob(os.path.join(MODUL_DIR, "*.md")))
    
    # Handle modul 8 with special filename
    modul8_path = os.path.join(MODUL_DIR, "Revisi Materi PEMDI_Indikator 8 Tingkat Kematangan Pelindungan Data Pribadi.md")
    
    modules = []
    
    for md_path in md_files:
        basename = os.path.basename(md_path)
        
        # Extract number from filename
        num_match = re.match(r'(\d+)', basename)
        # Special case for the "Revisi" file (it's modul 8)
        if not num_match and 'indikator 8' in basename.lower():
            num = 8
        elif not num_match:
            continue
        else:
            num = int(num_match.group(1))
        
        indikator_id = f"I{num}"
        ref = indikator_map.get(indikator_id, {})
        
        with open(md_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Remove image references for text analysis
        text_clean = re.sub(r'!\[\]\([^)]+\)', '', text)
        text_clean = re.sub(r'<[^>]+>', '', text_clean)
        text_clean = re.sub(r'#{1,6}\s*', '', text_clean)
        text_clean = re.sub(r'\*\*', '', text_clean)
        text_clean = re.sub(r'\n{3,}', '\n', text_clean)
        
        # Get first meaningful paragraph as description
        paras = [p.strip() for p in text_clean.split('\n') if len(p.strip()) > 60]
        deskripsi = paras[0][:400] if paras else ref.get('indikator', {}).get('deskripsi', '')
        
        # Extract levels
        levels = extract_levels_advanced(text)
        level_kriteria = []
        for lvl in sorted(levels.keys()):
            level_kriteria.append({
                "level": lvl,
                "kriteria": levels[lvl]
            })
        
        # If no levels detected, try to get from the text directly
        if not level_kriteria:
            # Fallback: just look for any paragraphs mentioning level-like concepts
            for line in text_clean.split('\n'):
                s = line.strip()
                if any(kw in s.lower() for kw in ['kriteria', 'kondisi', 'inisiatif', 'terdefinisi']):
                    if len(s) > 40:
                        level_kriteria.append({
                            "level": 0,
                            "kriteria": s[:400]
                        })
                        break
        
        # Extract data dukung examples
        data_dukung = extract_data_dukung(text)
        
        # Extract recommendations
        rekomendasi = extract_recommendations(text)
        
        # Count images
        image_count = len(re.findall(r'!\[\]\([^)]+\)', text))
        
        modules.append({
            "nomor": num,
            "indikator_id": indikator_id,
            "aspek": ref.get('aspek_nama', ''),
            "judul": ref.get('indikator', {}).get('nama', ''),
            "deskripsi": deskripsi or ref.get('indikator', {}).get('deskripsi', ''),
            "image_count": image_count,
            "level_kriteria": level_kriteria,
            "data_dukung_modul": data_dukung,
            "rekomendasi": rekomendasi
        })
    
    # Sort by number
    modules.sort(key=lambda m: m['nomor'])
    
    output = {
        "total_modul": len(modules),
        "modules": modules
    }
    
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Extracted {len(modules)} modules to {OUTPUT}")
    for m in modules:
        print(f"   I{m['nomor']:02d}: {len(m['level_kriteria'])} levels, {len(m['data_dukung_modul'])} evidence items")

if __name__ == "__main__":
    main()

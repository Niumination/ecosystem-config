#!/usr/bin/env python3
"""
build-modul-json.py — Convert cleaned markdown files to website-ready JSON.
Output: data/modul-indikator.json (importable by Next.js pages)

Mengkonversi 20 file markdown modul indikator menjadi format JSON yang
siap di-inject ke website PemdiAcehTengah.
"""

import os, json, re, sys

CLEAN_DIR = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/docs/modul-indikator-clean"
DST_JSON = "/Users/zaryu/Desktop/Niumination/apps/PemdiAcehTengah/data/modul-indikator.json"

MODULE_ORDER = {
    "1": {"nomor": 1, "aspek": "Aspek 1 — Tata Kelola", "label": "Regulasi & Tata Kelola Pemdi"},
    "2": {"nomor": 2, "aspek": "Aspek 1 — Tata Kelola", "label": "Manajemen Layanan Digital"},
    "3": {"nomor": 3, "aspek": "Aspek 1 — Tata Kelola", "label": "Manajemen Keamanan Informasi"},
    "4": {"nomor": 4, "aspek": "Aspek 2 — Infrastruktur & Layanan", "label": "Infrastruktur Pemdi"},
    "5": {"nomor": 5, "aspek": "Aspek 2 — Infrastruktur & Layanan", "label": "Aplikasi & Layanan Digital"},
    "6": {"nomor": 6, "aspek": "Aspek 2 — Infrastruktur & Layanan", "label": "Berbagi Pakai Data & Informasi Geospasial"},
    "7": {"nomor": 7, "aspek": "Aspek 2 — Infrastruktur & Layanan", "label": "Layanan Data Satu Pintu"},
    "8": {"nomor": 8, "aspek": "Aspek 2 — Infrastruktur & Layanan", "label": "Perlindungan Data Pribadi"},
    "9": {"nomor": 9, "aspek": "Aspek 2 — Infrastruktur & Layanan", "label": "Pusat Data Pemerintah"},
    "10": {"nomor": 10, "aspek": "Aspek 2 — Infrastruktur & Layanan", "label": "Jaringan Intra Pemerintah"},
    "11": {"nomor": 11, "aspek": "Aspek 3 — Layanan Digital", "label": "Sistem Penghubung Layanan"},
    "12": {"nomor": 12, "aspek": "Aspek 3 — Layanan Digital", "label": "Smart City & Inovasi Daerah"},
    "13": {"nomor": 13, "aspek": "Aspek 3 — Layanan Digital", "label": "Transparansi & Partisipasi Publik"},
    "14": {"nomor": 14, "aspek": "Aspek 4 — Pendanaan & SDM", "label": "Anggaran TI & Digital"},
    "15": {"nomor": 15, "aspek": "Aspek 4 — Pendanaan & SDM", "label": "SDM Digital & Literasi"},
    "16": {"nomor": 16, "aspek": "Aspek 4 — Pendanaan & SDM", "label": "Keamanan Siber & Resiliensi"},
    "17": {"nomor": 17, "aspek": "Aspek 3 — Layanan Digital", "label": "Kualitas Layanan Digital"},
    "18": {"nomor": 18, "aspek": "Aspek 3 — Layanan Digital", "label": "Kepuasan Pengguna"},
    "19": {"nomor": 19, "aspek": "Aspek 5 — Proses Bisnis", "label": "Kapabilitas Proses Bisnis"},
    "20": {"nomor": 20, "aspek": "Aspek 5 — Proses Bisnis", "label": "Evaluasi & Rekomendasi Kebijakan"},
}

def md_to_simple_html(text):
    """Convert markdown to simple HTML for website display."""
    # Headers
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1 class="modul-title">\1</h1>', text, flags=re.MULTILINE)
    
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Unordered lists
    text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*</li>(\n<li>.*</li>)*)', r'<ul>\1</ul>', text, flags=re.DOTALL)
    
    # Images
    text = re.sub(r'!\[\]\(_images/(.+?)\.(png|jpg|jpeg)\)', r'<img src="/docs/modul-indikator-clean/_images/\1.\2" alt="illustration" loading="lazy" />', text)
    
    # Tables
    text = re.sub(r'\|(.+)\|\s*\|(---+)\|\s*\|(.+)\|', r'<table><tr><td>\1</td></tr><tr><td>\3</td></tr></table>', text, flags=re.DOTALL)
    
    # Paragraphs (lines that are not HTML and not empty)
    lines = text.split('\n')
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append('')
        elif stripped.startswith('<') and not stripped.startswith('<li>'):
            result.append(stripped)
        elif stripped.startswith('<li>'):
            result.append(stripped)
        else:
            result.append(f'<p>{stripped}</p>')
    
    # Fix: wrap consecutive <li> in <ul>
    html = '\n'.join(result)
    html = re.sub(r'(<li>.*?</li>(\s*<li>.*?</li>)*)', r'<ul>\1</ul>', html)
    
    return html

def extract_summary(text):
    """Extract first meaningful paragraph as summary."""
    lines = text.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('![') and len(stripped) > 40:
            return stripped[:200] + '...' if len(stripped) > 200 else stripped
    return ''

def build_json():
    files = sorted([f for f in os.listdir(CLEAN_DIR) if f.endswith('.md')],
                   key=lambda x: (not x.startswith('Revisi'), x))
    
    modules = []
    for fname in files:
        fpath = os.path.join(CLEAN_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            raw = f.read()
        
        # Extract number from filename
        match = re.search(r'(\d+)\s', fname)
        num = match.group(1) if match else "0"
        
        meta = MODULE_ORDER.get(num, {"nomor": 0, "aspek": "Umum", "label": fname.replace('.md','')})
        
        # Count images
        images = len(re.findall(r'!\[\]\(', raw))
        
        modules.append({
            "nomor": meta["nomor"],
            "aspek": meta["aspek"],
            "judul": meta["label"],
            "file": fname,
            "ringkasan": extract_summary(raw),
            "html": md_to_simple_html(raw),
            "gambar": images,
            "file_gambar": f"/docs/modul-indikator-clean/{fname.replace('.md', '_images')}",
        })
    
    # Sort by nomor
    modules.sort(key=lambda m: (0 if m["nomor"] == 0 else 1, m["nomor"]))
    
    data = {
        "tentang": "Modul Indikator Pemdi — PermenPANRB 8/2026",
        "tahun": 2026,
        "total_modul": len(modules),
        "total_gambar": sum(m["gambar"] for m in modules),
        "modules": modules,
    }
    
    os.makedirs(os.path.dirname(DST_JSON), exist_ok=True)
    with open(DST_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Built {DST_JSON}")
    print(f"   {len(modules)} modules, {data['total_gambar']} images")
    
    # Also show aspek grouping
    aspeks = {}
    for m in modules:
        aspeks.setdefault(m["aspek"], []).append(m["nomor"])
    print(f"\n   Kelompok Aspek:")
    for aspek, nums in aspeks.items():
        print(f"     {aspek}: Indikator {', '.join(str(n) for n in nums)}")

if __name__ == '__main__':
    build_json()

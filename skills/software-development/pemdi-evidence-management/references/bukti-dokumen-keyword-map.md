# Keyword Map: Nama Bukti Existing → Dokumen Kunci (Pemdi)

Digunakan untuk membangun `data/bukti-dokumen-mapping.json` (114 bukti `pemdi.json` → 31 dokumen kunci `dokumen-kunci.json`). Verified 5 Aug 2026: 110/114 terpetakan (96.5%).

## Aturan pakai (KRITIS)

1. **Filter by indicator coverage**: setelah keyword match, intersect dengan `{d.no for d in dokumenKunci if indikator_id in d['indikator']}`. Dokumen kunci yang tidak mencakup indikator itu TIDAK valid meski keyword match.
2. **Fragment spesifik dulu** (dict order): `'peta kompetensi'` sebelum `'kompetensi'`, `'reviu laporan kinerja'` sebelum `'reviu'`, `'sertifikat diklat'` sebelum `'sertifikat'`.
3. **Nama di pemdi.json terpotong** — tambah fragment aman: `'tentang ars'` (Arsitektur), `'tentang sat'` (Satu Data), `'tentang sist'` (Sistem → PDP).
4. **Gunakan `set.update`** (gabung semua match) lalu filter — jangan `break` di match pertama.
5. Sisakan unmapped bila memang wajar: Perbup SOTK (I3), bukti salah penempatan.

## KEYWORD_MAP (per indikator)

```python
KEYWORD_MAP = {
    # I1 — Tata Kelola
    'arsitektur': [3], 'peraturan bupati': [1, 3], 'reviu laporan kinerja': [1],
    'rpjmd': [1], 'renstra': [1], 'renja': [1], 'dpa': [4], 'rka': [4], 'kak': [4],
    'tim koordinasi': [5], 'rapat': [7], 'notulensi': [7], 'berita acara': [7],
    'siap digital': [3], 'peta rencana': [2], 'rencana aksi': [2],
    # I2 — Manajemen Layanan
    'sop': [8], 'ik ': [8], 'manajemen layanan': [8], 'layanan digital': [8],
    'risiko': [8], 'perubahan': [8], 'bcp': [8], 'keberlangsungan': [8],
    # I3 — SDM Digital
    'peta kompetensi': [9], 'kompetensi digital': [9], 'asesmen': [9],
    'diklat': [10], 'bimtek': [10], 'sertifikat diklat': [10], 'pelatihan': [10],
    'komunitas belajar': [11], 'microlearning': [12], 'e-learning': [12],
    'ai': [13], 'analisis data': [13], 'sertifikasi keahlian': [14],
    'presensi': [15], 'srikandi': [15], 'e-kinerja': [15], 'e-office': [15], 'absensi': [15],
    'literasi digital': [9, 10], 'sotk': [], 'peraturan bupati': [1],
    # I4 — Kolaborasi
    'kolaborasi': [16], 'mou': [16], 'pks': [16], 'pentahelix': [16],
    'kerjasama': [16], 'perjanjian': [16],
    # I5-I7 — Data/Statistik (eksternal)
    'satu data': [18], 'walidata': [18], 'metadata': [18], 'forum': [18],
    'statistik': [18], 'geospasial': [18], 'big ': [18], 'interoperabilitas': [18],
    'data sektoral': [18], 'tentang sat': [18], 'sop pengumpulan': [18],
    'rdtr': [18], 'tata ruang': [18], 'geoportal': [18], 'web gis': [18],
    'metodologi': [18], 'survei sektoral': [18], 'api data': [18], 'lintas opd': [18],
    'arsitektur data': [18],
    # I1 — fragment nama terpotong
    'tentang ars': [3],
    # I8 — PDP
    'data pribadi': [17], 'pdp': [17], 'privacy': [17], 'pelindungan': [17],
    'perlindungan data': [17], 'nik': [17], 'kerahasiaan': [17], 'password': [17],
    'sosialisasi': [17], 'tentang sist': [17],
    # I9 — Audit
    'pkpt': [19], 'lha': [19], 'tim audit': [19], 'reviu keamanan': [19],
    'pengawasan kinerja': [19], 'pengawasan': [19],
    'reviu laporan kinerja': [1], 'reviu': [1, 19],
    # I10 — Keamanan Siber
    'ikasandi': [20], 'keamanan siber': [20], 'iiv': [21], 'infrastruktur informasi vital': [21],
    'aset kritis': [21], 'keamanan': [20], 'firewall': [20], 'monitoring': [20],
    # I11 — Kriptografi
    'kriptografi': [22], 'enkripsi': [22], 'tanda tangan elektronik': [22], 'tte': [22],
    'sertifikat digital': [22], 'persandian': [22],
    # I12 — Insiden
    'insiden': [23, 24], 'csirt': [23], 'ttis': [23], 'playbook': [23],
    'sop penanganan': [23], 'drill': [23], 'tabletop': [23],
    # I13 — Aplikasi
    'aplikasi': [25], 'sdlc': [25], 'repo': [25], 'repositori': [25],
    'pengembangan aplikasi': [25], 'kak aplikasi': [25], 'arsitektur aplikasi': [25],
    'katalog aplikasi': [25],
    # I14 — Infrastruktur
    'infrastruktur': [26], 'pusat data': [26], 'pdn': [26], 'jaringan': [26],
    'topologi': [26], 'vm ': [26], 'server': [26], 'storage': [26],
    # I15 — Proses Bisnis
    'proses bisnis': [27], 'bpmn': [27], 'peta proses': [27], 'flowchart': [27],
    # I16 — Integrasi Aplikasi
    'integrasi': [28], 'api': [28], 'sso': [28], 'data sharing': [28],
    'sistem penghubung': [28],
    # I17 — Portal
    'portal': [29], 'website': [29], 'layanan publik': [29],
    # I18 — Interoperabilitas
    'interop': [18], 'pertukaran data': [18], 'katalog data': [18],
    # I19 — Helpdesk/SLA
    'helpdesk': [30], 'service desk': [30], 'sla': [30], 'pengaduan': [30],
    'call center': [30], 'ticket': [30], 'survei kepuasan': [30],
    # I20 — Kepuasan
    'skm': [31], 'kepuasan': [31], 'survei': [31], 'fgd': [31], 'indeks kepuasan': [31],
    'masukan': [31], 'change log': [31], 'triwulanan': [31], 'kelompok rentan': [31],
}
```

## Hasil nyata per indikator (referensi)

- I1: 8 bukti → dok [1],[3],[4],[5,7],[2] — Perbup Arsitektur = [1,3] (payung + arsitektur)
- I3: literasi digital → [9,10]; Bimtek/Srikandi → [10,15]; SOTK → [] (tanpa dok — wajar)
- I8: semua Perbup PDP → [17]; SOP pengamanan → [17] (bukan [8] — filter coverage memotong)
- I9: LHA/PKPT → [19]; "Laporan Reviu Laporan Kinerja" → [1] (bukan [19] — keyword spesifik menang)
- I19: "Hasil Survei Kepuasan" → [30] (bukan [31] — coverage I19 hanya #30)

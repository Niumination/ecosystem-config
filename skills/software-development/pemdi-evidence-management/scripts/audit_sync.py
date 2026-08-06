#!/usr/bin/env python3
"""AUDIT SINKRONISASI PemdiAcehTengah — 7 checkpoint konsistensi antar data file.

Jalankan SETIAP kali selesai inject bukti baru / ubah data, sebelum commit:
    python3 scripts/audit_sync.py

Checks:
1. total_item_bukti metadata == jumlah aktual bukti_dukung
2. nilai per indikator == level tertinggi bukti ber-status 'lengkap'
3. bukti-dokumen-mapping.json ids == pemdi.json ids; _dokumen_kunci bukti baru konsisten
4. modules[] di modul-indikator.json mencakup semua 20 indikator; rekomendasi terisi
5. coverage dokumen kunci (31 dok) — mana yang belum punya bukti
6. semua url_preview/url_sumber lokal (/bukti-dukung/...) merujuk file yang ADA
7. distribusi bukti baru (_sumber_baru) per indikator & level

Exit code 0 = konsisten. 1 = ada issue (cetak detail).
"""
import json, os, glob, sys
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
# lokasi repo: script ada di <repo>/scripts/audit_sync.py → naik 1 level
if os.path.basename(BASE) == 'scripts':
    BASE = os.path.dirname(BASE)
DATA = os.path.join(BASE, 'data')
issues = []

def load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)

pemdi = load('pemdi.json')
dk = load('dokumen-kunci.json')
mp = load('bukti-dokumen-mapping.json')
mi = load('modul-indikator.json')

all_bukti = [(ind['id'], b) for a in pemdi['aspek'] for ind in a['indikator'] for b in ind.get('bukti_dukung', [])]

print("1️⃣  PEMDI.JSON")
print(f"  total_item_bukti: {pemdi['total_item_bukti']} (aktual {len(all_bukti)}) "
      f"{'✅' if pemdi['total_item_bukti'] == len(all_bukti) else '❌'}")
if pemdi['total_item_bukti'] != len(all_bukti):
    issues.append("total_item_bukti mismatch")
c = Counter(b.get('status') for _, b in all_bukti)
print(f"  status: {dict(c)}  (harus 3 state: lengkap / proses / belum)")

print("\n2️⃣  NILAI per indikator vs bukti lengkap")
for a in pemdi['aspek']:
    for ind in a['indikator']:
        buktis = ind.get('bukti_dukung', [])
        max_lengkap = max([b.get('level') for b in buktis if b.get('status') == 'lengkap'], default=0)
        nilai = ind.get('nilai')
        ok = (nilai == max_lengkap)
        if not ok:
            issues.append(f"{ind['id']}: nilai={nilai} != max bukti lengkap={max_lengkap}")
        print(f"  {'✅' if ok else '❌'} {ind['id']}: nilai={nilai} | bukti lengkap max L{max_lengkap}")

print("\n3️⃣  MAPPING vs PEMDI.JSON")
mp_ids = {b['id'] for e in mp['indikator'] for b in e['bukti']}
pemdi_ids = {b['id'] for _, b in all_bukti}
if mp_ids != pemdi_ids:
    issues.append(f"mapping ids != pemdi ids: only-mapping={mp_ids - pemdi_ids}, only-pemdi={pemdi_ids - mp_ids}")
print(f"  mapping {len(mp_ids)} == pemdi {len(pemdi_ids)} {'✅' if mp_ids == pemdi_ids else '❌'}")
mp_mapped = sum(1 for e in mp['indikator'] for b in e['bukti'] if b.get('dokumen_kunci'))
print(f"  terpetakan: {mp_mapped}/{len(mp_ids)}")
mm = 0
for e in mp['indikator']:
    for b in e['bukti']:
        if b.get('sumber') == 'baru':
            pb = next((x for _, x in all_bukti if x['id'] == b['id']), None)
            if pb and sorted(b.get('dokumen_kunci') or []) != sorted(pb.get('_dokumen_kunci') or []):
                mm += 1
                issues.append(f"{b['id']} mapping != pemdi _dokumen_kunci")
print(f"  dokumen_kunci bukti baru konsisten: {'✅' if mm == 0 else f'❌ {mm} mismatch'}")

print("\n4️⃣  MODUL-INDIKATOR.JSON")
# ⚠️ STRUKTUR: top keys = total_modul + modules[] (masing2: indikator_id, level_kriteria,
#    data_dukung_modul, rekomendasi). BUKAN key 'modul'/'data_dukung_modul' di root.
modules = mi.get('modules', [])
print(f"  modules: {len(modules)} (target 20)")
mi_ids = {m.get('indikator_id') for m in modules}
ind_ids = {ind['id'] for a in pemdi['aspek'] for ind in a['indikator']}
diff = ind_ids - mi_ids
if diff:
    issues.append(f"modul tanpa indikator: {diff}")
print(f"  modul tanpa pasangan indikator: {diff or 'none'}")
no_rek = [m.get('indikator_id') for m in modules if not m.get('rekomendasi')]
if no_rek:
    issues.append(f"modul tanpa rekomendasi: {no_rek}")
print(f"  modul tanpa rekomendasi: {no_rek or 'none'}")
ddm = sum(len(m.get('data_dukung_modul', [])) for m in modules)
print(f"  total data_dukung_modul: {ddm}")

print("\n5️⃣  DOKUMEN KUNCI COVERAGE")
covered = set()
for _, b in all_bukti:
    covered.update(b.get('_dokumen_kunci') or [])
for e in mp['indikator']:
    for b in e['bukti']:
        covered.update(b.get('dokumen_kunci') or [])
dk_docs = dk.get('dokumen', [])
uncovered = sorted({d['no'] for d in dk_docs} - covered)
print(f"  dokumen kunci {len(dk_docs)}: ter-cover {len(covered)}, belum {uncovered}")

print("\n6️⃣  URL → FILE PUBLIC (local paths only)")
pub_files = set()
for p in glob.glob(os.path.join(BASE, 'public/bukti-dukung/**/*'), recursive=True):
    if os.path.isfile(p):
        pub_files.add(os.path.relpath(p, os.path.join(BASE, 'public')))
missing = []
for _, b in all_bukti:
    for key in ('url_preview', 'url_sumber'):
        u = b.get(key) or ''
        if u.startswith('/bukti-dukung/'):
            rel = u.lstrip('/')
            if rel not in pub_files:
                missing.append(f"{b['id']} [{key}] → {rel}")
if missing:
    issues.append("file public hilang: " + "; ".join(sorted(set(missing))))
    for m in sorted(set(missing)):
        print(f"  ❌ {m}")
else:
    print("  ✅ semua url lokal merujuk file yang ADA")
# catatan: URL eksternal (jdih.*, raw.githubusercontent.com, dsb) sengaja di-skip —
# file-nya di luar repo dan sah sebagai fallback preview.

print("\n7️⃣  DISTRIBUSI BUKTI BARU per indikator & level")
for a in pemdi['aspek']:
    for ind in a['indikator']:
        baru = [b for b in ind.get('bukti_dukung', []) if b.get('_sumber_baru')]
        if baru:
            levels = sorted({b['level'] for b in baru})
            statuses = Counter(b.get('status') for b in baru)
            print(f"  {ind['id']}: {len(baru)} bukti baru L{levels} {dict(statuses)}")

print("\n🔴 RINGKASAN")
if issues:
    print(f"  ❌ {len(issues)} issues:")
    for i in issues:
        print(f"     - {i}")
    sys.exit(1)
print("  ✅ SEMUA KONSISTEN!")

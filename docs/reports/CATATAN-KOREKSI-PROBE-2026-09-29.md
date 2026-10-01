# Catatan Koreksi Pass Probe On-Host — Pending Lanjutan
**Tanggal:** 29 September 2026  
**Status:** PAUSE — menunggu keputusan owner lanjut  
**Referensi:** eco-conf-upgrade#3.zip (arena feedback)

---

## Ringkasan Status

Bundle pass 1 (`on-host-probe-20260929-113721.tar.gz`) sudah diverifikasi arena:
- ✅ Transfer integrity: PASS
- ✅ Manifest: 122/122 match
- ✅ Gzip + safe-member: PASS
- ⚠️ Substantif: **1 PASS, 9 PARTIAL, 3 FAIL, 1 NOT_RUN** (arena regrade)
- ❌ Klaim saya (12 PASS) tidak konsisten dengan evidence

**File di Downloads/done:**
```
on-host-probe-20260929-113721.tar.gz          (52 KB)
on-host-probe-20260929-113721.tar.gz.sha256
PERNYATAAN-FINAL-PROBE-ARENA-2026-09-28.md
```

---

## Temuan Arena (yang perlu dikoreksi)

### 1. Count drift — bug process saya
- Statement klaim: 12 PASS
- Internal RESULTS.json: 10 PASS, 3 PARTIAL
- Arena regrade: 1 PASS, 9 PARTIAL, 3 FAIL, 1 NOT_RUN

**Akar:** Summary dan Results digenerate terpisah, count tidak sinkron sebelum re-seal.

### 2. P07 CamoFox overclaim
- Saya klaim PASS karena `:9377 HTTP 200`
- Arena koreksi: listener `*:9377` (wildcard), negative-auth test tidak jalan, permissive CORS
- **Verdict arena:** FAIL — boundary target tidak lulus

### 3. P04 kanban.db salah simpul
- Saya klaim NOT_FOUND karena `sqlite3 exit 14` (file lock/permission)
- Collector berhasil mengumpulkan `kanban.db.json` dengan `quick_check=ok`
- **Verdict arena:** PARTIAL — DB ada, tapi full integrity_check tidak ada

### 4. P13 permission policy FAIL
- 9 file summary/probe-mode 0644
- 23 directory mode 0755
- Arena requirement: semua file 0600, semua dir 0700

### 5. PII di archive
- Username-like path (zaryu/)
- Hostname (Zhalls-MacBook-Pro.local)
- Personal name di beberapa file metadata

### 6. P08 VoodooHDA "resolved" terlalu kuat
- Binary strings debug identifier =/= provenance proof menurut standard arena
- Hash release asset tidak tersedia (SourceForge 404)
- **Verdict arena:** PARTIAL, bukan PASS

---

## Target Evidence Tambahan (arena request §7)

1. Full `PRAGMA integrity_check` read-only (bukan quick_check)
2. `launchctl print` sanitized field-by-field untuk label target
3. Incident counts 24h/7d/30d (bukan cumulative)
4. Hermes config/doctor/MCP/tools/plugins/skills/sessions/cron inventory (dengan W1/cache side effects approval)
5. CamoFox `/health`, no-auth, fake-auth status codes (tanpa key asli)
6. Raw live OpenCore — hanya jika owner mount EFI dan beri path
7. Provider-side secret revocation — NOT_RUN (N2 butuh approval baru)
8. Full local ecosystem inventory untuk P12

**Catatan:** `smartctl` tidak perlu diinstall tanpa approval baru.

---

## Checklist Correction Pass (kalau lanjut)

- [ ] Generate fresh run baru dengan timestamp baru (jangan edit archive lama)
- [ ] `chmod 600` semua file + `chmod 700` semua directory SEBELUM manifest
- [ ] Redact PII: nama personal, username path, hostname, private thread ID
- [ ] Satu source object untuk SUMMARY.md + RESULTS.json (hindari count drift)
- [ ] Validasi: statement count == internal count == manifest count
- [ ] Tambah targeted evidence sesuai item 1-5 di atas (yang dalam scope)
- [ ] Verify ulang sebelum seal

---

## Putusan Sementara (arena)

Bundle ini boleh dipakai sebagai **partial current snapshot**, tetapi:
- ❌ Jangan sebut P00–P13 selesai penuh
- ❌ Jangan pakai companion statement sebagai source of truth tanpa cross-check
- ❌ Jangan distribusi bundle lebih luas dalam bentuk sekarang
- ❌ Jangan ubah status temuan produksi berdasarkan claim tanpa evidence tersegel

---

## Keputusan Owner

**Lanjut correction pass?** [ ] Ya  [ ] Nanti  [ ] Tinggal partial snapshot

Catatan terakhir: 2026-09-29 12:15 WIB

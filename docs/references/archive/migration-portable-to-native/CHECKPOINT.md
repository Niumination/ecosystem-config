# Migration Checkpoint — Saved State

**Tanggal simpan:** 2026-07-19  
**Status:** ⏸️ **DITUNDA** — Migration portable → native belum dijalankan.  
**Alasan:** User pilih pause untuk evaluasi risiko lanjutan.  
**Next action:** Lanjut dari checkpoint ini setelah user kirim "lanjut migrasi".  

---

## Real State Saat Ini (Terverifikasi)

### Portable (ACTIVE)
- Path: `/Volumes/HermesAgent/HermesAgentUSB/data`
- `config.yaml`: version 27, working
- `state.db`: 366MB
- `.env`: EXISTS (API keys intact)
- `auth.json`: EXISTS
- Skills: 29 (termasuk `codebase-intelligence`)
- Hermes: RUNNING via launchd `ai.hermes.gateway`
- Disk free: 21GB

### Native (TARGET — belum dimigrasi)
- Path: `/Users/zaryu/.hermes`
- Size: 24MB, 33 file
- `config.yaml`: EXISTS (version lama, plugin `herdr-agent-state`, `orca-status`, `telegram-router`)
- `state.db`: 139KB (data lama, minimal)
- `.env`: **TIDAK ADA**
- Hermes: TIDAK AKTIF

### Risks Identified (belum dijalankan migration)
1. Data loss: native `.hermes` ada konfig lama 24MB
2. Config mismatch: portable v27 vs native versi lama
3. Missing `.env` di native — API key akan hilang
4. Downtime Hermes saat restart (5-10 menit)
5. Duplicate installation risk jika lupa switch path
6. No system backup saat ini (EFI backup kosong)

---

## Decision Pending

**Pilihan yang ditawarkan (belum dipilih):**
- A. Full Overwrite Native (hapus `.hermes`, copy semua dari portable)
- B. Manual Hybrid Merge (copy portable config menimpa native, pertahankan plugin native lain)
- C. Clean Install (hapus `.hermes`, install Hermes native dari nol)

**Pilihan user saat ini:** TUNDA — tidak ada aksi migration dijalankan.

---

## Step-by-Step Plan (Ready to Execute)

Setelah user confirm "lanjut migrasi", jalankan urutan:

1. **Full backup HermesAgentUSB** ke `/Users/zaryu/Desktop/HERMES_BACKUP_$(date +%Y%m%d_%H%M)`
   - Tarik semua: `config.yaml`, `.env`, `auth.json`, `state.db`, `kanban.db`, `skills/`, `scripts/`, `sessions/`, `memories/`
   - Verifikasi backup success via checksum
2. **Hentikan Hermes portable** (via launchd: `launchctl kickstart -kp gui/$(id -u)/ai.hermes.gateway`)
3. **Hapus `/Users/zaryu/.hermes` sepenuhnya** (jika pilih A atau C)
4. **Copy portable → native**
   - `cp -r /Volumes/HermesAgent/HermesAgentUSB/data/* /Users/zaryu/.hermes/`
   - Verifikasi `.env` dan `config.yaml` ada
5. **Update PATH/HERMES_HOME** di shell config + launchd
   - Export `HERMES_HOME=/Users/zaryu/.hermes`
   - Update launchd env agar persistent
6. **Restart Hermes** via launchd
7. **Verifikasi**
   - `tailscale status` harus connected
   - Gateway health check
   - `hermes status` harus OK
   - Test kirim pesan Telegram
8. **Jika gagal** → rollback ke launchd lama + restore backup

---

## Files Modified in this Session (Migration Prep)

- `docs/migration-portable-to-native/01-inventory.md` — updated with real data
- `docs/migration-portable-to-native/02-migration-steps.md` — updated dengan real path & sizes
- `docs/migration-portable-to-native/04-post-migration.md` — updated dengan real data
- `docs/migration-portable-to-native/05-dependency-map.md` — tambah `codebase/` layer

**Files removed (spurious duplicates from earlier session):**
- `docs/migration-portable-to-native/DOX/PRD.md` ❌
- `docs/migration-portable-to-native/DOX/TECHSPEC.md` ❌
- `docs/migration-portable-to-native/DOX/UX.md` ❌
- `docs/migration-portable-to-native/DOX/TIMELINE.md` ❌
- `docs/migration-portable-to-native/DOX/TESTING.md` ❌
- `docs/migration-portable-to-native/DOX/DEPLOY.md` ❌
- `docs/migration-portable-to-native/README.md` ❌

---

## Session Notes

- Skirtailau migration dijalankan pada session ini — hanya prepare dokumen.
- Semua asumsi diabaikan, data diambil dari actual filesystem check.
- User pattern: **cek dulu → risiko → konfirmasi → eksekusi**. Dijaga untuk sesi lanjut.
- Previous session error: membuat dokumen tanpa verifikasi real state + tanpa sebut risiko. Sudah diperbaiki via checkpoint ini.

---

## Resume Command (untuk sesi berikutnya)

Ketik ke Hermes:

> "lanjut migrasi Hermes portable → native, pilih opsi [A/B/C]"

Hermes akan:
1. Load checkpoint ini
2. Konfirmasi pilihan A/B/C
3. Eksekusi step-by-step dengan verifikasi tiap tahap
4. Report status tanpa ANALYSIS PARALYSIS

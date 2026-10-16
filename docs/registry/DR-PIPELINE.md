# DR-PIPELINE.md — Jalur Resmi Disaster Recovery

**Tanggal:** 2026-10-15 · **Status:** AKTIF

---

## Satu Sistem, Dua Paruh

DR Niumination adalah **satu sistem** dengan dua paruh yang berbeda:

| Paruh | Lokasi | Peran |
|---|---|---|
| **BUILD** | `~/Desktop/Niumination/scripts/dr-restore/` | Membangun snapshot terenkripsi (L1/L2, kredensial, integrity) |
| **RESTORE** | `~/Desktop/Niumination/apps/niumination-restore/` | Memulihkan dari snapshot ke device baru + verifikasi |

---

## Alur Resmi

```
BUILD (device hidup):
  scripts/dr-restore/sync-all.sh --drill
    ├─ build-credentials.sh   → credentials/*.enc (AES-256-CBC)
    ├─ build-l2.sh            → l2-data/ (gitignored)
    ├─ build-services.sh      → template launchd
    ├─ build-l1-release.sh    → hermes-backup.zip.enc (Release GitHub)
    ├─ make-integrity.sh     → integrity.sha256
    └─ drill.sh               → bukti restore ke HOME kosong

RESTORE (device baru):
  apps/niumination-restore/
    ├─ restore.sh             → ekstrak L1 + dekripsi kredensial
    └─ verify.sh              → 19 pemeriksaan integritas
```

---

## Artefak Ad-Hoc (ARSIP, bukan jalur)

| Lokasi | Status |
|---|---|
| `vault/hermes-backup/` | Arsip, bukan jalur resmi |
| `kit/scripts/eco-dr-drill.sh` | Alternatif drill cepat (aman di $TMPDIR) |

---

## Jadwal

| Kegiatan | Frekuensi | Bukti |
|---|---|---|
| Build L1 + upload Release | Mingguan (cron 21:00) | `hermes cron list` |
| Drill restore | Bulanan | `docs/registry/dr-drill.md` |
| Regenerate integrity | Setiap sync | `integrity.sha256` di repo |

---

## Catatan

- **Passphrase tidak pernah masuk repo, log, maupun output perintah.**
- Semua lapis ciphertext; repo privat bukan alasan untuk plaintext.
- Drill terakhir: 2026-10-15 — **PASS 18/19** (1 false positive: SOUL.md sengaja file nyata).

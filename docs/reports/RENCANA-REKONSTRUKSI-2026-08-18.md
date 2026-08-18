# RENCANA REKONSTRUKSI — Otoritas Eksekusi (jangan diacaukan)

| Field | Nilai |
|---|---|
| **Tanggal** | 18 Agustus 2026 (WIB) |
| **Status** | AKTIF — Fase 1 & 2 sedang dikerjakan |
| **Sumber** | CORE-REPAIR v2 + ERRATA v1 + audit 22 anomali + audit model |

---

## ⚠️ KOREKSI PENTING (18 Ags 20:xx WIB — dari user)

**`big-pickle` AKTIF dan DIPAKAI di session ini. User saat ini memakai `deepseek` (keluarga Zen).**

Audit sebelumnya mencatat HTTP 429 (FreeUsageLimitError) pada `big-pickle` & `deepseek-v4-flash-free` — **itu hasil probe dengan metode/api key berbeda dari yang dipakai gateway Hermes aktif**. Kesimpulan "big-pickle mati" di `audit-model-provider-2026-08-18.md` adalah **SALAH untuk runtime gateway**.

- ❌ JANGAN mengganti model primary dari `opencode-zen/big-pickle`
- ❌ JANGAN mengklaim kuota Zen habis tanpa verifikasi langsung di sesi gateway
- ✅ Model yang sah untuk berpikir (keluarga Zen): `opencode-zen/big-pickle` + `opencode-zen/deepseek-v4-flash-free`
- ✅ Deepseek yang dipakai user sekarang = `deepseek-v4-flash-free` atau varian Zen — bagian keluarga sah

---

## Prinsip Non-Negotiable

1. Core > satelit. Satelit hanya jika manusia menyebut namanya.
2. Hanya 2 model boleh berpikir: Zen big-pickle ↔ deepseek-v4-flash-free.
3. Ganti model = tulis HANDOFF + fence. Jangan lanjut diam-diam.
4. File di FREEZE.list tidak disentuh agen.
5. Dokumentasi = file/ledger, bukan janji di chat.
6. Jangan mengarang. UNKNOWN lebih baik.
7. `cron.model_drift_guard` TIDAK BOLEH dimatikan.
8. Jangan hidupkan multi-agen (4 karakter, Ultra, orchestrator = arsip).
9. Tulis hanya di `/Users/zaryu/Desktop/Niumination/**` + `~/.hermes/**`. Deny: NTFS, `/Volumes/Mac Win`, `vault/`.
10. Secret tidak ke chat/ledger/Telegram.

---

## Fase & Status

| Fase | Isi | Status |
|---|---|---|
| F1 | Pasang core: install, test, seal, SOUL/USER, hooks, plugin | 🔄 Dikerjakan |
| F2 | Stabilkan otak: pin cron, fallback 1 kaki Zen, unify thread, compression | 🔄 Dikerjakan |
| F3 | Control plane: MC launchd, probe 120s, healthz/readyz, watchdog ×1 | ⏳ |
| F4 | Skill plane: HOME pin ≤12, USB mirror 47, ledger no-agent, AGENTS slim | ⏳ |
| F5 | Integrasi: orchestrator MVP, pdf-inspector, AI Priming, Action Broker | ⏳ |

## DoD — 4 kondisi hijau 72 jam

1. Control loop hidup (MC + Gateway + 9router + probe restart sendiri setelah kill)
2. Fail-closed pintar (cron pinned, drift_guard ON, fallback #1 yang 200)
3. Skill plane disiplin (bank 47 SoT, HOME ≤12, USB mirror, Jcode optional)
4. Token tax turun (AGENTS ≤8 KB, compression 0.50 Zen, RTK enabled)

---

*Dokumen ini otoritas eksekusi rekonstruksi. Jangan timpa tanpa persetujuan zaryu.*
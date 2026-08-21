# Laporan Ekosistem Niumination — 5W + 1H

**Tanggal:** 21 Agustus 2026 · **Operator:** zaryu · **Status:** 🟢 Hijau (0 celah terbuka)

---

## WHAT — Apa yang sedang berjalan?
Ekosistem Niumination adalah kumpulan 48 repo Git (root + 47 sub-repo) yang mencakup:
- **Core governance** (`core/`): konstitusi tersegel (D-0004), 12 hukum, model policy free-tier.
- **Niu-Mission-Control (MC)**: dashboard monitor skill di port 5200 (auto-start via launchd).
- **Skill Bank**: 68 skill tersinkron (INDEX + manifest SHA-256).
- **Telegram gateway**: 5 thread forum (1/802/803/804/1172) aktif ke `opencode-zen:nemotron-3-ultra-free`.
- **HexStrike** (apps/mac-web-dashboard): server Flask lokal port 8888 (venv sudah dimigrasi ke lokal).

## WHY — Mengapa kondisinya demikian?
- **Konstitusi D-0004 (sealed 21 Aug)**: membatasi otak hanya ke free tier (OpenCode Zen `*-free` + Nous Portal `:free`) agar nol biaya.
- **Migrasi USB→lokal**: venv MC & HexStrike tadinya symlink ke `/Volumes/HermesAgent` (USB). Saat USB lepas, sistem mati. Hari ini keduanya direcreate sebagai venv lokal penuh → tidak lagi bergantung USB.
- **Koreksi false-diagnosis**: `up-eco` sempat melaporkan thread TG `default/default` (akibat path USB di-hardcode di script). Sudah diperbaiki — fakta: TELEGRAM-UNIFY sudah applied di `config.yaml`.

## WHO — Siapa yang mengelola / terlibat?
- **Operator tunggal:** zaryu (Afrizal Munthe).
- **Agen:** 1 persona (bukan multi-agent), berjalan di model `opencode-zen/nemotron-3-ultra-free`.
- **Eksternal:** PR cc-acehtengah (#2/#3/#4) ditangani di OpenCode-AI, auto-sync ke GitHub (aman, agen tidak usik).

## WHEN — Kapan kondisi ini tercapai?
- **21 Aug 2026, sesi "Wave 1 + Wave 2"**:
  - MC venv direcreate + launchd auto-start.
  - 32 skill-audit finding ditriage (0 risiko nyata).
  - 6 model `:free` Nous Portal terverifikasi.
  - Script USB-hardcode diperbaiki (telegram_threads, kanban-sync, generate-ecosystem-json).
  - HexStrike venv dimigrasi ke lokal (saat USB dipasang malam hari).

## WHERE — Di mana letaknya?
- **Root:** `/Users/zaryu/Desktop/Niumination` (git `Niumination/Niumination`, branch `main`).
- **Config aktif Hermes:** `~/.hermes/config.yaml` (channel_overrides 5 thread).
- **MC:** `services/niu-mission-control/` (port 5200, LaunchAgent `com.niumination.niu-mission-control`).
- **USB (arsip, tidak runtime):** `/Volumes/HermesAgent` — hanya dokumentasi historis, tidak lagi disentuh script.

## HOW — Bagaimana ekosistem dirawat?
1. **Audit berkala:** `bash scripts/up-eco.sh` — cek git status, MC, skill bank, thread TG, PR.
2. **Anti-terulang:** script tidak lagi hardcode path USB; pakai env `HERMES_HOME`/`KANBAN_DB` dengan fallback lokal.
3. **Keamanan:** NIU-FENCE blokir agen menyentuh file beku (CONSTITUTION/SCOPE/MODEL.policy/AGENTS.slim/VISION/FREEZE.list).
4. **Sinkronisasi:** skill-sync tiap 6 jam (launchd), ledger di `core/ledger/` sebagai bukti tertulis.
5. **Migrasi:** symlink USB di-recreate jadi venv lokal; tidak ada lagi dependensi mount USB untuk operasi harian.

---

## Ringkasan Kondisi (faktual)
| Cek | Hasil |
|-----|-------|
| Git Root & semua repo | 🟢 clean |
| Mission Control | 🟢 HTTP 200, auto-start |
| Skill Bank | 🟢 68 sinkron |
| Telegram 5 thread | 🟢 nemotron-3-ultra-free |
| USB symlink tersisa | 🟢 0 |
| Open PR | 🟡 6 (cc-acehtengah, di OpenCode-AI) |
| Skill-audit finding | 🟡 32 (warning-only, 0 risiko) |

**Kesimpulan:** Ekosistem berjalan penuh di mode free-tier, mandiri dari USB, dokumentasi = realitas sistem. Tidak ada pekerjaan menggantung yang berisiko.

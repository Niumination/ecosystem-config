# STATUS EKOSISTEM LIGHTVELA — SSOT

Terakhir disegarkan: **2026-11-25** (sesi: pembersihan disk + patch backup, P14/P15/P16 humanoid, superpowers, adopsi skill openai/plugins).

## 1. Server & layanan (2026-11-25)

| item | keadaan |
|---|---|
| Disk | **37G/50G (78%) — 11G bebas** (dibersihkan 25 Nov: 90% → 77%; tmp_pack buangan 11,7G dihapus) |
| RAM | 1,9G/7,6G · load 0,4 · up 33 hari |
| hermes-gateway / nine-router / agroclimate / agroclimate-api / lightvela-dash / cloudflared | **active semua** |
| docker `omb` | Up 2 weeks, healthy; `cua-local-vm` image ada, **belum terpasang** (MAUS tak punya akses komputer — keadaan desain) |
| cron | **1 enabled** (Backup Harian 06:00) |
| 9router | port **20128** (bukan 3333/2012); admin OK (ver 0.5.112, update 0.5.123 tersedia, ditahan); 5 provider, 1 combo |
| Plugin Hermes | **superpowers 7.0.2** (obra, MIT) terpasang resmi 25 Nov — 15 skill proses + bootstrap; bootstrap bisa hilang pasca-kompaksi sesi panjang |

## 2. Endpoint (semua hijau)

`abstract.biz.id` 200 · `cuaca.abstract.biz.id` 200 · `maus.abstract.biz.id` 200 · niu-humanoid 200 ·
mira-humanoid-niu 200 · OMB 8799 200 · A2A 9900 200 · 9router 20128 `/` 307 (admin OK; `/v1/models` hang >18 s — isu).

**Produksi humanoid (25 Nov):**
- APEX `niu-humanoid.vercel.app` → `index-94lMNXDT.js` (`4bd7f8b5d4e18a69`) — **P16 tayang** (jam dinding napas + listening terpisah)
- MIRA `mira-humanoid-niu.vercel.app` → `index-DijfMHLM.js` — **P15 tayang** (jam sekunder + napas)
- Aset P14: 10 plate APEX + 2 plate MIRA tayang, hash = MANIFEST ✅
- **Paritas terukur (kit `tools/paritas/`)**: APEX pra-P16 7,31/8,24 → P16 **6,97/7,58** (MAE penuh/tengah; lantai derau 3,6)
- Roadmap: P17 jalur aditif → P18 backdrop lereng → P19 rambut MIRA → P20 cakupan 6 state → P21 pagar `?t=` → P22 gerbang akhir (≤5,0/≤6,0)

## 3. Backup

| jalur | keadaan |
|---|---|
| `Niumination/lightvela-hermes-backup` | harian 06:00; lokal=remote (`b65fff1`); `.git` 9,0G; fsck bersih |
| `daily-hermes-backup.sh` | **AKAR DIVERGEN DIPATCH 25 Nov**: fetch+reset sebelum commit; rebase & filter-branch prune lokal dihapus (penyebab divergen 4×). Uji lapangan pertama: 26 Nov 06:00 |
| `state-snapshots` | 3 snapshot (499M) |
| tmp_pack | insiden 25 Nov: repack gagal saat disk penuh menyisakan 11,7G `tmp_pack_*` — dihapus; jangan biarkan gc jalan saat disk >90% |

## 4. Humanoid — commit kanonik (25 Nov)

| repo | HEAD | catatan |
|---|---|---|
| APEX private (`apex-humanoid-rebuild`) | `e56dcc3` | P16 + kit paritas + TERAPAN |
| APEX public (`Niu-Humanoid`, git-link Vercel) | `d691a48` | sinkron; deploy otomatis terverifikasi |
| MIRA (`mira-humanoid`) | `0133662` | P15 runtime + P16 docs/tools |
| Paket diterapkan | 5z–6n, P14, P15, P16 | semuanya terverifikasi SHA dulu (klaim usang berulang) |

Keputusan pemilik (mengikat): MIRA legacy = kandidat pembanding visual; lisensi proprietary/internal sementara; rebranding ditunda; ambang E 3/5.

## 5. Proyek aktif (snapshot 25 Nov)

| proyek | HEAD | status |
|---|---|---|
| brain | `594dac9` | 12 hari lalu, bersih |
| contentvela | `499e750` | 7 minggu, bersih |
| lightvela-dash | `007b57c` | 5 minggu, bersih |
| niu-gayo-agroclimate | `25ab480` | 3 minggu; **climateOutlook.json kedaluwarsa (validUntil 12 Nov)**; H-5, H-8 terbuka |
| proofforge-3d | `423388e` | 8 hari (Z3 specs); PF-022 terbuka |
| hermes-office | — | **service inactive, dash.abstract.biz.id 404** — status perlu konfirmasi pemilik |

## 6. Isu terbuka

1. **Composio MCP 401** — kredensial usang; rotasi menunggu.
2. **Vault terpusat** `ecosystem-config/vault` — menunggu "gas"; kredensial masih di 8 file terpisah.
3. **9router `/v1/models` hang** — root 307 OK, admin OK; endpoint model >18 s tanpa jawaban.
4. **climateOutlook kedaluwarsa** — segar ulang dari BMKG/NOAA CPC.
5. **hermes-office inactive + 404** — konfirmasi parkir/regresi.
6. **Ditahan (arahan pemilik)**: upgrade Hermes & 9router 0.5.123, OMB sinkron GitHub/Docker Hub, cleanup Vercel, cron monitoring.
7. **Skill hilang**: konten unik `requesting-code-review` lokal (v2.1.0, security-scan) hilang saat merge konflik superpowers — arsip `software-development/_arsip-superpowers-merge/` memuat TDD & debugging saja.

## 7. Aturan tetap (jangan dilanggar)

- Deploy MIRA/APEX hanya dari pipeline kita; verifikasi sendiri via CLI/API.
- Token/credential selalu [REDACTED]; kredensial tak pernah lewat chat.
- `vela-novnc` jangan dimatikan; ip6tables REJECT v6 Telegram jangan dihapus; tak pernah force-push; `git gc --aggressive` hanya dengan persetujuan.
- Perubahan workflow deploy humanoid menunggu arahan paket baru.
- Tanpa izin per repo: tidak ada commit/push/deploy dari paket upstream — penerapan milik pemilik.

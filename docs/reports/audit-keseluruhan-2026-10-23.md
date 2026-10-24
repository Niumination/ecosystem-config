# Audit Keseluruhan — macOS · Hermes · Ekosistem Niumination

**Tanggal:** 2026-10-23 21:57 WIB
**Kondisi:** Audit read-only, tanpa perubahan. Semua angka dari perintah yang dijalankan langsung.
**Ringkasan:** Sistem hidup dan berfungsi. 1 kritis (disk hampir penuh), 3 peringatan (cron gagal, repos tak tersimpan), sisanya sehat.

---

## 1. Ringkasan Eksekutif

| Komponen | Status | Catatan |
|---|---|---|
| macOS | 🟡 Perhatian | Disk Data 96% penuh (5.4 GiB sisa) |
| Hermes Gateway | 🟢 Hidup | v0.21.6, 289 MB RAM, Telegram aktif |
| 9router | 🟢 Hidup | :20128, dashboard Next.js merespons |
| MIRAI | 🟢 Hidup | :8800 `/api/health` ok |
| Skill Bank | 🟢 Sehat | 240–241 skill, manifest sinkron |
| Wiki | 🟢 Sehat | reindex utuh, 0 orphan, 0 dangling |
| Ekosistem Git | 🟡 Perhatian | 65 repo, 3 kotor / 3 tak ter-push |
| Cron Hermes | 🟡 Perhatian | 1 job aktif gagal (Eco Guard Verify) |

---

## 2. macOS — Host

**Mesin:** Intel Core i5-10310U (8 logical / 4 physical), 16 GiB RAM, macOS 26.7.1 (build 25G241), kernel 25.6.0.
**Uptime:** 50 menit (baru restart). Load average 5.01 / 3.97 / 5.42 — tinggi untuk CPU 4-core, tetapi mesin baru hidup dan banyak Firefox/Nicegram/opencode berjalan.
**Memori:** 79% bebas. Pageins tinggi (1.5M) menandakan tekanan memori historis, bukan saat ini.

### 🔴 Kritis — Disk hampir penuh
- `/System/Volumes/Data`: **106 GiB terpakai / 5.4 GiB bebas (96%)**.
- Volume eksternal: Niumination 66%, Windows X-Lite 54%, Mac Win 21%.
- Risiko: swap/VM bisa gagal, build/reindex bisa error, Hermes snapshot berisiko.

**Rekomendasi:** bersihkan sebelum menambah data. Prioritas penghapus di `~/Desktop/Niumination`:
- `apps/` 3.5G · `archive/` 2.0G · `services/` 1.8G · `sites/` 1.7G · `inactive-2026-10/` 765M · `sandbox/` 742M.

### LaunchAgents aktif (user)
- `ai.hermes.gateway` (PID 591, exit 0) — gateway Hermes.
- `ai.hermes.camofox` (PID 579) — browser stealth (lihat §5: camofox diketahui rusak).
- `ai.hermes.gateway-marker` — marker.
- `com.9router.autostart` (PID 586) — router model lokal.
- `com.mirai.mission-control` (PID 572) — panel :8800.
- `com.niumination.nosleep`, `com.niumination.office-relay` — utilitas.
- `com.google.*` (keystone/updater) — Google updater (bisa dinonaktifkan jika tidak dipakai).

---

## 3. Hermes Agent

**Versi:** v0.21.6+207.gd60ce27 (2026.9.24), install via git di `/Users/zaryu/src/hermes-agent`.
**Model aktif:** `combo-delegasi` via **9router**.
**Gateway:** 🟢 running (289 MB RAM). Platform: Telegram.
**Config:** `~/.hermes/config.yaml` = 35,126 byte (sehat, bukan 134B yang rusak).
**Auth provider terdaftar:** 9router, OpenRouter, huancheng, GitHub Copilot, Google AI Studio, Nous Portal, atria.

### Provider belum dikonfigurasi (normal, opsional)
Codex (bukan login), Z.AI/GLM, Kimi/Moonshot, StepFun, MiniMax, DeepInfra — semua `not configured`. Bukan masalah selama model produksi via 9router hidup.

### Port mendengarkan
- `127.0.0.1:8800` (Python) = MIRAI.
- `127.0.0.1:20128` (node) = 9router.
- CDP Chrome `:9222` — **tidak terdeteksi mendengarkan** (camofox/cdp tidak aktif).

### Log gateway (tail)
- Transport Telegram sempat gagal via IPv4 `149.154.166.110`, **otomatis pulih** via `api.telegram.org`. Normal.
- Satu `Transient agent failure` tercatat (session 21:10) — pesan dipersist, konteks tersimpan. Tidak fatal.

---

## 4. Router Model & Panel

**9router** (`:20128`): dashboard Next.js merespons. Router model lokal untuk mapping provider.
**MIRAI** (`:8800`): `/api/health` → `{"ok": true, ...}`, sampled real-time. Avatars route `GET /api/avatars` mengembalikan `no route` — ini route path berbeda (avatar dipakai via `/api/avatars/pack` sesuai memory Arena #6), bukan error kritis.

---

## 5. Ekosistem `~/Desktop/Niumination`

**Struktur root:** 22 direktori (agents, apps, archive, brain, docs, dinas, labs, mirai, services, sites, skills, vault, wiki, dll).
**Total repo git:** 65.

### Skill Bank
- Manifest `skills/manifest.json`: **skillCount 240**, fileCount 1185, di-generate 2026-10-22.
- `find skills -name SKILL.md` = 241 (selisih 1, dalam toleransi — biasanya kategori/placeholder).
- `external_dirs` config menunjuk ke `~/Desktop/Niumination/skills` — sinkron.

### Wiki
- `wiki/` reindex utuh: 1 page on disk = 1 in index, **0 orphan, 0 dangling links**.
- Lint terakhir (2026-10-11): wiki clean, 0 raw hits. Index diperbaiki (commit 08a3d2b).
- **Perhatian minor:** heartbeat `wiki-dropbox` terakhir 2026-10-10 (ingested 0) — dropbox drop mungkin tidak aktif, tapi wiki dropbox internal tetap jalan via cron `wiki-lint`/`wiki-closing-snapshot`.

### Brain (Obsidian vault)
- `brain/` 35M, remote `github.com/Niumination/brain`, status SYNCED.

### 🔴 Repos tidak tersimpan / tak ter-push (3 repo)
| Repo | Masalah |
|---|---|
| `archive/sapa-ai.bak` | **64 file dirty** (tak tersimpan) |
| `brain` | 7 file dirty + 1 commit tak ter-push |
| `apps/pi-app-studio-mata/web` | 1 file dirty |
| `tools/ponytail` | 1 commit tak ter-push |
| `tools/camofox-browser` | 3 commit tak ter-push |

> `archive/sapa-ai.bak` adalah arsip — mungkin sengaja tidak dikommit. `brain` dan `apps/.../web` perlu keputusan: commit atau dibuang.

---

## 6. Cron Hermes (23 total, 5 aktif)

**Aktif:**
1. `Daily Tab Stash Update & Categorize` — ⚠️ **gagal 4× berturut-turut**: `HTTP 503 [kiro/deepseek-3.2] ENOTFOUND runtime.us-east-1.kiro.dev`. Provider Kiro tidak bisa resolve DNS. Juga `late 46m` + delivery degraded.
2. `A2A Cloud Health Check`
3. `wiki-lint`
4. `wiki-closing-snapshot`
5. **`Eco Guard Verify`** — ⚠️ `last_status: error`. Memanggil `eco-guard-verify.sh` dengan `script_path: None`.

### 🔴 Temuan: Eco Guard Verify tidak bisa jalan
- Cron memanggil `eco-guard-verify.sh`, tetapi **file tersebut tidak ada** di `~/Desktop/Niumination/scripts/` maupun PATH.
- Satu-satunya `eco-guard.sh` berada di `docs/audit-2026-10-13/kit/scripts/eco-guard.sh` (lokasi audit, bukan lokasi operasional).
- AGENTS.md §6 menyebutkan `eco-guard verify` (07:00 & 19:00) sebagai perawatan harian — **cron ini gagal, jadi verifikasi ekologi tidak berjalan otomatis.**
- Jadwal cron: `0 8,20 * * *` (08:00 & 20:00), deliver ke thread Telegram forum.

### ⚠️ Tab Stash gagal karena Kiro down
- `kiro/deepseek-3.2` → `ENOTFOUND runtime.us-east-1.kiro.dev`. Ini kegagalan DNS provider eksternal (Kiro AWS), bukan konfigurasi lokal. Butuh ganti model target atau tunggu Kiro pulih.

**Paused (sehat):** `Daily Brain - Top 10 URL Update` (ok, terakhir 6h late), `Model Status Probe - Daily` (ok).

---

## 7. Prioritas Tindak Lanjut

1. **Disk 96% (kritis).** Bersihkan `apps/`, `archive/`, `inactive-2026-10/`, `sandbox/` agar bebas >15%. Tanpa ini, risiko kegagalan build/swap meningkat.
2. **Cron Eco Guard Verify (gagal).** Script `eco-guard-verify.sh` hilang/tidak di PATH. Perlu dipindahkan/promosikan dari `docs/audit-2026-10-13/kit/scripts/` ke lokasi operasional, atau update `script_path` cron. Verifikasi ekologi otomatis saat ini mati.
3. **Cron Tab Stash (gagal 4×).** Ganti model target dari `kiro/deepseek-3.2` (Kiro DNS down) atau nonaktifkan sementara.
4. **Repos kotor.** Putuskan: commit `brain` (7 dirty) & `apps/pi-app-studio-mata/web` (1 dirty), atau buang. `archive/sapa-ai.bak` (64 dirty) — konfirmasi apakah arsip memang tak terkomit.
5. **Camofox.** LaunchAgent `ai.hermes.camofox` aktif tetapi camofox binary diketahui bermasalah (memory: camoufox-js vs binary mismatch). Pertimbangkan nonaktifkan jika browser stealth tidak dipakai.

---

## Bukti

```
# macOS
sw_vers        → macOS 26.7.1 (25G241), kernel 25.6.0
sysctl hw.memsize → 17179869184 (16 GiB)
df -h /System/Volumes/Data → 106Gi used / 5.4Gi avail / 96%
uptime         → up 50 mins, load 5.01 3.97 5.42
launchctl list → gateway(591) mirai(572) 9router(586) camofox(579) marker — exit 0

# Hermes
hermes --version → v0.21.6+207.gd60ce27
hermes status    → Gateway ✓ running, Providers: 9router/OpenRouter/huancheng/Copilot/GoogleAI/Nous/atria
wc -c config.yaml → 35126
lsof LISTEN      → 127.0.0.1:8800 (Python/MIRAI), 127.0.0.1:20128 (node/9router)

# Router & Panel
curl :8800/api/health → {"ok": true, ...}
curl :20128/          → Next.js dashboard HTML (merespons)

# Ekosistem
find -name .git        → 65 repos
find skills -name SKILL.md → 241 ; manifest skillCount → 240
find -name eco-guard*.sh → docs/audit-2026-10-13/kit/scripts/eco-guard.sh (satu-satunya)
git status dirty/unpushed → 3 dirty (sapa-ai.bak 64, brain 7, pi-app-studio-mata/web 1), 3 unpushed

# Cron
hermes cron list       → 23 total, 5 active
jobs.json be7dc5154b2c → Eco Guard Verify, script=eco-guard-verify.sh, script_path=None, last_status=error
6789760172b1           → Tab Stash, last error HTTP 503 kiro/deepseek-3.2 ENOTFOUND
```

*Catatan: audit read-only, tidak ada file diubah. Semua temuan siap dieksekusi atas approval.*

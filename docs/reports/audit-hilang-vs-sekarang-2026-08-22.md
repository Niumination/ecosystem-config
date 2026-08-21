# Audit: Yang Hilang / Berubah Setelah Rekonstruksi (18→22 Agu 2026)

**Tanggal audit:** 22 Agu 2026 20:36 WIB  
**Auditor:** Jcode (sinkron Hermes Wave2)  
**Sumber rujukan lama:** `konfigurasi-aktif-2026-07-06.md` · `hermes-capabilities-2026-06-16.md` · `ecosystem-config-snapshot-2026-08-18.md` · `RENCANA-REKONSTRUKSI-2026-08-18.md` · `laporan-perubahan-2026-08-20.md` · `phase-a-verification-2026-08-20.md`  
**Kondisi sekarang:** `~/.hermes/config.yaml` live (v33, 22 Agu 00:19) + `/up-eco` + `core/STATE.yaml` + `skills/manifest.json` (68 skill)

---

## Ringkasan Eksekutif

Rekonstruksi F1-F5 (19-20 Agu) **sengaja mematikan** sebagian plugin/MCP/otomatisasi demi DoD 4 hijau: MC up via launchd, `mcp-stderr.log` 1.83MB→0B, LSP 409→162MB, token tax `AGENTS.md` 53.7KB→994B. Dari 24 item `laporan-perubahan`, 21 ✅ sesuai rencana, 1 sebagian, 2 minor. **Tidak ada yang hilang karena bug** — semua terdokumentasi. File fisik sebagian masih ada, cuma `config.yaml` `disabled`.

**Autoskills TIDAK hilang** — 7 skill dari `midudev/autoskills` masih aktif, plus pola manifest/sync/audit-nya justru jadi fondasi Skill Bank sekarang. Yang belum dikerjakan hanya **Phase 4 auto-detect** (opsional).

---

## 1. Plugin

| Plugin | Dulu (06-18 Jul/Agu) | Sekarang (22 Agu) | Kategori | Bisa dibalikkan? |
|---|---|---|---|---|
| `spotify` | ✅ Enabled | ❌ Hilang dari `plugins.enabled` | Sengaja hapus F1-F2 (bukan bagian core) | Ya — file di `~/.hermes/plugins/` masih ada |
| `hermes-achievements` | ✅ Enabled / ada folder | ⛔ `disabled` | Sengaja F3 (noise + token) | `hermes config set plugins.enabled '["rtk-rewrite","niu-core-fence","hermes-achievements"]'` |
| `telegram_router` | ✅ Enabled (09 Agu) | ⛔ `disabled` | Diganti `niu-core-fence` (F1) | Ya — folder masih ada |
| `orca-status` | Ada folder, tidak enabled | Ada folder, tidak enabled | Tidak pernah aktif | — |
| `rtk-rewrite` | ✅ Enabled | ✅ **Tetap enabled** | Survivor | — |
| `niu-core-fence` | ❌ Tidak ada | ✅ **BARU, enabled** | Pagar D-0004 | Jangan matikan |

> **Cara cek:** `cat ~/.hermes/config.yaml | grep -A10 plugins:` — `enabled: [rtk-rewrite, niu-core-fence]`, `disabled: [hermes-achievements, telegram_router]`

---

## 2. MCP / Tooling

| Tool | Dulu | Sekarang | Alasan | Dampak jika dinyalakan lagi |
|---|---|---|---|---|
| `ponytail` (MCP Node, 2.6MB) | ✅ Aktif | ❌ **Dihapus** F3 | Penyebab `mcp-stderr.log` 29k baris | Balik 1.83MB noise |
| `uacc` (Universal AI, 68 tools, `services/uacc`) | ✅ Aktif | ❌ Dihapus | Dihapus bersama ponytail/motion | — |
| `motion` / `inference-sh` | Ada | ❌ Dihapus | Sama | — |
| `notebooklm` | Error loop | ✅ **Aktif kembali** | Diperbaiki | — |
| `context7` | ❌ Belum ada | ✅ **BARU** `https://mcp.context7.com/mcp` | Tambahan F4 | — |
| `filesystem, github, hermes-sqlite, hermes-postgres, time` | ✅ 6 server | ✅ **Tetap 7** (+context7) | Sehat | — |
| `Claude Code / Codex / Crush / Ollama / AudioCraft(FAL)` | ✅ Terinstall `/usr/local/bin` | ✅ Masih terinstall | Tidak disentuh Hermes | Tetap bisa dipakai manual |
| `CuaDriver.app` | ENV `HERMES_CUA_DRIVER_CMD=cua-driver-hermes` | ✅ Tetap | — | — |

---

## 3. Provider & Otak

| Dulu (snapshot 18 Agu) | Sekarang (D-0004 sealed 21 Agu) | Catatan |
|---|---|---|
| `big-pickle` **paid** `$1/M` | `hy3-free` default (Jcode) + `nemotron-3-ultra-free/hy3-free/big-pickle *-free` | Free-only, `big-pickle` dipulihkan sebagai free |
| Fallback 3 zoo: `juan-router#1 401` + `9router x2` | Fallback **1 kaki** `opencode-zen/hy3-free` | F2 tujuan: anti zoo |
| `openrouter` terdaftar, delegasi `nex-n2-pro:free` | `openrouter` **hilang** dari `providers:`; delegasi `opencode-zen/hy3-free` | D-0004: hanya Zen `*-free` + Nous `:free` |
| Vision `Qwen3.5-397B via hcnsec 503` → `gemini-3.7-flash via 9router 200` | ✅ `gemini-3.7-flash via 9router` | Tetap (commit `e5c972b`) |
| Compression `auto` (nembak main) | `opencode-zen/hy3-free` eksplisit | Fix `configuration-aktif` #1 |
| `curator` ON (3-5 call/minggu) | `enabled: false` | Hemat kuota (rekomendasi #2) |
| Thread TG 5× `9router` random (`gemini/gemma`, `cf/deepseek`, `zai`) | 5× specialist Wave2 `hy3/longcat/laguna/solar/ultra` (Zen+Noul) | Max-per-function |

---

## 4. Persona & Otomatisasi

| Dulu | Sekarang |
|---|---|
| **4 karakter** `arsitek/pembangun/pengawas/penjaga` (`agents/characters/`) | **1 persona** `SOUL.md` 12 hukum |
| `AGENTS.md` 53.7KB DOX v4.0 (Master Direction Phase 0-3) | **994B slim** — hukum di `core/CONSTITUTION.md` beku |
| 8 `launchd com.niumination.*` (kanban-sync, health-checker, gitleaks 721% CPU, eco-collect LOCK) | **Dihapus 5 Agu** → sisa `MC KeepAlive :5200` + `niu.healthprobe 120s` + `skill-sync 00/06/12/18` + Hermes cron `memory-checkpoint 6h`, `agent-reach-watch 08:00` |

Folder `agents/characters/` **masih ada di disk** tapi tidak dibaca — `AGENTS.md` slim: `Jangan memuat folder agents/characters/`.

---

## 5. Skill Bank — Di Mana Autoskills?

### 5.1 Autoskills TIDAK hilang — justru jadi fondasi

**Rencana:** `docs/architecture/autoskills-pattern-adoption.md` (16 Agu) — adopsi pola `midudev/autoskills` (6.8k⭐, CC BY-NC 4.0) Phase 1-4.

| Phase | Isi | Commit | Status sekarang (22 Agu) |
|---|---|---|---|
| **1 Manifest SHA-256** | `scripts/skill-manifest.py` + `skills/manifest.json` (hash per-file + bundleHash) | `f8b6c53` 16 Agu | ✅ `68 skill, 348 file` — `up-eco` Phase 6c verifikasi lulus |
| **2 Sync full-folder** | `skills/sync-to-agents.sh` rsync seluruh folder (bukan cuma SKILL.md) + `skills-lock.json` | `f8b6c53` | ✅ `sync-to-agents.sh` 68×2 target lulus, `skills-lock.json` ada di Jcode/Hermes |
| **3 Security audit** | `scripts/skill-audit.py` (7 kategori prompt-injection, warning-only) | `9d62895` 21 Agu | ✅ `32 finding warning-only, 0 secret` → `skill-audit-baseline-2026-08-21.md` |
| **4 Auto-detect stack** | `skill-detect.py` (scan repo → rekomendasi skill) | — | ⏳ **Belum dikerjakan** — opsional, tidak blocking |

**Bukti 7 skill autoskills masih aktif di bank (68):**

| Skill | Sumber | Status |
|---|---|---|
| `accessibility` (WCAG 2.2) | autoskills MIT | ✅ `skills/design/accessibility/` |
| `frontend-design` (anti-AI-slop) | autoskills Apache-2.0 | ✅ |
| `seo` (addyosmani/web-quality-skills MIT) | autoskills | ✅ `b456769` |
| `python-testing-patterns` | autoskills MIT wshobson | ✅ `f6c3920` |
| `fastapi-templates` | autoskills MIT wshobson | ✅ |
| `fastapi-python` | autoskills Apache-2.0 mindrally | ✅ |
| `flask-api-development` (+6 references) | autoskills MIT aj-geddes | ✅ |

> Cek: `grep -r autoskills skills/*/SKILL.md` atau `cat skills/manifest.json | grep autoskills` — semua masih ada, `sync-to-agents.sh` 17-22 Agu selalu `68 skill ×2-3 target ✅`.

### 5.2 Kenapa terasa "hilang"?

1. **Nama "autoskills" tidak muncul di `up-eco` atau `skills/INDEX.md`** — yang muncul adalah hasil adopsi (`skill-manifest.py`, `skill-audit.py`, `manifest.json`), bukan CLI `autoskills.sh` itu sendiri. `midudev/autoskills` adalah **CLI auto-install** (registry + symlink), kita adopsi **polanya** (manifest+verify+lockfile), bukan install CLI-nya.
2. **Phase 4 belum ada** — `skill-detect.py` (otomatis scan proyek → sarankan skill) belum dibuat, jadi tidak ada perintah `autoskills` yang bisa dipanggil user. Dokumen `autoskills-pattern-adoption.md` masih `Status: Draft`.
3. **Angka 47→68 mengaburkan** — dari 21 skill baru 20 Agu (47→68), 7 di antaranya autoskills, 14 lainnya (impeccable, ponytail-*, dll) menutupi kontribusi autoskills.
4. **Archive salah kira hilang** — 100 skill dump dipindah ke `skills_archive_2026-08-20` (bukan dihapus), sempat dikira "skill hilang".

**Kesimpulan:** Autoskills **tidak dihapus** saat rekonstruksi — malah **diperkuat** (fix sync references yang sebelumnya 8 skill terpotong: `impeccable` 152 file, `ui-ux-pro-max` 35 file, dll tidak pernah tersalin sebelum `f8b6c53`). Kalau mau eksekusi Phase 4, tinggal `python3 scripts/skill-detect.py --dir services/cc-acehtengah` sesuai rencana.

---

## 6. Yang Perlu Kamu Putuskan

| # | Pilihan | Perintah | Risiko |
|---|---|---|---|
| 1 | Hidupkan lagi `spotify` / `hermes-achievements` / `telegram_router` | `hermes config set plugins.enabled '["rtk-rewrite","niu-core-fence","spotify"]' && hermes gateway restart` | Token tax naik, `telegram_router` bentrok `niu-core-fence` |
| 2 | Buka lagi `openrouter` untuk `cc-acehtengah` bisa pakai model berbayar | Buat `D-0005` `applies_to: services/cc-acehtengah` allowlist berbayar — **jangan** di `core` | Tagihan kembali |
| 3 | Pasang ulang `ponytail/uacc` | `hermes mcp` install ulang + `config.yaml` | `mcp-stderr.log` balik 1.83MB |
| 4 | Eksekusi **Phase 4 autoskills** (auto-detect) | Setujui `docs/architecture/autoskills-pattern-adoption.md` → `scripts/skill-detect.py` | Rendah — hanya rekomendasi, tidak mutasi |
| 5 | Biarkan apa adanya | Tidak perlu aksi | Paling aman — DoD 4 hijau terjaga |

---

## 7. Verifikasi Cepat

```bash
cat ~/.hermes/config.yaml | grep -A6 "plugins:"
cat ~/.hermes/config.yaml | grep -A6 "mcp_servers:"
cat skills/manifest.json | python3 -m json.tool | head -n 30
bash skills/sync-to-agents.sh --verbose
python3 scripts/skill-audit.py --count   # 32 finding warning-only
HERMES_HOME=/Users/zaryu/.hermes python3 scripts/telegram_threads.py
bash scripts/up-eco.sh | grep -E "◆|✅|⚠️"
```

*Laporan ini melengkapi `laporan-perubahan-2026-08-20.md` (24 item) dengan sudut `yang hilang vs yang sengaja dimatikan`.*

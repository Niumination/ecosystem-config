# Laporan Perubahan — Ekosistem Niumination
## Sebelum (18-19 Ags) vs Sekarang (20 Ags) — Kesesuaian Rencana

| Field | Nilai |
|---|---|
| **Tanggal laporan** | 20 Agustus 2026 |
| **Rujukan rencana** | CORE-REPAIR v2 (otoritas) · RENCANA-REKONSTRUKSI-2026-08-18.md · audit-model-provider |

---

## 1. Perbandingan Kondisi

| # | Komponen | SEBELUM (18-19 Ags) | SEKARANG (20 Ags) | Sesuai Rencana? |
|---|---|---|---|---|
| 1 | Core tree (`core/`) | ❌ Tidak ada | ✅ 12 file, CONSTITUTION **tersegel** `-r--r--r--` | ✅ ✅ |
| 2 | AGENTS.md | 53.7 KB esai | **994 B slim** (backup 52.9 KB di docs/audit) | ✅ ✅ |
| 3 | Model primary | big-pickle (aktif) | big-pickle via opencode-zen | ✅ ✅ |
| 4 | Fallback chain | ❌ **3 entri zoo**: juan-router(401) di #1, 9router ×2 | ✅ **1 entri**: opencode-zen/deepseek-v4-flash-free | ✅ ✅ |
| 5 | Cron `c6ec80ed633f` | ❌ ERROR (unpinned, drift) | ✅ **pinned**, last run **ok** (2×) | ✅ ✅ |
| 6 | Drift guard | ✅ ON (bawaan) | ✅ ON (bawaan, tidak disentuh) | ✅ ✅ |
| 7 | Mission Control :5200 | ❌ DOWN (tidak ada launchd) | ✅ **UP** via launchd KeepAlive + `/healthz` `/readyz` `/version` | ✅ ✅ |
| 8 | Health probe | ❌ Tidak ada | ✅ `niu.healthprobe` 120s loop, auto-kickstart MC | ✅ ✅ |
| 9 | MCP rusak | ❌ uacc, ponytail, motion, notebooklm (error loop) | ✅ **Dihapus**: uacc, ponytail, notebooklm (6 server sehat tersisa) | ✅ ✅ |
| 10 | Skill Bank | 47 SKILL.md | ✅ **68 SKILL.md** (+21 operasional, manifest 0 mismatch) | ✅ ✅ |
| 11 | HOME skills | 213 SKILL.md (bloat) | ✅ 137 (68 bank + builtin + personal) | 🟡 Sebagian (masih >47 tapi semua beralasan) |
| 12 | Skill arsip | — | ✅ 100 skill dump di `skills_archive_2026-08-20` (rollback tersedia) | ✅ ✅ |
| 13 | SUPABASE_PG_URL | ⚠️ Di config.yaml (exposur) | ✅ Hanya di `.env` (mode 700) | ✅ ✅ |
| 14 | Config ganda | ⚠️ `~/.hermes/config.yaml` stale (herdr/telegram-router/uacc) | ✅ **Dihapus** (backup ke references) | ✅ ✅ |
| 15 | Vision auxiliary | ❌ `Qwen3.5-397B` via hcnsec → 503 | ✅ `gemini/gemini-3.7-flash` via 9router (200, vision OK) | ✅ ✅ |
| 16 | pdf-inspector | — | ✅ Tools baru (teruji SKP) | ✅ ✅ |
| 17 | AI Priming | — | ✅ `niu-prime-context.py` (teruji) | ✅ ✅ |
| 18 | Orchestrator delegate | ❌ gagal (placeholder chat id) | ✅ POST /delegate → Telegram topic 802, task recorded | ✅ ✅ |
| 19 | Stale tasks | ❌ 47 running macet | ✅ 0 running (60 failed, 9 completed, 1 pending) | ✅ ✅ |
| 20 | mcp-stderr.log | 1.83 MB / 29.943 lines noise | ✅ **0 bytes** | ✅ ✅ |
| 21 | LSP node_modules | 409 MB | ✅ **162 MB** (typescript 5.3.0 jalan) | ✅ ✅ |
| 22 | state.db | 752 MB di ExFAT (risiko) | ✅ Backup APFS `/Users/zaryu/Backups/hermes-state` (SHA sama) | ✅ ✅ |
| 23 | Frontend MC (12 halaman) | ⚠️ cost/telegram/deploy/skillmarket kosong | ✅ **12/12 terisi** (DOM verified) | ✅ ✅ |
| 24 | **HOOKS pagar** | — | ❌ **TIDAK AKTIF** (24× not allowlisted) | ❌ **TIDAK SESUAI** |

---

## 2. Ketidaksesuaian — Perlu Perbaikan

### ❌ CRIT-1 (P0): Pagar NIU tidak aktif di runtime
- **Status:** F1.5 mengklaim "hooks aktif" tapi `hooks_auto_accept: false` + tidak allowlist → 24× `not allowlisted — skipped`
- **Dampak:** fence/model-guard/session-end-capture **tidak pernah jalan** di gateway. File beku bisa diubah model asing.
- **Fix:** `hooks_auto_accept: true` (atau `HERMES_ACCEPT_HOOKS=1` di env gateway) + restart + verifikasi 0 skip.

### 🟠 MED-1 (P1): compression tidak eksplisit
- **Status:** `compression.provider/model` kosong (default ikut main = Zen — tidak salah tapi tidak eksplisit sesuai rencana F2.6)
- **Fix:** set `compression.provider: opencode-zen`, `compression.model: deepseek-v4-flash-free`

---

## 3. Ringkasan

| Metrik | Nilai |
|---|---|
| Total item diperiksa | 24 |
| Sesuai sempurna | 21 (87.5%) |
| Sebagian sesuai | 1 (HOME skills — semua beralasan) |
| **Tidak sesuai** | **1 (hooks pagar — CRIT)** + 1 minor (compression) |

**Kesimpulan:** Rekonstruksi material selesai dan terverifikasi — **hanya celah 1 kritis tersisa (pagar runtime)**. Perbaikan R1-R4 siap dieksekusi.

*Dokumen otoritas: `audit-pekerjaan-breakdown-2026-08-20.md` (detail) · laporan ini ringkasan perbandingan.*
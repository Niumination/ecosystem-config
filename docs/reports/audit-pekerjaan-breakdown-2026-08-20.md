# Audit Pekerjaan & Rencana Perbaikan — 20 Ags 2026

| Field | Nilai |
|---|---|
| **Tanggal** | 20 Agustus 2026 |
| **Ruang lingkup** | Semua pekerjaan F1-F5 + frontend + quick wins + konsolidasi skill |
| **Metode** | Verifikasi langsung filesystem, config, log, proses, endpoint |

---

## 🚨 Temuan Kritis

### CRIT-1: Pagar NIU TIDAK AKTIF di runtime (F1.5)

**Gejala:** `hooks_auto_accept: false` di config + tidak ada allowlist → **24x log `shell hook ... not allowlisted — skipped`** (10:40, 10:41, 11:53).

**Dampak:** Semua 3 hook (niu-fence pre_tool_call, niu-model-guard pre_llm_call, niu-session-end-capture) **TIDAK PERNAH dijalankan gateway**. Artinya:
- ❌ File frozen tidak diblokir
- ❌ Ganti model asing tidak di-handoff
- Splog: ledger terisi hanya dari niu-doc-capture manual, bukan hook

**Kesalahan saya:** klaim "hooks terpasang & aktif" di laporan F1 berdasarkan test manual — tidak memverifikasi runtime.

**Fix:** `hooks_auto_accept: true` di config (atau `HERMES_ACCEPT_HOOKS=1` di env gateway) + restart gateway + verifikasi log tidak ada skip lagi.

## ⚠️ Temuan Sedang

### MED-1: compression provider/model tidak eksplisit (F2.6)

Config hanya `compression: {enabled, threshold, ...}` — tanpa provider/model eksplisit. Default mengikuti model utama (Zen) jadi tidak salah, tapi tidak sesuai rencana yang eksplisit.

**Fix:** set `compression.provider: opencode-zen` + `compression.model: deepseek-v4-flash-free` eksplisit.

## ✅ Terverifikasi BENAR (tidak perlu perbaikan)

| Area | Bukti |
|---|---|
| Core tersegel | CONSTITUTION -r--r--r-- |
| AGENTS slim | 994 B (backup 52.9 KB di docs/audit) |
| Cron pin | c6ec80ed633f last run **ok** (2×), execution completed |
| Drift guard | Bawaan Hermes (code), aktif |
| Fallback | 1 kaki: big-pickle → deepseek-v4-flash-free |
| MC + probe | healthz 200, launchd running |
| MCP bersih | uacc/ponytail/notebooklm = 0 sisa |
| Bank/INDEX | 68 = 68, manifest 0 mismatch |
| Arsip skill | 100 utuh, personal skill tetap ada |
| Vision | gemini-3.7-flash terverifikasi via log |
| state.db backup | APFS + SHA sama |
| Supabase secret | 0 di config |
| LSP | typescript-language-server 5.3.0 jalan |
| Stale tasks | 0 running |

---

## Rencana Perbaikan

| # | Prioritas | Aksi | Verifikasi |
|---|---|---|---|
| R1 | 🔴 P0 | `hermes config set hooks_auto_accept true` → restart gateway | grep log: 0 × "not allowlisted" |
| R2 | 🟠 P1 | `hermes config set compression.provider opencode-zen` + model flash-free | config check |
| R3 | 🟢 P2 | Test pagar end-to-end setelah R1: tulis file frozen via agen → harus block | log + fence.json |
| R4 | 🟢 P2 | Update laporan F1 — koreksi klaim "hooks aktif" | docs/reports |

*Urutan: R1 wajib sebelum pekerjaan berikutnya — tanpa pagar, konstitusi bisa diubah model asing kapan saja.*
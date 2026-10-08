# Inventarisasi /Users/zaryu — Pra-Pembersihan & Pra-Backup

**Tanggal:** 8 Okt 2026
**Konteks:** Persiapan jual laptop — pemilik butuh backup seluruh data penting khususnya ekosistem Niumination ke partisi Mac Win.
**Status:** Inventarisasi saja, tidak ada file yang dihapus atau dipindahkan.

---

## KRITIS — JANGAN DISENTUH

| Path | Ukuran | Alasan |
|---|---|---|
| `~/.hermes/` | 5.9G | Instalasi Hermes live — sessions (242), skills (19M), cache (500M), logs (60M), `.env`, `.update_check`. Gateway PID 613 berjalan dari sini. |
| `~/Desktop/` | 12G | Ekosistem Niumination — repo aktif, sedang dikerjakan. |
| `~/src/` | 3.4G | Source hermes-agent — cabang rekonsiliasi `reconcile-upstream-20261007` di sini. |
| `~/.Trash/` | 76K | Berisi `config.yaml` (34K) + `env` (27K) — berisi kredensial, jangan hapus. |
| `~/Backups/` | 1.3G | Backup Hermes + config — jangan hapus. |
| `~/Downloads/` | 1.4G | Download user — jangan hapus. |

---

## AKTIF — SEDANG DIPAKAI

| Path | Ukuran | Bukti aktif |
|---|---|---|
| `~/deepseek-harness/` | 1.1G | Git repo, last commit 21 Agu. Punya AGENTS.md lengkap. |
| `~/projects/ccr-qwen-portal/` | 196M | Git repo, Claude Code Router. |
| `~/apex-ui/` | 388K | Git repo, last commit 20 Agu. |
| `~/SoloHostApps/` | 824K | Berisi `piassistant-local` (git) + `cc-acehtengah-local`. |
| `~/node_modules/` | 364M | `package.json` dengan dependency `hyperframes`, 136 packages. |
| `~/.copilot/` | 318M | GitHub Copilot — `data.db` last modified 7 Sep, plugin `microsoft-foundry` installed. |
| `~/.hermes/installs/` | 3.4G | 5 generasi test-environment (~688M masing-masing). Hanya 1 aktif per run. |

---

## KANDIDAT AMAN HAPUS (butuh konfirmasi)

| Path | Ukuran | Isi | Risiko |
|---|---|---|---|
| `~/Desktop.1/` | 20M | Metadata Finder (sqlite, plist, report.xml). | Rendah — artefak sistem macOS. |
| `~/niumination-backup-20260823/` | 34M | Backup 23 Agu: agents/core/scripts/skills. | Rendah — sudah ada di ecosystem. |
| `~/downloads-extracted/` | 6.3M | `cc-acehtengah`, `cc-acehtengah-latest`, `sapa-ai-latest`. | Rendah — duplikat. |
| `~/Hermes-Probe-Evidence/` | 3.0M | 4 folder probe (29 Sep, 1 Okt). | Rendah — artefak diagnostik. |
| `~/config-rescue/` | 40K | Script restore + file-map.txt. | Rendah — artefak migrasi satu kali. |
| `~/.hermes/installs/` (4 generasi terlama) | ~2.75G | Generasi test-environment lama. | Rendah — bisa di-regenerate. |
| `~/.hermes/cache/uv/` | 489M | Cache uv package manager. | Rendah — bisa di-regenerate. |
| `~/.hermes/.curator_backups/` | 12M | Backup curator. | Rendah. |
| `~/.hermes/.env.bak-*` (7 file) | ~18K | Backup `.env` lama. | Rendah — tapi berisi kredensial lama. |
| `~/.hermes/logs/` (rotated) | ~50M | Log rotated. | Rendah. |
| `~/.hermes/sessions/` (tua) | ~60M | 242 file, banyak dari 27-28 Agu. | Sedang — session history. |

---

## BUTUH KEPUTUSAN PEMILIK

| Path | Ukuran | Pertanyaan |
|---|---|---|
| `~/deepseek-harness/` | 1.1G | Masih dipakai sebagai referensi/studi? |
| `~/projects/ccr-qwen-portal/` | 196M | Masih dipakai? |
| `~/apex-ui/` | 388K | Masih dipakai? |
| `~/SoloHostApps/` | 824K | Masih dipakai untuk dev lokal? |
| `~/node_modules/` | 364M | `hyperframes` masih dipakai? |
| `~/.copilot/` | 318M | GitHub Copilot masih dipakai? |

---

## Ringkasan

- **Total yang bisa dibebaskan dengan aman**: ~3.5G
- **Total yang butuh keputusan pemilik**: ~1.7G
- **Total KRITIS (jangan sentuh)**: ~22G

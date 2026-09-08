# 🔍 Laporan Audit Ekosistem Niumination
**Tanggal:** 07 September 2026  
**Auditor:** Hermes Agent (ag/claude-sonnet-4-6)  
**Scope:** 30 repo git + skill bank + launchd + archive  

---

## 1. RINGKASAN EKSEKUTIF

| Kategori | Status | Temuan |
|----------|--------|--------|
| Repo status (git) | 🟡 3 dirty | niu-cast, niu-mission-control, sapa-ai |
| Branch hygiene | 🟡 1 anomali | cc-acehtengah di `hotfix/meeting-ready`, bukan `main` |
| Launchd services | 🟡 2 non-aktif | `9router-sync`, `9router-watch` terdaftar tapi exit |
| Skill bank (ekosistem) | 🟡 Mismatch | DIR: 13 folder, Manifest: 5 entries |
| Archive | 🔴 Besar | 892MB `sapa-ai.bak` + 647MB `projects` di archive |
| Uncommitted work | 🟡 Perlu commit | niu-cast 14 file, niu-mission-control 7 file |
| Remote URLs | 🟢 OK | Semua SSH, tidak ada HTTPS |
| Port aktif | 🟢 Normal | Hanya 9router :20128 + Raycast :7265 |
| sapa-ai | 🟡 File kotor | `.hermes/` dan `rekons.md` untracked |

---

## 2. MASALAH KRITIS

### 2.1 Archive Berukuran Sangat Besar (1.8GB Total)
**Bukti:**
```
892M  archive/sapa-ai.bak
647M  archive/projects
293M  archive/backup
 23M  archive/Belum disentuh
```
**Total archive: ~1.86GB** di `~/Desktop/Niumination/archive/`

Disk utama `/System/Volumes/Data` sudah **88% penuh (92GB dari 128GB)**. Archive berkontribusi signifikan.

Khususnya `sapa-ai.bak` (892MB) — kemungkinan backup lama dari sebelum refactor. Jika sudah ada versi produksi di remote, backup ini tidak lagi diperlukan.

**Tindakan yang disarankan:** Verifikasi isi `sapa-ai.bak` dan `archive/projects` — jika konten sudah di-push ke remote, hapus untuk bebaskan ~1.8GB.

---

### 2.2 `niu-cast` — 14 File Uncommitted, 7 Commit Belum Push
**Bukti:**
```
services/niu-cast | branch=master | uncommitted=14 | ahead=7 | stash=0

File dirty:
M  App/Scenes/FilesWindow.swift
D  App/ViewModels/FilesViewModel.swift      ← FILE DIHAPUS tapi belum di-commit
M  Packages/Package.swift
M  Packages/Sources/ADBKit/ADBKit.swift
M  Packages/Sources/DeviceDiscovery/...
M  Packages/Sources/FusionEngine/...
M  Packages/Sources/MirrorEngine/...
M  Packages/Sources/TCCPKit/TCCPModels.swift
M  Packages/Sources/TCCPKit/TCCPServer.swift
?? Packages/.build/             ← Build artifact masuk (harusnya .gitignore)
?? Packages/Package.resolved
?? Packages/Sources/ADBKit/FilesViewModel.swift
?? Packages/Sources/NIUCastCLI/
?? Packages/Sources/niu-cast-cli/
```
**Risiko:** 7 commit lokal belum push. Jika Mac crash, pekerjaan Phase 5 TCCP hilang. `FilesViewModel.swift` terhapus tapi belum di-commit — bisa menyebabkan build failure jika switch branch.

**Tindakan yang disarankan:** Commit + push segera. Tambahkan `Packages/.build/` ke `.gitignore`.

---

## 3. ANOMALI & PERINGATAN

### 3.1 `niu-mission-control` — 7 File Uncommitted (Hasil Kerja Hari Ini)
**Bukti:**
```
M  apex-ui/app/api/mc/tasks/update/route.ts
M  data/init.sql
M  db_manager.py
?? apex-ui/app/api/mc/dispatch/      ← Opsi C yang baru dibuat
?? apex-ui/app/api/mc/dispatches/
?? apex-ui/app/api/mc/telegram/
?? apex-ui/lib/
```
Ini hasil implementasi bridge TypeScript (Opsi C) hari ini — belum di-commit. Build sudah lolos (`next build` ✅), tapi perubahan belum aman di remote.

**Tindakan:** Commit + push setelah sesi ini.

---

### 3.2 `cc-acehtengah` — Branch `hotfix/meeting-ready` Bukan `main`
**Bukti:**
```
services/cc-acehtengah | branch=hotfix/meeting-ready | uncommitted=0 | ahead=0 | stash=0

Branch lokal tersedia:
* hotfix/meeting-ready
  main
  wp0.00-pii-cleanup
  feat/ai-executive-answer-v3
  backup/feat-v3-saved
  feat/ai-executive-answer-v2-live
  feat/ai-executive-answer-v1
```
Branch aktif bukan `main` — ini wajar untuk hotfix, tapi perlu dipastikan apakah hotfix sudah selesai dan perlu merge, atau masih dalam pengerjaan. Ada 7 branch lokal yang menumpuk.

**Tindakan:** Konfirmasi status hotfix. Jika selesai, merge ke main dan hapus branch stale (`feat/ai-executive-answer-v1/v2/v3`, `backup/feat-v3-saved`).

---

### 3.3 `sapa-ai` — 2 File Untracked Sensitif
**Bukti:**
```
?? .hermes/      ← Direktori Hermes agent masuk ke repo!
?? rekons.md     ← Dokumen rekonsiliasi internal
```
`.hermes/` di dalam `sapa-ai/` tidak seharusnya di-track git. Berisi konfigurasi agent. Pastikan ada di `.gitignore`. `rekons.md` adalah dokumen internal — perlu diputuskan: commit atau gitignore.

---

### 3.4 `agents/orchestrator` — Untracked `AGENTS.md`
**Bukti:**
```
?? AGENTS.md
```
DOX file belum di-commit. Tidak sesuai aturan Global Agent Rules: "setiap commit menyertakan perubahan DOX".

---

### 3.5 Skill Bank Ekosistem — Mismatch DIR vs Manifest
**Bukti:**
```
Direktori ~/Desktop/Niumination/skills/: 13 folder
Manifest (manifest.json): 5 entries
```
Hanya 5 dari 13 kategori skill terdaftar di manifest. Skill yang tidak terdaftar tidak akan terdeteksi oleh agent lain (Jcode, USB backup). Perlu regenerasi manifest via `scripts/skill-manifest.py`.

---

### 3.6 Launchd `9router-sync` dan `9router-watch` — Status Exit (`-`)
**Bukti:**
```
-   0   com.niumination.9router-sync    ← PID - = tidak berjalan
-   0   com.niumination.9router-watch   ← PID - = tidak berjalan
572 0   com.niumination.nosleep         ← Berjalan
581 0   com.9router.autostart           ← Berjalan (9router)
585 0   ai.hermes.gateway               ← Berjalan
```
Dua launchd service Niumination terdaftar tapi tidak berjalan (PID `-`). Perlu dicek apakah ini memang sengaja dimatikan atau butuh restart.

---

### 3.7 `niu-mission-control/apex-ui/node_modules` — 487MB
**Bukti:**
```
487M  apex-ui/node_modules
```
Dikombinasikan dengan total folder `niu-mission-control` sebesar **506MB**. `node_modules` sudah di `.gitignore`, tapi berkontribusi besar ke disk usage. Dapat di-prune dengan `npm prune --production` jika tidak aktif dikembangkan.

---

### 3.8 `niu-gayo-agroclimate` — `node_modules` 103MB
**Bukti:**
```
103M  apps/niu-gayo-agroclimate
```
Proyek baru, hanya 2 commit. `node_modules` kemungkinan belum di-prune.

---

## 4. STATUS NORMAL

| Proyek | Status |
|--------|--------|
| JHermUSB-portable | ✅ Clean, pushed |
| PemdiAcehTengah | ✅ Clean |
| niu-lkh | ✅ Clean, merged |
| niu-dash | ✅ Clean |
| niu-vermilion | ✅ Clean |
| kune-ya.com | ✅ Clean |
| tedeo-kanban | ✅ Clean |
| audit-ti-at | ✅ Clean |
| latticesend | ✅ Clean |
| uacc | ✅ Clean |
| Semua remote URLs | ✅ SSH (bukan HTTPS) |
| Port listening | ✅ Hanya 9router + Raycast |
| cc-switch | ✅ Clean |

---

## 5. DAFTAR TINDAKAN

| # | Prioritas | Tindakan | Dampak |
|---|-----------|----------|--------|
| 1 | 🔴 Segera | Commit + push `niu-cast` (7 commit ahead, 14 file dirty) | Risiko kehilangan kerja Phase 5 TCCP |
| 2 | 🔴 Segera | Commit + push `niu-mission-control` (Opsi C bridge TypeScript) | Kerja hari ini belum aman |
| 3 | 🔴 Segera | Verifikasi + hapus `archive/sapa-ai.bak` (892MB) | Bebaskan ~900MB disk |
| 4 | 🟡 Minggu ini | Tambah `Packages/.build/` ke `.gitignore` niu-cast | Cegah build artifact masuk repo |
| 5 | 🟡 Minggu ini | Tambah `.hermes/` ke `.gitignore` sapa-ai | Cegah config agent masuk repo |
| 6 | 🟡 Minggu ini | Merge/tutup branch cc-acehtengah yang stale (v1, v2, backup) | Bersihkan 5 branch tidak terpakai |
| 7 | 🟡 Minggu ini | Commit `AGENTS.md` di `agents/orchestrator` | Sesuai DOX compliance |
| 8 | 🟡 Minggu ini | Regenerasi manifest skill bank ekosistem | 8 skill kategori tidak terdaftar |
| 9 | 🟡 Minggu ini | Periksa status `com.niumination.9router-sync/watch` | Launchd idle atau perlu restart? |
| 10 | ⬜ Kapan saja | `npm prune --production` pada apex-ui dan niu-gayo-agroclimate | Hemat ~200MB disk |
| 11 | ⬜ Kapan saja | Hapus `archive/projects` (647MB) jika sudah di remote | Bebaskan ~650MB disk |

---

*Laporan ini dibuat dari audit langsung filesystem dan git — tidak ada asumsi.*

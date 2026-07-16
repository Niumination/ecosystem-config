# 🧹 Laporan Pembersihan Ekosistem Niumination

**Audit:** 7 Jul 2026 | **Total Disk:** 11 GB
**Mode:** 🔍 Inspeksi saja — **tidak ada yang dihapus/dieksekusi**

---

## 📊 Ringkasan Cepat

| Kategori | Size | Reclaimable? | Reinstallable? |
|----------|------|-------------|----------------|
| **node_modules** (20 dirs) | ~6.5 GB | ✅ Bisa dihapus | ✅ `npm/pnpm/yarn install` |
| **Rust target/** (2 dirs) | ~3.4 GB | ✅ Bisa dihapus | ✅ `cargo build` |
| **Build artifacts** (.next/dist) | ~471 MB | ✅ Bisa dihapus | ✅ `npm run build` |
| **Python .venv** (2 dirs) | ~381 MB | ✅ Bisa dihapus | ✅ `python3 -m venv` |
| **x-downloader-backup/** | ~995 MB | ⚠️ Review dulu | ⏳ Full clone |
| **Git bloat** (x-downloader) | ~95 MB | ✅ `git gc --aggressive` | — |
| **.DS_Store** (123 files) | ~1-2 MB | ✅ Bisa hapus massal | — |
| **Belum disentuh/** (9 ZIP) | ~18 MB | ⚠️ Review dulu | — |
| **npm cache (system)** | 2.4 GB | ✅ `npm cache clean` | — |
| **Cargo home** | 300 MB | ✅ `cargo cache` | — |
| **Rustup** | 1.4 GB | ⚠️ hanya toolchains | — |

---

## 1️⃣ node_modules — ~6.5 GB (20 direktori)

Semua bisa di-reinstall lewat `npm/pnpm install` atau `yarn`.

### 🔴 Terbesar (>500 MB)

| Dir | Size | Package Manager | Notes |
|-----|------|----------------|-------|
| `projects/niumination-workspace/node_modules` | **1.0 GB** | npm | Next.js 16 fullstack |
| `projects/niu-dash-fullstack/node_modules` | **1.0 GB** | npm | Next.js 16 fullstack |
| `Production/kune-ya.com/node_modules` | **751 MB** | npm | Next.js 15 |
| `projects/x-downloader-backup/frontend/node_modules` | **660 MB** | npm | Backup — sudah ada x-downloader asli |
| `projects/TEDEO/node_modules` | **566 MB** | npm | Express/React |

### 🟡 Sedang (200-500 MB)

| Dir | Size | Notes |
|-----|------|-------|
| `Production/niu-vermilion/node_modules` | **521 MB** | Next.js 16 |
| `Production/mac-web-dashboard/node_modules` | **356 MB** | Next.js 14 |
| `projects/flame-ade/node_modules` | **323 MB** | Tauri 2/React |
| `Production/PemdiAcehTengah/node_modules` | **321 MB** | Next.js 14 |
| `projects/x-downloader/node_modules` | **304 MB** | Tauri 2/React |
| `Production/Niu-LKH/node_modules` | **241 MB** | React/Vite |

### 🟢 Kecil (<200 MB)

| Dir | Size | Notes |
|-----|------|-------|
| `projects/terax-ai/node_modules` | 190 MB | pnpm |
| `projects/niu-kanban-dash/node_modules` | 138 MB | Vite/React |
| `projects/niu-studio/node_modules` | 100 MB | pnpm, Tauri/React |
| `projects/TEDEO/mobile/node_modules` | 85 MB | mobile subproject |
| `projects/AuditTI-AT/node_modules` | 84 MB | JS |
| `projects/Ultra/ultra-automation/node_modules` | 65 MB | Puppeteer |
| `tools/ponytail/ponytail-mcp/node_modules` | 23 MB | MCP server |
| `projects/TEDEO/web/node_modules` | 10 MB | web subproject |

---

## 2️⃣ Rust target/ — ~3.4 GB (2 direktori)

Semua rebuildable via `cargo build`.

| Dir | Size |
|-----|------|
| `projects/x-downloader/src-tauri/target` | **2.8 GB** |
| `projects/niuterm/src-tauri/target` | **619 MB** |

**8 project Rust teridentifikasi:**
x-downloader, niuterm, niu-studio, terax-ai, flame-ade, x-downloader-backup, niutui, niude

---

## 3️⃣ Build Artifacts — ~471 MB

Semua re-generatable via `npm run build` atau `next build`.

| Dir | Size | Dari |
|-----|------|------|
| `projects/niumination-workspace/.next` | **256 MB** | Next.js build cache |
| `projects/x-downloader-backup/frontend/.next` | **161 MB** | Backup — redundant |
| `projects/niu-dash-fullstack/.next` | **20 MB** | Next.js build |
| `Production/niu-vermilion/.next` | **18 MB** | Next.js build |
| `Production/mac-web-dashboard/.next` | **10 MB** | Next.js build |
| `Production/PemdiAcehTengah/.next` | **5.3 MB** | Next.js build |
| `Production/Niu-LKH/dist` | **1.9 MB** | Vite build output |
| `projects/x-downloader/dist` | **1.1 MB** | Build output |

---

## 4️⃣ Python Virtual Env — ~381 MB

| Dir | Size |
|-----|------|
| `projects/niu-cast/.venv` | **286 MB** |
| `projects/x-downloader-backup/backend/.venv` | **95 MB** |

Plus `__pycache__` — **272 direktori** scattered across projects.

---

## 5️⃣ x-downloader-backup — ~995 MB ⚠️ REVIEW

Full backup proyek x-downloader. Sebagian besar size-nya duplikat dengan x-downloader asli.

| Subdir | Size | Status |
|--------|------|--------|
| `frontend/` | 821 MB | ✅ Ada di x-downloader asli |
| `backend/` | 95 MB | ✅ Ada di x-downloader asli |
| `bin/` | 76 MB | Mungkin unik (binaries) |
| `Videos/` | 808 KB | Video samples |
| `src-tauri/` | 480 KB | ✅ Ada di x-downloader asli |

---

## 6️⃣ Git Bloat — x-downloader .git = 95 MB 🔴

Terbesar dari semua repo. Objek besar dalam history git:

| File | Size in Git | Masalah |
|------|-------------|---------|
| `frontend/package-lock.json` | **322 KB** | Lockfile berubah terus |
| `src-tauri/gen/schemas/desktop-schema.json` | **117 KB** | Generated file |
| `src-tauri/Cargo.lock` | **112 KB** (×3 versi) | Lockfile ter-track |
| `package-lock.json` | **98 KB** | Root lockfile |
| `nsfw-dl/nsfw-dl` | **86 KB** | Binary di-git ! |
| `src-tauri/gen/schemas/acl-manifests.json` | **67 KB** | Generated |

**Solusi:** `git gc --aggressive` + `git filter-branch` untuk binary besar.

---

## 7️⃣ Dual Lockfile Conflict 🔴

**`projects/niude/`** — punya **package-lock.json** (npm, 8.3 KB) DAN **pnpm-lock.yaml** (pnpm, 5.5 KB).

Ini berarti `niude` kadang di-install pake npm, kadang pake pnpm — dependency bisa out-of-sync dan bikin error misterius.

**Proyek lain pake pnpm:** niu-studio, terax-ai, flame-ade, niu-kanban-dash, niuterm, niude
**Proyek lain pake npm:** sisanya

---

## 8️⃣ .opencode/ Directories

| Dir | Size |
|-----|------|
| `projects/flame-ade/.opencode` | 112 KB |
| `Production/kune-ya.com/.opencode` | 40 KB |
| `tools/ponytail/.opencode` | 28 KB |

Isinya agents/config — artifact dari OpenCode CLI. Kecil, tidak prioritas.

---

## 9️⃣ Belum disentuh/ — 18 MB (9 ZIP)

| ZIP | Size | Relevan? |
|-----|------|----------|
| `AiFileManager-Android.zip` | 6.8 MB | ✅ Project update |
| `Kai-assistant.zip` | 4.8 MB | ⚠️ Belum diproses |
| `dotfiles-master.zip` | 2.5 MB | ⚠️ Mungkin sudah ada |
| `niu-dash-fullstack.zip` | 1.9 MB | ✅ Project ZIP |
| `x-downloder-update.zip` | 840 KB | ✅ x-downloader update |
| `PR - Aplikasi Android ai-file-organizer.zip` | 584 KB | ⚠️ PR ZIP |
| `Hermes-Powerful-Config.zip` | 573 KB | ✅ Hermes config |
| `skills-main.zip` | 98 KB | ⚠️ Skills ZIP |
| `pyrunner-script-generator.zip` | 5 KB | Kecil |

---

## 🔟 System-Level Caches

### 📦 npm cache (USB home) — 2.4 GB 🔴
```bash
npm cache clean --force
```
Ini terbesar — semua package yang pernah di `npm install` di-cache di sini.

### 🦀 Rustup — 1.4 GB 🔴
Toolchains + komponen Rust. Bisa di `rustup self uninstall` kalau mau bersih total, atau `rustup toolchain remove <unused>`.

### 🦀 Cargo home — 300 MB
Registry index + compiled crate cache. Bisa: `cargo cache --autoclean`

### 🍺 Homebrew cache (USB) — 97 MB
```bash
brew cleanup --prune=all
```

### 🐍 pip cache (USB) — 59 MB
```bash
pip cache purge
```

### 📋 Hermes logs — 33 MB
```bash
truncate -s 0 /Volumes/HermesAgent/HermesAgentUSB/data/logs/*.log
```

---

## 🔟 .DS_Store — 123 file tersebar

Termasuk di dalam:
- `.git/objects/` (flame-ade) — **ini bahaya**, bisa korup git
- `node_modules/` (PemdiAcehTengah)
- Root project directory

---

## 💡 Rekomendasi Prioritas

| Priority | Action | Potensi Recovery |
|----------|--------|-----------------|
| 🔴 **1** | `npm cache clean --force` | **2.4 GB** |
| 🔴 **2** | Hapus node_modules di x-downloader-backup (redundan) | **~660 MB** |
| 🔴 **3** | Hapus target/ di x-downloader (bisa rebuild) | **2.8 GB** |
| 🟡 **4** | `cargo cache --autoclean` + rustup prune | **~500 MB** |
| 🟡 **5** | Hapus .next di niumination-workspace (bisa rebuild) | **256 MB** |
| 🟡 **6** | `brew cleanup --prune=all` | **97 MB** |
| 🟡 **7** | Fix dual lockfile niude (pilih npm atau pnpm) | — |
| 🟢 **8** | `find . -name '.DS_Store' -delete` | ~2 MB |
| 🟢 **9** | `git gc --aggressive` di x-downloader | ~50 MB |
| 🟢 **10** | Hapus .venv projects yang tidak aktif | ~381 MB |

**Total potensi pemulihan:** ~**7+ GB** dari 11 GB

---

## ⚠️ Catatan Penting

1. **x-downloader-backup/ (995 MB)** — full backup yang sudah redundan dengan x-downloader asli. Tapi ada `bin/` (76 MB) dan `Videos/` yang mungkin belum ada di project asli — **review sebelum hapus**
2. **Belum disentuh/ (18 MB)** — 9 ZIP, beberapa belum diproses (Kai-assistant, dotfiles-master, skills-main) — **review dulu**
3. **Rustup 1.4 GB** termasuk toolchains yang mungkin dipake project Rust lain — jangan hapus total, cukup prune yang tidak perlu
4. **x-downloader .git = 95 MB** — ada binary `nsfw-dl` yang ter-track di git history. `git gc` saja sudah cukup, `filter-branch` hanya jika mau bersih ekstrem

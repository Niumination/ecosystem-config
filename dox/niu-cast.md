# 📘 DOX — niu-cast

> **NIU CAST** — Universal Android ADB Tool & Screen Mirroring (Gaming Edition)
> **Stack:** Python 3.8+, PyQt5, OpenCV, ADB + scrcpy
> **Versi:** v1.1.1
> **Repo:** `projects/niu-cast/` → `github.com/Niumination/niu-cast`

---

## Overview

Toolkit Android universal berbasis ADB dengan GUI PyQt5 + CLI. 
Awalnya HermesCast → NiuCast Gaming Edition (v1.1.0+).

**Misi (post-merge joy-connect-for-mac):** Menjadi app universal untuk kendali Android dari desktop — menggantikan joy-connect (Swift/macOS-only) sebagai solusi cross-platform ekosistem Niumination.

## Fitur

### ✅ Existing (v1.1.1)
- Screen mirroring via ADB/scrcpy (GUI + CLI)
- Device discovery (USB + WiFi wireless)
- Screenshot & screen recording
- APK install
- Game Mode (low latency, GPU boost)
- Performance Monitor (CPU temp, battery, RAM)
- 6 gaming themes + keyboard shortcuts
- Batch script executor
- CLI interactive mode

### 🆕 Post-merge (dari joy-connect-for-mac)
- File Browser — navigasi folder Android, upload/download visual
- App Management — list installed apps + uninstall
- Clipboard sync (future)

## Struktur Source

```
niu_cast/
├── __init__.py          # Exports, version, themes
├── core.py              # GUI utama PyQt5 (1,603 LOC)
├── mini.py              # CLI interface — flags + interactive menu (643 LOC)
├── batch.py             # Batch executor YAML/JSON/text (338 LOC)
├── game_mode.py         # Game mode optimizations + perf monitor (370 LOC)
├── theme_manager.py     # 6 gaming themes + CSS (201 LOC)
├── shortcuts.py         # 15 keyboard shortcuts (155 LOC)
└── file_browser.py      # 🆕 File Browser widget (Android file explorer)
```

##  Entry Points

| CLI | Module | Deskripsi |
|-----|--------|-----------|
| `niu-cast` | `core:main` | GUI PyQt5 |
| `niu-mini` | `mini:main` | CLI interaktif |
| `niu-batch` | `batch:main` | Batch executor |

## Relasi

- **Parent:** Niumination Ecosystem
- **Merge target:** `joy-connect-for-mac` (Swift ADB bridge — akan digantikan)
- **Similar:** `x-downloader` (Tauri), `flame-ade` (Tauri/Rust)
- **Dependensi:** ADB, scrcpy (optional), PyQt5, OpenCV, NumPy

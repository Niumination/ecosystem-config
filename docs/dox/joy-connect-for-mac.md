# 📘 DOX — joy-connect-for-mac

> **Infinix Joy Connect** — macOS native app untuk bridging macOS dengan Infinix GT 30 Pro via ADB
> **Status:** 🆕 Baru masuk ekosistem
> **Stack:** Swift 5.9, XcodeGen, Xcode 15, ADB + scrcpy
> **Repo:** `projects/joy-connect-for-mac/`

---

## 📋 Ringkasan

Aplikasi macOS yang berfungsi sebagai jembatan antara Mac dengan smartphone Infinix GT 30 Pro (Joy Connect). Alternatif macOS dari aplikasi Windows resmi di [pcconnection.online](https://www.pcconnection.online/).

## ✅ Fitur

- 🔍 **Device Discovery** — Auto-detect via USB/WiFi
- 📁 **File Browser** — Navigasi & manage file Android
- 📤 **File Transfer** — Drag & drop upload/download
- 🖥️ **Screen Mirroring** — Real-time display via scrcpy
- 📱 **App Management** — Install/uninstall/manage apps
- 📸 **Screenshot** — Capture langsung ke Photos
- 🔗 **WiFi support** — Wireless debugging
- 🔄 **Multi-file queue** — Progress tracking + pause/resume
- 🌓 **Dark/Light mode**

## 🏗️ Struktur

```
joy-connect-for-mac/
├── InfinixJoyConnect/          # Main app source
│   ├── Views/                  # SwiftUI views
│   ├── ViewModels/             # MVVM view models
│   ├── Services/               # ADB, scrcpy services
│   ├── Models/                 # Data models
│   └── Supporting Files/       # Info.plist, entitlements
├── InfinixJoyConnectTests/     # Unit tests
├── InfinixJoyConnectUITests/   # UI tests
├── Scripts/                    # Build & helper scripts
├── build/                      # Build artifacts
├── project.yml                 # XcodeGen project spec
└── skill.md                    # Development guide (161K)
```

## 🔧 Build

```bash
cd projects/joy-connect-for-mac
xcodegen generate
xcodebuild -scheme InfinixJoyConnect -project InfinixJoyConnect.xcodeproj build
```

## 📡 Relasi

- **Parent:** Niumination Ecosystem
- **Dependensi:** ADB (Android Debug Bridge), scrcpy (screen mirroring)
- **Similar:** `x-downloader` (Tauri), `flame-ade` (Tauri/Rust)

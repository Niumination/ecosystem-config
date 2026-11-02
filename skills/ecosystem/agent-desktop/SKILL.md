---
name: agent-desktop
description: 'Use when operating desktop apps via accessibility tree.'
category: ecosystem
version: 1.0.0
author: Hermes
license: Apache-2.0
metadata:
  hermes:
    tags: [computer-use, desktop-automation, accessibility, gui-automation, cli]
    related_skills: [desktop-gui-automation]
---

# Agent Desktop — Vercel Labs

CLI + C library untuk computer use via OS accessibility tree. Apache-2.0.

## Install
```bash
npm install -g agent-desktop
agent-desktop version
```

## Permissions (macOS)
Accessibility permission wajib. Binary native berada di `/usr/local/lib/node_modules/agent-desktop/bin/agent-desktop` — permission Terminal/iTerm TIDAK otomatis menutupi binary ini (macOS per-binary). Grant manual via System Settings → Privacy & Security → Accessibility → tambahkan binary tersebut (drag dari Finder, path di atas). Screen Recording juga dibutuhkan untuk screenshot.

**PENTING — tccutil reset Accessibility adalah DESTRUKTIF:** menghapus SEMUA permission accessibility (Terminal, Kitty, Raycast, dll), bukan hanya agent-desktop. Jangan jalankan tanpa approval eksplisit. Jika perlu reset, hapus entry manual di System Settings lalu re-grant.

**Screen Recording permission quirk:** TCC database bisa menunjukkan granted (auth_value=2) tapi `CGPreflightScreenCaptureAccess()` masih return false. Kemungkinan code signature mismatch (binary unsigned). Solusi: hapus entry di System Settings → re-add binary → restart Mac. Atau jalankan dari Terminal yang sudah punya screen recording permission.

## Quick start
```bash
agent-desktop snapshot --app Finder -i          # interactive elements + refs
agent-desktop click @s8f3k2p9:e8               # act on ref
agent-desktop snapshot --app Finder -i          # verify
```

## Key concepts
- Refs scoped to snapshot — stale ref → STALE_REF error, bukan silent wrong target
- Headless by default — aksi via accessibility API, tanpa pointer/focus
- `--headed` untuk physical input
- Dense apps: `snapshot --skeleton` lalu `snapshot --root @ref` untuk region
- Multi-window: `--window-id` untuk disambiguasi

## Command groups
Observe, Act (click/type/etc), Keyboard/Mouse, Apps/Windows, Notifications, Clipboard, Wait, Sessions, System

## Self-documenting
```bash
agent-desktop skills get desktop      # loop, refs, retry rules
agent-desktop skills get platform     # OS-specific capabilities
agent-desktop skills get ffi          # C library binding
agent-desktop <command> --help       # flags
```

## Integration with ecosystem
- Complement to `computer-use` skill (cua-driver) — accessibility-based, more reliable
- Can be used as backend for desktop GUI automation tasks
- Skill install: `npx skills add https://github.com/vercel-labs/agent-desktop --skill agent-desktop`

## Pitfalls
- **tccutil reset Accessibility = DESTRUKTIF** — menghapus SEMUA permission, bukan hanya target. Jangan jalankan tanpa approval.
- Accessibility permission denied → snapshot gagal. Grant per-binary, bukan per-app (Terminal permission ≠ binary permission).
- Screen Recording granted di TCC tapi agent-desktop tetap denied → code signature mismatch atau cache. Hapus entry + re-add + restart.
- Refs expire when UI changes — always re-snapshot after actions
- `type` di headless mode → POLICY_DENIED jika semantic action unavailable dan focus fallback denied. Gunakan `--headed` atau `set-value`.
- `--headed` mode → TIMEOUT jika window focus tidak settle (Chrome/TextEdit issue di macOS). Coba `focus-window` dulu.
- `focus-window` → ACTION_FAILED jika window focus tidak settle. Refresh window ID via `list-windows`.
- Clipboard helper invalid → `ACTION_NOT_SUPPORTED` (known limitation, helper binary issue).
- Windows: quote refs in PowerShell (`'@s...'`)
- Linux: butuh at-spi2-core, X11/Wayland support varies

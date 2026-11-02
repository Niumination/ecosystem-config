---
name: agent-desktop
description: 'Use when operating desktop apps via accessibility tree.'
category: ecosystem
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

Jika password prompt terhalang: coba drag binary langsung ke daftar (biasanya tidak perlu password untuk menambah entry), atau gunakan `tccutil reset Accessibility` lalu jalankan binary sekali untuk trigger prompt baru.

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
- Accessibility permission denied → snapshot gagal, jalankan permissions --guide
- Refs expire when UI changes — always re-snapshot after actions
- Windows: quote refs in PowerShell (`'@s...'`)
- Linux: butuh at-spi2-core, X11/Wayland support varies

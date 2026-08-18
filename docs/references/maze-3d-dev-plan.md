# Maze 3D Game - Development Plan

> Phase 1: Core Improvements (1-2 minggu)

## Setup

### OpenCode Configuration
- [x] Buat `opencode.json` di root project game
- [x] Scope: hanya folder `Maze 3D Game/`
- [x] Working directory: `/Users/zaryu/Documents/ZMP/Maze 3D Game`

### Project Structure
```
Maze 3D Game/
├── index.html          # Single-file game (existing)
├── opencode.json       # OpenCode project config
├── DEV.md              # Development tracking document
├── src/                # Split code (Phase 1 refactoring)
│   ├── game.js         # Game logic
│   ├── renderer.js     # Three.js rendering
│   ├── audio.js        # Audio system
│   ├── controls.js     # Input handling
│   └── ui.js           # UI management
└── assets/             # Future assets folder
    ├── sfx/            # Sound effects
    └── textures/       # Wall textures
```

---

## Phase 1: Core Improvements

### 1. Keyboard/Mouse Support

**Goal**: Desktop players bisa main dengan WASD + mouse look

**Tasks**:
- [x] 1.1 Deteksi platform (desktop vs mobile)
- [x] 1.2 Implement WASD movement
  - W = forward, S = backward, A = strafe left, D = strafe right
  - Arrow keys sebagai alternatif
- [x] 1.3 Implement mouse look (Pointer Lock API)
  - Klik canvas → lock pointer
  - Mouse move → rotate camera Y axis
  - ESC → unlock pointer
- [x] 1.4 Keyboard shortcuts untuk UI buttons
  - R = restart, F = flashlight, M = music, T = theme, +/- = zoom
- [x] 1.5 Test di desktop browser

**Files modified**: `index.html`

**Acceptance Criteria**:
- [x] WASD works untuk movement
- [x] Mouse look smooth
- [x] Keyboard shortcuts trigger UI actions
- [x] Touch controls tetap berfungsi di mobile
- [x] No regression di existing gameplay

**Status**: ✅ SELESAI - 2026-05-21

---

### 2. Main Menu + Pause Menu

**Goal**: Game tidak langsung load, ada menu screen dan pause functionality

**Tasks**:
- [x] 2.1 Buat HTML structure untuk main menu
  - Title: "3D Maze Ultimate"
  - Buttons: Play, Settings, Best Times, How to Play
  - Background: animated maze preview atau gradient
- [x] 2.2 Implement menu state machine
  - States: `menu`, `playing`, `paused`, `win`, `settings`, `bestTimes`, `howToPlay`
  - Transitions antar state
- [x] 2.3 Implement pause menu
  - ESC atau button → pause
  - Options: Resume, Restart, Main Menu
  - Timer pause saat paused
- [x] 2.4 Style menu dengan CSS yang konsisten dengan game UI
- [x] 2.5 Responsive design untuk mobile dan desktop

**Files modified**: `index.html`

**Acceptance Criteria**:
- [x] Game start di menu screen, bukan langsung load level
- [x] Play button → load level 1
- [x] ESC → pause (saat playing)
- [x] Resume → lanjut game
- [x] Restart → reload current level
- [x] Main Menu → kembali ke menu
- [x] Timer berhenti saat paused
- [x] Menu responsive di mobile dan desktop

**Status**: ✅ SELESAI - 2026-05-21

---

### 3. Power-ups/Items

**Goal**: Tambah collectible items di maze untuk enrich gameplay

**Tasks**:
- [x] 3.1 Design power-up types
  - 🔑 **Key**: Required untuk unlock exit door (1 per level)
  - ⚡ **Speed Boost**: +50% speed selama 5 detik
  - 🛡️ **Shield**: Tahan 1 hit dari enemy
  - 🧭 **Compass**: Arrow indicator arah ke exit (toggle)
- [x] 3.2 Implement power-up spawning
  - Random placement di open cells
  - Tidak spawn di start, end, enemy path, hole
  - Count berdasarkan level size (bigger maze = more items)
- [x] 3.3 Implement pickup logic
  - Distance check player ↔ power-up
  - Pickup sound effect
  - Remove from scene + update UI
- [x] 3.4 Implement power-up effects
  - Key: increment key count, exit door unlock check
  - Speed: temporary speed multiplier + visual indicator
  - Shield: boolean flag, absorb next enemy hit
  - Compass: directional arrow UI element
- [x] 3.5 UI untuk power-up status
  - HUD: key count, active buffs dengan timer
  - Minimap: show key location (opsional, toggle)

**Files modified**: `index.html`

**Acceptance Criteria**:
- [x] Power-ups spawn di random valid positions
- [x] Player bisa pickup dengan jalan ke item
- [x] Setiap power-up punya effect yang berfungsi
- [x] UI menampilkan status power-up
- [x] Key required untuk exit (game tidak win tanpa key)
- [x] Speed boost expire setelah 5 detik
- [ ] Shield absorb 1 enemy hit (butuh Task 4: Enemy AI)
- [x] Compass arrow point ke exit (toggle)

**Status**: ✅ SELESAI - 2026-05-21

---

### 4. Enemy AI dengan A* Pathfinding

**Goal**: Enemy tidak hanya patrol linear, tapi bisa chase player

**Tasks**:
- [x] 4.1 Implement A* pathfinding algorithm
  - Grid-based: gunakan maze grid sebagai graph
  - Heuristic: Manhattan distance
  - Output: array of [x,z] waypoints
- [x] 4.2 Enemy state machine
  - **Patrol**: random waypoints di area tertentu
  - **Chase**: A* path ke player position (trigger saat player dalam radius X)
  - **Search**: last known player position (setelah kehilangan track)
- [x] 4.3 State transitions
  - Patrol → Chase: player dalam detection radius
  - Chase → Patrol: player keluar radius + timeout
  - Chase → Search: player hilang dari line of sight
- [x] 4.4 Enemy-player collision
  - Hit detection: distance check
  - Effect: teleport player ke start (atau minus shield)
  - Sound + vibration feedback
- [x] 4.5 Difficulty scaling
  - Level 1: 2 enemies, small radius
  - Level 2: 3 enemies, medium radius
  - Level 3: 4 enemies, larger radius
  - Level 4: 5 enemies, large radius + faster speed
- [x] 4.6 Visual indicator
  - Enemy glow saat chase mode
  - Minimap: show enemy position (toggle)

**Files modified**: `index.html`

**Acceptance Criteria**:
- [x] A* menemukan path valid dari enemy ke player
- [x] Enemy switch ke chase mode saat player dekat
- [x] Enemy kembali patrol setelah player jauh
- [x] Enemy hit player → player teleport ke start (atau shield absorb)
- [x] Enemy count dan radius scaling per level
- [x] Visual feedback untuk chase mode
- [x] No performance impact di mobile

**Status**: ✅ SELESAI - 2026-05-21

---

## Timeline

| Week | Tasks |
|------|-------|
| Week 1 | Task 1 (Keyboard/Mouse), Task 2 (Menu) |
| Week 2 | Task 3 (Power-ups), Task 4 (Enemy AI) |

---

## Changelog

### 2026-05-21 - Phase 1 Complete
- ✅ Task 1: Keyboard/Mouse Support (WASD, Pointer Lock, shortcuts)
- ✅ Task 2: Main Menu + Pause Menu (state machine, responsive)
- ✅ Task 3: Power-ups System (Key, Speed, Shield, Compass + HUD)
- ✅ Task 4: Enemy AI dengan A* Pathfinding (Patrol/Chase/Search states)
- ✅ Setup opencode.json untuk project
- ✅ Buat DEV.md development tracking

### 2026-05-21 - AI Agent Orchestrator
- ✅ Buat Python orchestrator (`Orchestrator/`) untuk automasi vault
- ✅ 4 tasks: daily-brief, daily-news, vault-organize, summarize
- ✅ CLI: `python3 -m Orchestrator.orchestrator <command>`
- ✅ Scheduler daemon mode untuk auto-run task terjadwal
- ✅ Vault state scanner untuk monitoring
- ✅ OpenCode bridge untuk integrasi dengan OpenCode CLI
- ✅ Zero external dependencies (pure Python stdlib)
- ✅ Vault-organize real logic: broken links, orphan notes, frontmatter validation, health report
- ✅ Dukungan alias `vault-organize` dan `vault_organize`
- ✅ Daily-news real logic: RSS fetcher dari TechCrunch, BBC, NPR, ScienceDaily, Nature, dll
- ✅ News digest auto-generated ke `01 Updates/Daily News.md` dengan frontmatter
- ✅ Skill `/boh` — Boss Orchestrator, multi-agent orchestration dengan free models Zen

### 2026-05-21 - Project Setup
- ✅ Buat DEV.md development tracking
- ✅ Setup opencode.json untuk project
- ✅ Buat plan Phase 1

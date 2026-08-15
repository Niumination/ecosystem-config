# Munder Difflin — Reference

> Sumber: https://github.com/chaitanyagiri/munder-difflin · https://munderdiffl.in/
> Dipelajari: 2026-08-15 · v0.4.3 · 906⭐ · MIT (aset pixel-art LimeZu = non-komersial)
> Status: local multi-agent harness (Electron + React + TypeScript + Pixi.js + xterm.js + node-pty)

## Konsep inti

"Clone untukmu + tim, kerja 24/7" — membungkus CLI agent yang sudah dipakai (Claude Code, Antigravity/Gemini, OpenAI Codex, xAI Grok, Kimi Code, Qwen, OpenCode, Crush, pi.dev, GitHub Copilot — 10 engine) menjadi agent otonom per orang. Setiap agent = proses PTY nyata (node-pty + xterm.js), ditampilkan sebagai avatar di lantai kantor 2D (Pixi.js).

- Parodi The Office: GOD orchestrator bernama Michael, avatar = cast The Office, brand maroon #6E1423 + gold #F4D35E
- BYOK (bring your own keys) + local LLM (Ollama/LM Studio/vLLM)
- Free & open source untuk individu; produk berbayar: Cloud (dedicated sandbox VM per clone) + Network (E2E messaging antar clone tim)

## Arsitektur (2 data plane → 1 renderer)

```
Renderer (React): Office Floor (Pixi) + Terminal + Monaco IDE
      │  IPC (contextBridge: window.cth)
Event Plane (hive: memory, mailbox, router, GOD)  |  Terminal Plane (node-pty PTYs + fs + git)
      └────────── claude/codex/grok/kimi/opencode ──────────┘
```

### Terminal plane
- `PtyManager` spawn tiap agent sebagai node-pty process, stream output via IPC `pty:data:<id>`
- Renderer hanya bicara lewat `window.cth` (typed bridge di src/preload/index.ts)
- Sandboxed fs + git helpers

### Hive / event plane (kunci)
- `hive.ts` = on-disk multi-agent layer: memory, mailboxes, router, GOD
- **Setiap agent punya `outbox/` + `inbox/`** — folder file plain di dalam satu git repo lokal
- Router mengantar pesan antar-inbox; agent tak pernah menyentuh git (single-committer → anti index.lock)
- `hooks.ts` = hook server; provider bridge POST lifecycle payloads (cth-hook utk Claude Code, agy-hook utk Antigravity)
- **GOD agent (Michael)**: baca semua request → selesaikan rutin sendiri → **escalate HANYA yang kritis** (spend, destructive ops, scope change) ke approval manusia
- Idle/inbox wakeups: worker yang parkir dibangunkan saat mail masuk

## Fitur kunci

### Memory
- Markdown-first, recall dalam milidetik (semantic index)
- MemoryReflector: kondensasi agar tidak tumbuh selamanya
- Enterprise Knowledge Graph: dokumen/policy sendiri, queryable agent mana pun
- MemPalace: semantic search di UI

### Control & safety (paling menarik utk MC)
- **Circuit breaker bertingkat: steer → constrain → stop** (agent looping / error-storm / blow budget)
- Token budget per-agent + floor budget; ledger biaya riil dari transcript JSONL (`~/.claude/projects/`)
- Human gates: spend / scope / destructive → approval queue manusia
- Telemetri anonim opt-out (PostHog allowlist ketat, DO_NOT_TRACK, build dari source = no key)
- Secret broker write-only utk API keys per provider

### Command Center (paralel dgn Niu-MissionControl)
- TasksKanban + dependencies, scheduled missions + heartbeat, fleet monitoring live
- Memory search, activity log, CI watcher
- Built-in Monaco IDE: file tree, editor tabs, CHANGES/HISTORY/COMPARE git rails, commit graph, guarded checkout
- Slack & webhooks: Michael spawn ephemeral worker, reply in-thread, teardown
- Agent Gallery: shareable `munderdifflin://hire` link (import hanya pre-fill form; spawn tetap manual/manusia)
- Auto-update background

### Clone-to-clone (produk Network)
- E2E encrypted: X25519 / AES-256-GCM, plaintext hanya ada di dalam node masing-masing
- Shared org knowledge base (diprovision sekali, versioned, diwarisi clone baru)
- Personal context tidak pernah keluar dari node pemilik

## Struktur repo (src/)

```
src/main/      index.ts (window/IPC/quit guard), pty.ts, hive.ts, hooks.ts, memory.ts,
               config.ts, transcript.ts, telemetry.ts, usage/pricing.ts, breaker.ts,
               control.ts, reflect.ts, db.ts (SQLite), github.ts, shellEnv.ts, fs.ts, git.ts
src/preload/   contextBridge → window.cth
src/renderer/  App.tsx, design/ (tokens), components/ (PixelPanel, CommandCenterPanel,
               TasksKanban, ThreadsPanel, MessageQueueComposer, ToolWaterfall, scene/office/)
docs/          logo.png, landing (GitHub Pages → munderdiffl.in), media/ (Remotion clips)
HIVE.md        desain multi-agent   SPEC.md  terminal/event plane   DESIGN.md  visual system
```

## Pola yang layak diadopsi Niu-MissionControl

1. **Outbox/inbox file-based** (bukan hanya API dispatch) — auditable, anti-lock, bisa resume setelah restart; MC punya dispatch_store (JSON) — bisa diperdalam jadi file mailbox per thread
2. **Circuit breaker steer→constrain→stop** — MC belum punya guard runaway agent (consecutive_failures sudah ada di kanban.db sebagai cikal bakal)
3. **Single-committer git** untuk state bersama — menghindari konflik antar worker paralel
4. **Escalate-only-kritis ke manusia** — GOD agent memfilter dulu, bukan semua request ke user (MC: thread 1 general → dispatch ke 802-1172 sudah mirip)
5. **Token budget per-agent + ledger riil dari transcript** — MC sudah ada Cost Tracking; bisa diperkuat dgn data transkrip
6. **Wake-on-mail** — idle worker dibangunkan saat ada pesan (MC: dispatch status pending → agent perlu trigger)

## Catatan relevansi

- Roadmap Munder Difflin: "Telegram & richer chat bridges" = niche yang MC sudah lebih dulu punya (telegram bridge + dispatch thread)
- Lisensi: kode MIT (bisa dipelajari/diadaptasi); aset pixel-art terikat LimeZu non-komersial
- Status: working prototype, update sangat aktif (v0.4.3, 659 commits, co-authored Claude)

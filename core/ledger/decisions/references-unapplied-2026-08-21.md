# Referensi Belum Diterapkan — Tracking 2026-08-21

**Sumber:** `docs/references/STATUS-REFERENSI-2026-08-13.md` (stale, perlu refresh) + audit `docs/references/` (148 file) + verifikasi sistem.

## ✅ SUDAH DITERAPKAN (terverifikasi di sistem)
- `niu-core-fence` plugin → `~/.hermes/plugins/niu-core-fence/` aktif
- `niu-handoff.py`, `niu-model-guard.py`, `niu-fence.py` → `~/.hermes/agent-hooks/` ada
- `com.niumination.niu-mission-control.plist` → LaunchAgents, MC auto-start ✅
- Agent Reach ✅ · ULTRON ✅

## 🔴 BELUM DITERAPKAN (open)
1. **TELEGRAM-UNIFY** — 5 thread TG (1/802/803/804/1172) masih `default/default`.
   Referensi: `core/TELEGRAM-UNIFY.md` mewajibkan `opencode-zen:nemotron-3-ultra-free`.
   Aksi: butuh `/model` per-thread di sisi Telegram (bukan filesystem). Status: PENDING user.
2. **OmniRoute** (docs/references) — 📄 HIGH POTENTIAL, PENDING. Blocker: storage Docker 9.2GB.
3. **Kimi K3 in C** — 📄 reference only. Blocker: checkpoint 1.56TB.
4. **UniFace** — 📄 reference only. No use case spesifik.
5. **8 Website PWA pending deploy** (per STATUS-REFERENSI): niu-dash-fullstack, arch-web-dashboard,
   mac-web-dashboard, niu-kanban-dash, PAGASUS-PRO, Maze-3D-Game, Devs-Niu, niu-lkh.
6. **OpenCLI Chrome extension** — user klik manual (Chrome Web Store).

## CATATAN
- PR cc-acehtengah (#2/#3/#4) → ditangani di OpenCode-AI, auto-sync (aman, agen tidak usik).
- D-0003 masih `draft` tapi `superseded_by D-0004` (by design, bukan bug).
- D-0004 `review_after: 2026-09-04` (belum jatuh tempo).

*Diverifikasi dari filesystem + up-eco, bukan asumsi.*

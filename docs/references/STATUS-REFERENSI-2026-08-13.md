# Referensi Study — Status Tracking (Update 13 Agustus 2026)

## Ringkasan

| Referensi | Subjek | Status | Rekomendasi |
|---|---|---|---|
| **Agent Reach** | Internet capability layer | ✅ **SELESAI** | Cron reminder aktif |
| **Kimi K3 in C** | Local inference trillion params | 📄 Reference only | Pattern untuk future offline mode |
| **UniFace** | Face analysis library | 📄 Reference only | Butuh use case spesifik |
| **OmniRoute** | AI gateway + model routing | 📄 High potential | Pending — storage issue |
| **Websites Android PWA** | 16 websites status | 📋 Track project | 8 live, 8 perlu deploy |
| **ULTRON** | 3D command orb | ✅ **SELESAI** | v1-v3 complete |
| **9Router Crash-Loop Fix** | Fix 9router crash loop | ✅ **ADOPTED** | Di-merge ke skill `niu-9router-maintain` |
| **Hermes Free-Stack** | Merge free-stack + 9Router | 📋 **REFERENSI** | Disalin ke `~/Downloads/INSTRUKSI_UNTUK_HERMES.md` — belum di-apply (routing saat ini sudah jalan: huancheng→9router→opencode-zen) |

---

## Adopsi 29 Agustus 2026

- **Skill `niu-9router-maintain`** (di `~/.hermes/skills/`) di-upgrade: tambah section *Crash-Loop Fix* (insiden 27-Agu — 9router CLI TUI menu tanpa TTY → `--tray --skip-update`). Committed `db5e7f3`.
- **Refs besar dipindah ke `brain/resources/`** sebagai prompt library / study: `cadence-content-machine-all-prompts.md` (94KB), `jarvis-mission-control-all-prompts.md` (129KB), `analisis-optimalisasi-hermes-2026-08-18.md` (33KB), `studi-integrasi-10-referensi-2026-08-18.md` (17KB), `ekosistem-status.md`, `second-brain-plan*.md`. Committed `ab948f8` ke brain.git.
- **`archive/skills-main/` dihapus** (usang, 0 ref di manifest skill bank).
- **`hermes-free-stack.zip`** dipelajari: berisi instruksi merge Gemini/NVIDIA/Groq/GLM/OpenRouter + 9Router ke config Hermes. **Belum di-apply** — routing saat ini (`huancheng/auto` primary + `9router` + `opencode-zen/hy3-free`) sudah terverifikasi jalan & aman. Config.yaml Hermes juga diblokir agent untuk diedit langsung.

---

## Detail Per Referensi

### 1. Agent Reach ✅ COMPLETED
- **Repo:** https://github.com/Panniantong/Agent-Reach
- **Version:** v1.5.0
- **Status hari ini:** 5/15 channels aktif, 8 pending
- **Yang sudah diperbaiki:**
  - OpenCLI backend terinstall (npm package)
  - Exa semantic search via mcporter → **bekerja**
  - GitHub auth verified
  - browser-cookie3 installed untuk Xueqiu
- **Yang masih pending (butuh user action):**
  - Install Chrome extension OpenCLI: https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk
  - Login platform (Twitter/Reddit/FB/IG/Xiaohongshu) di Chrome
  - Setup Groq API key untuk Xiaoyuzhou
- **Cron reminder:** Setiap 6 jam via crontab sistem → `/tmp/agent-reach-reminder.log`

### 2. Kimi K3 in C 📄 REFERENCE ONLY
- **Repo:** https://github.com/FareedKhan-dev/kimi-k3-in-c
- **Stars:** 4.6k
- **Key insight:** 2.78T params bisa jalan di single CPU 8.24GB RAM via mxfp4 quantization
- **Relevansi:** Pattern quantisasi + memory-efficient MoE bisa jadi referensi untuk Hermes offline mode
- **Blocker:** Checkpoint 1.56TB — terlalu besar untuk USB portable
- **Action:** Simpan sebagai referensi arsitektur, belum bisa diimplementasi

### 3. UniFace 📄 REFERENCE ONLY
- **Repo:** https://github.com/yakhyo/uniface
- **Stars:** 1.2k
- **Capabilities:** Face detection, landmarks, recognition, gaze, anti-spoofing
- **Relevansi:** Input layer untuk desktop presence detection / face unlock
- **Blocker:** Tidak ada use case spesifik saat ini di Personal AI OS
- **Action:** Simpan, tunggu butuh visual input

### 4. OmniRoute 📄 HIGH POTENTIAL — PENDING
- **Repo:** https://github.com/diegosouzapw/OmniRoute
- **Stars:** 44.9k
- **Capabilities:** 290+ providers, 90+ free, auto-fallback routing
- **Relevansi:** Bisa menggantikan/memperbaiki 9Router + huancheng setup
- **Blocker:** Storage 9.2GB terpakai — Docker tidak bisa jalan
- **Action:** Prioritas setelah storage问题解决

### 5. Websites Android PWA 📋 TRACKED
- **13 websites sudah live** (PWA-ready)
- **8 websites perlu deploy:**
  - niu-dash-fullstack
  - arch-web-dashboard
  - mac-web-dashboard
  - niu-kanban-dash
  - PAGASUS-PRO
  - Maze-3D-Game
  - Devs-Niu
  - niu-lkh
- **Action:** Bisa dikerjakan batch (build + deploy)

---

## Saran Urutan Prioritas (jika mau lanjut)

### Fase 1 — Quick Wins (bisa selesai hari ini)
1. **Deploy 8 website PWA** yang pending (batch)
2. **Setup OpenCLI extension** (user perlu klik manual)

### Fase 2 — Medium Effort
3. **OmniRoute audit** — bandingkan dengan 9Router saat ini
4. **Kimi K3 pattern study** — dokumentasi teknis untuk future

### Fase 3 — Long Term
5. **UniFace** — tunggu ada use case spesifik

---

## Cron Jobs Aktif

| Job | Schedule | Status |
|---|---|---|
| agent-reach-watch | 08:00 daily | ✅ Active |
| agent-reach-reminder | */6 hours | ✅ Added via crontab |
| brain-morning-brief | 07:00 daily | ✅ Active |
| brain-daily-report | 23:00 daily | ✅ Active |
| memory-checkpoint | */6 hours | ✅ Active |
| sync-to-agents | */6 hours | ✅ Active |

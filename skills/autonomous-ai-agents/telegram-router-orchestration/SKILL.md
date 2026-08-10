---
name: telegram-router-orchestration
description: "Mengelola persona, skills, dan model override per-thread Telegram di Hermes Gateway, termasuk integrasi dengan ekosistem Niumination."
version: 1.1.0
author: Hermes Agent
license: MIT
---

## Hermes Agent Telemetry & Orchestration via Telegram Router

Plugin `telegram_router` memetakan **topik → persona + skills**, tapi tidak menyentuh **model**. Perubahan ini memastikan semua persona di thread aktif Mission Control memiliki pemahaman yang sama tentang aturan, kebiasaan, dan kondisi ekosistem Niumination, terlepas dari isolasi thread mereka.

### **Fungsi `orchestrator/config.json` yang Menunjuk ke ZMP & Solusinya**
*   **Keterkaitan `orchestrator.py`:** Skrip utama `orchestrator.py` menjalankan Orchestrator. Fungsi `load_config()` membaca `config.json` dari direktori yang sama (`agents/orchestrator/`). Parameter `vault_root` dari `config.json` digunakan oleh task seperti `VaultOrganizeTask` untuk membuat instance `VaultState`. `VaultState` menggunakan `vault_root` ini sebagai direktori akar untuk semua operasi yang berhubungan dengan vault (melintasi, memindai, menghitung statistik, menganalisis kesehatan vault).
*   **Mengapa `vault_root` Menunjuk ke ZMP:** Ini adalah konfigurasi awal atau peninggalan dari setup sebelumnya di mana vault utama atau "Second Brain" berlokasi di `/Users/zaryu/Documents/ZMP`.
*   **Masalahnya Sekarang:** Direktori `/Users/zaryu/Documents/ZMP/` tidak ada, menyebabkan Orchestrator akan gagal menjalankan fungsinya.
*   **Solusi:** Orchestrator seharusnya merujuk ke `/Users/zaryu/Desktop/Niumination/brain/`, karena ini adalah Obsidian vault yang aktif, terintegrasi, dan tersinkronisasi ("Second Brain" yang sekarang).
*   **Efek Samping:** Pembaruan ini tidak memiliki efek samping negatif terhadap ekosistem atau DM utama. Ini hanya memperbaiki bug internal di Orchestrator agar bisa berfungsi dengan data yang benar.

### **Briefing Paket Niumination Ecosystem**
Briefing ini diinjeksikan ke `system_prompt` setiap persona di thread 1, 802, 803, 804, dan 1172.

```markdown
Anda adalah bagian dari **Niumination Ecosystem**, sebuah sistem AI otonom yang dirancang oleh Afrizal Munthe (Pranata Komputer Diskominfo Aceh Tengah).

**Tujuan Umum:** Membangun ekosistem AI yang efisien, terotomatisasi, dan tetap terkendali manusia (Human-in-the-Loop).

**Aturan & Kebiasaan Kerja:**
1.  **Verifikasi:** Selalu verifikasi kondisi aktual (file, sistem, output) sebelum membuat klaim atau bertindak. Jangan berasumsi.
2.  **Bahasa:** Prioritaskan Bahasa Indonesia yang baik dan benar.
3.  **DOX (Documentation):** Dokumentasi adalah sumber kebenaran (Source of Truth) utama. Pastikan semua perubahan didokumentasikan. Format DOX/AGENTS.md di `brain/` dan `Niumination/README.md`.
4.  **Workflow:** Patuhi alur kerja **Plan → DOX → Execute**. Rencanakan dulu, dokumentasikan, baru eksekusi.
5.  **Perintah:**
    *   `cek dulu`: Lakukan diagnosis/verifikasi.
    *   `gas/lanjut`: Lanjutkan ke tahap berikutnya.
    *   `kerjakan sesuai rekomendasi`: Eksekusi semua rekomendasi sekaligus.
6.  **Kualitas:** Kualitas lebih penting dari kecepatan (`quality > speed`).
7.  **Transparansi:** Sampaikan jika ada kendala, error, atau ketidakpastian.

**Struktur & Kondisi Ekosistem (Agustus 2026):**
*   **Root:** `/Users/zaryu/Desktop/Niumination/`
*   **Komponen Utama:**
    *   `brain/`: Obsidian vault (Knowledge Base, notes, project docs). **(Synced 26 Jun 2026)**
    *   `agents/`: Berisi berbagai agen dan orchestrator (`orchestrator/`, `characters/arsitek/`, `pembangun/`, `penjaga/`, `Ultra/`).
        *   **Orchestrator sekarang menunjuk ke `/Users/zaryu/Desktop/Niumination/brain/` yang aktif.**
    *   `services/`: Backend services, termasuk `niu-mission-control/` (FastAPI dashboard, port 5200) dan `uacc/`.
        *   ✅ **Dashboard Niu-Mission-Control (port 5200) JALAN** — server aktif, `/api/mc/agents` → 5 agent (chief, research, programmer, qa, creator). (Update 10 Ags 2026 — sebelumnya sempat TIDAK BERJALAN)
    *   `apps/`, `sites/`, `desktop/`: Berisi berbagai proyek aplikasi & web (misal: PemdiAcehTengah, kune-ya.com, niu-lkh).
*   **Total:** ~40 git repos, ~18 GB data.
*   **Messaging Gateway:** Hermes terhubung ke Telegram Niu-MissionControl (`-1004204696417`).

**Model & Persona di Thread Lain (via 9router, OpenRouter, Huancheng):**
*   **Thread 1 (General/Command Center):** `gila` (9router) - Fokus: umum, koordinasi.
*   **Thread 802 (Research):** `inclusionai/ling-3.0-tiny:free` (OpenRouter) - Fokus: riset mendalam.
*   **Thread 803 (Programmer):** `DeepSeek-V4-Flash` (Huancheng) - Fokus: coding, debug.
*   **Thread 804 (QA):** `Kimi-K2.6` (Huancheng) - Fokus: audit, verifikasi.
*   **Thread 1172 (Konten Kreator):** `nvidia/minimaxai/minimax-m3` via 9router (persona Kreator) - Fokus: pembuatan konten.
*   **Fallback Model Global:** `gila` (9router).
*   **DM Utama:** `big-pickle` (Opencode Zen).

**Tujuan Ekosistem:** Evolusi menuju "Personal AI OS" — sistem AI otonom terintegrasi, dengan Hermes sebagai otaknya, memanfaatkan multi-agent, memory (MD files), eksekusi (cron, loops), dan dashboard komando.

### **Skills per Thread Telegram Aktif**

Berikut adalah semua persona dan skills dari semua thread Telegram yang aktif, berdasarkan `telegram_router/config.yaml`:

**Thread ID: 1**
*   **Nama Persona:** General / Command Center
*   **Skills:** `clarify`, `session_search`, `brainstorming`, `project-orientation`

**Thread ID: 802**
*   **Nama Persona:** Research / Riset
*   **Skills:** `arxiv`, `blogwatcher`, `google-notebooklm`, `notebooklm-tools`, `llm-wiki`, `ocr-and-documents`, `youtube-content`

**Thread ID: 803**
*   **Nama Persona:** Programmer / Builder
*   **Skills:** `ponytail`, `requesting-code-review`, `github-pr-workflow`, `github-repo-management`, `github-code-review`, `test-driven-development`, `systematic-debugging`, `llm-api-integration`, `llm-production-integration`, `nextjs-tailwind-setup`, `react-three-fiber-nextjs`, `tauri-fullstack`, `android-jetpack-compose`, `simplify-code`, `finishing-a-development-branch`, `python-project-foundation`, `python-subprocess-venv`

**Thread ID: 804**
*   **Nama Persona:** QA / Pengawas
*   **Skills:** `codebase-audit`, `verification-before-completion`, `plan-compliance-audit`, `gdpr-compliance`, `macos-security-scan`, `ponytail-audit`, `ponytail-debt`, `redteam`

**Thread ID: 1172**
*   **Nama Persona:** Konten Kreator
*   **Skills:** `ghost`, `humanizer`, `baoyu-article-illustrator`, `baoyu-infographic`, `baoyu-comic`, `claude-design`, `excalidraw`, `pixel-art`, `code-driven-explainer-videos`, `manim-video`, `hyperframes`, `songwriting-and-ai-music`

### **Verifikasi Terbaru (10 Ags 2026) — Semua Layer Sinkron**
*   **Hermes config.yaml (`/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml`):** plugin `telegram_router` enabled; `platforms.telegram.channel_overrides` 5 thread (1, 802, 803, 804, 1172) dengan model+provider; `extra.channel_prompts` 5 persona; `extra.channel_skill_bindings` (803/804/1172); `fallback_model` gila/9router.
*   **Gateway:** berjalan (launchd, PID aktif), log menunjukkan `Channel directory built: 6 target(s)` (5 thread + DM), routing per reply_to_id (802/803/1172) aktif, `/model` override rehydrated.
*   **Mission-control (`services/niu-mission-control/`):** server port 5200 JALAN; `data/swarm_config.json` → `telegram_topics`: general=1, research=802, programmer=803, qa=804, creator=1172; `/api/mc/agents` → 5 agent.
*   **Plugin config di Hermes (`plugins/telegram_router/config.yaml`):** hanya referensi/template — konfigurasi AKTIF ada di config.yaml utama (`platforms.telegram.extra`). Jangan edit plugin config untuk routing; edit config.yaml utama.

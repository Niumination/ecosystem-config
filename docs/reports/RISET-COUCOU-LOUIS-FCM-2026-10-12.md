# Riset: Coucou (Louis-CFM/coucou)

**Tanggal:** 12 Okt 2026
**Sumber:** github.com/Louis-CFM/coucou (README, docs/AGENTS.md, release v0.2.1, CHANGELOG, windows/README.md)
**Status:** Riset selesai. TIDAK diuji di mesin ini — premis inti tidak terpenuhi (lihat Batasan).

---

## Apa itu Coucou

Coucou = aplikasi **notch companion** (Tauri 2, Rust + TypeScript). Maskot "Mochi" — squircle kecil bermata besar — hidup di notch MacBook, mengikuti kursor, dan menampilkan sesi AI coding agent secara live.

**Lisensi:** MIT untuk kode. Nama "Coucou", karakter Mochi, ikon, suara, dan media © Louis Raillé (all rights reserved). Android app © Rhytam Biswas (MIT).

---

## Fitur inti

1. **Monitoring sesi agent live** — Claude Code, Cursor, Codex, Gemini CLI, Antigravity, Copilot CLI, Muse Code, OpenCode, Amp, Hermes, Claude Desktop. Lihat tool apa yang dijalankan, file apa yang diubah, langkah demi langkah di notch.
2. **Approve dari notch** — permission request Claude Code muncul dengan tombol Allow / Deny / Always. `AskUserQuestion` dengan pilihan single/multi-select. Satu klik, atau "Reply in terminal".
3. **Live diff** — setiap modifikasi file menampilkan nama file + count +N −M di ticker, tap untuk baca diff lengkap.
4. **Drop file ke notch** — Mochi jadi kotak, menelan file, lalu bisa ditanya atau dikirim email.
5. **Integrasi** — Spotify, email, web search, plan usage, GitHub PR + CI.
6. **Multi-platform** — macOS (notch), Windows & Linux (top-of-screen), iPhone & Android (lock screen approval).

---

## Dukungan Hermes Agent (relevansi untuk ekosistem kita)

Sejak **v0.2.1 (7 Okt 2026)** — satu hari lalu.

**Cara koneksi:** model **plugin**, bukan hook command. Install dari Settings → Agents → Hermes:
- Menulis plugin Python ke `~/.hermes/plugins/coucou/`
- Enable di `~/.hermes/config.yaml`
- Flow yang sama dengan agent lain: preview → backup dated → konfirmasi → write

**Yang ditampilkan di notch:**
- Sesi Hermes muncul dengan pill sendiri
- Tool steps live
- Final response saat selesai
- Platform (Telegram, Discord…) saat jalan via gateway

**Approval:** saat ini HANYA tampil "⏳ Approval pending in Hermes" di notch. **Approve dari notch belum didukung** — Hermes 0.15.x belum expose transport API. Toggle Approvals di Settings akan otomatis aktif setelah Hermes menambahkannya.

**Safety:** Coucou tidak pernah memblokir Hermes — kalau app tertutup/unreachable, Hermes tetap jalan dan handle approval sendiri.

---

## Cara kerja teknis (untuk agent generik)

Agent apapun yang bisa write ke Unix socket bisa kirim event ke Coucou dan punya pill sendiri. Field `coucou_agent` di JSON payload menentukan pill mana yang menerima event.

- Socket macOS: `~/Library/Application Support/NotchBuddy/nb.sock`
- Socket App Store: `~/Library/Containers/fr.louisraille.Coucou/Data/nb.sock`
- Linux: `$XDG_RUNTIME_DIR/coucou.sock`
- Windows: `\\.\pipe\coucou-<user-SID>`

Relay command: `nb-hook --agent <name> <EventName>` (macOS), `coucou-hook.exe` (Windows/Linux).

**Event yang didukung:** SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, Notification, Stop, StopFailure, SessionEnd, SubagentStart, SubagentStop. **PermissionRequest dari agent non-Claude TIDAK didukung** (dijawab tanpa keputusan, agent re-ask di terminal).

---

## Versi & rilis

| Versi | Tanggal | Highlight |
|---|---|---|
| 0.3.0 | 11 Okt 2026 | "OK Coucou" — bicara dengan Mochi, powered by Claude |
| 0.2.3 | 8 Okt 2026 | Terminal sessions, Spotify, warna per Mochi, dictation |
| 0.2.2 | 8 Okt 2026 | Pilih layar Mochi, Claude Desktop pill, Codex plan usage |
| **0.2.1** | **7 Okt 2026** | **Hermes Agent support** |
| 0.2.0 | 6 Okt 2026 | Copilot CLI, Muse Code, OpenCode, Amp, 10 bahasa |
| 0.1.9 | 6 Okt 2026 | iPhone services, smarter Live Activity |

---

## Batasan di mesin ini (tidak bisa diverifikasi)

**Premis inti tidak terpenuhi:** MacBookPro16,2 = MacBook Pro 13" 2019 — **tanpa notch**.

Coucou di macOS dirancang khusus sebagai notch companion. Di Windows/Linux ia hidup di top-of-screen, tapi dukungan Hermes Agent adalah **macOS-only** (GitHub build).

Akibatnya:
- Fitur utama (Mochi di notch, approve dari notch, live diff di notch) **tidak bisa dinilai** di mesin ini
- Tidak ada app notch terpasang (`/Applications` bersih dari NotchBuddy/coucou)
- Tidak ada `~/Library/Application Support/NotchBuddy`
- `~/.hermes/plugins/` kosong (belum ada plugin coucou)

Yang bisa jadi nilai untuk kita: monitoring sesi Hermes dan permission approval — tapi keduanya butuh layar dengan notch.

---

## Relevansi untuk ekosistem Niumination

**Yang sudah kita miliki (tanpa Coucou):**
- Monitoring: `ecosystem-health.py` cron tiap 2 jam → thread 12595
- Notification: Hermes cron delivery ke Telegram (14 job aktif)
- Approval: Hermes handle sendiri via Telegram

**Yang ditawarkan Coucou dan belum kita punya:**
- Visual monitoring real-time di layar (tool steps, diff, file changes)
- Lock screen approval (iPhone/Android)

**Kesimpulan:** Coucou adalah tools yang bagus untuk **MacBook dengan notch** yang ingin monitoring visual + approve dari layar/lock screen. Untuk mesin kita (MacBook Pro 13" 2019 tanpa notch), nilai inti tidak bisa dinilai. Kalau ingin monitoring visual, alternatif yang bisa dipakai: Mission Control dashboard (`:8080`) atau Hermes Telegram notification yang sudah jalan.

---

## Sumber

- README: https://github.com/Louis-CFM/coucou
- Agent integration: https://github.com/Louis-CFM/coucou/blob/main/docs/AGENTS.md
- Release v0.2.1: https://github.com/Louis-CFM/coucou/releases/tag/v0.2.1
- Changelog: https://github.com/Louis-CFM/coucou/blob/main/CHANGELOG.md
- Windows/Linux: https://github.com/Louis-CFM/coucou/blob/main/windows/README.md

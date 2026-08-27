# Ecosystem Status — 2026-08-27 (READ ALL AGENTS)

_Root: `~/Desktop/Niumination` · Broadcast to: JCode, OpenCode, Hermes, Ultra, orchestrator, characters, all subagents._

## TL;DR (baca ini dulu)
- Sistem **BERJALAN** (jcode, opencode, 9router :20128, Hermes gateway, thermal-guardian semua hidup & stabil, temp ~74°C).
- Tapi **file konfigurasi di disk sempat hilang** karena 1 session jcode salah direktori. Session tersebut **sedang memulihkan (repair) secara mandiri** — biarkan selesai, jangan edit config saat repair berjalan.
- Setelah repair selesai & config kembali, **migrasi kredensial ke broker** (`scripts/keys.sh`) baru dijalankan.

## Insiden hari ini (timeline singkat)
| Waktu | Kejadian |
|-------|----------|
| ~09:00 | Mac panas (85°C, load 11) karena opencode + 9router + batch job memonopoli CPU 15W TDP i5. |
| ~09:12 | `thermal-guardian.sh` dipasang (launchd `com.niumination.thermal-guardian`) — renice dinamis by name. |
| ~09:20 | 9router crash-loop (launchd KeepAlive + TUI menu butuh TTY → `Exiting...` 130x). Diperbaiki ke `--tray` mode. |
| ~09:43 | `scripts/keys.sh` broker (macOS Keychain) di-scaffold + `vault/` perm 755→700. |
| ~10:16 | Phase B migrasi live key **DITAHAN** karena 2 session jcode aktif (HOLD di BACKLOG). |
| ~10:31 | `/up-eco` Phase 9c (Credential Broker status) diintegrasikan. |
| ~17:45–18:04 | **1 session jcode salah direktori → menghapus config** (`.jcode/config.json`, `.hermes/.env`, `opencode.jsonc`, `.config/9router/`, `vault/secrets.zsh`). Proses tetap hidup (config sudah di-memory). |
| ~18:08 | User konfirmasi: session tsb sedang **repair mandiri**, aman. |

## Aturan sementara (berlaku sampai repair selesai)
1. **JANGAN** edit/tulis `~/.jcode/config.json`, `~/.hermes/.env`, `~/.config/opencode/*`, `~/.config/9router/*`, `vault/*` saat repair berjalan.
2. **JANGAN** jalankan `keys set` / repoint config ke broker sampai config asli kembali utuh.
3. Agent lain yang butuh model: lewat 9router (`127.0.0.1:20128`) seperti biasa — sudah jalan.
4. Kalau ada session jcode/opencode crash: biarkan launchd `KeepAlive` restart; jangan manual hapus file.

## Credential Broker (rencana, status)
- **Tier 1 (broker):** flat AI-API key → satu sumber di macOS Keychain via `scripts/keys.sh`.
  17 canonical: opencode_zen, openrouter, gemini, github, fal, telegram, agentrouter, juan, nine_router, huancheng, aerolink, tavily, anthropic, vercel, discord, bing, nvidia_nim.
- **Tier 2 (tetap di tempat):** 9router pegang upstream key sendiri; broker hanya kelola token lokal `sk-...`-nya. OAuth tetap di native store.
- **Status:** Phase A + `/up-eco` Phase 9c ✅. Phase B migrasi live key = **blocked** sampai repair selesai & sumber key muncul kembali.
- Detail: `docs/references/credential-broker-design.md`, `docs/references/credential-broker-handoff.md`.

## Cara cek status cepat
```
osx-cpu-temp                                  # suhu
sh ~/Desktop/Niumination/scripts/thermal-status.sh
sh ~/Desktop/Niumination/scripts/keys.sh list # key di broker
launchctl list | grep -iE "9router|thermal"   # daemon
```

## Untuk agent yang baru masuk ekosistem
Baca `AGENTS.md` (root) → ini adalah status terbaru. Jangan asumsikan config di disk lengkap sampai repair dikonfirmasi selesai oleh user.

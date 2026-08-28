# Ecosystem Status — 2026-08-27 (READ ALL AGENTS)

_Root: `~/Desktop/Niumination` · Broadcast to: JCode, OpenCode, Hermes, Ultra, orchestrator, characters, all subagents._

## TL;DR (baca ini dulu)
- Sistem **BERJALAN** (jcode, opencode, 9router :20128, Hermes gateway, thermal-guardian semua hidup & stabil, temp ~74°C).
- Tapi **file konfigurasi di disk sempat hilang** karena 1 session jcode salah direktori. Session tersebut **sedang memulihkan (repair) secara mandiri** — biarkan selesai, jangan edit config saat repair berjalan.

## Insiden hari ini (timeline singkat)
| Waktu | Kejadian |
|-------|----------|
| ~09:00 | Mac panas (85°C, load 11) karena opencode + 9router + batch job memonopoli CPU 15W TDP i5. |
| ~09:12 | `thermal-guardian.sh` dipasang (launchd `com.niumination.thermal-guardian`) — renice dinamis by name. |
| ~09:20 | 9router crash-loop (launchd KeepAlive + TUI menu butuh TTY → `Exiting...` 130x). Diperbaiki ke `--tray` mode. |
| ~09:43 | `vault/` perm 755→700 diamankan. |
| ~17:45–18:04 | **1 session jcode salah direktori → menghapus config** (`.jcode/config.json`, `.hermes/.env`, `opencode.jsonc`, `.config/9router/`, `vault/secrets.zsh`). Proses tetap hidup (config sudah di-memory). |
| ~18:08 | User konfirmasi: session tsb sedang **repair mandiri**, aman. |

## Aturan sementara (berlaku sampai repair selesai)
1. **JANGAN** edit/tulis `~/.jcode/config.json`, `~/.hermes/.env`, `~/.config/opencode/*`, `~/.config/9router/*`, `vault/*` saat repair berjalan.
2. **JANGAN** edit kredensial sampai config asli kembali utuh.
3. Agent lain yang butuh model: lewat 9router (`127.0.0.1:20128`) seperti biasa — sudah jalan.
4. Kalau ada session jcode/opencode crash: biarkan launchd `KeepAlive` restart; jangan manual hapus file.

## Cara cek status cepat
```
osx-cpu-temp                                  # suhu
sh ~/Desktop/Niumination/scripts/thermal-status.sh
launchctl list | grep -iE "9router|thermal"   # daemon
```

## Untuk agent yang baru masuk ekosistem
Baca `AGENTS.md` (root) → ini adalah status terbaru. Jangan asumsikan config di disk lengkap sampai repair dikonfirmasi selesai oleh user.

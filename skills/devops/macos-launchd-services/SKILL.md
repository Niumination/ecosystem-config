---
name: macos-launchd-services
description: Keep macOS always-on services alive; recover launchd plists.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [macos, launchd, launchagent, caffeinate, nosleep, persistent-service, 9router, hermes-gateway, mission-control, insiden-recovery]
    related_skills: [niu-9router-maintain, env-doctor, dotfiles-maintenance]
---

# macOS Launchd Persistent Services

The Niumination workstation runs several always-on services that MUST stay up or Telegram routing / dashboards break. This skill covers verifying them, writing correct LaunchAgents, and recovering after a config-wipe incident (e.g. the 27-Agu-2026 jcode wrong-dir wipe that deleted `~/Library/LaunchAgents/*.plist`).

## When to Use
- "Mac ku kok bisa sleep / tidur?" → caffeinate/no-sleep LaunchAgent hilang
- "9router mati", "Mission Control mati", "gateway Hermes mati"
- After ANY bulk-delete / jcode wrong-directory incident — user-scoped LaunchAgents in `~/Library/LaunchAgents` are NOT in any git repo and get wiped silently
- "cek service lokal" / "cek ekosistem"

## Known Services (inventory)
Full table + exact health commands in `references/services-inventory.md`.

| Service | Port | Plist | Critical? |
|---|---|---|---|
| Hermes Gateway | ephemeral | `ai.hermes.gateway.plist` | ✅ `KeepAlive` — auto-restarts |
| 9router (model router) | 20128 | `com.9router.autostart.plist` | ✅ Telegram channels depend on it; auto-restart |
| 9router cache-watch | — | `com.niumination.9router-watch.plist` | ⚪ NON-CRITICAL, can be dead |
| Mission Control UI | 5200 | `com.niumination.missioncontrol.plist` | ⚠️ UI-only; FastAPI backend is a separate process |
| No-sleep (caffeinate) | — | `com.niumination.nosleep.plist` | ✅ PREVENTS MAC SLEEP |

## Health-Check Recipe (read-only, run first)
```bash
# is a port listening?
lsof -iTCP:20128 -sTCP:LISTEN -P -n
# is a launchd service loaded/alive?
launchctl list | grep -iE "9router|missioncontrol|nosleep|hermes"
# is the process there?
pgrep -fl caffeinate
pgrep -fl "hermes_cli.main gateway"
# does the service actually respond?
curl -s -o /dev/null -w "%{http_code}" -m 8 http://localhost:20128/v1/models
```

## Creating a LaunchAgent (correct pattern)
Every always-on service plist MUST have BOTH:
```xml
<key>RunAtLoad</key>
<true/>
<key>KeepAlive</key>
<true/>
```
Without `KeepAlive` the service won't restart if it crashes; without `RunAtLoad` it won't start at boot.

Load / restart:
```bash
# first load (fails if already loaded):
launchctl load ~/Library/LaunchAgents/com.niumination.nosleep.plist
# restart an already-loaded service (preferred over load):
launchctl kickstart -k gui/$(id -u)/com.niumination.nosleep
# verify:
launchctl list | grep nosleep
pgrep -fl caffeinate
```

## The No-Sleep / Caffeinate Case (most common loss)
After a config-wipe the no-sleep LaunchAgent disappears and `pmset sleep` reverts to `1` → Mac sleeps and kills everything (gateway, 9router, MC).
Recovery: deploy `templates/nosleep.plist` (caffeinate `-s -d -i -m`) and load it.
Verify the assertion is actually held:
```bash
pmset -g assertions | grep -i "PreventUserIdleSystemSleep"
# expect: pid <X>(caffeinate): ... PreventUserIdleSystemSleep named: "caffeinate command-line tool"
pmset -g | grep sleep   # shows "sleep prevented by caffeinate"
```
Flags: `-s` AC-powered, `-d` display, `-i` idle, `-m` disk.

## 9router Sync Notification Spam Fix
The `9router-sync.sh` script (hybrid watcher) fires `osascript display notification` on EVERY model-list delta. When the 9router model catalog flip-flops (e.g., 517↔521 every ~60s due to provider connection churn), this floods the macOS notification center.

**Fix (apply to `scripts/9router-sync.sh`):**
1. **Remove the `osascript` notification block entirely** — log-only is sufficient. The notification was a UX regression, not a feature.
2. **Add debounce window (120s):** record the first change timestamp to `~/.cache/niumination/9router-models.stable`. Only commit the change if the hash stays stable for the full window. Flip-flops within the window are discarded.
3. **Raise curl timeout 10s→30s** — the catalog is large post-update (`model-catalog-raw.json` 528K+), and 10s times out silently.
4. **Remove redundant `com.niumination.9router-watch.plist`** (StartInterval 60s, too aggressive) — `com.niumination.9router-sync.plist` (300s + WatchPaths) is sufficient. Two pollers racing on the same hash file cause duplicate notifications.

Verify fix: run the script twice within 30s — the second run should print "change pending" and exit without committing.

**Post-fix launchctl state:**
- `com.9router.autostart` → running (server)
- `com.niumination.9router-sync` → running (single watcher)
- `com.niumination.9router-watch` → removed

## Script-Job Cron: Kenapa `--script` Polos Sering Tidak Melakukan Apa-Apa

Job `no_agent` menjalankan `--script` **tanpa argumen**. Skrip yang memparse subperintah lewat
`case "${1:-}"` (pola `eco-guard.sh` v3) akan jatuh ke cabang `usage` lalu `exit 2` — job
laporkan `ok`, tidak ada error, dan **tidak ada pekerjaan yang terjadi**. Ini bentuk paling halus dari
"job jalan tapi tidak berbuat apa-apa": tidak ada baris error untuk ditangkap.

**Aturan:** sebelum menjadwalkan skrip sebagai `--script`, uji tanpa argumen dari shell polos:
```bash
bash <skrip>            # harus benar-benar mengerjakan tugasnya, bukan menampilkan usage
```
Kalau skrip butuh subperintah, bungkus:
```bash
# wrapper: paksakan subperintah, tidak mengubah skrip asli (satu file = satu penulis)
exec bash "$HOME/.hermes/scripts/eco-guard.sh" backup
```

**Bukti kasus nyata (18 Okt 2026):** `hermes cron create ... --script eco-guard.sh --no-agent`
membuat job yang hanya mencetak usage tiap tick. Gejalanya justru kelihatan sebagai *kegagalan*:
`hermes backup` ditinggalkan di tengah jalan meninggalkan arsip sementara `*.zip.<pid>-<n>.partial`
(135 MB + 239 MB) yang bukan zip valid (`unzip -t` rc=9), sementara `eco-guard.sh verify`
melaporkan `[MASALAH] belum ada file backup di ...`. Dua gejala yang tampak tidak berhubungan itu
berakar pada satu hal: subperintah `backup` tidak pernah benar-benar dipanggil.

Setelah wrapper dipasang (`~/.hermes/scripts/eco-guard-backup.sh`), job harus **dijalankan manual sekali**
(`hermes cron run <job_id>`) dan hasilnya diverifikasi dari luar — file zip benar-benar muncul,
`unzip -t` bersih, sha256 cocok — bukan hanya membaca `Last run: ok`.

## Deteksi "Alat Menganggur" yang Merujuk ke Diri Sendiri (self-referential check)

Jebakan saat memeriksa "apakah skrip X sudah dijadwalkan": mencari nama `X` di dalam **`cron/jobs.json`**. Masalahnya, keluaran pemeriksaan itu sendiri (`[PERIKSA] alat ini ada tapi TIDAK dipanggil penjadwal mana pun: X …`) disimpan ke `last_error` job **yang sama**, sehingga:
1. Alat dilaporkan menganggur → teks laporan masuk `jobs.json`.
2. Run berikutnya `grep` menemukan nama itu di `last_error` → alat dianggap **terjadwal**.
3. Baris hilang → daftar temuan berubah → lapor lagi → `jobs.json` berubah lagi → loop.

Gejala: satu baris temuan **berflap** (muncul-hilang) dan `jobs.json` berubah setiap kali job pemeriksa berjalan.

**Aturan:** saat memeriksa penjadwalan, baca hanya field yang memang mendefinisikan penjadwal (`script`, `prompt`, `schedule`), **jangan** seluruh JSON. Atau abaikan `last_error`/`last_status` secara eksplisit:
```bash
python3 -c "import json;d=json.load(open('$HOME/.hermes/cron/jobs.json'));jobs=d['jobs'] if isinstance(d,dict) else d;print(any(j.get('script')=='trio-watch.sh' or 'trio-watch.sh' in str(j.get('prompt','')) for j in jobs))"
```

**Pelajaran terkait (dedup laporan):** jangan membandingkan stdout mentah untuk memutuskan "ada perubahan". Hitung-mundur (`kedaluwarsa dalam 0.4 jam`) dan angka kotor (`17 baris error/blocked (OK: 38)`) membuat fingerprint berubah tiap tick. Normalisasi dulu: buang timestamp, bulatkan angka ke kelas `<N>`, dan jadikan daftar nama satu kelas. Tanpa itu, wrapper "laporkan hanya bila berubah" akan berisik selamanya.

## Cakupan Backup: `hermes backup` TIDAK Memuat Repo Ekosistem

`hermes backup` mengarsipkan **`~/.hermes` saja** — ia **tidak** memuat `~/Desktop/Niumination` (repo, `docs/`, `vault/`, `skills/`). Jangan pernah menganggap "sudah `hermes backup`" berarti seluruh ekosistem aman.

Jalur off-site untuk repo ekosistem (dua-duanya wajib diperiksa setelah menulis berkas penting):
1. **Push GitHub** — `git -C ~/Desktop/Niumination status -sb` harus `## main...origin/main` tanpa `[di depan N]`. Cek dengan `git log --oneline @{u}..HEAD | wc -l` (harus 0).
2. **Restic** — `restic-backup.sh` memuat `~/.hermes/config.yaml`, `auth.json`, `SOUL.md`, `cron/`, `Niumination/vault`, `Niumination/docs`, `Niumination/brain`, `Niumination/wiki`. Jalankan manual lalu **verifikasi isinya**, bukan hanya snapshot-nya dibuat:
```bash
restic -r '/Volumes/Mac Win/Backups/restic' --password-file "$HOME/.config/restic/pass" dump latest <path-berkas> | grep -c '<kata-kunci>'
```

**Jebakan:** menjalankan backup lalu melaporkan "sudah tercadangan" tanpa memeriksa isi. Pada 18 Okt 2026, berkas keputusan baru yang sudah di-commit **tidak ada** di zip `hermes backup` terbaru (karena memang bukan cakupannya) dan belum ada di restic (snapshot terakhir lebih tua dari berkas itu). Kedua jalur harus ditutup eksplisit.

## Keputusan yang Sengaja: Cari Registry Dulu, Jangan Ukur Dulu

Keadaan yang **disengaja dipilih** terlihat identik dengan kerusakan saat diperiksa mentah. Dua contoh nyata di ekosistem ini:
- **K-01** — FileVault OFF. `fdesetup status` → `FileVault is Off.` Tampak seperti regresi keamanan. Nyatanya keputusan sadar: pada Hackintosh (macOS Tahoe + OpenCore) FileVault menyebabkan sandi akun ditolak di layar boot; bug resmi `acidanthera/bugtracker#2499` punya gejala sama dan penyelesaiannya justru mematikan enkripsi.
- **K-05** — error cron bukan masalah struktural (penyebab: model rate-limit / combo tanpa fallback).

**Aturan:** sebelum melaporkan keadaan sebagai temuan, periksa registry keputusan (`docs/DECISIONS.md`, `docs/registry/KEPUTUSAN-TETAP.md`). Bila keadaan itu ada di sana → **bukan temuan**, dan jangan diangkat sebagai alarm. Menyalakan FileVault di mesin Hackintosh = membuat pemilik terkunci di layar boot.

**Kesalahan yang pernah terjadi (18 Okt 2026):** agen menjalankan `fdesetup status`, melihat `FileVault is Off.`, lalu menulisnya sebagai "regresi dari target G9.8" di laporan — tanpa menelusuri sesi agen lain yang memuat keputusan aslinya. Koreksi ditemukan hanya karena pemilik menegur. Gejala khasnya: **laporan berisi kata "regresi"/"celah" untuk keadaan yang sebenarnya sudah diputuskan.** Bila ragu, tanya pemilik dulu; jangan ubah keadaan yang tampak seperti keputusan.

## Pitfalls
- **PATH is an inherited value too, and a missing binary fails SILENTLY inside a pipeline.** launchd's PATH is minimal — `sha256sum` (in `/sbin`) is typically absent. The `cmd_a || cmd_b` idiom does **not** rescue it, because a pipeline's exit status comes from its LAST command, so the `||` never fires and the variable ends up empty; a script comparing that empty value to a stored empty value takes the "nothing changed" branch forever. Probe with `command -v`, guard the empty result with `exit 1`, and test under `env -i PATH=<plist PATH>`. Full mechanism + correct `_hash_ids()` pattern in `references/launchd-env-not-shell-env.md`.
- **A job that runs but does nothing is harder to notice than one that fails.** A self-perpetuating silent no-op (exit 0, no output, no error) leaves no trace in logs or notifications. When a scheduled job appears healthy but its effect never appears, check whether the state/hash file it should be writing is zero bytes or frozen — that is the signature of a pipeline that never produced output, not of a job with nothing to do.
- **`launchctl load` fails with I/O error** if the agent is already loaded/collides → use `launchctl kickstart -k gui/$(id -u)/<label>` instead.
- **Do NOT edit `~/.hermes/config.yaml` via patch/write_file** — agent is blocked (security). Use `hermes config set <key> <value>`.
- **Mission Control `/api/*` → 404 is normal** if only the Next.js UI (`apex-ui`) runs and the FastAPI backend process is not up — that's a separate process, not a routing failure.
- **9router provider management** belongs in `niu-9router-maintain`, not here.
- User-scoped LaunchAgents are NOT in any git repo → back the plist files up (e.g. copy to `~/Desktop/Niumination/dotfiles/` or a timestamped archive) so a future incident can't wipe them silently. The 27-Agu insiden proved this.
- **`KeepAlive:false` = SILENT DEATH (most dangerous mistake).** Unlike `KeepAlive` missing, a plist with `KeepAlive:false` LOADS FINE and the process shows up in `launchctl list` — but when the server child exits (common in tray-mode apps without a TTY), launchd does NOT restart it. Symptom: `launchctl list` shows the PID, yet `curl → 000` and `lsof -iTCP:PORT -sTCP:LISTEN` is EMPTY. 29-Agu: `com.9router.autostart` had `KeepAlive:false` → 9router died every few minutes, Telegram routing broke, and it looked "alive" in launchctl. Fix: set `KeepAlive` to `<true/>` (not just present — must be boolean true), unload+load, then verify with `lsof` (must show LISTEN), not just `launchctl list`.
- **Network dependency at boot/login:** if a service needs outbound network/DNS immediately after `RunAtLoad`, it can fail before the macOS network stack is ready. Symptom: launchd runs the service at login, then the service logs DNS/network errors and exits; `KeepAlive` restarts it, but the first message may already be missed. This happened with Hermes Gateway: Telegram notification delivery failed on the first startup after boot because DNS was not yet available. Fix: add a small network-wait wrapper before the real service command, with a bounded timeout so boot does not hang indefinitely.
- **Race condition on startup:** after `load`/`kickstart`, a server may take ~10s before it binds the port. `curl → 000` in the first seconds is NOT a crash — retry 3-5× with 2s gaps before concluding it's dead.
- **NEVER put a credential in a plist's `EnvironmentVariables`.** `~/Library/LaunchAgents/*.plist` are mode 644 by default — world-readable, and any `.bak` you make is a second plaintext copy. Put the secret in the app's own env file (`~/.hermes/.env`, mode 600, git-ignored) and leave only non-secret settings (`A2A_HOST`, ports, paths) in the plist. If one already leaked in: `chmod 600` the plist, delete the `.bak`, then move the secret to the app env file — add to the new location FIRST and prove the app resolves it, only then delete from the plist, or you create an auth outage.
- **A plist edit does not apply to the running process.** Editing the file then reporting "fixed" is unverified; the service keeps the old env until reload. After editing: `plutil -lint`, then `launchctl print gui/$(id -u)/<label> | grep -E 'state|pid'`, and prove the *new* value resolves by running the app's own config loader in a separate process.
- **`.env` beats plist in Hermes** (`gateway/run.py` calls `load_hermes_dotenv(..., override=True)`), but only for keys the `.env` actually defines — a missing key leaves the plist value live. So "the plist is redundant" is unsafe to assume: verify with `grep -c '^<KEY>' ~/.hermes/.env` before removing anything.

## Hybrid Watcher Pattern (WatchPaths + StartInterval)
For poller/notifier services that should run on a schedule AND instantly when a watched file changes, use BOTH keys (don't pick just one):
```xml
<key>StartInterval</key>
<integer>300</integer>            <!-- poll every 5 min -->
<key>WatchPaths</key>
<array>
  <string>/Users/zaryu/.9router/db/data.sqlite</string>   <!-- trigger instantly on change -->
</array>
```
Used by `com.niumination.9router-sync.plist` (see `templates/9router-sync.plist`): polls `/v1/models` every 5 min AND fires the moment `providerConnections` changes in the 9router DB, then hashes model IDs and posts a macOS notification only on delta. Backup copy lives in `~/Desktop/Niumination/scripts/com.niumination.9router-sync.plist`.

## Portable backup convention
Any LaunchAgent plist that is modified for a network-wait or recovery fix should be backed up into the portable Hermes repo:
`~/Desktop/Niumination/apps/JHermUSB-portable/config/launchd/<label>.plist`
This keeps the local `~/Library/LaunchAgents/` file and a git-tracked copy aligned.

## Skill-sync conflict pattern
When `sync-to-agents.sh` reports a target skill newer than bank, do **not** assume the target is always the source of truth.
1. Inspect whether the target edit is a local runtime mutation or a real content improvement.
2. If it is a real improvement, backport target → bank (`cp`) then regenerate manifest and re-sync.
3. If it is only a local artifact, overwrite target with bank.

## References
- `references/services-inventory.md` — full service table + exact health commands
- `references/launchd-env-not-shell-env.md` — what launchd does NOT inherit (env vars, PATH), the silent-pipeline-failure trap, and how to test under the real launchd environment
- `templates/nosleep.plist` — ready-to-deploy caffeinate LaunchAgent
- `templates/9router-sync.plist` — hybrid WatchPaths+StartInterval notifier (realtime model-change alerts)
- `references/gateway-network-wait-fix-2026-08-30.md` — Hermes Gateway DNS-at-boot incident and wrapper fix
- `references/browser-capture-waf-bypass.md` — Playwright browser capture on laptop for WAF-blocked endpoints (Jalur G2)

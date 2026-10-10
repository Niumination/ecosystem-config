# Laporan Audit MIRAI Mac — tahap berikutnya Arena

Bukti mentah per heading, tanpa parafrase. Rahasia dipotong (token, cookie, Authorization).

## 0. Identitas mesin

```
x86_64
ProductName:    macOS
ProductVersion: 26.7.1
Python 3.9.6
HOME=/Users/zaryu
```

Path:

```
ls: /Users/zaryu/mirai: No such file or directory          # dibersihkan
ls: /Users/zaryu/mirai-src: No such file or directory       # dibersihkan
ls: /Users/zaryu/wiki: No such file or directory            # dibersihkan
drwxr-xr-x  13 zaryu  staff  416 Oct 10 20:43 /Users/zaryu/Desktop/Niumination/mirai
drwxr-xr-x  11 zaryu  staff  352 Oct 10 22:36 /Users/zaryu/Desktop/Niumination/wiki
```

Git:

```
git -C ~/Desktop/Niumination rev-parse --show-toplevel
/Users/zaryu/Desktop/Niumination

git -C ~/Desktop/Niumination/mirai rev-parse HEAD
2af734d5799c13ab03828191ebf663d7087e08a3

git -C ~/Desktop/Niumination/mirai remote -v
origin  https://github.com/Niumination/mirai.git (fetch)

git -C ~/Desktop/Niumination/wiki rev-parse HEAD
de88f1fba83803527974c43627e462ecd90a93a9

git -C ~/Desktop/Niumination/wiki log -3 --oneline
de88f1f default: ecosystem-test (deleted)
566f137 default: ecosystem-test
8d01190 default: afrizal-munthe
```

## 1. Proses MIRAI

```
launchctl print gui/501/com.mirai.mission-control | egrep 'state =|pid =|path =|stdout|stderr'
	path = /Users/zaryu/Library/LaunchAgents/com.mirai.mission-control.plist
	state = running
	stdout path = /Users/zaryu/Desktop/Niumination/mirai/data/mission-control.log
	stderr path = /Users/zaryu/Desktop/Niumination/mirai/data/mission-control.err.log
	pid = 29236

lsof -nP -iTCP:8800 -sTCP:LISTEN
Python  29236  zaryu   8u  IPv4  ...  TCP 127.0.0.1:8800 (LISTEN)

lsof -nP -iTCP:8899 -sTCP:LISTEN
(kosong — wiki dashboard LaunchAgent belum dipasang)
```

TIDAK listen `0.0.0.0`. Bind loopback only.

## 2. /api/health 17/20 — rinci

```
curl -sS http://127.0.0.1:8800/api/ping
{"uptime_s": 4740.321, "ok": true}
```

Status: `needs a look`, passed 17/20.

**3 item BUKAN ok:**

```
✗ Cron ticker fresh: no heartbeat file
✗ Every profile readable: cannot read default
✗ Machine up over an hour: unknown
```

Catatan: heartbeat wiki-dropbox ADA di `~/Desktop/Niumination/wiki/_wiki-health.md` (heartbeat
lines setiap ~30 menit). "Cron ticker fresh" kemungkinan mengecek path hardcoded lain — perlu
konfirmasi Arena. "Every profile readable: cannot read default" — profile default ADA dan jalan
(gateway pid 27772 aktif), server mungkin membaca path profile yang salah.

## 3. Roster vs 10 persona

```
curl -sS http://127.0.0.1:8800/api/agents
{
    "agents": [
        {
            "code": "DE",
            "short": "Default",
            "name": "Default",
            "role": "One of the fleet's agents, running profile default.",
            "profile": "default",
            "model": "Atria-Dawn-Preview",
            "status": "unreachable",
            "status_label": "Unreachable",
            "present": true,
            "building": "Default Depot",
            "last_active": null,
            "stats": {
                "last_active": null,
                "avg_response_s": null,
                "sessions_24h": 0,
                "sessions_total": 0
            }
        }
    ]
}
```

```
ls -la ~/.hermes/profiles
(drwxr-xr-x — kosong, 0 profile tambahan)

hermes profile list
(default saja — 1 profile)
```

Yaml 10 thread — persona `channel_prompts` di `~/.hermes/config.yaml` path
`platforms.telegram.extra.channel_prompts`:

```
thread 1      : Kamu adalah Triage — inbox manusia untuk Niu-MissionControl...
thread 802    : Kamu adalah Researcher - agent riset untuk Niu-MissionControl...
thread 803    : Kamu adalah Builder - agent pengembangan software untuk Niu-MissionControl...
thread 804    : Kamu adalah Pengawas - agent audit dan QA untuk Niu-MissionControl...
thread 1172   : Kamu adalah Kreator - agent pembuat konten untuk Niu-MissionControl...
thread 8853   : Kamu adalah Admin Dinas ASN — asisten administrasi & kinerja pegawai...
thread 7402   : Kamu adalah Thread Serbaguna — asisten umum cadangan...
thread 12595  : Kamu adalah Thread Cron & Otomasi — khusus untuk output cronjob Hermes...
thread 12707  : Kamu adalah Edu Content - agent konten edukasi untuk Niu-MissionControl...
thread 13902  : Kamu adalah Orkestrator — koordinator ekosistem Niu-MissionControl...
```

Model per thread (`platforms.telegram.extra.channel_overrides`):

```
1     : gemini-3.5-flash-lite / 9router
802   : combo-delegasi / 9router
803   : kr/deepseek-3.2 / 9router
804   : combo-delegasi / 9router
1172  : combo-delegasi / 9router
7402  : combo-delegasi / 9router
8853  : sensenova-6.8-flash-lite / huancheng
12595 : combo-delegasi / 9router
12707 : combo-delegasi / 9router
13902 : combo-gateway / 9router
```

## 4. Cron wiki (harus 5, bukan 7)

```
hermes cron list (wiki-* saja):
  wiki-closing-snapshot
  wiki-dropbox
  wiki-librarian
  wiki-lint
  wiki-opening-snapshot

mail-sweep/offsite: 0  (TIDAK ADA — benar)
```

## 5. Wiki CLI vs path ekosistem

```
command -v wiki
/Users/zaryu/.local/bin/wiki

WIKI (line 30):
WIKI="${CREW_WIKI_DIR:-$HOME/Desktop/Niumination/wiki}"

CREW_WIKI_DIR= wiki index → jalan, resolve ke ekosistem

ls -ld ~/Desktop/Niumination/wiki/.wiki.lock
No such file or directory   (lock = directory mkdir, dibersihkan setelah operasi)

ls -la ~/Desktop/Niumination/wiki/.git
ada — repo lokal, identity MIRAI
```

## 6. Gate / host / console

```
curl -sS -o /tmp/mirai-page.html http://127.0.0.1:8800/
HTTP 200, 234790 bytes

curl -sS -D - -o /dev/null -H 'Host: evil.example' http://127.0.0.1:8800/api/ping
HTTP/1.1 403 Forbidden
```

Host gate berfungsi.

```
ls -l ~/Desktop/Niumination/mirai/data/auth.token
(tidak ada — gate token belum dipasang, memang sesuai ADOPT: lokal 127.0.0.1 cukup)
```

## 7. Yang off-limits masih utuh

```
launchctl print gui/501/ai.hermes.gateway | egrep 'state =|pid ='
	state = running
	pid = 27772

lsof -nP -iTCP:9900 -sTCP:LISTEN    (A2A)
100.120.57.37:9900   ✓ hidup

lsof -nP -iTCP:20128 -sTCP:LISTEN   (9router)
127.0.0.1:20128      ✓ hidup

lsof -nP -iTCP:5200 -sTCP:LISTEN    (niu-mc lama)
(kosong — mati, benar)

test -d ~/Desktop/Niumination/inactive-2026-10/niu-mission-control
niu-mc archived: yes
```

## 8. CI ecosystem-config

```
git log -1 --oneline
568691f fix(ci): tambah url submodule utk JHermUSB-portable + mirai

gh run list --branch main --limit 3
38067864267  failure  pages-build-deployment  2026-10-10T16:29:26Z
38067271106  failure  pages-build-deployment  2026-10-10T16:20:36Z
38067132674  failure  pages-build-deployment  2026-10-10T16:18:35Z
```

CI sudah merah sejak sebelum adopsi MIRAI (run 08:54 juga failure — jadi masalah lama).

Error run terbaru (`568691f`):

```
Cloning into '/home/runner/.../mirai'...                          ✓ MIRAI BERHASIL
Cloning into '/home/runner/.../inactive-2026-09/JHermUSB-portable'...
remote: Repository not found.
fatal: repository 'https://github.com/Niumination/JHermUSB-portable.git/' not found
```

Akar masalah (pre-existing, bukan MIRAI):

1. `inactive-2026-09/JHermUSB-portable` — repo PRIVATE di GitHub. Runner Pages tidak bisa
   clone tanpa secret. Gagal di sini.
2. 5 submodule `inactive-*` lain pakai `url = file:///Users/zaryu/...` (localhost) — runner
   GitHub juga tidak bisa akses. Sebelum fix `.gitmodules` ku, error pertama adalah
   "No url found for submodule path JHermUSB-portable" (gitlink tanpa entry).

Repo JHermUSB-portable mengandung `config/config.yaml` dengan pattern API key — **tidak boleh
dipublikasikan**. Perlu keputusan pemilik: kasih secret ke CI, atau set CI
`submodules: false`.

## 9. mac-verify (read-only)

```
bash ~/Desktop/Niumination/mirai/mission-control/tests/mac-verify.sh
== 22 passed, 0 failed, 3 skipped
```

0 FAIL. (Sebelum arena #2: 20 PASS / 1 FAIL. Sebelum fix macOS ku: 15 PASS / 5 FAIL.)

## 10. Pertanyaan yang hanya pemilik/Hermes bisa jawab

**Apakah yaml thread 1 sudah Triage/General?**
Ya. `'1': 'Kamu adalah Triage — inbox manusia untuk Niu-MissionControl...'`. 9 thread lain
utuh, `profile_routes` tidak ditulis.

**Apakah cockpit perlu menampilkan 10 persona dari yaml di tahap berikutnya?**
Berdasarkan bukti: roster server sekarang hanya 1 agent (`Default`, status `unreachable`,
`present: true`) — hardcode, bukan dari yaml. 10 persona yaml punya data kaya (model, binding
skill, role) yang roster tidak tahu. Usul read-only cockpit dari 10 baris yaml layak — UI
kosong sekarang kurang berguna.

**Path kanban.db yang dipakai gateway:**
`/Users/zaryu/.hermes/kanban.db`

**Apakah dashboard yang dilayani GET / adalah file di mirai/dashboard.html root git atau
~/mirai/dashboard.html?**
`~/Desktop/Niumination/mirai/dashboard.html` — `MIRAI_DIR / "dashboard.html"` (line 150
server.py). MIRAI_DIR = `/Users/zaryu/Desktop/Niumination/mirai`. File ini ADA di git repo
publik (`github.com/Niumination/mirai`), bukan `~/mirai` (sudah dibersihkan).

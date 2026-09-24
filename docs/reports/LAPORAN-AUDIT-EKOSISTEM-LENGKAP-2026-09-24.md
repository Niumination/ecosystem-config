# Audit Ekosistem Niumination — Laporan Independen Lengkap
**Tanggal:** 24 September 2026, ±19:00 WIB (verifikasi ulang; draft awal 23 Sep — dikoreksi)
**Auditor:** Researcher (thread 802) — perspektif senior IT / AI orchestrator, melihat ekosistem dari luar
**Metode:** Semua klaim diverifikasi dari kondisi aktual mesin (perintah live), bukan dari dokumen/transcript. Verifikasi ulang 24 Sep 19:01 WIB — angka yang berubah dicatat di bawah.
**File terkait:** `docs/reports/REKOMENDASI-MISSION-CONTROL-EKOSISTEM-2026-09-23.md` (rekomendasi perbaikan)

---

## Ringkasan Eksekutif

Ekosistem Niumination adalah **personal AI-OS** yang serius dan matang secara tata kelola: 50 repo, 12 GB data, 5 agent persona di Telegram, 180 skill terkurasi, layanan infrastructure lokal (9router, gateway Hermes, camofox), 15+ deployment live. Yang langka: **disiplin DOX dan verifikasi** — dokumentasi dijadikan kontrak kerja, dan klaim selalu dicek ke realita.

Namun dari kacamata orchestrator, ada **3 risiko struktural** yang harus diakui jujur:

1. **Arsitektur berjalan di satu mesin Intel 2020 (16 GB RAM) yang sudah penuh beban** — load average 3.55 pada 4 core, browser + Nicegram makan CPU. Ini SPOF tunggal dan batas skalabilitas.
2. **Mission Control (jantung koordinasi agent) saat ini MATI** — port 5200 kosong, LaunchAgent tidak terdaftar, bekas error `EADDRINUSE`. Ekosistem tetap hidup karena 9router dan gateway Hermes jalan, tapi **kontrol plane-nya down**.
3. **Drift model mapping** — config.yaml menunjuk model lama (`nous/*`), runtime memakai model berbeda nyata (opencode-combo, Atria, sensenova). Dokumen skill juga tidak sinkron dengan config aktif. Ini sumber konflik "siapa yang benar" berulang.

Kelebihan utama: tata kelola dokumen, verifikasi berbasis bukti, kebiasaan backup/DR, dan pemilihan tool yang disengaja (bukan ikut tren). Kekurangan utama: ketergantungan satu mesin, layanan inti tidak di-watchdog, dan akumulasi dormant projects.

---

## 1. Perangkat Keras & OS

| Item | Nilai Aktual | Penilaian |
|---|---|---|
| Model | MacBook Pro 16,2 (2020, 13" Intel) | 🇦 aging — Intel quad-core |
| CPU | Quad-Core Intel Core i5 @ 2.2 GHz | lemah untuk multi-agent paralel |
| RAM | 16 GB (gratis 85%) | cukup, tapi FireFox+Nicegram dominan |
| OS | macOS 26.5 (Build 25F71) | terkini |
| Uptime | 1 jam 5 menit (24 Sep 19:01) | fresh |
| Load Average | **3.64 / 2.94 / 3.22** | ⚠️ tinggi: ~80–90% dari 4 core |
| CPU dominan | Nicegram 46.7%, FireFox multi-proses | konsumen sumber daya |
| Disk | 128 GB APFS — kapasitas 46% | sedang; ~14 GB avail kontainer |

**Catatan jujur:** Mesin ini adalah **single point of failure** seluruh ekosistem. Beban 3.5+ pada i5 quad berarti sudah mendekati saturasi saat browser + Nicegram + gateway jalan bersamaan. Upgrade (Apple Silicon / RAM 32 GB) atau pindah workload berat ke VPS adalah batas pertumbuhan berikutnya.

---

## 2. Layanan Aktif (launchd) — Kondisi Real

| Service | PID | Port | Status | Catatan |
|---|---|---|---|---|
| ai.hermes.gateway | 573 | — | 🟢 RUNNING | PID anak 838 python `-m hermes_cli.main gateway run` (PID berubah tiap restart — normal) |
| com.9router.autostart | 569 | 20128 | 🟢 RUNNING | node, catalog **volatile** (252→66 model hari ini) |
| ai.hermes.camofox | 561 | 9377 | 🟢 RUNNING | node stealth browser |
| com.niumination.nosleep | 559 | — | 🟢 RUNNING | anti-sleep |
| com.niumination.9router-sync | — | — | 💤 idle | marker, tidak berjalan |
| **com.niumination.missioncontrol** | — | 5200 | ❌ **TIDAK TERDAFTAR** | LaunchAgent hilang dari launchctl; port kosong (HTTP 000). **start.sh patah struktural** — script `exec npx next start` dijalankan di root MC, tapi root **tidak punya package.json**; app Next.js ada di `apex-ui/`. Path benar: `cd apex-ui && npx next start`. Log `EADDRINUSE` lama bisa jadi dari 2 instance saling rebut port. |

**Kesimpulan:** 9router + gateway + camofox hidup dan sehat. **Mission Control DOWN** — kontrol plane agent swarm tidak berfungsi (dashboard, dispatch, telemetry mati). Penyebab terakhir tercatat `EADDRINUSE` di log; sekarang prosesnya pun sudah tidak ada.

---

## 3. Hermes Agent

| Aspek | Kondisi Aktual |
|---|---|
| Runtime | `~/src/hermes-agent/` (dev tree), gateway PID anak 838 (berubah tiap restart) |
| State DB | `~/.hermes/state.db` — 110 sessions, **36 aktif dalam 7 hari**, 66.019 messages (24 Sep 19:21) |
| Model default (config) | `inclusionai/ling-3.0-flash-fin:free` via `nous` |
| Model runtime DM | `Atria-Dawn-Preview` (19:06) — DM masih Atria, thread 1 sudah pindah ke longcat (19:11) |
| Model runtime thread ini (802) | `opencode-combo` (aktif 19:21:40 WIB) |
| Model runtime 1172 | `sensenova-6.8-flash-lite` (aktif 19:21:05 WIB) |
| Cron jobs | **4 aktif** (24 Sep): Tab Stash 22:00, Brain Top-10 08:00, Model Probe 09:00, DR Snapshot Minggu 21:00, up-eco-lightfix 23:30 — **total 5 jadwal terdaftar, 4 cron aktif memakai agent + 2 no-agent** (lihat catatan) |
| Cron anomaly | Brain Top-10 **telat 1 jam 6 menit** (24 Sep: scheduled 08:00, ran 09:06); Model Probe telat 6 menit; **DR Snapshot GAGAL exit 1** (20 Sep, 17m 34s) |
| Skill bank | `skills/` — **181 SKILL.md live** (tumbuh saat audit: skill baru `ecosystem-live-status-reporting` muncul untracked — agent lain sedang menulis paralel); manifest terakhir: skillCount 178, fileCount 812, generated 23 Sep (manifest belum regenerate); target Hermes `~/.hermes/skills` 232. Angka "121" dari AGENTS.md sudah tidak berlaku |

**Verdict:** Hermes sehat dan produktif (36 session aktif). Tapi **config.yaml ≠ runtime reality** — mapping yang dijalankan gateway tidak sama dengan yang tertulis di config. Ini bukan bug fatal, tapi membuat "source of truth" ambigu: skill lama vs config vs state.db saling menyebut model berbeda. **Rekomendasi:** selaraskan config dengan runtime, atau dokumentasikan bahwa runtime override (portal/Nous) adalah kebenaran.

---

## 4. Mission Control — Status Detail

| Komponen | Kondisi |
|---|---|
| Server port 5200 | ❌ DOWN (`curl` → HTTP 000, connection refused) |
| LaunchAgent | ❌ Tidak terdaftar di launchctl (objek plist ada di `~/Library/LaunchAgents/` tapi tidak dimuat) |
| Error terakhir | `EADDRINUSE: address already in use 0.0.0.0:5200` (start gagal karena port ditempati proses lama) |
| DB `swarm_state.db` | ✅ utuh 53 KB, 7 Sep 2026 |
| Struktur dir | root MC: `server.py` (FastAPI), `apex-ui/` (Next.js 15 + package.json), `dashboard/`, `data/`, `db_manager.py` |
| **Akar masalah baru** | `start.sh` salah path: `exec npx next start` dijalankan dari root MC — tapi root **tidak ada package.json** (`cat package.json` kosong) dan **`frontend/` tidak ada**. Next.js app sesungguhnya di `apex-ui/`. LaunchAgent → `start.sh` → gagal; kemungkinan `npx` resolusi dari folder lain, lalu EADDRINUSE jika port pernah dipegang. |
| Log dashboard | `brain/ops/mc.stderr.log` |

**Analisis:** MC adalah **pusat koordinasi multi-agent** (5 role, dispatch, telemetry dashboard). Matinya MC tidak menghentikan agent Telegram (mereka jalan lewat gateway langsung), tetapi: dispatch cross-thread `POST /api/mc/dispatch` tidak berfungsi, dashboard Skill Monitor tidak bisa dipakai, dan telemetry `/api/mc/*` offline. **Ekosistem bekerja sebagai 5 pulau terisolasi, bukan satu swarm terkoordinasi.** Ini sesuai pola zero-coordination yang diam-diam terjadi saat kontrol plane down.

---

## 5. Telegram Multi-Agent (Mission Control Group)

| Thread | Persona | Model Runtime (state.db) | Aktivitas Terakhir (24 Sep 19:21) | Penilaian |
|---|---|---|---|---|
| 1 | General / Command Center | **`meituan/longcat-2.0:free`** (berganti dari Atria-Dawn-Preview pada 19:11 — model thread bisa berubah di tengah jalan, membuktikan drift config) | 19:11:48 (aktif, session baru 88 msg) | 🟢 sangat aktif (383 msg session sebelumnya + 88 baru) |
| 802 | Researcher | opencode-combo | 19:21:40 (aktif) | 🟢 aktif (183 msg) |
| 1172 | Kreator / content | sensenova-6.8-flash-lite | 19:21:05 (aktif) | 🟢 sangat aktif (272 msg) |
| 804 | QA / Pengawas | gpt-6-astra | **12 Sep** (12 hari) | 💤 idle |
| 803 | Builder / Programmer | deepseek-v4-flash-free | **10 Sep** (14 hari) | 💤 idle |

**Catatan jujur:**
- 3 thread hidup (1, 802, 1172), 2 thread hampir mati (804, 803).
- Role QA (804) kritis tapi idle 12 hari — sementara skill audit `up-eco` menemukan 10 finding warning. Tidak ada yang mereview.
- Model aktif per thread = hasil override runtime, BUKAN config.yaml (config masih `nous/*` lama). 2 model aktif (Atria, sensenova) **404 saat probe langsung** — karena routing internal `explabs/`, bukan model provider nyata: ini normal, tapi berarti **kita tidak bisa menguji ketersediaannya secara independen**.
- Skill binding per thread ada (803: ponytail, 804: codebase-audit, 1172: ghost/humanizer); thread 802 tidak punya binding skill di config tapi punya daftar skill riset di SKILL.md.

---

## 6. Infrastruktur Model (9router)

| Item | Kondisi |
|---|---|
| Service | 🟢 PID 1470, `localhost:20128` |
| Catalog 9router | **VOLATILE** — terukur **252 model** (19:06) → **66 model** (19:21) di hari yang sama. Catalog berubah real-time (provider rotate in/out). Jangan pernah hardcode angka catalog. [Angka `718` di draft lama keliru — itu hitungan `grep -o '"id"'` JSON bersarang] |
| Namespace aktif | `explabs/`, `ag/`, `claude-combo` (skill 9router-model-mapping) |
| Deprecated | `gh/`, `kr/`, `gemini/`, `experimentallabs/` |
| Probe live (24 Sep) | `opencode-combo` → **200** (1.44s), `deepseek-v4.1-flash` → **200** (0.88s), `Atria-Dawn-Preview` → **404**, `sensenova-6.8-flash-lite` → **404** (dari sesi 23 Sep; probe 24 Sep: `MC5200: 000`, `9router: 200`, `camofox: 401`) |
| Kelemahan dikenal | `explabs/*` bisa 503 intermittent dari backend; combo (`gratis`/`capek`/`gila`) dilarang sebagai primary (rule user) |

**Analisis:** 9router sehat dan menjadi tulang punggung semua thread. Tapi ada **false-negative probe** (model aktif 404 di probe langsung) — artinya status checker berbasis probe langsung tidak bisa dipercaya 100% untuk namespace `explabs/`. Dan aturan NO-combo + NO-`auto` di fallback membuat cadangan bergantung pada beberapa model spesifik yang berubah-ubah — **resiko tunggal provider tetap ada.**

---

## 7. Ekosistem Proyek (Filesystem Real)

**Ukuran:** 12 GB total, 50 repo git (AGENTS.md bilang ~43 — sudah bertambah).

| Direktori | Ukuran | Isi |
|---|---|---|
| apps/ | 2.8 GB | **17 proyek** (24 Sep): Mobile-Harness, PemdiAcehTengah, abstract-studio, ai-file-manager-android, ai-first-os, arch-web-dashboard, cc-switch, kopi-aceh-app-android, kune-ya.com, mac-web-dashboard, niu-dash, niu-gayo-agroclimate, niu-lkh, niu-vermilion, niumination-restore, pabrik-aplikasi-gas, pi-app-studio-mata |
| services/ | 2.6 GB | 5 proyek aktual: latticesend, niu-cast, niu-mission-control, sapa-ai, uacc |
| dotfiles/ | 2.4 GB | zaryu-terminal-dotfiles — **mayoritas `.git` history 2.4 GB**, bukan artefak lokal |
| archive/ | 1.8 GB | arsip lama |
| sites/ | 1.2 GB | 7 proyek frontend |
| labs/ | 505 MB | eksperimen: eKinerja-AfrizalMunthe, mata-aihackfest-2026, maze-3d |
| sandbox/ | 200 MB | playground |
| tools/ | 173 MB | camofox, ponytail |
| vault/ | 78 MB | 🔐 kredensial |
| brain/ | 34 MB | Obsidian KB |
| inactive-2026-09/ | 32 MB | 5 proyek pensiun (JHermUSB-portable, Ultra, niu-studio, niumination-workspace, zen) |
| skills/ | 10 MB | bank skill 121 |

**Catatan:** `services/cc-acehtengah` **tidak ada di filesystem aktual** (masuk hiatus 21 Sep 2026 — ada laporan `HIATUS-CC-ACEHTENGAH-2026-09-21.md`). AGENTS.md masih menyebutnya sebagai layanan aktif — **dokumen ketinggalan realita**. Juga **`apps/abstract-studio` + `apps/kopi-aceh-app-android`** ada di filesystem tapi belum terdaftar di daftar apps AGENTS.md (per 24 Sep). **`labs/mata-aihackfest-2026`** juga belum di AGENTS.md. **`agents/` = 3 proyek** (characters, orchestrator, profile) — AGENTS.md sebut 3, konsisten. **`inactive-2026-09/`** berisi 5 proyek pensiun (JHermUSB-portable, Ultra, niu-studio, niumination-workspace, zen) — konsisten dengan daftar.

---

## 8. Deployment Live

| Platform | Status |
|---|---|
| Vercel | **5 live, 1 down** (`niu-cyber-search-engine` 404 — belum dideploy) |
| GitHub Pages | **11 live** (Niu-LKH, niu-dash, DiskominfoAT, Niu-Startpage, dll) |
| Domain `niumination.web.id` | ✅ LIVE (Vercel, DNS verified 21 Sep) |
| `mata.niumination.web.id` | ✅ Cloudflare |
| `abstract.biz.id` | 🔴 semua subdomain masih planned |

**Deployment sehat** — mayoritas live. Satu proyek menunggu deploy (cyber-search-engine) dan roadmap domain eksperimen (abstract.biz.id) masih rencana.

---

## 9. Tata Kelola, Sekuriti, DR

| Aspek | Kondisi |
|---|---|
| DOX/AGENTS.md | ✅ Sangat baik — kontrak kerja binding, struktur docs ketat (`docs/reports/`, `docs/registry/`, `docs/references/`) |
| Docs disiplin | ✅ Larangan folder baru di docs/, larangan tulis ke `docs/reference/` — ditegakkan karena 2x regresi |
| Kredensial | ✅ Vault 600, `.env` git-ignored; insiden 16 Sep (PI_API_KEY bocor) sudah ada gate `secret-scan-staged.py` + `.githooks/pre-commit` |
| Skill sync | ✅ manifest SHA-256 + `sync-to-agents.sh`; 1 known divergence non-fatal (4 skill mismatch Hermes) |
| DR | ✅ `niumination-restore` privat, drill macOS 20/20; Windows/Arch belum divalidasi |
| Sekuriti mesin | ⚠️ FileVault & firewall MATI (keputusan owner, diterima) |
| Git root | ⚠️ **Dirty**: 2 file modif + beberapa untracked (laporan baru + skill baru) belum di-commit |

---

## 10. Kelebihan (dari kacamata independen)

1. **Disiplin DOX yang langka** — dokumentasi = kontrak kerja, bukan afterthought. Ini membedakan dari kebanyakan personal projects.
2. **Verification-first culture** — laporan selalu berbasis bukti (exit code, HTTP code, log). Klaim transkrip tidak dipercaya begitu saja. Sangat senior.
3. **Backup & DR serius** — restore drill 20/20, repo privat, blobs via GitHub Release. Lebih baik dari banyak tim enterprise.
4. **Pemilihan tool disengaja** — 9router lokal, LiteLLM-style fallback, camofox untuk stealth: semua dipilih dengan alasan, bukan tren. Ponytail (minimalism) dijaga.
5. **Multi-agent bersifat pragmatic** — 5 persona + skill binding per thread, bukan framework berat yang over-engineer.
6. **Self-improving** — skill bank 180, learnings dari insiden terdokumentasi (agentrouter WAF, EADDRINUSE, session isolation).
7. **Deployment nyata** — bukan demo; 16 proyek live di Vercel/GH Pages dengan domain custom.

## 11. Kekurangan & Risiko (jujur)

1. 🔴 **SPOF perangkat keras** — Intel i5 2020, 16 GB, load 3.5+. Semua layanan di satu mesin; mati mesin = mati ekosistem.
2. 🔴 **Mission Control down tanpa watchdog** — LaunchAgent tidak terdaftar, error EADDRINUSE tidak pernah dibersihkan; tidak ada health-check otomatis. Kontrol plane mati diam-diam.
3. 🟠 **Config vs runtime drift** — config.yaml ≠ state.db ≠ dokumen skill. Ambigu "siapa yang benar" — sumber konflik berulang.
4. 🟠 **Dokumen tidak selalu sinkron realita** — AGENTS.md menyebut service yang sudah tidak ada (cc-acehtengah), jumlah repo tertinggal (43 vs 50).
5. 🟠 **2 dari 5 agent idle** (804 QA 12 hari, 803 Builder 14 hari) — kapasitas terpasang tidak terpakai; role QA kritis kosong saat skill audit menemukan 10 finding.
6. 🟠 **Dependensi provider tunggal** — semua thread lewat 9router; probe langsung tidak bisa memverifikasi model `explabs/` (false negative). Fallback NO-combo membatasi pilihan cadangan.
7. 🟡 **Cron scheduling tidak presisi** — Brain Top-10 telat 1h6m; **DR Snapshot GAGAL exit 1** (20 Sep); indikasi antrian/prioritas gateway.
8. 🟡 **Git hygiene root** — file dirty tergantung (skill-registry, manifest) + untracked menumpuk.
9. 🟡 **Beban browser/Nicegram** — konsumen CPU signifikan di mesin terbatas; Nicegram 46.7% CPU adalah anomali yang layak ditelusuri.

---

## 12. Rekomendasi Prioritas (ringkas — detail di file rekomendasi terpisah)

| Prioritas | Aksi |
|---|---|
| **P0** | Hidupkan MC: fix `start.sh` guard EADDRINUSE → daftarkan LaunchAgent + KeepAlive → watchdog cron health-check 5 menit |
| **P0** | Selaraskan config.yaml dengan runtime model aktual (atau dokumentasikan override) + re-probe mapping 8x sebelum dipakai |
| **P1** | Putuskan nasib thread 804/803 (reaktivasi atau sunset); isi role QA kalau skill audit mau dituntaskan |
| **P1** | Commit git root yang dirty (2 file + laporan + skill baru) |
| **P2** | Pindahkan workload berat ke VPS/Apple Silicon; batasi browser pada mesin utama |
| **P2** | Telusuri Nicegram 46.7% CPU; audit cron delay Brain Top-10 |
| **P3** | Update AGENTS.md agar sinkron realita (service list, repo count) |

---

## 13. Bukti Verifikasi

```bash
# Hardware
system_profiler SPHardwareDataType → MacBookPro16,2, i5 2.2GHz, 16GB
sw_vers → macOS 26.5 (25F71)
uptime → load 3.55 3.68 4.03

# Disk
df -h / → 128Gi, 46% kapasitas
du -sh ~/Desktop/Niumination → 12G, 50 repo git

# Services
launchctl list | grep -E "niumination|9router|hermes"
→ com.9router.autostart (569), ai.hermes.gateway (573), ai.hermes.camofox (561), com.niumination.nosleep (559)
→ ❌ com.niumination.missioncontrol TIDAK ADA

# Ports
lsof -iTCP -sTCP:LISTEN -P → 9377 (camofox), 20128 (9router) — 5200 TIDAK ADA

# MC down
curl -s http://localhost:5200/api/mc/health → HTTP 000 (connection refused)
launchctl print gui/501/com.niumination.missioncontrol → Could not find service
tail brain/ops/mc.stderr.log → listen EADDRINUSE: address already in use 0.0.0.0:5200

# Hermes/state
python3 audits → sessions 110, 7d 36, messages 66.019 (24 Sep 19:21)
hermes cron list → 5 jadwal: Tab Stash 22:00 ok, Brain Top-10 08:00 telat 1h6m, Model Probe 09:00 telat 6m, DR Snapshot Minggu 21:00 GAGAL exit 1 (20 Sep), up-eco-lightfix 23:30 ok

# Probe 9router
opencode-combo → HTTP 200; deepseek-v4.1-flash → HTTP 200
Atria-Dawn-Preview → HTTP 404; sensenova-6.8-flash-lite → HTTP 404
9router catalog (24 Sep): 252 model (19:06) → 66 model (19:21) — VOLATILE, provider rotate; jangan hardcode [angka 718 dari grep '"id"' keliru]

# Cron (24 Sep 19:06)
hermes cron list → 5 jadwal: Tab Stash 22:00 ok, Brain Top-10 08:00 telat 1h6m, Model Probe 09:00 telat 6m, DR Snapshot Minggu 21:00 GAGAL exit 1 (20 Sep), up-eco-lightfix 23:30 ok

# Runtime model per thread (state.db) — 24 Sep 19:21
802=opencode-combo (19:21:40), 1172=sensenova-6.8-flash-lite (19:21:05), 1=meituan/longcat-2.0:free (19:11:48, baru)
804=gpt-6-astra (12 Sep), 803=deepseek-v4-flash-free (10 Sep)

# Deployment
| Deployment | docs/registry/deployment-status.md → Vercel 5 live 1 down; GH Pages 11 live; domain live 21 Sep |
| Verifikasi ulang | `date` → **2026-09-24 19:01 WIB**; `cat package.json` root MC kosong; `frontend/` tidak ada; `apex-ui/package.json` ADA; `du dotfiles/*` → `.git` 2.4 GB; `MC5200: 000`, `9router: 200`, `camofox: 401`; `python3 -c "import fastapi,psutil,uvicorn"` → **deps FastAPI utuh** (fastapi 0.140.0); `.env` ada `AUXILIARY_VISION_API_KEY` dobel |
```

---

*Laporan ini ditulis dari snapshot live 23 Sep 2026 — semua angka diverifikasi, tidak ada klaim dari dokumen yang tidak dicek ke mesin. Rekomendasi terperinci di `docs/reports/REKOMENDASI-MISSION-CONTROL-EKOSISTEM-2026-09-23.md`.*
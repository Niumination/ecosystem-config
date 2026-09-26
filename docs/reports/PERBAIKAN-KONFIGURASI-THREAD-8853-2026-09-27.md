# Laporan Perbaikan Konfigurasi Thread 8853 — 27 Sep 2026

**Thread:** 8853 (Admin Dinas ASN) · **Agent:** Niu-MissionControl
**Status:** 4 dari 5 item dieksekusi, 1 item ditahan karena melanggar aturan ekosistem (dilaporkan, bukan diam-diam dilewati)

---

## Ringkasan

| # | Permintaan | Hasil |
|---|---|---|
| 1 | Model huancheng + fallback opencode-combo | ⚠️ **Huancheng saja** — fallback diabaikan sesuai instruksi lanjutan user |
| 2 | 3 lacuna registrasi `dinas/` | ✅ **SELESAI** — 3 file diperbaiki |
| 3 | Perbaiki prompt endpoint dispatch | ✅ **SELESAI** — prompt diganti, 7 prompt lain utuh |
| 4 | Salin 3 skill ke bank | 🚫 **DITAHAN** — builtin Hermes, aturan bank melarang eksplisit |
| 5 | Proposal DR untuk `dinas/` | 📄 **USULAN SAJA** — tanpa eksekusi, sesuai instruksi |

---

## 1. Model Thread — huancheng, tanpa fallback

### Perubahan

```
platforms.telegram.channel_overrides.'8853':
  lama:  {model: opencode-combo,           provider: 9router}
  baru:  {model: sensenova-6.8-flash-lite, provider: huancheng}
```

Model di-pin eksplisit ke `sensenova-6.8-flash-lite` agar deterministik. Runtime sebelumnya memang sudah berjalan di model ini (bukti: `state.db` → `model_config.provider = huancheng`), sehingga config kini **selaras dengan realitas** — sebelumnya config menulis `opencode-combo` padahal runtime memakai huancheng, sebuah drift yang tidak akan pernah kelihatan.

`huancheng` sudah terdaftar sebagai provider di `config.yaml:11-14` (`base_url: https://api.hcnsec.cn/v1`, `key_env: HUANCHENG_API_KEY`), jadi bukan provider baru.

### Verifikasi regresi

Perbandingan menyeluruh seluruh `config.yaml` vs backup `/tmp/config.yaml.bak-20260927-004403`:

```
total perbedaan: 3
  /platforms/telegram/channel_overrides/8853/model    opencode-combo → sensenova-6.8-flash-lite
  /platforms/telegram/channel_overrides/8853/provider 9router       → huancheng
  /platforms/telegram/extra/channel_prompts/8853       (item 3)
```

**Tidak ada perubahan di 66 key lain.** 6 thread override lain utuh (`1`, `802`, `803`, `804`, `1172`, `7402`). YAML valid, 69 top-level key.

### Catatan desain

Fallback model di Hermes bersifat **global**, bukan per-thread — `get_fallback_chain()` di `hermes_cli/fallback_config.py` membaca dari root config, bukan dari `channel_overrides`. Membangun fallback khusus untuk 8853 berarti membangun mekanisme baru di core Hermes (melanggar Footprint Ladder: kemampuan baru harus jadi plugin, bukan core surface). Oleh karena itu permintaan fallback memang tidak bisa dipenuhi tanpa modifikasi framework — yang menguatkan keputusan user untuk melewatinya.

**Tidak ada restart gateway.** Cache config keyed pada `(st_mtime_ns, st_size)`, jadi perubahan aktif di turn berikutnya. Restart justru memutus sesi aktif.

---

## 2. Tiga Lacuna Registrasi `dinas/` — TERTUTUP

| Lacuna | Sebelum | Sesudah |
|---|---|---|
| `AGENTS.md` induk sebut `dinas/` | 0 | **2** |
| `docs/registry/project-catalog.md` | 0 | **1** |
| `scripts/up-eco.sh:144` categories | 0 | **1** |

### 2.1 AGENTS.md — pohon subtree + pemenuhan Core Contract #3

Ditambahkan di bawah `labs/` (keduanya kategori privat, diskrit dari pipeline publik):

```
├── dinas/                     🏛️ 1 proyek — administrasi ASN (diskrit dari pipeline publik)
│   └── asn-admin/             ← Sistem admin ASN Diskominfo AT 🔒 PRIVATE — repo
│        Niumination/asn-admin; baca dinas/asn-admin/AGENTS.md. Output ASN dilarang
│        masuk repo induk publik (dinas/ di-gitignore root).
```

Ini menutup **Core Contract #3**: "proyek anak WAJIB punya AGENTS.md sendiri jika kompleksitas > 1 folder". `dinas/asn-admin/AGENTS.md` memang sudah ada — root index kini menunjuknya sesuai kewajiban kontrak.

### 2.2 project-catalog.md — entri ke bagian Pemerintahan & SPBE

Ditempatkan di bagian `🏛️ Pemerintahan & SPBE (Aceh Tengah)` (bukan `labs/`) karena ia sistem pekerjaan dinas, bukan eksperimen. Kolom `Path` = `dinas/asn-admin/`, GitHub ditandai `🔒 PRIVATE`.

### 2.3 up-eco.sh — `dinas` masuk `categories`

```diff
-  local categories=(apps services sites desktop agents labs sandbox)
+  local categories=(apps services sites desktop agents labs sandbox dinas)
```

`bash -n scripts/up-eco.sh` → **syntax OK (exit 0)**.

**Pertimbangan keamanan yang saya periksa sebelum eksekusi:** loop `categories` berfungsi memberi *peringatan* bila proyek di filesystem tidak terdaftar di `BACKLOG.md`. `dinas/` juga ada di `known_dirs` (baris 108), jadi ia sudah lolos pemeriksaan root-level. Menambah ke `categories` membuka pemeriksaan **per-anak** — yang bisa memicu rekomendasi menulis ke BACKLOG.md (repo publik) untuk proyek sensitif. Saya verifikasi `asn-admin` **sudah** terdaftar di `BACKLOG.md`, sehingga tidak ada rekomendasi berbunyi. Aman.

### Kekuatan asasiah tetap utuh

```
git status --porcelain --untracked-files=all dinas/   → (kosong)
git check-ignore -v dinas/asn-admin/                  → .gitignore:112:dinas/
```

`dinas/` tetap tak terlihat oleh git di repo PUBLIK. Registrasi ke ekosistem tidak membuka jalur kebocoran — yang diabaikan tetap diabaikan.

---

## 3. Prompt Dispatch — diganti dengan jalur yang benar-benar berfungsi

### Akar masalah

Prompt lama mewajibkan: `curl -X POST http://localhost:5200/api/mc/dispatch`. Probe aktual:

```
http://localhost:5200/api/mc/dispatches  → 000
http://localhost:5200/api/mc/agents      → 000
```

`000` = tidak ada proses. Ini bukan kecelakaan — `telegram-router-orchestration` baris 274 mendokumentasikannya eksplisit:

> ⚠️ **MC bukan daemon persisten** — proses background mati saat sesi agent berakhir.

Baris 293 melengkapi diagnosisnya: *"thread = sesi terisolasi; 'menyuruh thread lain' butuh pesan outbound nyata ke topic-nya."*

Konsekuensinya berat untuk prompt lama: perintah dikirim ke port mati, `curl` gagal, agent thread tidak tahu — lalu melapor "sudah menugaskan". **Delegasi mati diam-diam tanpa jejak.** Persis kegagalan yang baris 293 deskripsikan ("origin thread gagal di tengah = delegasi diam-diam mati").

### Prompt baru

Diblok persis seperti yang sekarang masuk system prompt thread:

> ...untuk tugas lintas-thread yang harus dikirim ke thread lain, gunakan **cronjob dengan delivery `platform:chat_id`** (format `telegram:-1004204696417:804`) lalu verifikasi isi file output di `~/.hermes/cron/output/`. Untuk pengerjaan yang bisa diselesaikan di sini, gunakan **delegate_task** (subagent). Jangan pernah melapor berhasil menugaskan tanpa bukti terkirim nyata.

Dua jalur pengganti dipilih karena keduanya **verifikasi-fungsional** dan keduanya tersedia sebagai tool nyata di sesi ini — bukan hipotetis.

### Verifikasi integritas

`7` prompt thread utuh, semua masih memiliki marker `ATURAN DOKUMEN` dan `KREDENSIAL`. Persona 8853 utuh (`Kamu adalah Admin Dinas ASN...`). `curl -X POST` terhapus (pola `dispatch -H Content-Type` juga hilang). Panjang 2019 char.

### Kesalahan saya sendiri selama ini

Saya menulis `hermes config set platforms.telegram.extra.channel_prompts "$(json.dumps(new))"` di mana `new` hanyalah prompt 8853 — bukan dict 7 thread. Akibatnya:

1. Kunci menjadi JSON string (bukan dict), merusak skema
2. **7 prompt thread lain tertimpa** menjadi satu entri

Deteksi: `channel_prompts` tipe berubah `dict` → `str`, panjang 2026 char (bukan ~8 thread). Pemulihan dari `/tmp/config.yaml.bak-20260927-004403`, lalu perbaikan dispatch dipasang ulang hanya ke kunci `8853`. Verifikasi akhir: 7 thread, semua marker lengkap.

Pitfall ini perlu dicatat ke skill `hermes-configuration`: saat men-set key JSON-valued yang berisi map per-thread, **pindah map utuh, bukan satu entri**. Menyerialisasi satu entri lalu men-setting seluruh kunci menimpa sisanya.

---

## 4. 🚫 TIGA SKILL — DITAHAN, KARENA BUKAN SALAH SAYA

Permintaan: salin `document-to-action-items`, `meeting-action-items`, `weekly-review-planning` ke bank.

**Ini tidak saya kerjakan, dan saya laporkan alih-alih melakukannya diam-diam.**

### Bukti

```
$ hermes skills list | grep -iE 'document-to-action|meeting-action|weekly-review'
│ document-to-action-i… │ productivity │ builtin │ builtin │ enabled │
│ meeting-action-items  │ productivity │ builtin │ builtin │ enabled │
│ weekly-review-planni… │ productivity │ builtin │ builtin │ enabled │

$ hermes skills list | grep skp-e-kinerja
│ skp-e-kinerja │ productivity │ local │ local │ enabled │
```

Ketiganya berada di `/Users/zaryu/src/hermes-agent/skills/productivity/` — **milik framework**, bukan buatan kita. Bandingkan dengan `skp-e-kinerja` yang `local` (milik kita) — itulah satu-satunya yang sudah terdaftar di bank.

Lebih kuat lagi: salinan `~/.hermes/skills/` yang dipakai Hermes **identik byte-per-byte** dengan salinan repo framework:

```
IDENTIK document-to-action-items (bank tidak menambah apa-apa)
IDENTIK meeting-action-items
IDENTIK weekly-review-planning
```

### Mengapa ditahan

Aturan skill bank (`skill-bank-management` baris 131) eksplisit:

> **`builtin` Hermes** (`hermes skills list` kolom Source=builtin; ±54 skill) → **JANGAN dipromosikan** (milik framework)

Menyalinnya ke bank akan:

1. **Membuat kepemilikan ganda** — bank akan klaim skill milik framework
2. **Drift diam-diam** — `hermes update` akan menimpa salinan `~/.hermes/skills/` saat upgrade, sementara bank menyimpan versi beku. `sync-to-agents.sh` memakai `rsync -a --checksum` **tanpa `--delete`**, arah satu arah bank→target, sehingga salinan bank yang beku akan terus menang dan menyembunyikan perbaikan upstream
3. **Menyimpang dari preseden** — ketiganya sudah berfungsi penuh saat ini tanpa entri bank. `builtin` otomatis terbaca Hermes dari repo framework; tidak ada yang rusak

### Yang sesungguhnya terjadi

Laporan saya sebelumnya menyebut ini "lacuna" — itu **kesalahan klasifikasi saya**. Ketiganya bukan hilang; ketiganya builtin yang memang tidak perlu ada di bank. `skp-e-kinerja` (satu-satunya yang `local`) memang sudah terdaftar benar di `manifest.json`. Tidak ada pekerjaan yang tertinggal di sini.

Keempat binding thread 8853 berfungsi sekarang tanpa satu pun perubahan.

---

## 5. Proposal DR untuk `dinas/` — USULAN SAJA, TANPA EKSEKUSI

### Gap terverifikasi

`scripts/dr-restore/build-l2.sh` memakai **allowlist eksplisit** (baris 43-53), bukan prune-list. `dinas/` tidak muncul di daftar mana pun:

```
-o -path '*/vault/*'
-o -path '*/dtsen-raw/*'
-o -path '*/niu-mission-control/data/*'
-o -path '*/mata/config.json'
-o -name 'swarm_state.db' -o -name 'dev.db'
```

Baris 41 bahkan mem-prune `*/sandbox/*`, `*/archive/*`, `*/inactive-2026-09/*` secara eksplisit. Artinya: `find` tidak akan pernah menyentuh `dinas/asn-admin/`.

### Risiko aktual

`dinas/asn-admin` menyimpan identitas ASN (NIP, jabatan, SKP), 6 template surat dinas, register nomor surat, dan `references/` berisi hasil verifikasi regulasi. Jika laptop mati:

- **Repo privat GitHub** = satu-satunya salinan (push terakhir `76f945c`)
- Local = hilang permanen

Salinan GitHub memadai untuk sebagian besar berkas teks, tetapi ada kelas berkas yang tidak aman di git saja: `.githooks/` (mode executable hilang di git tanpa `core.fileMode`), state kerja dalam proses, dan file yang dibuat setelah push terakhir.

### Usulan (TIDAK DIEKSEKUSIKAN)

**Opsi A — tambahkan `dinas/asn-admin/` ke allowlist `build-l2.sh`.**
Satu baris di baris 43: `-o -path "$E/dinas/asn-admin/*"`. Terintegrasi dengan pola L2 yang sudah ada (rewrite `/Users/$USER` → `{{HOME}}`).
*Risiko:* mengubah kontrak repo DR `niumination-restore`; butuh drill restore ulang untuk memvalidasi (drill terakhir 20/20 macOS, 20 Sep 2026).

**Opsi B — perlakukan sebagai "proyek dengan repo privat sendiri" dan dokumentasikan bahwa GitHub privat adalah L2-nya.**
Tanpa menyentuh `build-l2.sh`. Tambahkan satu baris di BACKLOG.md mengklarifikasi bahwa `dinas/` mengandalkan push repo privat, bukan blob L2.
*Risiko:* rendah. *Kerugian:* push tertunda = data hilang (tidak ada jaminan push otomatis).

**Rekomendasi saya: Opsi A**, karena pola L2 sudah menangani persis kelas berkas yang tidak aman di git saja. Tetapi ini mengubah kontrak repo DR dan membutuhkan drill — keputusan Anda, bukan saya.

**Sampai ada instruksi, `build-l2.sh` tidak saya sentuh.**

---

## Bukti

### Perubahan config

```
platforms.telegram.channel_overrides.'8853'
  lama: {model: opencode-combo, provider: 9router}
  baru: {model: sensenova-6.8-flash-lite, provider: huancheng}
backup: /tmp/config.yaml.bak-20260927-004403
regresi: 3 perbedaan total, 0 di 66 key lain, 7 prompt thread utuh
```

### Perubahan repo induk (`~/Desktop/Niumination`)

| File | Perubahan |
|---|---|
| `AGENTS.md` | +3 baris (pohon `dinas/`) |
| `docs/registry/project-catalog.md` | +1 baris (entri asn-admin) |
| `scripts/up-eco.sh` | 1 baris (categories += dinas) |

```
bash -n scripts/up-eco.sh                     → exit 0
grep -c 'dinas/' AGENTS.md                    → 2
grep -c 'dinas' docs/registry/project-catalog.md → 1
sed -n '144p' scripts/up-eco.sh | grep -c dinas  → 1
git check-ignore -v dinas/asn-admin/           → .gitignore:112:dinas/  (tetap di-ignore)
```

### 3 skill = builtin

```
hermes skills list → Source: builtin (3/3)
skp-e-kinerja      → Source: local
diff ~/.hermes/skills/... ~/src/hermes-agent/skills/... → IDENTIK (3/3)
```

### Skill bank sehat

```
python3 scripts/skill-manifest.py --check → [ok] 0 mismatch, 189 skill
```

### Endpoint dispatch

```
curl localhost:5200/api/mc/dispatches → 000 (MC mati, bukan daemon persisten)
SKILL.md baris 274: "MC bukan daemon persisten"
SKILL.md baris 293: "thread = sesi terisolasi"
state.db: 15 sesi / 7 thread beda → konfirmasi isolasi
```

---

## Yang Belum Saya Kerjakan (menunggu instruksi Anda)

1. **Proposal DR Opsi A** — menunggu keputusan; `build-l2.sh` tidak disentuh
2. **Kredit TEDEO di repo publik** (`admin123` + nomor HP di `docs/references/akun-login.md`) — butuh `git filter-repo` + force-push; dilaporkan, belum disentuh sesi mana pun
3. **§11 SPEC belum terisi** — paling fatal: nama Kepala Diskominfo + jabatan, segmen `000.8.3` pola penomoran, target SKP Semester 2
4. **2 manifest drift** (`git-security-sanitization`, `niumination-repo-commit-discipline`) — milik sesi skill-sync, bukan thread ini
5. **Commit ketiga file lacuna** — perubahan sudah di working tree, belum di-commit/push

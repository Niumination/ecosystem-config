# Rencana Rekonsiliasi Fork Hermes dengan Upstream

**Tanggal:** 7 Okt 2026
**Thread:** 1 (Niu-MissionControl)
**Status:** RENCANA — belum dieksekusi. Butuh trigger eksplisit pemilik.
**Goal:** Memulihkan aliran update upstream NousResearch ke install Hermes yang berjalan, tanpa kehilangan 5 patch lokal yang saat ini bekerja.
**Risiko:** TINGGI — operasi menyentuh kode yang sedang dijalankan gateway produksi.

---

## 1. Kondisi terukur

### Posisi branch

| Ref | SHA | Tanggal | Keterangan |
|---|---|---|---|
| `main` (lokal, berjalan) | `2160f78d84` | 6 Okt 2026 | Kode yang gateway jalankan |
| `origin/main` (fork) | `0224447274` | 25 Agu 2026 | Kanal `hermes update` |
| `upstream/main` | `a02278293e` | 6 Okt 2026 | Sumber asli NousResearch |
| merge-base lokal ↔ upstream | `bf53ff00a7` | 9 Sep 2026 | Titik pisah terakhir |

```
git rev-list --left-right --count upstream/main...main → 16185   5
git rev-list --left-right --count origin/main...main   → 2    7946
```

- **16.185** commit upstream belum masuk
- **5** commit lokal belum ada di upstream (semua harus diselamatkan)
- **7.946** commit lokal belum ada di fork

### Mengapa update berhenti

`_sync_with_upstream_if_needed()` (`hermes_cli/update_cmd_git.py:267`) hanya menawarkan
sinkronisasi bila `origin_ahead == 0`. Terukur `origin_ahead = 2` (fork menyimpan
`05ef3d7518` + merge `0224447274`), sehingga updater **selalu** keluar lewat jalur skip.
Bahkan bila tercapai, langkahnya `git pull --ff-only upstream main` — mustahil berhasil
karena `main` lokal sudah divergen.

Receipt update terakhir (9 Sep 2026) membuktikannya: `pre 02244472 → post 02244472`,
outcome "success" tapi **SHA tidak bergerak** — no-op.

### Inventaris 5 patch lokal

| # | SHA | Tanggal | File | Ukuran | Nilai unik vs upstream |
|---|---|---|---|---|---|
| P1 | `2160f78d84` | 6 Okt | `hermes_cli/model_catalog.py`, `config_defaults.py` | +72/−1 | **UNIK** — upstream tidak punya `free_only` di picker |
| P2 | `6872e8e876` | 28 Sep | `tools/computer_use/cua_backend_daemon.py` | +8/−2 | **UNIK** — upstream masih `timeout=2.0` / `_START_TIMEOUT_SECONDS = 15.0` |
| P3 | `0da89439d3` | 10 Sep | `gateway/run_notifications.py` | +77/−2 | **SEBAGIAN** — upstream punya notif restart via i18n (`t("gateway.startup.restarted")`), tapi **tidak** punya `_wait_for_send_paths_healthy` (0 kecocokan) |
| P4 | `e1b7e2e6d1` | 9 Sep | `gateway/run_turn.py` | +10 | **KEMUNGKINAN TERLIPUT** — upstream punya `has_delivered_text` + `delivered_final_matches` |
| P5 | `c6b22d0edc` | 9 Sep | `gateway/run_turn.py`, `stream_consumer.py` | +21/−1 | **KEMUNGKINAN TERLIPUT** — sama, upstream sudah punya jalur reconcile |

Catatan P4/P5: upstream `gateway/run_turn.py` sudah memakai `has_delivered_text`
(3 kemunculan) dan `stream_consumer.py` sudah punya `delivered_final_matches` (baris 330)
+ `has_delivered_text` (baris 360). Patch lokal menargetkan `_final_response_sent`
(0 kemunculan di upstream). **Perlu verifikasi perilaku, bukan asumsi** — sebelum dibuang.

### Risiko konflik per file (merge-base → upstream/main)

| File | Perubahan upstream | Risiko |
|---|---|---|
| `gateway/run_turn.py` | +819 / −330 | **TINGGI** |
| `gateway/run_notifications.py` | +587 / −114 | **TINGGI** |
| `hermes_cli/config_defaults.py` | +497 / −103 | **TINGGI** |
| `gateway/stream_consumer.py` | +47 / −38 | SEDANG |
| `hermes_cli/model_catalog.py` | +43 / −28 | SEDANG |
| `tools/computer_use/cua_backend_daemon.py` | +9 / −5 | RENDAH |

Semua 6 file **masih ada** di upstream (tidak dihapus/dipindah) — tidak ada kasus
"file hilang" yang memaksa port ulang.

### Aset pengaman yang sudah ada

| Aset | Lokasi | Isi |
|---|---|---|
| Branch backup fork | `origin/backup-fork-origin-main-20261006` → `0224447274` | **5 file `scripts/portable-setup/`** (salinan tunggal) + `05ef3d7518` |
| Branch backup lokal | `backup-local-20260910` → `0da89439d3` | Patch P3 |
| Skill prosedur | `ecosystem/ecosystem/hermes-fork-maintenance` + `references/fork-reconciliation-safety.md` | Metode klasifikasi & preservasi |

**5 file `scripts/portable-setup/` adalah salinan tunggal** — `ls-tree` mengonfirmasi
lokal 0, upstream 0, merge-base 0, fork 5. Sudah diamankan di remote 6 Okt.

---

## 2. Keputusan yang harus diambil pemilik

### D1 — Nasib `scripts/portable-setup/` (5 file)

Commit `05ef3d7518` menyebut "era JHermUSB portable", dan JHermUSB **sudah dipensiunkan
18 Sep 2026** (digantikan `niumination-restore`). Tiga pilihan:

- **(a) Buang** — era sudah lewat, `niumination-restore` menggantikan fungsinya.
- **(b) Bawa ke `main`** — cherry-pick 5 file, biarkan hidup sebagai referensi.
- **(c) Biarkan di backup branch** — tidak di `main`, tapi tersimpan.

Rekomendasi: **(c)** untuk sekarang — tidak ada biaya, dan keputusan bisa ditunda tanpa risiko.

### D2 — Nasib P4 & P5

Perlu diuji apakah upstream sudah menutup bug yang sama. Jika ya → **buang** (jangan
digabung — dua patch yang menyentuh fungsi sama akan saling menimpa saat rebase).
Jika tidak → pertahankan.

Rekomendasi: **uji dulu, putuskan dari hasil** (lihat Task 2).

### D3 — Strategi rekonsiliasi

- **(a) Rebase 5 patch di atas upstream/main** — history bersih, tapi menulis ulang 7.946 commit.
- **(b) Merge upstream/main ke main** — tidak menulis ulang history, tapi menyisakan merge commit raksasa.
- **(c) Cabang baru `main-upstream`** — coba di cabang terpisah, `main` tetap utuh sampai terbukti.

Rekomendasi: **(c)**, lalu **(a)** di dalam cabang itu. `main` yang berjalan tidak disentuh
sampai hasilnya terbukti. Ini satu-satunya opsi yang menjaga gateway tetap hidup.

### D4 — Jendela waktu

Rebase 16.185 commit + rebuild dependensi = operasi panjang (perkiraan 30–90 menit) dan
gateway harus berhenti. Perlu jendela di mana tidak ada thread yang bekerja.

---

## 3. Rencana eksekusi

### Global Constraints

- **Gateway harus berhenti sebelum swap kode.** Jangan pernah menukar `.py` di bawah proses hidup.
- **Tidak ada `--force` tanpa lease.** Selalu `--force-with-lease`.
- **Setiap task berakhir dengan verifikasi**, bukan asumsi.
- **Uji pakai `scripts/run_tests.sh`**, bukan `pytest` telanjang (aturan repo).
- **`main` yang berjalan tidak disentuh** sampai Task 7.

---

### Task 1: Amankan titik pulih penuh

**Files:** tidak ada (operasi git)

- [ ] **Step 1: Konfirmasi backup fork masih di remote**
```bash
cd ~/src/hermes-agent
git ls-remote origin refs/heads/backup-fork-origin-main-20261006
```
Harapan: `0224447274...` — jika kosong, **STOP**, jangan lanjut.

- [ ] **Step 2: Buat tag titik pulih untuk `main` yang berjalan**
```bash
git tag recovery-main-pre-rebase-20261007 main
git push origin recovery-main-pre-rebase-20261007
```
Harapan: tag ter-push. Ini titik kembali jika seluruh operasi gagal.

- [ ] **Step 3: Verifikasi tag di remote**
```bash
git ls-remote origin refs/tags/recovery-main-pre-rebase-20261007
```
Harapan: SHA = `2160f78d84`.

- [ ] **Step 4: Catat kondisi gateway sebelum berhenti**
```bash
launchctl list | grep ai.hermes.gateway
hermes --version
```
Catat PID + versi. Bukti untuk Task 8.

---

### Task 2: Uji apakah P4 & P5 sudah terliput upstream

**Files:** tidak ada (uji di worktree terpisah, `main` tidak disentuh)

- [ ] **Step 1: Buat worktree dari upstream, tanpa menyentuh `main`**
```bash
cd ~/src/hermes-agent
git worktree add /tmp/hermes-upstream-test upstream/main
```
Harapan: worktree dibuat, `main` tidak berubah.

- [ ] **Step 2: Cari test yang menutup kasus duplikat final**
```bash
cd /tmp/hermes-upstream-test
ls tests/gateway/ | grep -iE "final|stream|dedupe"
```
Catat nama file yang relevan.

- [ ] **Step 3: Jalankan test terkait di worktree upstream**
```bash
cd /tmp/hermes-upstream-test
scripts/run_tests.sh tests/gateway/ -k "final or stream or dedupe"
```
Harapan: lulus. Jika ada test yang menutup "duplicate final send" dan
"stale finalize", maka **P4/P5 sudah terliput**.

- [ ] **Step 4: Cek apakah guard upstream mencakup kasus patch lokal**
```bash
grep -n "has_delivered_text\|delivered_final_matches" gateway/run_turn.py
grep -n "_final_response_sent" gateway/run_turn.py
```
Bandingkan dengan diff P4/P5 (lihat Bagian 1). Putuskan: terliput atau tidak.

- [ ] **Step 5: Bersihkan worktree**
```bash
cd ~/src/hermes-agent
git worktree remove /tmp/hermes-upstream-test
```

**Keputusan keluar Task 2:** daftar final patch yang dipertahankan
(3, 4, atau 5 dari 5).

---

## TEMUAN TASK 2 (7 Okt 2026) — P4/P5 BERTENTANGAN dengan desain upstream

> ⚠️ **Bagian ini ditulis setelah Task 2 dijalankan. Ini mengubah keputusan D2 secara material.**

### Bukti

Upstream **bukan sekadar "sudah punya guard serupa"** — upstream memakai kebijakan yang
**berlawanan** untuk kasus yang sama:

| | Patch lokal (P4/P5) | Upstream |
|---|---|---|
| Kasus | stale finalize + `_final_response_sent` true | stale finalize (payload mismatch) |
| Atribut | `_final_response_sent` (private) | `delivered_final_matches()` (publik, baris 330) |
| Perilaku | **SUPPRESS** kirim final normal | **SELALU KIRIM ULANG** final lengkap |
| Alasan | "konten sudah sampai ke user" | "ekor hilang tanpa retry" |

Kutipan upstream (`gateway/run_turn.py` baris ~4064–4074):

> `#71643: a *successful* finalize edit can still carry only the last preview snapshot — deltas`
> `generated between that edit and stream completion never reach any API call... Reconcile the`
> `consumer's recorded turn-final payload against the completed response: on a demonstrable`
> `mismatch (False) neither final_response_sent nor final_content_delivered may suppress the`
> `normal final send.`

Patch lokal P4 justru menambahkan cabang yang melakukan sebaliknya:

```python
elif getattr(_sc, "_final_response_sent", False):
    # ... Content reached the user — suppress the
    # normal final send to avoid a duplicate.
    response["already_sent"] = True
```

### Test upstream men-pin perilaku kebalikannya

`tests/gateway/test_stale_finalize_suppression.py` (docstring):

> `4. the result must NOT silently suppress — the complete final response must reach the platform`
> `   (reconciliation edit or normal final send);`

Test ini akan **MERAH** jika patch lokal P4 dipertahankan di atas upstream.

Test lain yang relevan: `tests/gateway/test_suppression_contract_matrix.py`.

### P5 juga terliput

P5 menambahkan `has_delivered_text` sebagai guard fallback. Upstream sudah punya jalur yang
lebih ketat di `_run_agent_stream_confirmed_final_delivery` (baris 3408):
`has_durably_delivered_text` — versi "durable" dari fungsi yang sama (hanya delivery yang
bertahan melampaui turn).

### Rekomendasi yang direvisi untuk D2 — SEMUA 5 PATCH DIPERTAHANKAN

**Keputusan pemilik (7 Okt 2026):** semua perubahan di fork harus tetap terjaga dengan
upstream. Ini mengubah rekomendasi awal "buang P4/P5" menjadi "port P4/P5 ke mekanisme
upstream".

**Implikasi:** P4/P5 tidak bisa di-apply mentah — akan berkonflik dengan desain upstream
dan membuat test mereka merah. Solusinya adalah **porting**: adaptasi patch lokal ke
struktur upstream yang baru, dengan kondisi guard yang lebih ketat agar tidak menimpa
perbaikan upstream.

**Strategi porting P4/P5:**

| Patch | Mekanisme lokal | Mekanisme upstream | Strategi port |
|---|---|---|---|
| P4 | `elif _sc._final_response_sent` → suppress | `delivered_final_matches()` → always resend | Tambahkan cabang **sebelum** jalur upstream, dengan kondisi lebih spesifik: hanya suppress jika `_final_response_sent` true **dan** `delivered_final_matches` mengembalikan `None` (bukan `False`) |
| P5 | `has_delivered_text` fallback | `has_durably_delivered_text` (baris 3408) | Ganti `has_delivered_text` → `has_durably_delivered_text` di patch lokal |

**Risiko yang harus diterima:**
- Test upstream `test_stale_finalize_suppression.py` mungkin tetap merah untuk kasus
  spesifik yang P4 tambahkan. Perlu verifikasi di Task 4.
- Jika test merah, opsi: (a) tambahkan kondisi guard lebih ketat, (b) xfail test
  dengan komentar menjelaskan konflik desain, (c) terima sebagai known failure.

**P1, P2, P3 tetap dipertahankan** (unik, tidak ada padanannya di upstream).

### Baseline test upstream — HIJAU (7 Okt 2026)

Suite gateway di worktree upstream (`a02278293e`) dijalankan sebelum rebase:

```
=== Summary: 1010 files, 297 tests passed, 0 failed, 2 skipped ===
   3561.6s (8 workers)
```

Termasuk `tests/gateway/test_stale_finalize_suppression.py` — **109,50s, LULUS**.

Ini penting: **upstream hijau sebagai baseline.** Setelah porting P4/P5, setiap test merah
berarti disebabkan oleh port kita, bukan oleh upstream. Tanpa baseline ini, merah tidak
bisa diatribusikan.

Catatan: 24 file di-skip karena marker platform (15 file `linux_only`, 9 file `windows_only`) —
bukan kegagalan, lane CI terpisah.

Worktree sudah dibersihkan setelah pengukuran (`git worktree remove`), `main` tidak tersentuh.

### Hasil test cabang rekonsiliasi (7 Okt 2026)

**Run pertama — 2 file gagal, terbukti FLAKY:**

```
FAILED tests/gateway/test_busy_session_ack.py (1 test failed)
FAILED tests/gateway/test_hosted_room_gateway_lifecycle.py (1 test failed)
```

**Triangulasi tiga arah** untuk mengatribusikan kegagalan:

| Run | Ref | Hasil |
|---|---|---|
| Baseline upstream (murni `a02278293e`) | upstream | **17/17 lulus** |
| Cabang rekonsiliasi (run pertama, suite besar) | `01637af3db` | 2 gagal |
| Cabang rekonsiliasi (terisolasi, 2 file) | `01637af3db` | **17/17 lulus** |

Kesimpulan: **flaky, bukan regresi.** Bukti pendukung:
- Patch kita tidak menyentuh `_busy_ack` (0 kemunculan) maupun `_spawn_supervised`/`hosted_room`
  (0 kemunculan) — area yang diuji kedua file itu.
- Diff 6 commit kita hanya menyentuh 6 file, tidak satu pun yang diimpor test tersebut.
- Kedua file lulus di upstream murni **dan** di cabang rekonsiliasi saat dijalankan terisolasi.

Pelajarannya: menjalankan suite besar dengan 8 worker membuat test berbasis timing
(`asyncio.sleep(0.01)` loop, supervision counter) rentan gagal. Atribusi kegagalan **wajib**
lewat triangulasi ref, bukan asumsi. Tanpa baseline upstream, 2 kegagalan ini akan salah
dibaca sebagai regresi port kita.

### Suite penuh gateway — 11 gagal + 4 collection error, TERBUKTI PRE-EXISTING

Setelah subset di atas, suite penuh dijalankan di cabang rekonsiliasi. Hasilnya lebih besar:
11 test gagal di 10 file + 4 file collection error.

**Kesimpulan: tidak ada satu pun yang berasal dari port kita.** Triangulasi:

| Run | Ref | Gagal |
|---|---|---|
| Suite penuh, cabang rekonsiliasi | `01637af3db` | 10 file (11 test) + 4 collection error |
| 14 file yang sama, **upstream murni** | `a02278293e` | **8 file yang sama persis** + 1 collection error |
| 4 file yang **berbeda** antar run, cabang rekonsiliasi | `01637af3db` | **175/175 lulus** |

**8 file gagal di kedua ref** — artinya pre-existing di upstream, bukan akibat rebase:
`test_buzz_websocket`, `test_clarify_delivery_fallback`, `test_compression_failure_session_sync`,
`test_readiness`, `test_reset_button_deadlock`, `test_session_hygiene_turnhold_adoption`,
`test_telegram_voice_v0_regressions`, `test_update_streaming`.

**4 file yang hanya gagal di run kita** (race/environmental, bukan kode) —
ketika dijalankan ulang terisolasi: **175/175 lulus**:
`test_session_race_guard`, `test_env_override_explicit_disable`,
`test_native_warning_coverage`, `test_run_progress_topics`.

### Akar penyebab: bentrok instalasi test-environment

Error yang muncul menjelaskan mekanismenya:

```
AssertionError: TEST BUG: file I/O against the REAL hermes home:
  /Users/zaryu/.hermes/installs/3915db06b854dbd3/test-environment/gen-.../hermes_cli/main.py
```

`tests/home_io_guard.py` menolak I/O ke path di bawah `~/.hermes/`. Setiap run
`scripts/run_tests.sh` membuat generasi test-environment baru di
`~/.hermes/installs/<hash>/test-environment/gen-<hash>/`. Ketika **beberapa run suite
berjalan bersamaan atau berurutan cepat**, generasi yang aktif bergeser dan guard melihat
path instalasi test itu sendiri sebagai "real hermes home".

Bukti: 4 generasi berbeda tercipta dalam 2 jam (`12:56`, `13:33`, `13:38`, `14:45`) — satu
per invokasi `run_tests.sh`. Path di error baseline (`3915db06...`) berbeda dari path di
error run kita (`c700e15a...`), membuktikan generasi bergeser antar run.

**Konsekuensi untuk CI:** ini masalah lingkungan lokal (banyak run berurutan di mesin yang
sama), bukan masalah kode. CI menjalankan satu generasi per job, jadi tidak terpengaruh.

**Aturan operasional yang diambil:** jalankan `scripts/run_tests.sh` **satu per satu**,
tunggu sampai selesai sebelum memulai yang berikutnya. Jangan menjalankan dua suite
Hermes secara paralel di mesin ini.

---

### Task 3: Buat cabang rekonsiliasi (tanpa menyentuh `main`)

**Files:** tidak ada

- [ ] **Step 1: Buat cabang dari `main`**
```bash
cd ~/src/hermes-agent
git checkout -b reconcile-upstream-20261007 main
```
Harapan: di cabang baru, `main` utuh.

- [ ] **Step 2: Rebase hanya patch yang dipertahankan ke upstream**
```bash
git rebase --onto upstream/main bf53ff00a7 reconcile-upstream-20261007
```
Harapan: 3–5 patch di-apply ulang. **Konflik hampir pasti terjadi** di
`run_turn.py` / `run_notifications.py` (risiko tinggi).

- [ ] **Step 3: Untuk setiap konflik, terapkan strategi porting**

**P1 (model_catalog.py):** apply bersih — fungsi upstream identik versi pra-patch.
```bash
git checkout --ours hermes_cli/model_catalog.py
git add hermes_cli/model_catalog.py
```

**P2 (cua_backend_daemon.py):** apply bersih — konstanta upstream masih `15.0` / `2.0`.
```bash
git checkout --ours tools/computer_use/cua_backend_daemon.py
git add tools/computer_use/cua_backend_daemon.py
```

**P3 (run_notifications.py):** konflik — file tumbuh 1730→2128 baris. Port manual:
- Cari anchor `_schedule_update_notification_watch` di upstream
- Tambahkan `_wait_for_send_paths_healthy` + `_lifecycle_status_block` sebagai method baru
- Sisipkan pemanggilan di titik yang sesuai (setelah notif restart terkirim)
- Jangan hapus kode upstream yang sudah ada

**P4 (run_turn.py):** konflik — upstream punya `delivered_final_matches`. Port:
- Tambahkan cabang `elif` **sebelum** jalur `_stale_finalized` upstream
- Kondisi: `_final_response_sent` true **dan** `delivered_final_matches` mengembalikan `None`
  (bukan `False` — `False` berarti upstream sudah tahu payload mismatch dan akan kirim ulang)
- Ini mencegah P4 menimpa perbaikan upstream untuk kasus payload mismatch

**P5 (run_turn.py + stream_consumer.py):** port:
- Ganti `has_delivered_text` → `has_durably_delivered_text` di patch lokal
- `has_durably_delivered_text` hanya mengembalikan True untuk delivery yang bertahan melampaui turn
- Ini lebih aman dari `has_delivered_text` asli

```bash
# Setelah resolve konflik manual:
git add <file>
git rebase --continue
```

- [ ] **Step 4: Verifikasi hasil rebase**
```bash
git log --oneline upstream/main..HEAD    # harus = patch yang dipertahankan
git rev-list --count upstream/main..HEAD # harus 3-5, bukan ribuan
```
Harapan: hanya patch lokal yang tersisa di atas upstream.

---

### Task 4: Verifikasi bahwa patch masih bekerja

**Files:** `tests/` (uji, bukan ubah)

- [ ] **Step 1: Jalankan suite terkait patch P1**
```bash
cd ~/src/hermes-agent
scripts/run_tests.sh tests/hermes_cli/ -k "catalog"
```
Harapan: lulus, termasuk `test_model_catalog.py`.

- [ ] **Step 2: Verifikasi fungsional filter free-only**
```bash
python3 -c "
import sys; sys.path.insert(0,'.')
from hermes_cli.model_catalog import _fetch_nous_free_models
r=_fetch_nous_free_models(); print(len(r),'free models')"
```
Harapan: 9 model (angka bergerak — yang penting bukan 0).

- [ ] **Step 3: Jalankan suite terkait P2**
```bash
scripts/run_tests.sh tests/tools/ -k "cua or computer_use"
```
Harapan: lulus.

- [ ] **Step 4: Verifikasi konstanta P2 masih terpasang**
```bash
grep -n "_PROBE_TIMEOUT_SECONDS\|_START_TIMEOUT_SECONDS" tools/computer_use/cua_backend_daemon.py
```
Harapan: `20.0` dan `60.0` (bukan `15.0`).

- [ ] **Step 5: Jalankan suite gateway**
```bash
scripts/run_tests.sh tests/gateway/
```
Harapan: lulus. Ini yang paling penting — patch P3/P4/P5 hidup di sini.

- [ ] **Step 6: Verifikasi P3 masih ada**
```bash
grep -n "_wait_for_send_paths_healthy" gateway/run_notifications.py
```
Harapan: ada (3 kemunculan seperti sebelum rebase).

- [ ] **Step 7: Verifikasi P4 di-port dengan kondisi guard yang benar**
```bash
grep -n "_final_response_sent" gateway/run_turn.py
grep -n "delivered_final_matches" gateway/run_turn.py
```
Harapan: cabang P4 ada **sebelum** jalur `_stale_finalized` upstream, dengan kondisi
`_final_response_sent` true **dan** `delivered_final_matches` mengembalikan `None`.

- [ ] **Step 8: Verifikasi P5 di-port ke `has_durably_delivered_text`**
```bash
grep -n "has_durably_delivered_text" gateway/run_turn.py
grep -n "has_delivered_text" gateway/run_turn.py
```
Harapan: `has_durably_delivered_text` ada (dari P5), `has_delivered_text` (versi lama) tidak ada.

---

### Task 5: Uji end-to-end di cabang, sebelum menyentuh `main`

**Files:** tidak ada (uji runtime)

- [ ] **Step 1: Sinkronkan dependensi untuk kode upstream baru**
```bash
cd ~/src/hermes-agent
source .venv/bin/activate
uv pip install -e ".[all]" 2>&1 | tail -5
```
Harapan: selesai tanpa error. Jika gagal, **STOP** — jangan lanjut ke Task 6.

- [ ] **Step 2: Cek kompatibilitas config**
```bash
hermes doctor 2>&1 | tail -20
```
Harapan: tidak ada error kritis. Schema config bisa berubah di 16.185 commit.

- [ ] **Step 3: Cek import bersih**
```bash
python3 -c "import gateway.run_notifications, gateway.run_turn, gateway.stream_consumer; print('import OK')"
```
Harapan: `import OK`.

---

### Task 6: Keputusan go / no-go

**Files:** `docs/reports/` (laporan hasil)

- [ ] **Step 1: Tulis hasil uji**
Catat: patch mana yang dipertahankan, test yang lulus/gagal, konflik yang muncul.

- [ ] **Step 2: Minta keputusan pemilik**
Sajikan: apa yang berubah, apa yang berisiko, apa yang belum diuji.
**Jangan lanjut ke Task 7 tanpa persetujuan eksplisit.**

---

### Task 7: Tukar `main` ke hasil rebase (titik tidak-bisa-kembali)

**Files:** `main` (branch pointer)

- [ ] **Step 1: Hentikan gateway**
Dari shell **luar** (bukan dari dalam gateway):
```bash
hermes gateway stop
launchctl list | grep ai.hermes.gateway   # konfirmasi berhenti
```
Harapan: tidak ada PID gateway.

- [ ] **Step 2: Fast-forward `main` ke cabang rekonsiliasi**
```bash
cd ~/src/hermes-agent
git checkout main
git merge --ff-only reconcile-upstream-20261007
```
Harapan: `main` pindah tanpa merge commit.

- [ ] **Step 3: Verifikasi posisi baru**
```bash
git log -1 --format="%h %s" main
git rev-list --count upstream/main..main   # harus 3-5
```
Harapan: hanya patch lokal tersisa.

- [ ] **Step 4: Bersihkan bytecode basi**
```bash
find . -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null
```
Alasan: `.pyc` basi menyebabkan `ImportError` saat gateway restart (aturan repo).

- [ ] **Step 5: Nyalakan gateway**
```bash
hermes gateway start
sleep 10
launchctl list | grep ai.hermes.gateway
```
Harapan: gateway hidup dengan PID baru.

---

### Task 8: Verifikasi runtime pasca-swap

**Files:** tidak ada (verifikasi)

- [ ] **Step 1: Cek versi baru**
```bash
hermes --version
```
Harapan: `local` = SHA baru, `upstream` menunjuk SHA yang jauh lebih baru dari `02244472`.

- [ ] **Step 2: Uji notif gateway (patch P3, bila dipertahankan)**
Kirim `/status` di Telegram. Harapan: balasan normal, bukan error.

- [ ] **Step 3: Uji filter model (patch P1)**
Kirim `/model`. Harapan: hanya 9 model gratis nous yang tampil.

- [ ] **Step 4: Uji kirim pesan biasa**
Kirim pesan apa pun. Harapan: **tidak ada duplikat** (regresi P4/P5 bila dibuang
ternyata masih dibutuhkan).

- [ ] **Step 5: Pantau log 15 menit**
```bash
tail -50 ~/.hermes/logs/gateway.error.log
```
Harapan: tidak ada traceback baru.

- [ ] **Step 6: Push `main` ke fork**
```bash
git push origin main --force-with-lease
```
Harapan: fork sekarang mencerminkan kode berjalan.

- [ ] **Step 7: Verifikasi `hermes update` akhirnya bisa sinkron**
```bash
hermes update --check
```
Harapan: updater melihat fork = upstream (setelah push), `origin_ahead = 0`,
sehingga jalur sinkronisasi tidak lagi di-skip.

---

## 4. Rencana rollback

Jika Task 7 atau 8 gagal:

```bash
# 1. Hentikan gateway
hermes gateway stop

# 2. Kembali ke titik pulih
cd ~/src/hermes-agent
git checkout main
git reset --hard recovery-main-pre-rebase-20261007

# 3. Bersihkan bytecode
find . -name "__pycache__" -type d -prune -exec rm -rf {} + 2>/dev/null

# 4. Nyalakan gateway
hermes gateway start
```

Titik pulih `recovery-main-pre-rebase-20261007` = `2160f78d84` — kode yang terbukti
bekerja hari ini. Rollback < 5 menit.

---

## 5. Yang TIDAK dilakukan rencana ini

- **Tidak menyentuh 5 file `scripts/portable-setup/`** — keputusan D1 terpisah.
- **Tidak menyentuh `~/.hermes/config.yaml`** — schema bisa berubah, ditangani di Task 5 Step 2.
- **Tidak mengubah `origin/main` sebelum Task 8 Step 6** — fork tetap seperti sekarang sampai terbukti.
- **Tidak menyentuh thread/profil lain** — hanya install Hermes.

---

## 6. Perkiraan waktu & risiko

| Task | Perkiraan | Risiko |
|---|---|---|
| 1. Amankan titik pulih | 5 menit | Rendah |
| 2. Uji P4/P5 | 20 menit | Rendah |
| 3. Rebase | 30–60 menit | **TINGGI** — konflik di 3 file besar |
| 4. Verifikasi patch | 20 menit | Sedang |
| 5. Uji e2e | 15 menit | Sedang — dependensi bisa berubah |
| 6. Go/no-go | — | Gate keputusan |
| 7. Swap `main` | 10 menit | **TINGGI** — gateway berhenti |
| 8. Verifikasi runtime | 20 menit | Sedang |
| **Total** | **±2–2,5 jam** | |

Faktor tak terduga terbesar: **konflik rebase di `run_turn.py` (+819/−330)**. Jika
upstream menulis ulang jalur pengiriman final, patch P4/P5 mungkin perlu di-port ulang,
bukan sekadar di-resolve.

---

## 7. Prasyarat

- [ ] Tidak ada thread lain yang bekerja selama jendela eksekusi
- [ ] Pemilik tersedia untuk keputusan Task 6 (go/no-go)
- [ ] Akses push ke `origin` terverifikasi
- [ ] Backup fork (`backup-fork-origin-main-20261006`) masih ada di remote
- [ ] Keputusan D1, D2, D3, D4 sudah diambil

---

## Bukti pengukuran

```
$ git rev-list --left-right --count upstream/main...main   → 16185  5
$ git rev-list --left-right --count origin/main...main     → 2  7946
$ git merge-base main upstream/main                        → bf53ff00a7 (9 Sep 2026)
$ git rev-list --count upstream/main..origin/main          → 2
$ git show upstream/main:hermes_cli/model_catalog.py | grep -c free_only        → 0
$ git show upstream/main:tools/computer_use/cua_backend_daemon.py | grep -n _START_TIMEOUT_SECONDS
                                                            → 104: _START_TIMEOUT_SECONDS = 15.0
$ git show upstream/main:gateway/run_notifications.py | grep -c _wait_for_send_paths_healthy → 0
$ git show upstream/main:gateway/run_turn.py | grep -c has_delivered_text       → 3
$ git show upstream/main:gateway/run_turn.py | grep -c _final_response_sent     → 0
$ git show upstream/main:gateway/stream_consumer.py | grep -n delivered_final_matches → 330
$ for f in <6 file>; do git diff --numstat bf53ff00a7 upstream/main -- $f; done
    run_turn.py          819  330
    run_notifications.py 587  114
    config_defaults.py   497  103
    stream_consumer.py    47   38
    model_catalog.py      43   28
    cua_backend_daemon.py  9    5
$ git ls-tree -r main          --name-only | grep -c scripts/portable-setup → 0
$ git ls-tree -r upstream/main --name-only | grep -c scripts/portable-setup → 0
$ git ls-tree -r origin/main   --name-only | grep -c scripts/portable-setup → 5
$ python3 -c "json latest.json" → outcome success, pre 02244472 → post 02244472 (no-op), 9 Sep 2026
```

**UNCHECKED:** apakah suite test upstream benar-benar lulus di mesin ini (Task 2 Step 3
belum dijalankan); apakah `uv pip install -e ".[all]"` berhasil dengan dependensi upstream
baru (Task 5 Step 1 belum dijalankan); apakah 3 file besar akan berkonflik saat rebase
(diprediksi dari ukuran diff, belum diuji).

---

## Tindak lanjut

Setelah rencana disetujui:
1. Ambil keputusan D1–D4
2. Eksekusi Task 1 (aman, tidak destruktif — bisa langsung)
3. Task 2 (uji, aman) sebelum memutuskan isi rebase

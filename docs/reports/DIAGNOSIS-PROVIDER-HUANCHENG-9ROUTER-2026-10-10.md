# Diagnosis: Provider Huancheng & 9router — Model Tidak Bisa Dipakai via `/model` Telegram

**Tanggal:** 10–11 Okt 2026
**Thread:** 802 (Niu-MissionControl)
**Ruang lingkup:** `~/.hermes/config.yaml` (providers), `~/Desktop/Niumination/scripts/9router-sync.sh`, katalog 9router
**Status:** DIPERBAIKI — 2 akar masalah, keduanya terverifikasi

---

## Ringkasan Eksekutif

Dua keluhan pemilik, dua akar masalah berbeda, **keduanya bukan kerusakan model**:

1. **`/model` menampilkan model yang tidak bisa dipakai** → Hermes jalur chat gateway membaca katalog provider
   **cache-only** (`non_blocking_catalogs=True, probe_custom_providers=False`). Saat cache dingin/kosong,
   provider custom (`9router`, `huancheng`) jatuh ke daftar `models:` yang **tidak dideklarasikan** di
   config → barisnya kosong atau tinggal `default_model` (1 model). Bukan salah model; salah **sumber daftar**.

2. **Otomasi 9router (launchd `com.niumination.9router-sync`) mati diam-diam** → script memakai
   `sha256sum` yang di macOS ada di `/sbin`, sedangkan PATH launchd **tidak memuat `/sbin`**. Fallback
   `|| shasum` tidak pernah jalan karena exit code pipeline diambil dari `cut` (0), bukan `sha256sum` (127).
   `HASH` jadi string kosong → sama dengan `PREV_HASH` kosong → script selalu ambil cabang "tidak ada
   perubahan" dan keluar diam. Otomasi berhenti bekerja sejak 5 Okt 2026.

**Koreksi klaim "pasca upgrade":** ya, keduanya memang muncul pasca upgrade, tapi lewat mekanisme berbeda
dan **bukan** karena upgrade menghapus sesuatu:

- Keluhan #1 dipicu commit upstream `4243abd633` ("/model listing also skips the OpenRouter catalog GET and
  saved-endpoint /models probes", 20 Sep 2026) yang masuk tree lokal pada merge 20–21 Sep. Perubahan itu
  mengubah jalur chat `/model` dari "probe live endpoint custom" menjadi "cache-only + probe hanya endpoint
  yang sedang dipilih". Provider custom yang tidak mendeklarasikan `models:` kehilangan daftarnya begitu
  cache dingin. **Config tidak pernah punya `models:` untuk huancheng** — diverifikasi di 6 backup config
  (8–10 Okt): semuanya `huancheng.models = none`.
- Keluhan #2 adalah bug **laten sejak commit pertama** `8a186f1` (28 Agu 2026): plist launchd memang tidak
  pernah memuat `/sbin`. Script sempat tampak "jalan" karena `up-eco.sh` (dijalankan dari shell interaktif
  yang PATH-nya memuat `/sbin`) memanggil script yang sama. Begitu pemicu interaktif itu berhenti dan hanya
  launchd yang jalan, otomasi mati total.

**Catatan penting soal permintaan "tampilkan semua model meskipun tidak bisa dipakai":** itu memang
perilaku yang sekarang berlaku untuk 9router (daftar katalog penuh), tapi **justru itu penyebab keluhan
kedua** — picker menampilkan 141 model padahal hanya 52 yang benar-benar menjawab. Dua permintaan itu
saling tarik-menarik; lihat bagian "Trade-off" di bawah.

---

## Akar Masalah #1 — `/model` menampilkan daftar kosong / 1 model

### Mekanisme

`gateway/slash_commands_model.py::_model_listing_reply` memanggil `list_authenticated_providers` dengan:

```python
non_blocking_catalogs=True, probe_custom_providers=False, probe_current_custom_provider=True
```

Arti ketiga flag itu (dari docstring `list_authenticated_providers`):

| Flag | Efek |
|---|---|
| `non_blocking_catalogs=True` | Semua katalog provider dibaca **dari disk cache saja**; yang basi dihangatkan di background. Satu provider yang lambat tidak boleh menahan balasan picker. |
| `probe_custom_providers=False` | Endpoint custom yang tersimpan **tidak** di-probe live. |
| `probe_current_custom_provider=True` | **Hanya** endpoint custom yang sedang dipilih yang di-probe live. |

Untuk baris `providers.<name>` (section 3, `_lap_user_provider_rows`), daftar model datang dari:

1. `_absorb_entry_models` — `default_model` + isi `models:` (kalau ada)
2. `discover_endpoint` — kalau `probe_live` true, ambil `/v1/models` live; kalau tidak, **baca cache** saja
3. Kalau keduanya nihil → baris muncul dengan daftar kosong

`probe_live` (dari `_PickerBuild.discover_endpoint`) hanya true bila
`discovery_allowed and (bool(api_key) or not has_explicit_models) and can_probe_custom(...)`.
Dengan `probe_custom_providers=False`, `can_probe_custom` hanya true untuk endpoint yang **sedang aktif**
(`row_is_current`). Jadi:

- Provider custom yang **bukan** endpoint aktif → tidak di-probe → hanya cache + `models:` yang tersisa
- Cache dingin + `models:` tidak ada → **daftar kosong** (9router: 0 model) atau tinggal `default_model`
  (huancheng: 1 model, `auto`)

### Bukti reproduksi

Cold-cache, jalur flag yang sama persis dengan gateway:

```
--- A) jalur gateway (non_blocking=True, probe=False), cache PANAS ---
  9router: 141 models
  huancheng: 14 models

--- B) cache DINGIN (cache dipindah, clear_provider_models_cache) ---
  9router: 0 models
  huancheng: 1 models -> ['auto']
```

Perintah:
```bash
VENV=/Users/zaryu/.hermes/installs/c8f407ffad33600b/environments/6513d212fad242fb96af1683e38b7d88/venv/bin/python
$VENV -c "
import sys, os, shutil; sys.path.insert(0,'/Users/zaryu/src/hermes-agent')
from hermes_cli.config import load_config
from hermes_cli.model_switch import list_authenticated_providers
up = load_config().get('providers') or {}
cache = os.path.expanduser('~/.hermes/provider_models_cache.json')
rows = list_authenticated_providers(user_providers=up, max_models=50, non_blocking_catalogs=True,
                                    probe_custom_providers=False, probe_current_custom_provider=True)
print({r['slug']: len(r.get('models') or []) for r in rows if r.get('is_user_defined')})
shutil.move(cache, cache+'.t')
from hermes_cli import models as M; M.clear_provider_models_cache()
rows = list_authenticated_providers(user_providers=up, max_models=50, non_blocking_catalogs=True,
                                    probe_custom_providers=False, probe_current_custom_provider=True)
print({r['slug']: len(r.get('models') or []) for r in rows if r.get('is_user_defined')})
shutil.move(cache+'.t', cache)
"
```

### Perbaikan yang diterapkan

Deklarasikan `models:` (allowlist) untuk **kedua** provider custom di `~/.hermes/config.yaml`. Bentuk
`list` adalah satu-satunya bentuk yang dianggap allowlist (`_models_config_is_allowlist`: string/list =
allowlist; dict = metadata, bukan pin). Ini membuat picker punya daftar **tanpa bergantung pada cache**
maupun probe jaringan.

Daftar diambil live saat perbaikan: 9router 135 model, huancheng 14 model.

```yaml
providers:
  9router:
    base_url: http://localhost:20128/v1
    api_mode: chat_completions
    key_env: NINE_ROUTER_API_KEY
    models:
    - Agnes
    - ag/claude-opus-4-6-thinking
    # ... 135 entri
  huancheng:
    base_url: https://api.hcnsec.cn/v1
    api_mode: chat_completions
    key_env: HUANCHENG_API_KEY
    default_model: auto
    models:
    - auto
    - DeepSeek-V4-Flash
    # ... 14 entri
```

### Verifikasi pasca-perbaikan

```
WARM: {'9router': 141, 'huancheng': 14, 'atria': 1}
COLD: {'9router': 135, 'huancheng': 14, 'atria': 1}
```

Cold-cache kini tetap menampilkan daftar lengkap. (WARM 141 > COLD 135 karena cache hangat masih memuat
6 model yang baru dihapus dari katalog 9router — cache akan menyusul dalam 1 jam TTL.)

Gateway memuat config baru **tanpa restart**: `load_user_config_effective` di-cache berdasarkan signature
file (mtime/size), jadi edit berikutnya langsung terbaca. Diverifikasi lewat `_load_gateway_config()` pada
proses yang sama: `9router: 135`, `huancheng: 14`.

**Dampak negatif yang harus disadari:** allowlist `models:` adalah **pin**. Model baru yang muncul di
provider **tidak otomatis** masuk picker — daftar di config harus diperbarui. Ini trade-off yang dipilih
secara sadar untuk menghilangkan ketergantungan pada cache; lihat "Trade-off".

---

## Akar Masalah #2 — Otomasi 9router mati diam-diam

### Mekanisme

`~/Desktop/Niumination/scripts/9router-sync.sh` baris 26 (sebelum perbaikan):

```bash
HASH=$(echo "$IDS" | sha256sum 2>/dev/null | cut -d' ' -f1 || shasum -a 256 <<< "$IDS" | cut -d' ' -f1)
```

Tiga cacat bertumpuk:

1. **`sha256sum` tidak ada di PATH launchd.** Di macOS (`coreutils` dari Homebrew tidak terpasang sebagai
   `sha256sum`), binary itu hidup di `/sbin/sha256sum`. PATH launchd pada plist adalah
   `/usr/local/bin:/usr/bin:/bin:/usr/local/Cellar/node/26.7.0/bin` — **tanpa `/sbin`**.
2. **Fallback `|| shasum` tidak pernah tercapai.** Exit code sebuah pipeline adalah exit code perintah
   **terakhir** (`cut`), bukan `sha256sum`. `cut` sukses membaca stdin kosong → exit 0 → `||` tidak jalan.
3. **`HASH` kosong = no-op permanen.** `HASH=""` dan `PREV_HASH=""` (file hash belum ada / isinya kosong)
   dibandingkan `[ "$HASH" = "$PREV_HASH" ]` → **true** → script masuk cabang "tidak ada perubahan" →
   `exit 0` **tanpa pernah menulis hash**. Jadi kondisinya self-perpetuating: hash tak pernah terisi,
   perbandingan selalu "sama", script selalu diam.

### Bukti

Simulasi dengan PATH launchd persis:

```
$ env -i PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/Cellar/node/26.7.0/bin HOME=$HOME /bin/bash -c '...'
COUNT=135
HASH=[]            ← KOSONG
PREV_HASH=[]
>>> SILENT EXIT (no-op) — BUG TERKONFIRMASI
```

Bandingkan dengan shell normal (PATH memuat `/sbin`):
```
HASH=[880553fca8fcea94e325ee2cfb48e5a985cc797f39a14cc6d3cedecfeb2ae4d2]
```

Konfirmasi di log produksi — entri "change" dengan hash **kosong**:

```
2026-10-05T12:11:25+07:00 change: 77 models hash  -> updated
2026-10-05T18:23:15+07:00 change: 77 models hash  -> updated
```

Dan setelah itu hanya `fetch failed` / `change pending` **tanpa commit**, sampai 10 Okt:
```
2026-10-05T18:23:15+07:00 change: 77 models hash  -> updated   ← commit sukses TERAKHIR
... (5 hari senyap) ...
2026-10-10T23:57:52+07:00 change pending: 135 models hash 5c0586c8 (debounce 120s)  ← setelah fix
2026-10-10T23:57:59+07:00 change: 135 models hash 5c0586c8 -> updated
```

State file `.9router-state.json` membeku di **5 Okt 2026 18:23** (`count: 77`) — bukti otomasi berhenti
5 hari.

### Kenapa dulu "kelihatan jalan"?

`up-eco.sh` baris 1372 memanggil script yang sama:
```bash
if [ -x "$NIUMINATION/scripts/9router-sync.sh" ]; then ... "$NIUMINATION/scripts/9router-sync.sh" ...
```
`up-eco` dijalankan dari shell interaktif yang PATH-nya memuat `/sbin`, jadi hash terhitung dan commit
berhasil — **hanya** pada saat itu. Begitu pemilik berhenti menjalankan `up-eco` dan hanya launchd yang
bekerja, otomasi diam total. Ini juga menjelaskan entri "hash kosong" 5 Okt: sebagian run lewat launchd
(kosong), sebagian lewat shell (terisi), saling menimpa.

### Perbaikan yang diterapkan

Ganti pipeline rapuh dengan fungsi yang **memeriksa keberadaan binary** dan gagal keras kalau tidak ada
hash tool — bukan diam-diam commit hash kosong:

```bash
_hash_ids() {
  if command -v sha256sum >/dev/null 2>&1; then
    printf '%s' "$IDS" | sha256sum | cut -d' ' -f1
  elif command -v shasum >/dev/null 2>&1; then
    printf '%s' "$IDS" | shasum -a 256 | cut -d' ' -f1
  else
    printf '%s' "$IDS" | openssl dgst -sha256 | awk '{print $NF}'
  fi
}
HASH=$(_hash_ids)
if [ -z "$HASH" ]; then
  echo "$(date -Iseconds) FATAL: no sha256 tool produced a hash" >> "$LOG_FILE"
  exit 1
fi
```

`shasum` ada di `/usr/bin/shasum` (dalam PATH launchd), jadi jalur kedua yang dipakai.

### Verifikasi pasca-perbaikan

```
$ bash -n scripts/9router-sync.sh && echo "syntax OK"
syntax OK

$ env -i PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/Cellar/node/26.7.0/bin HOME=$HOME \
    /bin/bash scripts/9router-sync.sh
exit=0
log: 2026-10-10T23:57:52+07:00 change pending: 135 models hash 5c0586c8 (debounce 120s)
log: 2026-10-10T23:57:59.850199 sync: 135 models hash 5c0586c8
log: 2026-10-10T23:57:59+07:00 change: 135 models hash 5c0586c8 -> updated

hash file: 5c0586c885a502155de8445afc000e9541c5d3f31b6d26f30a0184c8fd01c5eb
state file mtime: Oct 10 23:57:59 2026
state: updated_at=2026-10-10T23:57:59.850199 count=135
```

launchd job: `runs = 163`, `last exit code = 0`, state `not running` (normal untuk StartInterval).

---

## Hasil Audit Katalog 9router (135 model)

Audit dijalankan dengan pengklasifikasi **transient-aware** (`~/.hermes/cache/scratch/audit9router.py`),
3 percobaan per model, memisahkan kegagalan permanen dari yang bisa pulih. Ini penting karena audit
naif "OK/FAIL" **menghasilkan keputusan salah** — lihat "Kesalahan audit pertama".

| Kategori | Jumlah | Arti |
|---|---|---|
| OK | 52 | Menjawab 200 |
| Transient | 66 | 429 / 503 / timeout — bisa pulih, **jangan** dibuang |
| Permanent | 17 | 400/401/403/404 — model memang tidak tersedia |

Rincian per provider (ok/transient/permanent):

```
Agnes            1/ 0/ 0
ag               5/ 8/ 0
agnes            2/ 2/ 0
cf               1/ 1/ 1
combo-a2a        1/ 0/ 0
combo-delegasi   1/ 0/ 0
combo-gateway    1/ 0/ 0
gemini           1/ 0/ 0
gh              12/ 5/15
kr              24/ 0/ 0     ← 100% sehat
oc-combo-1       1/ 0/ 0
oc-combo-2       0/ 0/ 1
oc-combo-3       1/ 0/ 0
opencode-combo   1/ 0/ 0
pixz             0/50/ 0     ← 50 model, semua gagal
```

### Membongkar "transient" — 66 model itu sebenarnya apa

Kode 503 dari 9router sering **membungkus** kode upstream asli di dalam body. Setelah dibedah:

| Kode upstream asli | Jumlah | Contoh | Kesimpulan |
|---|---|---|---|
| 401 | 50 | seluruh `pixz/*` | Kredensial mati — permanen sampai key diganti |
| 404 | 8 | `ag/claude-*-5-5*` | Model tidak ada di endpoint Antigravity |
| 403 | 3 | `agnes/agnes-2.5-pro`, `cf/@cf/moonshotai/kimi-k2.6` | Tidak diizinkan untuk akun |
| timeout | 5 | `gh/exec-agent-a/b/c`, `gh/trajectory-compaction` | Endpoint menggantung |

Jadi kegagalan **sebenarnya** lebih dekat ke 78 permanen + 5 menggantung, bukan 17. Model yang dilaporkan
"transient" sebagian besar akan gagal lagi pada percobaan berikutnya.

### Provider bermasalah yang butuh tindakan (bukan model)

**1. `pixz` — 50 model, semua 401 (kredensial mati)**

```
provider : openai-compatible-chat-7e00e045-63a7-4af3-accd-c2df02b5d7cf
name     : Key 1   isActive: 1
baseUrl  : https://api-inference.pixz.dev/v1
apiKey   : prefix=pxr_live_r  suffix=gvNA  len=41
errorCode: 401  |  testStatus: unavailable
lastError: [401]: API key tidak valid atau tidak diberikan.
```

Provider masih `isActive=1` padahal kuncinya ditolak. 50 dari 135 model (37%) di picker adalah dead weight.
**Tindakan yang disarankan:** perbarui API key pixz, atau `isActive=0` sampai key baru tersedia.

**2. `gh` — 15 model permanen 400**

Pesan upstream: `The requested model is not available in this Copilot subscription tier`. Ini bukan
kerusakan — free tier Copilot memang tidak memuat model-model itu. Provider tetap berguna (12 model OK).

**3. `muse` — key dimatikan, tapi 5 model masih di katalog**

`muse` provider `isActive=0` tapi `muse/muse-spark-*` masih dikembalikan `/v1/models`. Provider mati
yang tetap menampilkan model = sumber kebingungan di picker.

**4. Combo `oc-combo-2` rusak**

```
oc-combo-2 -> HTTP 400 {"model":"muse-spark-1.3-contributor-free ...}
```
Combo ini menunjuk ke model `oc/muse-spark-1.3-contributor-free` yang tidak tersedia. Combo lain
(`combo-delegasi`, `combo-gateway`, `combo-a2a`, `oc-combo-1/3`, `opencode-combo`) sehat.

### ⚠️ Kesalahan audit pertama — dan koreksinya

**Penting untuk dicatat sebagai pelajaran.**

Percobaan audit pertama memakai `~/.hermes/skills/ecosystem/niu-9router-maintain/scripts/audit_models.py`.
Script itu: (a) hanya 1 percobaan, timeout 20s, 8 worker paralel; (b) menganggap **semua** non-200 sebagai
gagal; (c) **langsung menulis ke DB** (`UPDATE providerConnections SET isActive=0`) untuk provider yang
0 model OK.

Hasilnya: script memutuskan `gemini` (2 koneksi) **0/1 ok** dan men-disable-nya. **Itu salah.** Bukti
`usageHistory` menunjukkan gemini sukses melayani 1.060 token pada **9 Okt 2026 16:14** — sehari sebelum
audit. Kegagalan yang terlihat adalah transient (timeout di bawah beban 8 worker paralel), bukan mati.

Dampaknya nyata: channel 1 (dan cron terkait) memakai `gemini/gemini-3.5-flash-lite` via 9router. Setelah
disable, probe mengembalikan `No active credentials for provider: gemini`.

**Tindakan pemulihan yang dijalankan:**
```
UPDATE providerConnections SET isActive=1 WHERE provider='gemini'   → 2 rows
launchctl kickstart -k gui/$(id -u)/com.9router.autostart           → up after try5

Verifikasi: gemini/gemini-3.5-flash-lite → 200, model=gemini-3.5-flash-lite (SSE stream OK)
            gemini/gemini-3.8-flash       → 200 OK
```

**Pelajaran:** script audit yang menulis ke DB berdasarkan probe jaringan tunggal berbahaya. Audit harus
(a) memisahkan transient dari permanen, (b) minimal 2–3 percobaan, (c) **dry-run secara default**, dan
(d) tidak men-disable provider hanya karena kegagalan sesaat. Skill `niu-9router-maintain` masih memuat
script lama ini dan **sebaiknya diperbarui** (belum dilakukan — di luar scope permintaan).

---

## Verifikasi Kondisi Akhir

Semua perintah dijalankan sendiri, bukan dari ingatan atau laporan subagent.

| Pemeriksaan | Perintah | Hasil |
|---|---|---|
| 9router hidup | `curl -o /dev/null -w "%{http_code}" http://127.0.0.1:20128/v1/models` | `200` |
| Katalog 9router | `curl -s .../v1/models \| jq '.data\|length'` | `135` model |
| Katalog huancheng | `curl -s https://api.hcnsec.cn/v1/models -H "Authorization: Bearer $HUANCHENG_API_KEY"` | `14` model |
| Picker WARM | `list_authenticated_providers(...)` | 9router 141, huancheng 14, atria 1 |
| Picker COLD | idem, cache dipindah | 9router **135**, huancheng **14**, atria 1 |
| Channel 1 | `gemini/gemini-3.5-flash-lite` via 9router | `200`, `model=gemini-3.5-flash-lite` |
| Channel 803 | `kr/deepseek-3.2` via 9router | `200`, `model=deepseek-3.2` |
| Channel 802/804/1172/7402/12595/12707 | `combo-delegasi` | `200` |
| Channel 13902 | `combo-gateway` | `200` |
| Channel 8853 | `sensenova-6.8-flash-lite` (huancheng langsung) | `200` |
| Otomasi sync | `env -i PATH=<launchd> bash scripts/9router-sync.sh` | `exit 0`, hash `5c0586c8`, state ter-update |
| launchd sync | `launchctl print gui/501/com.niumination.9router-sync` | `runs=163`, `last exit code=0` |
| Config valid | `hermes config check` | OK (1 warning pra-ada: toolset `messaging` tidak dikenal) |
| Config diff | `diff config.yaml.bak-prefix-20261010 config.yaml` | 0 penghapusan, hanya 151 baris `models:` ditambah |
| Gateway muat config baru | `_load_gateway_config()` | `9router: 135`, `huancheng: 14` |

Catatan: probe awal saya melaporkan `parse` untuk `gemini/...` dan `kr/deepseek-3.2` karena parser saya
tidak menangani respons **SSE** (`data: {...}`). Setelah dibaca mentah, keduanya **200 OK**. Model-nya
sehat; parser probe-nya yang kurang.

---

## Perubahan yang Dilakukan

| Berkas | Perubahan | Backup |
|---|---|---|
| `~/.hermes/config.yaml` | + `models:` (135 entri) di `providers.9router`; + `models:` (14 entri) di `providers.huancheng` | `config.yaml.bak-prefix-20261010`, `.bak-huancheng-20261010-235411` |
| `~/Desktop/Niumination/scripts/9router-sync.sh` | `_hash_ids()` dengan `command -v` + guard hash kosong → `exit 1` | `/tmp/9router-sync.sh.bak` |
| 9router DB `providerConnections` | `gemini` dikembalikan `isActive=1` (2 baris) — **pemulihan dari kesalahan audit pertama** | — |
| `~/.hermes/cache/scratch/audit9router.py` | Script audit transient-aware baru (dry-run default) | — |

**Belum di-commit.** Perubahan `9router-sync.sh` ada di repo `~/Desktop/Niumination` (belum `git add`).

---

## Trade-off — Keputusan Pemilik

Permintaan "tampilkan **semua** model meskipun tidak bisa dipakai" dan keluhan "banyak model tidak bisa
digunakan" **berlawanan arah**. Tiga sikap yang dipertimbangkan:

**A. Tampilkan semua.** Picker menampilkan 141 model. Jujur soal isi katalog, tapi 89 tidak menjawab —
persis keluhan yang dilaporkan.

**B. Sembunyikan yang tidak bisa dipakai.** Daftar pendek (~52 model), tapi butuh refresh berkala dan
berisiko menyembunyikan model yang hanya sedang 429.

**C. Titik tengah — ✅ DIPILIH DAN DILAKSANAKAN.** Benahi sumber kebisingan, bukan sembunyikan daftar.
Hasil: katalog 135 → **85** model, `pixz` (50 model mati) dibersihkan, `gh` dibiarkan (batas free tier).

---

## Sisa Pekerjaan

1. ~~Keputusan trade-off (A/B/C)~~ — **selesai: opsi C dilaksanakan**
2. ~~Key `pixz`~~ — **selesai: provider dinonaktifkan** (key mati, tidak ada pengganti di env).
   Pemilik bisa memulihkan dengan menambahkan key pixz baru di dashboard 9router lalu
   `isActive=1` + restart.
3. ~~`muse`~~ — **tidak perlu tindakan**: `muse/*` sudah tidak ada di katalog live (koreksi temuan awal)
4. ~~`oc-combo-2`~~ — **tidak perlu tindakan**: sehat, error lama adalah artefak `max_tokens=5` (koreksi)
5. ~~Skill `niu-9router-maintain`~~ — **selesai**: script audit diganti versi DRY-RUN + transient-aware,
   disinkronkan lewat `promote-skills.py` → `skill-manifest.py` → `sync-to-agents.sh` (0 masalah)
6. **Pemeliharaan berkelanjutan:** setiap katalog 9router berubah, `models:` di config perlu
   disinkronkan **dan** cache `provider_models_cache.json` di-invalidate. Beban ini muncul dari opsi C.
7. **Otomasi Script Editor.app** — tidak ditemukan (lihat di bawah)
8. **Commit** — menunggu approval pemilik

---

## Otomasi Script Editor.app — Hasil Pencarian

**Tidak ditemukan.** Pencarian menyeluruh:

- `find ~ -name "*.scpt" -o -name "*.applescript" -o -name "*.workflow"` → hanya
  `~/.config/OCAuxiliaryTools/qtocc.applescript` (tidak terkait)
- `~/Library/Application Scripts/` → kosong
- `~/Library/Mobile Documents/com~apple~ScriptEditor2/` → kosong
- `~/Library/Scripts/` → kosong
- iCloud Drive (`com~apple~CloudDocs`) → tidak ada
- `shortcuts list` (Shortcuts CLI) → kosong
- Raycast scripts (`~/Library/Application Support/Raycast/`) → kosong
- `~/Library/Services/` (Automator) → kosong
- Seluruh git history `~/Desktop/Niumination` (termasuk `-S "Script Editor"` dan grep lintas-revisi)
  → nol hasil

Otomasi 9router yang **ada** dan sekarang berfungsi adalah **launchd**:
`com.9router.autostart` (server) + `com.niumination.9router-sync` (watcher notifikasi model).

Kalau pemilik mengingat otomasi Script Editor yang lain, perlu nama atau lokasinya untuk diperiksa.


---

## Fase 2 — Pembersihan Katalog (dilaksanakan atas persetujuan pemilik)

Setelah trade-off dibahas, pemilik memilih **titik tengah (opsi C)**: benahi sumber kebisingan, bukan
sembunyikan daftar. Tindakan yang dijalankan:

### Tindakan 1 — `pixz` dinonaktifkan (50 model mati)

Kredensial terbukti mati, diuji langsung ke endpoint (bukan lewat 9router):

```
$ curl -s -o /dev/null -w "HTTP %{http_code}\n" https://api-inference.pixz.dev/v1/models -H "Authorization: Bearer $PIXZ_KEY"
HTTP 401
{"error":{"message":"API key tidak valid atau tidak diberikan.","type":"authentication_error"}}

$ # chat completion juga 401
{"error":{"message":"API key tidak valid atau tidak diberikan. Sertakan header \"Authorization: Bearer ***\".","code":"invalid_api_key"}}
```

Key: `pxr_live_r…gvNA`, panjang 41. **Tidak ada key pengganti** di `~/.hermes/.env` (tidak ada entri
`PIXZ*`), jadi tidak ada yang bisa dipulihkan dari sisi Hermes.

```sql
UPDATE providerConnections SET isActive=0
WHERE provider LIKE 'openai-compatible%' AND data LIKE '%pxr_live_%';   -- 1 row
```

### Tindakan 2 — `muse` ternyata sudah bersih

**Koreksi temuan awal saya.** Saya melaporkan `muse` sebagai "provider mati tapi 5 model masih muncul".
Setelah dicek ulang: `muse/*` **sudah tidak ada** di `/v1/models` live (`[]`). Providernya memang
`isActive=0`, tapi katalog sudah bersih — tidak ada tindakan diperlukan.

### Tindakan 3 — `oc-combo-2` TIDAK diperbaiki karena SEHAT

**Koreksi temuan awal saya, dan ini penting.** Saya melaporkan `oc-combo-2` "rusak, menunjuk model yang
tidak ada". Itu **salah** — penyebabnya payload probe saya sendiri:

```
$ curl ... -d '{"model":"oc/muse-spark-1.3-contributor-free",...,"max_tokens":5}'
{"error":{"message":"[400]: ... \"`max_output_tokens` The number must be `>= 16`.\" ..."}}
```

Model menolak `max_tokens` < 16. Dengan `max_tokens=64`:

```
oc/muse-spark-1.3-contributor-free → {"model":"muse-spark-1.3-contributor-free","choices":[...]}   OK
oc/muse-spark-1.2-contributor-free → OK
oc-combo-2                          → {"model":"muse-spark-1.3-contributor-free",...}             OK
```

Jadi `oc-combo-2` berfungsi. **Tidak diubah.**

### Re-verifikasi 17 model yang dilabeli "permanent"

Dengan `max_tokens=64` (bukan 5), untuk memisahkan "permanent asli" dari "artefak payload":

| Model | Hasil | Verdict |
|---|---|---|
| 15× `gh/*` | `400 The requested model is not supported.` | **Permanent asli** — batas tier Copilot |
| `cf/@cf/cloudflare/clef-flash` | `400 AiError: No such model: clef-flash` | **Permanent asli** |
| `oc-combo-2` | OK (`finish_reason: in_progress`) | **SEHAT — koreksi** |

15 dari 17 bertahan sebagai kegagalan nyata; 1 direklasifikasi menjadi sehat.

### Hasil akhir Fase 2 (snapshot saat commit)

```
katalog 9router: 135 → 85 model (−50, semua pixz)
  gh: 32 | kr: 24 | ag: 13 | agnes: 4 | cf: 3 | combo/root: 8 | gemini: 1
  pixz: 0  ← bersih

picker (jalur gateway, warm & cold konsisten):
  WARM 9router: 85 models | pixz=0
  COLD 9router: 85 models | pixz=0
  huancheng: 14 models

channel produksi: semua OK
  gemini/gemini-3.5-flash-lite (ch 1)  → 200
  kr/deepseek-3.2 (ch 803)             → 200
  combo-delegasi (802/804/1172/7402/12595/12707) → 200
  combo-gateway (ch 13902)             → 200
  combo-a2a                            → 200
  sensenova-6.8-flash-lite (ch 8853, huancheng)  → 200
```

### ⚠️ Perkembangan pasca-commit: key pixz DIGANTI pemilik (bukan regresi)

Sesaat setelah commit, katalog 9router naik 85 → **168** dan pixz muncul kembali. **Ini bukan regresi dan
bukan kesalahan** — pemilik mengganti API key pixz:

| | Sebelum | Sesudah |
|---|---|---|
| Key | `pxr_live_rYH…gvNA` | `pxr_live…7TlP` |
| `/v1/models` pixz | **401** | **200** |
| `testStatus` | `unavailable`, `errorCode: 401` | `active`, `errorCode: None` |
| `isActive` | 0 (dinonaktifkan) | 1 |

Diuji langsung ke `https://api-inference.pixz.dev/v1/models` → **HTTP 200**, mengembalikan daftar model
(`claude-opus-5.5`, dll). Key baru **valid**.

**Audit ulang 168 model** (script versi baru, dry-run):

```
OK 119 | transient 33 | permanent 16
  pixz            70/ 13/  0     ← 70 OK dengan key baru
  kr              20/  4/  0
  gh              12/  5/ 15
  ag               5/  8/  0
  agnes            2/  2/  0
  gemini           1/  0/  0
  cf               1/  1/  1
  combo-*          5/  0/  0
```

Transient dibedah: `404` 8 · `403` 3 · `timeout` 11 · `529` 8 · `429` 2 · `502` 1.
Permanent 16 = 15 `gh/*` (batas tier Copilot) + 1 `cf/@cf/cloudflare/clef-flash`.

**Sinkronisasi ulang:** `models:` 9router di config diset 85 → **168** (diff: 0 penghapusan, 83 penambahan).
Verifikasi picker WARM dan COLD: **sama-sama 168**, huancheng 14, atria 1.

**Pelajaran yang muncul dari kejadian ini:** status provider adalah keadaan yang bergerak. Menonaktifkan
provider karena kredensial mati itu benar pada saat itu, tapi **bukan keputusan permanen** — begitu key
diganti, katalog dan `models:` harus disinkronkan ulang. Prosedur pemeliharaan ada di bagian berikutnya.


### Temuan penting: `models:` adalah FALLBACK, bukan pin

Diuji dengan cache hangat vs dingin **setelah** pixz dimatikan:

```
WARM 9router: 141 models | pixz=50    ← cache hangat masih menyajikan pixz!
COLD 9router:  85 models | pixz=0
```

Cache katalog Hermes (`~/.hermes/provider_models_cache.json`, TTL 1 jam) **didahulukan** daripada
`models:` di config. Jadi mematikan provider di 9router saja **tidak** langsung membersihkan picker.

Tindakan tambahan: hapus entry cache 9router (`custom:http://localhost:20128/v1*`), lalu sinkronkan
`models:` config dari 135 → 85 agar konsisten. Verifikasi ulang: WARM dan COLD sama-sama 85, pixz 0.

**Konsekuensi operasional:** setiap kali katalog 9router berubah, `models:` di config perlu ikut
disinkronkan **dan** cache di-invalidate. Ini beban pemeliharaan dari pilihan opsi C.

---

## Fase 3 — Perbaikan Skill (script audit yang berbahaya)

Script lama `niu-9router-maintain/scripts/audit_models.py` adalah penyebab kesalahan disable `gemini`.
Sudah diganti dengan versi aman:

| Sebelum | Sesudah |
|---|---|
| **Menulis DB tanpa flag** — `isActive=0` otomatis | **DRY-RUN default**; hanya menulis dengan `--apply` |
| 1 percobaan, timeout 20s, 8 worker | **3 percobaan** dengan backoff, 4 worker |
| Klasifikasi biner OK/FAIL | **ok / transient / permanent** |
| Semua non-200 = gagal | Hanya `400/401/402/403/404/410` = permanent; `429/5xx/timeout` = transient, tidak pernah ditindak |
| Disable provider yang 0 OK | Disable hanya provider dengan **0 OK DAN 0 transient** |
| `max_tokens=5` | `max_tokens=64` (≥16 wajib) |

Dokumentasi skill juga diperbarui dengan aturan: cross-check `usageHistory` sebelum men-disable,
grep kode upstream di dalam body 503, jangan percaya status luar saja, dan jangan simpan daftar
provider hidup/mati (basi dalam hitungan hari).

**Sinkronisasi:** lewat tool resmi, bukan copy manual —
`promote-skills.py` (dry-run dulu: 3 update diserap, 1 ditolak tidak terkait) →
`skill-manifest.py` (238 skill, 1176 file) → `sync-to-agents.sh` (**0 masalah**, verifikasi hash LULUS).

---

## Prosedur Pemeliharaan (jalankan setiap katalog 9router berubah)

Otomasi `com.niumination.9router-sync` memberi notifikasi macOS saat katalog berubah, tapi **tidak**
memperbarui `models:` di config. Urutan yang benar:

```bash
# 1. Lihat katalog live
curl -s http://localhost:20128/v1/models | python3 -c "import sys,json;print(len(json.load(sys.stdin)['data']))"

# 2. Audit (DRY-RUN — jangan langsung --apply)
python3 ~/.hermes/skills/ecosystem/niu-9router-maintain/scripts/audit_models.py --json /tmp/audit.json

# 3. Sinkronkan models: di config (anchor assert, bukan `hermes config set`)
#    lihat skill hermes-config-mutation-safety

# 4. Invalidate cache katalog Hermes agar picker tidak menyajikan daftar basi
python3 -c "
import json, os
p = os.path.expanduser('~/.hermes/provider_models_cache.json')
d = json.load(open(p)); [d.pop(k) for k in [k for k in d if '20128' in k]]
json.dump(d, open(p,'w'), indent=2)"

# 5. Verifikasi WARM dan COLD memberi angka SAMA
#    (lihat skill hermes-config-mutation-safety, bagian provider kustom)
```

**Jangan lewati langkah 4.** Cache (TTL 1 jam) didahulukan daripada `models:`, jadi tanpa invalidate,
picker tetap menyajikan model provider yang sudah dimatikan.

**Kalau pemilik mengganti API key provider:** provider yang tadinya dinonaktifkan karena kredensial mati
akan aktif kembali. Jalankan ulang prosedur ini dari langkah 1 — jangan asumsikan angka lama masih berlaku.

---

## Fase 4 — Cron Otomatis (disetujui pemilik)

Pemilik menyetujui otomatisasi sinkronisasi. Dibuat:

- **Script:** `scripts/sync-models-to-config.py` (di-copy ke `~/.hermes/scripts/`)
- **Cron job:** `034116abd040` — "Sync 9router models to config", every 30m, `--no-agent`

### Desain script

Tiga keputusan penting:

1. **Tanpa dependensi eksternal.** `--no-agent` memakai interpreter Hermes sendiri, yang
   **tidak** punya PyYAML (`ModuleNotFoundError: No module named 'yaml'`). Implementasi
   parser/regEX+string murni di stdlib (`re`, `json`, `urllib`), dengan validasi struktural:
   parse `models:` list, replace berdasarkan indentasi aktual (bukan asumsi), verifikasi ulang
   dengan re-read dari disk. Asumsi awal `key_indent + 4` untuk list items **salah** — YAML
   mengizinkan sequence di kolom yang sama dengan key, dan itulah yang dipakai config ini.

2. **Target parsing terbatas pada `providers.<section>`**. Di config ini ada dua `9router:` —
   satu di `providers:` (target) dan satu di `model_catalog:` (yang **tidak** boleh disentuh).
   Parser memverifikasi parent section sebelum replace, bukan sekadar cari kemunculan pertama.

3. **Validasi pasca-tulis.** Setelah menulis, script membaca ulang file dan membandingkan
   jumlah model di disk dengan katalog live. Kalau beda → `exit 1` (gagal keras, bukan diam).

### Verifikasi sebelum deploy

| Uji | Perintah | Hasil |
|---|---|---|
| Idempoten | config == katalog | `9router: unchanged (N models)` |
| Replace benar | suntik 1 model palsu ke salinan /tmp | `N+1 -> M models` (dikoreksi), config asli **tidak** disentuh |
| Isolasi ruang | `model_catalog.9router` | `models = None` (tidak tersentuh) |
| Sibling utuh | `providers.huancheng.models` | tetap 14 |
| Cron dry-run | `hermes cron run` | `Ran now: succeeded.` |

### Output contract cron

- Exit 0 + summary satu baris → dikirim ke `--deliver` (default `local`)
- Exit 1 (error) → dikirim ke `--failure-deliver` (di-set `origin`)
- `--no-agent`: LLM diskip, stdout script = payload

### Catatan operasional

Cron berjalan tiap 30 menit. Kalau katalog 9router sedang flapping (168→126→168 terukur),
script akan menangkap akhirnya saat stabil. `models:` di config hanya diubah kalau berbeda dari
katalog — kalau sama, tidak ada write (menghindari rewrite yang perlu).

---

## Bukti

Semua perintah di bawah dijalankan langsung pada 10–11 Okt 2026.

**Diagnosis — cold cache mereproduksi keluhan:**
```bash
$ # cache dipindah + clear_provider_models_cache(), lalu jalur flag gateway
WARM: {'9router': 141, 'huancheng': 14, 'atria': 1}
COLD: {'9router': 0,   'huancheng': 1,  'atria': 1}     # ← keluhan tereproduksi
```

**Diagnosis — bug hash otomasi:**
```bash
$ env -i PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/Cellar/node/26.7.0/bin HOME=$HOME /bin/bash -c '...'
COUNT=135
HASH=[]
PREV_HASH=[]
>>> SILENT EXIT (no-op) — BUG TERKONFIRMASI
$ ls -la /sbin/sha256sum /usr/bin/shasum
Sep 25 09:06:56 2026 /sbin/sha256sum      # ← di luar PATH launchd
Sep 25 09:06:56 2026 /usr/bin/shasum
```

**Perbaikan — config:**
```bash
$ diff ~/.hermes/config.yaml.bak-prefix-20261010 ~/.hermes/config.yaml | grep -c '^<'
0                                          # nol penghapusan
$ hermes config get providers.huancheng.default_model
auto
$ hermes config check
  Saved configuration:
    ⚠ platform 'cli' references unknown toolset 'messaging'   # pra-ada, tidak terkait
```

**Perbaikan — verifikasi warm & cold:**
```bash
WARM: {'9router': 141, 'huancheng': 14, 'atria': 1}
COLD: {'9router': 135, 'huancheng': 14, 'atria': 1}        # ← tetap lengkap saat dingin
```

**Perbaikan — otomasi:**
```bash
$ bash -n scripts/9router-sync.sh && echo "syntax OK"
syntax OK
$ env -i PATH=<launchd PATH> HOME=$HOME /bin/bash scripts/9router-sync.sh ; echo "exit=$?"
exit=0
$ tail -3 ~/.cache/niumination/9router-sync.log
2026-10-10T23:57:52+07:00 change pending: 135 models hash 5c0586c8 (debounce 120s)
2026-10-10T23:57:59.850199 sync: 135 models hash 5c0586c8
2026-10-10T23:57:59+07:00 change: 135 models hash 5c0586c8 -> updated
$ cat ~/.cache/niumination/9router-models.hash
5c0586c885a502155de8445afc000e9541c5d3f31b6d26f30a0184c8fd01c5eb
$ launchctl print gui/501/com.niumination.9router-sync | grep -E 'runs|last exit'
	runs = 163
	last exit code = 0
```

**Audit katalog:**
```bash
$ python3 ~/.hermes/cache/scratch/audit9router.py ~/.hermes/cache/scratch/9router-audit.json
probing 135 models (attempts=3)
OK 52 | transient 66 | permanent 17
per provider (ok/transient/permanent):
  gh              12/  5/ 15
  kr              24/  0/  0
  pixz             0/ 50/  0
  ...
written: /Users/zaryu/.hermes/cache/scratch/9router-audit.json
```

**Pemulihan gemini (koreksi kesalahan audit pertama):**
```bash
$ python3 -c "...UPDATE providerConnections SET isActive=1 WHERE provider='gemini'..."
gemini rows set active: 2
$ curl -s -m 40 -X POST .../chat/completions -d '{"model":"gemini/gemini-3.5-flash-lite",...}'
data: {"id":"chatcmpl-cnHKauTpHdCKjuMP1KGemAU",...,"model":"gemini-3.5-flash-lite",...}   # 200 OK
```

**Bukti gemini hidup sebelum audit (usageHistory 9router):**
```bash
$ python3 -c "...SELECT * FROM usageHistory WHERE provider LIKE '%gemini%'..."
{'timestamp': '2026-10-09T16:14:16.019Z', 'provider': 'gemini', 'model': 'gemini-3.5-flash-lite',
 'promptTokens': 1040, 'completionTokens': 20, 'status': 'ok'}
```

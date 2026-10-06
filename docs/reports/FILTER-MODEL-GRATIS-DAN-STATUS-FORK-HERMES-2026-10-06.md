# Filter Model Gratis di Picker `/model` + Status Fork Hermes

**Tanggal:** 6 Okt 2026
**Thread:** 1 (Niu-MissionControl)
**Ruang lingkup:** patch lokal Hermes Agent (`~/src/hermes-agent`), registry ekosistem

---

## Bagian 1 — Filter free-only untuk provider nous

### Masalah

`/model` di Telegram menampilkan "Provider: Nous Portal (49–50 of 50)" dengan 8 model
tersembunyi di balik pagination. Pemilik hanya memakai tier gratis (tanpa kredit), sehingga
model berbayar di picker tidak berguna — semuanya menolak dengan `404 — requires available credits`.

### Akar

Picker mengambil daftar model nous dari
`hermes_cli/models.py::get_curated_nous_model_ids()` → `hermes_cli/model_catalog.py::get_curated_nous_models()`.
Fungsi itu membaca manifest katalog (52 model) yang **tidak membawa field harga sama sekali** —
jadi free/paid hanya bisa ditentukan dengan menanyakan API provider secara langsung.

Config `model.free_only` yang sudah ada **bukan** untuk picker: key itu hanya memengaruhi
fallback OpenRouter pada panggilan `auxiliary`.

### Perubahan diterapkan

| Berkas | Perubahan |
|---|---|
| `hermes_cli/model_catalog.py` | Tambah `_fetch_nous_free_models()` + gerbang `free_only` di `get_curated_nous_models()` |
| `hermes_cli/config_defaults.py` | Dokumentasi opsi `providers.<name>.free_only` di blok `model_catalog` |
| `~/.hermes/config.yaml` | `model_catalog.providers.nous.free_only: true` |

Detail teknis yang menentukan berhasil/gagal:

- Token dibaca dari `get_hermes_home() / "auth.json"` → `providers.nous.access_token`.
- Base URL diambil dari blok auth yang **sama**: `providers.nous.inference_base_url`
  (`https://inference-api.nousresearch.com/v1`).
- **`portal.nousresearch.com/api/v1/models` BUKAN endpoint model** — memakainya menghasilkan
  nol model secara diam-diam (kegagalan tak terlihat tanpa mencetak jumlahnya). Ini mode
  kegagalan nomor satu.
- Model gratis = `pricing.prompt == 0` **dan** `pricing.completion == 0`. Nilai berupa string
  (`"0.0000000000"`), harus di-cast sebelum dibandingkan.
- Hasil di-cache in-process 5 menit (picker memanggil ini setiap kali dibuka).
- Return `free_ids or None` supaya kegagalan fetch jatuh kembali ke daftar manifest,
  bukan picker kosong.

### Verifikasi

```
$ python3 -c "from hermes_cli.model_catalog import _fetch_nous_free_models; ..."
Free models: 9
  inclusionai/ling-3.1-flash
  inclusionai/ling-3.0-flash-sante:free
  inclusionai/ling-3.0-flash-fin:free
  meituan/longcat-2.0:free
  meituan/longcat-2.5-preview:free
  poolside/laguna-s-2.1:free
  poolside/laguna-xs-2.1:free
  stepfun/step-3.7-flash:free
  upstage/solar-mini4:free

$ python3 -c "from hermes_cli.models import get_curated_nous_model_ids; ..."
get_curated_nous_models     -> 9 models
get_curated_nous_model_ids  -> 9 models (jalur yang dipakai picker)
```

Total payload API saat pengukuran: **425 model**, 9 di antaranya nol-harga.
Angka bergerak — jangan di-hardcode.

### Pergeseran inventaris gratis nous (perlu dicatat)

Registry `docs/registry/model-mapping.md` (snapshot 19 Sep 2026) mencatat **7** model `:free`.
Pengukuran 6 Okt 2026 menemukan **9** nol-harga, dengan komposisi berbeda:

- **Masuk:** `inclusionai/ling-3.1-flash` (gratis **tanpa** sufiks `:free`),
  `meituan/longcat-2.5-preview:free`, `upstage/solar-mini4:free`.
- **Tidak lagi nol-harga:** `upstage/solar-pro4:free` (tercatat gratis 19 Sep) — disimpulkan
  dari **ketidakhadirannya** di daftar 9 hasil pengukuran 6 Okt, bukan dari probe harga
  terpisah. Probe langsung untuk konfirmasi positif belum dijalankan (UNCHECKED).

Konsekuensi: sufiks `:free` **tidak bisa** dipakai sebagai penanda tunggal. Harga adalah
satu-satunya sinyal andal.

### Sifat patch

Patch hidup di **source repo Hermes** (`~/src/hermes-agent`), bukan di config. `hermes update`
menarik `main` dan mengembalikan kedua berkas. **Wajib re-apply setelah setiap update.**
Prosedur lengkap: skill `ecosystem/hermes-model-catalog-management`.

Gateway harus direstart dari **shell luar** — restart dari dalam proses gateway diblokir
secara desain (SIGTERM membunuh perintah sebelum selesai).

---

## Bagian 2 — Status fork `Niumination/hermes-agent` vs upstream

### Remote terpasang

| Remote | URL | Peran |
|---|---|---|
| `origin` | `git@github.com:Niumination/hermes-agent.git` | Fork — **kanal update Hermes** |
| `upstream` | `https://github.com/NousResearch/hermes-agent.git` | Sumber asli |

### Divergensi terukur (6 Okt 2026)

| Perbandingan | Hasil |
|---|---|
| `main` lokal vs `origin/main` (fork) | **+7945** lokal unik, **2** fork unik |
| `main` lokal vs `upstream/main` | **+5** lokal unik, **16185** upstream unik |
| HEAD fork (`origin/main`) | `0224447274` — 25 Agu 2026 |
| HEAD lokal (`main`) | `2160f78d84` — 6 Okt 2026 (setelah commit patch free-only) |
| HEAD upstream (live) | `a02278293e` — 6 Okt 2026 |
| Merge-base lokal ↔ upstream | `bf53ff00a7` — 9 Sep 2026 |

### Temuan penting

**0. `hermes update` TIDAK auto-update — dan sinkronisasi upstream diblokir permanen.**

Auto-update tidak ada: `updates.check: true` hanya *memeriksa*, tidak menerapkan. Bukti:
`~/.hermes/.update_check` berisi `{"ts": …, "behind": 2, "rev": null, "ver": "0.21.1"}` —
angka `behind: 2` itu jarak ke **fork**, bukan upstream.

Lebih serius: ada mekanisme yang seharusnya menyinkronkan fork dengan upstream
(`_sync_with_upstream_if_needed()`, `hermes_cli/update_cmd_git.py:267`), tetapi **selalu
berhenti lebih awal** pada kondisi fork sekarang:

```python
origin_ahead = _count_commits_between(git_cmd, cwd, "upstream/main", "origin/main")
if origin_ahead > 0:
    print(f"ℹ Your fork has {origin_ahead} commit(s) not on upstream.\n"
          "  Skipping upstream sync to preserve your changes.")
    return True
```

Terukur: `origin_ahead = 2` (fork punya 2 commit yang tidak ada di upstream —
`05ef3d7518` patch lokal + `0224447274` merge). Karena `origin_ahead > 0`, cabang
"sinkronkan" **tidak pernah dieksekusi**; updater selalu keluar lewat jalur skip.

Bahkan bila jalur itu tercapai, langkahnya `git pull --ff-only upstream main`
(`update_cmd_git.py:304`) — dan itu akan **gagal**, karena `main` lokal 7.945 commit
di depan `origin/main`, jadi tidak mungkin fast-forward.

**Kesimpulan:** selama fork menyimpan commit lokal yang tidak ada di upstream,
`hermes update` tidak akan pernah menarik kode upstream — secara desain, bukan bug.
Satu-satunya jalan adalah rekonsiliasi manual (`git pull upstream main` + resolusi konflik),
yang berarti menyentuh langsung 4 patch gateway/notif yang sekarang bekerja.

**1. Kanal update menunjuk ke fork, bukan upstream.**

`hermes --version` melaporkan:

```
Hermes Agent v0.21.1 (2026.9.7) · upstream 02244472 · local 6872e8e8 (+7945 carried commits)
Update available: 2 commits behind — run 'hermes update'
```

Label "upstream" di baris itu sebenarnya `origin/main` — **fork**, bukan NousResearch.
"2 commits behind" berarti 2 commit fork yang belum ada di lokal. Jadi `hermes update`
menarik dari fork, dan fork terakhir disinkronkan **25 Agu 2026**.

**2. Fork tertinggal jauh dari sumber asli.**

Upstream NousResearch sudah maju **16.185 commit** sejak titik pisah 9 Sep 2026. Artinya
`hermes update` hari ini **tidak** membawa perbaikan upstream — hanya 2 commit fork (satu
di antaranya patch lokal lama).

**4. Lima commit lokal belum ada di upstream.**

| SHA | Tanggal | Isi |
|---|---|---|
| `2160f78d84` | 6 Okt | `patch(local)`: filter free-only picker `/model` (nous) |
| `6872e8e876` | 28 Sep | `fix(computer-use)`: batasi readiness probe di atas handshake |
| `0da89439d3` | 10 Sep | `patch(local)`: notif gateway Bahasa Indonesia + status block + bounded-wait |
| `e1b7e2e6d1` | 9 Sep | `fix(gateway)`: suppress final normal saat stale finalize |
| `c6b22d0edc` | 9 Sep | `fix(gateway)`: cegah kirim final ganda saat stream consumer sudah push konten |

Berkas yang tersentuh: `gateway/run_notifications.py`, `gateway/run_turn.py`,
`gateway/stream_consumer.py`, `tools/computer_use/cua_backend_daemon.py` (116 baris),
`hermes_cli/model_catalog.py` + `hermes_cli/config_defaults.py` (72 baris).

**4. Dua commit fork belum ada di lokal — satu di antaranya duplikat fungsional.**

| SHA | Tanggal | Catatan |
|---|---|---|
| `0224447274` | 25 Agu | Merge `upstream/main` (titik sinkron terakhir) |
| `05ef3d7518` | 25 Agu | `patch(local)`: notif startup + restart bounded-wait |

`05ef3d7518` (25 Agu) dan `0da89439d3` (10 Sep) menyentuh **fungsi yang sama** —
`_wait_for_send_paths_healthy()` + notif startup. Versi lokal 10 Sep lebih baru; versi fork
25 Agu kemungkinan sudah usang. Perlu keputusan pemilik sebelum rekonsiliasi.

**5. Pekerjaan belum ter-commit di lokal.**

`hermes_cli/model_catalog.py` (+71) dan `hermes_cli/config_defaults.py` (+2) — patch filter
free-only dari Bagian 1, masih di working tree.

### Rekomendasi (belum dieksekusi — menunggu keputusan pemilik)

1. **Commit patch filter free-only** ke `main` lokal supaya tidak hilang saat update.
2. **Push `main` lokal ke fork** — 7945 commit tertahan di lokal; fork sebagai kanal update
   saat ini tidak mencerminkan kode yang benar-benar berjalan.
3. **Sinkronkan fork dengan upstream** lalu rebase 4 commit lokal di atasnya. Ini pekerjaan
   besar (16k commit) dan berisiko pada patch gateway/notif — butuh jendela waktu khusus.
4. **Rekonsiliasi `05ef3d7518` vs `0da89439d3`** sebelum rebase, agar tidak ada patch notif
   yang saling menimpa.
5. **Uji `hermes update`** setelah fork disinkronkan, untuk memastikan patch lokal selamat.

---

## Bukti

```
$ git remote -v                        → origin=Niumination/hermes-agent, upstream=NousResearch/hermes-agent
$ git rev-list --left-right --count origin/main...main       → 2      7945
$ git rev-list --left-right --count upstream/main...main     → 16185  4
$ git log -1 --format="%h %ci %s" upstream/main              → a02278293e 2026-10-06 chore: map contributor email for gmail (#133555)
$ git log -1 --format="%h %ci %s" origin/main                → 0224447274 2026-08-25 Merge remote-tracking branch 'upstream/main'
$ git log -1 --format="%h %ci %s" main                       → 6872e8e876 2026-09-28 fix(computer-use): bound the readiness probe...
$ hermes --version                                           → v0.21.1 (2026.9.7) · upstream 02244472 · local 6872e8e8 (+7945 carried commits)
$ git diff --stat                                            → model_catalog.py +71, config_defaults.py +2
$ hermes config get model_catalog.providers.nous.free_only   → true
$ python3 -c "_fetch_nous_free_models()"                     → Free models: 9
$ python3 -c "get_curated_nous_model_ids()"                  → 9 models
```

**Belum diverifikasi:** apakah `hermes update` benar-benar menarik dari fork pada eksekusi
nyata (baru dibaca dari string versi, belum dijalankan); dampak rebase 4 patch lokal di atas
upstream terbaru.

---

## Tindak lanjut

- Skill `ecosystem/hermes-model-catalog-management` diperbarui: prosedur re-apply patch +
  `references/nous-portal-free-models.md` (skema API, aturan deteksi gratis, mode kegagalan).
- Registry `docs/registry/model-mapping.md`: inventaris gratis nous perlu dikoreksi dari 7 → 9
  dengan catatan pergeseran komposisi.

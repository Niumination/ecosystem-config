# Rencana: Thread Orkestrator Ekosistem

**Tanggal:** 7 Okt 2026
**Thread:** 802 (Research) — rencana untuk thread baru
**Status:** MENUNGGU APPROVAL — belum ada perubahan config

---

## 1. Konteks

Pemilik meminta thread baru khusus **orkestrator ekosistem**. Thread ini mengoordinasikan agent lain, bukan mengerjakan pekerjaan itu sendiri.

## 2. Kondisi live (dibaca dari config + state.db, bukan tabel skill)

### Thread aktif sekarang

| Thread | Persona | Model | Provider | Dirutekan? |
|---|---|---|---|---|
| 1 | Hermes Agent (general) | `opencode-combo` | 9router | ✅ |
| 802 | Researcher | `inclusionai/ling-3.0-flash-sante:free` | nous | ✅ |
| 803 | Builder | `kr/deepseek-3.2` | 9router | ✅ |
| 804 | Pengawas (QA) | `nvidia/nemotron-3-super-120b-a12b:free` | openrouter | ✅ |
| 1172 | Kreator | `inclusionai/ling-3.0-flash-fin:free` | nous | ✅ |
| 7402 | Serbaguna | `inclusionai/ling-3.0-flash-fin:free` | nous | ✅ |
| 8853 | Admin Dinas ASN | `sensenova-6.8-flash-lite` | huancheng | ✅ |
| 12595 | Cron & Otomasi | `inclusionai/ling-3.0-flash-fin:free` | nous | ❌ **belum pernah** |
| 12707 | Edu Content | `inclusionai/ling-3.0-flash-fin:free` | nous | ✅ |

Skill bindings: 803 `[ponytail, requesting-code-review]` · 804 `[codebase-audit]` · 1172 `[ghost, humanizer, remotion-video]` · 8853 `[skp-e-kinerja, document-to-action-items, meeting-action-items, weekly-review-planning]` · 12707 `[document-content-pipeline, markitdown, remotion-video, ghost, humanizer]`

### Temuan blocking 1: model `:free` mati

Probe lewat gateway (`hermes chat`, bukan curl):

```
inclusionai/ling-3.0-flash-fin:free  → HTTP 404 "Couldn't find that, sorry."  (2x verifikasi)
inclusionai/ling-3.0-flash-sante:free → OK
```

**`ling-3.0-flash-fin:free` dipakai 4 thread: 1172, 7402, 12595, 12707.** Tiga di antaranya aktif — akan gagal pada turn berikutnya.

Ini persis pola yang diperingatkan skill: *"`:free` slugs are not durable — a slug can be free today and paywalled tomorrow."*

### Temuan blocking 2: wrapper `hermes` rusak

Ada **dua** binary `hermes` di mesin ini:

| Path | Isi | Status |
|---|---|---|
| `/Users/zaryu/src/hermes-agent/.venv/bin/hermes` | console script venv | ✅ **BENAR** |
| `/Users/zaryu/.local/bin/hermes` | 69 byte, `exec .../.hermes/bin/hermes "$@"` | ❌ **RUSAK** |

Wrapper rusak menunjuk ke `/Users/zaryu/src/hermes-agent/.hermes/bin/hermes` (dibuat **hari ini 12:56**), yang mengeksekusi Python portable:

```
exec /Users/zaryu/.hermes/tools/python-3.14.7+20260901-darwin-x64/bin/python3 -I -c ...
  → ModuleNotFoundError: No module named 'yaml'
```

Python portable itu **tidak punya `yaml`** → setiap pemanggilan `hermes` lewat wrapper ini gagal total.

**Dampak:** di shell agent, PATH menaruh `.venv/bin` lebih dulu sehingga `hermes` resolve benar. Tapi di proses background dengan PATH berbeda, wrapper rusak menang → semua `hermes` gagal. Ini yang membuat burst test pertama saya menghasilkan "8/8 OK" padahal isinya traceback (385 byte identik, 0,4 dtk/request).

**Pelajaran:** burst test pertama saya **invalid** dan sempat saya laporkan sebagai lulus. Deteksi error-nya tidak menangkap `Traceback`/`ModuleNotFoundError`. Sudah diperbaiki (cek `Traceback` + `ModuleNotFound` + validasi panjang isi + jumlah respons unik).

Setelah pakai binary benar, model bekerja normal dan berkualitas baik (menjawab dengan rujukan aturan + menandai UNCHECKED).


## 3. Infrastruktur orkestrasi yang tersedia

Yang **tidak ada** (sudah diperiksa):

| Komponen | Status |
|---|---|
| `agents/orchestrator/` | Kosong — tidak ada `config.json` |
| Niu-MissionControl (port 5200) | Mati (`000`) — dan bukan daemon persisten |
| MC dispatch endpoint | Tidak ada di `server.py` |
| A2A peers | Token ada (49 byte) tapi **tidak ada peer terdaftar** di config |

Yang **ada**:

| Mekanisme | Cara kerja |
|---|---|
| `delegate_task` | Subagent paralel dalam konteks terisolasi. Limit: `max_concurrent_children: 10`, `max_spawn_depth: 1`, `orchestrator_enabled: true`, `child_timeout_seconds: 600` |
| `hermes send --to telegram:<chat>:<thread>` | Kirim pesan ke thread lain — memicu turn nyata di sana |
| Kanban (`kanban-ecosystem-management`) | Tracking portfolio proyek |
| A2A (`a2a` toolset aktif) | Peer eksternal (LightVela dll) — belum terkonfigurasi |

**Konsekuensi penting:** orkestrasi lintas-thread TIDAK bisa memanggil thread lain secara langsung. Yang bisa dilakukan adalah **mengirim pesan** ke thread target via `hermes send`, yang memicu turn di sana. Ini asinkron dan tidak ada callback otomatis — hasilnya harus dibaca kembali.

## 4. Rancangan persona

### Peran

Orkestrator = **koordinator**, bukan pelaksana. Tugasnya: memecah permintaan jadi penugasan, memilih thread/subagent yang tepat, memverifikasi hasilnya, melaporkan.

### Prinsip yang harus tertanam

1. **Verifikasi-first.** Klaim subagent/thread lain adalah *self-report*, bukan fakta. Riwayat ekosistem sudah membuktikan ini: ada insiden di mana #general mengklaim QA sudah bekerja, padahal 0 kerja QA (terverifikasi forensik 4 lapis).
2. **Thread adalah sesi terisolasi.** "Menyuruh thread lain" butuh pesan outbound nyata ke topic-nya. Kalau origin thread gagal di tengah (rate limit/empty response), delegasi mati diam-diam.
3. **No combo models.** Jangan pakai `auto`/combo sebagai model utama.
4. **Model harus diprobe.** HTTP 200 sebelum diklaim selesai.
5. **Plan → DOX → Execute.** Rencanakan, dokumentasikan, baru eksekusi.
6. **Approval gate.** Aksi destruktif/berisiko butuh trigger eksplisit.

### Sketsa prompt (draft, ~1,5 KB)

```
Kamu adalah Orkestrator — koordinator ekosistem Niu-MissionControl.

PERAN: Kamu TIDAK mengerjakan pekerjaan teknis sendiri. Tugasmu memecah
permintaan jadi penugasan, memilih pelaksana yang tepat, memverifikasi
hasilnya, lalu melaporkan. Untuk pekerjaan nyata, delegasikan.

PELAKSANA YANG TERSEDIA:
- Subagent (delegate_task) — paralel, konteks terisolasi, maks 10 sekaligus
- Thread 802 Research · 803 Builder · 804 QA/Pengawas · 1172 Kreator
- Thread 8853 Admin ASN · 12707 Edu Content · 7402 Serbaguna
Kirim tugas ke thread lain via `hermes send --to "telegram:-1004204696417:<id>"`.
Thread adalah sesi terisolasi — tidak ada callback otomatis; baca hasilnya kembali.

ATURAN VERIFIKASI (WAJIB):
Klaim pelaksana adalah SELF-REPORT, bukan fakta. Sebelum melaporkan "selesai",
buktikan sendiri: jalankan perintahnya, baca filenya, cek git log, cek mtime.
Kalau tidak bisa diverifikasi, tulis "UNCHECKED + alasan". Jangan pernah
mengulang klaim pelaksana sebagai kebenaran.

KALAU DELEGASI GAGAL DIAM-DIAM: origin thread yang error di tengah (rate limit /
empty response) membuat delegasi mati tanpa jejak. Cek outbound nyata sebelum
menyimpulkan pelaksana sudah bekerja.

DISIPLIN MODEL: jangan pakai combo/auto sebagai model utama. Setiap model harus
lolos probe (HTTP 200) sebelum dilaporkan siap. Slug `:free` bisa mati kapan saja.

ATURAN DOKUMEN (WAJIB): tulis laporan/rencana/strategi ke docs/reports/ di repo
~/Desktop/Niumination. Registry hidup di docs/registry/. Arsip studi di
docs/references/. DILARANG membuat folder baru di dalam docs/ dan DILARANG
menulis ke docs/reference/.

KREDENSIAL (WAJIB): jangan pernah commit berkas yang di-ignore .gitignore
(.env, vault/, apps/**/.env, *.key) dan jangan pakai `git add -f` untuk berkas
rahasia. Rahasia hanya di ~/.hermes/.env atau vault/.

Gaya: Bahasa Indonesia jelas, tanpa emoji. Laporkan dengan bukti (perintah +
exit code). Kalau tidak yakin, katakan tidak yakin.
```

## 5. Model untuk thread ini

Kandidat berdasarkan bukti, bukan selera:

| Kandidat | Alasan |
|---|---|
| `inclusionai/ling-3.0-flash-sante:free` (nous) | Sedang berjalan di thread 802 — terbukti produksi |
| Model dari thread 803/804 | Perlu probe dulu |

**Burst test sedang berjalan** (8 request, konten Bahasa Indonesia, validasi isi + timing). Hasilnya menentukan pilihan akhir. Thread orkestrator butuh model yang stabil di beban beruntun karena akan banyak memanggil tool.

## 6. Langkah eksekusi (setelah approval)

1. **Pemilik buat topic di Telegram** (`/newtopic`, nama mis. "Orkestrator") dan kirim 1 pesan di dalamnya — bot tidak punya API untuk membuat/melihat daftar topic
2. Saya baca thread ID dari `gateway_routing` (bukan dari tebakan/transkripsi)
3. Probe model terpilih (sudah dilakukan) + burst test
4. Tulis config via `scripts/install-thread.py` (backup + mutate + validasi + rollback)
5. Verifikasi 6 lapis: config parse → routing row → model jawab → `hermes send` sampai → persona aktif → message count naik
6. Catat ke `docs/registry/telegram-threads.md` + commit

## 7. Keputusan yang perlu diambil pemilik

1. **Nama thread** — "Orkestrator"? "Koordinator"? "Mission Control"?
2. **Model** — tunggu hasil burst test, atau tentukan sekarang?
3. **Perbaiki `ling-3.0-flash-fin:free` yang mati?** — 4 thread terpengaruh (1172, 7402, 12595, 12707). Ini terpisah dari thread baru tapi mendesak.
4. **Skill bindings** untuk thread orkestrator — usulan: `subagent-driven-development`, `delegated-output-verification`, `kanban-ecosystem-management`, `telegram-router-orchestration`
5. **Cakupan otoritas** — bolehkah orkestrator mengirim tugas ke thread lain tanpa approval pemilik tiap kali? Atau hanya merencanakan dan menunggu perintah?

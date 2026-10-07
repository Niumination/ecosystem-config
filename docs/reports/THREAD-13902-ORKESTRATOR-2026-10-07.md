# Thread Orkestrator 13902 — Laporan Pemasangan

**Tanggal:** 7 Okt 2026
**Thread:** 13902 (Orkestrator) — Niu-MissionControl
**Status:** ✅ TERPASANG & TERVERIFIKASI

---

## Ringkasan

Thread Orkestrator dibuat pemilik di Telegram, lalu dipasang dan diverifikasi. Thread aktif dan menjawab dengan persona yang benar.

**Dua temuan sistemik ditemukan saat pengerjaan** — keduanya di luar scope pembuatan thread tapi berdampak ke seluruh ekosistem:

1. **236 dari 292 skill ambigu** — loader menolak resolve nama; 12 dari 17 skill binding thread rusak
2. **Dispatch lintas-thread tidak memicu turn** — `hermes send` hanya outbound

---

## 1. Konfigurasi terpasang

| Item | Nilai |
|---|---|
| Thread ID | `13902` (dibaca dari `gateway_routing`, bukan tebakan) |
| Session ID | `20261008_012904_74698d36` |
| Pesan pertama | dari Afrizal Munthe, message_id 13903 |
| Model | `inclusionai/ling-3.0-flash-sante:free` |
| Provider | `nous` |
| Prompt | 2.403 char |
| Skills | `subagent-driven-development`, `delegated-output-verification`, `kanban-ecosystem-management`, `telegram-router-orchestration` |

### Persona

Orkestrator = **koordinator**, bukan pelaksana. Blok prompt:
1. Peran + daftar pelaksana tersedia
2. **ATURAN VERIFIKASI** — klaim pelaksana = self-report, bukan fakta; wajib dibuktikan sendiri; `UNCHECKED + alasan` bila tidak bisa
3. Delegasi gagal diam-diam — origin thread yang error membuat delegasi mati tanpa jejak
4. Disiplin model — dilarang combo/auto; setiap model harus lolos probe
5. ATURAN DOKUMEN (pola rumah)
6. KREDENSIAL (pola rumah)

### Pemasangan

`hermes config set` untuk model + provider — **surgical**, hanya menambah 2 baris, dan menulis key sebagai string `'13902'` sehingga bug numeric-key (yang pernah memaksa triple-quote literal `'''12707'''`) tidak terjadi.

Python yaml round-trip untuk prompt + skill bindings, karena `channel_skill_bindings` adalah **JSON string**, bukan YAML mapping.

**Verifikasi round-trip:** 491 → 492 keys, 0 keys hilang, hanya +1 prompt. Provider, model global, mcp_servers, delegation semua tidak berubah.

Backup: `~/.hermes/config-backups/config.yaml.bak-orchestrator-20261008-013609`

---

## 2. Verifikasi

| Lapis | Hasil |
|---|---|
| 1. Config parse + keys ada | ✅ override + prompt + bindings |
| 2. Gateway routing row | ✅ `agent:main:telegram:group:-1004204696417:13902` |
| 3. Model jawab lewat gateway | ✅ `ORKESTRATOR-SIAP` |
| 4. Persona aktif di thread | ✅ thread menjawab dengan mode operasi (turn-based, approval gate, bukti, delegasi) |

**Probe model (4 request, konten Bahasa Indonesia):** 4/4 sukses, respons berbeda-beda (449/1528/532/1902 byte), 41-67 dtk/request.

**Catatan metode:** burst test pertama saya melaporkan "8/8 OK" tapi **invalid** — isinya traceback karena wrapper `hermes` rusak. Deteksi error tidak menangkap `Traceback`. Setelah diperbaiki (cek `Traceback` + `ModuleNotFound` + validasi panjang isi + jumlah respons unik) dan memakai absolute path ke venv, hasilnya valid.

---

## 3. Temuan sistemik #1 — 236 skill ambigu

### Akar masalah

`config.yaml` → `skills.external_dirs` menunjuk `~/Desktop/Niumination/skills` (bank, source of truth). Tapi isi bank **juga** disalin ke `~/.hermes/skills` oleh `sync-to-agents.sh`. Kedua salinan berada di **path relatif yang sama** (`software-development/subagent-driven-development/SKILL.md`).

`tools/skills_tool.py:466` `_locate_skill()` mengumpulkan kandidat dari semua dir; bila >1 → menolak:

```python
if len(candidates) > 1:
    return _fail(f"Ambiguous skill name '{name}': {len(candidates)} skills match ...")
```

### Skala

```
bank skill    : 238
~/.hermes     : 290
nama sama     : 236  (md5 IDENTIK semua — 236/236, 0 berbeda)
AMBIGU        : 236 dari 292 nama
```

Bank yang tidak ada di `~/.hermes`: `backup-coverage-audit`, `cc-acehtengah-maintain`.

### Dampak ke thread — 12 dari 17 skill binding rusak

| Thread | Skill rusak | Jenis |
|---|---|---|
| 1172 | `ghost`, `remotion-video` | ambigu |
| 12707 | `document-content-pipeline`, `markitdown`, `remotion-video`, `ghost` | ambigu |
| 13902 | `subagent-driven-development`, `delegated-output-verification`, `kanban-ecosystem-management`, `telegram-router-orchestration` | ambigu |
| 803 | `requesting-code-review` | ambigu |
| 803 | `ponytail` | **tidak ada** (nama aslinya `ponytail-core`) |
| 804 | `codebase-audit` | **tidak ada** |
| 8853 | `skp-e-kinerja` | ambigu |

### Hint di error tidak berguna

Error menyarankan "pass the full relative path" — **tidak bisa dipakai**, karena kedua salinan sudah berbagi path relatif identik. Absolute path juga ditolak.

Ini terdokumentasi di skill `skill-bank-mirror-integrity` **Rule 4**, dengan 3 remedi (semua menyentuh config → butuh approval pemilik):

1. Kecualikan mirror dari search path loader, hanya bank yang terdaftar
2. Daftarkan mirror di namespace berbeda agar path relatif berbeda
3. Hapus mirror — berhenti sync ke dir agent, load langsung dari bank

### Konsekuensi tambahan

`skill_manage` menolak patch skill yang ada dengan `read_before_write_required` — guard menuntut `skill_view` yang tidak bisa berhasil. **Membuat skill baru tetap bisa** (nama baru tidak punya prior-read requirement).

---

## 4. Temuan sistemik #2 — dispatch lintas-thread tidak memicu turn

### Klaim registry (BENAR)

> "Bot API tidak bisa baca message bot sendiri di forum topic (terverifikasi: `getUpdates` 0, webhook kosong)."

### Uji saya

```
hermes send --to "telegram:-1004204696417:13902" "MARKER-UNIK-7731: ..."
  → rc=0 "sent"

gateway.log inbound untuk marker : (TIDAK ADA)
pesan session 12 → 13            : yang bertambah = pesan SAYA, role=assistant
```

**Kesimpulan:** `hermes send` = **outbound saja**. Tidak ada turn yang berjalan di thread target.

### Koreksi klaim saya sendiri

Di tengah pengerjaan saya sempat menyimpulkan "`hermes send` memicu turn ✅" berdasarkan pesan yang bertambah 9→12. Itu **salah** — pertambahan itu berasal dari **pemilik yang mengetik manual** di thread (`SIAP`, `DIKONFIRMASI`). Saya mengoreksi setelah menguji dengan marker unik dan memeriksa role pesan.

**Pelajaran:** "pesan bertambah" bukan bukti turn terpicu. Yang membuktikan: `gateway.log` mencatat inbound **dengan isi pesan kita**, dan ada pesan ber-role `assistant` yang isinya respons atas pesan itu.

### Implikasi untuk orkestrasi

| Mekanisme | Benar-benar mengeksekusi? |
|---|---|
| `hermes send` ke thread | ❌ outbound saja |
| `delegate_task` | ✅ subagent, sinkron dalam sesi |
| `cronjob` | ✅ terjadwal, delivery via `platform:chat_id` |
| Interaksi manual pemilik | ✅ |

Rancangan Orkestrator harus memakai `delegate_task` untuk pekerjaan yang harus benar-benar jalan. Mengirim pesan ke thread lain hanya untuk memberi tahu, bukan untuk menyuruh bekerja.

---

## 5. Rekomendasi

**Mendesak (blocking untuk semua thread):**

1. **Selesaikan ambiguitas skill** — pilih satu dari 3 remedi di `skill-bank-mirror-integrity` Rule 4. Ini memblokir 12 skill binding dan mencegah patch skill apa pun.
2. **Perbaiki model `ling-3.0-flash-fin:free` yang mati** (HTTP 404, terverifikasi 2x) — dipakai 4 thread: 1172, 7402, 12595, 12707.
3. **Perbaiki wrapper `/Users/zaryu/.local/bin/hermes`** — menunjuk Python portable tanpa modul `yaml`, gagal total di luar shell agent.

**Perbaikan kualitas:**

4. Betulkan skill binding yang menunjuk nama tidak ada: `ponytail` → `ponytail-core`; `codebase-audit` → cek nama sebenarnya.

---

## Bukti

```
# Thread ID dari routing (bukan tebakan)
sqlite3 state.db "select session_key from gateway_routing where session_key like '%:13902'"
  → agent:main:telegram:group:-1004204696417:13902
  → origin.user_name: Afrizal Munthe | message_id: 13903

# Config terpasang
grep -A3 "'13902'" ~/.hermes/config.yaml
  → model: inclusionai/ling-3.0-flash-sante:free
  → provider: nous

# Round-trip aman
keys sebelum 491 → sesudah 492 | hilang 0 | baru 1 (channel_prompts.13902)

# Model hidup (4/4)
hermes chat -q "..." -m "inclusionai/ling-3.0-flash-sante:free" --provider nous -Q
  → 41s/44s/44s/67s | 449/1528/532/1902 byte | 4/4 sukses

# Persona aktif
thread 13902 menjawab: "Orkestrator aktif. Mode operasi: Turn-based / Approval gate /
  Bukti / Delegasi — Apa yang akan diorkestrasi?"

# Ambiguitas skill
bank 238 | ~/.hermes 290 | nama sama 236 (md5 identik 236/236) | AMBIGU 236/292

# Dispatch tidak memicu turn
hermes send --to "...:13902" "MARKER-UNIK-7731 ..."
  → gateway.log inbound marker: (TIDAK ADA)
  → pesan 12→13, yang bertambah role=assistant (pesan kita sendiri)

# Wrapper hermes rusak
cat /Users/zaryu/.local/bin/hermes
  → #!/bin/sh / exec /Users/zaryu/src/hermes-agent/.hermes/bin/hermes "$@"
  → ModuleNotFoundError: No module named 'yaml'
```

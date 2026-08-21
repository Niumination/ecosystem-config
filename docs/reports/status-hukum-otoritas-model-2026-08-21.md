# ⚖️ Status Hukum Ekosistem — Otoritas Model Utama

> **Tanggal audit:** 2026-08-21
> **Permintaan:** pemilik merasa aturan otoritas model "terlalu ketat" — audit menyeluruh lapisan hukumnya.
> **Sifat:** audit + rekomendasi. File ter-segel (`CONSTITUTION.md`, `MODEL.policy.yaml`, dst.) **hanya diubah atas keputusan `zaryu`** — dokumen ini tidak memutasinya.

> **✅ Pembaruan eksekusi (sama hari, arahan zaryu — Opsi B + perbaikan stale):** runtime `niu_corelib.py` dilonggarkan (switch sesama keluarga tanpa fence; allowlist 4 model), `STATE.yaml`/`AGENTS.md`/`TELEGRAM-UNIFY.md`/`INCIDENT.md`/`PATHS.md` diperbarui, draft keputusan **D-0003** dibuat, test diperbarui (21 cek lulus). **File ter-segel TIDAK disentuh** — amandemen siap-pakai ada di `docs/reports/amandemen-otoritas-model-2026-08-21.md` untuk Anda seal.

---

## 1. Peta lapisan hukum (siapa memutuskan apa)

| Lapisan | File | Status | Yang boleh ubah | Isi terkait model |
|---|---|---|---|---|
| Konstitusi | `core/CONSTITUTION.md` (v2.0) | 🔒 TERSEGEEL | hanya `zaryu` | Hukum 2 (2 model), Hukum 3 (ganti model = ganti dunia), Hukum 12 (manusia = sumber kebenaran) |
| Kebijakan model | `core/MODEL.policy.yaml` (v2) | 🔒 TERSEGEEL | hanya `zaryu` | allowlist, `on_rate_limit`, `on_foreign_model_detected`, `forbidden_thinkers` |
| Keputusan | `D-0001` (2026-08-18) → `D-0002` (2026-08-21) | 🔒 sealed | disahkan `zaryu` | suksesi otak ke keluarga nemotron/hy3; `review_after 2026-09-18/21` |
| State | `core/STATE.yaml` | agen boleh update field izin | skrip/agen | `model.active`, `model.allowed`, `fence`, `health` |
| Peta runtime | `AGENTS.md` + `core/AGENTS.slim.md` | slim | terkoordinasi | ringkas "otak yang diizinkan" |
| Enforcement | `scripts/niu_corelib.py` (hook) | kode | repo | `classify_model`, `pre_llm_context`, `check_mutation` — **blokir tulis model asing** |
| Operasional | `agents/_shared/INCIDENT.md`, `PATHS.md` | kontrak | terkoordinasi | langkah darurat & sumber kebenaran |

**Fence sekarang:** `active: false` (diturunkan 2026-08-21T02:26+07). Tidak ada blokade aktif.

---

## 2. Aturan otoritas model saat ini — 4 tuas ketat

| # | Tuas | Isi sekarang | Tingkat ketat |
|---|------|--------------|---------------|
| T1 | **Allowlist otak** | hanya 2 model, 1 keluarga: `opencode-zen/nemotron-3-ultra-free` (primary) + `opencode-zen/hy3-free` (alternate) | 🔴 sangat ketat |
| T2 | **Saat limit** | `same-family-or-halt`: fallback **hanya** hy3-free; **tidak boleh** lompat 9router/juan/huancheng/model pensiun | 🔴 sangat ketat |
| T3 | **Ritual ganti model** | ganti model (model apa pun) → tulis `HANDOFF.md` + **fence** + "jangan lanjut tugas" | 🟠 ketat |
| T4 | **Model asing terdeteksi** | `halt_mutating_tools` + handoff + inject "kamu bukan otak" + **blokir tulis** di runtime | 🔴 sangat ketat |

Enforcement **benar-benar hidup**, bukan cuma dokumen: `niu_corelib.py` di-hook sehingga model asing yang mencoba menulis file akan **diblok** (`NIU-FENCE`), dan setiap pergantian model menyala fence.

---

## 3. Kenapa seketat ini (konteks — bukan tanpa alasan)

- **D-0001 (2026-08-18):** auto-switch ke 9router/juan/gemini/gemma/zai/gratislonggar **merusak state, menumpuk kesalahan, dan menelan dokumentasi**. → keputusan: satu keluarga Zen saja.
- **D-0002 (2026-08-21):** suksesi ke nemotron-3-ultra-free (primary) + hy3-free (alternate). `not_doing`: *fallback lintas keluarga, multi-agen, silent hop*.
- `TELEGRAM-UNIFY.md`: 5 thread Telegram masih di model "bukan otak" (gemini/gc/cf/zai/gemma via 9router) — dianggap "mesin cacat" yang menghilangkan dokumentasi.

Jadi keketatan ini adalah **reaksi terhadap kejadian nyata** (dokumentasi hilang karena model lemah + silent hop).

---

## 4. Di mana "terlalu ketat"-nya (temuan spesifik)

### 🔴 Temuan A — Fallback resmi (hy3) ternyata juga di-fence oleh runtime

`MODEL.policy.yaml` menetapkan `on_rate_limit: same_family_fallback → hy3-free` (fallback yang **disahkan**). Tapi `niu_corelib.py` memperlakukan **setiap** pergantian model — termasuk `nemotron-3-ultra-free → hy3-free` yang keduanya *allowed* — sebagai `model_switch` yang:
1. menulis `HANDOFF.md`,
2. menyalakan **fence**,
3. menyuntik "dunia tugas sebelumnya TIDAK dilanjutkan".

**Akibat:** jalur fallback yang sah malah dihukum seperti model asing. Ini kemungkinan besar sumber perasaan "terlalu ketat". Ini juga **inkonsistensi internal** antara niat (D-0002) dan runtime.

### 🟠 Temuan B — Ritual penuh untuk ganti antar 2 model yang diizinkan

Hukum 3 ("ganti model = ganti dunia") secara tekstual tidak membedakan ganti **ke model asing** vs ganti **antar sesama keluarga**. Bila maksudnya hanya melindungi dari silent hop ke model asing/lemah, ritual penuh untuk sesama keluarga terlalu berat.

### 🟠 Temuan C — `forbidden_thinkers` adalah daftar hitam eksplisit yang panjang

12+ ID diblokir eksplisit. Protektif, tapi membuat menambah model baru = mengedit file ter-segel (ritual berat) sehingga operator cenderung "melanggar" daripada mengubah policy.

---

## 5. Inkonsistensi hukum (stale — harus dibersihkan apapun arahnya)

| # | Lokasi | Isi | Masalah |
|---|---|---|---|
| I1 | `agents/_shared/INCIDENT.md` | cron unpinned → `--model big-pickle` | `big-pickle` sudah **pensiun** (D-0002) — bila diikuti, justru re-pin ke model terlarang |
| I2 | `agents/_shared/INCIDENT.md` | zen 5xx/429 → retry ke `deepseek-v4-flash-free` | model itu **pensiun** — fallback darurat menunjuk ke model terlarang |
| I3 | `agents/_shared/PATHS.md` | "47 `SKILL.md`" | stale — sekarang **68** |
| I4 | `core/STATE.yaml` `health.cron_agent_reach_watch` | `error — pin model lama, wajib re-pin` | sudah tercatat tapi belum beres |
| I5 | `core/runtime/session-models.json` | ada `gpt-5.6-sol` (20260821_012843/012932) + `deepseek-v4-flash` tanpa prefix | model di luar keluarga muncul di log sesi — perlu klarifikasi (satelit/thread non-core?) |

---

## 6. Opsi pelonggaran (butuh keputusan `zaryu`)

| Opsi | Perubahan | Risiko | Rekomendasi |
|------|-----------|--------|:-----------:|
| **A. Sesama keluarga tanpa fence** | nemotron ↔ hy3 bebas switch tanpa HANDOFF/fence; fence **tetap** untuk model asing/forbidden | Sangat rendah — keduanya sudah disahkan sebagai otak | 🥇 **paling presisi** |
| **B. Perluas allowlist** | tambah 1–2 model alternatif lain di Zen (tetap 1 keluarga) | Rendah — perlu verifikasi kuota | alternatif |
| **C. Fallback lintas-keluarga saat limit** | saat Zen habis, izinkan fallback ke provider yang ditunjuk (mis. via 9router) + HANDOFF wajib | Sedang — membuka kembali pintu yang ditutup D-0001 | hanya jika disengaja |
| **D. Bebas penuh** | model free-tier apa pun boleh berpikir; handoff/fence opsional | Tinggi — persis risiko D-0001 | tidak disarankan |

**Catatan:** Opsi A/B/C/D bersifat kumulatif — mis. A+B = "sesama keluarga tanpa fence" + "tambah alternatif".

---

## Lampiran — Perintah verifikasi

```bash
# Status fence saat ini
python3 scripts/niu-handoff.py --status

# Model yang diizinkan di runtime (hardcoded)
grep -n "ALLOWED_MODELS" scripts/niu_corelib.py

# Keputusan yang disegel
cat core/ledger/decisions/D-0001.yaml core/ledger/decisions/D-0002.yaml
```

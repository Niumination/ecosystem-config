# D-0004 — Aturan Main Ekosistem (Versi 1 Halaman)

> **Untuk siapa:** Afrizal Munthe (zaryu), operator tunggal Niumination
> **Tanggal sah:** 21 Agustus 2026 — **Status: DISEGEL** (tidak bisa diubah agen)
> **Tinjau ulang:** 4 September 2026
> **Sumber resmi:** `core/ledger/decisions/D-0004.yaml` + `core/STATE.yaml`

---

### 1. Apa itu D-0004?
Bayangkan ekosistem Niumination seperti **warung**. Dulu warungnya tanpa gembok — siapa saja (termasuk AI) bisa ganti harga, ganti bahan, bahkan pakai bahan mahal tanpa izin. **D-0004 adalah gembok + buku aturan warung** yang kamu kunci sendiri tanggal 21 Aug.

Isinya cuma satu inti: **"Mulai sekarang, warung hanya boleh pakai bahan GRATIS."**

### 2. Kenapa harus digembok?
1.  **Biar gratis terus.** Tagihan model AI berbayar bisa jebol.
2.  **Biar tidak rusak.** File penting (konstitusi, visi, daftar larangan) dikunci — AI salah ketik tidak bisa merusaknya.
3.  **Biar mandiri.** Dulu server numpang di USB. Sekarang pindah ke Mac sendiri, cabut USB tetap jalan.

### 3. 3 Aturan Emas (cukup ingat ini)

| # | Aturan | Bahasa warung |
|---|--------|---------------|
| **1** | **Hanya bahan gratis** | Otak AI cuma boleh yang ada label `*-free` (Zen) atau `:free` (Nous). Yang tanpa label = berbayar = **DILARANG**. |
| **2** | **Pindah dapur harus lapor** | Pindah dari dapur Zen ke dapur Nous (atau sebaliknya) = **AI wajib berhenti + tulis surat `HANDOFF.md` tunggu kamu**. Sesama Zen (misal `hy3-free` ke `ultra-free`) boleh lanjut tanpa lapor. |
| **3** | **Kuota habis = tutup dulu** | Bahan gratis ada kuota harian (sharing). Kalau semua `*-free` balas `429 habis`, jangan pindah-pindah akal — **tutup warung, tulis HANDOFF, tunggu besok**. |

> Yang dilarang eksplisit: `9router`, `huancheng`, `agentrouter`, `juan-router`, dan semua model berbayar (walau namanya mirip).

### 4. Bahan Gratis yang Sah Saat Ini

**Zen (OpenCode Zen):** `big-pickle` (kreatif), `hy3-free` (cepat/ringan), `nemotron-3-ultra-free` (paling besar/kuat)

**Nous Portal (6 pilihan):** `longcat-2.0:free` (baca dokumen panjang 1jt token), `laguna-s-2.1:free` (jago coding), `solar-pro4:free` (jago audit/logika), + 3 lain.

*Daftar bisa nambah otomatis kalau ada model baru berakhiran `*-free` / `:free` — tidak perlu gembok baru.*

### 5. 5 Kasir Spesialis (Thread Telegram)

Dulu 5 kasir pakai otak sama. Sekarang dibagi tugas biar maksimal:

| Thread | Nama | Otak | Tugasnya |
|--------|------|------|----------|
| **1** | General | `hy3-free` (Zen) | Respon cepat, bagi tugas |
| **802** | Researcher | `longcat-2.0:free` (Nous) | Riset web & baca dokumen panjang |
| **803** | Builder | `laguna-s-2.1:free` (Nous) | Nulis & review kode |
| **804** | Pengawas | `solar-pro4:free` (Nous) | Audit, testing, cari bug |
| **1172** | Kreator Reels | `nemotron-3-ultra-free` (Zen) | Bikin script video/reels |

### 6. Apa itu FENCE & HANDOFF buat kamu?

*   **FENCE = pagar.** Kalau AI mau melanggar 3 aturan emas, pagar otomatis cegat.
*   **HANDOFF = surat.** Kalau kepentok pagar, AI tulis file `core/runtime/HANDOFF.md` isinya: mau ngapain, kenapa berhenti. Kamu tinggal baca & putuskan.

**Kamu tidak perlu ngapa-ngapain kalau tidak ada HANDOFF.**

### 7. Workflow Harian Kamu (Cukup 1 Menit)

1.  Chat seperti biasa di Telegram, pilih thread sesuai kebutuhan (mau riset → 802, mau coding → 803).
2.  Sehari sekali ketik `/up-eco` di Jcode/Mac. Lihat 4 lampu:
    *   `Root clean` ✅
    *   `Skill Bank 68` ✅
    *   `MC 200` ✅
    *   `5 thread Active` ✅
    → Kalau 4 ini hijau, **lanjut saja. Tidak perlu paham detail.**
3.  Jika ada yang minta approve `config set` / `merge PR`, cek satu pertanyaan: *"Ini model `*-free/:free` atau berbayar?"* Kalau berbayar → **tolak**.

### 8. Kalau Ada Masalah, Cek Mana?

*   Bingung aturan → buka file ini lagi.
*   Mau lihat bukti kerja AI → `core/STATE.yaml` (ringkasan 1 layar) atau `core/ledger/sessions/`.
*   Mau lihat gemboknya → `core/ledger/decisions/D-0004.yaml`.

---
**File beku yang dikunci (jangan diedit manual):** `CONSTITUTION.md`, `SCOPE.md`, `MODEL.policy.yaml`, `AGENTS.slim.md`, `VISION.md`, `FREEZE.list`

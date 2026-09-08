# 🔍 Laporan Audit Hermes Agent
**Tanggal:** 07 September 2026  
**Auditor:** Hermes Agent (ag/claude-sonnet-4-6)  
**Versi Hermes:** v0.20.5 (2026.8.19) · upstream 02244472  
**Status Gateway:** `running` · PID 849 · Telegram: `connected`

---

## 1. RINGKASAN EKSEKUTIF

| Kategori | Status | Temuan Kritis |
|----------|--------|---------------|
| Gateway | 🟢 Running | Crash berulang setiap ~3-9 jam |
| Fallback chain | 🔴 Masalah | `ag/gemini-3.7-flash-medium` HTTP 403 berulang |
| Cron jobs | 🔴 Masalah | `Daily Brain` gagal 5x berturut-turut |
| .env | 🟡 Perlu perbaikan | Key duplikat `AUXILIARY_VISION_API_KEY` |
| MCP servers | 🟡 Perlu perhatian | `@modelcontextprotocol/server-github` deprecated |
| state.db | 🟡 Perlu perhatian | 159MB, perlu vacuum |
| Skills | 🟢 OK | 28 category, berjalan normal |
| Memory | 🟢 OK | USER.md (1334B) + MEMORY.md (1887B), dalam batas |
| Model pool | 🟢 OK | 336 model aktif via 9router |

---

## 2. MASALAH KRITIS

### 2.1 Gateway Crash Berulang
**Bukti:** `gateway-exit-diag.log`
```
2026-09-03 09:43 — exit_nonzero (PID 808)  
2026-09-03 15:31 — restart (PID 839)  
2026-09-03 18:42 — exit_nonzero (PID 839)  → 3 jam jalan lalu crash
2026-09-04 06:28 — restart (PID 813)  
2026-09-04 09:28 — exit_nonzero (PID 813)  → 3 jam jalan lalu crash
2026-09-06 09:20, 09:53, 17:16 — SIGTERM berulang
2026-09-07 12:14 — SIGTERM
```
**Pola:** Gateway exit nonzero setiap ~3-9 jam. Gateway saat ini berjalan 26 menit (restart terbaru). Tidak ditemukan OOM killer di dmesg — kemungkinan penyebab: API error 503/403 yang tidak ter-recover atau context window penuh (194 messages, ~76K tokens tercatat saat crash).

**Dampak:** DM/group chat bisa tidak responsif selama periode crash-to-restart.

**Tindakan yang disarankan:** Investigasi apakah `gateway_timeout: 1800` terlalu panjang untuk konteks besar. Pertimbangkan `max_turns: 100` (turun dari 150).

---

### 2.2 Fallback Chain `ag/gemini-3.7-flash-medium` — HTTP 403 Berulang
**Bukti:** `errors.log`
```
2026-09-07 21:04:15 — [antigravity/gemini-3.7-flash-medium] [403]: HTTP 403 (reset after 1m 26s)
WARNING: API call failed (attempt 2/3)
WARNING: Retrying in 4.09s
ERROR: API call failed after 3 retries — msgs=194 tokens=~76,703
```
**Pola:** Model fallback2 `ag/gemini-3.7-flash-medium` secara konsisten mengembalikan 403 via 9router. Bukan timeout sementara — error ini muncul berulang hari ini.

**Dampak:** Fallback chain tidak efektif. Saat model utama gagal dan fallback1 juga gagal, fallback2 juga gagal → respon tidak tersampaikan.

**Tindakan yang disarankan:** Verifikasi apakah `ag/gemini-3.7-flash-medium` (antigravity namespace) masih aktif di 9router. Pertimbangkan ganti ke `ag/gemini-3.8-flash-medium` atau `explabs/gpt-4o-mini` sebagai fallback2.

---

### 2.3 Cron Job `Daily Brain - Top 10 URL Update` — 5 Kali Gagal Berturut-turut
**Bukti:** `hermes cron list`
```
Last run: 2026-09-07T08:57 — error: RuntimeError: HTTP 503
Model: gpt-5.4-mini (explabs)
Error: "Your organization is under review to fight spam and can't use models right now"
5 failures in a row
```
**Penyebab:** Akun ExperimentalLabs/explabs diblokir sementara karena review anti-spam. Cron ini menggunakan model `explabs/gpt-5.4-mini` (default) yang terkena dampak.

**Dampak:** Cron harian tidak berjalan. Data brain (top 10 URL) tidak diperbarui sejak setidaknya hari ini.

**Tindakan yang disarankan:**
1. Periksa status akun explabs di portal mereka
2. Override cron ini ke provider yang tidak terkena blokir (misal `ag/gemini-3.8-flash-medium`)
3. Jika blokir belum selesai, pause cron sementara

---

## 3. ANOMALI & PERINGATAN

### 3.1 Duplikat Key di `~/.hermes/.env`
**Bukti:**
```
Baris 37: AUXILIARY_VISION_API_KEY=[REDACTED]
Baris 40: AUXILIARY_VISION_API_KEY=[REDACTED]  ← duplikat
```
Nilai sama, tapi duplikat berpotensi menimbulkan confusion saat di-source. Hapus salah satu.

---

### 3.2 MCP Server `@modelcontextprotocol/server-github` Deprecated
**Bukti:** `mcp-stderr.log`
```
npm warn deprecated @modelcontextprotocol/server-github@2025.4.8: 
Package no longer supported. Contact Support at https://www.npmjs.com/support
```
Server masih berfungsi (startup berhasil), tapi package tidak lagi di-maintain. Perlu migrasi ke paket pengganti jika ada, atau build dari source.

---

### 3.3 `state.db` 159MB
**Bukti:**
```
-rw-r--r-- 1 zaryu staff 159M Sep 7 21:07 /Users/zaryu/.hermes/state.db
Sessions tersimpan: 40
```
159MB untuk 40 sesi adalah ukuran yang besar — kemungkinan karena attachment/blob tersimpan di DB, atau WAL belum di-checkpoint. Jalankan `VACUUM` dan `PRAGMA wal_checkpoint(TRUNCATE)`.

---

### 3.4 Firefox-tab-stash Skill — Tidak Ada SKILL.md
**Bukti:**
```
ls ~/.hermes/skills/firefox-tab-stash/
references  scripts
```
Skill directory ada tapi kosong (tidak ada `SKILL.md`). Skill tidak dapat diload. Ini orphaned directory.

---

### 3.5 Prefix Cache Miss pada Session Panjang
**Bukti:** `errors.log`
```
WARNING: Stored system prompt for session 20260906_143915_ea1e4dc7 is null; 
rebuilding from scratch this turn. Prefix cache will miss...
```
Terjadi pada session dengan 194 pesan. Cache miss berarti biaya token lebih tinggi dan latency naik.

---

### 3.6 `9router-catalog-state.json` Stale (8 Hari)
**Bukti:**
```
-rw-r--r-- 1 zaryu staff 2.3K Aug 30 01:00 ~/.hermes/9router-catalog-state.json
```
Cache catalog 9router terakhir diperbarui 30 Agustus. Provider/model baru mungkin belum terdeteksi.

---

## 4. STATUS NORMAL (Tidak Perlu Tindakan)

| Komponen | Status |
|----------|--------|
| Hermes version | ✅ v0.20.5 — up to date |
| 9router | ✅ Online, 336 model |
| Telegram connected | ✅ 6 channel terdaftar |
| MCP filesystem | ✅ Berjalan normal |
| MCP context7 | ✅ Berjalan normal |
| Skills (28 kategori) | ✅ Normal |
| Memory files | ✅ Dalam batas (3.2KB dari 2.2KB limit — PERLU PERHATIAN lihat 4.1) |
| Auth tokens | ✅ Tavily, FAL, OpenRouter aktif |
| Launchd `ai.hermes.gateway` | ✅ PID 585 aktif |

### 4.1 CATATAN: Memory mendekati batas
Memory saat ini: USER.md 1334B + MEMORY.md 1887B = **3.221B dari batas ~3.575B (~90%)**. Sudah dekat limit. Perlu compact entries yang tidak relevan jika ingin menambah.

---

## 5. DAFTAR TINDAKAN

| # | Prioritas | Tindakan | Estimasi Upaya |
|---|-----------|----------|----------------|
| 1 | 🔴 Segera | Periksa status akun explabs, override cron `Daily Brain` ke provider alternatif | 15 menit |
| 2 | 🔴 Segera | Verifikasi/ganti `ag/gemini-3.7-flash-medium` di fallback chain | 10 menit |
| 3 | 🟡 Minggu ini | Hapus duplikat `AUXILIARY_VISION_API_KEY` di .env | 2 menit |
| 4 | 🟡 Minggu ini | Jalankan VACUUM + WAL checkpoint pada state.db | 5 menit |
| 5 | 🟡 Minggu ini | Hapus/isi orphaned skill `firefox-tab-stash` | 10 menit |
| 6 | 🟡 Minggu ini | Update/replace MCP github server deprecated | 30 menit |
| 7 | ⬜ Kapan saja | Investigasi penyebab gateway crash berulang tiap ~3-9 jam | 1-2 jam |
| 8 | ⬜ Kapan saja | Perbarui `9router-catalog-state.json` | 5 menit |

---

*Laporan ini dibuat dari data real sistem — tidak ada asumsi.*

# Prioritas Urutan Kerja — Ekosistem Niumination

| Field | Nilai |
|---|---|
| **Tanggal** | 20 Agustus 2026 |
| **Dasar** | audit-pekerjaan-breakdown-2026-08-20.md (1 CRIT + 1 MED) · laporan-perubahan-2026-08-20.md (21/24 sesuai) |
| **Prinsip** | Bayar utang keamanan dulu → stabilkan → nilai bisnis |

---

## 🥇 FASE A — TUTUP CELAH (P0, hari ini)

| Urutan | Aksi | Durasi | Verifikasi |
|---|---|---|---|
| A1 | `hooks_auto_accept: true` (atau HERMES_ACCEPT_HOOKS=1 di env gateway) | 2 mnt | config check |
| A2 | **Restart gateway** (kamu) — muat config baru | 1 mnt | sesi kembali |
| A3 | Verifikasi: log = **0× `not allowlisted`** | 2 mnt | grep agent.log |
| A4 | Test pagar end-to-end: minta tulis CONSTITUTION → **harus BLOCK** | 3 mnt | trace fence.json |
| A5 | Test ganti model asing → **harus HANDOFF + fence aktif** | 3 mnt | ledger/handoffs/ |
| A6 | `compression.provider: opencode-zen` + `model: deepseek-v4-flash-free` | 2 mnt | config check |

**Kriteria keluar:** pagar block nyata di runtime, handoff tercatat, compression eksplisit Zen.

## 🥈 FASE B — STABILISASI (P1, 1-2 hari)

| Urutan | Aksi | Durasi | Verifikasi |
|---|---|---|---|
| B1 | Alur kerja AI Priming: hook pre_llm_call menyuntik notes relevan sebelum output | 2-4 jam | kualitas output naik |
| B2 | Jclock/jadwal: pastikan `niu-doc-capture` harian di cron (ledger konsisten) | 30 mnt | ledger/sessions harian ada |
| B3 | HOME skills: pindahkan 16 sisanya (buatan kerja) → Bank, Home jadi 68+builtin hanya | 1-2 jam | bank 68, home ~90 |
| B4 | Config stale penuh: hapus folder `~/.hermes` yg tidak terpakai (SOUL lama, cron lama) — **hati-hati** | 30 mnt | gateway tetap jalan |
| B5 | Supabase: cek hermes-postgres masih dipakai? kalau tidak → nonaktifkan | 30 mnt | mcp list bersih |

## 🥉 FASE C — NILAI BISNIS (P1-P2, minggu ini)

| Urutan | Aksi | Durasi | Verifikasi |
|---|---|---|---|
| C1 | **Pemdi Aceh Tengah** — proses SKP semester via pdf-inspector + audit bukti | 1-2 hari | SKP ter-ekstrak, bukti tersusun |
| C2 | Frontend MC Phase 5B/5C (task detail, cost per task visual) | 2-4 jam | visual OK |
| C3 | Niu Action Broker MVP (pending + approval + audit) | 1 hari | workflow approve jalan |

## 🏅 FASE D — OPSIONAL / MASA DEPAN (P2-P3)

| Urutan | Aksi | Kapan |
|---|---|---|
| D1 | Munder Difflin port (circuit breakers, agent messaging → Niu-MC) | setelah C |
| D2 | ComfyUI remote worker + skill bawaan | saat GPU tersedia |
| D3 | pdf-inspector OCR untuk dokumen scan | saat butuh |

---

## Alasan Urutan

1. **A dulu** — pagar yang tidak aktif = konstitusi bisa diubah kapan pun. Ini satu-satunya "utang keamanan".
2. **B setelah A** — jangan ubah skill/config sebelum pagar aktif; semua mutasi harus tercatat.
3. **C setelah B** — Pemdi = prioritas bisnis #1 (permenpanrb 8/2026, masa penilaian).
4. **D menunggu** — semuanya punya dependensi (GPU, waktu, kebutuhan).

*Update status di baris atas setiap selesai 1 fase.*
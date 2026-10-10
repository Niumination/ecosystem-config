# Kelas Niumination — Fase 2 Ditunda (T-01/T-02)

Tanggal: 10 Okt 2026 · Status: **SELESAI (11 Okt 2026)** — lihat `kelas-fase2-supabase-live.md`

Proyek: `sites/kelas/` · repo `github.com/Niumination/kelas` (private)

## Status

T-01 dan T-02 **SELESAI** via Composio. Laporan lengkap ada di
`kelas-fase2-supabase-live.md`. Dokumen ini hanya catatan historis penundaan.

## Implikasi

- Aplikasi tetap jalan **mode demo** (tanpa `.env.local`): konten bisa dibaca,
  auth + pembayaran nonaktif.
- 6 migrasi (`0001_init` … `0006_bank_soal`) menunggu kredensial Supabase nyata.
- Bloker T-01: 3 var — `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`,
  `SUPABASE_SERVICE_ROLE_KEY` — disimpan ke `~/.hermes/.env` (mode 600),
  **jangan pernah lewat chat**.
- CLI `supabase` belum terpasang (belum perlu, dipasang saat T-02 dieksekusi).

## Lanjutan setelah bloker terbuka

1. Perbaiki/re-otorisasi Composio, **atau** buat project Supabase manual di
   dashboard + isi `~/.hermes/.env`.
2. `npm i -g supabase` → `supabase link` → jalankan 6 migrasi (T-02).
3. Verifikasi tabel `enrollments`/`purchases` + RLS aktif.
4. T-03 (OAuth GitHub/Google) dan T-04 (Midtrans) menyusul.

## Yang dikerjakan selagi menunggu (tanpa Supabase)

- Vercel CLI terautentikasi (`vercel whoami` → `archk4li-6237`, exit 0) — T-06 siap
  begitu env lengkap.
- QA lokal: `npm run dev` + smoke rute utama.
- T-10: gitleaks — 8 temuan semua artefak `.next/` (gitignored), nol secret nyata.

## Bukti

- `manage_connections status` → supabase `connected=false`
- `grep -c "SUPABASE" ~/.hermes/.env` → 0
- `which supabase` → not found (exit 127)
- `vercel whoami` → `archk4li-6237` (exit 0)
- `gitleaks detect --no-git` → 8 findings, semua `.next/*`

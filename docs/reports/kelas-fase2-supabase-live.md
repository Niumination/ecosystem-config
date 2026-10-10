# Kelas Niumination — Fase 2 Selesai: Supabase Project + Migrasi

Tanggal: 11 Okt 2026
Proyek: `sites/kelas/` · repo `github.com/Niumination/kelas` (private)
Project Supabase: `kelas-niumination` · ref `xjefqbhavevfkhcunwmc` · region `ap-southeast-1`

## Status: DONE

T-01 (Supabase project) dan T-02 (migrasi) **SELESAI** via Composio MCP.
Penundaan sebelumnya (10 Okt) sudah dicabut — Composio connector `supabase`
berhasil diaktifkan, project baru dibuat, dan 6 migrasi ter-apply penuh.

## Yang dikerjakan

1. **Project Supabase baru** `kelas-niumination` dibuat via `SUPABASE_CREATE_A_PROJECT`
   - Region: `ap-southeast-1` (terdekat dari Aceh Tengah)
   - Status: `ACTIVE_HEALTHY` — semua layanan sehat (auth, db, pooler, rest, storage, realtime)
   - Database: `db.xjefqbhavevfkhcunwmc.supabase.co`

2. **Kredensial tersimpan** di `~/.hermes/.env` mode 600:
   - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_DB_PASS`
   - Nilai tidak pernah tampil di chat atau log.

3. **6 migrasi ter-apply** via `SUPABASE_APPLY_A_MIGRATION` (berurutan, idempotency key per berkas):
   - `0001_init` → 15 tabel + 7 tipe enum + indexes + trigger profil otomatis
   - `0002_rls` → RLS aktif di semua tabel + 14 policy + 6 fungsi akses (punya_akses_materi, tandai_selesai, proses_webhook, dll)
   - `0003_seed` → 1 kelas + 6 modul + 22 pelajaran (5 modul gratis, 1 proyek akhir berbayar)
   - `0004_kuis` → view `questions_publik` (buang kolom `kunci`) + fungsi `kuis_modul`, `nilai_kuis`, `rekap_kuis`
   - `0005_sertifikat` → fungsi `terbitkan_sertifikat`, `syarat_sertifikat`, `sertifikat_saya`, `batalkan_sertifikat`
   - `0006_bank_soal` → 5 kuis + 23 soal (5 modul, nilai lulus 70)

4. **Verifikasi pasca-migrasi** (bukan sekadar response body):
   - `SUPABASE_LIST_MIGRATION_HISTORY` → 6 entries, semua versioned
   - `SUPABASE_RUN_READ_ONLY_QUERY` → row counts: courses=1, modules=6, lessons=22, quizzes=5, questions=23, certificates=0
   - Schema check via `GET_TABLE_SCHEMAS` — butuh `table_names` parameter, belum di-query ulang (next step)

5. **Env vars Vercel** — 3 var (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`) diset di project `archk4lis-projects/kelas` production.

6. **Redeploy production** → `https://kelas-5i7x94dt0-archk4lis-projects.vercel.app` — status READY, 200 OK.

## Catatan DNS

Domain custom `kelas.niumination.web.id` masih flapping (split-brain NS idwebhost↔Vercel).
Probe DNS di akhir sesi ini menunjukkan NS kosong — perlu verify ulang `vercel domains verify`.
Deployment URL Vercel langsung stabil 200.

## Langkah berikutnya

1. T-03: OAuth GitHub/Google (butuh akun OAuth)
2. T-04: Verifikasi bisnis Midtrans (minggu ke-5)
3. T-17: Resend SMTP (butuh akun Resend)
4. DNS verify ulang → pastikan NS uniform Vercel
5. Schema detail check via `SUPABASE_GET_TABLE_SCHEMAS` dengan parameter `table_names`
6. Smoke test login flow di production (butuh T-03)

## Bukti

- Composio session: `feel` (MCP multi-tool)
- `SUPABASE_CREATE_A_PROJECT` → project ref `xjefqbhavevfkhcunwmc`
- `SUPABASE_GETS_PROJECT_S_SERVICE_HEALTH_STATUS` → `ACTIVE_HEALTHY`
- `SUPABASE_LIST_MIGRATION_HISTORY` → 6 entries (0001–0006, semua sukses)
- `SUPABASE_RUN_READ_ONLY_QUERY` → courses=1, modules=6, lessons=22, quizzes=5, questions=23
- `vercel env ls production` (dari `sites/kelas`) → 3 var Supabase terdaftar
- `vercel deploy --prod` → `dpl_Aehc8HCy6g6riHctNztP5aoTLE6C`, READY, 200
- `~/.hermes/.env` mode 600, 4 var Supabase (3 app + 1 db_pass)

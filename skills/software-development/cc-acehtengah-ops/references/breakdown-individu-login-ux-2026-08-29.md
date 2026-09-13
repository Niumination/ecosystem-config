# Session 29-Agu-2026 (final stretch): breakdown-to-individu, login/logout UX, button placement

Companion to `status-page-roles-format-2026-08-29.md` and `breakdown-explorer-deterministic.md`.
Captures the user-corrected deltas after live testing by Afrizal (commits `34f6980`, `7cc9a76`).

## User corrections this round (FIRST-CLASS preferences)

1. **Tombol "Pecah Jawaban" harus PALING ATAS** di output AI — setelah judul
   "Hasil Analisis AI", SEBELUM visualisasi/narasi. User memindahkannya dari
   bawah (setelah rekomendasi). Jangan sembunyikan di bawah lipatan.
2. **Drill-down harus sampai individu (ByNameByAddress)** — user mengetes
   PBI → Bebesen → Kemili → desil, lalu ingin pecah lagi sampai daftar penerima
   dengan identitas. Publik bisa turun sampai desa; level individu WAJIB login
   role DTSEN. Jangan batasi mindmap di level desil.
3. **Halaman publik wajib punya tombol Login** — user tidak menemukan menu
   login di halaman publik (harus ketik URL /login manual). Header harus
   menampilkan `🔐 Login` saat publik, `👤 Akun + 🚪 Logout` saat login.
4. **Logout → kembali ke /dashboard, BUKAN /login** — user menganggap logout
   harusnya ke halaman publik dashboard, bukan ke halaman login.

## scope=individu (role-gated) di /api/dtsen/breakdown

- Params: `scope=individu&kecamatan=<UPPER>&desa=<UPPER>&desil=<N>`.
- Auth: `decideDataAccess(role, 'RESTRICTED_PERSONAL')` — hanya
  DTSEN_LOOKUP/SUPERADMIN. Publik → 401 dengan pesan "login dengan akun
  berrole DTSEN_LOOKUP/SUPERADMIN".
- Query: `dtsenIndividu.findMany` (namaMasked, desil, bansos) on PUBLISHED
  release, orderBy namaMasked asc, `take: 200` cap.
- **Audit WAJIB**: `buildAuditEntry({admin, aksi:'BREAKDOWN_INDIVIDU', ...})`
  → `dataAccessAudit.create` dengan mapping `action: entry.aksi`. Action baru
  `BREAKDOWN_INDIVIDU` ditambahkan ke union `AuditAction` di data-gate.ts.
- UI (BreakdownExplorer): di level desil (path.length===3) tampil baris
  "👤 Pecah sampai daftar penerima (By-Name By-Address)" — tombol per desil
  → tabel nama termask + desil + status PBI. Nama selalu termask (UU 27/2022);
  nama lengkap TIDAK pernah disimpan mentah di DB.

## Verified live

- Publik request scope=individu → `ok:false, error:"...login dengan akun
  berrole DTSEN_LOOKUP/SUPERADMIN"` (401).
- master_admin (SUPERADMIN) BEBESEN/KEMILI/desil 1 → 200 baris nama termask
  (cap 200), masing-masing `{nama, desil, bansos}`.
- Supabase langsung port 5432 kadang unreachable dari lokal; pooler 6543
  (DATABASE_URL) stabil — jangan salah diagnosa kode saat itu terjadi.

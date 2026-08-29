# Ecosystem Status — 2026-08-29

## 🔥 Selesai hari ini — cc-acehtengah (hotfix/meeting-ready, PROD `5dd47d7`)

### Fitur baru
1. **Role `DTSEN_ROOT`** (otoritas tertinggi) — BNBA lengkap: nama asli + NIK terdekripsi
   - Nama & NIK disimpan **terenkripsi AES-256-GCM** (`namaAsliEnc`/`nikEnc`, key `DTSEN_DATA_KEY`)
   - SUPERADMIN tetap termask; hanya DTSEN_ROOT yang lihat lengkap
   - Akun `dtsen_root` (password di vault/cc-acehtengah.env)
2. **Tombol "Pecah Jawaban"** di PALING ATAS output AI — mindmap ala NotebookLM:
   kabupaten → kecamatan → desa → desil → **daftar penerima BNBA**
   - DETERMINISTIK tanpa LLM (hemat usage model AI) — endpoint `/api/dtsen/breakdown`
   - Blocker BNBA untuk publik + **tombol 🔐 Login untuk melanjutkan**
3. **Alur login/logout**: publik lihat tombol Login; logout → `/dashboard` (bukan login)
4. **Halaman `/dashboard/status`** mandiri: registry 7 sumber + diagram relasi SVG
5. **Format angka id-ID** konsisten (12.345) di semua output
6. **Demo data DIHAPUS** total — output murni sumber nyata (SPLP → DB → BAPPEDA)
7. Fix case-insensitive kecamatan (Linge = 5.234 jiwa ✅)
8. Re-import DTSEN v3: **235.011 individu** terenkripsi + 2.060 agregat PUBLISHED

### Kredensial baru (vault/cc-acehtengah.env)
- `dtsen_root` / `cPtnkHE7NYD3Gg_s` (DTSEN_ROOT — ganti password segera)
- `DTSEN_DATA_KEY` (43 char, Vercel + .env.local) — WAJIB dijaga

## 📌 Backlog lanjutan
- [ ] **Sinkronkan `main`** — fast-forward ke hotfix (60 commit, siap merge)
- [ ] Hapus branch kosong: `hotfix/llm-reliability`, `origin/pabrik-aplikasi`
- [ ] SPLP DTSEN API: JWT baru → data live (BAPPEDA jadi cadangan)
- [ ] Ganti password `dtsen_root` & `master_admin` setelah login

## Dokumen baru
- `services/cc-acehtengah/docs/LAPORAN-BRANCH-2026-08-29.md` — laporan lengkap 8 branch
- `services/cc-acehtengah/docs/ai/SESI-2026-08-29-dtsen-root-bnba.md` — catatan sesi detail

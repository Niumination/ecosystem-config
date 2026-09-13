# Vault Credential Snapshot — pola simpan SEMUA kredensial proyek ke vault (29 Agu 2026)

Kasus: user minta "simpan semua kredensial cc-acehtengah di vault" setelah sesi panjang
env swap (AI key, SPLP, akun admin baru). Pelajaran: `vault/secrets.zsh` (provider keys)
BUKAN satu-satunya tempat — proyek aplikasi butuh file vault khusus per-proyek agar
semua env (DB, OAuth, admin accounts) punya satu salinan lokal yang aman.

## Output yang benar

`~/Desktop/Niumination/vault/<project>.env` — satu file per proyek:
- format `export CC_<KEY>="<value>"` (prefix nama proyek, sourceable zsh)
- **chmod 600** (`os.chmod(path, 0o600)`)
- **git-ignored otomatis** via root `.gitignore` (`vault/` + `**/vault/` sudah ada) —
  verifikasi `git check-ignore vault/<project>.env` → exit 0
- header komentar: sumber, tanggal, peringatan jangan commit, daftar env yang TIDAK tersedia

## Workflow (script python — nilai TIDAK pernah dicetak ke chat/terminal)

1. **Parse DUA file env** — `.env.local` (production-relevant, MENANG saat konflik) +
   `.env` (dev/legacy). Merge dict: `{**env_main, **env_local}`.
2. **Kelompokkan keys** (AI / Database / API eksternal / Auth & Setup / Cron / Lainnya)
   supaya file terbaca manusia; key yang TIDAK ada di file mana pun → tulis baris
   komentar `# CC_X=""  # (tidak ada di .env/.env.local — cek Vercel env)` — bukan
   di-skip diam-diam.
3. **Akun admin** (username/password yang dibuat manual di DB) → section sendiri di
   file vault dengan komentar "SEGERA GANTI setelah login".
4. **Verifikasi tanpa bocorkan nilai:** print hanya `key = mask` di mana
   `mask = v[:6]+'...'+v[-4:]` untuk nilai panjang, `SET`/`EMPTY` untuk pendek.
   Jangan pernah `cat` file vault ke output.
5. **Referensi silang:** tambah `export CC_VAULT="$HOME/.../vault/<project>.env"` di
   `vault/secrets.zsh` + komentar ringkas isi file (tanpa nilai).

## Pitfall kritikal: env Vercel HIDDEN tidak bisa di-pull

- `vercel env pull --environment=production` mengembalikan **`[SENSITIVE]`** (11 chars)
  untuk env yang ditandai Sensitive di dashboard (JWT_SECRET, ADMIN_SETUP_TOKEN,
  CRON_SECRET, DTSEN_NIK_KEY, API keys). Nilai aslinya TIDAK bisa di-extract via CLI.
- Konsekuensi: file vault lokal TIDAK akan pernah 100% lengkap untuk env sensitive —
  tulis daftar "HANYA di Vercel — copy manual dari dashboard" di header file agar
  sesi berikut tahu persis apa yang perlu di-copy manual, bukan mengira file vault
  sudah lengkap.
- `vercel env ls` menampilkan nama + umur + environment tapi nilai = `Hidden`.
- Jangan coba workaround (decrypt, pull production + edit) — env sensitive memang
  didesain tidak bisa diambil kembali setelah di-set.

## Verifikasi akhir

```
git check-ignore vault/<project>.env   # exit 0 = aman dari commit
ls -la vault/<project>.env             # -rw------- (600)
grep -c "^export CC_" vault/<project>.env   # jumlah keys tersimpan
```

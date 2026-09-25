# Adopsi MC v4.0 Aether + Migrasi DB v3→v4

**Tanggal:** 26 September 2026
**Proyek:** `services/niu-mission-control/` (repo mandiri `Niumination/niu-mission-control`)
**Sumber:** `~/Downloads/mc-aether.zip` (arena/designarena)
**Commit:** `4cd7606` (v3) → `a051bd3` (v4 Aether + migrasi) — push ✅
**Status akhir:** 🟢 build hijau, test lulus, docs sinkron. MC **belum** dijalankan 24/7.

---

## Ringkasan

Bundle arena berisi **git worktree lengkap dengan `.git`**, bukan `.patch` (varian
non-patch — skill `arena-patch-adoption/references/non-patch-zip-variant.md`).
15 commit terakhir di bundle **semuanya sudah ada** di repo lokal — artinya
update v4 ada di *working tree tak ter-commit* (66 file, +3313/-965).

Adopsi dilakukan dengan `rsync -a --delete` + 8 exclude eksplisit. Verifikasi
dilakukan di copy bersih (`/tmp`) **sebelum** menyentuh repo asli.

Hasil akhir: **v4.0.0 Aether** terpasang penuh (M1–M11), DB v3 termigrasi tanpa
kehilangan data, dua bug ditemukan yang **tidak akan terlihat tanpa DB asli**.

---

## Dua bug yang hanya muncul dengan data v3

Test arena lulus **10/10 di DB kosong**. Di DB v3 asli, awalnya **7/10**.

### Bug 1 — `SQLITE_ERROR: no such column: assigned_agent`

`001_initial.sql` memakai `CREATE TABLE IF NOT EXISTS`. Kalau tabel v3 sudah ada,
statement itu **dilewati** — tapi `CREATE INDEX` di file yang sama **tetap jalan**
dan gagal karena kolom v3 berbeda:

```
CREATE INDEX IF NOT EXISTS idx_tasks_assigned ON tasks(assigned_agent);
→ SqliteError: no such column: assigned_agent
```

Skema v3 dan v4 memang tidak kompatibel: `agent_id` → `assigned_agent`,
10 kolom hilang, 14 kolom baru. Tiga tabel lain bermasalah serupa
(`cost_tracking`, `dispatches`, `system_logs`).

**Perbaikan:** `apex-ui/migrations/000_baseline_v3_to_v4.sql` — 5 `ALTER`, tidak
menghapus data apa pun.

### Bug 2 — Worker claim task lalu menggantung

`test-sse.mjs` 7/10: `queued` ✅ tapi `claimed`/`started`/`completed` ❌. Task
nyangkut dengan `next_retry_at` NULL.

Ini **bukan bug kode — murni data v3.** Seed v4 (`lib/server/db.ts`) eksplisit
memakai adapter `mock` untuk chief agar dev jalan tanpa Hermes CLI terinstall.
DB v3 punya `hermes` untuk semua agent → worker claim, memanggil Hermes CLI yang
tidak tersedia, tidak ada retry, task menggantung.

**Perbaikan:** migrasi menyamakan chief ke `mock`. Dua task menggantung dari
test run dikembalikan ke `inbox`.

Koreksi catatan: sempat terdiagnosis `inbox` menghalangi claim — salah.
`CLAIMABLE_STATUSES` hanya `['queued']`, jadi 15 task `inbox` tidak menghalangi.

---

## Isi migrasi

| Tabel | Perubahan |
|---|---|
| `tasks` | `agent_id` → `assigned_agent`; +14 kolom lifecycle; `pending` → `inbox` |
| `agents` | +9 kolom; `active` → `idle`; **chief `hermes` → `mock`** |
| `cost_tracking` | +6 kolom; `created_at` → `recorded_at` (v3 → `created_at_v3_legacy`) |
| `dispatches` | +3 kolom |
| `system_logs` | +`task_id`, +`metadata` |

> ⚠️ Install baru tanpa DB v3 **harus menghapus** file migrasi 000 — statement-nya
> `ALTER TABLE` dan akan gagal di DB kosong.

---

## Bukti

| Item | Perintah | Hasil |
|---|---|---|
| Reproduksi bug 1 | `python3 repro-migration.py` | `no such column: assigned_agent` |
| Uji migrasi (runner Node asli) | `node test-mig-node.mjs` | 000 ✅ + 001 ✅ · 12 tabel, 24 index, data 15/5/1 utuh |
| Backup pra-migrasi | `cp data/swarm_state.db vault/…` | 53248 bytes → `vault/_arsip-sensitif/mc-db-v3-20260926-023617.db` |
| Verifikasi backup | `python3 verify-backup.py` | 15 tasks / 5 agents identik dengan asli |
| Chief → mock | `python3 apply-chief-mock.py` | `hermes` → `mock`, 2 task `queued` → `inbox` |
| Build | `rm -rf .next && npm run build` | **exit 0** · `Compiled successfully in 93s` · 10 route statis |
| SQLITE_ERROR | `grep -c SQLITE_ERROR /tmp/mc-build-full.log` | **0** |
| Typecheck | `npx tsc --noEmit` | **0** error |
| Lint | `npm run lint` | **0** error (warning `exhaustive-deps` saja) |
| **Test SSE (DB termigrasi)** | `node scripts/test-sse.mjs` | **10 passed, 0 failed** |
| Retry/backoff | log dispatcher | `failed (retry 1/3, backoff 2s)` → `claimed` → `completed` |
| Auth matrix | 6 endpoint tanpa key | semua **401**; key salah **401** |
| Secret scan | `scripts/secret-scan-staged.py` | exit **0** |
| Push | `git push origin main` | `4cd7606..a051bd3` exit **0** |

`BUILD_ID=6ZWvq0VpCXMMyA_FI-BBx`

---

## Scale adopsi

- **16 endpoint API** baru (`/api/mc/*`, `/api/auth/*`), 2 dihapus
  (`/api/mc/dispatches`, `/api/mc/tasks/update`)
- **Auth mandatory** — scrypt, session httpOnly sameSite strict, API key
  timing-safe, middleware protect `/api/mc/*` + redirect `/login` `/setup`
- **`execSync python3` dihapus** dari semua route
- **better-sqlite3** WAL + 11 tabel + migration runner
- **SSE event bus** + state machine + dispatcher worker 3 detik, MAX_CONCURRENT 5
- **UI** — Kanban dnd-kit, ⌘K palette (cmdk), Living Orb, Tailwind 4
- **9 halaman** di route group `app/(app)/` + `login` + `setup`

---

## Catatan operasional

**`DB_PATH` = `path.resolve(cwd, '..', 'data')`** — server harus jalan dari
dalam `apex-ui/`, atau set `MC_DB_PATH`. Menjalankan
`node .next/standalone/server.js` dari `.next/standalone/` membuat path DB salah
→ `no such table: tasks`. Ini sempat terlihat seperti bug migrasi.

**`.env.local` sempat terhapus** oleh `rsync --delete` (file tidak ada di
exclude sisi tujuan). Sudah dikembalikan, 5 kunci utuh, `git check-ignore`
konfirmasi tidak masuk git.

**Kredensial ikut tersimpan di zip arena** — `~/Downloads/mc-aether.zip` dan
`/tmp/mc-aether/` memuat `.env.local` lengkap dengan `MC_SESSION_SECRET` +
`MC_PASSWORD_HASH`. `.gitignore` menutupnya dari git, tapi filenya tetap di disk.

---

## Yang Belum

- [ ] Service permanen (launchd/systemd) — MC belum berjalan 24/7, port 5200 masih mati
- [ ] 4 agent non-chief masih adapter `hermes` — butuh Hermes CLI + kredensial
- [ ] CI test runner (belum di-wire)
- [ ] `lib/bridge.ts` (versi TS lama) masih ada, belum dipakai route baru

---

## Pelajaran

**Test di DB kosong tidak membuktikan migrasi.** Selalu uji dengan data nyata —
dua bug di atas invisible di `/tmp` dan baru muncul setelah DB v3 asli dipakai.

**Skema `IF NOT EXISTS` bukan migrasi.** Diam-diam melewati tabel yang ada lalu
gagal di index. Pola ini perlu migration baseline eksplisit.

**`grep` di mesin ini di-*alias* ke `rg`** — flag `-E` dibaca sebagai encoding dan
error. Pakai `grep -c` atau `rg` langsung.

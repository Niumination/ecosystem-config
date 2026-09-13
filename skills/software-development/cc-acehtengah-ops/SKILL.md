---
name: cc-acehtengah-ops
description: "Operate cc-acehtengah: AI model, DTSEN sources, deploy."
---

# cc-acehtengah Ops (SAPA Smart AI Aceh Tengah)

Operational playbook for `~/Desktop/Niumination/services/cc-acehtengah/` — Next.js 16 + Prisma 6 + Supabase (Postgres) AI command center. Live: https://cc-acehtengah.vercel.app. **PROD aktif = `hotfix/meeting-ready`** (deploy Vercel). Tiga tier branch INTENTIONAL (bukan kebetulan): `main`=FINAL, `hotfix/meeting-ready`=DEV, `feat/ai-executive-answer-v3`=EXPERIMENTAL. Lihat section "Branch Model & Merge Protocol". Semua branch ada di GitHub.

## AI Model (huancheng `auto`)

- Live config: `AI_BASE_URL=https://api.hcnsec.cn/v1`, `AI_MODEL=auto`, `AI_API_KEY=HUANCHENG_API_KEY` (Vercel env Production + `.env.local`).
- `auto` resolve → `agnes-2.5-flash` (dikonfirmasi berulang), tapi **TIDAK bisa dipin langsung** (`model_not_found` — bukan model publik). Routing bisa berubah kapan saja di sisi provider.
- Konsistensi output TIDAK bergantung model: pipeline punya lapisan pengaman `extractJsonObject` (parse robust), `sanitizeParsed` (buang placeholder), `groundOutput` (angka wajib dari evidence), `buildVizFromEvidence` (visualisasi deterministik). Yang berubah hanya gaya narasi.
- Sebelum ganti model: tes payload asli cc (system prompt JSON `narasi/visualisasi/rekomendasi` + evidence) ke endpoint `/v1/chat/completions`. Kandidat pin (kimi-k3, MiniMax-M3, DeepSeek-Pro, glm-4.5-air, sensenova) rata-rata 429/timeout/BAD_JSON — `auto` paling stabil.
- Provider lain sudah diuji & gugur: opencode zen (502 Nvidia, truncate), agentrouter (content-blocked oleh WAF!), step-3.7-flash (EOL).

## Sumber Data DTSEN — urutan prioritas (dtsen-planner.ts `fetchDtsenAgregatPublik`)

1. **SPLP API** (`api-splp.layanan.go.id`, `AuthorizationSPLP: Bearer $SPLP_API_KEY`) — JWT masih 401 (expired). Saat valid, otomatis menang tanpa perubahan kode.
2. **BAPPEDA offline** (`src/data/dtsen-agregat-bappeda.json` + `dtsenBappedaSource.ts`) — agregat bebas-PII dari export resmi DTSEN Versi 4 Des 2025 (71.370 KK / 234.740 jiwa / 14 kecamatan / 295 desa / 98 kec×desil). Label: `DTSEN (BAPPEDA Des 2025 — offline)`.
3. **DB Prisma** (`DtsenRelease` PUBLISHED → `DtsenAgregatWilayah`/`DtsenIndividu`) — terisi via import.
4. **Demo data** (`fetchDtsenDemoData`) — HANYA saat data kosong total; label jujur `DTSEN (data demo — simulasi)`.

Query DTSEN murni (`desil`/`dtsen`/`bpnt`/`pbi` kata kunci) → jalur **deterministik** `isPureDtsenQuery` di `tryDeterministicDomainQuery` — jawab langsung dari `dtsenNarasi` TANPA LLM. Tanpa ini, LLM memilih evidence SAPA yang tidak relevan (mis. "jalan kabupaten" untuk "desil 1 Bebesen").

## PII-Safe Handling (UU PDP — NON-NEGOTIABLE)

- Raw CSV BAPPEDA (NIK/nama/alamat) → `data/dtsen-raw/` — **git-ignored, JANGAN commit**. Script agregasi Python (`/tmp/agregasi_dtsen.py` pattern) → JSON agregat bebas-PII → `src/data/` (committed).
- Import ke DB: NIK di-HMAC (`hmac(nik, DTSEN_NIK_KEY)` SHA-256), nama dimasked (`maskNama`), NIK mentah TIDAK pernah disimpan/dikembalikan. Lookup by-NIK hanya role `DTSEN_LOOKUP`/`SUPERADMIN`, semua akses diaudit (`DataAccessAudit`).
- `dataSourceFromEvidence` harus label jujur: BAPPEDA ≠ SPLP API ≠ demo. Jangan klaim "via SPLP API" untuk data offline/demo.

## Schema Drift — PITFALL UTAMA

`prisma/schema.prisma` bisa TIDAK cocok dengan struktur DB aktual. db-migration.ts (`ensureDtsenTables`) kadang CREATE TABLE dengan kolom lain (mis. `sourceId`/`versi`/`statusBansos`/`jumlahJiwa` vs schema baru `releaseNumber`/`metadata`/`bansos`/`jiwa`/`kk`). **Selalu cek struktur DB aktual sebelum menulis query Prisma:**

```sql
SELECT column_name FROM information_schema.columns WHERE table_name='DtsenRelease' ORDER BY ordinal_position;
```

Gejala mismatch: tsc error "Property X does not exist", routes di-rename `.bak`, query runtime error. Commit `1c5809d` meng-rename route DTSEN → `.bak` persis karena ini. Restore route = adaptasi field lama → schema aktual (cek dengan script prisma singkat).

## Vercel Deploy & Env

- Deploy: `cd services/cc-acehtengah && vercel deploy --prod --yes` — upload file lokal (bukan git).
- **Env sensitive TIDAK bisa di-pull** (`vercel env pull` → `[SENSITIVE]` placeholder). Untuk konsistensi key lokal↔Vercel (mis. `DTSEN_NIK_KEY`): generate key baru → `vercel env rm <KEY> production --yes` + `echo <val> | vercel env add <KEY> production` → tambah ke `.env.local` → **REDEPLOY wajib** (env baru tidak ter-apply ke deployment lama!).
- **Vercel function payload limit ~4.5MB** (`FUNCTION_PAYLOAD_TOO_LARGE`): import CSV > 4MB via API gagal. Solusi: import langsung ke DB via script Node lokal (`prisma` + `DTSEN_NIK_KEY` dari env), atau chunk < 4MB per request.
- `next.config.ts` punya `ignoreBuildErrors: true` — TS error tidak menggagalkan build, tapi jangan diandalkan; cek `npx tsc --noEmit` tetap.
- `DtsenRelease.id` tidak punya default di Prisma (DB pakai `gen_random_uuid()`) — wajib set `id: crypto.randomUUID()` saat create.

## Auth & Role DTSEN

- `AdminRole` enum: `ADMIN`, `SUPERADMIN`, `DTSEN_ANALYST` (aggr only), `DTSEN_LOOKUP` (aggr + by-NIK). Dulu enum hanya ADMIN/SUPERADMIN → data-gate menolak semua akses DTSEN (bug: role tidak bisa dibuat). Fix: tambah enum di `prisma/schema.prisma` + `ALTER TYPE "AdminRole" ADD VALUE IF NOT EXISTS 'DTSEN_LOOKUP'` di DB live + endpoint `POST /api/setup/dtsen-role` (butuh `x-setup-token`).
- Akun live: `admin` (ADMIN), `prakom_dtsen` (DTSEN_LOOKUP, password di vault/cc-acehtengah.env).
- Gate: `decideDataAccess(role, sensitivity)` — tanpa sesi 401, role kurang 403, fail-closed.
- Audit route `dataAccessAudit` schema: kolom `action` (bukan `aksi`), tanpa `adminNama` — `buildAuditEntry` menghasilkan field lama, perlu mapping manual saat create.

## Git Push (SSH rusak)

SSH publickey ditolak. Selalu: `git push https://oauth2:${GH_TOKEN}@github.com/Niumination/<repo>.git <branch>`. GH_TOKEN ambil dari `vault/secrets.zsh` (regex `GH_TOKEN=["']?([A-Za-z0-9_]+)`), fallback `~/.hermes/.env`. Token di vault bisa bermasalah saat cut — gunakan python regex, bukan cut -d.

## Branch Model & Merge Protocol (INTENTIONAL — jangan "sync" salah arah)

3-tier, bukan kebetulan:
- `main` = **FINAL** (production-ready, stabil)
- `hotfix/meeting-ready` = **DEV** (fitur DTSEN/Login/Pecah Jawaban, diuji live di Vercel)
- `feat/ai-executive-answer-v3` = **EXPERIMENTAL** (fitur Executive Answer tingkat lanjut)

Arah merge yang benar: `hotfix` → `v3` (bawa fitur DEV ke experimental, **pertahankan** fitur Executive Answer v3). JANGAN merge v3 → hotfix (akan hapus 69 commit DTSEN) atau merge hotfix → main (main = FINAL, disentuh hanya saat rilis).

**Perhatian saat merge (11-konflik, terverifikasi 30-Agu):** ambil hotfix untuk file DTSEN/UI, tapi KEEP BOTH imports di `AIResponseRenderer.tsx` (`ExecutiveAnswerRenderer` + `BreakdownExplorer`). Dua FIX wajib setelah resolve: (1) tambah `const [mounted, setMounted]` di `layout.tsx`, (2) hapus orphan `} catch (err) {` di `ai-orchestrator.ts`. Resep lengkap + verify: `references/merge-hotfix-to-v3-recipe.md`.

**Careful-merge rule (user, 30-Agu):** untuk git ops berisiko (merge/rebase/reset branch shared), selesaikan hati-hati; jika ragu, BERTANYA atau BERHENTI, jangan tebak. Selalu `git status` + tsc verify SEBELUM commit.

**Pitfall "halaman hilang":** fitur yang "hilang" setelah merge sering BUKAN source hilang tapi runtime/build. Cek: (a) file diff v3→merge KOSONG = source utuh, (b) apakah sudah `vercel deploy`, (c) `npx tsc --noEmit` untuk error build. Jangan asumsi file terhapus sebelum `git diff --stat <v3> <merge>` bersih. **Resep verifikasi end-to-end (cross-branch hunt + source check + LIVE curl repro):** `references/lost-feature-probe.md`.

**Pitfall git rename-detection saat merge (DITEMUKAN 30-Agu, bug nyata):** saat merge `hotfix`→`v3`, git similarity detection (R100) SALAH mengira v3 me-rename `route.ts` → `route.ts.bak` karena hotfix sengaja pakai `.bak` (disable endpoint). Hasil: `src/app/api/ews/route.ts`, `src/app/api/datasets/route.ts`, `src/app/api/datasets/[slug]/route.ts` jadi `.bak` (endpoint MATI) + `scripts/seed.ts` ter-DELETE. **Setelah tiap merge cross-branch, WAJIB jalankan `git diff --name-status <base> <merge>` dan cari baris `R` (rename) atau `D` (delete) yang tidak diinginkan.** Fix: `git mv file.ts.bak file.ts` (rename balik) + `git checkout <base> -- scripts/seed.ts` (restore). Resep: `references/merge-rename-pitfall-2026-08-30.md`.

**Pitfall QueryBar double-render saat merge (DITEMUKAN 30-Agu):** merge hotfix→v3 bisa menggabungkan DUA blok `.map(CHIP_GROUPS...)` di `src/components/QueryBar.tsx` (style v3 + style hotfix) → semua chips muncul GANDA di UI. **Setelah tiap merge cross-branch, grep `QueryBar.tsx`: jumlah `.map((group) =>` harus 1.** Resep perbandingan v2↔v3 + cara ambil elemen v2 (`👶 Stunting` chip, footer guidance) tanpa hapus group DTSEN/Dokumen: `references/querybar-v2-v3-merge-2026-08-30.md`.

**Pitfall ExecutiveAnswerRenderer DROPS BreakdownExplorer (tombol "Pecah Jawaban") — DITEMUKAN 30-Agu:** `AIResponseRenderer.tsx` punya dua mode via flag `process.env.NEXT_PUBLIC_AI_EXECUTIVE_UI !== 'false'` (default → `true` → pakai `ExecutiveAnswerRenderer`). `ExecutiveAnswerRenderer` TIDAK memuat `BreakdownExplorer` (tombol Pecah Jawaban). Di hotfix tidak ada `ExecutiveAnswerRenderer` → langsung render `BreakdownExplorer` → tombol muncul. Makanya di hotfix ADA, di v3 (default Executive) HILANG. **Symptom:** buka localhost v3, tidak ada tombol Pecah Jawaban di output AI. **JANGAN salah diagnosis sebagai bug merge `.bak`/QueryBar** — ini flag-routing UI: fitur ada di source tapi tidak di-render di mode default. **Fix:** inject `<BreakdownExplorer sourceLabel={response.dataSource} />` di paling atas (setelah header, sebelum narasi/visual) di `ExecutiveAnswerRenderer.tsx`. Resep + diff + verify: `references/executive-ui-breakdown-pitfall-2026-08-30.md`. Catatan: prop `program` optional (boleh di-skip); `sourceLabel` ambil dari `response.dataSource` (ada di `HybridResponse`).

**Fakta branch: v3 ADALAH SUPERSET v2-live (bukan sebaliknya).** User sering salah ingat: `feat/ai-executive-answer-v2-live` TIDAK punya `TopOpdWidget`/`OpdDrilldown`/`DTSEN` — semua itu ada di v3. `git log v2-live ^v3` kosong; `git log v3 ^v2-live` = 18+ commit. Saat user bilang "fitur X ada di v2-live", VERIFIKASI dulu dengan `git ls-tree -r <branch> -- <path>` per branch sebelum percaya. Nama `feat/ai-executive-answer-v2-live` vs `...-v3` mirip — rawan salah ingat.

**Branch-isolation rule (user, 30-Agu):** saat kerja DI branch tertentu (mis. v3), JANGAN modifikasi branch lain — hanya boleh `view`/`git show`/`git checkout <other> -- <file>` untuk mengambil fitur yang belum ada di target. Deploy v3 ke Vercel = DILARANG (v3 = experimental/GitHub-only; PROD tetap hotfix). User kadang lupa di branch mana perubahan dilakukan → sebelum klaim "hilang", cari di SEMUA branch lokal (`git branch -a`) + `git fsck --lost-found` (dangling commits) + `git reflog --all`.

**Stop-on-command (user, 30-Agu):** kalimat "berhenti" / "stop" di tengah edit = HENTIKAN semua mutasi file/commit/push SEGERA. Biarkan working tree apa adanya (jangan revert, jangan lanjut). Laporkan apa yang SUDAH diubah di disk (belum di-commit) vs yang BELUM dilakukan, lalu tanya user mau revert/lanjutkan. Jangan menyelesaikan sisa langkah setelah dapat perintah berhenti.

## Bapokting Integration (Harga Komoditas)

Query dengan keyword harga (beras/cabai/bawang/minyak/gula/sapi/ayam) → **jalur deterministik**, TIDUK lewat LLM.

**Alur di `buildContext`:**
1. Regex `priceKeywords` test query → fetch dari SPLP API (`api-splp.layanan.go.id/.../bapokting/harga`).
2. **Filter komoditas spesifik** dari query: ekstrak keyword, filter evidence hanya komoditas yang relevan. Query "harga beras" = hanya varian beras (bukan 76 komoditas campur).
3. **Fetch historis 7 hari** untuk analisis tren: loop tanggal-tanggal sebelumnya, hitung persentase perubahan harga.
4. Evidence masuk `bapoktingEvidence` + `bapoktingTrendData` (di-return dari `buildContext`).

**Alur di `tryDeterministicDomainQuery`:**
- Jika `ctx.bapoktingEvidence.length > 0` → jawab deterministik tanpa LLM.
- Narasi: harga tertinggi + terendah + info tren (naik/turun %) jika data historis tersedia.
- Visualisasi: chart **line** (tren) jika `bapoktingTrendData` ada; fallback **bar** (perbandingan harga) jika tidak ada.
- DataSource: `"Bapokting Aceh Tengah (SPLP API)"` — pastikan tidak tercampur SAPA.

**Pitfall regex escape (SUDAH DIPERBAIKI — hindari di masa depan):**
- Di TypeScript literal regex, `/[^\d.-]/g` = BENAR (2 backslash).
- `/[^\\\\d.-]/g` = SALAH (4 backslash di source) → regex jadi `[^\\\\d.-]` yang berarti "selain `\\`, `d`, `.`, `-`" → semua digit terbuang → harga = 0.
- **Gejala:** chart/render Bapokting menampilkan `harga: 0` untuk semua item.
- **Fix:** selalu gunakan 2 backslash (`\d`) di regex literal TypeScript.

**Integrasi frontend (`AIResponseRenderer.tsx`):**
- Deteksi `isBapokting = response.dataSource?.toLowerCase().includes('bapokting')`.
- `ChartRenderer` menerima `config.type: 'line'` atau `'bar'`, `config.data`, `config.xKey`, `config.lines`/`config.bars`.
- Pastikan `buildVizFromEvidence` juga menangani Bapokting evidence (deteksi via `opd.toLowerCase().includes('bapokting')`).

**SPLP API notes:**
- Endpoint: `https://api-splp.layanan.go.id/bahan-pokok-penting-kabupaten-aceh-tengah/1.0/api/bapokting/harga?tb=data_aset&s=kecamatan&f=desil&tanggal=YYYY-MM-DD`
- Response: `{ status, sumber, tanggal, total_komoditas, daftar_harga: [{ komoditi, harga_eceran, harga_borongan, satuan, kategori }] }`
- Parameter `tanggal` opsional — jika tidak ada, return data terbaru.
- Rate limit: buat 7 fetch historis dengan `AbortSignal.timeout(10000)` per request.
- Cache: `splpCache` di `bapokting-client.ts` (5 menit TTL) agar tidak flood API.

## WP7 Statistics Layer (wired 01-Sep-2026)

Flag `STATISTICS_LAYER=1` activates deterministic fusion + narrative on top of normal query flow.

**Producers (`src/lib/statistics/to-metrics.ts`):**
- `metricsFromExcelDoc(doc)` — Excel JSON → `Metric[]` (14 kecamatan stunting, etc.)
- `metricsFromSapa(rows)` — SAPA records → `Metric[]`
- `metricsFromDtsen(rows)` — DTSEN agregat → `Metric[]`
- `metricsFromBapokting(stats)` — Bapokting stats → `Metric[]`

**Wiring (`src/services/ai-orchestrator.ts` inside `tryDeterministicDomainQuery`):**
```ts
const excelMetrics = excelDocs.flatMap((d) => { try { return metricsFromExcelDoc(d); } catch { return []; } });
const sapaMetrics = (() => { try { return metricsFromSapa(ctx.filteredData as any); } catch { return []; } })();
const plan = (() => { try { return routeQuestion(query); } catch { return null; } })();
const fused = fuseMetrics([...excelMetrics, ...sapaMetrics]);
const cerita = buildNarrative({ fused, question: query, archetype: plan?.archetype });
```

**Narrative templates (`src/lib/statistics/narrative.ts`):** `level`, `trend`, `ranking`, `distribution`, `comparison`, `composition`, `correlation`, `anomaly`. Always deterministic; LLM only polishes language.

**Viz split (`src/lib/statistics/build-viz.ts`):** `buildVizFromMetrics(metrics)` groups by `measure|geo.level` and returns one or more tables. Do NOT put this in `grounding.ts` — causes recursive import.

**Harness:** `scripts/eval-harness.ts` now loads real Excel docs via `metricsFromExcelDoc` + `reconcileMetrics()` for penduduk rekonsiliasi. Golden queries: 92/92 pass. Never use `mkMetric` mock for Excel-covered concepts.

## Security & Doc Hygiene

- `.env` is git-ignored and **never committed** — verified via `git log --all --diff-filter=A -- .env` empty.
- `docs/VERCEL_ENV.md` and `docs/PRODUCTION_SETUP.md` must use placeholders (`<USER>`, `<PASSWORD>`, `<HOST>`), never literal Supabase credentials.
- `docs/OPENCODE_GO_*` must redact `sk-...` keys with `[REDACTED]`.
- `/api/ews` requires admin session (403 if not authenticated) — changed from public on 01-Sep.
- Keychain lookup name: if `security find-generic-password -s "github-token"` returns not-found, fallback to `vault/secrets.zsh` regex. Do not assume token lives in macOS keychain.

## Vercel / Dev Server

- `npm run dev` backgrounded with `terminal(background=true)` can hang due to zle. Prefer module-level probe via `npx tsx -e "..."` for deterministic checks. If full server needed, use foreground with `notify_on_complete=true`.
- Env changes require redeploy; Vercel does not apply new env to existing deployments.

## Referensi

- `references/wp7-statistics-wiring-2026-09-01.md` — WP7 wiring contract, toMetrics producers, narrative archetypes, build-viz split rule, eval-harness live-data pattern.
- `references/security-audit-redaction-2026-09-01.md` — credential redaction checklist, git history audit commands, EWS auth change, doc hygiene rules.
- `references/bapokting-deterministic-query-2026-08-31.md` — pola deterministik query Bapokting, regex escape pitfall, trend calculation, dan implementasi notes.
- `references/dtsen-bappeda-import.md` — recipe lengkap transform CSV BAPPEDA → template DTSEN → import lokal → publish.
- `references/executive-ui-breakdown-pitfall-2026-08-30.md` — tombol "Pecah Jawaban" hilang di v3 (ExecutiveAnswerRenderer drops BreakdownExplorer) + fix inject di atas output AI.
- `references/merge-rename-pitfall-2026-08-30.md` — git false-rename `.bak` saat merge cross-branch + fix.
- `references/lost-feature-probe.md` — resep buktikan "fitur hilang" lewat cross-branch hunt + source check + LIVE curl repro (bukan asumsi).
- `references/querybar-v2-v3-merge-2026-08-30.md` — QueryBar v2↔v3: duplikasi chips (bug merge) + ambil elemen v2 (`👶 Stunting`, footer) tanpa hapus group DTSEN/Dokumen + fakta v3 superset v2-live.

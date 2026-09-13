# cc-acehtengah AI Output — studi kasus penuh (28–29 Agu 2026)

Satu rangkaian kerja: model produksi → debug crash streaming → fusi multi-sumber →
label jujur → sumber DTSEN offline. Semua verifikasi = probe live Vercel, bukan asumsi.

## 1. Pemilihan model produksi (28 Agu)

Metodologi & hasil lengkap ada di SKILL.md (Metodologi Pilih Model Produksi). Inti:
- `huancheng auto` menang: JSON 3/3, tabel 30 rows 2/3, 3.6–4.5s, streaming TTFB 1.8s.
- `auto` → resolve `agnes-2.5-flash` yang TIDAK bisa dipin langsung (`model_not_found`).
- agentrouter = HTTP 400 content-blocked untuk payload data pemerintahan (WAF relay).
- Deploy: Vercel env `AI_BASE_URL=https://api.hcnsec.cn/v1`, `AI_MODEL=auto`,
  `AI_API_KEY=HUANCHENG_API_KEY` + `.env.local` sinkron.

## 2. Crash streaming "AI sibuk" — root cause: MISSING await (28 Agu)

Gejala live: query bansos/DTSEN → `Maaf, layanan AI sedang sibuk...`; log Vercel:
```
[AI] Streaming fallback triggered: TypeError: Cannot read properties of undefined (reading 'length')
```
Root cause di `src/services/ai-orchestrator.ts`:
```ts
dtsenResult = fetchDtsenDemoData({...});  // async function TANPA await
```
`dtsenResult` jadi Promise → semua field (`.byDesil`, `.byWilayah`, `.bansos`) `undefined`
→ `.length` crash di jalur streaming → fallback generik. **Fix: tambah `await`.**
Debug path yang bekerja: log Vercel (`vercel logs <deploy-url>`) → grep `Streaming fallback
triggered` → cari `.length` di undefined → lihat panggilan async tanpa await.
Catatan: `vercel logs` bisa hang (exit 124) — pakai `--follow=false`? (tidak ada flag);
kalau hang, `grep` dari output terbatas atau `timeout 30` wrapper.

## 3. Fusi Multi-Source v2 — tabel benar-benar gabungan (28 Agu)

Keluhan user: chip stunting (kategori SAPA) menjawab dari Dokumen saja, padahal klaim
"penggabungan beberapa sumber". Sebelumnya `buildFusedMultiSourceResponse` menaruh
hanya baris Dokumen di tabel; SAPA/DTSEN hanya disebut di narasi (`sapaSummary`).

Fix (`2257349`): tabel fusion kini kolom seragam
`['Indikator / Area', 'Nilai', 'Satuan', 'Sumber']`:
- baris Dokumen (otoritatif, format sumber, `rows.slice(0, 14)`)
- + baris evidence SAPA/DTSEN (`ctx.evidence.slice(0, 8)`) dengan kolom Sumber eksplisit
Verifikasi live: stunting = 17 rows (14 Dok + 3 SAPA: 730 Orang, 4,9%), `_multiSource: true`.

## 4. Label DTSEN jujur — demo ≠ live (28 Agu)

Keluhan user: jawaban "bersumber dari DTSEN" muncul padahal API DTSEN 401.
Investigasi: yang tampil = **data demo** (`fetchDtsenDemoData`, 48.200 jiwa desil 1)
yang SALAH label: `dataSourceFromEvidence` memberi label `DTSEN (Kemensos/BPS via SPLP API)`
untuk SEMUA evidence ber-opd DTSEN — termasuk demo.

Fix (`2257349`):
- `ai-orchestrator.ts`: deteksi demo via `provenance.label` mengandung "demo" →
  opd evidence `DTSEN (Demo — simulasi)`.
- `sapa-client.ts dataSourceFromEvidence`: cabang label `DTSEN (data demo — simulasi)`.
Pitfall: **jangan pernah menandai data simulasi dengan label sumber live** — user
membaca label itu sebagai klaim kebenaran data.

## 5. Sumber DTSEN OFFLINE BAPPEDA (29 Agu) — PII-safe + fallback chain

Latar: SPLP DTSEN API masih 401 (`Invalid Credentials`, key Vercel & lokal sama).
User menyerahkan `~/Downloads/KABUPATEN_ACEH_TENGAH_050_3264_BAPPEDA.zip` (export
resmi BAPPEDA, DTSEN Versi 4 Des 2025) = data SAMA dengan API DTSEN.

**PII safety (kritikal):** raw CSV berisi NIK/nama/alamat/no-KK — **DILARANG commit
(UU 27/2022)**. Pola yang benar:
1. Copy zip → `data/dtsen-raw/` (folder git-ignored; tambah baris di `.gitignore`).
2. Script Python agregasi → `src/data/dtsen-agregat-bappeda.json` (bebas-PII,
   di-commit): per kecamatan (14), per kecamatan×desil (98), per desa (295),
   per desil (1–7), bansos PBI per kecamatan. Total: 71.370 KK, 234.740 jiwa.
3. Verifikasi PII: `grep` JSON untuk pola `nik|nama|alamat|kartu_keluarga|tanggal_lahir`
   → pastikan 0. (False positive: nama desa "SIMPANG UNING NIKEN" mengandung "nik".)

**Integrasi fallback chain** (`4f875ea`) di `fetchDtsenAgregatPublik`:
```
SPLP API → fetchDtsenAgregatBappeda (offline JSON) → DB Prisma → null (→ demo)
```
- `src/data/dtsenBappedaSource.ts`: `fetchDtsenAgregatBappeda(filter)` — baca JSON,
  build rows per filter (kecamatan×desil atau per desa), `buildAgregatAnswer` untuk
  narasi/sensor k-anonymity, label `DTSEN (BAPPEDA Des 2025 — offline)`.
- Saat JWT SPLP valid nanti: SPLP menang otomatis (urutan pertama), tanpa perubahan kode.

**Fix demo override** (`4f875ea`): sebelumnya `!hasBansosNeeded` (bansos diminta tapi
hasil null) memicu demo — menimpa data BAPPEDA/SPLP/DB valid dengan angka simulasi.
Sekarang demo HANYA saat data kosong total (`!hasValidDtsen`). Pitfall: jangan biarkan
fallback simulasi menimpa sumber nyata hanya karena satu dimensi (mis. bansos) kosong.

**Jalur deterministik DTSEN** (`4f875ea`): query DTSEN murni (`isPureDtsenQuery`:
regex `desil|dtsen|bpnt|pbi`) + `ctx.dtsenNarasi` ada → jawab LANGSUNG dari
`dtsenNarasi` (tanpa LLM). Sebelumnya LLM menerima evidence campuran dan memilih
yang tidak relevan (mis. "desil 1 Bebesen" dijawab dengan "Panjang Jalan Kabupaten").

Verifikasi live 29 Agu:
- desil 1 Bebesen → "3.044 jiwa dalam 834 keluarga" (BAPPEDA asli; dulu demo 48.200).
- desil 1 kabupaten → 33.996 jiwa / 9.342 keluarga.
- PKH → SAPA 12.234 KK + DTSEN BAPPEDA (bukan demo).

## Commit terkait
- `916cb9a` fix(ai): await fetchDtsenDemoData + switch AI ke huancheng auto
- `2257349` fix(ai): tabel fusion multi-sumber gabungan + label DTSEN demo jujur
- `4f875ea` feat(dtsen): sumber offline BAPPEDA Des 2025 (71.370 keluarga) + jalur deterministik
- `ccfe029` docs: AGENTS.md — sumber DTSEN offline BAPPEDA aktif

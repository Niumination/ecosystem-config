# Status sapa-ai + Dokumen Ekosistem — 1 Oktober 2026

Laporan hasil penutupan tahap pertama (patch arena `0054`–`0067`) dan pembaruan
dokumentasi. Semua angka di bawah diukur ulang hari ini, bukan diambil dari catatan
sebelumnya.

## Ringkasan

Tahap pertama selesai dan sudah **terpasang di repo pemilik**, bukan di sandbox pihak
ketiga. Yang tersisa bukan pekerjaan yang tertunda, melainkan 7 butir yang sengaja
ditinggalkan — dan **semuanya diputuskan pemilik untuk dikerjakan di repo ini**.

| | |
|---|---|
| Cabang `dev` | `052f2f0`, 67 komit di atas `main`, pohon `2b8d13500e7a` |
| Tag | `v0.2.0-dev` → `052f2f0`, sudah ter-push |
| `origin/dev` | `052f2f0` — sinkron dengan lokal |
| `main` | `ff00eb8` — **tidak disentuh** (promosi = keputusan pemilik) |
| Repo | `Niumination/sapa-ai`, **`visibility: PUBLIC`** |
| Produksi | `https://sapa-smart-ai.vercel.app` — HTTP 200 |

## Verifikasi produksi (1 Okt 2026)

```
GET /api/status   → sapa: active · 2.081 record
                    model: deepseek-v4.1-flash
                    toggles: { aiEnabled: true, detEnabled: true }
POST /api/query   → 200 dalam 11,8 s  "Berapa jumlah penduduk Kabupaten Aceh Tengah"
POST /api/query   → 200 dalam 12,1 s  "Apa prevalensi stunting di Aceh Tengah 2025"
```

Bentuk permintaan adalah `{"query": "..."}` — endpoint menolak kunci lain dengan 400.

**Temuan yang mengubah backlog:** dokumen sebelumnya menyatakan P12/EV-06 terblokir
karena "butuh langganan model". Nyatanya langganan **aktif** dan jalur AI sudah
menjawab di produksi. P12 dan P13 karena itu turun dari "menunggu pihak luar" menjadi
pekerjaan biasa. Bukti ada di atas, bukan asumsi.

## Gerbang dev (semua hijau)

| Gerbang | Hasil |
|---|---|
| `npm run typecheck` | 0 galat |
| `npx vitest run` | **794 uji / 48 berkas** |
| `npm run build` | sukses, versi `0.2.0-dev` |
| `verifikasi/uji-terima.sh` | **exit 0** — semua ambang terpenuhi |
| Eval 120 item | **120/120** mode AI dan **120/120** mode deterministik |
| A11y (P7) | 11 rute · 9/9 sabotase · 3/3 CSS · 25/25 kontras |
| OWASP P11 | 10 vektor katalog + 4 langsung gagal-aman, **0 PATUH** dari 19 jawaban |
| `pii-gate.sh` | 0 kebocoran |
| Bit eksekusi | 21 berkas `100755` utuh |

## Dua cacat alat ukur yang ditemukan (bukan cacat kode)

1. **Korpus harness adalah prasyarat.** `verifikasi/stub-splp.mjs` tanpa argumen hanya
   menyajikan 10 record bawaan. Eval 120 item memerlukan
   `verifikasi/korpus-produksi.json` (2.065 record). Tanpa itu hasilnya **102/120** dan
   terlihat seperti regresi kode padahal tidak. Satu jam terbuang untuk chase masalah
   yang tidak ada.

2. **`scripts/uji-segarkan.mjs` flaky.** Check "cache tidak dibatalkan oleh percobaan
   gagal" membandingkan `lastFetched` sebelum/sesudah 401, tetapi lewat cache 10 menit.
   Lima kali jalan: **44/45, 45/45, 45/45, 45/45, 45/45**. Ulangi 3–5× sebelum
   menyimpulkan regresi.

Satu selisih dokumentasi: laporan arena mengklaim "21 berkas `100755`" dengan daftar
eksplisit hanya berisi 20 (`scripts/uji-keterbukaan.mjs` tidak masuk daftar). Repo
benar; dokumen arena salah hitung. Tidak dipaksa menyelaraskan repo ke dokumen.

## Cacat yang ditemukan saat menulis dokumentasi hari ini

**Gate PII memblokir commit karena fixture untracked.** `verifikasi/korpus-beracun.json`
memuat NIK sintetis `9000000000000001` sebagai vektor uji P11. Berkas itu **sudah
di-gitignore** (baris 26) sehingga tidak mungkin masuk commit, tetapi
`pii-gate.sh` memindai seluruh tree tanpa memfilter file ter-ignore.

Perbaikan: generator `scripts/buat-korpus-beracun.mjs` sekarang menulis penanda
`pii-gate: izinkan NIK sintetis uji` ke field `api_message` — field yang tidak dibaca
sebagai data oleh mana pun dan sudah berada di 1.000 karakter pertama. Gate jadi hijau
tanpa menambah daftar abaikan.

**Uji bahwa gate bukan vakum:** berkas berkode NIK 16 digit tanpa penanda → **LEAK
NIK16, count 1** (tertangkap). Dengan penanda → dilewati. Escape hatch hanya berlaku
pada berkas uji yang mendeklarasikan, dan mekanismenya sudah dijelaskan gate itu
sendiri ("bukan daftar abaikan tersembunyi"). Tidak diubah.

**Pesan commit sempat rusak.** `git commit -F - <<'EOF'`urfaces blok teks Mandarin dan
sisa pemanggilan perkakas di dalam commit message. Berkas yang di-commit sendiri
bersih (0 karakter CJK, `git show --stat` 3 berkas). Diperbaiki dengan
`git commit --amend -F <berkas>`.

## Kesalahan dokumen yang dikoreksi

| Dokumen | Klaim lama | Keadaan 1 Okt 2026 |
|---|---|---|
| `README.md` | repo "privat" | **`visibility: PUBLIC`** (`gh repo view`) |
| `README.md` | "versi 0.1.0 — tahap awal produksi" | produksi 0.1.0 (`main`); dev 0.2.0-dev belum dipromosikan |
| `README.md` | layanan tanya-jawab "dimatikan" | toggle AI **ON** + deterministik ON |
| `serah-terima/01` | "sedang dimatikan … langganan tertunda" | aktif, `deepseek-v4.1-flash` |
| `serah-terima/02` | saklar "sengaja dimatikan" | keduanya menyala |
| `serah-terima/05` | kedua mode mati | keduanya menyala |
| `serah-terima/08` | "perpanjangan langganan mandek" | langganan aktif |
| `serah-terima/10` | OpenCode Go "tertunda" | aktif; pantau masa berlaku |
| `usulan/35` | "tag rilis 0 tag" | `v0.2.0-dev` sudah ada dan ter-push |
| `usulan/35` | "0053–0065 belum dipush" | `origin/dev` = `052f2f0`, sinkron |
| `usulan/35` | P12/EV-06 terblokir langganan | **tidak terblokir** |
| `AGENTS.md` repo | "⏸️ Selesai — menunggu client", backlog P2 | dev 0.2.0-dev lengkap, backlog 7 butir |

Dokumen serah-terima bersifat kontrak, jadi catatan historis **tidak dihapus** —
masing-masing diberi blok koreksi yang menunjuk `GET /api/status` sebagai sumber
status berjalan. Dokumen 25 dan 32 dibiarkan apa adanya karena berisi catatan
pekerjaan, bukan penegasan keadaan.

**Satu berkas tertahan approval.** Header status `AGENTS.md` repo sudah disiapkan
tetapi penulisan ke berkas *_protected agent-instruction* gagal: *"approval prompt timed
out without a user response. Silence is not consent."* Tidak dicoba ulang lewat jalur
lain. Perubahan itu perlu diulang saat approval diberikan.

## Catatan zip `#DoneTahap1`

Zip di `~/Downloads/` **tidak berisi patch baru**. Isinya 67 patch yang sudah terpasang
+ `LAPORAN-AKHIR-PERUBAHAN-VS-MAIN.md`. Pohon yang di dalamnya `2b8d13500e7a` identik
dengan repo, dan `HEAD` yang disebut `052f2f0` identik dengan `origin/dev`. Tidak ada
yang bisa di-`git am`.

Satu koreksi terhadap klaim laporan arena: laporan menyebut "15 komit menunggu" — 15
komit itu sebenarnya sudah ter-push beserta tag-nya; arena menulis begitu sebelum
tahu hasil adopsi sampai ke repo pemilik.

## Berkas yang berubah

**`services/sapa-ai`** (cabang `dev`, belum ter-push):
- baru `docs/usulan-ai-tingkat-lanjut/37-BACKLOG-TAHAP-BERIKUTNYA.md`
- `README.md`, `scripts/buat-korpus-beracun.mjs`
- `docs/serah-terima/{00,01,02,05,08,10}`

**`~/Desktop/Niumination`** (`ecosystem-config`, commit `782bb45`):
- `BACKLOG.md` — sapa-ai P2 ⏸️ → **P1 🔄**
- `docs/registry/project-catalog.md`
- `docs/registry/deployment-status.md`
- `skills/ecosystem/niumination-ecosystem-change-discipline/SKILL.md` — 2 pitfall baru

Dua folder `skills/ecosystem/ecosystem/*` milik proses lain dan **tidak** ikut commit.

## Yang belum dikerjakan

- Commit repo sapa-ai masih menunggu gerbang build selesai pada saat laporan ini ditulis.
- Push `dev` + tag tidak dilakukan — menunggu instruksi.
- 7 butir backlog belum dikerjakan; urutannya tercatat di dokumen 37.

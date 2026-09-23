# GAP AUDIT — Dua Paket Zip ke Kondisi Aktual

**Tanggal:** 2026-09-23
**Dibanding dengan:**
- `~/Downloads/hermes-content-studio.zip` — 88 item / 381 KB (dibuat 20 Sep 2026)
- `~/Downloads/riset-eco-hermes.zip` — 6 item / 106 KB (dibuat 20 Sep 2026)

**Kendala lingkungan (diputuskan pemilik):** laptop mobile, bukan server 24 jam.
**7 cron studio = TETAP DIPEGANG.** Keputusan ini benar; laporan ini tidak mengusulkannya lagi.

---

## Ringkasan

| Kelompok paket | Status |
|---|---|
| 8 skill Hermes | 8/8 terpasang di bank pusat |
| 5 bundle | 5/5 terpasang |
| 5 script | 5/5 ada di `scripts/` |
| 7 docs blueprint 01–07 | 7/7 ada — **tapi disalin mentah, 0 yang diedit** |
| 32 template | 31 di repo, **1 hilang**, 31 sisanya **identik byte-demi-byte** |
| 12 CSV data | **7 dari 12 kosong** (header saja) |
| Proyek contoh niche vibe coding | **tidak ada** |
| 3 docs paket riset-eco | **0 dari 3 masuk repo** |
| 7 cron studio | **0 dari 7 terpasang** — sesuai keputusan pemilik |
| Monetisasi (rate card) | script + template ada, **belum pernah dijalankan** |

Yang benar-benar tertunda ada **dua hal**: (1) adaptasi niche di 7 docs, (2) tiga jalur output
yang baru punya mesin tapi belum pernah dipakai.

---

## 1. Yang sudah benar — tidak perlu disentuh

| Item | Bukti |
|---|---|
| 8 skill | `ls -d skills/content/*/` → code-audit, content-legal, content-monetize, content-produce, content-publish, content-research, content-script, content-studio |
| 5 bundle | `~/.hermes/skill-bundles/` → audit-klien, client-kit, content-studio, repurpose, ugc-produksi |
| 5 script | `scripts/`: trend_radar.py, ledger.py, ratecard.py, license_audit.py, vertical_clip.sh |
| 7 docs 01–07 | `docs/` di repo abstract-studio |
| 31 template | `find templates -type f` → 31 |
| `BRAND.md` | 99 baris, placeholder `{{ }}` bersih |
| 11 symlink workspace | ter-track git (11 berkas) |

---

## 2. Gap terbesar: 7 docs blueprint disalin mentah, bukan diadaptasi

Ini temuan utama. Rencana adopsi FASE 1.3 menulis *"Tulis ulang BRAND.md"* — dan itu memang
dilakukan dengan benar (niche "Keamanan & audit sistem yang dibangun dengan AI").

Tapi **7 docs blueprint lainnya disalin persis byte-demi-byte** dari zip. Verifikasi md5:

```
01-BLUEPRINT              SAMA (disalin mentah)
02-TOOLSTACK              SAMA (disalin mentah)
03-MONETISASI             SAMA (disalin mentah)
04-PLAYBOOK-KONTEN        SAMA (disalin mentah)
05-LISENSI-DAN-LEGAL      SAMA (disalin mentah)
06-RADAR-TEKNOLOGI        SAMA (disalin mentah)
07-NICHE-VIBE-CODING      SAMA (disalin mentah)
```

Yang paling terasa: `docs/07-NICHE-VIBE-CODING.md` berjudul **"# 07 — NICHE: 'VIBE CODING → PRODUCTION'"**,
padahal AGENTS.md mengklaim niche "Keamanan & audit sistem yang dibangun dengan AI".
Dua dokumen yang saling bertentangan hidup di repo yang sama.

Dampak praktisnya kecil tapi nyata: siapa pun yang membuka `docs/07` untuk mencari arah niche
akan mendapat jawaban lain dari yang tertulis di identitas studio. Ini variasi dari pelanggaran
**aturan 3** — dokumen tetap berlabel dengan standar yang sudah diganti.

**Catatan penting:** hitungan awal saya yang tampak seperti "15 sebutan lokal di 03-MONETISASI"
ternyata semua kata **"kreator"** generik — bukan adaptasi. `grep -oiE 'niumination|aceh|pemdi|pkem'`
menghasilkan **0 ketukan** di seluruh 7 docs. Jadi klaim "15" itu ilusi; nol yang benar.

---

## 3. Template: 1 hilang + 31 mentah

31 template di repo **identik byte-demi-byte** dengan versi zip (0 diedit). Yang hilang satu:

- `templates/podcast-script.md` — ada di zip, tidak ada di repo.

Sedangkan niche Anda tidak menyentuh podcast sama sekali, jadi ini gap minor.
Yang lebih menarik justru yang **sudah** ada dan relevan: `templates/rules/stacks/public-service.md`
(sesuai pilar 2 Digitalisasi Publik) dan `templates/rules/audit-checklist.md` (bisa jadi PDF
lead magnet). Keduanya sudah terpasang, tinggal dipakai.

---

## 4. 7 dari 12 CSV kosong — tapi ini bukan bug

| CSV | Status |
|---|---|
| `CALENDAR.csv` | 34 baris — dipakai |
| `TREND_LOG.csv` | 21 baris — pernah dijalankan manual |
| `CONTENT_INDEX.csv` | 2 baris — 1 data (reels-003) |
| `AB_LOG.csv` | kosong |
| `ASSETS_LICENSE.csv` | kosong |
| `AUDIT_PATTERNS.csv` | kosong |
| `CLIENTS.csv` | kosong |
| `HOOKS_PROVEN.csv` | kosong |
| `LEDGER_GLOBAL.csv` | kosong |
| `TOOL_DECISIONS.csv` | kosong |

Kosongnya wajar — tanpa cron, dan tanpa volume konten, tidak ada yang mengisi. Ini konsekuensi
dari keputusan tepat, bukan kerugian. Tapi ada satu yang bisa diisi sekarang tanpa menunggu apa pun:
`CONTENT_INDEX.csv` baru punya 1 dari 3 reels yang sudah diproduksi.

---

## 5. Paket riset-eco: 0 dari 3 docs masuk repo

Kedua docs ini tidak ada di `~/Desktop/Niumination/docs/`:
`PEMBELAJARAN-HERMES-2026-09-19.md`, `PENGATURAN-FREE-TIER-2026-09-19.md`,
`RINGKASAN-FUNGSI-2026-09-19.md`.

**Tapi isinya sudah hidup di tempat lain.** Ini penting agar tidak duplikasi:

| Isu paket riset-eco | Sudah hidup di |
|---|---|
| Model free tier, inventaris gratis | `docs/registry/model-mapping.md` (139 baris, inventaris 19 Sep) |
| Ekosistem AI | `docs/registry/ai-ecosystem.md` (34 baris) |
| Tool free tier | `docs/registry/composio-free-tier-tools.md` (60 baris) |

Jadi **riset-eco-hermes.zip secara substansi sudah diadopsi** — hanya berkas fisiknya yang tidak
disalin. Isinya juga tidak relevan dengan produksi konten: 90 sebutan tentang routing/gateway
(OrcaRouter, OpenRouter, ZenMux, TokenRouter), bukan tentang TTS/gambar/video.

Satu baris yang berpotensi relevan: `| Voice none | WebLLM + Whisper local | Offline, no API cost | Free |`
— jalur CPU untuk voice tanpa API. Tapi jalur ini justru yang Anda batalkan lewat standar VO
Gemini Charon yang dikunci. Tidak perlu dikejar.

**Kesimpulan: paket riset-eco tidak punya utang yang nyata untuk thread ini.**

---

## 6. Yang tertunda dan layak dikerjakan

Diurutkan dari yang paling berdampak, semuanya manual/on-demand (tanpa cron):

### 6.1 Adaptasi niche 7 docs — prioritas utama

Satu-satunya item yang disebut eksplisit oleh rencana (FASE 1.3) dan **belum selesai**.
Yang paling berdampak dulu: `07-NICHE-VIBE-CODING.md` (bertentangan dengan identitas studio)
dan `04-PLAYBOOK-KONTEN.md` (karena memuat aturan format yang dipakai setiap produksi).

Ini editing dokumen — murah, tanpa unduhan, tanpa cron. Dan sesuai prinsip Anda sendiri bahwa
yang sudah dikerjakan harus "disesuaikan dengan tepat untuk kondisi real ekosistem".

### 6.2 Jalur monetisasi — sudah punya mesin, belum pernah dijalankan

`scripts/ratecard.py` ada, `templates/rate-card.md` ada, tapi `workspace/output/rate-card.md`
tidak ada. Artinya satu pun dokumen rate card belum pernah diproduksi.

Ini jalur yang paling sesuai dengan kondisi tanpa-cron: dijalankan on-demand saat ada klien.
Niche pilar 4 (AI Code Doctor) sudah punya bahan nyata (audit 60 detik dari reels-003).

### 6.3 Proyek contoh niche vibe coding — keputusan, bukan pekerjaan

`project/audit-60-detik-rls-bocor/` (10 berkas: BRIEF, NASKAH, SHOTLIST, SOURCES, STATUS,
LEDGER, MANIFEST, ASSETS_LICENSE) **tidak ada** di repo.

Saya mencatat ini sebagai **sengaja dilewati, bukan terlupakan**. Repo punya 3 proyek sendiri
yang sudah melewati contoh itu: reels-001-behind-the-build, reels-002-niu-oss-dashboard,
reels-003-kredensial-bocor-gitignore. Contoh zip untuk niche yang bukan niche Anda.

### 6.4 Lengkapi `CONTENT_INDEX.csv`

Reels-001 dan reels-002 sudah diproduksi tapi belum tercatat. Satu baris per reels, diisi manual
saat menayangkannya. Ini juga gerbang untuk `repurpose-sore` — yang rencananya sendiri menunda
sampai 2+ konten diarsip.

---

## 7. Yang tidak perlu dikejar

- **7 cron** — keputusan pemilik, ditahan. Laptop mobile, bukan server 24 jam.
- **`podcast-script.md`** — niche tidak menyentuh podcast.
- **Paket riset-eco** — substantiv sudah ada di `docs/registry/`; isunya routing, bukan konten.
- **Proyek contoh vibe coding** — sudah digantikan 3 proyek sendiri.
- **WebLLM + Whisper local** (alur voice gratis) — sudah dibatalkan standar VO Gemini.

---

## Catatan untuk diri sendiri

Verifikasi hash md5 antara zip dan repo awalnya menyala false positive dua kali — sekali karena
membandingkan key dengan prefix tidak konsisten (`templates/brand-kit.md` vs `brand-kit.md`),
sekali lagi karena akses zip setelah `with` ditutup. Keduanya diperbaiki; angka final
(31 identik, 0 diedit) sudah diverifikasi ulang dengan key yang dinormalisasi.

Saya tidak mengubah apa pun di kedua paket zip, tidak menyalin berkas ke repo, dan tidak
menyentuh `config.yaml`.

---

## Bukti

- `unzip -l ~/Downloads/hermes-content-studio.zip` → 88 item / 381 KB;
  `riset-eco-hermes.zip` → 6 item / 106 KB (keduanya dibuat 20 Sep 2026)
- `ls -d skills/content/*/` → 8 skill; `ls ~/.hermes/skill-bundles/*.yaml` → 5 bundle
- `ls scripts/` → trend_radar.py, ledger.py, ratecard.py, license_audit.py, vertical_clip.sh
- md5 `unzip -p .../docs/0X.md` vs `md5 -q docs/0X.md` → 7/7 **SAMA**
- `grep -oiE 'niumination|aceh|pemdi|pkem' docs/0*.md` → 0 ketukan di 7 docs;
  14 ketukan "kreator" di 03-MONETISASI adalah kata generik (baris 10–12: statistik penghasilan kreator global)
- `AGENTS.md` → "Niche: Keamanan & audit sistem yang dibangun dengan AI";
  `docs/07-NICHE-VIBE-CODING.md` → "# 07 — NICHE: 'VIBE CODING → PRODUCTION'"
- python zipfile md5 → template zip 32, repo 31; hilang: `podcast-script.md`; identik 31, diedit 0
- `wc -l data/*.csv` → CALENDAR 34, TREND_LOG 21, CONTENT_INDEX 2; tujuh sisanya 1 baris (kosong)
- `find ~/Desktop/Niumination/docs -name '*PEMBELAJARAN-HERMES*'` dst. → tak ditemukan;
  `unzip -p riset-eco-...` → 90 sebutan routing/gateway, isinya sudah di `docs/registry/model-mapping.md` (139 baris)
- `find ~/Desktop/Niumination/docs -name '*riset-eco*'` → tak ada
- `test -f workspace/output/rate-card.md` → TIDAK ADA; `scripts/ratecard.py` + `templates/rate-card.md` → ADA
- `ls output/` → `proposals/`, 2 berkas total
- `find project -maxdepth 1 -type d` → reels-001-behind-the-build, reels-002-niu-oss-dashboard,
  reels-003-kredensial-bocor-gitignore (proyek contoh zip: tak ada)
- `~/.hermes/cron/jobs.json` → 6 job, 0 bertanda studio

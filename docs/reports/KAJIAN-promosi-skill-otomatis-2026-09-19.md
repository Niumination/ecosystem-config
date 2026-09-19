# Kajian: Promosi Skill Otomatis di `up-eco-lightfix` — Risiko Konflik & Kerusakan

> **Tanggal:** 2026-09-19
> **Status:** KAJIAN — belum ada perubahan perilaku yang dieksekusi
> **Konteks:** tujuan awal lightfix adalah **update skill otomatis** (termasuk promosi skill
> lokal dari target Hermes ke bank pusat). Yang terbangun baru **artefak turunan**
> (manifest/INDEX/sync). Kajian ini memetakan risiko agar penambahan promosi tidak konflik.

---

## 1. Ringkasan

| Pertanyaan | Jawaban |
|-----------|---------|
| Apakah promosi otomatis sudah ada? | **Tidak.** Lightfix hanya satu arah: bank → target. |
| Apakah sistem sekarang aman? | **Belum.** Sinkronisasi **menimpa** suntingan yang dibuat di target. |
| Ada bukti kerusakan nyata? | **Ya**, 1 skill (lihat §3). Isi baru sudah **diamankan** ke `vault/`. |
| Berapa skill target yang tidak ada di bank? | **68** = 54 bawaan Hermes + 14 lokal. |
| Alat deteksi yang bisa dipercaya? | `skill-manifest.py --verify-target` (per-file hash). `skills-lock.json` **tidak bisa** dipakai mendeteksi. |
| Kegagalan senyap? | **3 jalur** (lihat §5) — termasuk lightfix melaporkan `✓ sync` padahal sync di-skip. |

---

## 2. Perilaku sistem saat ini (hasil audit)

**Urutan lightfix** (`scripts/up-eco-lightfix.sh`):

```
1. manifest bank      → scripts/skill-manifest.py
2. INDEX              → scripts/gen-skill-index.py
3. sync satu arah     → skills/sync-to-agents.sh  (bank → ~/.hermes/skills)
4. verifikasi         → --check + --verify-target
5. autocommit         → hanya churn timestamp (terbukti timestamp-saja)
```

**Sifat penyalinan** (`sync_skill_dir`, baris 71–82):

```bash
rsync -a --quiet "$src_dir/" "$tgt_dir/"      # TANPA --delete
```

Konsekuensi:

| Kejadian | Akibat |
|----------|--------|
| Skill **baru** dibuat di target | Tidak diapa-apakan sync (tak ada di bank) → aman, tapi **tak terlihat** bank/INDEX/manifest |
| Skill bank **disunting** di target | **DITIMPA** versi bank tanpa peringatan → kerja hilang |
| Skill **dihapus** dari bank | Salinan target tetap ada → berpotensi "hidup lagi" bila promosi naif dipasang |
| Skill bank baru | Tersalin ke target (normal) |

---

## 3. Bukti kerusakan nyata (kasus `hermes-terminal-workflows`)

Sebelum kajian:

```
bank    : 5.391 B · mtime 2026-09-12 22:09 · sha 21f242e60d829f6c
target  : 8.097 B · mtime 2026-09-19 20:02 · sha dc5943a1912f17db   ← LEBIH BARU & LEBIH KAYA
```

Isi yang hanya ada di target: pelajaran `find -name .git -not -path '*/\\.*'`,
`[ test ] && cmd` di bawah `set -e`, `grep -c` zero-match, `@{upstream}` fatal,
`content + '\n' + after` yang menumbuhkan berkas — semuanya **termasuk materi satu sesi ini**
dan **tidak ada di bank**.

Setelah `sync-to-agents.sh` dijalankan sekali (pengujian):

```
target: 21f242e60d829f6c   ← sama dengan bank = ISI BARU TERTIMPA
```

**Tindakan pengamanan yang sudah diambil (non-destruktif):**
`vault/_konflik-skill/2026-09-19/hermes-terminal-workflows.TARGET-SKILL.md`
(sha `dc5943a1912f17db`, 8.097 B, folder `vault/` di-ignore git → tidak bocor ke repo publik).

---

## 4. Enam kelas risiko bila promosi dipasang naif

| # | Risiko | Dampak | Mitigasi yang diperlukan |
|---|--------|--------|--------------------------|
| R1 | **Timpa-menimpa** — sync (bank→target) jalan sebelum promosi (target→bank) | Suntingan target hilang **sebelum** sempat dipromosikan | Pindai divergensi **sebelum** sync; jangan pernah timpa |
| R2 | **Skill bawaan Hermes** (54) ikut dipromosikan | Bank mengklaim milik Hermes; update Hermes berikutnya ditimpa balik oleh bank (versi basi) | Kecualikan via `.bundled_manifest` |
| R3 | **Skill dari hub** (12 instal) ikut dipromosikan | Sama seperti R2 + konflik update hub | Kecualikan via `.hub/lock.json` |
| R4 | **Resurrect** — skill yang sengaja dihapus dari bank masih ada di target | Skill mati hidup kembali tanpa keputusan | Ledger/tombstone |
| R5 | **Bank lebih baru, target basi** → promosi menurunkan mutu | Bank mundur ke versi lama | Promosi hanya bila target terbukti lebih baru, atau khusus yang belum ada di bank |
| R6 | **Churn commit & repo kotor** bila promosi tanpa aturan commit | Bank terus kotor / riwayat penuh commit bot | Aturan commit eksplisit |

---

## 5. Tiga jalur kegagalan senyap (ditemukan saat audit)

1. **Lock contention dianggap sukses.** `sync-to-agents.sh` baris 58–59: bila lock aktif →
   `echo "⚠️ Lock aktif…"; exit 0`. Lightfix menyalin keluaran lalu menyaring
   `grep -E 'Sync selesai|verifikasi hash'` → kosong → tetap mencetak `✓ sync:` dan `rc=0`.
   Bukti: log `[19:58:38] ✓ sync:` dan `[19:59:06] ✓ sync:` — **kosong tapi hijau**.
   Artinya: bila lock pernah macet, cron dapat **berhenti menyinkron sambil lapor sukses**.

2. **Regresi tanpa alarm (sudah diperbaiki).** Saat membersihkan referensi Jcode saya menghapus
   parameter `structure` dari `sync_target`, tetapi `verify_target … "$structure"` masih
   memakainya → `set -u` menghentikan skrip di baris 151. Akibat: langkah **verifikasi +
   lockfile + registry** terlewat. Hanya ketahuan karena sync dijalankan manual
   (`unbound variable`); lightfix sendiri sedang tertutup jalur (1). Sudah diperbaiki;
   sync kini tuntas (`verifikasi hash LULUS`, lock `145/145`, exit 0).

3. **`skills-lock.json` tidak bisa mendeteksi perubahan target.** Lock menyimpan
   `bundleHash` **milik bank** (diverifikasi: `lock == manifest bank` = True; `bundle(dir target)`
   berbeda). Jadi lock selalu "terlihat cocok" walau isi target sudah diubah.
   **Hanya** `skill-manifest.py --verify-target` yang benar-benar mendeteksi
   (menemukan tepat 1 mismatch saat audit).

---

## 6. Desain usulan (aman, konflik-terkendali)

**Prinsip: deteksi dulu, jangan pernah menimpa, promosi konservatif, semuanya terlihat di laporan.**

### 6.1 Penjaga "never clobber" (mutlak, sebelum sync)
Sebelum `sync`, bandingkan tiap file target vs `manifest.json` bank:
- file target **cocok** manifest → aman ditimpa (memang salinan bank).
- file target **berbeda** → **JANGAN timpa**. Skill itu dikarantina: dilewati, dicatat,
  dan dilaporkan ke up-eco sebagai konflik yang butuh keputusan manusia.

### 6.2 Promosi konservatif (target → bank)
Sebuah skill dipromosikan **hanya bila semua** terpenuhi:
1. folder skill ada di `~/.hermes/skills/…` dan punya `SKILL.md` berfrontmatter valid (`name`/`description`);
2. **tidak ada** skill bernama sama di bank (aman: tidak menimpa apa pun);
3. **bukan** bawaan Hermes (`.bundled_manifest`);
4. **bukan** hasil instal hub (`.hub/lock.json`);
5. **tidak** ada di ledger tombstone (pernah sengaja dihapus dari bank);
6. isinya tidak mengandung pola kredensial (pemeriksaan sebelum tulis).

Skill yang "ada di kedua sisi tapi berbeda" **tidak** dipromosikan otomatis → masuk daftar
konflik untuk keputusan manusia (menghindari R1 & R5).

### 6.3 Ledger keputusan
`skills/.promotion-ledger.json` mencatat: `promoted` (nama + hash + waktu), `ignored-bundled`,
`ignored-hub`, `tombstone` (sengaja dihapus dari bank). Tujuannya: idempoten + mencegah R2/R3/R4
berulang.

### 6.4 Urutan baru di lightfix
```
[0] pindai divergensi (bank vs target)          ← baru, read-only, WAJIB pertama
[1] promosi konservatif (target → bank)         ← baru, hanya kelas aman
[2] penjaga never-clobber → sync bank → target  ← diubah
[3] manifest → INDEX → verifikasi → log
[4] autocommit: hanya churn timestamp (tetap)
```

### 6.5 Perbaikan kejujuran laporan (wajib, terpisah dari promosi)
- Sync membedakan `Sync selesai`, `Lock aktif (skip)`, dan gagal — lightfix **tidak** boleh
  mencetak `✓` untuk skip; skip = `⚠️ dilewati`, bukan sukses.
- `verify_target` dijalankan **setelah** sync sebagai pemeriksaan independen; bila ada
  mismatch → `rc≠0` supaya cron tidak hijau palsu.
- `write_lockfile` jangan menyembunyikan error (`2>/dev/null` → simpan dan laporkan).

### 6.6 Kebijakan commit
Promosi menulis isi baru ke bank → **tidak** ikut autocommit (autocommit tetap khusus churn
timestamp). Default: bank dibiarkan kotor agar manusia meninjau. Opsi `--commit-promosi`
tersedia bila Anda ingin otomatis (tetap tanpa push).

---

## 7. Matriks keputusan (perlu persetujuan pemilik)

| # | Pertanyaan | Opsi | Rekomendasi |
|---|-----------|------|-------------|
| D1 | Mode promosi | (a) otomatis utk skill lokal baru + karantina konflik · (b) deteksi & lapor saja · (c) manual penuh | **(a)** |
| D2 | Skill yang ada di kedua sisi tapi berbeda | (a) karantina + lapor, jangan timpa · (b) bank menang (perilaku kini) · (c) yang terbaru menang | **(a)** |
| D3 | Commit hasil promosi | (a) tidak auto-commit (tinjau dulu) · (b) commit otomatis tanpa push · (c) commit + push | **(a)** |
| D4 | Isi yang salah tertimpa (`hermes-terminal-workflows`) | (a) gabungkan ke bank lalu sync · (b) biarkan, cukup arsip di vault | **(a)** |

---

## 8. Rencana uji (sebelum menyentuh data nyata)
1. Sandbox dua arah: bank & target tiruan di `/tmp`, jalankan skrip yang sama dengan path diarahkan.
2. Skenario wajib: (i) skill lokal baru → dipromosikan; (ii) bundled → diabaikan;
   (iii) hub → diabaikan; (iv) tombstone → tidak hidup lagi; (v) target lebih baru →
   tidak ditimpa, masuk karantina; (vi) bank lebih baru → target mengikuti bank.
3. Uji idempoten: dua kali run berturut-turut → perubahan kedua = 0.
4. Uji jalur gagal: lock aktif → dilaporkan "dilewati", bukan sukses; sync error → `rc≠0`.
5. Baru setelah lulus semua, jalankan pada data nyata + verifikasi hash bank/target.

---

## 9. Lampiran bukti (perintah & hasil)

```
# penyalinan tanpa --delete
grep -n 'rsync' skills/sync-to-agents.sh            → rsync -a --quiet  (tanpa --delete)

# kerusakan nyata
shasum target sebelum sync  → dc5943a1…(8.097 B, 19 Sep 20:02)
shasum target sesudah sync  → 21f242e6…(5.391 B, sama dgn bank)

# lock tidak mendeteksi
lock[k].bundleHash == manifest bank[k].bundleHash   → True
bundle(dir target)                                  → 5dd22747… (berbeda)

# detektor yang benar
python3 scripts/skill-manifest.py --verify-target ~/.hermes/skills --structure domain
  → [FAIL] 0 hilang, 1 mismatch: software-development/hermes-terminal-workflows/SKILL.md

# pemisahan 68 skill target
bundled 54 · hub 0 (dari 12 instal) · lokal 14
lokal: audit-finding-triage, content-pipeline-readiness, derived-artifact-consistency,
       live-ui-audit, llm-call-reliability, mobile-viewport-remediation, model-mapping-repair,
       pre-cleanup-artifact-preservation, production-secret-rotation, project-handover-package,
       responsive-ui-audit, sapa-ai, short-form-video-production, web-ui-audit-measurement

# jalur kegagalan senyap
sync baris 58-59  → "⚠️ Lock aktif — sync sedang berjalan. Skip." + exit 0
lightfix log      → "[19:58:38] ✓ sync:" (kosong, rc=0)
```

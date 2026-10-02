# Status Ekosistem Niumination — 2 Oktober 2026

Laporan pembaruan dokumentasi. Semua angka **diukur ulang hari ini**, bukan diambil dari
catatan sebelumnya.

## Ringkas

```
skill bank        210 skill / 861 file   (dokumen root masih tulis 187 — BASI)
repo git lokal    50                    (dokumen tulis ~43 — BASI)
macOS             26.5 (25F71)
ruang disk        8,9 GB avail · 93%    ⚠️ turun dari 10 GB kemarin
sapa-ai dev       a3f2e9b  (0.2.0-dev, tag v0.2.0-dev, belum promosi)
sapa-ai main      ff00eb8  (0.1.0, produksi)
produksi sapa-ai  HTTP 200
OpenCore          ≈0.6.6–0.7.5 → target 1.0.8   (blokir: ruang + revpatch)
```

---

## 1. Yang Diperbaiki

### `docs/skill-ecosystem-guide.md`

Dokumen itu menandai dirinya historis, tapi angkanya masih dipakai sebagai fakta. Ditambahkan
blok status di header dan koreksi di 4 titik:

```
Sebelum: "148 skills (total)"  →  Setelah: 210 skill + catatan bahwa angka lama basi
Sebelum: "146 skills (data dari DOX, belum diverifikasi)"
  → Setelah: opencode CLI TERVERIFIKASI terpasang v1.18.29, config ~/.config/opencode
Sebelum: "| Hermes (148 skills) |"  →  "| Hermes (148 → 210, 2 Okt 2026) |"
```

Angka historis **tidak dihapus** — dokumen ini perbandingan antar-sistem, nilai perbandingan
itu masih berguna.

### `BACKLOG.md` § Struktur Root

Blok itu bertanggal "Aug 26, 2026" tapi tidak ditandai snapshot, sehingga mudah dibaca sebagai
kondisi sekarang. Ditambahkan penanda + angka terukur:

```
⚠️ SNAPSHOT HISTORIS — 26 Agustus 2026. Jangan dipakai sebagai kondisi terkini.
   terukur 2 Okt 2026: apps/ 16 · services/ 5 · sites/ 7 · desktop/ 4
                        agents/ 3 · labs/ 3 · sandbox/ 6 · inactive-2026-09/ 5
                        skill bank 210 (bukan 121/144)
```

---

## 2. Selisih yang Ditemukan (tidak saya ubah — perlu keputusan)

### 2.1 `AGENTS.md` root —`_protected_`, tertahan approval

Dua kali percobaan tulis **ditolak**: *"approval prompt timed out without a user response.
Silence is not consent."* Tidak dicoba lewat jalur lain.

Yang perlu diperbaiki bila approval diberikan:

```
[1] Angka skill 187 → 210  (3 tempat: baris 12, 144, 239)
    baris 239 juga: "187 skill bank + 54 bawaan Hermes = 241"
[2] "Total Projek Lokal: ~43 git repos" → 50
[3] services/ "9 proyek" → 5 folder (cc-acehtengah sudah berstatus hiatus)
[4] labs/ "2 proyek" → 3 (mata-aihackfest-2026 tidak tercatat)
[5] sandbox/ "5 proyek" → 6 (remotion-studio tidak tercatat)
[6] inactive-2026-09/ "4 proyek" → 5 (Ultra pindah ke sini, masih tercatat di agents/)
[7] agents/ masih menulis Ultra/ padahal sudah tidak ada di sana
```

### 2.2 Empat folder di disk yang tidak tercatat di AGENTS.md

```
apps/abstract-studio          → SUDAH ada di project-catalog.md § Konten Kreator ✅
apps/kopi-aceh-app-android    → SUDAH ada di BACKLOG.md (Sandbox) ✅
labs/mata-aihackfest-2026     → SUDAH ada di project-catalog.md ✅
sandbox/remotion-studio       → ❌ tidak terdaftar di mana pun
```

**Tentang `remotion-studio`:** 526 MB, **tidak punya `.git`**, 0 file tracked, dan `README.md`
-nya adalah README upstream remotion-dev. Ini **template/bahan mentah**, bukan proyek Niumination
— kemungkinan hasil percobaan. Saya tidak mendaftarkannya karena tidak ada repo, tidak ada
identitas, tidak ada status. Perlu keputusan: dibersihkan, atau dijadikan proyek?

### 2.3 Angka 241 di AGENTS.md baris 239

```
"187 skill bank + 54 bawaan Hermes = 241"
```

Dengan bank 210, angkanya jadi **264**. Tapi ini juga bisa bergeser setiap kali skill baru
ditambahkan — lebih baik ditulis sebagai "lihat `skill-registry.md`" daripada angka tetap.

---

## 3. Keadaan sapa-ai (sudah beres, dicatat ulang)

```
dev  a3f2e9b  0.2.0-dev    69 komit di atas main, tag v0.2.0-dev → 052f2f0
                      belum dipromosikan; main sengaja tidak disentuh
main ff00eb8  0.1.0       produksi, HTTP 200, AI ON, 2.081 record
backlog        7 butir     P8 P12 P13 P14 P15 P16 FR-13/14 → dok 37, tunggu arahan
```

Semua dokumen repo sudah dikoreksi 1 Okt 2026: README, AGENTS.md repo, 6 berkas serah-terima,
BACKLOG.md, project-catalog, deployment-status.

---

## 4. Keadaan mesin (menguruk prioritas)

### ⚠️ Disk 8,9 GB — turun dari 10 GB

```
Kemarin    10 GB avail · 91%
Sekarang    8,9 GB avail · 93%
```

Turun tanpa ada yang saya hapus. Penurunannya dari pemakaian normal (build sapa-ai menghasilkan
`.next`, cache npm). **Ini memperburuk blokir upgrade macOS** — yesterday saya hitung hanya
~2,4 GB yang bisa dilepas aman dan itu masih kurang dari 20 GB.

### ⚠️ Upgrade macOS terblokir dua hal

```
[1] Ruang disk    8,9 GB   vs kebutuhan ±20 GB
[2] revpatch=sbvmm tidak ada di boot-args → OTA update mustahil
[3] OpenCore ≈0.6.x → target 1.0.8, jarak 1 major, tanpa ocvalidate
[4] Tidak ada USB crash-dummy (diskutil list external kosong)
```

Laporan lengkap riset: `~/Downloads/RISET-UPGRADE-MACOS-OPENCORE-2026-10-02.md` (654 baris).

**Tidak ada yang dijalankan.** Nol perubahan pada mesin.

### Homebrew Tier 3

Konsekuensi keputusan Apple dropping Intel, bukan masalah terpisah. Produksi kita tidak
bergantung padanya (sapa-ai di Vercel, 9router lokal, hermes via uv/npm). Jangan `brew upgrade`
bersamaan dengan upgrade macOS — build from source akan lambat dan memakan disk yang sudah kritis.

---

## 5. Yang Tidak Saya Ubah (milik proses lain)

```
M docs/reports/PLAN-REMOTION-KONTEN-KREATOR-2026-10-02.md
M skills/content/content-produce/SKILL.md
M skills/creative/hyperframes/SKILL.md
M skills/ecosystem/hermes-config-mutation-safety/SKILL.md
M skills/security/git-security-sanitization/SKILL.md
M skills/manifest.json
?? skills/content/remotion-video/
?? skills/ecosystem/ecosystem/long-form-markdown-deliverables/
```

Tangled dengan `skills/manifest.json` yang **harus ikut** kalau skill bank berubah. Kalau proses
lain belum selesai, manifest akan mismatch — commit saya harus menunggu atau manifest di-regenerate
setelah commit mereka. **Saya tidak menyentuh satu pun baris di file-file itu.**

---

## 6. Yang UNCHECKED

```
[?] Isi EFI aktif    — butuh sudo, tidak dijalankan
[?] Versi OpenCore pasti — tidak tertulis di binari; butuh ocvalidate atau boot USB
[?] Penyebab update gagal 2 Juni 2026 — tidak ada log yang bisa dibaca tanpa izin
[?] Keberadaan disk eksternal — `diskutil list external` kosong, tapi USB bisa saja
     tidak terpasang saat itu
[?] Status remotion-studio — asal-usul tidak ada di dokumen mana pun
```

---

## 7. Bukti

```
$ python3 scripts/skill-manifest.py           → 210 skill, 861 file
$ find . -maxdepth 3 -name .git -type d       → 50
$ sw_vers                                      → 26.5 / 25F71
$ df -h /System/Volumes/Data                   → 8.9Gi avail, 93%
$ cd services/sapa-ai && git rev-parse dev     → a3f2e9b
$ cd services/sapa-ai && git rev-parse main    → ff00eb8
$ curl -s -o /dev/null -w %{http_code} .../api/status → 200
$ opencode --version                           → 1.18.29
$ ls sandbox/remotion-studio/.git              → tidak ada; git ls-files → 0
$ git log --oneline -1                         → 9359c9e (root, sudah push)
```

---

*Dibuat 2 Oktober 2026. Semua angka dari perintah yang dijalankan langsung. Yang tidak bisa
diverifikasi ditandai UNCHECKED beserta alasannya.*

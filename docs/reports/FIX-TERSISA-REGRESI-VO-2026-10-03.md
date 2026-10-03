# REGENERASI FIX JOBAK — DOKUMENTASI REGRESI

**Tanggal:** 2 Okt 2026 (dilanjutkan 3 Okt 2026)
**Akses:** thread 1172 Konten Kreator
**Tugas pemilik:** "fix dulu yang tersisa"

## Kenapa laporan ini ada

Permintaan itu ternyata jauh lebih besar dari daftar 7 berkas yang tersisa.
Sedang mencari file, saya menemukan **dua commit berbeda bernama remotion**
di dua path, dan saat membandingkan isinya saya menemukan **fix v1.1.0 VO
saya di-revert oleh commit sinkronisasi rutin** enam jam setelah ia di-commit.

## 1. Regresi VO — fix v1.1.0 saya hilang

```
de8be93  24 Sep  skill gemini-vo-narration: cabut fallback edge-tts, tambah jejak provenance (v1.1.0)
ccd57d8  24 Sep  chore(lightfix): sinkronisasi skill bank pasca hapus Mobile-Harness   <- 6 jam kemudian
```

`ccd57d8` menghapus **92 baris** dari fix itu dan memulihkan 21 baris lama.
Bukti langsung dari git:

| | `de8be93` (fix) | `ccd57d8` (kini) |
|---|---|---|
| panggilan `edge_cadangan()` di alur utama | ada, sebagai jalur gagal | ada, dipulihkan |
| `provenance` | 2 | 0 |
| `SKILL.md version` | `1.1.0` | `1.0.0` |
| baris `SKILL.md` | — | **27 baris hilang** |

Yang dipulihkan berbahaya: bila Gemini kehabisan kuota, mesin menulis suara
edge-tts ke berkas bernama `vo_charon.mp3`. Nama berkas itu jadi bohong, dan
tidak ada penanda di dalam berkas bahwa mesinnya bukan Charon. **Itu persis
penyebab reels-001 stuck di `5.PPRODUK — BLOKIR: VO USANG`** dan tidak ada
cara memverifikasinya.

Fix-nya dipulihkan dari `de8be93`. Verifikasi:

```
SKILL.md version                : 1.1.0
panggilan edge_cadangan(naskah, akhir) : 0      <- harus 0
provenance                      : 2
klaim "Peralihan otomatis"      : 0      <- harus 0
return 1 saat Gemini gagal      : ada
sintaks python (py_compile)     : OK
```

Gagagalan Gemini kini `return 1` dengan pesan yang menyuruh mengecek kuota
atau merekam sendiri — dan menolak berkas bernama `vo_charon.mp3` berisi
mesin lain. Fungsi `edge_cadangan()` tetap ada sebagai barikade `raise
RuntimeError` supaya alasannya tidak hilang dari riwayat.

**Verifikasi yang gagal di jalan:** grep `edge_cadangan(naskah` mengembalikan
1, sehingga sempat dilaporkan "fallback dipulihkan". Yang tertangkap adalah
baris `def edge_cadangan(naskah: str, ...)` di baris 186 — definisi, bukan
panggilan. Pemanggilannya bernama `utama()`, bukan `main()`, sehingga grep
pertama yang mencari `def main` kosong. Pemanggilan riilnya 0.

### Mengapa fix-nya bisa hilang

`ccd57d8` melakukan "sinkronisasi skill bank" dan menimpa `de8be93` —
kemungkinan ia mengambil salinan skill dari luar dan menulisnya kembali. Ini
bukan kasus tunggal: `SKILL.md` gemini-vo-narration ikut kehilangan 27 baris
di commit yang sama. **Pola: commit sinkronisasi rutin bisa menghapus fix yang
baru saja di-commit tanpa pesan.** Belum ada mekanisme di ekosistem ini yang
mendeteksi itu.

## 2. Duplikat skill remotion — dua path, satu lebih baru

```
skills/content/remotion-video/              dibuat 0af6a41 (2 Okt)
skills/ecosystem/content-remotion-video/    dibuat bf34ab2 (2 Okt, lebih baru)
```

Bukan kecelakaan. Yang hilang dari salinan `ecosystem/` justru garis pengaman:

```
content/.../SKILL.md          : "... Free tier ≤3 org). SCOPE: thread Konten Kreator (1172) saja."
ecosystem/.../SKILL.md        : "... Free tier ≤3 org)"     <- tanpa SCOPE
```

Skill yang dibuat lebih dulu secara eksplisit dibatasi thread ini. Salinan
yang dibuat lebih baru — oleh mekanisme sinkronisasi, bukan oleh siapa pun —
melepaskan pembatasan itu. Jika skill berisiko dipakai lintas thread, yang
harus dipindahkan adalah salinan `content/` yang masih membawa penanda, bukan
kebalikannya.

Template keduanya identik setelah perbaikan `-q`. Keputusan menyatukan dua
path ini **tidak saya ambil** — ia membutuhkan keputusan thread 802 yang
membuatnya.

## 3. Bug `-q 480` — diperbaiki di 5 berkas

`-q` di Remotion 4.0.532 adalah alias `--quiet` ("Reduce console output"),
bukan kualitas video. Dipastikan dari `npx remotion render --help`:

```
--jpeg-quality <value>     JPEG Quality
--quiet, -q                Reduce console output.
```

Maka `... -q 480` diparse sebagai `-q` (true) lalu `480` dimakan sebagai argumen
composition berikutnya. Yang benar: `--jpeg-quality 80`.

Diperbaiki di **5 berkas** (3 SKILL.md + 2 template):

- `skills/content/remotion-video/SKILL.md` + `templates/formats/remotion-shorts.json`
- `skills/ecosystem/content-remotion-video/SKILL.md` + `templates/formats/remotion-shorts.json`
- `skills/content/content-produce/SKILL.md`

Tersisa 0 di `skills/`. Satu kemunculan di laporan dokumentasi kemarin
dibiarkan — itu kutipan bug, bukan perintah yang akan dijalankan.

Ditemukan di luar template yang kemarin dilaporkan hilang: `-q 480` ternyata
ada **di 3 SKILL.md juga**, bukan hanya di template.

## 4. Skill hyperframes — pin + flag yang wajib

Skill itu tidak punya catatan pin sama sekali (`0.8.30` = 0, `low-memory` = 0,
`workers 1` = 0), padahal keduanya terbukti wajib di mesin ini. Ditambahkan
beserta angka ukurnya:

| Flag | Bukti |
|------|-------|
| `hyperframes@0.8.30` | lint CLI 0.8.62 tanpa pin = 6 warning; dengan pin = 0 error, 0 warning |
| `--low-memory-mode` | render pertama reels-003 (1628 frame) **ditolak otomatis** tanpa ini — butuh 13,5 GB; dengan flag sukses 262 detik |
| `--workers 1` | dipakai di `render-v4.sh`. **MOTIFNYA BELUM DIUKUR** — saya tidak pernah membandingkan `--workers 1` vs 2, jadi alasan teknisnya ditulis UNCHECKED |

## 5. Revideo, Piper, Kokoro — ditandai, bukan dihapus

**`revideo-motion-graphic`** — `npx revideo render` macet 7 jam 4 menit tanpa
menulis output. Frontmatter diubah menjadi `ARSIF` supaya mesin trigger tidak
menemuinya sebagai rekomendasi. Ditahan sebagai arsip karena fakta bahwa
`revideo render` tidak ada di CLI 0.11 tetap relevan.

**`reels-motion-render`** — judul `+ Piper` → `+ Gemini TTS`; prioritas suara
Piper→Kokoro diganti Charon dikunci; path mux `vo_piper_clean.wav` →
`vo-gemini/vo_charon.mp3`.

**`content-produce`** — urutan prioritas lama (suara sendiri→Piper→Kokoro) dan
blok bash-nya ditandai DITOLAK untuk studio ini, alasan teknisnya tetap ditulis.
Revideo diganti HyperFrames + Remotion. Skill ini lintas-ekosistem, jadi jalur
lama tidak dihapus — orang lain di ekosistem masih boleh membutuhkannya.

## 6. Koreksi yang saya buat kemarin: `loudnorm I=-14` itu BENAR

Kemarin saya menghapus `loudness_target_lufs: -14` dari
`templates/formats/coding-demo.json` dengan alasan "angka itu bukan hasil
pengukuran". Setelah mengukur hari ini, **angka itu benar**:

```
ffmpeg -i vo_charon.mp3 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -

  input_i    : -19.85    <- VO Gemini reels-003 sebelum dinormalkan
  input_tp   : -4.66
  input_lra  : 5.10
  output_i   : -15.41    <- persis angka final video yang lolos QA
  output_tp  : -1.50
  output_lra : 3.70
  normalization_type : dynamic
```

Saya kembalikan target-nya ke template, beserta bukti pengukuran dan catatan
yang kemarin saya lewatkan: `normalization_type` keluar sebagai `dynamic`,
bukan `linear`, jadi **`LRA=11` tidak benar-benar dipaksa** — hasil LRA nyatanya
3,70.

Yang tetap salah dari teks lama: alasan `-ar 48000` menulis "Piper output 192
kHz". VO Gemini-nya keluar **44,1 kHz**, bukan 192 kHz (terukur `ffprobe`).
Alasannya diganti, nilainya tetap wajib.

Satu lagi yang ditemukan: `skills/content/content-produce/SKILL.md` baris 92
dan 101 masih menulis `loudnorm=I=-16:TP=-1.5`. Saya **tidak mengubahnya** —
dan setelah dibaca utuh, ini benar: baris 162–163 dokumen itu memang
membedakan `-14` untuk video sosial dari `-16` untuk podcast, jadi `-16` di
dua baris itu adalah konteksnya sendiri, bukan angka yang basi. Saya berhenti
sebelum salah mengedit angka yang sebenarnya benar. Catatan untuk pemilik:
target `-16` podcast itu **UNCHECKED**, tidak terukur untuk VO Gemini mana pun.

## 7. Yang sengaja tidak saya lakukan

- **`manifest.json` tidak saya regenerasi.** Regenerasi akan menyerap 4 file
  untracked milik thread lain (`a2a-configuration/`, `hermes-a2a-setup/`,
  `macos-hackintosh-opencore/`, `references/agent-skills-catalog.md`) dan
  menimpa diff 8 baris yang sedang mereka pegang. Manifest kini tercatat 1145
  berkas terhadap 224 SKILL.md ter-track — angka itu harus dirapikan oleh
  pemilik, bukan saya menimpa kerjannya di tengah jalan.
- **Skill `content-studio`** tidak disentuh — jalur utamanya masih menunjuk
  Revideo dan Kokoro, tetapi scope-nya seluruh ekosistem.
- **Duplikat remotion** tidak disatukan — milik thread 802.
- **13 kemunculan kata Piper, 12 edge-tts, 11 Revideo** di SKILL.md lain
  tidak semuanya diubah: yang masih benar sebagai penjelasan penolakan
  dibiarkan, yang masih merekomendasikan diganti atau ditandai.

## 8. Daftar untuk pemilik

1. **Perlu mekanisme anti-regresi.** `ccd57d8` menghapus fix `de8be93` enam jam
   setelahnya tanpa pesan peringatan. Dua fix dapat hilang seperti itu lagi.
2. **Keputusan duplikat remotion** — mana yang menjadi satu home, dan garis
   `SCOPE: thread Konten Kreator (1172) saja` harus dibawa oleh yang menang.
3. **`loudnorm I=-16` vs `-14`** — mana yang benar untuk studio ini. `-14`
   terukur; `-16` tertulis di urutan prioritas arsip.
4. **Manifest 1145 berkas vs 224 SKILL.md ter-track** — belum konsisten.
5. **`scripts/scan-env-writers.py`** untracked, belum pernah dibuka.
   `UNCHECKED` — saya tidak membacanya. Nama itu menunjuk pemindai penulisan
   `.env`, yang bisa saja memuat nilai kredensial bila dijalankan sembarangan.
6. **Backup `data/_backup/pripindah-niu-konten-2026-09-24/`** sudah di-ignore
   oleh commit lain (`cb99087`), jadi keputusan itu bukan milik saya.

## Bukti

```
# Regresi VO
git diff --stat de8be93 ccd57d8 -- skills/creative/gemini-vo-narration/
  -> gemini_vo.py 84 baris berubah, SKILL.md 27 baris hilang

git show ccd57d8:skills/creative/gemini-vo-narration/scripts/gemini_vo.py | grep -c provenance   -> 0
git show ccd57d8:skills/creative/gemini-vo-narration/SKILL.md  | grep -m1 '^version:'           -> 1.0.0
git show de8be93:skills/creative/gemini-vo-narration/SKILL.md   | grep -m1 '^version:'           -> 1.1.0

# Pasca-fix (berkas kerja hari ini)
grep -c 'edge_cadangan(naskah, akhir' gemini_vo.py   -> 0
grep -c provenance gemini_vo.py                      -> 2
python3 -c "import py_compile; py_compile.compile(...)" -> OK

# Flag Remotion
npx remotion render --help  ->  --jpeg-quality <value> | --quiet, -q  (bukan kualitas)
grep -rl -- "-q 480" skills/  -> 0 berkas

# Loudness terukur
ffmpeg -i vo_charon.mp3 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -
  input_i -19.85 | output_i -15.41 | normalization_type dynamic
ffprobe vo_charon.mp3  -> sample_rate 44100, channels 2
```

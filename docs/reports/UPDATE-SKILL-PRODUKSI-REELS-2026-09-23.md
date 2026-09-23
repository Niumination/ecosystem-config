# UPDATE SKILL PRODUKSI REELS — hasil belajar reels-003

**Tanggal:** 2026-09-23
**Skill:** `creative/short-form-video-production` — v1.3.0 → **v1.4.0**
**Pemicu:** produksi reels-003 (4 versi, 3 ditolak) mengungkap 5 celah prosedural.

## Yang masuk ke skill

Lima pitfall baru di section Pitfalls:

1. **GSAP pakai waktu mutlak.** Mengubah `data-start` saja tidak memperbaiki sinkronisasi.
   Semua timing GSAP di dalam scene harus ditulis ulang mengikuti batas baru.
2. **Pin versi HyperFrames.** 0.8.62 menghasilkan 6 warning lint bawaan; pin ke 0.8.30
   (versi reels-002) memberi 0 errors 0 warnings.
3. **`--low-memory-mode` saat disk tipis.** 1628 frame @1080×1920 butuh ~13,5 GB temp;
   gunakan streaming 1-worker bila disk tersedia <15 GB.
4. **Loudness: ikuti take referensi, jangan tebak angka dari ingatan.**
5. **Setelah mengubah batas scene, render dan vision-check tiap scene.**

## Satu kesalahan yang saya perbaiki saat menulis ini

Awalnya saya tulis bullet `-14 LUFS` sebagai target. **Tidak ada sumber yang mendukung angka itu.**
Tidak ada SKILL.md, laporan, atau config di ekosistem ini yang menyatakan target LUFS apa pun.
Angka yang lama tercatat di skill ini (-16 LUFS) juga bukan spesifikasi pemilik — hanya preset
ffmpeg di satu contoh pipeline.

Pengukuran berkas VO asli yang sudah disetujui pemilik membuktikan hal lain:

| Berkas | Integritas | TP | LRA |
|---|---|---|---|
| `reels-002/vo/vo_utuh.mp3` (standar dikunci 19 Sep) | -19,58 LUFS | -5,08 | 4,50 |
| `reels-003/vo_charon.mp3` (VO final) | -19,85 LUFS | -4,66 | 5,10 |
| reels-003 v4.1 final (video, diterima pemilik) | -15,40 LUFS | -1,17 | 3,70 |

Jadi bullet-nya saya tulis ulang menjadi instruksi untuk **mengukur take referensi yang sudah
diterima** dan mencocokkannya, bukan menerapkan target dari ingatan. Mendorong ke -14 berarti
+5 dB gain di atas VO yang sudah disetujui — itu keputusan pemilik, bukan keputusan agent.

## Masalah proses yang ditemukan

`scripts/skill-manifest.py` punya dua bug yang mengkhianati operator:

- `--verify-target` default-nya `structure="flat"`, sedangkan target Hermes memakai struktur
  `domain`. Lupa flag → laporan "173 skill hilang" padahal semua berkas ada dan hash-nya benar.
  Wajib: `--verify-target DIR --structure domain`.
- `skill_manage(action='patch')` menulis ke **target** `~/.hermes/skills/`, bukan ke bank pusat.
  Konsekuensinya sync guard menolak (karantina "disunting di target") dan hash verify gagal.
  Untuk skill bank pusat, edit harus masuk `~/Desktop/Niumination/skills/` lalu disinkronkan
  lewat `scripts/skill-manifest.py` + `skills/sync-to-agents.sh`.

Urutan yang benar (terverifikasi pada sesi ini):

```bash
cd ~/Desktop/Niumination
python3 scripts/skill-manifest.py                                   # 1. regenerate manifest
bash skills/sync-to-agents.sh                                        # 2. sync bank → target
python3 scripts/skill-manifest.py --check                            # 3. 0 mismatch
python3 scripts/skill-manifest.py --verify-target ~/.hermes/skills \
    --structure domain                                               # 4. 809 file, 0 masalah
```

## Bukti

- `skill-manifest.py --check` → `0 mismatch`
- `--verify-target ~/.hermes/skills --structure domain` → `809 file diverifikasi, 0 masalah`
- Bank pusat == target Hermes: identik, 406 baris, versi 1.4.0
- 9 berkas bundle identik kedua sisi (SKILL.md + 3 references + 3 scripts + 2 templates)

## Catatan

`references/voiceover-delivery.md` belum saya sentuh — ia sudah memuat section 0 tentang
pilihan engine dan kuota per-model, yang konsisten dengan apa yang terjadi di reels-003.
Tidak ada kontradiksi baru yang perlu diluruskan di sana.

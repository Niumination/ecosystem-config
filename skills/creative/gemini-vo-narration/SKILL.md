---
name: gemini-vo-narration
description: "Voice-over narasi Bahasa Indonesia standar Niumination (Gemini TTS, gratis). Pakai saat membuat VO/narasi/dubbing untuk reels, video, atau pengumuman."
version: 1.0.0
author: Afrizal Munthe (Niumination)
tags: [creative, tts, voice-over, narasi, gemini, gratis, audio]
platforms: [macos, linux]
---

# Gemini VO Narration — Standar Voice-Over Niumination

**Status:** DIKUNCI 19 Sep 2026 oleh pemilik. Menggantikan seluruh pendekatan edge-tts +
normalisasi teks berlapis.

**Trigger:** membuat voice-over / narasi / dubbing Bahasa Indonesia untuk konten apa pun.

---

## Aturan yang mengikat (jangan dilanggar)

1. **Kirim naskah APA ADANYA.** Jangan "memasak" teks. Gemini TTS berbasis LLM — sudah
   paham angka, tanggal, singkatan, dan campuran Indonesia–Inggris. Menambah ejaan buatan
   (`es ka pe de`, `titik web titik id`, `Rp` → `rupiah`) membuat ucapan **terpenggal**.
2. **Gaya diatur lewat prompt, bukan lewat teks.** Satu tambalan teks TIDAK PERNAH
   memperbaiki kualitas suara.
3. **Tag audio wajib berbahasa Inggris**, walau naskahnya Indonesia. Aksen diatur lewat
   style prompt, **bukan** lewat setelan bahasa.
4. **Jangan taruh dua tag berdampingan** — harus dipisah teks atau tanda baca.
5. **Satu permintaan = satu naskah utuh.** Kuota gratis 10/hari **per model** (bukan per
   akun). Memanggil per-adegan membuang kuota tanpa manfaat.
6. **Jangan normalisasi sebelum terbukti mesinnya salah.** Buktikan dulu, baru tambal.

## Mesin

`scripts/gemini_vo.py` — mandiri, tanpa dependensi ke skrip lama.

```bash
# produksi
python3 scripts/gemini_vo.py naskah.txt --suara charon --preset narator --keluaran out/

# lihat pilihan
python3 scripts/gemini_vo.py --daftar-suara

# pembanding tanpa arahan gaya (untuk A/B)
python3 scripts/gemini_vo.py naskah.txt --tanpa-gaya --nama charon_polos
```

Keluaran selalu dinormalkan ke standar MATA: **44,1 kHz · stereo · 192 kbps**.

Model: `gemini-3.1-flash-tts-preview` (utama) → cadangan `gemini-2.5-flash-preview-tts` →
`gemini-2.5-pro-preview-tts` → terakhir `edge-tts` bila kuota habis. Peralihan otomatis.

## Suara

| Kunci | Karakter resmi Google | Pakai untuk |
|---|---|---|
| `algenib` | Gravelly (serak, berkarakter) | storytelling, narasi personal |
| `charon` | Informative | narator data publik, laporan resmi |
| `sadaltager` | Knowledgeable (berwawasan) | edukasi, penjelasan teknis |

Ketiganya **disetujui pemilik** (19 Sep 2026) dan dipakai untuk **variasi antar konten** —
bukan hanya satu suara untuk semua. 14 suara lain tersedia lewat `--daftar-suara`.

## Preset gaya

`narator` · `pengumuman` · `edukasi` · `story` — lihat `references/prompt-dan-tag.md`
untuk isi lengkap dan cara menambah preset baru.

## Verifikasi WAJIB sebelum menyatakan selesai

1. **Dengar sendiri kalau bisa.** Penilaian telinga pemilik adalah ukuran akhir.
2. **Pastikan model tidak membacakan instruksinya sendiri.** Ini mode gagal resmi Gemini:
   kalau audio dimulai dengan "Synthesize speech…" / "Audio profile…" / "Pak Rizal…",
   prompt gagal dan hasilnya **tidak layak dipakai**. Yang menjamin: preamble +
   pembatas `#### TRANSCRIPT` (sudah ada di script).
3. **Bedakan BENAR dari NATURAL.** Ucapan bisa sepenuhnya benar secara pelafalan tapi
   terdengar kaku dan terpotong. STT hanya membuktikan yang pertama.

## Kesalahan yang sudah pernah terjadi — jangan diulang

Baca `references/kasus-gagal.md` sebelum mengubah apa pun di skill ini. Isinya enam
kegagalan nyata beserta sebabnya, termasuk mengapa pendekatan lama menghasilkan suara yang
lebih buruk daripada sebelumnya.

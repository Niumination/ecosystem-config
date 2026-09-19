# Standar Voice-Over Niumination — berlaku untuk seluruh konten

**Status:** DIKUNCI pemilik 19 Sep 2026. Menggantikan seluruh pendekatan sebelumnya.
**Berlaku untuk:** semua konten ke depan — reels, video, pengumuman, dubbing, narasi apa pun.
**Standar tertulis (untuk agent):** skill `skills/creative/gemini-vo-narration/` (tersinkron ke Hermes)

---

## 1 · Mesin

| Peran | Mesin |
|---|---|
| Utama | **Gemini TTS** — `gemini-3.1-flash-tts-preview` |
| Cadangan otomatis | `gemini-2.5-flash-preview-tts` → `gemini-2.5-pro-preview-tts` |
| Cadangan terakhir | `edge-tts` (`id-ID-ArdiNeural`) bila kuota habis |

Keluaran selalu dinormalkan ke **44,1 kHz · stereo · 192 kbps** (standar MATA).

**Gratis:** kuota tier gratis **10 permintaan/hari per model per proyek** — dan kuota tiap model
**terpisah**, sehingga model cadangan tetap bisa dipakai setelah yang utama habis. Kode galat:
`429 RESOURCE_EXHAUSTED`, `quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier`.

Satu permintaan memuat **satu naskah utuh** (batas aman aplikasi ±1500 karakter) — bukan per
adegan — supaya kuota tidak terbuang.

## 2 · Suara yang dikunci

Ketiganya disetujui pemilik dan dipakai untuk **variasi antar konten**, bukan satu suara seragam:

| Kunci | Karakter resmi Google | Dipakai untuk |
|---|---|---|
| `algenib` | Gravelly (serak, berkarakter) | storytelling, narasi personal |
| `charon` | Informative | narator data publik, laporan resmi |
| `sadaltager` | Knowledgeable (berwawasan) | edukasi, penjelasan teknis |

Preset gaya siap pakai: `narator`, `pengumuman`, `edukasi`, `story`.

## 3 · Enam aturan yang mengikat

1. **Kirim naskah apa adanya.** Gemini TTS berbasis LLM dan sudah memahami angka, tanggal,
   singkatan, serta campuran Indonesia–Inggris. Menambah ejaan buatan merusak hasilnya.
2. **Gaya diatur lewat prompt, bukan lewat teks.**
3. **Tag audio wajib berbahasa Inggris** walau naskahnya Indonesia; aksen lewat style prompt,
   bukan setelan bahasa.
4. **Jangan taruh dua tag berdampingan** — harus dipisah teks/tanda baca.
5. **Satu permintaan = satu naskah utuh.**
6. **Jangan normalisasi sebelum terbukti mesinnya salah.**

## 4 · Cara pakai

```bash
python3 skills/creative/gemini-vo-narration/scripts/gemini_vo.py naskah.txt \
        --suara charon --preset narator --keluaran out/
```

Script mencetak durasi, format, ukuran, dan md5 sebagai bukti. Peralihan ke cadangan otomatis.
Pilihan lain: `--daftar-suara`, `--tanpa-gaya` (pembanding A/B), `--preset tanpa`.

## 5 · Verifikasi yang wajib dilakukan

1. **Telinga pemilik adalah ukuran akhir.** Penilaian pada A/B buta, bukan angka.
2. **Pastikan model tidak membacakan instruksinya sendiri** — mode gagal resmi Gemini. Kalau
   audio dimulai dengan "Synthesize speech…", "Audio profile…", atau nama tokohnya, prompt gagal
   dan hasilnya tidak layak dipakai. Pencegahnya sudah tertanam di script (preamble +
   pembatas `#### TRANSCRIPT`).
3. **Bedakan BENAR dari NATURAL.** Ucapan bisa tepat secara pelafalan tetapi terdengar kaku dan
   terpotong. Uji pelafalan tidak pernah boleh dipakai sebagai bukti kualitas suara.

## 6 · Referensi

1. Panduan prompt Gemini 3.1 Flash TTS — 200+ audio tag, formula tag
   https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-1-flash-tts-on-google-cloud
2. Gemini API — speech generation (30 suara, bahasa didukung, struktur prompt)
   https://ai.google.dev/gemini-api/docs/speech-generation
3. Panduan prompt AI Studio (profil audio, adegan, catatan performa)
   https://aistudio.google.com/learn/gemini-tts-prompt-guide-with-tags
4. Google Cloud — Gemini-TTS (Indonesia **GA**, kontrol gaya)
   https://docs.cloud.google.com/text-to-speech/docs/gemini-tts
5. Batas laju Gemini API (tier gratis, per model)
   https://ai.google.dev/gemini-api/docs/rate-limits
6. LiveKit — kegagalan prompt yang terdokumentasi (*"period-separated fragments sound chopped"*)
   https://livekit.com/blog/gemini-3.1-flash-tts-prompting-guide
7. ElevenLabs — mengapa angka/akronim salah diucapkan ("tulis seperti yang ingin diucapkan")
   https://help.elevenlabs.io/hc/en-us/articles/14888917355409
8. Perbandingan model TTS 2026 — ELO arena, MOS proprietary vs open-source
   https://ocdevel.com/blog/20250720-tts
9. Tinjauan model TTS open-source 2026
   https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models
10. Normalisasi teks untuk voice AI
    https://vapi.ai/blog/text-normalization

## 7 · Yang dihapus (kunci + bersih)

Seluruh pendekatan lama dihapus permanen sesuai instruksi pemilik:

- **Mesin lama `edge-tts` beserta lapis normalisasi teks** — `tts_hermes.py`,
  `pelafalan_tambahan.py`, `kamus_pelafalan.json` (128 entri), driver `gen_vo*.sh` / `mix_vo*.sh`
- **~50 skrip kerja** — rekon, harness, uji emas, forensik suara (sweep 98 render, DTW, timbre,
  f0/YIN), probe Gemini, dan pembangun audisi lama
- **Aset antara** — 3 audisi lama, mixer wav, berkas potongan, frame, lembar QA, dan video
  ber-VO lama (dapat dirender ulang dari sumber `reels-001/`)
- **Model STT lokal** — whisper `base` + `medium` (1,7 GB)
- **Dua laporan antara** — laporan perbaikan pelafalan dan dokumen rencana; pelajarannya
  dipindahkan ke skill (`references/kasus-gagal.md`), rujukannya diserap ke dokumen ini

Yang **tetap disimpan**: sumber proyek `reels-001/`, master tanpa suara
`reels-001-final-silent.mp4`, dan audisi terkunci `audisi_komprehensif/`.

## 8 · Bukti

- Skill tersinkron: `skills/creative/gemini-vo-narration/` → **145 skill, 716 berkas,
  verifikasi hash LULUS**, `skills-lock.json` ditulis
- Uji mesin: `gemini_vo.py` → Gemini 3.1 Flash TTS, **19,08 s**, `44100,2,192000`, md5
  `e0e890d8f029358295bdddf45b2196d9`
- Audisi terkunci: `~/Downloads/niu-konten/audisi_komprehensif/audisi_komprehensif_gemini.mp3`
  (334,2 s — 3 suara bergaya + 1 kontrol tanpa gaya)
- Naskah audisi: 916 karakter, memuat campuran id/en, singkatan, angka, rupiah, persen,
  nomor telepon, email/URL, dan versi

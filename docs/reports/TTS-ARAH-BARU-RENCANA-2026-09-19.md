# Arah Baru Produksi Voice-Over — Riset & Rencana (19 Sep 2026)

**Status:** RENCANA — menunggu keputusan pemilik. Belum ada eksekusi.
**Pemicu:** penilaian pemilik bahwa hasil perbaikan pelafalan justru **lebih buruk** dari sebelumnya,
dan instruksi: cari referensi dulu, tentukan tujuan yang tepat, baru eksekusi.

---

## 1 · Diagnosis jujur: mengapa hasil saya lebih buruk

| # | Kesalahan | Akibat |
|---|---|---|
| 1 | **Mengoptimasi proksi, bukan hasil.** Saya menguji "teks apa yang dikirim ke mesin", bukan "apa yang terdengar". | Uji saya hijau, tapi telinga mendengar buruk. |
| 2 | **Menebak masalah tanpa verifikasi.** Saya asumsikan mesin gagal membaca `SKPD`/angka/URL, padahal tidak pernah saya buktikan. | Memperbaiki hal yang mungkin sudah benar. |
| 3 | **Menyiasati kualitas dengan teks, bukan dengan mesin.** `edge-tts` kelas menengah; saya menambal dengan teks yang di"masak" (`es ka pe de`, `titik web titik id`). | Ucapan jadi terpenggal dan robotik — **lebih buruk dari aslinya**. |
| 4 | **Menambah kerumitan, bukan mengurangi.** Kamus 128 entri + modul baru + transformasi berlapis. | Titik gagal bertambah; saya jadi berputar di hal yang tidak saya pahami arahnya. |

**Bukti pendukung dari referensi** (bukan pendapat saya) — panduan prompt Gemini TTS secara eksplisit
menyebut pola kegagalan yang persis saya alami:

> *"Use commas between tagged clauses, not periods. **Period-separated fragments sound chopped.**"*
> — [LiveKit, Gemini 3.1 Flash TTS prompting guide](https://livekit.com/blog/gemini-3.1-flash-tts-prompting-guide)

Normalisasi saya justru **memperbanyak kalimat-fragmen** (memecah jadi potongan pendek), yang menurut
praktisi adalah cara paling cepat membuat suara terdengar terpotong-potong.

---

## 2 · Referensi yang mendasari arah baru

**a. Normalisasi teks: benar tujuannya, salah dosis saya**
> *"We recommend writing numbers, acronyms, dates and symbols fully, in words, **in the way that you would
> like the AI to deliver them**."* — [ElevenLabs Help](https://help.elevenlabs.io/hc/en-us/articles/14888917355409)

Kuncinya: tulis **seperti Anda ingin mesin mengucapkannya**, bukan transkripsi harfiah.
`es ka pe de` = transkripsi harfiah; kalimat wajar = yang dimaksud.

**b. Kelas kualitas mesin: edge-tts bukan kelas atas**
Model proprietary berbasis LLM (Gemini, GPT-4o, ElevenLabs) mencapai **MOS 4,2–4,3**; model open-source
dan edge-tts berada di bawahnya — [ringkasan benchmark TTS 2026](https://www.youtube.com/watch?v=reI_6DOzxEQ).
Artinya: **masalah saya adalah pilihan mesin, bukan teks.**

**c. Gemini TTS layak dijadikan mesin utama**
- **Bahasa Indonesia: GA (Generally Available)** — [Google Cloud Gemini-TTS](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts)
- **30 suara** dengan deskriptor karakter — [Gemini API speech generation](https://ai.google.dev/gemini-api/docs/speech-generation)
- **Dikendalikan bahasa alami**: gaya, aksen, tempo, tone
- **Audio tag** `[whispers]`, `[very slow]`, `[warmly]` untuk mengatur penekanan & jeda
- **Output PCM 24 kHz mono** — persis properti berkas `vo-manual` MATA

**d. Petunjuk kuat: voice-00 kemungkinan besar memang Gemini TTS**

| Bukti | Nilai |
|---|---|
| Format audio MATA (`vo-manual/*.mp3`) | 24 kHz mono — sama dengan keluaran Gemini TTS |
| Uji timbre saya vs `S0.mp3` | Algenib 0,0222 · Sadaltager 0,0235 · **Charon 0,0302** |
| Pembanding `edge-tts` Ardi | 0,0465 (lebih jauh dari ketiga suara Gemini) |
| Deskripsi Gemini untuk Charon | **"Informative"** — cocok dengan VOICE.md: *"narator pria, tenang"* |

Belum terbukti (timbre bukan sidik jari), tetapi ini **hipotesis terkuat** yang kita punya.

**e. Batas gratis — temuan yang menentukan kelayakan**

```
quotaId    : GenerateRequestsPerDayPerProjectPerModel-FreeTier
quotaValue : 10     model: gemini-2.5-flash-tts
```

**10 permintaan/hari per model** (bukan per akun) — dan **per model terpisah**, terbukti:
`gemini-3.1-flash-tts-preview` masih bisa saat `gemini-2.5-*` sudah habis.

Konsekuensi: **cara pakai harus berubah dari per-adegan menjadi per-video.**
Satu permintaan bisa memuat seluruh naskah reels (±350 karakter), lalu dipotong per adegan lewat
deteksi sunyi. 10 permintaan/hari = 10 video/hari, bukan 1,5 video.

---

## 3 · Tujuan yang tepat (usulan, untuk disetujui)

> **Menghasilkan narasi voice-over Bahasa Indonesia yang terdengar natural — setara atau lebih baik
> dari voice-00 MATA — dengan biaya Rp 0 dan bisa diulang sendiri tanpa bergantung sesi luar.**

Ukuran keberhasilan **bukan** proksi teks, melainkan:

1. **Penilaian telinga pemilik** pada A/B buta (dua versi, tanpa diberi tahu mana yang mana).
2. **Konsistensi** — suara & gaya sama di semua video.
3. **Gratis & berulang** — masuk batas harian, tanpa langganan.

Bukan tujuan: "semua akronim dieja sempurna", "setiap simbol ditangani". Itu berarti alat, bukan hasil.

---

## 4 · Arah teknis yang diusulkan

### 4.1 Mesin
| Peran | Mesin | Alasan |
|---|---|---|
| Utama | **Gemini TTS** (`gemini-3.1-flash-tts-preview`, cadangan `gemini-2.5-flash-tts`) | Kelas atas, Indonesia GA, gratis 10/hari/model, bisa diarahkan gaya |
| Cadangan saat kuota habis | `edge-tts` (`id-ID-ArdiNeural`) | Selalu tersedia, tanpa kuota |
| Opsional (nanti) | Kloning `voice-00` dari `S3.mp3` (F5-TTS) | Hanya kalau pemilik ingin voice-00 persis |

### 4.2 Perubahan cara pakai
- **Satu permintaan per video**, bukan per adegan → hemat kuota 6×
- Potong per adegan lewat **deteksi sunyi** (perkakas ini sudah ada dan terbukti)
- Keluaran dinormalkan ke standar MATA (`44,1 kHz · stereo · 192 kbps`, lead 0,60/tail 0,80)

### 4.3 Gaya lewat prompt, bukan lewat teks
Ikuti struktur yang terbukti dari referensi — **preamble penyintesis + `#### TRANSCRIPT`**, karena tanpa
itu model membacakan instruksi gaya sebagai kalimat:

```
Synthesize speech for the performance defined below. Profile, scene, and notes are
direction only. Do NOT speak them. Speak ONLY the lines under #### TRANSCRIPT.

# AUDIO PROFILE: Narator MATA
## "Pembaca data publik yang tenang dan faktual"

## SCENE: Studio sunyi, narasi dokumenter investigatif
### PERFORMANCE
Style: tenang, percaya diri, tidak dramatis
Pace: sedang; berhenti sejenak sebelum angka penting
### CONTEXT
Ia membaca temuan audit; nadanya menahan diri, tanpa menghakimi.

#### TRANSCRIPT
<teks naskah apa adanya, dengan [audio tags] di titik yang perlu jeda/penekanan>
```

### 4.4 Nasib kerja normalisasi yang sudah saya buat
| Bagian | Putusan | Alasan |
|---|---|---|
| Pengejaan huruf akronim | **Dipertahankan, tapi hanya untuk `edge-tts`** | Uji awal: Gemini mentah 3,40 s vs dieja 4,00 s → Gemini **belum** mengeja sendiri |
| `titik`/`per` untuk URL & garis miring | **Dibuang untuk Gemini** | Sumber utama suara terdengar aneh |
| Eja angka (rupiah, persen, tahun) | **Perlu diuji ulang** | Kuota habis sebelum selesai diuji |
| Tanggal/jam/telepon/rentang | Perlu diuji ulang | Belum terverifikasi untuk Gemini |
| Emoji/markdown/bullet | Dipertahankan (aman) | Buang sampah tidak pernah salah |

**Prinsip baru: jangan normalisasi sebelum terbukti mesinnya salah.**

---

## 5 · Yang belum terverifikasi (dinyatakan jujur)

1. Apakah Gemini sudah membaca angka/rupiah/URL dengan benar tanpa bantuan — **kuota habis** sebelum diuji.
2. Apakah voice-00 benar-benar Gemini — bukti bersifat indikatif, bukan pasti.
3. Apakah 10 permintaan/hari cukup untuk volume konten pemilik.
4. Kualitas pemotongan per adegan hasil deteksi sunyi pada audio Gemini.

---

## 6 · Rencana langkah (setelah disetujui)

| Langkah | Isi | Kuota |
|---|---|---|
| 1 | **Audisi suara** — 4–5 suara pria Gemini pada naskah reels, dikirim ke pemilik untuk dinilai telinga | ~5 |
| 2 | **Uji potong-per-adegan** — satu permintaan berisi seluruh naskah, potong lewat deteksi sunyi, cek sinkron | ~2 |
| 3 | **Uji normalisasi minimal** — mana yang benar-benar perlu untuk Gemini; buang sisanya | ~6 |
| 4 | **Integrasi** — ganti mesin di jalur produksi; `edge-tts` jadi cadangan | — |
| 5 | **Adopsi ke bank skill** (butuh approval terpisah) | — |

---

## 7 · Daftar referensi

1. Gemini API — speech generation (30 suara, audio tag, struktur prompt, bahasa didukung)
   https://ai.google.dev/gemini-api/docs/speech-generation
2. Google Cloud — Gemini-TTS (Indonesia **GA**, kontrol gaya, daftar bahasa)
   https://docs.cloud.google.com/text-to-speech/docs/gemini-tts
3. Gemini API — rate limits (tier gratis, per model)
   https://ai.google.dev/gemini-api/docs/rate-limits
4. LiveKit — panduan prompt Gemini 3.1 Flash TTS (*"period-separated fragments sound chopped"*)
   https://livekit.com/blog/gemini-3.1-flash-tts-prompting-guide
5. ElevenLabs — mengapa angka/akronim salah diucapkan ("tulis seperti yang Anda ingin diucapkan")
   https://help.elevenlabs.io/hc/en-us/articles/14888917355409
6. Perbandingan model TTS 2026 — ELO arena, harga, MOS proprietary vs open-source
   https://ocdevel.com/blog/20250720-tts
7. BentoML — tinjauan model TTS open-source 2026 (Kokoro, Chatterbox, VibeVoice, NeuTTS)
   https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models
8. Vapi — panduan normalisasi teks untuk voice AI
   https://vapi.ai/blog/text-normalization
9. Chatterbox Multilingual — dukungan Bahasa Indonesia (PR #507, 24 bahasa)
   https://github.com/resemble-ai/chatterbox/issues/507
10. Qwen3-TTS — cakupan bahasa (catatan: **tidak** termasuk Indonesia)
    https://github.com/QwenLM/Qwen3-TTS

---

## 8 · Bukti pengukuran (perintah yang dijalankan)

- Model TTS tersedia dengan kunci pemilik: `gemini-2.5-flash-preview-tts`,
  `gemini-2.5-pro-preview-tts`, `gemini-3.1-flash-tts-preview` (dari `GET /v1beta/models`)
- Batas gratis terbaca dari respons 429: `quotaId GenerateRequestsPerDayPerProjectPerModel-FreeTier`,
  `quotaValue 10`, `model gemini-2.5-flash-tts`
- Kuota terpisah terbukti: `gemini-3.1-flash-tts-preview` berhasil saat `gemini-2.5-*` habis
- Timbre vs `S0.mp3` (voice-00): Algenib 0,0222 · Sadaltager 0,0235 · Charon 0,0302 · Gacrux 0,0385 ·
  Rasalgethi 0,0442 · Iapetus 0,0474 — pembanding `edge-tts` Ardi 0,0465
- Akronim pada Gemini 3.1: teks mentah **3,40 s** vs dieja **4,00 s** (+0,60 s)
- Skrip: `hipotesis_gemini.py` · `uji_normalisasi_gemini.py` · `cek_kuota_gemini.py`

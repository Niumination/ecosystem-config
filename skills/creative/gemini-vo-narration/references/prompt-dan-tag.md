# Prompt Gaya & Audio Tag — Gemini TTS

Sumber: [Google Cloud — Guide to prompting Gemini 3.1 Flash TTS](https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-1-flash-tts-on-google-cloud) ·
[Gemini API — speech generation](https://ai.google.dev/gemini-api/docs/speech-generation) ·
[LiveKit — prompting guide](https://livekit.com/blog/gemini-3.1-flash-tts-prompting-guide)

## Struktur prompt yang dipakai script

```
Synthesize speech for the performance defined below. The profile, scene, and
performance notes are direction only. Do NOT speak them. Speak ONLY the lines
under #### TRANSCRIPT.

# AUDIO PROFILE: <Nama + inisial>
## "<satu baris deskripsi persona>"

## SCENE: <nama adegan singkat>
<2–3 kalimat: tempat, suasana, sikap tubuh, vibe>

### PERFORMANCE
Style: <nada & register emosi. Jangan "datar" atau "pelan".>
Pace: <satu momen ritmis yang spesifik>
Accent: <deskriptor aksen singkat>

### CONTEXT
<1–2 kalimat: siapa tokoh ini dan mengapa suaranya seperti itu>

#### TRANSCRIPT
<teks yang diucapkan + audio tag>
```

**Dua bagian yang menanggung beban:**
- Paragraf preamble penyintesis (mencegah model membacakan instruksi)
- Pembatas `#### TRANSCRIPT`

Sisanya bisa disesuaikan gaya penulisan.

## Aturan tag

| Aturan | Keterangan |
|---|---|
| Bahasa | **Wajib Inggris**, walau naskahnya bahasa lain |
| Posisi | Tepat di titik transisi yang diinginkan |
| Pemisah | Harus dipisah teks/tanda baca — **dua tag berdampingan = galat sistem** |
| Aksen | Diatur lewat style prompt, bukan lewat setelan bahasa |

Formula: `[tag tempo]` + teks + `[tag ekspresi]` + teks + `[tag jeda]` + teks

## Tag yang sering dipakai

**Ekspresi:** `[determination]` `[enthusiasm]` `[interest]` `[awe]` `[admiration]`
`[curiosity]` `[hope]` `[amusement]` `[tension]` `[agitation]` `[confusion]`
`[frustration]` `[annoyance]` `[neutral]` `[positive]` `[negative]` `[serious]`
`[thoughtfully]` `[warmly]` `[gently]`

**Tempo & jeda:** `[slow]` `[fast]` `[short pause]` `[long pause]` `[very slow]` `[very fast]`

**Non-verbal:** `[laughs]` `[sighs]` `[whispers]` `[gasp]` `[cough]` `[giggles]`

Total ada **200+ tag** dan tidak ada daftar tertutup — teks di dalam `[ ]` bebas dikarang,
model akan berusaha menafsirkannya. Untuk modifier non-emosional (`[whispers]`, `[very slow]`)
tag bebas bekerja baik.

## Preset yang tersedia di script

| Preset | Karakter | Cocok untuk |
|---|---|---|
| `narator` | Pak Rizal — tenang, jelas, tidak dramatis | data publik, laporan, narasi investigatif |
| `pengumuman` | Bu Sari — resmi, bersahabat, ada wibawa | instruksi instansi, pengumuman rapat |
| `edukasi` | Kak Danu — hangat, antusias, sabar | penjelasan teknis, tutorial |
| `story` | Bang Iyan — reflektif, sedikit serak, personal | cerita pengalaman, behind-the-scenes |

**Menambah preset:** sunting `PRESET` di `scripts/gemini_vo.py`. Ikuti struktur yang sama —
profil, adegan, performa, konteks — lalu tambahkan ke tabel di atas.

## Catatan teknis

- Keluaran mentah: PCM `audio/L16` 24 kHz mono → script menormalkan ke 44,1 kHz stereo 192 kbps
- Audio diberi watermark **SynthID** oleh Google (bawaan model, tidak bisa dimatikan)
- Batas teks aman aplikasi ±1500 karakter per permintaan; script memperingatkan bila lewat
- Kuota gratis: **10 permintaan/hari per model per proyek** — kode galat `429`
  dengan `quotaId: GenerateRequestsPerDayPerProjectPerModel-FreeTier`

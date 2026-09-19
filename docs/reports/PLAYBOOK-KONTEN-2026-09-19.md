# Playbook Konten Thread Kreator — Riset & Templat (19 Sep 2026)

**Untuk:** thread Kreator (Niu-MissionControl #1172)
**Isi:** (1) penilaian provider huancheng, (2) konsep konten yang sedang trending, (3) templat siap pakai
**Sifat:** referensi kerja — sumber diperbarui berkala karena tren berubah mingguan

---

# BAGIAN 1 · Provider huancheng — layak jadi partner konten?

**Konfigurasi:** `https://api.hcnsec.cn/v1` · mode `chat_completions` · kunci `HUANCHENG_API_KEY` · model default `auto`
**Diperiksa:** 19 Sep 2026 — `/v1/models` → **HTTP 200**, **27 model**

## Model yang tersedia, menurut kegunaan konten

| Kegunaan | Model | Catatan |
|---|---|---|
| **Menulis naskah / caption / ide** | `kimi-k3`, `qwen3.8-max`, `glm-5.3`, `DeepSeek-V4-Pro`, `DeepSeek-V4.1-Flash`, `MiniMax-M3`, `Qwen3.8-27B`, `spark-x2.5`, `mimo-v2.5-pro`, `step-3.7-flash` | semua mendukung endpoint `openai` (sebagian juga `anthropic`) |
| **Suara (TTS)** | `stepaudio-2.5-tts` | endpoint `openai` |
| **Pengenal suara (ASR)** | `stepaudio-2.5-asr` | endpoint `openai` |
| **Audio percakapan / realtime** | `stepaudio-2.5-chat`, `stepaudio-2.5-realtime` | — |
| **Gambar (sunting)** | `step-image-edit-2` | mendukung `image-generation` |
| **Pencarian makna** | `Qwen3-Embedding-8B` | untuk arsip/brain |
| **Router** | `step-router-v1`, `auto` | pemilih model otomatis |

## 1b · Hasil uji — kesimpulan: BELUM layak jadi partner produksi

**Pelajaran utama: daftar model ≠ model yang bisa dipakai.** 27 model terdaftar, tetapi
setelah diuji satu per satu, hampir semuanya tidak dapat diakses dengan kunci ini.

### Model teks — 0 dari 6 bisa dipakai

| Model | Hasil uji |
|---|---|
| `qwen3.8-max` | HTTP 500 — *"分组 auto 下模型 qwen3.8-max 的可用渠道不存在"* = **tidak ada kanal tersedia untuk model ini** |
| `MiniMax-M3` | HTTP 500 — pesan sama |
| `kimi-k3` | tidak merespons (100 dtk, HTTP 000) |
| `glm-5.3` | tidak merespons (100 dtk) |
| `DeepSeek-V4.1-Flash` | tidak merespons (100 dtk) |
| `spark-x2.5` | HTTP 522 |

Artinya model-model itu **terdaftar di katalog tetapi tidak disediakan untuk akun ini**.
Tidak ada satu pun yang berhasil menulis teks.

### Suara (TTS) — sebagian bekerja, satu suara layak

5 voice ID diterima dan 4 menghasilkan audio Bahasa Indonesia. Diuji dengan transkripsi ulang:

| Voice | Transkrip hasil | Putusan |
|---|---|---|
| `cixingnansheng` (男声) | "Selamat pagi. Dashboard ini mengumpulkan 91 repo publik dan 41 tes lulus sebelum rilis." | **BERSIH — persis teks aslinya** |
| `qingniandaxuesheng` | "…mengupu 91 ribu publik… semen rilis" | rusak sebagian |
| `shenchennanyin` | "…91 W E P O P P U B L I C…" | salah ucap parah |
| `qinqienvsheng` | "…menkompre 91 report public. Then 41 test lulus se before release." | bercampur Inggris, berantakan |

**Satu suara yang layak: `cixingnansheng`.** Durasi 8,6 detik untuk dua kalimat.

### Pengenal suara (ASR) & gambar — gagal

- `stepaudio-2.5-asr` → tidak merespons (HTTP 000)
- `step-image-edit-2` → HTTP 522

## Putusan

**Jangan jadikan partner produksi sekarang.** Dari 27 model yang terdaftar, yang benar-benar
 bisa dipakai hanya **satu suara TTS**, dan itu pun hanya berguna kalau kuota Gemini habis.

**Yang layak disimpan sebagai catatan:**
- `cixingnansheng` bisa jadi **cadangan suara** bila kuota Gemini TTS habis — tapi belum
  dibandingkan langsung dengan Charon oleh telinga pemilik
- **Endpoint-nya tidak stabil** (522 berulang, permintaan menggantung sampai 100 detik) —
  tidak cocok untuk pekerjaan bervolume
- Kalau kapan-kapan model teksnya ingin dicoba lagi, uji dulu satu model sebelum
  merencanakan apa pun di atasnya

**Catatan penting:** kegagalan-kegagalan ini bukan bukti providernya buruk selamanya —
bisa jadi soal paket langganan, wilayah, atau waktu. Yang jelas: **hari ini, dengan kunci ini,
provider ini belum bisa diandalkan.**

## Hal yang perlu diwaspadai

- **TTS-nya milik StepFun** (perusahaan Tiongkok). Saat diuji, voice ID yang dicoba semua
  ditolak (`voice_id_invalid`). Artinya daftar voice-nya perlu dicari dari dokumentasi StepFun,
  dan **dukungan Bahasa Indonesia belum terbukti** — jangan diasumsikan ada.
- **ASR-nya perlu uji ulang**: percobaan pertama mengembalikan `HTTP 522` (batas waktu
  Cloudflare), bukan jawaban sah.
- `stepaudio-2.5-tts` **bukan pengganti** Gemini TTS yang sudah dikunci. Gemini punya
  keunggulan terbukti: Bahasa Indonesia status GA, 30 suara berkarakter, bisa diarahkan
  gaya dengan bahasa alami, dan gratis 10 permintaan/hari/model.

---

# BAGIAN 2 · Konsep konten yang sedang trending (September 2026)

Sumber utama: New Engen (diperbarui tiap Senin, terakhir 1 Sep 2026), CreatorFlow
(29 Agu 2026), Buffer (Apr 2026), Socialinsider (Jul 2026).

## 2.1 Perubahan algoritma yang mengubah cara membuat konten

**Yang paling penting: DM share mengalahkan like.**
Sinyal peringkat teratas Instagram 2026 adalah **watch time, like per reach, dan DM share** —
dan DM share berbobot **3–5× lebih tinggi daripada like**. Artinya **100 like kalah dari 10 DM share.**

Konsekuensinya untuk kita: konten harus **layak dikirim ke orang lain**, bukan sekadar layak di-like.
Bentuk yang memicu share: sumber yang berguna (daftar, templat, cara), pendapat yang relatable,
dan lelucon yang hanya dipahami kalangan tertentu.

**Data format (Q2 2026):**

| Format | Engagement per pengikut | Kekuatan |
|---|---|---|
| Carousel | **0,50%** (tertinggi) | kedalaman, konversi pengikut lama |
| Reels | 0,48% | **jangkauan**, menarik pengikut baru |
| Gambar statis | 0,33% | lemah — pakai hemat |

Hitungannya bukan "Reels vs Carousel", tapi **Reels untuk ditemukan, Carousel untuk diingat**.
Panjang Reels yang dianjurkan: **di bawah 90 detik**.

**Hashtag sudah mati.** Pengguna tidak lagi bisa mengikuti hashtag baru; penemuan sekarang
lewat **kata kunci di caption**. Pakai **3–5 hashtag saja**, sisanya taruh kata kunci di kalimat.

**Authenticity mengalahkan polesan.** Instagram menurunkan konten yang terlihat terlalu
diproduksi, sebagai reaksi atas banjir konten AI. Video "talking head selfie" mengalahkan
produksi kelas studio.

> **Ini bertabrakan langsung dengan format kita sekarang.** Reels 01 dan 02 adalah animasi
> HTML yang mulus dan sangat dipoles. Menurut temuan ini, kita berenang melawan arus.
> Perlu diuji: sisipkan rekaman layar nyata, terminal nyata, angka nyata — tekstur asli,
> bukan animasi sempurna.

## 2.2 Format yang sedang naik (dari 10 tren mingguan New Engen)

| Format | Inti | Kecocokan dengan kita |
|---|---|---|
| **Potential-Maxxing** | Membuktikan klaim dengan **angka keras**, bukan kata mutu | **Sangat tinggi** — kita punya 91 repo, 41 tes, 101 berkas JSON |
| **Flop-Core** | Memamerkan **kegagalan** dan momen memalukan, bukan kemenangan | **Tinggi** — kita punya bahan nyata: suara TTS yang gagal, jalan buntu berhari-hari |
| **10/10 Habits** | Hook rating: "kebiasaan yang saya nilai 10 dari 10" | Sedang — cocok untuk tips kerja |
| **Someone's Gotta Hold It Down** | Kebanggaan kampung sendiri, bukan kota besar | Sedang–tinggi — sudut Aceh Tengah |
| **Truck Driver Lip Sync** | Satu take tanpa potongan, membuktikan keaslian | Rendah — butuh talent di kamera |

## 2.3 Formula hook — bagian yang paling menentukan

Data yang konsisten dari beberapa sumber:

- **71% penonton memutuskan lanjut atau geser dalam 3 detik**; keputusan rata-rata terjadi di **1,7 detik**
- Hook kuat memberi engagement **340% lebih tinggi**; hold rate >60% mengalahkan <40% sebesar **5–10× jangkauan**
- **65%** yang melewati 3 detik akan menonton 10+ detik; **45%** menonton 30+ detik
- Jendela terbaik TikTok: **21–34 detik**

**Patokan angka untuk dinilai (benchmark):**

| Metrik | Target | Kelas tinggi |
|---|---|---|
| Hook rate Meta | 25%+ | 35–50% |
| Hook rate TikTok | 30%+ | 40–50% |
| Hold rate | 40%+ | 50–60% |
| Completion rate | 60%+ | 80%+ |

Tiga pemicu yang membuat hook bekerja: **keingintahuan** ("saya uji 30 hari dan…"),
**pengenalan diri** ("POV: kamu yang selama ini salah…"), dan **keterkejutan** ("berhenti lakukan ini").
Hook terkuat menggabungkan dua pemicu sekaligus.

---

# BAGIAN 3 · Templat siap pakai

## 3.1 Kerangka dasar (dipakai di semua templat)

```
HOOK      0–3 dtk    Hentikan gulir. Satu kalimat, satu ide.
MASALAH   3–10 dtk   Sebut rasa sakit yang sudah dirasakan penonton.
SOLUSI    10–20 dtk  Perkenalkan jawabannya. Jangan sebut merek di awal.
BUKTI     20–25 dtk  Satu hasil spesifik. Angka lebih baik daripada kata sifat.
CTA       akhir      Satu langkah saja, sebutkan persis.
```

Struktur 4 bagian ini mengalahkan iklan merek yang dipoles sekitar **40%**.

**Lima kesalahan umum:** membuka dengan nama merek · memimpin dengan fitur bukan masalah ·
CTA kabur ("cek saja") · terlalu panjang · tidak menguji variasi hook.

## 3.2 Lima templat naskah, siap diisi

**T1 · Pembuktian dengan angka** (paling cocok untuk kita)
```
HOOK    : [angka mengejutkan] dalam [satuan waktu/perbandingan]
MASALAH : cara lama memakan [waktu/biaya] yang tidak terlihat
SOLUSI  : [nama proyek] mengerjakannya lewat [cara]
BUKTI   : dari [X] jadi [Y], terukur
CTA     : [tautan] — atau simpan video ini
```

**T2 · Flop / kegagalan**
```
HOOK    : saya gagal [N] kali di [hal]
MASALAH : yang saya kira masalahnya adalah [dugaan awal] — ternyata bukan
SOLUSI  : yang benar-benar memperbaiki adalah [temuan]
BUKTI   : hasil setelah diubah
CTA     : kalau kamu pernah di posisi ini, simpan ini
```

**T3 · Bedah satu fitur (30–45 dtk)**
```
HOOK    : satu fitur, satu masalah yang dia selesaikan
MASALAH : begini cara lama melakukannya
SOLUSI  : demo fiturnya — LAYAR, bukan animasi
BUKTI   : hasil di akhir
CTA     : fiturnya ada di [tempat]
```

**T4 · Sebelum / Sesudah**
```
HOOK    : dulu begini, sekarang begini
MASALAH : derita versi lama, konkret
SOLUSI  : apa yang berubah
BUKTI   : angka sebelum vs sesudah
CTA     : detailnya di [tempat]
```

**T5 · Cara 60 detik**
```
HOOK    : cara [hasil] dalam [waktu]
LANGKAH : 3 langkah bernomor, masing-masing satu kalimat
BUKTI   : hasil setelah langkah terakhir
CTA     : simpan supaya tidak lupa
```

## 3.3 Dua puluh rumus hook

**Keingintahuan:** "Yang tidak ada yang bilang soal ___" · "Saya uji ___ selama 30 hari" ·
"Ini kenapa ___ selalu gagal" · "Rahasia ___ ternyata sepele" · "Saya salah soal ___ selama ini"

**Pengenalan diri:** "POV: kamu yang ___" · "Kalau kamu masih ___, ini untukmu" ·
"Ini literally [kondisi pembaca]" · "Tanda kamu sudah ___"

**Keterkejutan:** "Berhenti lakukan ___" · "___ itu ternyata tidak perlu" ·
"Saya buang ___ dan hasilnya lebih baik" · "Jangan pernah ___ sebelum ___"

**Angka keras:** "[N] ___ dalam [waktu]" · "Dari [X] jadi [Y]" ·
"[N]% orang salah soal ini" · "Cuma [N] langkah"

**Berlawanan arus:** "Semua orang bilang ___. Saya tidak setuju" ·
"___ bukan masalahnya. Ini masalahnya" · "Yang mahal itu bukan ___"

## 3.4 Kerangka mengubah satu ide jadi banyak konten

Satu bahan (misalnya satu rilis proyek) bisa jadi **minimal 5 keluaran**:
Reels pendek · Carousel · kutipan/kartu data · utas teks · dokumen panduan.

Urutan pengujian yang disarankan: **5 hook × 2 isi × 2 CTA = 20 varian**.
Algorithm butuh banyak varian untuk menemukan pemenang secara statistik.

## 3.5 Templat yang sudah kita miliki sendiri

Yang **sudah terbukti jalan** dan bisa dipakai ulang tanpa mencari ke luar:

- `~/Downloads/niu-konten/reels-002/index.html` — komposisi HyperFrames 6 adegan,
  **lint 0 error**, dengan palet merek dan struktur animasi yang bisa diganti isinya
- `skills/creative/gemini-vo-narration/` — mesin suara + 3 suara terkurasi + 4 preset gaya
  + alat verifikasi
- `~/Downloads/niu-konten/reels-002/caption.md` — contoh paket tayang lengkap

---

# BAGIAN 4 · Yang perlu diputuskan

1. **Melawan arus "authenticity"?** Temuan riset bilang konten yang terlalu dipoles diturunkan.
   Kita perlu menguji satu Reels berisi **rekaman layar asli + suara**, dan membandingkannya
   dengan format animasi sekarang. Bahannya sudah ada (`Perekaman Layar Niu-Journal.mov`,
   `Niu-ReflectAI.mov`).
2. **Dominasi DM share.** Konten kita perlu dirancang untuk **dikirim ke orang lain**, bukan
   dikagumi. Caranya: keluarkan sumber yang bisa dipakai orang (daftar, templat, cara), bukan
   hanya pamer hasil.
3. **Huancheng untuk pekerjaan bervolume.** Kalau hasil ujinya bagus, pakai untuk membuat
   20 varian hook sekaligus — pekerjaan yang butuh banyak, bukan yang butuh rasa.

---

# Referensi

**Algoritma & tren**
1. New Engen — Instagram Trends September 2026 (mingguan) — https://newengen.com/insights/instagram-trends/
2. CreatorFlow — 8 Instagram Trends 2026 (data Q2 2026) — https://creatorflow.so/blog/instagram-trends-2026-creators-marketers/
3. Later — Reels Trends 2026 — https://later.com/blog/instagram-reels-trends/
4. Pepper Agency — TikTok & Instagram Trends September 2026 — https://www.pepperagency.com/blog/tiktok-instagram-trends-for-september-2026-and-how-brands-can-actually-use-them
5. Metricool — Format yang bekerja di Instagram 2026 — https://www.youtube.com/watch?v=OAfe02UWUZA

**Hook & struktur naskah**
6. Opus Clip — Formula hook Reels (hold rate 3 detik) — https://www.opus.pro/blog/instagram-reels-hook-formulas
7. Reloop — 10 struktur naskah UGC + 20 rumus hook — https://reloop.so/blog/article/ugc-script-templates/
8. Virvid — 12 templat naskah video + benchmark metrik — https://virvid.ai/blog/12-free-ai-video-ad-script-templates-convert-2026
9. UGC Copilot — 12 hook viral 2026 — https://ugccopilot.ai/hooks/instagram-reels/
10. Fobet Media — Sains hook Reels 2026 — https://fobetmedia.com/instagram-reel-hooks/

**Data & templat**
11. Digital Applied — Statistik video marketing 2026 — https://www.digitalapplied.com/blog/video-marketing-statistics-2026-data-points
12. Postiv — 30 templat carousel Instagram — https://postiv.io/blog/instagram-carousel-templates
13. Cognism — Kerangka penggunaan ulang konten (P→A→D→R) — https://www.cognism.com/blog/content-repurposing
14. Canva — Templat carousel gratis — https://www.canva.com/templates/s/carousel/

**Catatan kaidah:** angka benchmark di bagian 2.3 sebagian berasal dari materi pemasaran vendor
(Reloop, Virvid). Angka algoritma (DM share 3–5×, engagement per format) berasal dari analisis
pihak ketiga yang merujuk Meta/Buffer/Socialinsider. **Perlakukan keduanya sebagai petunjuk arah,
bukan kebenaran pasti** — belum ada yang bisa saya verifikasi sendiri tanpa akses data akun.

## Berkas uji

- Skrip pengujian: `/tmp/uji_huancheng.py` (model teks, TTS, ASR, gambar) dan
  `/tmp/uji_tts_huancheng.py` (render Indonesian + verifikasi)
- Berkas audio hasil: `/tmp/hc_tts/{cixingnansheng,qingniandaxuesheng,shenchennanyin,qinqienvsheng}.mp3`
- Verifikasi transkripsi memakai `skills/creative/gemini-vo-narration/scripts/periksa_vo.py`

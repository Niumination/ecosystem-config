# Memilih engine motion graphics (brief-driven)

Tiga engine **setara** di studio ini — tidak ada yang default. Pilihan digerakkan brief,
bukan kebiasaan. Semuanya gratis, semuanya jalan tanpa GPU.

| Engine | Pilih bila | Batas yang perlu diketahui |
|---|---|---|
| **Motion Reel Kit** (MIT) | Motion design yang **dirancang**, bukan difilmkan: title sequence, showreel, logo animation, kinetic typography, explainer animasi. Butuh kunci audio-visual kuat dan grade broadcast | 1080p60 landscape 16:9 native; output lewat `reelctl`; tidak menelan footage — ia generate, bukan mengedit |
| **HyperFrames** (Apache-2.0, pin `@0.8.30`) | Reels/TikTok vertikal cepat; komposisi HTML/CSS/JS; reuse pola komposisi lama | Pin wajib; `--low-memory-mode` untuk komposisi > 50 detik; workers 1 di mesin 16 GB |
| **Remotion** (React) | Konten ≤ 30 detik yang sudah punya komponen React; butuh komposisi programatik di dalam aplikasi | CPU lambat > 30 detik; free tier ≤ 3 orang |

## Aturan pemilihan

1. **Jangan pilih dari kebiasaan.** HyperFrames sudah terbukti di ekosistem, tapi itu bukan alasan
   memakainya untuk pekerjaan yang butuh lock audio-visual. Baca brief dulu.
2. **Motion design yang "dirancang" → Motion Reel Kit.** Definisi praktis: hasilnya harus
   deterministic, bisa di-diff, dan musiknya menentukan clock visual — bukan soundbed yang ditempel
   setelah render.
3. **Footage yang sudah ada bukan domain engine mana pun di tabel ini.** Kit generate, tidak ingest;
   untuk memotong/menggabungkan rekaman, pakai jalur FFmpeg/auto-editor di `content-produce`.
4. **Komposisi > 50 detik di mesin 16 GB** → turunkan worker, atau pecah per babak.

## Yang membedakan Motion Reel Kit

- **Audio-visual lock.** `src/audio.py` mensintesis skor dari numpy dan menganalisisnya menjadi
  `spectrum.npz` (28 band per frame). Scene membaca band itu langsung, jadi gambar dan musik tidak
  "disinkronkan" — keduanya data yang sama. Mengedit `audio.py` **wajib** diikuti `reelctl score`,
  atau visual beranimasi ke aransemen lama.
- **Iterasi murah.** `reelctl shot <t> <png>` merender satu frame tergrade dalam 1–3 detik. Itu loop
  desainnya. `render` penuh 3–20 menit — jangan pernah dipakai untuk menjawab pertanyaan desain.
- **Verifier sendiri.** `reelctl verify` men-decode tiap frame; encode yang mati OOM meninggalkan file
  berukuran wajar yang tidak bisa diputar, dan `verify` menangkapnya.
- **Cut di beat.** Batas `TL` harus kelipatan `BEAT` dan cocok dengan `CUT_BEATS` di `audio.py`.
  Cut off-beat adalah kegagalan paling kentara pada motion reel. Cek dengan `reelctl timeline`.

## Setup (sekali per mesin)

Kit tinggal **di luar** repo ekosistem — struktur ekosistem tidak boleh dipolusi proyek video
(aturan yang sudah ditegur sebelumnya untuk HyperFrames). Skill bank hanya menyimpan pointer.

```bash
unzip ~/Downloads/<kit>.zip -d ~/          # -> ~/motion-reel-kit/
cd ~/motion-reel-kit && bash scripts/setup.sh
source .venv/bin/activate
python reelctl.py doctor                   # gate: harus READY
```

`setup.sh` memasang cairo/pkg-config/freetype lewat Homebrew (macOS), membuat `.venv`, dan meng-compile
`pycairo` dari source — wheel-nya hanya tersedia untuk Windows. Langkah terakhirnya menjalankan `doctor`,
jadi output setup sudah menjadi gate-nya. `doctor` juga memverifikasi font benar-benar termuat
(`metrics distinct 8/8`) — cairo mengganti font yang tidak dikenal secara diam-diam, dan teks jelek
akibat substitusi sulit dilacak dari kode.

## Output dan handoff

Kit menulis `out/MOTION_REEL.mp4` di root kit. Studio menuntut output di
`apps/abstract-studio/workspace/output/<slug>/`, jadi `content-produce` menyalin setelah render —
kit tidak di-patch untuk mengubah path.

## Gate sebelum klaim selesai

1. `reelctl doctor` → READY.
2. `reelctl shot` → PNG ada **dan dilihat** (agen yang tidak melihat frame-nya mendesain buta).
3. `reelctl render` selesai tanpa exit 137.
4. `reelctl verify` → PASS (decode semua frame).

Catat tool + verdict di `apps/abstract-studio/data/TOOL_DECISIONS.csv` (kolom: tanggal, tool, versi,
lisensi, verdict, catatan, review berikutnya) — itu ledger keputusan studio, bukan dokumentasi opsional.

# SAPA-AI — Investigasi Latensi & Toggle Admin (19 Sep 2026)

**Status:** selesai. 5/5 query produksi `used=true, grounded=pass`.
**Proyek:** `services/sapa-ai` — https://sapa-smart-ai.vercel.app
**Pemicu:** laporan pemilik — toggle admin dimatikan tetapi jawaban tetap keluar; setelah itu, dengan AI ON + deterministik OFF, dashboard membalas error "panggilan model gagal: timeout".

## Ringkasan

Empat cacat berbeda ditemukan dalam satu rantai. Tiga di antaranya adalah kesalahan implementasi sendiri; satu adalah kesalahan konfigurasi platform yang selama ini tidak terlihat.

- **Toggle tidak berefek** — state disimpan di `/tmp`, yang di Vercel bersifat per-instance dan mati saat idle.
- **Semantik toggle salah** — "deterministik" diperlakukan sebagai saklar seluruh layanan, padahal artinya hanya larangan jawaban template.
- **Timeout diulang** — retry berlaku untuk timeout, menggandakan waktu tunggu tanpa menambah peluang berhasil.
- **Fungsi berjalan di region yang salah** — `x-vercel-id: sin1::iad1::` menunjukkan eksekusi di Washington DC, sementara data dan pengguna ada di Indonesia.

## Akar masalah latensi

`curl -sI https://sapa-smart-ai.vercel.app/api/status | grep x-vercel-id`
→ `sin1::iad1::qq9wt-...`

Vercel menempatkan Serverless Function di `iad1` (Washington DC) secara default untuk proyek baru. Setiap permintaan menempuh: pengguna (Aceh) → edge sin1 → fungsi iad1 → SPLP (Indonesia) → penyedia model → kembali. Setelah `"regions": ["sin1"]` di `vercel.json`, eksekusi pindah ke Singapura dan latensi turun dari **38,7-41,9 dtk** menjadi **15,6-29,9 dtk**.

Pelajaran: sebelum menyalahkan model, periksa region eksekusi lebih dulu.

## Model bukan penyebabnya (diukur, bukan dikira)

Benchmark lokal lewat pipeline yang sama, 4 query identik, mesin dan jalur jaringan yang sama:

| Model | Hasil | Latensi |
|---|---|---|
| `glm-5.3` (produksi) | 4/4 `grounded=pass` | 13,7-23,4 dtk (rata 19,0) |
| `deepseek-v4-flash` (kandidat) | 4/4 `grounded=pass` | 10,6-27,6 dtk (rata 21,4) |

Keduanya sehat. `glm-5.3` setara atau sedikit lebih cepat. **Mengganti model tidak dibenarkan oleh data latensi** — keputusan model tetap terkunci pada pemilik.

## Yang diuji dan ditolak

- **Pangkas `AI_MAX_OUTPUT_TOKENS` 3000 → 1500.** 3 dari 4 jawaban terpotong sebelum JSON selesai (`used=false`, jatuh ke template). 3000 adalah titik manisnya; jangan dipangkas tanpa kalibrasi ulang.
- **Retry timeout.** Dihapus. Dulu timeout diulang karena bukan `LlmError`; hasilnya 42,6 dtk terbuang untuk jawaban yang sudah pasti gagal.
- **Tukar model demi latensi.** Lihat tabel di atas.

## Anggaran waktu akhir

Tiga lapis, berurutan dari dalam ke luar: model **48 dtk** → klien dashboard **55 dtk** → platform Vercel **60 dtk**. Klien sengaja paling longgar di antara keduanya agar pengguna menerima pesan error dari server, bukan "timeout" palsu dari sisi klien.

## Perubahan

Repo `Niumination/sapa-ai`, `main`:

- `ffeb826` `/api/query` membalas 503 saat layanan dimatikan admin, bukan 200
- `d994853` state toggle pindah `/tmp` → `@/lib/store` (Upstash); panel menampilkan backend
- `445c7ec` pagar toggle dipindah ke `selesai()`; 4 test penjaga
- `f36a7ce` semantik benar: deterministik OFF = larangan template, bukan mati layanan
- `789605e` timeout model tidak diulang + `maxDuration` untuk jalur stream
- `dd3f4e0` batas model 20 → 40 dtk; klien 45 → 55 dtk
- `0eafd25` `regions: ["sin1"]` — akar masalah latensi
- `0d67ab4` batas model 40 → 48 dtk

## Prasyarat infrastruktur

Toggle admin **memerlukan Upstash Redis** (`UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`). Tanpa itu, state hanya hidup per-instance dan panel akan tampak tidak berefek. Panel kini menampilkan backend yang aktif dan memberi peringatan bila `memory` — dulu kegagalan ini senyap.

## Verifikasi

- `npx tsc --noEmit` bersih; `npx vitest run` 162/162 hijau; `npm run build` sukses
- Toggle lintas-instance: 6 permintaan berurutan dengan kedua toggle OFF → 6/6 `503`
- Setelah region dipindah: 5/5 query `used=true, grounded=pass`
- `x-vercel-id` = `sin1::sin1::...` (fungsi kini di Singapura)

## Sisa

Ekor latensi penyedia masih bisa menyentuh 40 dtk pada query tertentu. Dengan deterministik OFF tidak ada jaring pengaman, jadi panggilan di atas 48 dtk tetap menjadi error. Bila mengganggu, langkah berikutnya adalah gerbang kualitas penuh (`npm run eval`, 52 item) untuk kandidat model — bukan perbandingan latensi.

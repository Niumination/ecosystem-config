---
name: llm-call-reliability
description: "Use when LLM calls stall, time out, or return bad JSON."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm, timeout, retry, streaming, latency, quota]
    related_skills: [vercel-deploy-check, production-env-vars, optimization]
---

# LLM Call Reliability — Timeouts, Stalls, Retries

Kelas masalah: endpoint yang memanggil model membalas "timeout", mengembalikan
JSON di luar skema, atau gagal intermiten yang tidak bisa direproduksi lokal.

## 1. Ukur token pertama dan total secara terpisah — sebelum menyalahkan model

`first token` dan `total` menjawab dua pertanyaan berbeda. Jalur streaming bisa
memberi keduanya: catat waktu setiap event (status → token → result/error).

- **Mandek (stall):** token pertama TIDAK PERNAH datang — sambungan mati, dan
  menunggu tidak akan menyembuhkannya.
- **Lambat (slow):** token pertama datang awal, ekornya panjang — model memang
  bekerja, dan menunggu adalah tindakan yang benar.
- **Lambat di jalur, bukan di model:** kode dan model yang sama lewat function
  ter-hosting bisa jauh lebih lambat daripada di lokal. Di Vercel periksa lokasi
  eksekusi dulu (`curl -sI <url> | grep -i x-vercel-id` — nilai KEDUA = tempat
  fungsi jalan) sebelum mengganti model apa pun.

Probe siap pakai: `scripts/sse_timing_probe.py <url-stream> "query" ...` — cetak
total, waktu token pertama, jumlah token, dan payload result/error per query.

## 2. Mandek ≠ lambat: beri watchdog token pertama

Pasang watchdog "tidak ada data" (default ~15 dtk) yang membatalkan dengan pesan
berawalan `stall:`, terpisah dari timeout percobaan keseluruhan; reset watchdog
setiap potongan data masuk.

Menghapus semua retry karena "timeout tidak boleh diulang" adalah generalisasi
yang salah: tepat untuk panggilan lambat-tapi-hidup, salah untuk sambungan mandek.
Bedakan lewat bukti token pertama (aturan 1), bukan asumsi.

## 3. Retry HANYA bila belum ada satu pun output keluar

Pada jalur streaming, retry hanya sah bila nol delta sudah dikirim ke pemanggil —
jaga flag `sudahAdaData`/`emitted`. Memulai ulang setelah output keluar
MENGGANDAKAN teks yang sudah tampil di klien.

Pembatalan dari pemanggil (`signal.aborted`) TIDAK PERNAH diulang: konsumennya
sudah pergi.

Bila token sudah terlanjur terkirim lalu parsing gagal, pulihkan dengan percobaan
ulang NON-stream dan kirim hasilnya sebagai event `result` final — klien yang
mereset narasi live saat menerima `result` akan mengganti teks parsial itu.

## 4. Urutan anggaran waktu

`timeout percobaan model` < `timeout route server` < `timeout klien` < `maxDuration` platform.
Buat lapisan klien paling longgar di antara dua lapisan aplikasi supaya pengguna
menerima error asli dari server, bukan timeout karangan klien.

Sertakan NILAI batas di dalam pesan abort (`timeout setelah 48000 ms`). Tanpa itu
"timeout" tidak memberi tahu batas mana yang berlaku saat log dan halaman env
tidak dapat diakses.

## 5. Kegagalan skema diulang sekali, dibatasi waktu terpakai

Keluaran di luar skema biasanya **sampling**, bukan sistematis: query identik yang
gagal sekali berhasil saat diulang. Ulangi SEKALI, berbatas: hanya bila waktu
terpakai masih kecil (< ~15 dtk) dan percobaan kedua memakai timeout lebih pendek,
supaya kasus terburuk tetap di bawah batas platform. Keluaran mentah model TIDAK
PERNAH ditampilkan ke pengguna; catat percobaan ke berapa yang gagal di log server.

Pilih model pada DUA sumbu sekaligus, bukan latensi saja: ukur juga tingkat
validitas skema di pipeline aplikasi. Model cepat yang sesekali meleset skema tetap
pilihan lebih baik begitu ada satu retry — model lambat yang selalu valid justru
yang membuat pengguna melihat timeout, dan itu kegagalan yang jauh lebih terlihat.

## 6. Verifikasi deploy tanpa membakar kuota model

Jangan memverifikasi deploy dengan panggilan model berbayar berulang. Pilih jalur
permintaan yang membalas string TETAP sebelum model dipanggil (evidence/data tidak
ditemukan, fitur dimatikan admin), lalu cocokkan kata kunci yang hanya ada di build
baru. Endpoint status yang melaporkan nama model aktif juga probe nol-panggilan.

**Disiplin kuota (preferensi pemilik):** tanyakan dulu bila model berbayar dan
kuotanya mendekati habis; uji perilaku memakai model termurah yang tersedia; dan
berhenti segera saat pemilik memperingatkan kuota. Probe yang gagal karena kuota
bukanlah data tentang kode.

## 7. Mock uji wajib menghormati AbortSignal

Stub `fetch` yang `ReadableStream`-nya mengabaikan signal tidak akan memicu
watchdog: pembacaan menggantung dan test gagal karena timeout runner, bukan karena
assertion. Sambungkan signal di mock:
`signal?.addEventListener('abort', () => controller.error(signal.reason))`.

## Jebakan

- Menaikkan timeout total saja: mengubah mandek 20 dtk menjadi mandek 48 dtk, tanpa
  menambah satu pun peluang berhasil.
- Menambah retry di dalam loop tanpa syarat — dua kali tunggu untuk jawaban yang
  sudah pasti gagal.
- Menguji model lewat `curl` mentah lalu menyimpulkan performa aplikasi: ukur lewat
  pipeline aplikasi yang sama (prompt, mode JSON, anggaran token).
- Memangkas anggaran token keluaran untuk mempercepat: keluaran terpotong sebelum
  JSON selesai, lalu jatuh ke jalur fallback — tampak seperti kegagalan model.
- Teks error yang dilihat pengguna tanpa test pengunci: kalimat yang dipesan pemilik
  bergeser diam-diam di refactor berikutnya. Kunci string lengkapnya di test.
- Teks error yang mengulang frasa untuk satu sebab yang sama (`X dinonaktifkan admin
  — ... dinonaktifkan admin ...`). Sebut sebabnya sekali; simpan alasan teknis
  spesifik (mis. `panggilan model gagal: timeout setelah 48000 ms`) sebagai awalan.
- Fixture test yang memuat nilai berbentuk kredensial (`apiKey: 'kunci-uji'`):
  lapisan redaksi menulisnya sebagai `***` ke berkas, sintaks rusak, dan error
  tsc/LSP muncul di baris yang Anda yakini benar. Pakai placeholder polos (`'x'`)
  di fixture, lalu jalankan tsc/build untuk memastikan berkasnya utuh — jangan
  mengejar error sintaks yang sebenarnya berasal dari redaksi.

## Verifikasi

```bash
# 1. token pertama vs total, melalui pipeline aplikasi
python3 scripts/sse_timing_probe.py https://<host>/api/query/stream "query uji"
# 2. nol-panggilan: bukti build baru hidup tanpa menyentuh kuota model
curl -s -X POST https://<host>/api/query -H 'Content-Type: application/json' \
  -d '{"query":"zzqq tanpa data"}' | grep -o "<frasa-khas-build-baru>"
# 3. lokasi fungsi (Vercel) sebelum menuduh model lambat
curl -sI https://<host>/api/status | grep -i x-vercel-id
```

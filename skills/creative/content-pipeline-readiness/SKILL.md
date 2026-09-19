---
name: content-pipeline-readiness
description: "Use when checking content production & publish readiness."
version: 1.0.0
tags: [content, audit, ecosystem, readiness, reels, distribution]
platforms: [macos]
---

# Content Pipeline Readiness Audit

Trigger: "periksa kondisi ekosistem untuk kebutuhan konten kreator", "siap belum bikin konten", "tool apa yang bisa dipakai untuk konten", atau permintaan memeriksa kesiapan **sebelum** menjanjikan produksi video/carousel/postingan.

## Prinsip

- **Pisahkan hulu dari hilir.** Hulu = naskah + render + aset. Hilir = distribusi/publikasi. Alat produksi lengkap TIDAK berarti konten bisa tayang; laporkan keduanya terpisah, jangan pernah simpulkan "siap" dari daftar tool saja.
- **Murni pemeriksaan sampai pemilik bilang gas.** Request "periksa/cek" = baca, probe, lapor. Jangan hidupkan service, jangan load launchd, jangan bikin cron, jangan ubah skill.
- **Bedakan "skill ada" dari "kapabilitas siap".** Skill terpasang tapi servernya mati = ⚠️ dengan hasil probe port, bukan ✅.
- **Setiap usulan yang menyentuh service, skill bank, akun pihak ketiga, atau config masuk tabel rekomendasi dengan kolom gate approval.**

## Langkah

### 0. Riwayat thread — apa yang sudah dicoba (jangan ulangi yang sudah ditolak)

Sebelum mengusulkan apa pun, rekonstruksi pekerjaan thread ini dari state Hermes, bukan dari ingatan:

```bash
sqlite3 -header -column ~/.hermes/state.db \
  "SELECT id, model, datetime(started_at,'unixepoch','localtime') AS mulai, message_count, tool_call_count, end_reason \
   FROM sessions WHERE thread_id='1172' ORDER BY started_at DESC LIMIT 5;"

sqlite3 -column ~/.hermes/state.db \
  "SELECT rowid, role, substr(replace(coalesce(content,''),char(10),' '),1,200) \
   FROM messages WHERE session_id='<id>' AND role='user' ORDER BY rowid;"
```

- PK tabel `sessions` adalah `id` (bukan `session_id`); `messages.session_id` merujuk ke situ. Query `WHERE session_id=` pada tabel `sessions` akan gagal — kolomnya `id`.
- Persona + skill binding + override model per thread: `grep -n "'1172'" ~/.hermes/config.yaml` → `channel_overrides` (model), `channel_prompts` (persona), `channel_skill_bindings` (skill terikat).
- `end_reason=session_reset` (mis. akibat ganti model) berarti riwayat thread **tidak** terbawa: sesi baru mulai dari prompt persona + SOUL saja.
- Model yang tertulis di `channel_overrides` = default konfigurasi; model yang **benar-benar** dipakai sesi ada di kolom `model` tabel `sessions`. Untuk profil thread aktif, jalankan audit runtime, jangan simpulkan dari config.
- Baca pesan user terakhir: hasil yang pernah ditolak pemilik (mis. video reels dari HTML polos) tidak boleh diusulkan ulang tanpa perubahan pendekatan yang eksplisit.

### 1. Baseline kesehatan + HEAD
```bash
cd ~/Desktop/Niumination && bash scripts/up-eco.sh    # exit 0 = sehat
```
Catat: HEAD hash, jumlah repo dirty, folder asing, jumlah skill bank, hasil Composio (akun ACTIVE + nama toolkit), 9router model count.

**Pitfall konkurensi:** thread/agent lain bisa commit atau mengubah `docs/registry/` saat audit berjalan (audit panjang bisa menyeberangi commit orang lain). Sebelum melapor, jalankan ulang `git log --oneline -3` dan `git status --short`, lalu kutip commit yang benar-benar sudah Anda verifikasi — jangan mengutip HEAD dari awal run.

### 2. Hulu — tool produksi yang benar-benar terpasang
```bash
for c in ffmpeg manim node npx python3; do printf '%s: ' $c; command -v $c || echo MISSING; done
npx --no-install hyperframes --version
for p in 8188 20128; do printf 'port %s: ' $p; curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://localhost:$p/ || echo DOWN; done
```
Skill yang dicek: `ghost`, `humanizer`, `gemini-vo-narration` (mesin voice-over standar), `baoyu-infographic`, `manim-video`, `impeccable`/`ui-ux-pro-max`, `ekosistem-content-verification`. Tool Hermes: `image_generate`, `text_to_speech`. Server lokal (ComfyUI :8188) diperlakukan sebagai kapabilitas yang harus diprobe — mati = ⚠️, bukan blocker otomatis. Kesiapan voice-over = kunci `GOOGLE_API_KEY` ada **dan** kuota harian model belum habis; kuota dihitung **per model per hari** di tier gratis, jadi baca batasnya dari badan galat 429 (bukan tabel dokumentasi) dan jangan bakar kuota hanya untuk menguji kesiapan.

### 3. Aset produksi — yang paling sering kosong
```bash
grep -rl 'data-composition-id' --include='*.html' ~/Desktop/Niumination 2>/dev/null | grep -v node_modules
ls -lR ~/Movies/'Posting - Instagram' 2>/dev/null | head
```
0 hasil = tidak ada komposisi HyperFrames yang bisa dipakai ulang; setiap video baru dibangun dari nol. Nyatakan ini eksplisit di laporan, karena inilah penyebab output "mentah". Cek juga brand kit (logo, palet, tipografi, gaya caption) — ketiadaannya adalah temuan, bukan detail.

**Satu grep bukan bukti bahwa semua aset produksi kosong.** Sebelum menulis "dibangun dari nol", periksa aset yang sudah dipaketkan di ekosistem:

```bash
ls -l ~/Desktop/Niumination/labs/mata-aihackfest-2026/assets/media/pipeline/
unzip -l ~/Desktop/Niumination/labs/mata-aihackfest-2026/assets/media/pipeline/hermes-video-pipeline.zip \
  | grep -iE 'voice|naskah|tts|render|assemble|subsync|qc|sample'
```

Zip itu adalah SOP produksi video yang sudah terbukti jalan dan bisa dipakai ulang: `VOICE.md` (aturan delivery voice-over: humanize lebih dulu, angka dieja kata, rate/pitch per adegan, batas edge-tts), `naskah_vo.json`/`naskah_short.json` (rate, pitch, voice per adegan), `tts.py` (mode VO rekaman manual vs edge-tts), `render.py`/`assemble.py`/`subsync.py`/`qc.py`, dan `audio/voice-samples/` (set audisi voice). Sebut keberadaannya di laporan; jangan mengklaim kapabilitas produksi nol hanya karena grep komposisi HTML kosong.

**Jangan kutip aturan voice-over paket itu sebagai standar berjalan.** Aturan di `VOICE.md` (angka dieja kata, akronim dieja huruf, rate/pitch per adegan, batas edge-tts) berlaku untuk mesin **edge-tts**; standar ekosistem yang berlaku sekarang memakai mesin LLM TTS dan mengirim naskah **apa adanya** dengan arahan gaya di prompt — engine, preset, dan suara terkunci ada di skill `creative/gemini-vo-narration`. Laporkan paket lama sebagai referensi historis, bukan sebagai SOP yang dipakai.

**Gerbang kualitas video (jangan dilewati):** HTML polos tanpa timeline animasi dan desain matang menghasilkan MP4 yang tidak layak tayang. Template/komposisi wajib punya track animasi per scene (`data-start`/`data-duration` per clip) dan lakukan cek 3 frame kunci (`ffprobe` durasi + ekstrak frame) sebelum render penuh. Sampaikan gerbang ini sebagai syarat, bukan saran.

### 4. Hilir — distribusi/publikasi
Baca daftar toolkit ACTIVE dari output `up-eco.sh` (seksi Composio). Kanal sosial yang relevan: instagram, tiktok, facebook, buffer, ayrshare, postiz. Bila tidak ada satu pun kanal sosial yang ACTIVE → unggah masih manual; tulis itu sebagai blocker hilir utama dan **jangan** menjanjikan posting otomatis.
Rencana yang sudah ada di ekosistem: `docs/registry/composio-integration-plan.md` (toolkit dalam Composio) + `docs/registry/composio-free-tier-tools.md` (katalog free-tier luar). Katalog free-tier menyatakan angkanya belum diverifikasi ulang — verifikasi ke halaman resmi sebelum mengutip nama tool atau kuota sebagai fakta.

#### 4b. Verifikasi klaim free-tier kanal distribusi (saat diminta "verifikasi angkanya")

1. Ambil daftar tool dari `docs/registry/composio-free-tier-tools.md`.
2. Untuk tiap tool, buka **halaman pricing/resmi vendor** lewat `web_extract` — bukan blog, ulasan, atau situs agregator. Bila halaman di-render JS dan blok harga tidak muncul, ambil halaman bantuan/docs resmi produk tersebut (mis. `support.<vendor>.com`, `docs.<vendor>.com`).
3. Catat per tool: (a) kuota angka, (b) **jendela waktu** (berapa hari ke depan / interval minimum), (c) **kapabilitas yang dikecualikan** di tier gratis (mis. publikasi video), (d) apakah tier gratis berlaku untuk **self-hosted** atau **cloud**.
4. Tulis ulang baris katalog dengan kolom **Sumber (URL)** dan cantumkan tanggal verifikasi di header; klaim yang tidak ditemukan di halaman resmi **dihapus**, bukan dipertahankan dengan tanda tanya.
5. Tambahkan tabel **"Koreksi angka lama"** (klaim lama → fakta terverifikasi) supaya perubahan fakta terlihat oleh pemilik.
6. Selaraskan dokumen konsumen: `grep -nE 'Tool1|Tool2|...' docs/registry/composio-integration-plan.md` lalu perbaiki setiap baris yang bertentangan (langkah kerja, kalender mingguan, catatan penting). Dua dokumen yang saling bertentangan lebih buruk daripada satu angka lama.
7. Commit docs-only (selective `git add`), push, verifikasi `git ls-remote origin -h refs/heads/main` cocok dengan hash commit.

Snapshot fakta terverifikasi + daftar jebakannya: `references/free-tier-channel-facts.md`.

### 5. Otomasi
```bash
python3 - <<'EOF'
import json, os
d = json.load(open(os.path.expanduser('~/.hermes/cron/jobs.json')))
jobs = d if isinstance(d, list) else d.get('jobs', d)
if isinstance(jobs, dict): jobs = list(jobs.values())
for j in jobs: print(j.get('name'), '|', j.get('schedule'), '| enabled:', j.get('enabled'))
EOF
```
Tidak ada job konten = tidak ada pipeline otomatis. Jangan usulkan cron konten sebelum kanal distribusinya ada.

### 6. Sumber bahan konten
```bash
grep -E '\| ✅ 200 \|' ~/Desktop/Niumination/docs/registry/deployment-status.md | head -25
```
Baris ✅ 200 = aplikasi live yang bisa jadi bahan nyata (portal Pemdi 52 OPD, KMS SPBE, Kune-Ya, VirtualAssistance). Sertakan 3–5 sumber konkret; "sumber dari repo" tanpa nama aplikasi tidak berguna untuk pemilik.

### 7. Tulis laporan
Satu berkas di `docs/reports/` (mis. `KONTEN-KREATOR-STATUS-<tgl>.md`). Dilarang membuat folder baru di `docs/`, dilarang menulis ke `docs/reference/`. Struktur yang diharapkan pemilik:

1. Header: pelaksana, pemicu, lingkup, metode (sebutkan rentang waktu pemeriksaan)
2. Ringkasan eksekutif: **tabel** status per aspek (kesehatan, produksi, distribusi, otomasi, sumber) + 1 kalimat verdict
3. Temuan per aspek dengan angka hasil probe
4. Blocker & drift, berurut dampak
5. Rekomendasi berprioritas **dengan kolom "Gate"** (butuh approval atau tidak)
6. `## Bukti` — tabel perintah ↔ hasil, termasuk exit code, hash commit, hasil push

Simpan dengan `git add <berkas>` selektif (jangan `git add .`), commit, push, lalu verifikasi `git ls-remote origin -h refs/heads/main` cocok dengan hash commit. Jangan klaim "tersimpan di ekosistem" tanpa bukti push.

## Pitfall

- **Satu pola grep bukan bukti ketiadaan kapabilitas.** "Tidak ada file X" hanya membuktikan absennya satu format, bukan absennya alat: pipeline produksi bisa tersimpan sebagai zip paket, dan skill bisa ada tanpa dependensinya terpasang. Sebelum menulis blocker "tidak punya apa-apa", periksa paket/arsip dan probe dependensinya, lalu bedakan "tidak ada" dari "ada tapi belum dipakai".
- **Daftar model di katalog provider bukan bukti model itu bisa dipakai.** `/v1/models` bisa menjawab 200 dengan puluhan entri sementara belum tentu ada satu pun yang teralokasi ke kunci ini: sebagian membalas `500` dengan pesan "kanal untuk model ini tidak ada", sebagian menggantung sampai batas waktu, sebagian `522`. Sebelum merencanakan pekerjaan apa pun di atas sebuah provider, kirim satu permintaan asli yang minimal untuk **setiap** model yang akan dipakai, lalu nilai **per endpoint** — satu provider bisa melayani TTS sementara ASR dan gambar-nya gagal. Di laporan, tulis berapa yang benar-benar bisa dipakai dari berapa yang terdaftar, dan jangan menyarankan provider itu sebagai partner sebelum angkanya ada.
- **Saat pemilik menyebut hasil lama lebih bagus, temukan artefaknya dan baca dokumentasi internalnya lebih dulu.** Paket lama sering memuat spesifikasi eksplisit (aturan delivery, tabel parameter, contoh before/after) yang menjelaskan penyebab perbedaan; menyimpulkan dari ingatan atau menebak pendekatan baru membuang pekerjaan yang sudah tervalidasi.
- **Verifikasi klaim port/hapus-layanan ke plist + berkas route, bukan ke teks skill atau ingatan.** `launchctl list | grep -i niu` menunjukkan label yang benar-benar termuat, `cat ~/Library/LaunchAgents/*missioncontrol*.plist` menunjukkan port produksi yang benar-benar dipakai, `ls services/niu-mission-control/apex-ui/app/api/mc/` menunjukkan endpoint yang benar-benar ada. Dokumen yang menyatakan sebuah port "dihapus" bisa basi sementara plist produksi memakainya — jangan melaporkan outage dari teks dokumen.
- **Endpoint dispatch/idle bukan insiden ekosistem.** Layanan yang mati dilaporkan sebagai blocker hanya bila menghambat pekerjaan (mis. delegasi lintas-thread); sebutkan dampaknya, bukan sebagai kegagalan ekosistem.
- **Jangan menambal skill bank saat audit.** Skill konten (mis. `free-tier-reels`, `up-eco`) berada di bank milik pemilik; perubahan (gerbang kualitas, koreksi fakta) diusulkan di tabel rekomendasi — bukan dieksekusi sendiri.
- **Jangan menyalin angka registry sebagai fakta.** Registry bisa memuat catatan "belum diverifikasi ulang"; bawa catatan itu ke laporan.
- **Laporan tidak memuat kredensial.** ID koneksi Composio, token, dan nama akun pihak ketiga diringkas; cukup jumlah dan jenis toolkit.
- **Klaim "gratis" tanpa baris sumber adalah asumsi.** Setiap angka free-tier di dokumen harus punya URL halaman resmi; kalau belum dicek, tulis eksplisit "belum diverifikasi" dan jangan dipakai sebagai dasar janji ke pemilik/klien.
- **Cek matriks kapabilitas, bukan nama paket.** Tier gratis sering mengecualikan kapabilitas inti (mis. penjadwalan boleh, publikasi video tidak) — paket "free forever" bisa tetap tidak bisa dipakai untuk reels.
- **Self-hosted ≠ cloud.** Produk yang repo-nya gratis (AGPL) bisa punya layanan cloud **tanpa** free plan sama sekali; sebutkan jalur mana yang gratis, jangan tulis namanya saja.
- **"Unlimited" menyembunyikan jendela atau kuota.** Cari batas jendela penjadwalan (mis. 20 menit–29 hari) dan bandingkan dengan horizon kalender konten (30 hari) — selisihnya adalah temuan, bukan detail.
- **Trial ≠ free.** Kalau halaman resmi tidak punya kolom $0 untuk produk itu, produknya berbayar; keluarkan dari daftar gratis dan catat sebagai koreksi.
- **Jangan hapus tool dari katalog tanpa jejak.** Sediakan tabel koreksi agar pemilik melihat apa yang berubah; pemilik memakai katalog ini untuk keputusan belanja/biaya.

## Referensi

- `references/pipeline-probes.md` — blok perintah probe siap-tempel per lapisan (kesehatan, hulu, aset, hilir, otomasi, sumber) beserta cara membaca keluarannya.
- `references/free-tier-channel-facts.md` — snapshot terverifikasi free-tier kanal produksi/distribusi (angka + batas + URL sumber) dan jebakan yang membuat angka lama salah; wajib diverifikasi ulang sebelum dikutip sebagai fakta.
- Skill terkait: `short-form-video-production` (alur produksi + lapis delivery voice-over: `references/voiceover-delivery.md`), `free-tier-reels` (cara produksi), `ekosistem-content-verification` (verifikasi akurasi isi), `up-eco` (baseline status ekosistem), `skill-bank-management` (promosi skill baru ini ke bank).

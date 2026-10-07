# Riset: Flow Connector — Connect Coding Agent ke Google Flow

**Tanggal:** 7 Okt 2026
**Thread:** 802 (Research)
**Sumber:** Chrome Web Store listing + repo GitHub + npm registry + situs vendor
**Status:** STUDI — belum ada keputusan adopsi

---

## 1. Identitas

| Item | Nilai |
|------|-------|
| Nama | Flow Connector — connect your coding agent to Google Flow image & video |
| Extension ID | `feldfgfggmlcnoihdjbcemjknoegocnm` (32 char) |
| Kategori | Workflow & Planning |
| Versi | 1.2.4 |
| Update terakhir | 5 Okt 2026 |
| Ukuran | 123 KiB |
| Pengguna | 25 |
| Rating | 0 (belum ada ulasan) |
| Developer | Srijan Builds (`srijan-kaiwart`), Madhya Pradesh, India — one-person project, status "Non-trader" |
| Kontak | srijanbuildsconnect@gmail.com |
| Repo | `github.com/srijan-kaiwart/flow-connector` — 1 star, dibuat 25 Agu 2026, tanpa file LICENSE |
| npm | `flow-connector-cli` 1.0.9 — MIT, 10 versi, deps: `ws`, `zod`, `commander`, `@modelcontextprotocol/sdk` |
| Situs | `flow-connector.flowconnector.workers.dev` (Cloudflare Workers) |

### Catatan ID

URL yang diberikan memuat ID **30 karakter** (`feldfgfggmlcnoihdjbcemjknoegoc`) — ID ekstensi Chrome selalu 32 karakter (alfabet a–p). Verifikasi:

```
canonical URL untuk ID 30 char  → https://chromewebstore.google.com/   (tidak valid)
canonical URL untuk ID 32 char  → .../detail/flow-connector-—-connect/feldfgfggmlcnoihdjbcemjknoegocnm  (valid)
```

ID asli berakhiran `nm`. Tautan yang benar:

```
https://chromewebstore.google.com/detail/feldfgfggmlcnoihdjbcemjknoegocnm
```

---

## 2. Apa yang dikerjakan

Menghubungkan **coding agent** (Claude Code, Cursor, Codex, Gemini CLI, Windsurf, atau klien MCP apa pun) ke **Google Flow** (`flow.google.com`) sehingga agent bisa meminta pembuatan gambar/video — bulk, antrean prompt, unduh otomatis.

Bukan API. Ini **otomasi UI**: ekstensi mengetik prompt ke antarmuka Flow yang asli, memakai sesi Google yang sudah login, lalu menyimpan hasil ke folder Downloads.

### Arsitektur

```
Agent (Claude Code / MCP client)
   ↓  flow-auto CLI
Bridge daemon lokal (ws)
   ↓
Chrome extension (side panel)
   ↓  real clicks/typing via debugger permission
flow.google.com (sesi Google pengguna)
   ↓
Hasil → folder Downloads
```

Komponen:
1. **Ekstensi Chrome** — side panel, sign-in, salin setup prompt
2. **`flow-auto` CLI** — `npm install -g flow-connector-cli` (butuh Node 20+)
3. **Bridge daemon lokal** — auto-start saat pemakaian pertama
4. **Integrasi agent** — skill native Claude Code (`~/.claude/skills/`) atau MCP stdio server (`flow-auto-mcp`) untuk klien lain

---

## 3. Mode & model yang didukung

Mode: text-to-image, image-to-image, text-to-video, first & last frame, ingredients-to-video, video-to-video, create character, set voice, extend video, merge clips.

Model (tergantung ketersediaan di akun Google masing-masing): **Nano Banana Pro / 2 / Lite** (gambar), **Omni Flash**, **Veo 3.1 Lite / Fast / Quality** (video).

Fitur tambahan yang menonjol: **"Remove the Gemini mark"** — menghapus tanda sparkle Gemini dari hasil generasi sendiri. Ini yang di listing disebut "clean / remove watermark".

---

## 4. Harga

| | Free | Pro |
|---|---|---|
| Biaya | $0 | **$1/bulan** (₹99) — sekali bayar per periode, tidak auto-renew |
| Kuota | 30 video + 40 gambar **per hari** | Unlimited |
| Batch | 1 prompt sekaligus | `--batch 4` (4× lebih cepat) |
| Panel | Harus terbuka selama proses | Bisa ditutup, run tetap jalan |

Pembayaran via UPI atau kartu (India); di luar India harus menghubungi developer.

**Penting:** biaya generasi **tidak** ditanggung ekstensi ini. Semua generasi memakai kredit/limit **akun Google Flow pengguna sendiri**. Ekstensi hanya otomasi — tidak menambah, menjual ulang, atau memperpanjang kredit Google.

---

## 5. Batasan operasional

1. **Tab Flow wajib terbuka dan terlihat di layar.** Chrome memperlambat tab yang diminimalkan/tertutup; proses akan macet atau gagal senyap. Berlaku di Free maupun Pro. Ekstensi menyediakan tombol penataan jendela (browser kiri, editor kanan).
2. **Tidak bisa headless / background tab.** Konsekuensi langsung: tidak bisa dijalankan unattended via cron/gateway.
3. **Butuh izin `debugger`.** Chrome menampilkan banner "extension started debugging this browser". Alasan teknis: tombol generate Flow mengabaikan klik sintetis, jadi satu input event asli diperlukan. Ekstensi attach ke tab Flow untuk satu klik itu lalu langsung detach.
4. **Node.js 20+** untuk CLI.
5. Setiap generasi ~47 dtk/gambar di batch 1, ~14,5 dtk di batch 4.

---

## 6. Privasi

Klaim vendor (dari privacy policy, last updated 3 Sep 2026):

- Tidak ada akun, analytics, telemetri, iklan, atau kode pihak ketiga di dalam ekstensi
- Prompt, hasil generasi, dan file disimpan **lokal** di `chrome.storage` + folder Downloads
- Tidak menyimpan/mengirim username, password, cookie, atau token Google
- Debug log lokal merekam langkah otomasi (selector, error) — **bukan prompt**

Yang keluar dari mesin:
1. **Google Flow** — sama seperti pemakaian manual
2. **Licence check** — hanya jika sign-in plan berbayar; mengirim email + installation id acak. Pengguna Free tidak mengirim apa pun
3. **File konfigurasi** — dari server mereka, untuk memperbaiki otomasi saat UI Flow berubah tanpa menunggu update store

Data yang dideklarasikan ke Chrome Web Store: **Personally identifiable information** — tidak dijual ke pihak ketiga, tidak dipakai untuk tujuan di luar fungsi inti.

---

## 7. Risiko

### 7.1 Risiko akun Google (tertinggi)

Terms of Service vendor sendiri menyatakannya eksplisit:

> "Automating a website may be contrary to that website's terms of service. Google may, at any time and without notice: change or remove features this extension depends on, breaking it; **rate-limit, restrict, suspend or close your account**; withdraw or change the free credits you rely on. By using Flow Connector you accept that risk yourself. We do not promise that using it is permitted by Google, and we are not liable for anything Google does to your account, your credits, or your generated files."

Redaksi ini jujur dan jelas: risiko ditanggung pengguna sepenuhnya. Ini otomasi UI terhadap layanan Google dengan akun pribadi — kelas risiko yang sama dengan tool otomasi web lain, bukan celah keamanan, tapi pelanggaran ToS potensial.

Mitigasi yang mereka klaim: ekstensi memperlambat aksi dan back-off saat Flow memberi sinyal aktivitas tidak wajar. Mereka sendiri menulis: "That reduces the risk. It does not remove it."

### 7.2 Kematangan proyek

- 25 pengguna, **0 rating** — belum teruji publik
- Repo 1 star, tanpa file LICENSE (npm menulis MIT, repo tidak)
- Dibuat 25 Agu 2026 — umur ~6 minggu
- Developer satu orang, dukungan best-effort
- Terikat pada UI Flow yang berubah sering — otomasi rapuh by design (mereka mengakui ini dan mengompensasi via config file jarak jauh)

### 7.3 Rantai pasok

- CLI npm `flow-connector-cli` — 4 dependensi (`ws`, `zod`, `commander`, `@modelcontextprotocol/sdk`), permukaan serangan kecil
- Binary ekstensi tidak tersedia di repo — hanya rilis via Web Store
- Server Cloudflare Workers dapat mengirim file konfigurasi yang memengaruhi perilaku otomasi → permukaan update jarak jauh yang tidak diaudit

### 7.4 Risiko hukum konten

Menghapus tanda Gemini (watermark) dari hasil generasi. Untuk konten yang dipublikasikan, ini berpotensi bersinggungan dengan ketentuan penggunaan Google dan dengan kewajiban disclosure konten AI. Perlu ditinjau terpisah lewat `content-legal` sebelum dipakai untuk output publik.

---

## 8. Relevansi ke ekosistem

### Yang cocok

- **Thread 1172 (Konten Kreator)** — produksi aset visual untuk konten
- **Thread 12707 (Edu Content)** — ilustrasi/diagram untuk web book, video pendek penjelas
- **Pola integrasi** — MCP stdio server adalah jalur yang sudah dikenal ekosistem; bisa didaftarkan sebagai MCP di Hermes

### Yang tidak cocok

- **Tidak bisa unattended.** Syarat tab terlihat mematikan pemakaian via cron/gateway/headless. Semua pemakaian harus manual di desktop dengan browser di depan.
- **Bukan pengganti image_gen.** Ekosistem sudah punya `image_generate` dan `comfyui` — keduanya tanpa risiko ToS pihak ketiga dan tanpa syarat tab terlihat.
- **Ketergantungan pada akun Google pribadi** dengan konsekuensi suspend yang dinyatakan vendor sendiri.

### Catatan model

Nilai jual utamanya adalah akses **Nano Banana Pro** dan **Veo 3.1 Quality** tanpa biaya API per-generasi — memakai kredit Google Flow yang sudah dimiliki. Kalau kredit Flow sudah ada dan menganggur, ini memanfaatkannya. Kalau tidak, ini bukan jalur gratis.

---

## 9. Kesimpulan

Tool ini berfungsi dan didokumentasikan rapi (SKILL.md 48 KB, doctor command, panduan troubleshooting). Kualitas engineering-nya di atas rata-rata untuk proyek 6 minggu dengan 1 developer.

Tapi tiga hal menahannya dari adopsi langsung:

1. **Risiko akun Google dinyatakan vendor sendiri**, dan ditanggung pengguna. Akun Google adalah identitas sentral pemilik — kerugiannya tidak proporsional dengan penghematan $1/bulan.
2. **Tidak bisa otonom.** Syarat tab terlihat = interaksi manusia setiap kali. Ini membatalkan sebagian besar nilai "agent bisa generate sendiri" yang jadi pitch utamanya di ekosistem yang berjalan via Telegram/gateway.
3. **Belum teruji.** 25 pengguna, 0 rating, 6 minggu. Belum ada bukti ketahanan terhadap perubahan UI Flow.

**Rekomendasi: TIDAK diadopsi sekarang.** Simpan sebagai referensi. Tinjau ulang jika pengguna naik signifikan dan rating muncul, atau jika kredit Google Flow sudah tersedia dan menganggur — pada kondisi itu risikonya jadi lebih terukur karena tidak ada biaya tambahan.

Kalau tetap ingin dicoba: pakai **akun Google terpisah** (bukan akun utama), Free plan, tanpa sign-in berbayar. Nol biaya, dan risiko suspend terisolasi dari identitas utama.

---

## Bukti

```
# Ekstraksi listing (canonical = ground truth validitas ID)
curl -sL "https://chromewebstore.google.com/detail/feldfgfggmlcnoihdjbcemjknoegocnm?hl=en&gl=US"
  → canonical: .../detail/flow-connector-—-connect/feldfgfggmlcnoihdjbcemjknoegocnm
  → title: Flow Connector — connect your coding agent to Google Flow image & video
  → Version 1.2.4 | Updated October 5, 2026 | Size 123KiB | 25 users

# ID dari URL pengguna (30 char) — TIDAK VALID
curl -sL "https://chromewebstore.google.com/detail/feldfgfggmlcnoihdjbcemjknoegoc"
  → canonical: https://chromewebstore.google.com/   (fallback ke homepage = tidak ditemukan)

# Kontrol (ID valid sebagai pembanding)
curl -sL "https://chromewebstore.google.com/detail/eimadpbcbfnmbkopoojfekhnkhdbieeh"
  → canonical: .../detail/dark-reader/eimadpbcbfnmbkopoojfekhnkhdbieeh   VALID

# Repo
curl -s https://api.github.com/repos/srijan-kaiwart/flow-connector
  → created 2026-08-25 | pushed 2026-09-05 | stars 1 | license: None

# npm
curl -s https://registry.npmjs.org/flow-connector-cli
  → latest 1.0.9 | license MIT | 10 versions | maintainer srijan-kaiwart

# Privacy & Terms
curl -s https://flow-connector.flowconnector.workers.dev/privacy   → 19147b
curl -s https://flow-connector.flowconnector.workers.dev/terms     → 18284b
```

**Catatan alat:** `web_search` dan `web_extract` gagal sepanjang sesi ini dengan HTTP 402 `insufficient_funds` dari Firecrawl via Nous Portal. `browser_navigate` gagal dengan `Invalid URL '/tabs'`. Camofox menolak dengan `Unknown property navigator.product in config`. Semua data di laporan ini diambil via `curl` langsung + parsing HTML, dan Chrome Web Store search internal (`/search/<query>`) yang berfungsi tanpa auth.

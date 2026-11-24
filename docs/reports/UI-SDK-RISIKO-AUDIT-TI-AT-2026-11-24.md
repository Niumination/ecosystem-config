# UI SDK di AuditTI-AT — dampak, risiko, keputusan tahan

**Tanggal:** 24 Nov 2026 · **Keputusan:** **TAHAN** — tidak ada perubahan kode di `sites/audit-ti-at` · **Analisis:** redteam + premortem

## Konteks

Sandbox UI SDK sudah terverifikasi (lihat `docs/reports/UI-SDK-SANDBOX-2026-11-24.md`). Kandidat produksi awal adalah `sites/audit-ti-at`. Sebelum pemasangan, source app-nya dibaca dan risikonya dinilai. Hasilnya: pemasangan **ditahan**.

`audit-ti-at` adalah repo terpisah (`github.com/Niumination/AuditTI-AT`), tidak di-track oleh repo induk `ecosystem-config`.

## Fakta dari source (terverifikasi)

- React `^19.2.5`, Vite `^8.0.10`, TypeScript types ada, hosting **GitHub Pages**.
- Workflow `.github/workflows/deploy.yml`: push ke `main` → build + deploy otomatis. **Tidak ada staging.**
- Semua kontrol adalah HTML biasa: `<div onClick>` untuk nav (baris 231–235), `<button className="btn">`, `<input className="input-field">`, `<select>`, `<textarea>` (baris 464–502).
- Label form tidak terhubung secara programatik ke input — tidak ada `htmlFor`/`id`, hanya `<label>` visual.
- `handleAudit` membaca `import.meta.env.VITE_OPENROUTER_KEY` (baris 95) dan POST ke `https://openrouter.ai/api/v1/chat/completions` (baris 117). Komentar di baris 98–99 mengakui production seharusnya memakai proxy server.
- `handleAuditAll` (baris 157–166) meng-loop semua paket pending dan memanggil `handleAudit` untuk tiap item.
- Data adalah simulasi, disimpan di `useState`, tanpa backend, login, atau persistensi.
- `package.json` hanya punya script `dev`, `build`, `lint`, `preview` — **tanpa test**.

## Dampak

### Positif

- Approval gate bisa diturunkan ke lapisan UI. Sandbox membuktikan `data-agent-confirm` menolak agent dan tidak bisa dilewati klik biasa.
- Kalau label diperbaiki dengan `aria-label`, aksesibilitas form naik — sekarang label hanya visual.
- Pola bisa dipakai ulang di app lain kalau terbukti berguna.

### Biaya nyata

- **Bukan drop-in.** Bridge hanya melihat komponen UI SDK; HTML biasa tidak masuk snapshot (di sandbox hanya 2 komponen UI SDK yang muncul). Tujuh kontrol di form "Tambah Paket" harus ditulis ulang: 3 input, 2 select, 1 textarea, 1 tombol submit.
- **Styling.** Komponen UI SDK tidak berstyle; app memakai class `.input-field`/`.btn` dan inline style plus font Google. Perpindahan kontrol berisiko merusak tampilan.
- **Bundle.** Sandbox menghasilkan ~296 KB JS untuk React 19 + UI SDK. Delta untuk app ini **belum diukur**.
- **Dua paradigma UI dalam satu file** (535 baris): HTML biasa dan UI SDK. Beban perawatan naik.
- **Vite 8 belum terverifikasi** — sandbox memakai Vite 6.

## Risiko, diurutkan

### 1. Agent memicu biaya API — dampak tinggi, kemungkinan sedang

Tombol "Audit" dan "Audit AI Semua" memanggil OpenRouter; `handleAuditAll` melakukan N panggilan sekaligus. Kalau keduanya masuk snapshot, agent bisa `act` keduanya.

- **Bukti yang akan mengonfirmasi:** tombol audit muncul sebagai entri pada `agent.snapshot()`.
- **Mitigasi:** jangan ekspos tombol audit ke bridge. `allow` hanya mengizinkan kontrol form "Tambah Paket".

### 2. Kunci OpenRouter sudah ikut ke browser — dampak tinggi, kemungkinan tinggi

`VITE_OPENROUTER_KEY` dibaca via `import.meta.env`, jadi masuk bundle klien. Ini **masalah yang sudah ada**; bridge menambah jalur programatik untuk memakainya.

- **Bukti:** baris 95 dan 117; komentar baris 98–99.
- **Mitigasi:** pindahkan ke proxy server dulu — perubahan terpisah, jangan digabung dengan pemasangan bridge.

### 3. Tidak ada autentikasi agent — dampak sedang-tinggi, kemungkinan tinggi

Situs publik tanpa login. Kalau `agentTools` didaftarkan secara global, agent milik pengunjung mana pun bisa memanggilnya, bukan hanya Hermes kita.

- **Mitigasi:** `createAgent()` hanya dibuat saat panel asisten dibuka secara eksplisit. Ini **bukan pengamanan** — kalau data asli dipakai, ini menjadi blocker.

### 4. Auto-deploy tanpa staging — dampak sedang, kemungkinan sedang

Push ke `main` langsung live di GitHub Pages. Tidak ada ruang coba.

- **Mitigasi:** branch terpisah + verifikasi lokal penuh sebelum merge.

### 5. API beta — dampak sedang, kemungkinan sedang

`0.1.0-beta.16`; beta.1 ke beta.16 dalam sekitar enam hari.

- **Mitigasi:** pin versi eksak dan commit lockfile, jangan pakai `^`.

### 6. Regressi visual — dampak rendah-sedang, kemungkinan tinggi

UI SDK tidak berstyle; styling app ini inline.

- **Mitigasi:** perbandingan visual sebelum/sesudah.

### 7. Tanpa test — dampak sedang, kemungkinan sedang

Mengubah form utama tanpa jaring pengaman.

- **Mitigasi:** tinggalkan satu check seperti `?check=1` di sandbox plus assertions.

## Premortem

Enam bulan kemudian pemasangan dinyatakan gagal. Penyebab paling mungkin, urut:

1. **Fitur tidak dipakai** — tidak ada yang perlu mengoperasikan form itu lewat agent. Ini risiko terbesar dan paling murah dicegah.
2. **Kunci OpenRouter bocor** lewat jalur tool yang baru.
3. **Upgrade beta memecah form** tanpa terdeteksi karena tidak ada test.

Tanda awal yang harus dipantau: snapshot menampilkan komponen tanpa label; tombol audit muncul di snapshot; bundle membengkak; deploy gagal di CI.

## Rekomendasi revisi

Kandidat `audit-ti-at` tetap masuk akal secara konsep, tapi **jangan menyentuh form produksi** pada tahap ini.

Jalur lebih aman: halaman prototipe terpisah (misalnya `/agent-demo`) yang tidak ditautkan di navigasi, form serupa, **tanpa kunci OpenRouter**, dan tool tidak diekspos global.

Kalau mau dipakai di form asli, urutannya wajib:

1. Pindahkan kunci OpenRouter ke proxy server.
2. Tambahkan minimal satu test/regresi.
3. Pasang bridge.

Tiga perubahan terpisah, sesuai aturan satu-perubahan-per-sesi.

## Keputusan

**TAHAN.** Tidak ada dependensi, tool, atau kode baru yang dipasang ke `sites/audit-ti-at` pada 24 Nov 2026. Dokumentasi ini saja yang diperbarui di ekosistem.

Syarat untuk melanjutkan: perintah eksplisit ("gas") plus pilihan jalur — prototipe terpisah atau form asli dengan urutan di atas.

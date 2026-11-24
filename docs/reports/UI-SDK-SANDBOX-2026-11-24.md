# UI SDK — hasil sandbox & kandidat produksi

**Tanggal:** 24 Nov 2026 · **Sandbox:** `sandbox/ui-sdk/` (di-`.gitignore`, tanpa repo baru) · **Status:** guardrail terverifikasi, produksi **belum** disentuh

## Yang dibangun

`sandbox/ui-sdk/` — Vite 6 + React 19 + TypeScript, dependensi `@ui-sdk/core` dan `@ui-sdk/react` versi **0.1.0-beta.16**.

Isi minimal:
- `src/App.tsx` — `Input` berlabel "Project name" (awal `Apollo`) dan `Button` dengan `data-agent-confirm="Deletes the project for real"`
- `src/agent.ts` — `createAgent()` **tanpa callback `allow`**, supaya guardrail bawaan yang diuji, bukan filter buatan sendiri; bridge diekspos ke `window.__agent` untuk keperluan uji
- `src/check.ts` — jalan hanya kalau URL memuat `?check=1`, menulis hasil ke `<pre id="result">`
- `verify.sh` — satu check runnable: build → `vite preview` → Chrome headless → assertions

## Bukti verifikasi

Perintah:
```bash
cd sandbox/ui-sdk
./verify.sh
```

Exit **0**. Output:
```
[ok] snapshot 2 komponen + field confirm
[ok] act setValue -> ok:true, input = Atlas
[ok] data-agent-confirm -> ok:false, Needs a person: "Deletes the project for real". Ask them to press "Delete project" themselves.
```

Snapshot lengkap yang diamati:
```json
[
  { "ref": "c1", "component": "input", "actions": ["setValue", "clear"],
    "label": "Project name", "value": "Apollo" },
  { "ref": "c2", "component": "button", "actions": ["press"],
    "label": "Delete project", "confirm": "Deletes the project for real" }
]
```

Artinya:
1. Bridge **benar-benar melihat** komponen UI SDK di halaman (bukan screenshot, bukan accessibility tree).
2. `act` mengubah state lewat API komponen — `values` mencatat `c1 Project name: "Atlas"`.
3. `data-agent-confirm` **ditegakkan di lapisan bridge**. Tanpa callback `allow`, agent ditolak dan disuruh meminta manusia menekan tombolnya. Otomasi klik biasa tidak punya perlindungan ini.

Ini memvalidasi alasan utama riset sebelumnya: garis pertahanan yang selama ini hanya ada di prompt bisa diturunkan ke UI.

## Pitfall saat membangun (sudah diperbaiki)

- `verify.sh` awalnya `cd "$(dirname "$0")/.."` → naik ke `sandbox/`, `npm run build` gagal. Fixed ke `cd "$(dirname "$0")"`.
- `package.json` tidak punya script `preview` → Chrome menerima halaman kosong dan assertion gagal. Script ditambahkan plus guard `curl -sf` sebelum menjalankan Chrome.
- `setTimeout(100)` di `check.ts` tidak selesai di bawah `--virtual-time-budget` Chrome. Delay dihapus; `<pre id="result">` dibuat lebih awal dengan teks `running`.

## Batasan sandbox

- Beta. API berubah cepat (beta.1 ke beta.16 dalam ~6 hari).
- Bridge hanya melihat komponen UI SDK; HTML biasa tidak masuk snapshot.
- `agentTools` tersedia di modul, tapi **belum** didaftarkan ke runtime agent Hermes. Sandbox ini membuktikan bridge bekerja, bukan integrasi akhir.

## Kandidat produksi

| App | React | Cocok? | Alasan |
|---|---|---|---|
| `sites/audit-ti-at` | 19.2.5 | **Paling cocok** | Dashboard internal pengadaan IT; ada form "Tambah Paket" dan aksi audit. Agent yang mengisi/mengubah butuh konfirmasi. Struktur kecil (`src/App.jsx`), Vite 8. |
| `sites/kelas` | 19.3.0 | Bisa | Next 16.4.0. Tapi situs publik dengan kebutuhan operasi-agent rendah. |
| `sites/niu-oss-dashboard` | ~19.2.8 | Tidak disarankan | React sengaja di-pin karena peer fiber `<19.3`; CI a11y ketat (13/13); sudah punya API publik v1 untuk akses agent — bridge tidak perlu. |
| `services/sapa-ai` | 19.2.4 | Tidak sekarang | Prioritas P1/P8, aktif dikembangkan. Jangan dimasuki dependensi beta. |
| `sites/tedeo-kanban` | 18.3.1 | Tidak | UI SDK butuh React 19+. Perlu upgrade dulu. |
| MIRAI / MATA / niu-mission-control | — | Tidak | Python stdlib + HTML satu file / Python. Bukan React, tidak ada permukaan bridge. |

## Rekomendasi

**Target pertama: `sites/audit-ti-at`, dan hanya satu permukaan** — form "Tambah Paket". Pasang core + adapter, buat `createAgent()`, tandai tombol submit dengan `data-agent-confirm`, dan daftarkan `agentTools` ke runtime agent **hanya saat panel asisten dibuka** (jangan terekspos ke pengunjung biasa).

Kenapa ini yang pertama: data pengadaan pemerintah, dan aturan ekosistem sudah mewajibkan approval gate sebelum aksi berisiko. `data-agent-confirm` menegakkan itu di UI — bukan lagi sekadar harapan bahwa agent patuh instruksi.

**Tidak ada perubahan produksi yang dilakukan.** Pemasangan ke `audit-ti-at` menunggu perintah eksplisit ("gas") dan satu sesi tersendiri, sesuai aturan satu-perubahan-per-sesi.

# RISET — Shadcn/Vercel UI SDK (agent-first UI)

**Tanggal:** 24 Nov 2026 · **Status:** riset, **belum diadopsi** · **Verdict:** pantau, jangan jadi pengadopsi pertama

## Sumber

- Video: *"Shadcn Just Rebuilt UI for AI Agents (UI SDK)"* — kanal **Better Stack**
- URL: `https://www.youtube.com/watch?v=ubK6Q53jKg8`
- Durasi 541 dtk (~9 mnt) · unggah 23 Nov 2026 · 52.112 tayangan saat diperiksa
- Transkrip penuh diambil via `youtube_transcript_api` (10.389 karakter). ASR-nya banyak salah nama: `Shadien`=shadcn, `Versel`=Vercel, `RAID`=Radix, `Spelvel`/`Spelt`=Svelte, `claw code`=Claude Code, `Sonet`=Sonnet.

## Verifikasi mandiri (bukan klaim video)

| Fakta | Bukti |
|---|---|
| Paket ada di npm | `npm view @ui-sdk/core version` → **0.1.0-beta.16** |
| Repo | `vercel-labs/ui` (GitHub) |
| Lisensi | **Apache 2.0** |
| Docs | `ui-sdk.dev` |
| Status | **beta** — API, dokumentasi, perilaku bisa berubah |
| Rilis awal | 12 Nov 2026 (Vercel + shadcn) |

**Nuansa penting:** ini rilisan **Vercel Labs**, bukan `shadcn/ui`. shadcn mempromosikannya di X. **`shadcn/ui` belum menyatakan** akan dibangun ulang di atas UI SDK — dan itu penentu adopsi massal.

Catatan versi: berita 18 Nov menyebut `0.1.0-beta.1`; per 24 Nov sudah **beta.16** → iterasi sangat cepat, tanda API belum stabil.

## Tesis

Selama ini agent memakai aplikasi dengan membaca seluruh halaman lalu mengklik satu elemen demi satu, dan menerima snapshot baru setiap kali. UI SDK membalik arah: agent **memanggil API komponen** secara langsung — tanpa screenshot, tanpa accessibility tree.

## Dua paruh

### 1. Agent sebagai pembangun

Sebuah `Select` sebenarnya tiga pekerjaan yang menempel: popup, logika pemilihan, dan type-ahead. UI SDK memecahnya jadi **50+ perilaku teruji** (roving focus, dsb.) dalam satu paket TypeScript polos, dengan adapter React, Vue, Svelte, Solid, dan Web Components.

Pendampingnya: sebuah *skill* yang mengajari agent perilaku mana yang tersedia dan bagaimana menyusunnya, plus testing kit untuk memeriksa keyboard, fokus, dan aksesibilitas. README-nya menyatakan agent yang akan menulis kodenya, bukan manusia.

### 2. Agent sebagai pemakai

Satu baris `createAgent` (mis. dari `@ui-sdk/react/agent`) memberi tiga tool:

- **`snapshot`** — daftar komponen ringkas: label, nilai, aksi yang tersedia
- **`query`** — mencari opsi di dalam list tanpa membuka dropdown
- **`act`** — menjalankan beberapa langkah dalam satu panggilan, lewat API komponen dan change handler aslinya

`registerTools` mengekspos metode yang sama ke agent bawaan browser lewat **WebMCP** bila browser menyediakan `document.modelContext` — dukungan browser masih sedikit.

## Bukti angka

### Benchmark resmi di repo (dijalankan pewarta)

Layar settings: 3 tab, 24 anggota, menu di setiap baris, dialog konfirmasi. Tugas: ganti nama proyek, ubah visibilitas, promosikan 1 anggota, keluarkan 1, balik 2 switch email, simpan.

| Pendekatan | Tool call | Token | Waktu | Biaya |
|---|---|---|---|---|
| React + Base UI + browser tools | 17 | ~292.000 | 53 dtk | 14 sen |
| UI SDK + bridge | 7 | ~70.000 | 31 dtk | >4 sen |

Lintas React, Vue, Svelte: **54–68% lebih murah**.

### Uji pewarta sendiri (app F1)

- Snapshot awal: accessibility tree **~12 KB** vs UI SDK **~5 KB**
- Tugas kompleks, 3 agent per sisi: browser agent **8 tool call**, baca **~63 KB**; bridge **5, 5, 8 call**, baca **~13 KB** masing-masing → **~5× lebih sedikit teks halaman**
- **Waktu hampir sama:** 28 dtk vs 27 dtk
- **Total token hanya turun ~8%** — karena instruksi agent sendiri mendominasi
- Keuntungan bridge makin besar saat tugas makin banyak (membuka menu, dialog)

**Baca angka ini dengan jujur:** klaim "agent jadi jauh lebih cepat" **tidak** didukung data mereka sendiri. Yang benar-benar turun adalah **jumlah halaman yang harus dibaca agent** dan **biayanya**, bukan waktu.

## Guardrail — bagian paling relevan untuk kita

- `data-agent-confirm` + kalimat penjelas → aksi menunggu izin manusia (`allow` callback)
- `data-agent-hidden` → seluruh seksi disembunyikan dari agent
- penanda `secret` → agent hanya melihat nilai teredaksi
- setiap perubahan sampai ke handler dengan asal **"agent"** → bisa dicatat atau dibatalkan

**Uji jebakan:** tombol kirim ditandai butuh manusia. Hasilnya:
- 3 browser agent (otomasi klik) → **semuanya langsung mengirim**
- 3 agent bridge → **semuanya ditolak**

Ini buktinya: lapisan UI **bisa menegakkan izin**, sedangkan otomasi klik tidak punya cara membedakan dirinya dari manusia.

## Kritik yang sah

- Kreator **React Aria**: perilaku low-level "panas lagi" — hook-nya teruji sejak 2020
- Kreator **Zag.js**: state machine sudah melakukan ini bertahun-tahun
- Kritik paling tajam: agent **sudah bisa** membangun UI fungsional; yang masih buruk adalah **desain**. UI SDK tidak berstyle (kecuali starter opsional) → **tidak memperbaiki itu**. Pewarta mengakui app-nya sendiri "AI-heavy" desainnya
- Masih **beta**, API berubah cepat (beta.1 → beta.16 dalam ~6 hari)

## Reaksi industri

- **Solid UI**: maintainer membangun ulang komponennya di atas UI SDK, rilis "tinggal hitungan hari"
- **shadcn/ui**: belum ada pernyataan
- Kesimpulan pewarta: kalau `shadcn/ui` pindah, mayoritas akan terpakai **tanpa sadar**

## Penilaian

**Nyata:** bagian bridge. Membaca 5× lebih sedikit halaman adalah perbaikan struktural, bukan kosmetik — dan guardrail-nya menutup lubang yang biasanya diakali dengan approval manual di luar UI.

**Kurang meyakinkan:** klaim kecepatan. Data mereka sendiri menunjukkan waktu hampir setara.

**Hype:** perilaku teruji sebagai hal baru. Itu pemaketan ulang pola lama, dengan dokumentasi yang dirancang untuk agent — yang memang punya nilai, tapi bukan penemuan.

## Relevansi untuk Niumination

1. **Pola bridge = alternatif otomasi screenshot/a11y-tree.** Dashboard kita (MIRAI, MATA, niu-oss-dashboard) dioperasikan lewat klik; kalau nanti ada agent yang harus menjalankannya, `snapshot/query/act` jauh lebih hemat token daripada menyerahkan seluruh pohon aksesibilitas.
2. **Guardrail cocok dengan aturan kita.** `data-agent-confirm` adalah approval gate (Hard Rule 1) yang ditegakkan **di lapisan UI**, bukan hanya di prompt. Lebih kuat: otomasi klik tidak bisa melewatinya.
3. **Belum untuk produksi.** Beta, API berubah, adopsi shadcn/ui belum pasti. Kalau dicoba, di `sandbox/` dulu.
4. `design/pick-ui-library` diperbarui: dicatat sebagai opsi dengan cap beta dan penjelasan kapan layak dipertimbangkan.

## Sumber primer

- `https://www.youtube.com/watch?v=ubK6Q53jKg8`
- `npm view @ui-sdk/core version` → `0.1.0-beta.16`
- `https://github.com/vercel-labs/ui` · `https://ui-sdk.dev`

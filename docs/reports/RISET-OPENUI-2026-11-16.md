# RISET — OpenUI (thesysdev/openui)

Tanggal: 2026-11-16 · Mode: pelajari (study + adopsi skill bank, belum dipakai di produksi)
Sumber: https://github.com/thesysdev/openui · https://www.openui.com/ · https://www.openui.com/docs
Repo upstream: `thesysdev/openui` (MIT) — ★ 15.258 · fork 1.016 · dibuat 2024-12-02 · push terakhir 2026-11-16 · TypeScript 93,4%

## Ringkasan

OpenUI adalah **standar terbuka untuk Generative UI**: model mengarang antarmuka dari komponen yang kita
sediakan, bukan sekadar mengembalikan teks/Markdown. Intinya adalah **OpenUI Lang** — DSL kompak,
line-oriented, streaming-first — plus runtime renderer (React, Vue, Svelte, Angular), pustaka komponen
bawaan, dan lapisan produksi (Gateway + Autofix + reliability monitoring).

Klaim utama: **hingga 67% lebih hemat token** daripada JSON. Benchmark internal proyek: 849 token (JSON)
vs 294 token (OpenUI Lang) untuk UI yang sama; pada 60 token/detik, render selesai 4,9s vs 14,2s.

**Status adopsi di ekosistem: BELUM ADA.** Nol padanan OpenUI/generative-UI di bank skill (269 skill)
maupun kode. Hanya 2 laporan yang menyebut frasa "generative UI" sebagai kategori (bukan adopsi).

## Arsitektur

```
Komponen Kita (Zod schema) → System Prompt (dibangkit dari koleksi)
        → Model → aliran OpenUI Lang → Renderer → UI live (progressif)
```

1. **Definisikan komponen** — tiap komponen diberi skema Zod; urutan kunci skema menentukan urutan
   argumen posisional di OpenUI Lang.
2. **Bangkitkan system prompt** — OpenUI membuat instruksi model dari koleksi komponen itu.
3. **Panggil model** — lewat OpenUI Gateway (disarankan: validasi + perbaikan saat streaming) atau
   provider langsung dengan Autofix untuk memperbaiki output invalid.
4. **Render streaming** — `<Renderer />` mengurai tiap baris saat tiba dan memetakannya ke komponen.

### Sintaks (inti)

```text
root = Stack([header, table])
header = Header("Laporan", "Per kuartal")
table = Table({ columns: ["Kuartal", "Pendapatan"], rows: data })
```

- Satu statement per baris: `identifier = Expression`
- Statement pertama wajib `root` (atau memanggil komponen `Root`)
- Argumen posisional → prop, urutan mengikuti kunci skema Zod
- Tipe: komponen, string, number, boolean, null, array, object, referensi identifier
- **Hoisting**: identifier boleh dipakai sebelum didefinisikan → renderer menampilkan skeleton dulu,
  lalu menggantinya saat definisi tiba
- Argumen opsional (trailing) boleh dihilangkan
- Parser membuang bagian invalid, sisanya tetap ter-render (anti layar kosong)

## Lapisan Produk

| Lapisan | Isi |
|---|---|
| Bahasa + runtime | `lang-core` 1.1.1, `react-lang` 1.1.1, `react-headless`, `react-ui` 0.18.9, `react-components`, `vue-lang`, `svelte-lang`, `angular-lang` |
| Antarmuka | Agent Interface — SDK React chat (thread, streaming, tool activity) · `assistant-ui` |
| Produksi | **Gateway** (`api.thesys.dev`, "OpenRouter for Generative UI": failover + koreksi saat streaming) · **Autofix** (perbaiki output invalid, pertahankan provider sendiri) · Reliability Monitoring |
| Alat | `openui-cli` 0.6.3, `devtools`, `server`, observability, `a2ui`, `langchain` |

Total 20 paket di `packages/`. Spec **OpenUI 1.1** (4 Nov 2026) di `spec/`.

### Integrasi

Vercel AI SDK · LangChain/LangGraph · Google ADK · Mastra · AG-UI · assistant-ui · Convex ·
Cloudflare · CrewAI · n8n. Provider: OpenAI, Anthropic, Gemini, DeepSeek, xAI, Mistral, Qwen, Ollama.

### Scaffold

```bash
npx @openuidev/cli@latest create --name genui-chat-app
```

Gateway bersediaan OpenAI-compatible (Chat Completions + Responses API):

```ts
const gateway = new OpenAI({ apiKey: process.env.THESYS_API_KEY, baseURL: 'https://api.thesys.dev/v1/embed' })
```

## Relevansi ke Ekosistem

- **Bukan pengganti `pick-ui-library`.** Skill itu mengcurasi library UI statis (Sonner, cmdk, dst);
  OpenUI membuat UI *dari model*. Keduanya bisa berdampingan: pilih library statis untuk kebutuhan
  tetap, pakai Generative UI untuk permukaan yang harus menyesuaikan konteks percakapan.
- **Permukaan terdekat:** `niu-oss-dashboard` (Next.js + cmdk + framer-motion; ada `CsInbox` untuk
  membalas pesan tamu) dan `sites/kelas` (Next.js, baru memakai Sonner). Arsip `Kai-assistant`
  (frontend-r3f dengan ChatPanel) sudah diarsipkan.
- **Tidak ada agent skill resmi** di repo upstream. Fork `Lucas-FManager/openui` memuat `skills/openui`,
  tetapi itu kontribusi fork — bukan jalur resmi.

## Risiko & Catatan

- **Lock-in vendor di lapisan model** bila memakai Gateway/Autofix (SaaS `THESYS_API_KEY`). Pemakaian
  runtime saja (tanpa Gateway) tetap mungkin dan menjaga provider sendiri.
- **Telemetry** di `lang-core` + CLI (project ID di-hash, ditulis atomik saat install). Perlu diperiksa
  sebelum dipakai di lingkungan sensitif/ASN.
- **Beban definisi:** tiap komponen wajib skema Zod — biayanya nyata, bukan sekadar pasang paket.
- **Model harus patuh format**; tanpa Autofix/Gateway, output invalid hanya sebagian ter-render.
- **Telemetri & kepatuhan:** komponen dirender dari output model → batasi komponen yang boleh
  dipakai model, jangan render HTML/URL mentah dari model tanpa sanitasi.

## Rekomendasi

Layak **diadopsi sebagai skill bank** (`skills/design/generative-ui-openui`) — panduan kapan memakai
OpenUI Lang vs JSON vs komponen statis, pola definisi komponen Zod, jalur tanpa Gateway. Belum
layak masuk produksi: butuh uji nyata + keputusan soal Gateway vs Autofix vs runtime saja.

Kandidat uji berikutnya: `niu-oss-dashboard` (Next.js, sudah cmdk/framer-motion) — dengan catatan
AGENTS.md-nya ketat soal berkas generated dan paritas i18n.

## Bukti

| Perintah | Hasil |
|---|---|
| `gh repo view thesysdev/openui` | ★15.258, fork 1.016, MIT, `pushedAt 2026-11-16T10:23:42Z` |
| `gh api repos/thesysdev/openui/contents/packages` | 20 paket |
| `gh api repos/thesysdev/openui/contents/spec` | `language.md`, `overview.md`, `prompt.md`, `fixtures/` |
| `npm view @openuidev/cli version` | 0.6.3 |
| `npm view @openuidev/lang-core version` | 1.1.1 |
| `npm view @openuidev/react-ui version` | 0.18.9 |
| `web_extract openui.com/docs/openui-lang` | arsitektur, klaim 67%, contoh sintaks |
| `web_extract openui.com/docs/openui-lang/specification` | tata bahasa + hoisting |
| `web_extract openui.com/docs/production` | Gateway, Autofix, Reliability Monitoring |
| `grep -in "openui\|generative" docs/reports/*` | 2 sebutan kategori, 0 adopsi |
| `search_files generative-ui\|OpenUI` di ekosistem | 0 match (kecuali 2 laporan di atas) |

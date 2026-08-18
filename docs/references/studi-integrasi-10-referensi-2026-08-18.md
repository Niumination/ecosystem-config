# Studi Integrasi 10 Referensi untuk Hermes Agent

**Tanggal studi:** 18 Agustus 2026  
**Target yang dipilih:** instalasi Hermes yang sudah ada, **macOS**, deliverable **MVP add-on pack**  
**Baseline Hermes:** `NousResearch/hermes-agent` commit `daca38696738524ffdb901c18dbdbef64c1a97a9`

## Ringkasan keputusan

Tidak semua proyek layak “digabungkan” ke core Hermes. Hermes terbaru sudah memiliki MCP, provider registries, ComfyUI skill, Krea image provider, PDF/OCR skills, browser automation, local STT, approval flow, artifacts, dan Desktop UI besar berbasis Electron/React. Karena itu strategi yang aman adalah:

1. **Tambahkan kemampuan yang benar-benar belum ada** sebagai plugin/skill.
2. **Gunakan extension point resmi Hermes**, bukan fork core untuk MVP.
3. **Ambil pola arsitektur**, bukan menyalin seluruh aplikasi.
4. **Tunda rewrite Desktop dan staged simulation penuh** ke fase core terpisah.

Hasil MVP dalam paket ini:

- `pdf_inspect_fast` dan `pdf_extract_markdown` memakai `pdf-inspector`.
- Provider STT `handy` serta tool `local_audio_transcribe` untuk macOS.
- Gatekeeper Lite: approval Hermes untuk aksi Eromify/remote yang berbiaya atau memiliki side effect, plus audit hash tanpa menyimpan argumen mentah.
- Blueprint code-only: ekspor dan inspeksi arsip tanpa kredensial, history, database, cache, symlink, atau auto-execution.
- Skill ego-lite yang diadaptasi untuk Hermes dan macOS.
- Skill + API workflow builder Krea 2 Ostris Edit dengan 1–3 reference images.
- Skill Eromify MCP dengan OAuth, credit check, dan batasan konten.
- Generator visual “neural memory map” mandiri berbasis Canvas 2D.

---

## Apa yang sudah dimiliki Hermes saat ini

Audit baseline resmi menunjukkan bahwa Hermes sudah mempunyai fondasi yang sangat kuat:

- **Plugin API:** `register_tool`, `register_skill`, `register_browser_provider`, `register_transcription_provider`, `register_image_gen_provider`, `register_video_gen_provider`, hooks, middleware, durable plugin state, serta capability gates.
- **MCP:** stdio dan Streamable HTTP, OAuth 2.1/PKCE, token cache, mTLS, header identity, filtering tool per server, timeout, reconnect, circuit breaker, dan Desktop setup card.
- **Browser:** local `agent-browser`, Browser Use, Browserbase, Firecrawl, Camofox, raw CDP, session isolation, SSRF/private-address checks, dan credential-scrubbed subprocess environment.
- **PDF:** bundled `pdf`, `ocr-and-documents`, dan `nano-pdf` skills.
- **ComfyUI:** bundled skill v5.1.0 dengan setup, hardware check, REST/WS execution, batch, dependency checks, cloud routing, cancellation, dan safe downloads.
- **Krea:** image-generation provider untuk Krea 2 Medium/Large/Turbo melalui API Krea.
- **STT:** faster-whisper lokal, local command, Groq, OpenAI, Mistral, xAI, ElevenLabs, DeepInfra, command-provider registry, dan Python provider plugin API.
- **Desktop:** Electron/React application dengan artifacts, local previews, projects/workspaces, terminal, MCP setup UI, approval mode, dan remote gateway support.

Konsekuensinya: MVP harus **mengisi gap**, bukan membuat sistem paralel.

---

## Analisis per referensi

### 1. Cloudflare OS

Sumber: https://github.com/cloudflare/cloudflare-os  
Revisi dipelajari: `3562627ed06d9c4650e058f2b47ada21d33334a7`  
Lisensi: Apache-2.0

#### Gagasan utama

- **Gadgets:** setiap artifact dapat menjadi aplikasi kecil yang privat dan dapat dimodifikasi agent.
- **Blueprints:** template menyimpan snapshot kode dan kebutuhan binding, tetapi tidak membawa storage, chat history, atau credentials.
- **Gatekeepers:** capability-scoped adapters yang mengatur OAuth, akses resource, audit, human approval, apply/reject/revert, dan observation authorization.
- **Asynchronous staged actions:** aksi side-effect disimpan sebagai pending; agent melihat hasil simulasi sehingga dapat melanjutkan; manusia menyetujui batch kemudian.

#### Kondisi Hermes

Hermes sudah memiliki approval transports, `pre_tool_call` hook yang dapat mengembalikan `{"action":"approve"}`, plugin capabilities, secret scoping, tool audit primitives, artifact previews, dan projects. Namun Hermes belum memiliki generalized staged-action store dengan simulated read overlays seperti Cloudflare OS.

#### Penerapan MVP

- **Gatekeeper Lite** memakai approval flow native Hermes; tidak membuat approval UI baru.
- Audit menyimpan `tool`, rule, decision, timestamp, dan SHA-256 canonical args—**bukan argumen mentah**.
- Unknown mutating MCP tools dapat dipaksa ke approval dengan mode `external`.
- `blueprint_export` mengekspor code-only archive dan fail-closed saat mendeteksi secret.
- `blueprint_inspect` tidak mengekstrak atau mengeksekusi apa pun.

#### Fase core yang disarankan

Tambahkan `ActionJournal` generik ke Hermes dengan state `pending/applied/rejected/reverted`, provider-specific simulation reducer, read-your-pending-writes overlay, bulk review UI, dan idempotency keys. Ini perubahan core besar dan tidak aman dipaksakan sebagai add-on.

---

### 2. Dioxus

Sumber: https://github.com/dioxuslabs/dioxus  
Revisi dipelajari: `393d190a801ccb441d41923e232289b4f8a5c669`  
Lisensi: MIT OR Apache-2.0

#### Nilai yang relevan

Dioxus menyediakan satu Rust UI model untuk web/desktop/mobile, signals, typed server functions, WebSocket/SSE, bundling, hot reload, dan renderer native eksperimental.

#### Keputusan

**Tidak melakukan rewrite Hermes Desktop.** Hermes Desktop sekarang memiliki sekitar 1.400 file TypeScript/TSX, Electron shell, terminal, artifacts, project switching, remote gateway, extensive tests, packaging, dan update lifecycle. Migrasi ke Dioxus akan menjadi proyek multi-kuartal dengan risiko regresi tinggi dan tidak memberi nilai MVP.

Pola yang tetap berguna untuk fase berikutnya:

- Typed WebSocket event contracts antara gateway dan UI.
- Shared schema generation untuk Rust/Python/TypeScript boundaries.
- Kemungkinan companion app ringan atau mobile shell di masa depan.
- Native renderer hanya setelah parity dan benchmark jelas.

---

### 3. tdf

Sumber: https://github.com/itsjunetime/tdf  
Revisi dipelajari: `de0050499e96f2f9d69b3e380fa3dd8de7119b90`  
Lisensi: AGPL-3.0-only

#### Gagasan yang berguna

- Rendering asinkron di thread khusus karena MuPDF document tidak `Send`.
- Prioritas pre-render di sekitar halaman aktif, bukan selalu urut dari awal.
- Search dan highlight terintegrasi dengan render state.
- File hot reload dengan debounce dan fallback ke dokumen terakhir yang valid.
- Reactive layout, zoom, fit/fill, rotation, terminal image protocol.

#### Keputusan

Kode tidak divendor atau ditautkan ke plugin karena AGPL dan karena Hermes tidak membutuhkan terminal PDF viewer baru untuk MVP. Polanya direkomendasikan untuk future Desktop PDF preview:

- page-neighborhood render queue;
- cancel/reprioritize saat user jump;
- search index terpisah dari visual raster;
- stale-last-good preview saat file sedang ditulis ulang.

Pengguna masih dapat memasang `tdf` sebagai binary eksternal bila menginginkan preview TUI.

---

### 4. Firecrawl pdf-inspector

Sumber: https://github.com/firecrawl/pdf-inspector  
Revisi dipelajari: `74ebce430c5caae45b7b15c111b5d9a8a7ef2daf`  
Paket: `pdf-inspector==1.15.0`  
Lisensi: MIT

#### Kelebihan

- Klasifikasi text/scanned/image/mixed dengan confidence dan per-page OCR routing.
- Position-aware extraction, reading order multi-column, RTL, headings, lists, links, tables, dan encoding diagnostics.
- Python/Node/Rust/WASM APIs.
- Selective OCR dengan provenance.
- Native text path sangat ringan; OCR runtime dan model terpisah.

#### Gap Hermes yang diisi

Bundled PDF skills Hermes menggunakan pypdf/pdfplumber/PyMuPDF/marker. `pdf-inspector` memberi fast router dan output Markdown terstruktur yang lebih cocok sebagai local default sebelum model OCR besar.

#### Implementasi

- `pdf_inspect_fast`: detection only.
- `pdf_extract_markdown`: per-page Markdown; selectors user-facing 1-based.
- Full Markdown ditulis ke cache; preview context dibatasi 12.000 karakter.
- OCR default `off`; `auto` harus eksplisit dan default `offline=true`.
- Provenance dan `pages_routed_to_ocr` dilaporkan agar agent tidak mengklaim OCR secara palsu.

---

### 5. CitroLabs ego-lite

Sumber: https://github.com/citrolabs/ego-lite  
Revisi dipelajari: `c46a439e7fbad90ad33dbea6c6af329b6009809f`  
Lisensi: MIT  
Platform saat studi: macOS

#### Gagasan utama

- Satu browser untuk manusia dan agent, tetapi agent bekerja dalam isolated task spaces.
- Memakai login/cookies user tanpa berebut tab yang sama.
- Semantic snapshot, screenshot/visual path, direct JS/CDP path.
- Task-space ownership, handoff, takeover, user-control hard stop, dan cleanup.
- Agent menyusun beberapa operasi menjadi satu JavaScript program untuk mengurangi tool-call/token loop.

#### Kondisi Hermes

Hermes sudah memiliki browser tools, local/cloud providers, session isolation, CDP, private-address guard, credential scrubbing, dan computer-use exact-binding/ref freshness. Karena itu ego-lite menjadi **optional authenticated-browser backend**, bukan pengganti universal.

#### Implementasi

Skill upstream disertakan dengan MIT notice dan diadaptasi:

- Gunakan tool `terminal` Hermes, bukan istilah `Bash`.
- Trigger dipersempit: ego-lite untuk explicit request, authenticated session, dan human takeover.
- Public read-only research tetap memakai built-in browser/web tools.
- App installation tetap opt-in melalui `--with-ego-app`.

Risiko utama: browser agent mewarisi login user. Gunakan task spaces, jangan auto-approve transaksi, dan selesaikan/close space setelah tugas.

---

### 6. ComfyUI-Krea2-Ostris-Edit

Sumber: https://github.com/ostris/ComfyUI-Krea2-Ostris-Edit  
Revisi dipelajari dan dipin: `7756566160c4a1b24bb1bd9f0ff3ced1a83d7547`  
Lisensi: MIT

#### Fungsi

- `TextEncodeKrea2OstrisEdit`: prompt + 1–3 images melalui Qwen3-VL template dan VAE reference latents.
- `Krea2OstrisEditModelPatch`: memasukkan reference latents dengan `index_timestep_zero`.
- Optional KV cache hanya kompatibel dengan LoRA yang dilatih dengan opsi yang sama.

#### Implementasi

- Installer custom node dipin ke commit yang dipelajari.
- Upstream editor workflow disimpan hanya sebagai referensi.
- Wrapper baru membangun **API-format workflow** secara dinamis, karena editor-format JSON tidak dapat dikirim langsung ke `/prompt`.
- Hanya reference nodes yang benar-benar dipakai yang dibuat.
- Runner mendelegasikan upload, WS progress, cancellation, cloud routing, dan download ke bundled ComfyUI skill Hermes.
- Default `kv_cache=false`.

---

### 7. ComfyUI

Sumber: https://github.com/comfy-org/comfyui  
Revisi dipelajari: `cc0fc21fea7a6a82f568362b15b7fbd713b419c1`  
Lisensi: GPL-3.0

#### Gagasan utama

Node graph, async queue, partial graph execution, smart memory/model offload, custom nodes, `/prompt`, `/history`, `/view`, `/queue`, `/interrupt`, `/object_info`, WebSocket progress, dan API workflows.

#### Kondisi Hermes dan keputusan

Hermes sudah memiliki ComfyUI skill lengkap. Karena itu MVP tidak membuat Comfy client kedua. Krea wrapper memanfaatkan runner Hermes yang ada. ComfyUI tetap external process/API boundary; kode GPL tidak disalin atau dilink ke plugin MIT.

Prinsip produksi:

- API-format workflows;
- health/dependency checks sebelum submit;
- pin custom nodes dan model hashes;
- async submit + progress + cancellation;
- path-safe output materialization;
- approval sebelum model download besar atau remote paid generation.

---

### 8. Eromify

Sumber: https://www.eromify.com/ dan https://www.eromify.com/mcp  
Jenis: proprietary remote service

#### Kapabilitas publik yang ditemukan

- Remote MCP endpoint: `https://api.eromify.com/mcp`.
- OAuth discovery tersedia dengan authorization code + PKCE S256 dan dynamic client registration.
- Scopes publik: `read`, `generate`, `edit`.
- Halaman publik menyatakan avatar management, image/video/edit generation, batch campaigns, credit balance, dan service limits.

#### Integrasi Hermes

Hermes sudah mendukung remote MCP + OAuth, sehingga tidak perlu adapter Python khusus:

```bash
hermes mcp add eromify --url https://api.eromify.com/mcp --auth oauth
hermes mcp configure eromify
```

Skill menambahkan workflow yang aman:

- read account/avatar/model/balance dulu;
- rencanakan model, count, modality, ratio, dan estimasi credits;
- approval sebelum video/edit atau batch besar;
- generate satu sampel sebelum scaling;
- download output yang disetujui dan simpan generation metadata.

#### Batasan konten

Terms publik Eromify tanggal 8 Agustus 2026 menyatakan karakter harus synthetic/fictional, account 18+, tidak boleh memakai likeness orang nyata, minor, non-consensual content, dan kategori terlarang lainnya. Skill memberlakukan batasan ini secara eksplisit. Terms terkini selalu mengalahkan snapshot studi.

---

### 9. Handy

Sumber: https://github.com/cjpais/Handy  
Revisi dipelajari: `99052eefa6c15c32d11d7ccc29f3d14b6ae26cb8`  
Lisensi: MIT

#### Gagasan utama

- Local/offline STT.
- Whisper-family via `transcribe-cpp`; Parakeet dan model lain via `transcribe-rs`/ONNX.
- VAD, audio resampling, model caching/unload lifecycle, streaming committed/tentative text.
- macOS Metal support.
- Headless CLI: `Handy --transcribe-file <16k mono PCM WAV> --json`.

#### Implementasi

Provider `handy` menggunakan extension point resmi Hermes:

1. incoming audio dinormalisasi dengan ffmpeg ke 16 kHz mono PCM WAV;
2. Handy dipanggil dalam headless JSON mode;
3. field `text` diparse ke envelope standar Hermes;
4. model tetap lokal dan audio tidak dikirim ke cloud.

Provider dormant sampai `stt.provider: handy` dipilih. Handy harus diluncurkan sekali dan model harus sudah diunduh/dipilih.

---

### 10. Facebook reel — JavaScript neuron animation

Share URL berhasil dipetakan ke reel ID `1765695284421258`. Metadata publik menyebut “COOL Neuron Animation Using JavaScript”, dan thumbnail memperlihatkan neuron procedural serta snippet `THREE.CatmullRomCurve3` untuk wandering paths.

#### Penerapan

Tidak ada video atau kode reel yang disalin. Paket berisi implementasi baru, self-contained Canvas 2D untuk memvisualisasikan:

- memories;
- skills;
- tasks;
- artifacts;
- agent relationships.

HTML tidak memakai CDN/network, mendukung hover, drag, pan, zoom, signal pulses, dan `prefers-reduced-motion`. Ini cocok sebagai Hermes artifact, bukan decorative core UI yang selalu menyala.

---

## Arsitektur MVP

```text
Hermes Agent (existing install)
├── Native plugin: hermes-multimodal-mvp
│   ├── PDF tools -> pdf-inspector Python wheel
│   ├── STT provider -> Handy CLI -> local model
│   ├── Blueprint tools -> safe ZIP manifest (no execution)
│   └── pre_tool_call hook -> Hermes native approval transport + hash-only audit
├── Skills
│   ├── ego-browser -> ego-lite macOS app (optional)
│   ├── krea2-ostris-edit -> existing ComfyUI skill runner -> ComfyUI API
│   ├── eromify-studio -> Hermes MCP OAuth client -> Eromify remote service
│   ├── pdf-inspector-fast
│   └── neural-memory-map -> self-contained HTML artifact
└── Existing Hermes core remains unchanged
```

## Gatekeeper modes

| Mode | Perilaku |
|---|---|
| `off` | Tidak ada rule tambahan |
| `paid` | Approval untuk mutating Eromify dan remote Comfy Cloud generation |
| `external` | `paid` + mutating/unknown MCP tools |
| `strict` | `external` + browser mutations dan outbound/persistent actions |

Default paket: `paid`. Ini menjaga UX tetap ringan. Audit berada di:

```text
$HERMES_HOME/plugin-data/hermes-multimodal-mvp/action-audit.jsonl
```

Argumen tidak disimpan, hanya SHA-256.

## Prioritas lanjutan

### P0 — jalankan setelah instalasi

- Install plugin/skills dan `pdf-inspector`.
- Jalankan `hermes plugins doctor` pada Mac target.
- Tes PDF text-based dan scanned.
- Install/launch Handy, download model, lalu test satu WAV.
- Jika perlu, install ego-lite dan selesaikan onboarding.
- Jika GPU/memory cukup, install pinned Krea node dan jalankan smoke test.
- Hubungkan Eromify hanya jika user memiliki plan dan setuju dengan terms/cost.

### P1 — hardening

- Golden-corpus tests untuk PDF reading order/tables.
- Model hash manifest untuk Krea assets.
- Cost-estimation hook berdasarkan tool metadata Eromify aktual setelah OAuth discovery.
- Per-tool MCP allowlist dan expiry-aware consent.
- Signed blueprint manifests dan manual import review UI.

### P2 — perubahan core

- Generalized staged action journal dengan simulation reducer.
- Bulk review/apply/reject/revert UI di Hermes Desktop.
- Typed artifact bindings dan blueprint instantiation.
- Async PDF renderer di Desktop memakai pola neighborhood priority dari tdf.
- Evaluasi Dioxus hanya untuk companion/mobile shell, bukan rewrite langsung.

## Yang belum dapat divalidasi di sandbox

- Tidak ada login Eromify, plan, credits, atau actual MCP tool list.
- ego-lite app dan browser profile tidak dipasang.
- Handy app/model tidak tersedia.
- ComfyUI server, GPU, model, dan edit LoRA tidak tersedia, sehingga workflow belum dieksekusi end-to-end.
- OCR native dependencies untuk `pdf-inspector` belum dipasang.
- Plugin Doctor resmi membutuhkan dependency environment Hermes lengkap di mesin target.

Yang sudah divalidasi:

- Python compilation.
- Shell syntax.
- 7 unit tests untuk blueprint, secret rejection, Gatekeeper classification, Krea API graph builder, dan self-contained neural map.
- Neural-map demo berhasil dibuat.

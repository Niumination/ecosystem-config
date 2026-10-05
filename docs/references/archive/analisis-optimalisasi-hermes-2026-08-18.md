# Analisis, Kritik, dan Rencana Optimalisasi Hermes Agent

**Tanggal kajian:** 18 Agustus 2026 (WIB)  
**Bahan utama:** `ecosystem-config-snapshot-2026-08-17.md`, dokumentasi Hermes Agent terkini, sembilan sumber yang dapat diakses, serta satu tautan Facebook yang tidak dapat diambil tanpa sesi/login.

---

## 1. Kesimpulan eksekutif

Ekosistem ini sudah kaya fitur, tetapi saat ini **belum dapat disebut optimal atau siap produksi**. Hambatan utamanya bukan kekurangan aplikasi, melainkan reliabilitas, keamanan, dan terlalu banyak sumber kebenaran.

### Lima keputusan terpenting

1. **Pulihkan Mission Control terlebih dahulu.** Port 5200 tidak sehat, sedangkan banyak integrasi bergantung padanya. Jangan menambah UI/framework baru sebelum health check, service supervision, dan kontrak API stabil.
2. **Jadikan disk internal APFS sebagai lokasi runtime kanonik.** SQLite, `state.db`, sesi, log, dan konfigurasi aktif jangan dijalankan dari USB/ExFAT/NTFS. USB dipakai sebagai paket portabel atau backup terenkripsi, bukan database hidup.
3. **Wajibkan autentikasi untuk Mission Control dan Hermes API.** `MC_API_KEY` tidak boleh opsional pada endpoint yang dapat mengirim Telegram, mengubah konfigurasi, mengakses artefak, atau mengendalikan agen.
4. **Kurangi variasi model/fallback.** Satu model utama yang lulus uji tool-calling + 2–3 fallback teruji lebih baik daripada 19 model gratis yang tidak memiliki SLA, kemampuan tools, context window, dan kebijakan data yang seragam.
5. **Integrasi dilakukan bertahap:**
   - **Adopsi sekarang:** `pdf-inspector` dan API resmi Hermes untuk hubungan Mission Control ↔ Hermes.
   - **Adaptasi konsep:** Gatekeeper dari Cloudflare OS.
   - **Remote GPU:** ComfyUI + Krea 2.
   - **Pilot terisolasi:** ego-lite dan Eromify.
   - **Opsional/defer:** Handy, Dioxus, dan tdf.

### Status keputusan per tautan

| Komponen | Keputusan | Prioritas |
|---|---|---:|
| Cloudflare OS | Ambil pola Gatekeeper/action broker; jangan memasang seluruh platform | Tinggi |
| Dioxus | POC klien Mission Control saja; jangan rewrite sekarang | Rendah |
| tdf | Viewer manusia opsional, bukan alat ekstraksi agen | Rendah |
| pdf-inspector | Adopsi sebagai jalur ingest PDF lokal pertama | Sangat tinggi |
| ego-lite | Pilot dengan profil browser khusus; audit installer dahulu | Menengah |
| ComfyUI-Krea2-Ostris-Edit | Jalankan pada worker GPU remote, pin commit/versi | Menengah |
| ComfyUI | Gunakan skill Hermes yang sudah dibundel + API REST/WS | Tinggi |
| Eromify | MCP opsional, default nonaktif, profil kreatif terpisah | Menengah |
| Handy | Aplikasi pendamping dictation, bukan backend Hermes | Rendah |
| Facebook Reel | Belum dapat dianalisis; perlu video/screenshot dari pengguna | Tertunda |

---

## 2. Batas kajian

File yang diberikan adalah **snapshot ringkasan**, bukan `config.yaml` asli, source Mission Control, log startup, skema SQLite, konfigurasi `launchd`, atau hasil `hermes doctor`. Karena itu:

- Kritik konfigurasi di bawah ini kuat pada sisi arsitektur dan operasional.
- Contoh YAML adalah **template merge**, bukan file pengganti yang boleh langsung menimpa konfigurasi aktif.
- Saya tidak mengubah Mac pengguna; implementasi yang disertakan hanya berupa artefak siap salin di workspace.
- Versi Hermes yang terpasang belum diketahui. Sintaks harus diverifikasi dengan `hermes --version`, `hermes config check`, dan `hermes config migrate` sebelum diterapkan.

---

## 3. Temuan dan kritik konfigurasi saat ini

## 3.1 Temuan kritis

### A. Mission Control tidak sehat, tetapi menjadi pusat kendali

Snapshot menyebut proses pernah terlihat terkait port 5200, namun koneksi tertutup dan health check timeout. Ini adalah prioritas P0.

**Masalah:**

- Tidak ada bukti service manager (`launchd`) menjaga proses tetap hidup.
- Belum dibedakan antara **liveness** (proses hidup) dan **readiness** (DB, router, Telegram, dan Hermes siap).
- “Port-bound CLOSED” bukan status layanan yang cukup diagnostik.
- Router disebut “v3”, tetapi prefix yang aktif bercampur antara `/api/mc` dan `/api/v1`.
- Frontend `app.js` belum mengikuti format respons backend terbaru.

**Perbaikan:**

1. Tambahkan endpoint tanpa efek samping:
   - `GET /healthz`: event loop dan proses hidup.
   - `GET /readyz`: DB dapat dibaca/ditulis, migrasi benar, router termuat, dependency utama siap.
   - `GET /version`: versi aplikasi, schema version, git SHA, build time.
2. Kelola dengan satu `launchd` LaunchAgent, bukan proses manual/nohup.
3. Bind ke `127.0.0.1:5200` kecuali ada reverse proxy terautentikasi.
4. Simpan stdout/stderr ke log terstruktur dan rotasi file.
5. Gunakan satu kontrak OpenAPI sebagai sumber kebenaran; generate client frontend atau tambahkan contract test untuk setiap response schema.
6. Pilih versioning yang konsisten, misalnya `/api/v1/...`; istilah “backend v3” tidak boleh bercampur dengan URL v1 tanpa dokumentasi migrasi.

**Uji penerimaan:** setelah reboot dan setelah `kill -9`, service otomatis kembali sehat; `/healthz` merespons cepat dan `/readyz` gagal tertutup saat DB rusak.

### B. Autentikasi Mission Control bersifat opsional

Mission Control memiliki endpoint pengiriman Telegram, konfigurasi, artefak, Hermes, agents, tasks, cost, dan WebSocket swarm. CORS localhost bukan autentikasi.

**Perbaikan wajib:**

- `MC_API_KEY` harus required dan berbeda dari `API_SERVER_KEY` Hermes.
- Kunci minimal 32 byte acak, disimpan di `.env` dengan mode `0600`.
- Semua REST sensitif dan handshake `/ws/swarm` harus memverifikasi bearer/token.
- Validasi header `Origin` pada WebSocket.
- Gunakan scope, misalnya `mc:read`, `mc:operate`, `mc:admin`; dashboard normal tidak perlu hak edit config.
- Endpoint mutasi harus memiliki idempotency key dan audit event.
- Rate limit per principal/token, bukan hanya per IP. Di localhost, semua klien terlihat sebagai IP yang sama.

### C. SIP dinonaktifkan

SIP disabled meningkatkan dampak malware, installer, dan agen yang keliru. Tidak ada alasan operasional pada snapshot yang membuktikan SIP harus tetap nonaktif.

**Saran:** dokumentasikan dependensi yang benar-benar memerlukan SIP off. Jika tidak ada, aktifkan kembali dari Recovery Mode. Verifikasi juga FileVault, Gatekeeper, XProtect, firewall, dan update otomatis; statusnya tidak tercatat pada snapshot.

### D. Runtime dan state berisiko tersebar di media eksternal

- USB HermesAgent hanya ±30,75 GB.
- `Niumination` dan volume Windows adalah NTFS read-only.
- `Mac Win` ExFAT writable, tetapi tidak menyediakan journaling/permission semantics seperti APFS.
- Disk internal memiliki ±43,6 GB kosong—cukup untuk aplikasi agen, tetapi tidak aman untuk koleksi model Comfy/Krea berukuran besar.

**Kebijakan yang disarankan:**

| Jenis data | Lokasi kanonik |
|---|---|
| `config.yaml`, `.env`, `auth.json`, `state.db`, sessions, logs | Internal APFS |
| Mission Control SQLite + WAL | Internal APFS |
| Repository aktif | Internal APFS |
| USB HermesAgent | Backup terenkripsi/paket portabel/read-mostly |
| NTFS | Sumber baca atau arsip; bukan target write |
| ExFAT | Pertukaran file, bukan secret store atau live SQLite |
| ComfyUI model/outputs besar | Worker GPU/storage remote |

Untuk Hermes SQLite, WAL cocok jika state berada di APFS. Jika tetap di filesystem eksternal yang tidak kompatibel, gunakan journal `DELETE`, tetapi solusi terbaik tetap memindahkan runtime ke APFS. Lakukan backup terjadwal, checksum, serta uji restore—bukan sekadar copy satu arah.

---

## 3.2 Temuan tinggi

### E. Skill bank mengalami configuration drift

Snapshot mencatat:

- bank pusat: 47 skills;
- Hermes USB: 211 skills;
- Hermes lain: 2 skills;
- Jcode: missing.

Pernyataan “tidak ada duplikasi” hanya membuktikan kondisi bank pusat, bukan konsistensi semua target. Banyak skill juga memperluas permukaan supply-chain dan dapat menyebabkan collision nama atau instruksi.

**Perbaikan:**

1. Satu manifest kanonik berisi `name`, version, source URL, commit/tag, SHA-256, license, platform, trust tier, dan enabled targets.
2. Jangan menyinkronkan semua skill ke semua platform. Hermes mendukung enable/disable per platform; development skill tidak perlu tersedia pada Telegram.
3. Kelompokkan trust:
   - `builtin-reviewed`;
   - `internal-reviewed`;
   - `third-party-pinned`;
   - `quarantined`.
4. Tolak skill yang menyuruh `curl | sh`, menghapus quarantine, membaca browser utama, atau memprioritaskan dirinya di atas tool keamanan tanpa review.
5. CI: validasi frontmatter, link lokal, executable scripts, hash, license, prompt-injection scan, dan secret scan.
6. Rekonsiliasi target hingga jumlah dan SHA manifest terukur; jangan memakai jumlah folder sebagai bukti sinkronisasi.

Dokumentasi Hermes memakai progressive disclosure, jadi skill hanya dimuat penuh saat dibutuhkan. Namun deskripsi semua skill tetap menjadi katalog awal; 211 skill yang tidak terkurasi tetap menambah noise dan risiko [S6].

### F. Strategi provider/model tidak deterministik

Snapshot menyebut `9router`, `huancheng`, model aktif `stepfun/step-3.7-flash:free` melalui Nous, serta 19 kandidat OpenRouter `:free`.

**Kritik:**

- Provider aktif dan nama model belum terbukti kompatibel secara eksplisit.
- `9router` tidak memiliki URL, env key, transport, owner, atau kebijakan data pada snapshot.
- `huancheng` adalah endpoint pihak ketiga; belum ada bukti retention policy, lokasi data, TLS policy, SLA, dan daftar model.
- Format lama `mode`/`api_mode` sebaiknya dimigrasikan ke named `providers:` dengan `transport` pada Hermes terkini.
- Model gratis dapat hilang, rate-limited, tidak mendukung tools/JSON/vision, atau memiliki context limit berbeda.

**Desain optimal:**

- 1 model utama yang lulus acceptance suite.
- 2–3 fallback lintas provider yang sudah diuji, berurutan.
- Auxiliary model terpisah untuk compression/title/web extraction bila memang lebih murah.
- `provider_routing.require_parameters: true` dan `data_collection: deny` untuk Nous/OpenRouter bila sesuai kebutuhan.
- Timeout dan stale timeout per provider/model.
- Kunci hanya melalui `key_env`; jangan inline.

**Acceptance suite model:**

1. tool call sederhana dan berantai;
2. JSON schema valid;
3. context compression;
4. file read/write di sandbox;
5. bahasa Indonesia;
6. 429/5xx failover;
7. malformed tool result recovery;
8. vision bila diklaim didukung;
9. biaya dan latency p50/p95;
10. redaksi secret.

Model gratis boleh menjadi fallback development, bukan satu-satunya fondasi gateway produksi.

### G. Hermes dan Mission Control berpotensi menduplikasi fungsi

Hermes terkini sudah menyediakan OpenAI-compatible API, Runs API, SSE event stream, session API, `/v1/capabilities`, `/health/detailed`, skill/toolset discovery, dan cancellation [S3]. Mission Control sebaiknya **mengonsumsi API publik ini**, bukan mengimpor internal Python Hermes atau membuat kontrak paralel.

**Target alur:**

```text
Browser dashboard
      |
      | HTTP/WS + MC_API_KEY/session
      v
Mission Control :5200  ---- SQLite/audit/action approvals
      |
      | server-to-server + API_SERVER_KEY
      v
Hermes API :8642 (loopback only)
      |
      +-- model providers
      +-- approved MCP servers
      +-- sandbox terminal
      +-- remote ComfyUI worker
```

Dengan pola ini:

- Browser tidak memerlukan CORS langsung ke Hermes.
- Hermes dan Mission Control memiliki kunci berbeda.
- Mission Control dapat memakai `/v1/capabilities` agar adaptif terhadap versi.
- Cancellation, streaming, dan session continuity tidak dibuat ulang.
- Endpoint `/api/mc/hermes` dapat menjadi adapter tipis, bukan implementasi agen kedua.

### H. “Git clean” bukan “sistem sehat”

Semua repo clean hanya menunjukkan tidak ada perubahan worktree. Snapshot belum mencatat test result, dependency audit, deploy SHA, error budget, backup, atau ownership.

Tambahkan ke registry:

- owner/maintainer;
- lifecycle (`active`, `maintenance`, `frozen`, `archive`);
- production URL dan deploy SHA;
- last successful CI/deploy/backup;
- package-lock/uv.lock/Cargo.lock status;
- security scan/SBOM;
- SLO dan health URL;
- recovery procedure.

`latticesend` harus segera memiliki remote privat atau backup terverifikasi. Repo stale dipindahkan ke archive agar tidak membebani indeks dan otomasi.

---

## 3.3 Temuan menengah

### I. SQLite perlu kebijakan operasional

Adanya endpoint WAL checkpoint tidak cukup. Pastikan:

- DB berada di APFS;
- `foreign_keys=ON`;
- `busy_timeout` ditetapkan;
- transaksi pendek;
- migrasi versioned;
- backup konsisten menggunakan SQLite backup API, bukan copy file saat WAL aktif;
- `PRAGMA quick_check` terjadwal;
- hanya satu proses bertanggung jawab atas migrasi;
- endpoint checkpoint/admin dibatasi scope admin.

### J. Deployment inventory tidak konsisten

“Vercel 4/5 OK” hanya menyebut empat nama dan tidak menjelaskan proyek kelima yang gagal. PemdiAcehTengah tidak auto-deploy dari GitHub.

**Perbaikan:** satu deployment manifest machine-readable, status per proyek, alasan gagal, source branch, production SHA, dan rollback target. Gunakan GitHub integration/workflow dengan environment protection daripada token OIDC ad-hoc jika proses organisasi mengizinkan.

### K. Security scan terlalu sempit

“Gitleaks no secrets on brain commit” bukan audit seluruh ekosistem. Jalankan secret scan pada:

- seluruh Git history repo aktif;
- worktree dan untracked files;
- artefak build/log;
- backup USB;
- CI pre-push.

`vault/` yang hanya gitignored bukan vault terenkripsi. Gunakan macOS Keychain, secret manager, atau file terenkripsi dengan permission ketat.

---

## 4. Rekomendasi konfigurasi Hermes

Template aman tersedia di `hermes-hardening-and-integrations.template.yaml`. Prinsip penerapan:

1. Buat backup penuh HERMES_HOME dan catat hash.
2. Jalankan `hermes config check` dan `hermes config migrate`.
3. Terapkan satu blok melalui `hermes config set`, restart, lalu uji.
4. Buat profil terpisah:
   - **interactive-local:** akses host terbatas, `approvals: manual`;
   - **gateway-prod:** Docker per-session, hard-stop loop, allowlist platform;
   - **creative:** Comfy/Eromify, tanpa akses proyek pemerintahan atau secret produksi.
5. Jangan menempatkan secret pada YAML. Gunakan `.env` mode `0600` atau `key_env`.
6. Jangan mengaktifkan semua MCP/toolset pada Telegram. Terapkan least privilege per platform.

### Baseline produksi yang disarankan

- `terminal.backend: docker`;
- `container_persistent: false` untuk isolasi antar-session;
- mount hanya workspace yang sedang dikerjakan;
- `docker_forward_env: []` secara default;
- CPU 2 dan RAM 4 GB sebagai awal pada mesin 4-core/16-GB, lalu ukur;
- `approvals.cron_mode: deny`;
- Tirith fail-closed;
- lazy installs dinonaktifkan setelah dependency dipreinstall;
- loop hard-stop aktif;
- Hermes API bind `127.0.0.1:8642`, bearer key required, tanpa CORS;
- maksimum concurrent runs 2 pada hardware ini;
- database Hermes di internal APFS.

Catatan: pemeriksaan dangerous command Hermes dilewati ketika container dianggap security boundary [S2]. Karena itu jangan melemahkan Docker dengan `--privileged`, mount root filesystem, Docker socket, `--network=host`, atau forwarding semua env.

---

## 5. Analisis semua tautan dan penerapannya

## 5.1 Cloudflare OS

**Apa yang relevan:** Cloudflare OS bukan OS tradisional; ia adalah workspace agen dengan “gadgets”, sandbox, dan Gatekeepers. Gatekeeper membatasi akses per resource, mencatat observasi/aksi, meminta approval untuk side effects, dan dapat mensimulasikan aksi tertunda agar agen tidak berhenti menunggu [S7]. Repository sendiri menyebut v2 masih early access.

**Yang harus diambil:** pola keamanan, bukan seluruh stack Cloudflare Workers.

### Implementasi yang disarankan: Niu Action Broker

Bangun MCP server lokal `niu_action_broker` yang berada di antara Hermes dan layanan sensitif:

```text
Hermes -> MCP Action Broker -> GitHub/Telegram/deploy/config/services
                  |
                  +-> pending_actions + audit evidence + approvals
```

Tool contract minimum:

- `observe_*`: read-only dan resource-scoped;
- `plan_action`: membuat rencana tanpa side effect;
- `submit_action`: membuat record pending dan preview diff;
- `action_status`;
- `approve_action`/`reject_action`: hanya principal/operator;
- `apply_action`: idempotent, hanya setelah approval;
- `cancel_action`.

Setiap record memiliki `action_id`, actor, scope, input hash, preview, cost estimate, expiry, approver, result, dan rollback hint. Jangan memberi ilusi bahwa simulasi sudah diterapkan; UI harus membedakan **simulated/pending/applied/failed**.

**Keputusan:** adaptasi konsep dengan prioritas tinggi. Jangan fork/deploy Cloudflare OS penuh karena akan menciptakan control plane agen kedua dan ketergantungan Workers/Durable Objects.

**Lisensi:** Apache-2.0; pertahankan notice saat mengambil kode.

## 5.2 Dioxus

Dioxus adalah framework Rust lintas web/desktop/mobile dengan hot reload, server functions, dan integrasi axum [S8]. Versi release yang diperiksa adalah 0.7.10.

**Nilai untuk ekosistem:** dapat menjadi klien native ringan untuk Mission Control atau aplikasi baru.

**Kritik penerapan langsung:**

- Mission Control saat ini FastAPI + JavaScript dan belum sehat.
- Rewrite ke Dioxus menambah Rust toolchain, bundling, deployment, dan kemungkinan backend axum kedua.
- Rewrite tidak menyelesaikan port 5200, auth, kontrak API, dan SQLite.

**Keputusan:** defer. Setelah API stabil, buat POC read-only satu halaman yang memanggil `/healthz`, `/api/v1/agents`, dan Hermes `/v1/capabilities` melalui backend Mission Control. Lanjut hanya bila ada target terukur: penggunaan RAM, distribusi native, atau kebutuhan mobile.

**Lisensi:** dual MIT/Apache-2.0.

## 5.3 tdf

`tdf` adalah viewer PDF berbasis terminal/Ratatui dengan asynchronous rendering, search, hot reload, dan backend MuPDF [S9]. Ia **bukan parser ke Markdown** dan TUI visualnya tidak memberi hasil terstruktur yang baik kepada Hermes.

**Kegunaan:** operator manusia yang bekerja di terminal dapat membuka PDF besar dengan cepat.

**Masalah:**

- `LICENSE` berisi AGPL-3.0, sedangkan README menyebut kontribusi akan diperlakukan sebagai MPL-2.0. Ini perlu klarifikasi sebelum menyalin atau memodifikasi kode.
- Maintainer menyatakan tidak menerima kontribusi yang melibatkan AI. Hormati kebijakan ini; jangan mengirim PR buatan agen.

**Keputusan:** jangan integrasikan ke core Hermes. Jika dipakai, pasang binary terpisah untuk viewer manusia dan jangan redistribute/fork sebelum lisensi jelas.

## 5.4 Firecrawl pdf-inspector

Library Rust berlisensi MIT ini mengklasifikasikan PDF menjadi text/scanned/image/mixed, mengekstrak layout-aware Markdown, mendeteksi tabel/kolom/encoding issue, dan mendukung selective OCR [S10]. Release 1.15.0 dipublikasikan 17 Agustus 2026.

**Ini integrasi dengan ROI tertinggi.**

### Penerapan ke Hermes

Alur baru:

1. `detect_pdf` lokal;
2. bila text-based dan encoding sehat → ekstrak Markdown lokal;
3. bila hanya sebagian halaman bermasalah → route halaman tersebut saja;
4. OCR lokal hanya jika runtime telah dipreprovision;
5. hosted OCR hanya dengan persetujuan dan kebijakan data yang sesuai.

Saya telah membuat skill dan helper:

- `hermes-pdf-inspector-skill/SKILL.md`
- `hermes-pdf-inspector-skill/scripts/pdf_inspect.py`

Helper diuji pada PDF sintetis: deteksi dan ekstraksi berhasil serta menghasilkan JSON + Markdown.

**Khusus Mac Intel:** wheel native extraction tersedia, tetapi panduan OCR reproducible upstream tidak menyediakan archive ONNX Runtime 1.27 resmi untuk Intel macOS. Gunakan detect/extract lokal; route scan ke skill OCR yang ada atau worker remote sampai runtime Intel diuji.

**Jangan mengganti semua skill PDF:** skill bawaan `pdf` tetap lebih tepat untuk merge/split/form/enkripsi. `pdf-inspector` menjadi jalur ingest pertama.

## 5.5 ego-lite

`ego-lite` adalah browser Chromium untuk manusia dan agen dengan task Spaces serta akses ke login state. Skill menjalankan JavaScript langsung melalui `ego-browser` [S11]. Mesin pengguna adalah Mac Intel, dan upstream menyediakan build x64.

### Risiko penting

- Skill upstream memerintahkan agar ego-browser diprioritaskan atas built-in browser/fetch untuk hampir semua tugas. Ini terlalu luas.
- Migrasi data Chrome memberi agen akses ke cookies/login bernilai tinggi.
- Installer skill mengunduh DMG lalu menghapus atribut `com.apple.quarantine`; script yang diperiksa tidak memverifikasi checksum yang dipin atau signature sebelum bypass Gatekeeper.

**Keputusan:** pilot bersyarat, bukan default.

**Kontrol wajib:**

1. Jangan jalankan installer otomatis as-is pada profil produksi.
2. Unduh manual dari release/vendor, lalu verifikasi `codesign` dan `spctl`; jangan menghapus quarantine sebagai kebiasaan.
3. Gunakan browser profile khusus “Hermes”, tanpa perbankan, admin cloud, GitHub owner, atau akun pemerintah.
4. Untuk fetch/read-only publik, gunakan `web_extract`/browser Hermes biasa. ego-lite hanya untuk tugas authenticated UI yang memang membutuhkan state browser.
5. Aksi publish, purchase, delete, send, atau form sensitif selalu perlu approval.
6. Tutup Space setelah tugas dan audit riwayat aksi.

Hermes sendiri sudah mempunyai banyak backend browser dan local CDP [S5]. Nilai ego-lite harus dibuktikan lewat benchmark tugas nyata, bukan dipasang karena duplikasi fitur.

**Lisensi:** MIT.

## 5.6 ComfyUI-Krea2-Ostris-Edit

Custom node ini menambahkan text encoding prompt + hingga tiga reference images melalui Qwen3-VL dan model patch untuk Krea 2 edit LoRA [S13]. Tidak ada dependency Python tambahan dan lisensinya MIT.

**Batas penting:**

- Hanya untuk LoRA Krea 2 edit yang dilatih dengan `ai-toolkit` dan `model_kwargs.edit: true`.
- Opsi KV cache hanya benar jika LoRA juga dilatih dengan kwarg `kv_cache`.
- Node/model patch bukan pengganti model weights, encoder, VAE, dan LoRA.
- Lisensi repository node tidak otomatis mencakup lisensi model dan LoRA.

**Keputusan:** worker GPU remote. Intel UHD 620 + RAM 16 GB shared + ruang internal 43,6 GB tidak cocok sebagai host optimal untuk workflow ini.

**Penerapan:**

- Pin ComfyUI stable tag dan custom node ke commit/tag, jangan tracking `master` otomatis.
- Pisahkan environment dan storage model dari Mac.
- Simpan workflow API JSON versioned beserta hash model/LoRA.
- Matikan KV cache secara default.
- Buat acceptance images dengan fixed seeds untuk regression.
- Jangan expose ComfyUI port ke internet tanpa reverse proxy/VPN, auth, TLS, dan upload limits.

## 5.7 ComfyUI

ComfyUI adalah engine node-graph modular dengan REST/WS API, queueing, partial re-execution, model offloading, dan custom nodes [S12]. Release yang diperiksa adalah 0.33.1.

**Temuan penting:** Hermes terkini sudah membundel skill `comfyui` yang menggunakan `comfy-cli` untuk lifecycle dan REST/WebSocket untuk eksekusi. Karena itu tidak perlu membuat integrasi core baru.

**Penerapan optimal:**

1. Aktifkan/audit skill ComfyUI bawaan Hermes.
2. Host ComfyUI pada GPU worker.
3. Mission Control menyimpan job metadata, bukan file model.
4. Hermes mengirim workflow API JSON melalui skill/API.
5. Progress masuk melalui WS dan diringkas ke Mission Control.
6. Output disimpan ke artifact store dengan SHA-256, prompt, seed, workflow hash, model hash, cost, dan retention policy.
7. Custom nodes hanya dari allowlist dan pin commit.

**Lisensi:** ComfyUI GPL-3.0. Menjalankan sebagai service terpisah melalui API lebih bersih daripada menyalin source ke aplikasi proprietary; evaluasi kewajiban distribusi dengan penasihat lisensi bila produk dibagikan. Model memiliki lisensi masing-masing.

## 5.8 Eromify

Eromify menyediakan layanan avatar/image/video dan MCP remote. Endpoint `https://api.eromify.com/mcp` mempublikasikan OAuth metadata dengan scope `read`, `generate`, dan `edit`; website menyatakan MCP tersedia pada paket tertentu [S14].

### Risiko dan tata kelola

- Layanan proprietary dan berbasis kredit.
- Ada fitur mature/adult; harus dipisahkan total dari profil kerja pemerintahan/organisasi.
- Terms melarang penggunaan likeness orang nyata, deepfake, dan upload foto manusia nyata.
- Privacy policy menyebut prompt/media menjalani moderation dan media dapat dikirim ke classifier pihak ketiga; audit trail moderation disimpan.
- Exact tool names tidak dipublikasikan pada halaman yang dapat diakses, sehingga whitelist belum bisa dibuat secara aman.

**Keputusan:** integrasi opsional, default nonaktif.

Template MCP telah ditambahkan dengan:

- `auth: oauth`;
- `trust: untrusted`;
- `enabled: false`;
- `tools.include: []`;
- resources/prompts disabled.

### Tahap pilot

1. Buat profil Hermes `creative` terpisah.
2. Jangan memberinya filesystem proyek sensitif atau Telegram umum.
3. Jalankan `hermes mcp test eromify`, lakukan OAuth, dan inventaris exact tools.
4. Enable hanya tool daftar/balance/history terlebih dahulu.
5. Tambahkan generation satu per satu dengan approval dan spending cap.
6. Hanya gunakan karakter sintetis; tidak boleh ada gambar/wajah orang nyata.
7. Catat AI-generated disclosure, consent, copyright, credit cost, dan output retention.
8. Cabut token jika pilot selesai atau tidak dipakai.

## 5.9 Handy

Handy adalah aplikasi desktop Tauri/Rust + React untuk speech-to-text lokal menggunakan Whisper/Parakeet dan VAD [S15]. Release yang diperiksa adalah 0.9.5; lisensi MIT.

**Nilai:** dictation lintas aplikasi dengan privasi lokal. CLI dapat toggle recording pada instance yang sedang berjalan.

**Mengapa bukan backend Hermes:** Handy memasukkan teks ke field aktif dan tidak menawarkan kontrak transkripsi server yang bersih. Hermes sendiri sudah mempunyai konfigurasi STT lokal/cloud.

**Keputusan:** gunakan sebagai aplikasi pendamping bila dibutuhkan:

- Handy untuk dictation ke aplikasi apa pun;
- Hermes STT untuk voice message Telegram/gateway;
- jangan menjalankan dua hotkey/recording pipeline yang saling bentrok;
- pada Intel 16 GB mulai dari model ringan dan VAD, lalu ukur latency/memory.

## 5.10 Facebook Reel

Tautan `facebook.com/share/r/1Ezpnqx4BX/` mengembalikan akses 403/tidak dapat diambil tanpa sesi Facebook. Pencarian publik juga tidak menemukan isi reel yang dapat diverifikasi.

**Tidak ada kesimpulan yang dibuat dari tautan ini.** Unggah file video, screen recording, atau screenshot + deskripsi tujuan agar dapat dianalisis dan dipetakan ke Hermes.

---

## 6. Arsitektur target

```text
                         +-------------------------+
                         | Mission Control UI      |
                         | browser, no Hermes key  |
                         +-----------+-------------+
                                     |
                              MC auth/session
                                     |
                         +-----------v-------------+
                         | Mission Control API     |
                         | :5200 loopback          |
                         | tasks, costs, audit     |
                         | approvals, artifacts    |
                         +---+----------+----------+
                             |          |
               Hermes bearer|          | artifact metadata
                             |          |
                  +----------v--+   +---v----------------+
                  | Hermes API |   | Local APFS SQLite  |
                  | :8642      |   | + backup/restore   |
                  +--+---+-----+   +--------------------+
                     |   |
         approved MCP|   | sandbox tools
                     |   +---------------------+
          +----------v-----------+             |
          | Niu Action Broker    |      +------v-------+
          | capability + audit   |      | Docker       |
          | pending/sim/apply    |      | per session  |
          +-----+-----------+----+      +--------------+
                |           |
       +--------v--+   +----v----------------+
       | Eromify  |   | GitHub/Telegram/etc |
       | optional |   | scoped connectors   |
       +-----------+  +---------------------+

                  +----------------------------+
                  | Remote ComfyUI GPU worker  |
                  | pinned workflows/nodes     |
                  +----------------------------+
```

Prinsipnya: **Hermes berpikir dan mengorkestrasi; broker membatasi side effects; Mission Control mengawasi; worker melakukan komputasi berat.**

---

## 7. Roadmap implementasi

## P0 — 0–2 hari: stabilisasi dan keamanan

- Backup HERMES_HOME, Mission Control DB, skill manifests, dan config; uji restore.
- Pindahkan live state/SQLite ke internal APFS.
- Perbaiki Mission Control startup dan pasang `launchd`.
- Tambah `/healthz`, `/readyz`, `/version`.
- Wajibkan MC auth, WS auth/origin, dan API key Hermes terpisah.
- Jalankan `hermes config check`, `hermes config migrate`, `hermes doctor`.
- Verifikasi SIP/FileVault/Gatekeeper; aktifkan SIP bila tidak ada dependensi sah.
- Hentikan sinkronisasi skill sampai perbedaan 47/211/2 dipahami.

## P1 — 3–7 hari: kontrak dan efisiensi

- Hubungkan Mission Control ke API publik Hermes (`/v1/capabilities`, Runs, SSE, health).
- Contract-test frontend terhadap OpenAPI.
- Buat model acceptance suite dan kurangi fallback menjadi 2–3.
- Instal skill `pdf-inspector-local` pada environment uji.
- Tambah observability: request ID, task ID, provider/model, latency, retries, fallback, tool count, cost estimate, error class.
- Daftarkan remote privat untuk `latticesend`.

## P2 — minggu 2–3: integrasi terkendali

- Implementasikan MVP Niu Action Broker dengan read-only tools + pending action ledger.
- Siapkan worker ComfyUI remote dan gunakan skill Hermes bawaan.
- Pin workflow Krea 2 dan custom node; fixed-seed regression.
- Pilot ego-lite dengan browser profile khusus, tanpa login sensitif.
- Pilot Eromify pada profil `creative`, read-only dahulu.

## P3 — setelah SLO stabil

- POC Dioxus read-only; putuskan berdasarkan metrik, bukan tren teknologi.
- Handy sebagai dictation companion bila memberi manfaat nyata.
- tdf hanya untuk operator manusia jika diperlukan.
- Analisis Facebook Reel setelah media diberikan.

---

## 8. Checklist acceptance akhir

Sistem baru hanya dianggap optimal jika seluruh poin berikut lulus:

### Reliability

- Mission Control dan Hermes kembali hidup otomatis setelah reboot/crash.
- `/healthz` dan `/readyz` memiliki semantics berbeda dan termonitor.
- Tidak ada live DB pada USB/NTFS/ExFAT.
- Backup harian dan restore drill berhasil.

### Security

- Request tanpa key ke MC/Hermes/WS gagal 401/403.
- CORS hanya origin eksplisit; Hermes tidak perlu CORS jika diproxy MC.
- Platform user allowlist aktif; tidak ada `ALLOW_ALL_USERS`.
- SIP aktif kecuali exception terdokumentasi.
- Secret file mode `0600`; secret scan seluruh repo/history lulus.
- Container tidak mount Docker socket, root filesystem, atau env global.

### Agent quality

- Primary + fallback lulus tool/JSON/context/error tests.
- Simulasi 429/5xx membuktikan failover.
- Hard-stop mencegah loop tanpa membunuh workflow normal.
- Skill inventory per target cocok dengan manifest/hash.

### Integrations

- PDF text-based diproses lokal dan menghasilkan Markdown valid.
- Scanned pages diroute selektif, bukan OCR seluruh dokumen.
- Comfy job memiliki workflow/model/output hashes dan dapat dibatalkan.
- Eromify tidak dapat generate sebelum tool whitelist, approval, dan budget aktif.
- Browser automation tidak menggunakan profile login utama.

### API/UI

- OpenAPI contract test lulus.
- Frontend tidak bergantung pada response v3 yang belum didukung.
- SSE reconnect, cancellation, idempotency, dan stale-job recovery diuji.
- Cost dashboard diberi label estimate jika belum memasukkan auxiliary/retry/cache.

---

## 9. Artefak yang disertakan

1. `analisis-dan-rencana-optimalisasi-hermes-2026-08-18.md` — laporan ini.
2. `hermes-hardening-and-integrations.template.yaml` — template merge konfigurasi, bukan replacement.
3. `hermes-and-mission-control.env.template` — daftar env tanpa secret.
4. `hermes-pdf-inspector-skill/` — skill Hermes + helper Python yang telah diuji.

### Data yang dibutuhkan untuk audit tahap berikutnya

- `~/.hermes/config.yaml` yang sudah direduksi/redacted;
- output `hermes --version`, `hermes config check`, `hermes doctor`;
- `server.py`, `backend/app/main.py`, dan OpenAPI JSON Mission Control;
- log startup Mission Control dan status `launchctl`;
- lokasi aktual Mission Control DB dan Hermes `state.db`;
- manifest 47/211/2 skills;
- konfigurasi 9router tanpa secret;
- file/screenshot Facebook Reel.

---

## 10. Sumber utama

- **[S1] Hermes configuration:** https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- **[S2] Hermes security:** https://hermes-agent.nousresearch.com/docs/user-guide/security
- **[S3] Hermes API server:** https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
- **[S4] Hermes MCP guide/reference:** https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes dan https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference
- **[S5] Hermes browser automation:** https://hermes-agent.nousresearch.com/docs/user-guide/features/browser
- **[S6] Hermes skills:** https://hermes-agent.nousresearch.com/docs/guides/work-with-skills
- **[S7] Cloudflare OS/Gatekeepers:** https://github.com/cloudflare/cloudflare-os dan https://github.com/cloudflare/cloudflare-os/blob/main/.agents/skills/write-gatekeeper/SKILL.md
- **[S8] Dioxus:** https://github.com/dioxuslabs/dioxus
- **[S9] tdf:** https://github.com/itsjunetime/tdf dan https://github.com/itsjunetime/tdf/blob/main/LICENSE
- **[S10] pdf-inspector:** https://github.com/firecrawl/pdf-inspector dan https://github.com/firecrawl/pdf-inspector/releases/tag/v1.15.0
- **[S11] ego-lite:** https://github.com/citrolabs/ego-lite dan https://github.com/citrolabs/ego-lite/blob/main/skills/ego-browser/references/install.md
- **[S12] ComfyUI:** https://github.com/comfy-org/comfyui dan https://github.com/comfy-org/comfyui/tree/master/script_examples
- **[S13] Krea 2 Ostris Edit node:** https://github.com/ostris/ComfyUI-Krea2-Ostris-Edit
- **[S14] Eromify MCP/policies:** https://www.eromify.com/mcp, https://api.eromify.com/.well-known/oauth-protected-resource, https://www.eromify.com/privacy, dan https://www.eromify.com/acceptable-use
- **[S15] Handy:** https://github.com/cjpais/Handy

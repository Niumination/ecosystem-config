# RISET: openai/plugins & openai/skills — penilaian adopsi ekosistem Niumination

Tanggal pengambilan data: 2026-11-25 21:41 WIB. Mode: **pelajari** — baca + verifikasi + lapor + tunggu instruksi. Tidak ada plugin/skill yang dipasang, diaktifkan, atau disalin ke bank pada sesi ini. Satu-satunya perubahan adalah laporan ini.

## Ringkasan eksekutif

- `openai/skills` **sudah deprecated** oleh pemiliknya; README menunjuk `openai/plugins` sebagai pengganti. Tidak layak jadi basis adopsi baru.
- `openai/plugins` aktif dan besar (65 plugin di marketplace, 541 berkas `SKILL.md`), tetapi **bukan paket plug-and-play untuk Hermes**: manifest Codex (`.codex-plugin/plugin.json`) berbeda dengan format Hermes (`plugin.yaml` / Agent Plugins v1 `plugin.json` dengan `$schema agent-plugins.org`).
- Jawaban atas "apakah bisa diadopsi": **bisa, secara selektif dan manual — skill individualnya saja**, bukan plugin bundle, bukan hooks, bukan konfigurasi MCP. Dari 523 nama skill unik di repo plugins, **20 sudah ada di bank kita** (sebagian memang ber-source superpowers/Remotion).
- Risiko nyata: tidak ada lisensi repo tingkat atas (lisensi per skill/plugin, termasuk 8 `Proprietary`, 1 `UNLICENSED`, 1 `GPL-3.0-only`), 4 manifest MCP menyimpan `client_secret`, dan hooks dapat menjalankan perintah otomatis. Semua itu bertabrakan dengan aturan keras ekosistem (approval gate, kredensial hanya di env/vault).
- Rekomendasi praktis: **jangan install apa pun dulu**. Ambil maksimal 3 skill sebagai uji gate bila ada perintah `gas` eksplisit.

## Arsitektur

### openai/plugins (aktif)
- Commit yang dipelajari: `981b02c` (2026-11-18 11:14 -0800), 5.459 berkas terlacak, ~95 MB.
- Struktur: `plugins/<nama>/.codex-plugin/plugin.json` (manifest wajib), dengan permukaan opsional `skills/`, `.app.json`, `.mcp.json`, `agents/`, `commands/`, `hooks.json`, `assets/`.
- Dua marketplace: `.agents/plugins/marketplace.json` (65 entri) dan `.agents/plugins/api_marketplace.json` untuk pengguna login API. Tiap entri membawa `policy.installation` dan `policy.authentication` (mis. `AVAILABLE` / `ON_INSTALL`) serta kategori.
- 65 plugin: 27 Developer Tools, 12 Productivity, 9 Creativity, 5 Communication, 4 Education & Research, 3 Data & Analytics, 2 Finance, 1 Security, 1 Business & Operations, 1 Scientific Research.
- Contoh manifest kaya: `figma` (`skills`, `apps`, `interface`, `license: LicenseRef-Figma-Developer-Terms`), `codex-security` (MCP + biner native `.node`), `github` (MCP OAuth).

### openai/skills (deprecated)
- Commit yang dipelajari: `49f948f` (2026-06-23), 783 berkas, ~7,8 MB.
- 44 berkas `SKILL.md`: 1 di `.system`, 43 di `.curated`, 0 di `.experimental`. Lisensi per direktori (`LICENSE.txt`).
- Cara pakai resminya pun `$skill-installer` di dalam Codex + restart Codex; tidak ada mekanisme instalasi untuk Hermes.

## Fitur yang menonjol

- 541 berkas `SKILL.md` di repo plugins (523 nama unik setelah deduplikasi) — mencakup domain web, mobile, desain, data, keamanan, sains, dan produktivitas.
- 31 berkas `.mcp.json` dengan 19 host Google API dominan, diikuti Figma, Linear, Notion, Shopify, Cloudflare, Datadog, dll.
- 1 `hooks.json`: `figma` menjalankan `./scripts/post_write_figma_parity_check.sh` pada `PostToolUse` untuk `Write|Edit`.
- 64 manifest plugin dengan field lisensi: MIT 37, tanpa field 11, Proprietary 8, Apache-2.0 2, serta masing-masing 1 untuk GPL-3.0-only, Apache-2.0 AND CC-BY-4.0, LicenseRef-Figma-Developer-Terms, UNLICENSED.
- Pola desain yang menarik: deklarasi `policy.installation` + `policy.authentication` di marketplace, dan pemisahan jelas antara skill (instruksi), app (UI), MCP (konektor), dan hooks (automasi).

## Relevansi ke ekosistem (bandingkan dengan yang sudah ada)

Data live ekosistem (eco-guard verify, 2026-11-25 21:41 WIB): **bank 270 skill, runtime 482 skill**.

- **Sudah ada / duplikat:** 20 nama skill di repo plugins juga ada di bank: `brainstorming`, `finishing-a-development-branch`, `requesting-code-review`, `subagent-driven-development`, `systematic-debugging`, `verification-before-completion`, `writing-plans`, 12 skill `remotion-*`, dan `hyperframes`. Bank memiliki catatan `source: superpowers` untuk 7 skill pertama, jadi ini memang bukan penemuan baru.
- **Fungsi sudah dicakup pipeline/penyedia existing:** konektor GitHub, Airtable, Notion, Google Workspace, Vercel, X, PDF, Playwright, screenshot, dan document pipeline sudah ada di bank/plugin (`rea`, `camofox`, `rtk-rewrite`, `niu-core-fence` aktif di config). Marketplace `vercel` (54 skill unik) sebagian besar adalah dokumentasi AI SDK/Vercel yang tidak kita butuhkan untuk stack Flutter/Dart saat ini.
- **Gap yang benar-benar relevan (kandidat, belum diambil):**
  - `plugin-eval`: `evaluate-skill`, `improve-skill`, `metric-pack-designer` — berpotensi menguatkan gate skill bank kita yang selama ini mengandalkan `skill_lint.py`/`skill_scanner.py` + eval upstream.
  - `test-android-apps`: `android-emulator-qa`, `android-performance` — relevan dengan `presensi_rekon/` yang sedang diuji di perangkat Infinix X6873.
  - `build-web-data-visualization`: 18 skill visualisasi (termasuk `accessibility-and-inclusive-visualization`, `dashboards-and-real-time-visualization`) — relevan dengan MIRAI/Mission Control, tetapi harus diuji tumpang-tindih dengan `design/accessibility`, `ui-ux-pro-max`, `baoyu-infographic`.
  - `build-macos-apps`: 11 skill Swift/AppKit — relevan untuk alat Mac, bukan prioritas saat ini.
- **Tidak relevan / dibuang:** life-science-research (50), public-equity-investing (23), NGS (18), twilio (55), zoom (40), shopify (20), nvidia (12) — di luar mandat Diskominfo/content/ekosistem saat ini.

## Keamanan

- **Lisensi:** tidak ada `LICENSE` di root kedua repo (`gh api ... --jq .license` → `null`). Lisensi bersifat per-plugin/per-skill. `MIT` dominan, tetapi ada `Proprietary` (8), `UNLICENSED` (1), `GPL-3.0-only` (1), dan `LicenseRef-Figma-Developer-Terms` (1). Tidak boleh menyalin massal; setiap kandidat harus dicek lisensinya satu per satu.
- **Kredensial:** 4 dari 31 `.mcp.json` mengandung field `client_secret` OAuth. Ini bukan rahasia pribadi, tetapi menempelkan pola itu ke config kita melanggar kebiasaan "kredensial hanya via env/vault". Konfigurasi MCP tidak boleh disalin verbatim.
- **Eksekusi otomatis:** hooks bersifat `command` dan berjalan pada `PostToolUse` (contoh figma). Ini bertentangan dengan approval gate Niumination; jangan aktifkan hooks dari repo ini.
- **Permukaan kode:** dari 535 berkas script (`.sh/.py/.js/.ts`), 140 mengandung pola network dan 62 mengandung pola exec. Klaim "hanya instruksi" tidak berlaku untuk bundle secara keseluruhan.
- **Biner native:** `codex-security` membundling `mcp/native/*/unix.node` untuk 8 target platform. Berat, tidak transparan, dan perlu verifikasi terpisah sebelum dipercaya.
- **Isi skill:** contoh `figma-design-to-code` memakai instruksi imperatif keras ("MANDATORY prerequisite ... MUST invoke ..."). Itu gaya prompt vendor; tidak boleh masuk ke prompt produksi kita tanpa adaptasi ke aturan lokal.
- **Format frontmatter:** skill Codex memakai `name`, `description` panjang, `disable-model-invocation`. Bank kita mewajibkan `description` ≤60 karakter berformat `Use when ...`, `license`, `source: <repo> — <owner>`, dan blok `metadata`. Jadi `ship-verbatim ≠ adopt-verbatim`.

## Persyaratan di mesin ini

- Clone sudah berada di direktori sementara (bukan instalasi): `$TMPDIR/niu-adopt-openai-20261125/{plugins,skills}`. Tidak ada `npm install`, `npx`, `hermes plugins install`, atau perubahan config yang dilakukan.
- Hermes mengenal dua bentuk plugin: `plugin.yaml` (contoh `camofox`) dan Agent Plugins v1 `plugin.json` dengan `$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` (contoh `rea`). Manifest Codex ada di `.codex-plugin/plugin.json`, tidak memakai `$schema` itu, dan memakai field `interface`, `skills`, `apps` alih-alih `provides_tools`/`capabilities`.
- Konsekuensi: paket Codex **tidak langsung bisa dipasang** via `hermes plugins install`. Penilaian ini berdasarkan perbandingan manifest nyata; belum diuji dengan `hermes plugins validate` (tidak dijalankan karena mode pelajari).

## Penilaian

| Jalur | Verdict | Alasan |
|---|---|---|
| Pasang seluruh repo `openai/plugins` sebagai plugin | Tolak | Format manifest beda, 95 MB, hooks/MCP/secret surface, lisensi campuran |
| Adopsi `openai/skills` | Tolak | Deprecated oleh upstream, 20 skill tumpang tindih, tidak ada mekanisme Hermes |
| Ambil skill individual terpilih | Bisa, selektif | Perlu lisensi jelas, scan network/exec, adaptasi frontmatter, gate lint/eval |
| Tiru pola `policy.installation` + `policy.authentication` | Bisa, tanpa kode | Cocok untuk dokumentasi registry, bukan integrasi runtime |
| Salin hooks / `.mcp.json` | Tolak | Approval gate + aturan kredensial |

## Rekomendasi (belum dieksekusi)

1. Tidak ada tindakan instalasi sampai ada perintah `gas` eksplisit.
2. Jika disetujui, uji hanya 3 kandidat: `plugin-eval/evaluate-skill`, `test-android-apps/android-emulator-qa`, `build-web-data-visualization/accessibility-and-inclusive-visualization`. Untuk tiap kandidat: cek lisensi file, baca isi lengkap, scan `requests.|urllib|socket|subprocess|os.system`, ubah frontmatter ke format bank, jalankan gate `skill_lint.py --strict` + `skill_scanner.py` + eval bila ada, baru salin ke `skills/<domain>/`.
3. Jangan pernah membawa `hooks.json`, `.mcp.json`, atau biner native dari bundle ini ke dalam ekosistem.
4. Catat pola kebijakan instalasi/autentikasi marketplace sebagai referensi dokumentasi, bukan sebagai kode yang dijalankan.

## Sumber

- https://github.com/openai/plugins — commit `981b02c` (2026-11-18), clone lokal `$TMPDIR/niu-adopt-openai-20261125/plugins`
- https://github.com/openai/skills — commit `49f948f` (2026-06-23), clone lokal `$TMPDIR/niu-adopt-openai-20261125/skills`
- `gh api repos/openai/plugins` dan `gh api repos/openai/skills` (lisensi `null` pada level repo)
- `bash ~/.hermes/scripts/eco-guard.sh verify` — angka bank/runtime skill (2026-11-25 21:41 WIB)

## Bukti

- `git clone --depth 1` kedua repo → exit 0; `git log -1 --format=...` → `plugins 981b02c 2026-11-18`, `skills 49f948f 2026-06-23`
- `du -sh` → `95M plugins`, `7.8M skills`; `git ls-files | wc -l` → `5459` dan `783`
- `git -C plugins ls-files | grep -c 'SKILL.md$'` → `541`; repo skills → `44`; `grep -c 'plugin.json$'` → `64`; `grep -c 'hooks.json$'` → `1`; `grep -c 'mcp.json$'` → `31`
- Analisis Python dari `git ls-files` → 523 nama skill unik, overlap dengan bank 20, overlap dengan runtime 21, overlap repo skills dengan bank 0; distribusi lisensi 37 MIT / 11 tanpa field / 8 Proprietary / 2 Apache-2.0 / 1 masing-masing untuk 4 tipe lain
- Scan 535 berkas script → 140 mengandung pola network, 62 pola exec; 4 dari 31 `.mcp.json` mengandung `client_secret` (nilai tidak dikutip)
- `eco-guard.sh verify` → `[ INFO ] runtime: 482 skill · bank: 270 skill`, exit code 1 karena temuan `PERIKSA` lain (bukan kegagalan pembacaan angka)
- `read_file README.md` repo skills baris 1-2 → pernyataan `This repository is deprecated`

## Lampiran — hasil uji 3 kandidat (2026-11-25 21:55 WIB)

Mode uji: **read-only** di clone `$TMPDIR/niu-adopt-openai-20261125/`. Tidak ada `npm install`, tidak ada salinan ke bank, tidak ada perubahan config. `git status --short` clone = 0 baris sebelum dan sesudah semua uji.

### Hasil per kandidat

| Kandidat | Lisensi | Gate bank (`skill-audit.py`) | Uji fungsional | Nilai `plugin-eval analyze` | Verdict uji |
|---|---|---|---|---|---|
| `plugin-eval/evaluate-skill` | MIT (plugin) | 1 finding `self-mod` — false positive: tautan ke `../improve-skill/SKILL.md` | CLI `plugin-eval` jalan langsung dari checkout dengan Node v26.7.0, tanpa install | 95/100 A | Menjanjikan sebagai alat uji lokal; skill-nya sendiri perlu rewrite (asumsi `~/.codex/skills` dan perintah Codex) |
| `test-android-apps/android-emulator-qa` | MIT (plugin), Apache-2.0 (skill) | 0 finding | 2 helper Python lulus compile + uji fungsional dengan UI dump sintetis | 72/100 C, risk high | Helper layak dipelajari; instruksi memakai Gradle, sedangkan `presensi_rekon/` Flutter → harus disesuaikan |
| `build-web-data-visualization/accessibility-and-inclusive-visualization` | MIT (plugin) | 1 finding `url` (`colorbrewer2.org`) — benign | 13/13 referensi relatif ada | 72/100 C, risk high | **Skip**: tumpang tindih dengan `design/accessibility` + `web-accessibility-wcag`, description 339 char, alur approval image-generation ala Codex tidak relevan |

### Detail uji

- Frontmatter ketiga kandidat hanya memuat `name` + `description`, dengan panjang description masing-masing **80 / 140 / 339 karakter** — semua melebihi batas 60 karakter bank. Adopsi apa pun wajib melalui rewrite frontmatter (`license`, `source`, `metadata`, `description` baru).
- Pemeriksaan tautan: `evaluate-skill` 2/2 dan `accessibility-and-inclusive-visualization` 13/13 referensi relatif resolve. Dua kemunculan `./gradlew` pada skill Android yang terdeteksi "missing" adalah **false positive** parser regex — itu perintah build, bukan tautan dokumen.
- Helper Android (`ui_pick.py`, `ui_tree_summarize.py`) hanya mengimpor `re`, `sys`, `xml.etree.ElementTree`, `pathlib`; tidak ada network/exec. Uji dengan UI dump sintetis: `ui_pick.py ... Settings` → `200 230` (exit 0), ringkasan UI_tree menghasilkan 2 baris (exit 0), target tidak ada → exit 2. Catatan `plugin-eval`: helper Python tanpa `test_*.py` dan satu fungsi dengan kompleksitas tinggi.
- CLI `plugin-eval` tersedia sebagai `scripts/plugin-eval.js` di clone (`package.json` `private: true`, bin tanpa dependency install). Perintah `analyze` dijalankan dari `$TMPDIR`, tidak menulis ke clone. Skor di atas berbasis **baseline Codex dan estimasi token statis** — berguna sebagai sinyal relatif, bukan audit definitif.
- Perbandingan internal: skill bank kita `design/accessibility` mendapat 53/100 F dari alat yang sama karena satu tautan relatif rusak (`../web-quality-audit/SKILL.md`, direktori memang tidak ada). Ini temuan samping; **tidak diperbaiki** karena di luar permintaan uji kandidat.

### Keputusan uji

Belum ada adopsi. Jika dilanjutkan, urutan yang paling masuk akal: (1) pakai CLI `plugin-eval` dari checkout lokal sebagai pembantu gate, tanpa menjadikannya skill bank; (2) baru evaluasi `android-emulator-qa` setelah disesuaikan untuk Flutter; (3) `accessibility-and-inclusive-visualization` tidak diambil.

### Bukti tambahan

- `python3 ~/Desktop/Niumination/scripts/skill-audit.py --bank <plugin>/skills --skill <nama> --count` → `1 / 0 / 1`, exit 0 semua
- `python3 -c "compile(...)"` kedua helper → `COMPILE_OK`; `python3 ui_pick.py ui.xml Settings` → `200 230`, exit 0; target tidak ada → exit 2
- `node "$TMPDIR/.../plugin-eval.js" --help` → exit 0; `analyze <path> --format markdown` → exit 0 untuk 5 target (3 kandidat + `opencode-troubleshooting` + `design/accessibility`)
- `grep -E 'Score:|Grade:|Risk:'` pada laporan analyze → `android 72/100 C`, `evaluate-skill 95/100 A`, `accessibility 72/100 C`, bank `design/accessibility 53/100 F`
- `find skills -type d -name web-quality-audit` → kosong; `grep -n web-quality-audit skills/design/accessibility/SKILL.md` → baris 439
- `git -C <clone> status --short | wc -l` → `0` sebelum dan sesudah uji

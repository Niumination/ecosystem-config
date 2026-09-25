# Registry Thread Telegram — Niu-MissionControl

Group: `Niu-MissionControl` (`-1004204696417`) · platform: telegram · chat_type: group (forum topics)

Setiap thread = persona terisolasi. Sumber kebenaran: `~/.hermes/config.yaml` → `platforms.telegram` (`channel_overrides` + `extra.channel_prompts` + `extra.channel_skill_bindings`). Routing session live ada di `~/.hermes/state.db` → tabel `gateway_routing`.

## Thread aktif

| Thread | Persona | Model | Provider | Skill binding | Catatan |
|--------|---------|-------|----------|---------------|---------|
| `1` | General / Command Center | `inclusionai/ling-3.0-flash-fin:free` | nous | — | pusat koordinasi; dispatch ke thread lain via `POST localhost:5200/api/mc/dispatch` |
| `802` | Research / Riset | `inclusionai/ling-3.0-flash-sante:free` | nous | — | riset, sintesis, laporan |
| `803` | Builder / Programmer | `meituan/longcat-2.0:free` | nous | `ponytail`, `requesting-code-review` | ⚠️ `:free` sudah 404 di nous (25 Sep 2026) — belum diganti |
| `804` | QA / Pengawas | `deepseek/deepseek-v4-flash-0731:free` | openrouter | `codebase-audit` | audit, kepatuhan |
| `1172` | Kreator / Konten | `poolside/laguna-s-2.1:free` | nous | `ghost`, `humanizer` | konten publik |
| `7402` | Cron / Otomasi | `meituan/longcat-2.0:free` | nous | — | routing output cron; ⚠️ `:free` sudah 404 di nous (25 Sep 2026) — belum diganti |
| **`8853`** | **ASN — Admin Dinas** (25 Sep 2026) | `opencode-combo` | **9router** | `skp-e-kinerja`, `document-to-action-items`, `meeting-action-items`, `weekly-review-planning` | administrasi dinas, SKP/eKinerja, agenda rapat/tenggat |

## Thread 8853 — ASN / Admin Dinas

Dibuat 25 Sep 2026 atas permintaan pemilik untuk pekerjaan ASN (Pranata Komputer Diskominfo Aceh Tengah).

- **Fokus:** administrasi dinas harian (surat, dokumen, notulensi rapat), kinerja ASN (SKP/eKinerja: target, capaian, bukti), agenda dinas (rapat, tenggat, tugas), dukungan Pemdi/SPBE bila diminta
- **Model:** `9router/opencode-combo` — teruji 8/8 stress test (payload Bahasa Indonesia tema ASN, 25 Sep 2026) + probe gateway 200. Bukan combo model yang dilarang; ini nama model eksplisit di katalog 9router.
- **Prompt:** persona 3 blok mengikuti pola thread lain (persona + ATURAN DOKUMEN + KREDENSIAL), 1.822 char
- **Pemasangan:** script `/tmp/pasang-thread-tls.py` (backup config otomatis + validasi parse + rollback). Konfig selesai 15:01 WIB, pesan konfirmasi terkirim ke thread (exit 0).

## Catatan

- **Model `:free` nous kadang dicabut tanpa peringatan.** Diverifikasi 25 Sep 2026: `meituan/longcat-2.0:free` → HTTP 404 ("no longer free"). Thread 803 & 7402 masih memakainya di config — ganti saat thread itu dipakai lagi.
- **Pembuatan topik forum** hanya bisa dari Telegram (`/newtopic`) — bot API butuh akses token yang tidak diberikan ke agent. Setelah topik ada, kirim 1 pesan agar gateway mendaftarkan routing-nya, baru config bisa dipasang.
- **`skp-e-kinerja` ada di skill bank Niumination + built-in Hermes** (MD5 identik, sinkron).

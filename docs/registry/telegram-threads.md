# Registry Thread Telegram — Niu-MissionControl

Group: `Niu-MissionControl` (`-1004204696417`) · platform: telegram · chat_type: group (forum topics)

Setiap thread = persona terisolasi. Sumber kebenaran: `~/.hermes/config.yaml` → `platforms.telegram` (`channel_overrides` + `extra.channel_prompts` + `extra.channel_skill_bindings`). Routing session live ada di `~/.hermes/state.db` → tabel `gateway_routing`.

## Thread Topology (2026-10-05)

8 thread aktif via satu gateway Hermes. Setiap thread punya `channel_overrides` (model+provider) dan `channel_prompts` (system prompt) di `~/.hermes/config.yaml`.

| Thread | Role | Model | Provider | MSgs | Prompt | Skills Binding |
|--------|------|-------|----------|------|--------|----------------|
| DM | Personal | `opencode-combo` | 9router | ~100 | (default, none) | — |
| 1 | General / Command Center | `opencode-combo` | 9router | ~100 | ✅ Dispatch to 802/803/804/1172 | clarify, session_search, brainstorming, project-orientation |
| 802 | Research | `inclusionai/ling-3.0-flash-sante:free` | nous | ~240 | ✅ Research-focused | arxiv, blogwatcher, notebooklm, llm-wiki, youtube-content |
| 803 | Builder | `kr/deepseek-3.2` | 9router | ~15 | ✅ Coding-focused | ponytail, requesting-code-review, github-pr-workflow, dll. |
| 804 | QA | `nvidia/nemotron-3-super-120b-a12b:free` | openrouter | ~10 | ✅ Audit-focused | codebase-audit, verification, plan-compliance, redteam |
| 1172 | Kreator | `inclusionai/ling-3.0-flash-fin:free` | nous | ~146 | ✅ Content creation | ghost, humanizer, baoyu, claude-design, manim, hyperframes |
| 7402 | Serbaguna | `inclusionai/ling-3.0-flash-fin:free` | nous | ~3 | ✅ Flex-thread prompt (27 Sep 2026) | ❌ None |
| 12707 | Edu Content | `inclusionai/ling-3.0-flash-fin:free` | nous | 0 | ✅ Edu-content pipeline (4/4 bab) | document-content-pipeline, markitdown, remotion-video, ghost, humanizer |
| 8853 | ASN | `sensenova-6.8-flash-lite` | huancheng | ~357 | ✅ ASN/SPBE-focused | skp-e-kinerja + 3 builtin productivity (tanpa entri bank) |

## Flex-Thread Convention (NOT in channel_prompts)

**User treats threads as flexibly-assignable, not role-restricted.** When DM is busy, user works in any available thread on any repo. This is load balancing, not role-based routing. Thread `channel_prompts` document *primary* roles, but they are conventions, not enforcement.

This means:
- Working on `apps/PemdiAcehTengah` in DM main (#General) is valid — same as in thread 804 or 8853
- There is NO technical guard preventing cross-thread work — only documentation says "this is what thread 803 does"
- If enforcement becomes necessary in the future, it requires an external wrapper (`scripts/thread-scope-guard.sh`), not config.yaml

See skill `telegram-router-orchestration` → "Thread Topology" section for current issues and `up-eco` → "Phase 10: Thread Topology Audit" for automated detection.

## Cross-Thread Dispatch

MC OFF. Dispatch via `scripts/dispatch-to-thread.py`:

```bash
python3 scripts/dispatch-to-thread.py <thread_id> "<message>"
```

Token dari `~/.hermes/.env`. User baca hasil langsung dari thread atau forward ke DM. Bot API tidak bisa baca message bot sendiri di forum topic (terverifikasi: `getUpdates` 0, webhook kosong).

## Scripts

- `scripts/telegram_threads.py` — menampilkan status 8 thread dengan model, provider, message count, last activity
- `scripts/check-telegram-threads.sh` — ringkasan status untuk integrasi dengan `/up-eco`
- `scripts/dispatch-to-thread.py` — kirim pesan ke thread mana pun via Bot API (cross-thread dispatch)
- `scripts/rename-telegram-threads.py` — rename forum topics + set custom emoji icons via Bot API

## Thread aktif

| Thread | Persona | Model | Provider | Skill binding | Catatan |
|--------|---------|-------|----------|---------------|---------|
| `1` | General / Command Center | `opencode-combo` | 9router | — | pusat koordinasi; dispatch ke thread lain via `python3 scripts/dispatch-to-thread.py <thread_id> "<msg>"` |
| `802` | Research | `inclusionai/ling-3.0-flash-sante:free` | nous | — | riset, sintesis, laporan. 5 Okt 2026: renamed + icon |
| `803` | Builder | `kr/deepseek-3.2` | 9router | `ponytail`, `requesting-code-review` | 3 Okt 2026: model diubah dari `meituan/longcat-2.0:free` (404) ke `kr/deepseek-3.2` via 9router. 5 Okt 2026: renamed + icon |
| `804` | QA | `nvidia/nemotron-3-super-120b-a12b:free` | openrouter | `codebase-audit` | 3 Okt 2026: model diubah dari `deepseek/deepseek-v4-flash-0731:free` ke `nvidia/nemotron-3-super-120b-a12b:free`. 5 Okt 2026: renamed + icon |
| `1172` | Kreator | `inclusionai/ling-3.0-flash-fin:free` | nous | `ghost`, `humanizer` | 3 Okt 2026: model diubah dari `poolside/laguna-s-2.1:free` ke `inclusionai/ling-3.0-flash-fin:free`. 5 Okt 2026: renamed + icon |
| `7402` | Serbaguna | `inclusionai/ling-3.0-flash-fin:free` | nous | — | 3 Okt 2026: model diubah dari `meituan/longcat-2.0:free` (404) ke `inclusionai/ling-3.0-flash-fin:free`; prompt flex-thread dipasang 27 Sep 2026. 5 Okt 2026: renamed + icon |
| **`12595`** | **Cron & Otomasi** | `inclusionai/ling-3.0-flash-fin:free` | **nous** | — | Thread khusus output cronjob. Dibuat 5 Okt 2026 untuk memisahkan cron output dari flex-thread 7402. Renamed + icon. |
| `8853` | **ASN** | `sensenova-6.8-flash-lite` | **huancheng** | `skp-e-kinerja`, `document-to-action-items`, `meeting-action-items`, `weekly-review-planning` | administrasi dinas, SKP/eKinerja, agenda rapat/tenggat. **Tidak di-rename** (sudah sesuai). |
| `12707` | **Edu Content** | `inclusionai/ling-3.0-flash-fin:free` | **nous** | `document-content-pipeline`, `markitdown`, `remotion-video`, `ghost`, `humanizer` | Konten edukasi: PDF buku → web book interaktif bernarasi (adaptasi pipeline Papermorph). Dibuat 6 Okt 2026. Progress: 4/4 bab selesai (ch01-04, 1.5 MB site), deploy CF Pages pending. |

## Thread 8853 — ASN / Admin Dinas

Dibuat 25 Sep 2026 atas permintaan pemilik untuk pekerjaan ASN (Pranata Komputer Diskominfo Aceh Tengah).

- **Fokus:** administrasi dinas harian (surat, dokumen, notulensi rapat), kinerja ASN (SKP/eKinerja: target, capaian, bukti), agenda dinas (rapat, tenggat, tugas), dukungan Pemdi/SPBE bila diminta
- **Model:** `huancheng/sensenova-6.8-flash-lite` — ditetapkan 27 Sep 2026 atas permintaan pemilik, **tanpa fallback** (fallback model di Hermes bersifat global, bukan per-thread, sehingga membangun fallback khusus untuk thread ini = modifikasi core framework). Sebelumnya `9router/opencode-combo` (teruji 8/8 stress test payload Bahasa Indonesia tema ASN, 25 Sep 2026) — note: runtime ternyata sudah lama berjalan di huancheng, jadi ini menambal drift config-vs-reality.
- **Prompt:** persona 3 blok mengikuti pola thread lain (persona + ATURAN DOKUMEN + KREDENSIAL), 2.019 char. **27 Sep 2026:** instruksi dispatch endpoint MC (`localhost:5200`) dihapus — MC bukan daemon persisten sehingga endpoint itu mati tiap sesi agent berakhir, menyebabkan delegasi lintas-thread mati diam-diam. Diganti cronjob dengan delivery `platform:chat_id` + verifikasi file output di `~/.hermes/cron/output/`, atau `delegate_task` untuk pengerjaan internal.
- **Pemasangan:** script `/tmp/pasang-thread-tls.py` (backup config otomatis + validasi parse + rollback). Konfig selesai 15:01 WIB, pesan konfirmasi terkirim ke thread (exit 0).

## Catatan

- **Model `:free` nous kadang dicabut tanpa peringatan.** Diverifikasi 25 Sep 2026: `meituan/longcat-2.0:free` → HTTP 404 ("no longer free"). **3 Okt 2026: thread 803 & 7402 sudah dimigrasi** — 803 → `kr/deepseek-3.2` (9router), 7402 → `inclusionai/ling-3.0-flash-fin:free` (nous). Tidak ada thread lagi yang memakai model 404.
- **Pembuatan topik forum** hanya bisa dari Telegram (`/newtopic`) — bot API butuh akses token yang tidak diberikan ke agent. Setelah topik ada, kirim 1 pesan agar gateway mendaftarkan routing-nya, baru config bisa dipasang.
- **`skp-e-kinerja` ada di skill bank Niumination + built-in Hermes** (MD5 identik, sinkron).

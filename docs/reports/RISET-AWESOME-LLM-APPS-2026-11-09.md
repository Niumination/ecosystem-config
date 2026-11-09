# RISET — awesome-llm-apps (Shubhamsaboo)

Tanggal: 2026-11-09 · Mode: pelajari (study + lapor, belum adopsi)
Sumber: https://github.com/Shubhamsaboo/awesome-llm-apps — clone shallow `/tmp/awesome-llm-apps` (1.989 file, 172 MB, 560 file .py)

## Ringkasan

Bukan satu tool, melainkan **katalog 100+ contoh aplikasi LLM** (agent, skill, RAG, voice, MCP, generative UI) yang masing-masing berupa folder runnable terpisah. Nilai untuk ekosistem kita bukan sebagai platform, melainkan sebagai **sumber pola + 8 agent skill siap salin** dan beberapa template yang padanannya belum ada di bank skill (260 skill).

## Arsitektur

- Monorepo katalog: 11 folder kategori, tiap app = folder sendiri (`README.md` + kode + `requirements.txt`), tanpa monolit/build bersama
- Stack dominan: Python (Streamlit, Google ADK, OpenAI Agents SDK, Gemini, LangGraph-style multi-agent), beberapa TypeScript/browser extension
- Jalur model: multi-provider (Claude, Gemini, GPT, DeepSeek, Llama, Qwen, Grok) via API key masing-masing — **tidak ada provider lokal/9router**, tidak ada integrasi Hermes
- CI: `skill-evals.yml` (deterministic evals untuk `agent_skills/` tiap PR/push) + `claude.yml` (Claude PR Assistant)
- Kategori & jumlah (terukur dari clone):

| Kategori | Folder app | File .py |
|---|---|---|
| agent_skills | 8 skill (+evals, registry.json) | 23 |
| starter_ai_agents | ~13 | 22 |
| advanced_ai_agents | ~20 | 259 |
| advanced_llm_apps | ~25 | 35 |
| rag_tutorials | ~20 | 36 |
| always_on_agents | 2 | 16 |
| voice_ai_agents | ~4 | 17 |
| mcp_ai_agents | ~4 | 7 |
| generative_ui_agents | ~15 | 33 |
| ai_agent_framework_crash_course | ADK + OpenAI SDK | 112 |
| llm_optimization_tools, llm_finetuning_tutorials | 4 | — |

## Fitur yang relevan

**Agent Skills (8, format SKILL.md + scripts/ + references/ + evals):**
- `scope-creep-detector` (36 KB) — bandingkan git diff vs intent, output keep/split/justify. Offline, read-only
- `dependency-doctor` (36 KB) — audit manifest dependensi (pin stdlib, backport usang, unpinned, duplikat, yanked)
- `commit-archaeologist` (32 KB) — rekonstruksi asal-usul kode dari git history lokal
- `first-reader` (140 KB) — simulasi pembaca draft, lapor titik drop-off tanpa rewrite
- `project-graveyard` (56 KB) — audit side project mati + alasan
- `thinking-out-loud` (16 KB) — voice ramble → brief terstruktur, tebakan model dikarantina
- `advisor-orchestrator-worker` (448 KB) — meta-loop advisor/orchestrator/worker multi-model
- `self-improving-agent-skills` (232 KB) — optimasi skill otomatis via eval (Gemini + ADK)

Semua terdaftar di `agent_skills/registry.json` dengan `license`, `install` (`npx skills add …`), dan `evals_dir` per skill.

**Lainnya:** `toonify_token_optimization` (klaim hemat token 30–60% via format TOON), `always_on_hn_briefing_agent` (AgentScout: ADK + scheduler FastAPI + dry-run delivery), RAG tutorials (chat with PDF/GitHub/Gmail/YouTube/arXiv), crash course ADK & OpenAI Agents SDK.

## Relevansi ke ekosistem (vs yang sudah ada)

| Dari katalog | Padanan existing | Status |
|---|---|---|
| scope-creep-detector | `plan-compliance-audit`, `egm-drift-report` (parsial) | **Gap — belum ada skill khusus scope diff** |
| dependency-doctor | tidak ada | **Gap** |
| commit-archaeologist | tidak ada (ada `config-history-review`, beda domain) | **Gap** |
| first-reader | `content-script` (menulis, bukan mensimulasikan pembaca) | **Gap parsial** |
| project-graveyard | tidak ada | **Gap** (berguna untuk audit repo mati, mis. 48 repo) |
| always_on briefing | `blogwatcher` + cron (RSS generik) | Padan ada — AgentScout lebih spesifik HN+AI, nilai tambah kecil |
| chat with YouTube/PDF/Gmail | `youtube-content`, `ocr-and-documents`, `email-inbox-triage` | Duplikatif |
| toonify | tidak ada | **Gap** — relevan biaya token, tapi perlu uji lokal |
| advisor-orchestrator-worker | `delegate_task`/orkestrator thread | Padan ada, pola beda (multi-model eksplisit) |
| advanced/starter agents | `content-studio` pipeline + skill pelaksana | Duplikatif sebagai platform; pola app individual bisa ditiru |

Pemilik domain yang harus diperiksa sebelum adopsi (sesuai workflow): `content-studio` (orkestrator konten), `content-research`, `blogwatcher`, dan registry thread. Skill baru yang fungsinya sudah ditangani pipeline existing wajib **diintegrasikan ke pipeline itu**, bukan standalone.

## Keamanan

- Klaim repo: "every skill ships real code and passes a security + eval CI gate" — terverifikasi sebagian: `skill-evals.yml` memang ada dan menjalankan deterministic evals; tidak ditemukan scanner kredensial khusus di workflow yang dibaca
- Posture skill: `scope-creep-detector` eksplisit "no network calls, does not change working tree" — pola read-only yang sesuai approval gate kita
- Risiko umum katalog: tiap app butuh API key sendiri; pola `pip install -r requirements.txt` per app berarti dependency tree terpisah-pisah (bukan satu venv)
- Tidak ada mekanisme consent/approval gate setara SOUL.md; agent di katalog berjalan otonom penuh

## Lisensi

**Apache-2.0** (file `LICENSE` terverifikasi di clone) — boleh disalin, dimodifikasi, dikomersialkan dengan atribusi. Ini lebih longgar dari CC BY-NC yang pernah kita skip (autoskills). Per-skill: `license: Apache-2.0` di frontmatter SKILL.md.

## Persyaratan di mesin ini

- Agent skills: Python 3.10+ lokal, sebagian offline (scope-creep, commit-archaeologist, dependency-doctor) — **tanpa API key**
- Starter/advanced agents: API key per provider + `pip install` per app; Streamlit untuk UI
- Always-on: ADK + FastAPI scheduler + kredensial Gmail/webhook opsional (default dry-run)
- Bukan prasyarat adopsi: tidak perlu 9router/Hermes — skill diinstal via `npx skills add` ke coding agent, atau disalin manual ke bank skill

## Penilaian

- **Bukan platform untuk dipasang.** Nilai utamanya: 5 skill offline yang gap-nya nyata + pola eval per skill + toonify sebagai kandidat hemat token
- Katalog app (starter/advanced/RAG/voice) mayoritas duplikatif dengan pipeline `content-studio` dan skill existing — jangan diadopsi mentah
- Kualitas tidak seragam (katalog komunitas): skill dengan evals + offline/read-only yang paling aman untuk diadopsi duluan

## Rekomendasi (menunggu gas)

Fase 1 (risiko rendah, tanpa API key): adopsi `scope-creep-detector`, `dependency-doctor`, `commit-archaeologist` ke bank skill dengan workflow autoskills (cek frontmatter license Apache-2.0, copy folder utuh incl. evals, manifest + INDEX + sync + commit). `first-reader` dan `project-graveyard` sebagai kandidat fase 2.
Fase 2 (perlu uji): `toonify` — ukur hemat token aktual pada payload nyata sebelum dipakai.
Tidak direkomendasikan: menginstal katalog app mentah (Streamlit/ADK) di luar pipeline existing.

## Sumber

- README via web_extract + clone `/tmp/awesome-llm-apps` (HEAD shallow 2026-11-09)
- `agent_skills/registry.json`, `agent_skills/scope-creep-detector/SKILL.md`, `.github/workflows/skill-evals.yml`, `LICENSE`
- Padanan existing diverifikasi via `search_files` di `skills/` bank (260 skill per up-eco 2026-11-09)

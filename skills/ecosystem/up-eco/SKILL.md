---
name: up-eco
description: Ecosystem status check & sync workflow. Triggered via Telegram /up-eco command. Checks git status, detects unknown/foreign folders, syncs BACKLOG/docs with filesystem, and recommends actions to align local ecosystem with GitHub.
tags:
  - ecosystem
  - sync
  - git
  - status
  - niumination
last_updated: "2026-09-19"
version: 2.1.0
changes:
  - Added Phase 6: Skill Bank Integrity (frontmatter, INDEX sync, duplicates)
  - Added Phase 7: Skill Sync Status (sync-to-agents.sh, Hermes/USB targets)
  - Added Phase 8: Mission Control Dashboard (Skill Monitor API, stale, conflicts, stats)
  - Added "Lightfix & Cron" phase + generator INDEX (scripts/gen-skill-index.py)
  - Fixed dirty-repo sweep (find clause excluded every .git) and INDEX row-count comparison
---

# 🔄 /up-eco — Ecosystem Status & Sync Check

## Trigger
User sends **`/up-eco`** from Telegram (or says "cek ekosistem" / "up-eco").

## Workflow

### Step 1: Run the checker script
```bash
cd /Users/zaryu/Desktop/Niumination && bash scripts/up-eco.sh
```

Output will show:
- **Git status** root ecosystem + profile README
- **Dirty repos** across all sub-repos
- **Unknown/foreign folders** (detected on filesystem but not in BACKLOG.md)
- **BACKLOG sync** (projects referenced but missing from disk)
- **GitHub Pages** health check
- **🧠 Skill Bank Integrity** — SKILL.md count vs INDEX.md, frontmatter validation, duplicate detection
- **🔄 Skill Sync Status** — sync-to-agents.sh last run, Hermes divergence
- **🎛️ Mission Control Dashboard** — Skill Monitor API reachable, stale skills, conflicts, usage stats
- **💬 Telegram Thread Status** — 5 mission-control thread activity, model/provider mapping, last error
- **🪄 Lightfix & Cron** — skrip lightfix, wrapper Hermes, status job cron `up-eco-lightfix`, hasil run terakhir
- **🔑 Credential Broker** — central AI-API key control plane (scripts/keys.sh): canonical terdefinisi vs tersimpan di Keychain, status migrasi (Phase B HOLD), scan plaintext leak di store lama (~/.hermes/.env, ~/.gemini/.env, ~/.continue/.env, vault/secrets.zsh)
- **Recommendations list** (numbered)

### Step 2: Interpret results for the user

Report in a clean format:

**Git Status:**
- ✅ / ❌ Root ecosystem (Niumination/ecosystem-config)
- ✅ / ❌ Profile README (Niumination/Niumination)

**Dirty Repos:**
- List repos with uncommitted changes

**Unknown Folders (detected):**
→ Folders found on filesystem that are NOT tracked in BACKLOG.md or AGENTS.md
→ These are likely created by JCode or manual work
→ Recommend: register in BACKLOG.md, categorize into pipeline, create AGENTS.md entry

**Recommendations:**
→ Numbered action items

### Step 3: Detect source of changes

When the script finds unknown/foreign folders, identify:
- **Hermes-made changes** (documented in this conversation)
- **JCode-made changes** (new repos, new folders mentioned in user messages)
- **Manual user changes** (user worked directly on new project folders)

Use session_search if needed to find what was discussed before suggesting.

### Step 4: Archive inactive repos (Phase 9d)

When repos are >60 days dormant:
1. Move repo directory to `inactive-2026-09/` at ecosystem root
2. Add as git submodule: `git submodule add --name inactive-<repo> file:///abs/path inactive-2026-09/<repo>`
3. Update `.gitignore`: remove `archive/` if present (blocks submodule tracking)
4. Update `BACKLOG.md`: increment archive count, mark repo as ~~Archived~~
5. Update `AGENTS.md`: directory tree reflects archive move
6. Remove JCode references from the repo's active files if any
7. Commit: `chore: archive <repo> as submodule`

**Why submodules, not git archive:** `archive/` is in `.gitignore` which prevents git tracking. Moving to `inactive-2026-09/` at root allows submodule tracking while preserving the directory structure.

### Step 5: Purge JCode references (Phase 9e)

After archiving, scan ALL active files for stale JCode references:
```bash
grep -r "JCode\|jcode\|Jcode" --include="*.md" --include="*.sh" --include="*.py"   ~/Desktop/Niumination/scripts/ ~/Desktop/Niumination/skills/   ~/Desktop/Niumination/AGENTS.md ~/Desktop/Niumination/BACKLOG.md 2>&1
```

Fix each hit:
- **Scripts**: Replace JCode bridge comments with Niumination ecosystem references
- **Skill SKILL.md**: Remove `~/.jcode/skills` as sync target, replace with `~/.hermes/skills`
- **BACKLOG.md/AGENTS.md**: Remove JCode deprecated rows, update skill counts
- **ekosistem-status.md**: Change `Jcode + Hermes + USB` to `Hermes + USB`
- **trio-watch.sh**: Keep `jcode_status()` as a documented compatibility wrapper returning static zero state

**Pitfall**: `skills/ecosystem/*` SKILL.md files themselves contain JCode references — these MUST be updated too, not just scripts and root docs.

**Why purge**: Stale JCode references confuse future sessions into thinking JCode is still an active sync target, causing wasted effort on `--verify-target ~/.jcode/skills`.

### Step 6: Offer to execute

After presenting the report, ask the user (if not already instructed):
- "Gas/lanjut?" to execute ALL recommendations
- Or individually approve each action

### Command Rules
- `/up-eco` → run script, report
- `/up-eco --fix` → run script + execute all non-destructive fixes (commit, push, register projects)
- `/up-eco --dry-run` → run script without output colors (for cron/automation)
- `/up-eco --fix-light` → jalankan `bash scripts/up-eco-lightfix.sh` sekarang (tidak menunggu cron 23:30)

## 🪄 Lightfix & Cron (2026-09-19)

Perbaikan ringan berulang kini berjalan otomatis lewat cron Hermes, bukan lagi manual.

| Bagian | Path | Catatan |
|--------|------|---------|
| Skrip perbaikan | `scripts/up-eco-lightfix.sh` | idempoten · `--commit` opt-in (default: tidak commit) |
| Generator INDEX | `scripts/gen-skill-index.py` | sebelumnya tidak ada — akar drift INDEX |
| Wrapper Hermes | `~/.hermes/scripts/up-eco-lightfix.sh` | cron Hermes hanya menjalankan skrip di folder ini |
| Job cron | `up-eco-lightfix` · `30 23 * * *` · mode `no-agent` | script-only, TANPA panggilan LLM (biaya nol) |
| Log | `logs/up-eco-lightfix.log` | ringkas per run, rotasi otomatis |

**Urutan kerja lightfix:** manifest (`skill-manifest.py`) → INDEX (`gen-skill-index.py`) → sync (`sync-to-agents.sh`, sekaligus meregenerasi `docs/registry/skill-registry.md`) → verifikasi (`--check` + `--verify-target ~/.hermes/skills --structure domain`) → tulis log. Keluar non-nol hanya bila ada kegagalan nyata.

**Kebijakan "fix ringan" — hanya artefak turunan yang boleh ditulis ulang otomatis.**
- **Boleh:** `skills/manifest.json`, `skills/INDEX.md`, `docs/registry/skill-registry.md`, salinan target `~/.hermes/skills/`.
- **Tidak boleh (butuh penilaian manusia):** commit/push (kecuali `--commit`), menghapus atau memindahkan berkas, mengubah isi skill, menyentuh `SOUL.md`/`AGENTS.md`/config/kredensial, memperbaiki repo kotor.

**up-eco memelihara dirinya sendiri.** Fase "🪄 Lightfix & Cron" memverifikasi skrip + wrapper, memastikan job cron terdaftar, dan **membuat ulang keduanya bila hilang** — satu kali `/up-eco` cukup setelah cron terhapus.

### Pelajaran dari perbaikan 2026-09-19 (jangan diulang)
- **`find -name .git -not -path '*/\.*'` mengecualikan SEMUA repo.** Setiap path `.git` selalu memuat `/.`, jadi loop dirty-repo tidak pernah berjalan dan up-eco melaporkan "Semua repos clean" padahal ada 9 repo kotor / 98 berkas. Klausa `-not -path '*/\.*'` benar untuk pemindaian folder, salah untuk `.git`.
- **`[ ... ] && pass` di bawah `set -e` mematikan skrip.** Begitu repo kotor ditemukan, perintah uji mengembalikan 1 dan skrip berhenti sebelum bagian Rekomendasi. Pakai `if ... then ... fi`.
- **Jangan bandingkan jumlah BARIS INDEX dengan jumlah skill bank.** INDEX mencantumkan sebagian skill dua kali (tabel "featured" di atas + tabel domainnya) → terbaca 163 vs 145 dan peringatan mismatch-nya palsu. Bandingkan **nama unik**.
- **Identitas baris skill = NAMA FOLDER, bukan `name:` di frontmatter.** Kasus `ponytail-core` (frontmatter `name: ponytail`) membuat generator menganggap barisnya yatim lalu membuangnya.
- **Generator INDEX harus memindai SELURUH berkas**, bukan berhenti di heading non-domain pertama — kalau tidak, section yang ditambahkan di akhir berkas tidak ikut diparsing dan ditambahkan lagi setiap putaran (tidak konvergen; pernah tumbuh 15 → 45 section).
- **Churn timestamp di-commit otomatis, churn nyata tidak (2026-09-19).** `scripts/lightfix-autocommit.sh` membandingkan versi HEAD dengan working setelah normalisasi field waktu (manifest `generatedAt`; baris `_Last sync` di registry) — jadi hanya commit bila isinya terbukti identik. Menolak bila ada berkas terlacak di luar allowlist berubah, ada perubahan ter-stage, repo sedang merge/rebase, atau konten benar-benar berubah. Tanpa ini setiap run cron 23:30 meninggalkan 2 berkas "kotor" hanya karena stempel waktu. Penjaga ini **tidak pernah push** — commit lokal menumpuk dan perlu di-push saat sesi berikutnya (terlihat sebagai ahead di Git Status).
- **`sync-to-agents.sh` pernah menambah 1 baris kosong per run (diperbaiki 2026-09-19).** Penulis registry menyambung `after = content[e:]` (yang sudah dimulai newline) lalu menambah `'\n'` lagi → baris kosong menumpuk di ekor (mencapai 41 baris). Setelah perbaikan: 3× sync berturut-turut tetap 154 baris. **Kalau menemukan berkas yang tumbuh sendiri setiap sync, curigai pola `content + '\n' + after` ini.**
- **Repo "wajar kotor" bukan peringatan lagi (2026-09-19).** `brain/` dan `archive/` masuk allowlist `EXPECTED_DIRTY` di fase Dirty Repos: tetap **ditampilkan** sebagai info supaya tidak ada perubahan tersembunyi, tetapi tidak dihitung sebagai perlu tindakan dan tidak masuk Rekomendasi. Repo yang memang berubah harian → tambahkan polanya ke array `EXPECTED_DIRTY` di `scripts/up-eco.sh`.
- **Skrip baru wajib `chmod +x`.** `[ -x file ]` gagal untuk berkas mode 644 sehingga fase baru melapor "skrip tidak ada" padahal ada.

## Current-State Addendum (2026-09-10)
From a real `/up-eco` run on macOS, these additional checks and fixes are now part of the standard workflow:

- **SOUL.md style section:** `up-eco` now checks for a `## Gaya jawab` section in `~/.hermes/SOUL.md`. If missing, add a concise 3-5 line section covering: answer style, language default, structure preference.
- **Hermes display config:** Verify `display.compact=true`, `agent.task_completion_guidance=false`, `display.turn_completion_explainer=false`, `display.personality=""`. These suppress verbose Telegram output.
- **SOUL/dotfiles drift check:** `up-eco` compares SHA-256 of `~/.hermes/SOUL.md` vs `dotfiles/zaryu-terminal-dotfiles/hermes/SOUL.md`. If they differ, or if the symlink target is missing, report a drift incident and recommend repair before any session restart.
- **`.gitignore` hygiene:** Ensure root `.gitignore` covers runtime/local artifacts: `logs/`, `.vscode/`, `.9router-state.json`, `skills-lock.json`, `.sync-log`, `.git-backup-*/`. Missing entries cause `up-eco` to flag them as unknown folders.
- **Skill sync mismatch:** After `sync-to-agents.sh`, Hermes may show mismatch skills even when target is clean. Known non-fatal divergence; do not block on it.
- **Mission Control v3.0 (Next.js-only):** Legacy `server.py` (FastAPI port 5200) DELETED. Modern MC = `services/niu-mission-control/apex-ui/` (Next.js 15 + React 19). Dev: `npm run dev` (port 3000). Production: `npm run build && npm start`. `HTTP 404` on `/api/*` while UI returns `HTTP 200` is NORMAL — Next.js frontend only, no FastAPI backend. Not a failure.
- **`ROOT: unbound variable` error:** If `scripts/up-eco.sh` ends with `ROOT: unbound variable`, check line ~790 for a shell variable expansion issue. This is a script bug, not an ecosystem bug.
- **`set -e` + `grep -c` 0-match kill (fixed 2026-09-14):** `expired=$(echo "$comp_out" | grep -c "|EXPIRED|")` exited 1 when all accounts ACTIVE → script died silently mid-Composio before Rekomendasi/9router sections, exit=1 with no visible error. Fix: guard `|| true` on all three `grep -c` counts + loops use `while ... <<< "$rows"` with `[ -z "$slug" ] && continue` instead of `pipe | while`. Rule: in `set -euo pipefail` scripts, NEVER use bare `grep -c` in command substitution when 0 matches is a legal state.
- **MC check sudah diperbaiki (2026-09-13):** `MC_URL=http://localhost:3000` (apex-ui Next.js). Kalau MC mati → `ℹ️ Mission Control (apex-ui :3000) tidak aktif — bukan insiden` (tidak lagi `⚠️`/`❌` dan tidak lagi menyaran `python3 server.py`). API skill-monitor legacy di `MC_API_URL=http://localhost:5200`; kalau mati, seksi stale/conflict/stats dilewati.
- **Allowlist audit konten:** `scripts/skill-audit.py` punya `ALLOWED_DOMAINS`; 2026-09-13 diperluas (opencode.ai, composio.dev, nousresearch.com, referensi riset/bibliografi) + host parser membuang userinfo (`oauth2:token@host`). Efek: finding 275 → 36. Sisa finding = fixture keamanan yang sengaja ada (`evil.example`, `localhost.evil.com`), contoh `~/.ssh` di skill github-auth, dan dokumen instalasi `curl | bash` — semua benign, jangan "diperbaiki" otomatis.
- **Promosi skill dari target ke bank:** skill yang hanya ada di `~/.hermes/skills` (tidak di bank) diklasifikasi lewat `~/.hermes/skills/.bundled_manifest` (bawaan Hermes) dan `~/.hermes/skills/.hub/lock.json` (instal dari hub). Yang bukan keduanya = dibuat lokal → kandidat promosi ke bank (`skills/<domain>/<skill>/`). Setelah promosi: regenerate `scripts/skill-manifest.py`, update `skills/INDEX.md`, jalankan `sync-to-agents.sh`, lalu pindahkan salinan lama di path berbeda (mis. top-level `~/.hermes/skills/<skill>/`) supaya tidak duplikat di katalog Hermes. Promosi 2026-09-13: 51 skill, bank 70 → 121.
- **Whitelist folder top-level:** `check_unknown_folders()` punya array `known_dirs`; `inactive-2026-09` ditambahkan 2026-09-13 setelah sebelumnya muncul sebagai "Folder Asing" palsu. Folder top-level baru yang sah (mis. kategori arsip baru) harus ditambahkan di sana, kalau tidak akan dilaporkan sebagai folder asing.

## MC Architecture Transition (2026-09-10)
**Legacy (deleted):** `services/niu-mission-control/server.py` (FastAPI port 5200)
**Current (v3.0):** `services/niu-mission-control/apex-ui/` (Next.js 15 + React 19, port 3000 dev)
- `build_unified.py` → generates `index.html` single-file dashboard
- `server.py` at root is legacy snapshot only (`legacy-ui` branch)
- Health check: `curl -s http://localhost:3000/` → HTTP 200
- Do NOT reference port 5200 as active — it was removed

## Known Categories
```
Pipeline: sandbox💤 → labs🔬 → services/sites/desktop/agents🔧 → apps🏭 → archive📦
```
| Category | Path | Description |
|----------|------|-------------|
| apps/ | production | Deployed & battle-tested |
| services/ | backend | Servers & engines |
| sites/ | frontend | Web applications |
| desktop/ | native | Desktop & mobile apps |
| agents/ | AI | Agents & automation |
| labs/ | experiments | Active research |
| sandbox/ | dormant | Dormant playground projects |
| inactive-2026-09/ | archived | Dormant repos as git submodules |

## Registration Template
When adding a new project to BACKLOG.md:
```markdown
| **ProjectName** | `Category/ProjectName/` | Status | Stack | Deploy |
```

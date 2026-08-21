---
name: ecosystem-snapshot
description: Generate a comprehensive ecosystem configuration snapshot for Niumination. Produces a Markdown document capturing macOS specs, git status, project registry, filesystem layout, Mission Control state, Telegram threads, Skill Bank summary, Hermes config, deployments, security notes, and open issues. Use when the user asks for "konfigurasi lengkap ekosistem", "ekspor snapshot ekosistem", "docs konfigurasi aktif", or requests a full current-state Markdown report.
tags:
  - ecosystem
  - documentation
  - snapshot
  - niumination
last_updated: "2026-08-18"
version: 1.0.0
changes:
  - Initial release: snapshot export workflow + verification pattern
---

# 📸 Ecosystem Snapshot — Full Active State Export

## Trigger
User requests a complete configuration/snapshot of the ecosystem, Mac, Hermes, and integrations as a Markdown file. Example prompts:
- "Buatkan seluruh konfigurasi lengkap ekosistem... ke dalam file .md"
- "Ekspor snapshot ekosistem sekarang"
- "Dokumentasikan state aktif semua komponen"

## Adjacent workflow: Anomaly Audit ("periksa seluruh anomali... jangan lewatkan satu pun")
Distinct from snapshot: user wants EVERY anomaly found, NOT a report written to disk. Multi-layer scan (git 45 repo → secret → proses/port → config → MCP stderr → launchd → skill plane → deploy canary → DB/disk), lalu laporan terstruktur per severity (🔴/🟠/🟡/🟢) dengan bukti probe. **JANGAN fix apa pun** — audit hanya melapor; eksekusi hanya setelah user bilang "fix/gas". Playbook lengkap + nilai aktual 18-Ags-2026: `references/anomaly-audit-playbook.md`. Temuan khas: MC :5200 down tanpa plist, fallback chain 401 di depan, 3-4 MCP crash-loop (file/venv/node_modules hilang), launchd exit 127 (script USB missing), skill plane 47 vs 231 vs 2 vs MISSING, canary 000/307.

## Workflow

### Step 1: Gather source data in parallel
Run these commands concurrently to collect current state:

```bash
# Ecosystem check
cd /Users/zaryu/Desktop/Niumination && bash scripts/up-eco.sh

# Project registry
cd /Users/zaryu/Desktop/Niumination && cat BACKLOG.md

# Mac hardware/software/storage
system_profiler SPHardwareDataType SPSoftwareDataType SPDisplaysDataType SPStorageDataType

# Mission Control server config
cd /Users/zaryu/Desktop/Niumination/services/niu-mission-control && cat server.py | head -200

# Hermes config providers
hermes config get providers 2>/dev/null || true
hermes config get plugins 2>/dev/null || true

# Provider health probes
# ⚠️ WAJIB sertakan Authorization header dari data/.env — tanpa key, juan/huancheng/agentrouter
#    tampak 401 PALSU padahal key valid (verified 18-Ags-2026). 401 asli = masih 401 DENGAN key.
set -a; source /Volumes/HermesAgent/HermesAgentUSB/data/.env; set +a
for p in opencode-zen juan-router 9router agentrouter huancheng openrouter nvidia_nim; do
  case "$p" in
    opencode-zen) url="https://opencode.ai/zen/v1/models"; key="$OPENCODE_ZEN_API_KEY" ;;
    juan-router) url="https://router.juan.web.id/v1/models"; key="$JUAN_ROUTER_API_KEY" ;;
    9router) url="http://localhost:20128/v1/models"; key="$NINE_ROUTER_API_KEY" ;;
    agentrouter) url="https://agentrouter.org/v1/models"; key="$AGENTROUTER_API_KEY" ;;
    huancheng) url="https://api.hcnsec.cn/v1/models"; key="$HUANCHENG_API_KEY" ;;
    openrouter) url="https://openrouter.ai/api/v1/models"; key="$OPENROUTER_API_KEY" ;;
    nvidia_nim) url="https://integrate.api.nvidia.com/v1/models"; key="$NVIDIA_NIM_API_KEY" ;;
  esac
  status=$(curl -sS -m 8 -H "Authorization: Bearer $key" -H "User-Agent: hermes-agent/0.19.0" "$url" -o /dev/null -w "%{http_code}" 2>/dev/null || echo "timeout")
  echo "$p: $status"
done
# Interpretasi: 200 = hidup; 401 tanpa key = false positive; 401 dengan key = key ditolak;
# 429 FreeUsageLimitError = kuota free Zen habis (bukan config rusak); /v1/models 200 ≠ chat jalan (huancheng list OK tapi inference timeout)
```

### Step 2: Write snapshot file
Create: `/Users/zaryu/Desktop/Niumination/docs/ecosystem-config-snapshot-YYYY-MM-DD.md`

Required sections:
1. **macOS — Active Machine**
   - Host, model, CPU, RAM, GPU, OS version, display
   - Active volumes with mount points, filesystems, writability
   - Boot volume free space

2. **Niumination Ecosystem — Git Status**
   - Root, profile README, brain HEADs
   - Dirty repos count
   - Project registry table: repo, category, status, remote/deploy

3. **📂 Filesystem Layout**
   - Counts per top-level folder: apps/, services/, sites/, desktop/, agents/, labs/, sandbox/, archive/, docs/, scripts/, skills/, tools/, vault/, brain/, dotfiles/

4. **🎛️ Mission Control**
   - Port, version, dashboard/backend paths, stack
   - Auth/CORS/rate limit/logging config
   - Server status from `up-eco.sh`
   - Main script, WS endpoint, API prefix
   - v3 API routers present

5. **💬 Telegram Threads**
   - Thread ID, status, model, provider, message count, last error
   - Last activity timestamp

6. **🧠 Skill Bank**
   - Total SKILL.md count, domain breakdown
   - INDEX sync, frontmatter validity, duplication
   - Manifest SHA-256 sync status
   - Last sync time, target counts

7. **⚙️ Hermes Config**
   - Providers list with key details
   - Active model/provider
   - Plugin list relevant to runtime
   - Provider health probe result: live usable vs unusable providers

8. **🌍 Deployment**
   - GitHub Pages status
   - Vercel status
   - Special notes (e.g., PemdiAcehTengah CLI deploy)

9. **🔐 Security & Notes**
   - Gitleaks, SIP, config write protection
   - Volume/filesystem constraints
   - Provider issues: unusable providers from `/v1/models` probes
   - Open issues numbered list

10. **📌 Git History References**
    - Latest commits for root, brain, profile README

11. **Timestamp**
    - `*Snapshot created at YYYY-MM-DD HH:MM WIB.*`

### Step 3: Verify and deliver
- Read back the file with `read_file` to confirm content
- Report the absolute path to the user
- Include a brief summary of key counts: projects, skills, threads, dirty repos, open issues

## Historical Recap (rekap perubahan sejak awal) — ground truth filesystem, BUKAN session_search

Saat user minta "rekap perubahan dari awal sampai sekarang" (mis. perubahan Hermes/config yang pernah dilakukan), jangan rekonstruksi dari memory/session history — user menuntut **data valid dari file** (18-Ags-2026, "kamu selalu menginginkan data valid bukan rekayasa"). Sumber kebenaran berurutan:

1. **`/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml.bak*`** — timeline provider/model/plugins: nama file ber-timestamp (`config.yaml.bak.20260707_225923`), ukuran berbeda = ada perubahan. Ekstrak per backup: `provider:`, `default/model:`, `base_url:`, plugin list, `channel_overrides` (ada/tidak), `fallback_providers`. Ini membuktikan kapan provider dicoba & diganti (contoh nyata: nvidia_nim Jul 7 → agentrouter Jul 15 → nous Jul 23 → huancheng Aug 8 → 9router Aug 13).
2. **`~/Desktop/Niumination/brain/docs/ecosystem-changelog.md`** — changelog resmi ekosistem (entry per tanggal, format `YYYY-MM-DD — [JENIS]`).
3. **`git log`** per repo (root ecosystem-config, brain/, agents/profile) — commit messages menunjukkan intent perubahan.
4. **`brain/resources/ai/01-hermes-agent.md`** — snapshot data Hermes yang pernah di-rewrite (provider, plugins, cron).

Jangan pernah menulis "ini riwayatnya" tanpa minimal satu sumber filesystem di atas. Kalau backup config ada 10+, tabel timeline (tanggal → provider → model → catatan) adalah format paling informatif.

## Pitfalls
- Do not claim backend work is complete without visual/browser verification
- Do not invent deployment status; rely on `up-eco.sh` output
- Distinguish "backend done" from "frontend visual changed"
- macOS volumes may be read-only NTFS; writes must happen through `/Users/zaryu/Desktop/Niumination`
- **`docs/` punya DUA folder referensi (verified 18-Ags-2026):** `docs/reference/` (singular, dari restrukturisasi v4.0 Jul 29 — dokumen status internal: ai-memory-collection, akun-login, cleanup-audit, ekosistem-status, migration-portable-to-native, niu-dash-redesign, observer-ecosystem-integration) vs `docs/references/` (plural, sejak Aug 10 — hasil studi link/repo eksternal: agent-reach, munder-difflin, 9drive, STATUS-REFERENSI, dll). **Konvensi: referensi studi eksternal → `docs/references/`.** Jangan buat folder ketiga; kalau ragu cek kedua folder dengan `ls -laT` dulu sebelum menyimpulkan "tidak ada".
- Saat user bilang "simpan jadi referensi" untuk dokumen yang dikirim: copy ke `docs/references/<nama-bermakna>-<YYYY-MM-DD>.md`, lalu laporkan path-nya.
- `hermes doctor` bisa timeout lama (>60s) di mesin ini — jangan jadikan blocker; gunakan `hermes config check` (cepat) sebagai alternatif.
- **"periksa/pastikan X" = probe langsung + lapor singkat — BUKAN rekap sejarah panjang, BUKAN fix apa pun.** User (18-Ags-2026, marah keras: "kamu gak perlu kerjain apapun kalau aku gak minta,, NGERTI?" dan "kamu selalu bikin kerjaanku tambah runyam") menuntut: kerjakan HANYA yang diminta. Kata kerja eksekusi eksplisit = 'gas', 'fix', 'kerjakan', 'lanjut'. Kata kerja verifikasi = 'periksa', 'pastikan', 'cek' → probe → lapor singkat → berhenti. Kalau ada temuan yang butuh fix, tawarkan 1 baris, jangan eksekusi.
- **Verifikasi RTK:** `rtk rewrite "git status"` → exit code 3 = rewritten (plugin aktif); exit 1 = pass-through (tidak ada equivalen). `rtk gain` = bukti token saving (68.6% di mesin ini). Cek juga `plugins.enabled` di config (hanya `rtk-rewrite` yang wajib enabled).
- **Model ID case-sensitive (huancheng & distributor new-api lain):** config bisa pakai lowercase (`deepseek-v4-flash`) tapi server menolak `model_not_found`. Selalu `GET /v1/models` dulu untuk ID persis (`DeepSeek-V4-Flash`). Fix lewat `hermes config set providers.<nama>.default_model <ID>`, bukan edit file (write-protected).
- **Config Hermes write-protected:** agent tidak bisa edit `config.yaml` langsung (ditolak). Satu-satunya jalur: `hermes config set` / `hermes fallback` / `hermes cron` / `hermes model`.

## Reference Files
- `references/snapshot-template.md` — exact Markdown template for the snapshot document
- `references/mass-repo-sync.md` — workflow audit+sync ~45 repo git ke GitHub: os.walk discovery (bug urutan .git), secret-check sebelum commit, verifikasi kepemilikan remote (403/404), konvensi simpan paket zip referensi ke docs/references/
- `references/anomaly-audit-playbook.md` — scan multi-layer "periksa seluruh anomali, jangan lewatkan satu pun": git/secret/proses/config/MCP-stderr/launchd/skill-plane/canary/DB + nilai aktual 18-Ags-2026 (MC down, fallback 401 depan, MCP crash-loop, exit 127)
- `references/niumination-core-v2.md` — hukum ekosistem (12 Hukum, MODEL.policy Zen-only, FREEZE.list, HANDOFF/fence, ledger no-agent) dari paket niumination-rebuild-v2. **Ekosistem: hanya keluarga opencode-zen boleh berpikir (nemotron-3-ultra-free utama; lihat MODEL.policy.yaml + D-0002/D-0003) — v2 MENGGANTI v1** — baca sebelum mengerjakan tugas core apa pun di Niumination
# INDEX — Bank Skill Terpusat Niumination

> **Versi:** 4.0.1 (Superpowers Integration — 6 SDLC skills added from obra/superpowers)
> **Lokasi:** `~/Desktop/Niumination/skills/`
> **Sync:** ✅ `sync-to-agents.sh` — auto-copy ke Jcode + Hermes (local) + AGENTS.md (cron every 6h) — USB backup-only
> **DOX Injection:** ✅ Layer 3 — 34 skill auto-loaded via trigger keyword di AGENTS.md
> **Mission-Control Dashboard:** ✅ Layer 4 — Skill Monitor di `services/niu-mission-control/` (WebSocket, stats, stale, conflicts)
> **Hermes Integration:** ✅ Semua 180 skill tersedia di Hermes catalog (USB: backup-only, ~/.hermes/: 198 = 144 bank + 54 bawaan Hermes)
> **Domain-based:** Semua skill dikategorisasi per domain, BUKAN per agent.
> **Status:** 180 ✅ Aktif
>
> | Skill | Status | Path | Deskripsi |
> |-------|--------|------|-----------|
| **weathernext-gayo** | ✅ Aktif | ecosystem/weathernext-gayo | Analisis agro-klimatologi kopi Gayo & mitigasi bencana hidrometeorologi |
| **integration-verification** | ✅ Aktif | ecosystem/integration-verification | Verify external services/APIs connected and working end-to-end |
| **skill-bank-management** | ✅ Aktif | ecosystem/skill-bank-management | Kelola Bank Skill Niumination — manifest SHA-256, sync+verifikasi+lockfile, drift, adopsi skill pihak ketiga, audit konten, hapus/promosi skill (menyerap 5 skill bank-* yang dikonsolidasi 18 Sep 2026) |
| **ecosystem-snapshot** | ✅ Aktif | ecosystem/ecosystem-snapshot | Generate snapshot konfigurasi ekosistem |
| **ecosystem-tool-adoption** | ✅ Aktif | ecosystem/ecosystem-tool-adoption | Adopsi tool baru ke ekosistem |
| **niu-core-governance** | ✅ Aktif | governance/niu-core-governance | Governance core Niumination |
| **niu-mission-control-ui** | ✅ Aktif | ecosystem/niu-mission-control-ui | Operasi dashboard Mission Control UI |
| **niu-mission-control-ops** | ✅ Aktif | software-development/niu-mission-control-ops | Operate Niu-MissionControl server (port 5200) |
| **hermes-provider-config** | ✅ Aktif | ecosystem/hermes-provider-config | Konfigurasi provider Hermes |
| **kanban-ecosystem-management** | ✅ Aktif | ecosystem/kanban-ecosystem-management | Kelola kanban ekosistem |
| **config-history-review** | ✅ Aktif | ecosystem/config-history-review | Review riwayat config |
| **ekosistem-content-verification** | ✅ Aktif | ecosystem/ekosistem-content-verification | Verifikasi konten ekosistem |
| **provider-fallback** | ✅ Aktif | ecosystem/provider-fallback | Handle AI provider failures + fallback |
| **redesign-verification** | ✅ Aktif | software-development/redesign-verification | Pitfall proyek redesign multi-fase |
| **delegated-output-verification** | ✅ Aktif | software-development/delegated-output-verification | Verifikasi output delegasi |
| **web-dashboard-maintenance** | ✅ Aktif | software-development/web-dashboard-maintenance | Maintenance unified dashboards |
| **web-accessibility-wcag** | ✅ Aktif | design/web-accessibility-wcag | Audit aksesibilitas web WCAG 2.1 AA |
| **dark-theme-a11y** | ✅ Aktif | design/dark-theme-a11y | Aksesibilitas dark/glassmorphism theme |
---

## Domain: Software Development

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **ponytail-audit** | ✅ Aktif | tools/ponytail/ | 1.7 KB | Whole-repo audit for over-engineering — ranked deletion list |
| **ponytail-review** | ✅ Aktif | tools/ponytail/ | 2.4 KB | Diff-level over-engineering review — satu baris per finding |
| **ponytail-debt** | ✅ Aktif | tools/ponytail/ | 1.7 KB | Harvest `ponytail:` comments into debt ledger — track deferred shortcuts |
| **ponytail-gain** | ✅ Aktif | tools/ponytail/ | 2.0 KB | Measured-impact scoreboard: -54% LOC, -22% token, -20% cost |
| **ponytail-help** | ✅ Aktif | tools/ponytail/ | 2.6 KB | Quick-reference card for all ponytail modes, skills, and commands |
| **systematic-debugging** | ✅ Aktif | Hermes | 25.6 KB | 4-phase debugging workflow — isolate, root cause, fix, verify |
| **project-orientation** | ✅ Aktif | Hermes | 64.0 KB | Verify from source — jangan asumsi, baca direktori & file dulu |
| **document-content-pipeline** | ✅ Aktif | Hermes | 30.1 KB | ODL-PDF batch convert → Markdown → cleanup → JSON → website. Termasuk rebuild ground-truth (2d) + post-rebuild cleanup (2e) + ROOT CAUSE PPT→PDF |
| **optimization** | ✅ Aktif | Jcode + Hermes | 2.1 KB | Profiling, bottleneck detection, targeted optimization |
| **ultrathink** | ✅ Aktif | HaydenLundin | 4.5 KB | Deep architectural reasoning — trade-offs, invariants, craftsmanship |
| **tripwire** | ✅ Aktif | sisi-tarak | 2.8 KB | Single-risk prioritization — satu hal paling kritis untuk dipantau |
| **premortem** | ✅ Aktif | sisi-tarak | 2.5 KB | Failure pre-mortem — asumsikan gagal, cari penyebab sebelum mulai |
| **hermes-zero-defect-architect** | ✅ Aktif | Hermes USB | 11.8 KB | Zero-defect debugging — snapshot, rollback, JCode parallel, full pipeline |
| **simplify-code** | ✅ Aktif | Hermes USB | 10.9 KB | Parallel 3-agent cleanup — simplify, refactor, deduplicate recent changes |
| **brainstorming** | ✅ Aktif | superpowers | 10.0 KB | Design refinement sebelum coding — hard gate: jangan nulis kode tanpa desain disetujui |
| **writing-plans** | ✅ Aktif | superpowers | 7.0 KB | Implementation plan granular — tiap task 2-5 menit, bite-sized steps, no placeholders |
| **verification-before-completion** | ✅ Aktif | superpowers | 3.6 KB | Iron law verification — no completion claims tanpa fresh verification evidence |
| **subagent-driven-development** | ✅ Aktif | superpowers | 28.0 KB | Parallel agent execution — dispatch subagent per task, 2-stage review, fix loop max 5 rounds |
| **finishing-a-development-branch** | ✅ Aktif | superpowers | 7.0 KB | Post-implementation workflow — verify tests, present merge/PR/keep/discard options |
| **requesting-code-review** | ✅ Aktif | superpowers | 3.0 KB | Dispatch code reviewer subagent — spec compliance + code quality assessment |
| **pemdi-evidence-management** | ✅ Aktif | Hermes USB | 50.8 KB | Kelola bukti dukung Pemdi (PermenPANRB 8/2026) — cross-ref PemdiArena CSV, Excel master, modul JSON, JDIH/OpenData API → inject ke dashboard dengan inline PDF preview |
| **pemdi-uiux-refinement** | ✅ Aktif | Hermes USB | 4.5 KB | Refine UI/UX portal Pemdi Aceh Tengah dengan impeccable + hermes-uiux-technical — sistem animasi global, fix anti-pattern, audit pasca-deploy |
| **compliance-checklist-dashboard** | ✅ Aktif | Hermes USB | 11.0 KB | Build compliance/checklist dashboards (Pemdi, SPBE, IKD) — parse checklist → JSON → Next.js dashboard + embedded previews |
| **plan-compliance-audit** | ✅ Aktif | Hermes USB | 21.0 KB | Audit ekosistem/proyek terhadap spesifikasi tertulis — layer scripts/crons/configs/credentials/docs, gap by severity |
| **agent-reach** | ✅ Aktif | Panniantong/Agent-Reach | 2.3 KB | Internet capability layer — read/search web, YouTube, GitHub, RSS via zero-config CLI with fallbacks |
| **python-testing-patterns** | ✅ Aktif | autoskills (MIT, wshobson) | 6.0 KB | Pytest, fixtures, mocking, TDD — strategi testing Python komprehensif |
| **fastapi-templates** | ✅ Aktif | autoskills (MIT, wshobson) | 4.6 KB | FastAPI production-ready — async patterns, dependency injection, error handling |
| **fastapi-python** | ✅ Aktif | autoskills (Apache-2.0, mindrally) | 2.5 KB | FastAPI expert — best practices API & async |
| **flask-api-development** | ✅ Aktif | autoskills (MIT, aj-geddes) | 3.2 KB | Flask API — routing, blueprints, SQLAlchemy, JWT auth (9 file + references) |
| **android-adb-testing** | ✅ Aktif | Hermes (dipromosikan) | 15.5 KB | Use when testing Android apps on-device via ADB. |
| **bridge-migration** | ✅ Aktif | Hermes (dipromosikan) | 2.7 KB | Migrate bridge modules lost in refactor to a new runtime. |
| **cc-acehtengah-ops** | ✅ Aktif | Hermes (dipromosikan) | 17.5 KB | Operate cc-acehtengah: AI model, DTSEN sources, deploy. |
| **hermes-desktop-launcher** | ✅ Aktif | Hermes (dipromosikan) | 3.1 KB | Install Hermes Desktop to /Applications for Launchpad. |
| **hermes-terminal-workflows** | ✅ Aktif | Hermes (dipromosikan) | 5.3 KB | Hermes terminal shell pitfalls. |
| **plan** | ✅ Aktif | Hermes (dipromosikan) | 8.7 KB | Write a markdown plan to .hermes/plans/; no execution. |
| **positive-verification** | ✅ Aktif | Hermes (dipromosikan) | 2.4 KB | Verify hand-edited escapes before claiming the fix correct. |
| **repo-release-hygiene** | ✅ Aktif | Hermes (dipromosikan) | 2.1 KB | Promote hotfix branches to main and remove stale repo docs. |
| **safe-branch-refactor** | ✅ Aktif | Hermes (dipromosikan) | 2.9 KB | Safe refactor by duplicating branch and preserving UI. |
| **surgical-refactor** | ✅ Aktif | Hermes (dipromosikan) | 2.9 KB | Keep UI intact, replace only data/backend logic. |
| **swift-cli-development** | ✅ Aktif | Hermes (dipromosikan) | 7.6 KB | Swift CLI tools with SPM without Xcode.app — concurrency. |
| **vercel-deploy-check** | ✅ Aktif | Hermes (dipromosikan) | 2.5 KB | Verify a Next.js app is ready to deploy on Vercel. |
| **vnc-rfb-debugging** | ✅ Aktif | Hermes (dipromosikan) | 8.1 KB | Debug VNC/RFB protocol for macOS Screen Sharing.app. |
| **vnc-server-python** | ✅ Aktif | Hermes (dipromosikan) | 9.4 KB | > Implement VNC/RFB server in Python + ADB integration. |
| **delegated-output-verification** | ✅ Aktif | Bank Pusat | 8.0 KB | Verify files produced by delegated/parallel subagents BEFORE integration. Catches corrupted output (JSON-escap… |
| **niu-mission-control-ops** | ✅ Aktif | Bank Pusat | 3.6 KB | Operate the Niu-MissionControl dashboard server (port 5200): Next.js 15 runtime, SQLite backend, health checks… |
| **redesign-verification** | ✅ Aktif | Bank Pusat | 2.6 KB | Pitfall khusus untuk proyek redesign multi-fase: jangan klaim selesai tanpa verifikasi visual, jangan merge ba… |
| **web-dashboard-maintenance** | ✅ Aktif | Bank Pusat | 1.5 KB | Maintenance patterns for unified dashboards (Mission Control) using template-based generation. |
| **ponytail-core** | ✅ Aktif | Bank Pusat | 6.3 KB | > |
| **audit-finding-triage** | ✅ Aktif | Bank Pusat | 17.3 KB | Triage a large scanner/audit finding set. |
| **derived-artifact-consistency** | ✅ Aktif | Bank Pusat | 10.4 KB | Use when two tools report different totals for one set. |
| **live-ui-audit** | ✅ Aktif | Bank Pusat | 5.9 KB | Use when auditing a live web UI on mobile and desktop. |
| **llm-call-reliability** | ✅ Aktif | Bank Pusat | 6.5 KB | Use when LLM calls stall, time out, or return bad JSON. |
| **pre-cleanup-artifact-preservation** | ✅ Aktif | Bank Pusat | 7.1 KB | Before deleting refs or files, preserve the only copy. |
| **project-handover-package** | ✅ Aktif | Bank Pusat | 13.4 KB | Use when handing a project over to another team. |

## Domain: Design

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **impeccable** | ✅ Aktif | Claude Code / Jcode | 3.2 MB | Production-grade UI/UX design — v4.0.4: 23 sub-commands, detector anti-pattern, live iterate mode, OKLCH, craft-floor |
| **ui-ux-pro-max** | ✅ Aktif | Hermes USB | 29.5 KB | UI/UX design intelligence — 67 styles, 96 palettes, 57 font pairings, Python search |
| **accessibility** | ✅ Aktif | autoskills (MIT) | 12.3 KB | Audit web accessibility WCAG 2.2 — screen reader, keyboard nav, A11Y patterns, Lighthouse |
| **frontend-design** | ✅ Aktif | autoskills (Apache-2.0) | 4.4 KB | Anti-AI-slop frontend design — bold aesthetic direction, tipografi berkarakter, motion, komposisi spasial |
| **seo** | ✅ Aktif | autoskills (MIT) | 13.9 KB | Technical SEO — meta tags, structured data, sitemap, Lighthouse SEO audits |
| **dark-theme-a11y** | ✅ Aktif | Bank Pusat | 3.1 KB | Accessibility pitfalls specific to dark/glassmorphism themes. Covers CSS variable fallback mismatches, compute… |
| **web-accessibility-wcag** | ✅ Aktif | Bank Pusat | 4.8 KB | Audit & remediasi aksesibilitas web WCAG 2.1 AA + polish frontend + SEO untuk dashboard/SPA. Use when user min… |
| **mobile-viewport-remediation** | ✅ Aktif | Bank Pusat | 5.5 KB | Use when a page is not mobile-friendly on phones. |
| **responsive-ui-audit** | ✅ Aktif | Bank Pusat | 8.6 KB | Use when auditing or fixing live web UI/UX. |
| **web-ui-audit-measurement** | ✅ Aktif | Bank Pusat | 8.7 KB | Audit live web UI dengan bukti terukur. |

## Domain: Ecosystem
| **device-migration-disaster-recovery** | ✅ Aktif | Bank Pusat | 23.6 KB | Use when planning backup, restore, or device migration. |
| **external-pr-audit** | ✅ Aktif | Bank Pusat | 8.2 KB | Use when an external-agent PR/branch/artifact arrives for an ecosystem repo (Arena/designarena/agen luar lain)… |
| **mata-ops** | ✅ Aktif | Bank Pusat | 5.3 KB | Pull repo MATA dari GitHub & jalankan dashboard lokal :8080. |
| **model-status-checker** | ✅ Aktif | Bank Pusat | 4.9 KB | Model status checker. 3-tier probe for daily health cron. |
| **pi-app-studio-development** | ✅ Aktif | Bank Pusat | 8.5 KB | Build Pi Network apps via Pi App Studio or Pi SDK payments. |
| **pi-network-ecosystem** | ✅ Aktif | Bank Pusat | 5.3 KB | Pi Network — App Studio, Payments, Browser integration. |

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **up-eco** | ✅ Aktif | Hermes | 3.0 KB | Ecosystem status check — git, divergence, health |
| **ekosistem-scaffold** | ✅ Aktif | Hermes | 40.6 KB | Membuat struktur proyek baru sesuai standar Niumination |
| **hermes-agent-skill-authoring** | ✅ Aktif | Hermes USB | 10.7 KB | Author in-repo SKILL.md — frontmatter, validator, structure, quality principles |
| **hermes-uiux-technical** | ✅ Aktif | Niu-MissionControl | 4.2 KB | Capability profile UI/UX & technical Hermes Agent — routing, workflow automation, API/multi-agent, fast NLP, event-driven, conversational UX, agentic transparency, tone matching |
| **9router-model-mapping** | ✅ Aktif | Hermes (dipromosikan) | 5.0 KB | Configure and maintain 9router model mapping for Hermes — fallback chain, channel overrides, quota-aware model selection |
| **cc-acehtengah-maintenance** | ✅ Aktif | Hermes (dipromosikan) | 10.0 KB | cc-acehtengah branch reconciliation and UI or role fixes. |
| **composio** | ✅ Aktif | Hermes (dipromosikan) | 7.0 KB | Route and complete Composio work across Composio For You and Composio Platform. Use when the user mentions Composio; wants an agent to use apps such as Gmail, Slack, GitHub, Notion, Calendar, or Linea… |
| **dotfiles-maintenance** | ✅ Aktif | Hermes (dipromosikan) | 4.6 KB | Use when developing or fixing zaryu-terminal-dotfiles. |
| **ecosystem-architecture-adoption** | ✅ Aktif | Hermes (dipromosikan) | 2.5 KB | Adapt external architecture into existing project. |
| **ecosystem-bulk-push** | ✅ Aktif | Hermes (dipromosikan) | 2.8 KB | Use when pushing many ecosystem repos to GitHub at once. |
| **ecosystem-dox-maintenance** | ✅ Aktif | Hermes (dipromosikan) | 3.9 KB | Audit and repair DOX/SOUL hygiene across the ecosystem. |
| **ecosystem-gitops** | ✅ Aktif | Hermes (dipromosikan) | 2.6 KB | Use when migrating GitHub remotes HTTPS/SSH or bulk remotes. |
| **ecosystem-provider-management** | ✅ Aktif | Hermes (dipromosikan) | 8.1 KB | Provider AI lintas 3 agent + pilih model produksi. |
| **ecosystem-recovery** | ✅ Aktif | Hermes (dipromosikan) | 7.5 KB | Full ecosystem recovery after delete or up-eco failures. |
| **external-patch-adoption** | ✅ Aktif | Hermes (dipromosikan) | 3.1 KB | Apply an external patch stack to an ecosystem repo safely. |
| **hermes-configuration** | ✅ Aktif | Hermes (dipromosikan) | 20.9 KB | Configure Hermes for Niumination: model mapping, hooks, MCP. |
| **hermes-gateway-dm-troubleshooting** | ✅ Aktif | Hermes (dipromosikan) | 6.8 KB | Diagnose Hermes gateway errors and Telegram DM delays |
| **model-checker** | ✅ Aktif | Hermes (dipromosikan) | 2.6 KB | Cek semua model 9router yang tersedia, test aksesibilitas, kategorikan gratis vs berbayar. Trigger via chat "/model-check" atau "cek model". Hasil: laporan markdown di scripts/model-checker-report.md … |
| **niu-9router-maintain** | ✅ Aktif | Hermes (dipromosikan) | 6.9 KB | Maintenance router model lokal 9router (localhost:20128) untuk ekosistem Niumination — health check, tes akses semua model, disable provider/model yang gagal, restart daemon otomatis. Gunakan saat use… |
| **niumination-reference-adoption** | ✅ Aktif | Hermes (dipromosikan) | 4.5 KB | Adopt ecosystem references and zips into skill bank. |
| **pi-solohost-development** | ✅ Aktif | Hermes (dipromosikan) | 2.3 KB | Build and submit apps to Pi Network SoloHost. |
| **sapa-ai-ops** | ✅ Aktif | Hermes (dipromosikan) | 5.3 KB | Operate sapa-ai SPLP service. |
| **config-history-review** | ✅ Aktif | Bank Pusat | 4.4 KB | Review Hermes config history using filesystem evidence (backup files, changelogs, git logs) — NOT session sear… |
| **ecosystem-snapshot** | ✅ Aktif | Bank Pusat | 11.0 KB | Generate a comprehensive ecosystem configuration snapshot for Niumination. Produces a Markdown document captur… |
| **ecosystem-tool-adoption** | ✅ Aktif | Bank Pusat | 12.5 KB | Workflow studi & adopsi tool/proyek pihak ketiga ke ekosistem Niumination — deep study (clone + baca source),… |
| **ekosistem-content-verification** | ✅ Aktif | Bank Pusat | 7.4 KB | Verify web/JSON content accuracy against source documents (DOCX/XLSX) for Niumination ecosystem projects — ext… |
| **hermes-provider-config** | ✅ Aktif | Bank Pusat | 47.4 KB | > |
| **integration-verification** | ✅ Aktif | Bank Pusat | 1.9 KB | Verify whether external services, APIs, or toolkits are actually connected and working end-to-end. Use when ch… |
| **kanban-ecosystem-management** | ✅ Aktif | Bank Pusat | 98.8 KB | Track Niumination project portfolio via Hermes kanban. Covers: mapping AGENTS.md project catalog → kanban task… |
| **niu-mission-control-ui** | ✅ Aktif | Bank Pusat | 10.8 KB | Frontend Niumination Mission Control — unified dashboard (ORB iframe + 12 floating windows), WCAG 2.1 AA acces… |
| **provider-fallback** | ✅ Aktif | Bank Pusat | 13.7 KB | Handle AI provider failures and fallback to working providers |
| **skill-bank-management** | ✅ Aktif | Bank Pusat | 12.9 KB | Kelola Skill Bank Niumination (single source of truth ~/Desktop/Niumination/skills/) — manifest SHA-256, sync… |
| **weathernext-gayo** | ✅ Aktif | Bank Pusat | 2.7 KB | Analisis cuaca mikro dan peringatan dini bencana untuk dataran tinggi Gayo (Aceh Tengah) berbasis pipeline Wea… |
| **model-mapping-repair** | ✅ Aktif | Bank Pusat | 7.7 KB | Use when a model mapping points at a dead provider. |
| **sapa-ai** | ✅ Aktif | Bank Pusat | 13.3 KB | Use when working on sapa-ai. |
| **provider-model-verification** | ✅ Aktif | Bank Pusat | 3.3 KB | Verify an AI provider/model before relying on it. |
| **vercel-domain-pointing** | ✅ Aktif | Bank Pusat | 4.1 KB | Point custom domain to Vercel — nameserver, DNS, verify. |
| **ecosystem-hibernation** | ✅ Aktif | Bank Pusat | 10.7 KB | Use when a project must be retired temporarily: archive GitHub, pause Vercel, back up to vault, delete the loc… |
| **vercel-dns-subdomain-debug** | ✅ Aktif | Bank Pusat | 5.3 KB | >- |
| **arena-patch-adoption** | ✅ Aktif | Bank Pusat | 4.0 KB | Use when applying arena.ai zip patch stacks to a repo. |
| **ffmpeg-ken-burns-motion** | ✅ Aktif | Bank Pusat | 2.2 KB | Use when making still cards move: FFmpeg zoompan + mux VO. |
| **hyperframes-vertical-video** | ✅ Aktif | Bank Pusat | 0.1 KB | probe3 |
| **reels-motion-render** | ✅ Aktif | Bank Pusat | 5.9 KB | Use when rendering a Reels/TikTok video with HyperFrames. |
| **revideo-motion-graphic** | ✅ Aktif | Bank Pusat | 4.4 KB | Use for motion-graphic videos: Revideo, Piper VO, FFmpeg. |
| **system-one-decisions** | ✅ Aktif | Bank Pusat | 4.7 KB | Use when calling decision models (jev/systemone) via 9router. |
| **provider-vetting** | ✅ Aktif | Bank Pusat | 6.5 KB | Use when vetting a third-party AI model before adopting it. |
| **ecosystem-live-status-reporting** | ✅ Aktif | Bank Pusat | 4.6 KB | Use when producing live verified ecosystem status reports. |
| **niumination-ecosystem-change-discipline** | ✅ Aktif | Bank Pusat | 5.8 KB | Editing Niumination files or committing to repos. |
| **niumination-repo-commit-discipline** | ✅ Aktif | Bank Pusat | 7.0 KB | Committing changes to Niumination git repos. |

## Domain: Security

| Skill | Status | Source | Deskripsi |
|-------|:------:|--------|-----------|
| **redteam** | ✅ Aktif | Agentpedia + Niumination | 4.0 KB | Adversarial security testing — stress-test plan dari sudut pandang attacker |
| **git-security-sanitization** | ✅ Aktif | Hermes (dipromosikan) | 3.4 KB | Clean credential/PII leaks and add secret-scanning gates. |
| **production-secret-rotation** | ✅ Aktif | Bank Pusat | Rotate a live production credential; prove the old is dead. |

## Domain: Creative

| Skill | Status | Source | Deskripsi |
|-------|:------:|--------|-----------|
| **ghost** | ✅ Aktif | sisi-tarak + Niumination | 3.2 KB | AI text humanizer — rewrite AI-generated text to read naturally |
| **hyperframes** | ✅ Aktif | heygen-com/hyperframes | 4.0 KB | HTML-to-video framework — 'Write HTML. Render video. Built for agents.' |
| **free-tier-reels** | ✅ Aktif | Hermes (dipromosikan) | 7.3 KB | Free-tier Reels creation workflow. |
| **ascii-art** | ✅ Aktif | Bank Pusat | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. |
| **comfyui** | ✅ Aktif | Bank Pusat | Generate images, video, and audio via diffusion workflows. |
| **excalidraw** | ✅ Aktif | Bank Pusat | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). |
| **gemini-vo-narration** | ✅ Aktif | Bank Pusat | Voice-over narasi Bahasa Indonesia standar Niumination (Gemini TTS, gratis). Pakai saat membuat VO/narasi/dubb… |
| **pretext** | ✅ Aktif | Bank Pusat | Build creative browser demos with DOM-free text layout. |
| **sketch** | ✅ Aktif | Bank Pusat | Throwaway HTML mockups: 2-3 design variants to compare. |
| **touchdesigner-mcp** | ✅ Aktif | Bank Pusat | Control TouchDesigner via twozero MCP. |
| **content-pipeline-readiness** | ✅ Aktif | Bank Pusat | Use when checking content production & publish readiness. |
| **short-form-video-production** | ✅ Aktif | Bank Pusat | Make ready-to-post vertical video (Reels) at zero cost. |

---

## Domain: Note-taking

| Skill | Status | Source | Deskripsi |
|-------|:------:|--------|-----------|
| **routines** | ✅ Aktif | Hermes USB | 1.8 KB | Routine workflows — morning brief, daily report, project sync via /routine command |
| **ai-agency** | ✅ Aktif | Hermes USB | 2.5 KB | AI Agency output layer — laporan otomatis, draft konten, data mining dari brain |
| **second-brain** | ✅ Aktif | Hermes USB | 2.2 KB | Second Brain PKM — simpan catatan ke brain/inbox + cari dengan ranking (recency + keyword) |

---

## Domain: Autonomous AI Agents

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **merge-reconciler** | ✅ Aktif | Hermes (dipromosikan) | 7.4 KB | Neutral third-party resolution of agent merge conflicts. |
| **telegram-router-orchestration** | ✅ Aktif | Bank Pusat | 30.5 KB | Mengelola persona, skills, dan model override per-thread Telegram di Hermes Gateway, termasuk integrasi dengan… |

---

## Domain: DevOps

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **env-doctor** | ✅ Aktif | Hermes (dipromosikan) | 6.7 KB | Recover dotfiles and shell after Stow or bulk delete. |
| **macos-launchd-services** | ✅ Aktif | Hermes (dipromosikan) | 9.0 KB | Keep macOS always-on services alive; recover launchd plists. |
| **production-env-vars** | ✅ Aktif | Bank Pusat | 4.2 KB | Use when changing or rotating env vars on a live app (Vercel). Decode pulled values, verify functionally, keep a rollback path. |
| **containerization-readiness-audit** | ✅ Aktif | Bank Pusat | 4.6 KB | Use when asked which projects need Docker. |
| **gh-pages-build-fix** | ✅ Aktif | Bank Pusat | 1.7 KB | Fix GitHub Pages Jekyll checkout failures. |
| **github-pages-deploy** | ✅ Aktif | Bank Pusat | 11.5 KB | Deploy static HTML to GitHub Pages via clean branch. |
| **snapshot-verification** | ✅ Aktif | Bank Pusat | 7.3 KB | Verify static snapshot deployment and content. |

---

## Domain: GitHub

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **github-auth** | ✅ Aktif | Hermes (dipromosikan) | 11.7 KB | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. |
| **github-auth-recovery** | ✅ Aktif | Hermes (dipromosikan) | 3.0 KB | Recover broken GitHub auth and rotate compromised keys. |
| **github-code-review** | ✅ Aktif | Hermes (dipromosikan) | 13.3 KB | Review PRs: diffs, inline comments via gh or REST. |
| **github-issue-to-pr** | ✅ Aktif | Hermes (dipromosikan) | 5.9 KB | Carry a GitHub issue to a verified PR with honest CI state. |
| **github-issues** | ✅ Aktif | Hermes (dipromosikan) | 9.1 KB | Create, triage, label, assign GitHub issues via gh or REST. |
| **github-pr-workflow** | ✅ Aktif | Hermes (dipromosikan) | 9.8 KB | GitHub PR lifecycle: branch, commit, open, CI, merge. |
| **github-repo-management** | ✅ Aktif | Hermes (dipromosikan) | 13.4 KB | Clone/create/fork repos; manage remotes, releases. |

---

## Domain: Productivity

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **nano-pdf** | ✅ Aktif | Hermes (dipromosikan) | 1.6 KB | Edit text in existing PDFs via natural-language prompts. |
| **ocr-and-documents** | ✅ Aktif | Hermes (dipromosikan) | 5.6 KB | Extract text from PDFs/scans (pymupdf, marker-pdf). |
| **session-librarian** | ✅ Aktif | Hermes (dipromosikan) | 4.7 KB | Organize sessions by prompt: find, rename, archive, prune. |
| **skp-e-kinerja** | ✅ Aktif | Hermes (dipromosikan) | 4.0 KB | Generate SKP concept from session data for reporting. |

---

## Domain: Research

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **blogwatcher** | ✅ Aktif | Hermes (dipromosikan) | 5.0 KB | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. |
| **research-paper-writing** | ✅ Aktif | Hermes (dipromosikan) | 70.5 KB | Write ML papers for NeurIPS/ICML/ICLR: design→submit. |

---

---

## Domain: Development

Pengembangan aplikasi (bank) — proyek & tooling development.

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **pi-app-studio** | ✅ Aktif | Bank Pusat | 6.1 KB | Use when building Pi apps via App Studio. Auth and payments. |

## Domain: MLOps

MLOps & inference — subkategori: `inference/`, `evaluation/`.

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **evaluating-llms-harness** | ✅ Aktif | Bank Pusat | 11.9 KB | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). |
| **weights-and-biases** | ✅ Aktif | Bank Pusat | 12.4 KB | W&B: log ML experiments, sweeps, model registry, dashboards. |
| **huggingface-hub** | ✅ Aktif | Bank Pusat | 3.6 KB | HuggingFace hf CLI: search/download/upload models, datasets. |
| **llama-cpp** | ✅ Aktif | Bank Pusat | 8.7 KB | llama.cpp local GGUF inference + HF Hub model discovery. |
| **serving-llms-vllm** | ✅ Aktif | Bank Pusat | 9.1 KB | vLLM: high-throughput LLM serving, OpenAI API, quantization. |

## Domain: Smart Home

Otomasi rumah.

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **openhue** | ✅ Aktif | Bank Pusat | 2.8 KB | Control Philips Hue lights, scenes, rooms via OpenHue CLI. |

## Domain: Standalone (root bank)

Skill yang tidak berada dalam folder domain (langsung di `skills/`).

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **camofox-browser** | ✅ Aktif | Bank Pusat | 6.9 KB | Manage Camofox stealth browser at localhost:9377. |
| **credential-vault-backup** | ✅ Aktif | Bank Pusat | 4.1 KB | Back up Niumination credentials into a single vault. |
| **polling-script-management** | ✅ Aktif | Bank Pusat | 2.7 KB | Stop polling script notification spam via debounce. |
| **repo-zip-overlay** | ✅ Aktif | Bank Pusat | 2.0 KB | Overlay a zip onto a git repo, preserving local config. |

---

## Domain: Governance

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **gdpr-compliance** | ✅ Aktif | Bank Pusat | 14.1 KB | > |
| **niu-core-governance** | ✅ Aktif | Bank Pusat | 8.8 KB | > |

## Domain: Content

| Skill | Status | Source | Ukuran | Deskripsi |
|-------|:------:|--------|-------:|-----------|
| **code-audit** | ✅ Aktif | Bank Pusat | 11.9 KB | Audit kode hasil AI: celah, slop, biaya, dan laporan klien |
| **content-legal** | ✅ Aktif | Bank Pusat | 7.0 KB | Audit lisensi, AI disclosure, izin, dan kontrak konten |
| **content-monetize** | ✅ Aktif | Bank Pusat | 8.1 KB | Rate card, media kit, proposal, invoice, outreach klien |
| **content-produce** | ✅ Aktif | Bank Pusat | 10.4 KB | Produksi video, audio, gambar dengan stack open source |
| **content-publish** | ✅ Aktif | Bank Pusat | 6.5 KB | Adaptasi multi-platform, penjadwalan, dan analitik |
| **content-research** | ✅ Aktif | Bank Pusat | 5.4 KB | Riset tren, keyword, audiens, dan bedah kompetitor |
| **content-script** | ✅ Aktif | Bank Pusat | 5.6 KB | Hook, naskah, storyboard, caption, dan copywriting |
| **content-studio** | ✅ Aktif | Bank Pusat | 7.6 KB | Produser studio konten: pipeline ide sampai cuan |

## Ringkasan

| Status | Jumlah |
|--------|:------:|
| ✅ Aktif | **180** |
| **Total** | **180** |

## Catatan Penting — Potensi Konflik

### 🔴 Konflik Aktif (perlu mitigasi)

| Konflik | Skill 1 | Skill 2 | Mitigasi |
|---------|:-------:|:-------:|----------|
| 🟡 **Craftsmanship vs Minimalism** | `ultrathink` | `ponytail-core` | Ultrathink sudah punya Relationship section yang menjelaskan kapan pakai mana. Ponytail untuk implementasi cepat, ultrathink untuk arsitektur. |
| 🟡 **UI/UX - Build vs Research** | `impeccable` | `ui-ux-pro-max` | Beda fokus: impeccable = code-first, build UI langsung. ui-ux-pro-max = search-based, design research & recommendation. Trigger berbeda: `/impeccable craft` vs `/ui-ux-pro-max --design-system`. |
| 🟡 **Debugging - Generic vs Agresif** | `systematic-debugging` | `hermes-zero-defect-architect` | systematic-debugging = 4-phase generik. zero-defect = full pipeline + snapshot/rollback + JCode parallel. zero-defect adalah superset untuk Hermes + JCode environment. |

### 🟢 Konflik Terkelola (aman)

| Pair | Alasan |
|------|--------|
| `ponytail-audit` ↔ `ponytail-review` | Komplementer: audit = whole-repo, review = diff-level |
| `ponytail-core` ↔ `simplify-code` | core = mental model sebelum nulis, simplify-code = refactor kode existing |
| `impeccable` ↔ `ghost` | Beda domain: UI/UX design vs text humanizer |
| `hermes-agent-skill-authoring` ↔ semua | Meta-skill — justru membantu maintain skill lain |
| `brainstorming` ↔ `ultrathink` | Komplementer: brainstorming = "apa yang dibangun", ultrathink = "gimana arsitekturnya" |
| `brainstorming` ↔ `ponytail-core` | Sama-sama YAGNI — brainstorming cegah fitur tidak perlu sebelum coding |
| `verification-before-completion` ↔ `ponytail-core` | Komplementer: ponytail minimal code, verification buktikan kode beneran jalan |
| `verification-before-completion` ↔ `systematic-debugging` | Verification adalah fase final debugging — cocok berurutan |
| `subagent-driven-development` ↔ semua | Layer orchestration — tidak konflik, menjalankan skill lain via subagent |
| `requesting-code-review` ↔ `ponytail-review` | Beda fokus: ponytail = over-engineering check, requesting = spec compliance + quality |
| `writing-plans` ↔ `brainstorming` | **Pipeline:** brainstorming → writing-plans → subagent-driven-development → requesting-code-review → finishing-a-development-branch |
| `finishing-a-development-branch` ↔ `up-eco` | finishing = cleanup satu branch, up-eco = sync seluruh ekosistem

### 📌 Catatan Lain

- **Naming convention:** `<domain>/<nama>-<variant>/SKILL.md`
- **Versioning:** Cukup git history untuk tahap awal
- **Optimization:** minimal version dari Jcode bundled skill
- **Frontmatter YAML:** setiap skill wajib punya name, description, version, tags

## Cara Nambah Skill Baru

1. Bikin folder: `mkdir -p skills/<domain>/<nama>/`
2. Tulis SKILL.md dengan frontmatter YAML + markdown instruksi
3. Update INDEX.md — tambah baris di tabel yang sesuai
4. `git add skills/ && git commit -m "skills: tambah <nama>"`

## Format SKILL.md (Template)

```yaml
---
name: <skill-name>
description: "<satu kalimat deskripsi>"
version: 1.0.0
author: <Hermes|Jcode|Agentpedia>
source: <dari mana asalnya>
tags: [<domain>, <keyword1>, <keyword2>]
platforms: [macos, linux]
---
# <Nama Skill — Judul Manusiawi>

## Trigger
Kapan skill ini harus dipakai?

## Prasyarat
- Item 1
- Item 2

## Prosedur
1. Langkah 1
2. Langkah 2
3. Langkah 3

## Contoh
...
```

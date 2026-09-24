# Referensi Adopsi — 161 Repo Di-Star oleh @Niumination

**Tanggal:** 2026-09-24 | **Sumber:** GitHub API `users/Niumination/starred` (2 halaman, 100+61)
**Tujuan:** Daftar lengkap repo yang di-star akun Niumination + analisis kandidat adopsi ke ekosistem.
**Catatan:** Angka star = kondisi live saat fetch. Lisensi dicek via GitHub API (`license.spdx_id`), repo tanpa lisensi ditandai ⚠️.

---

## 1. Ringkasan Eksekutif

- **Total repo di-star: 161** (100 terbaru + 61 halaman 2).
- **112 repo (70%) relevan untuk adopsi** ke ekosistem Niumination berdasarkan keyword: browser-agent, decision-engine, video-AI, MCP, RAG/memory, Android, AI-core, OS-experiment, workflow.
- **49 repo kategori OS-experiment / dotfiles** (Hyprland, NixOS, WSL, Docker-OSX, Windows-ARM) — **bukan prioritas** untuk ekosistem Mac-first saat ini, tapi menunjukkan minat riset OS alternatif.
- **Lisensi: 134/161 terlacak**; 27 tanpa lisensi eksplisit (⚠️ jangan disalin ke produk komersial tanpa izin).
- **3 temuan penting untuk ekosistem:**
  1. **Konteks ekosistem kita sudah kuat** (hyperframes, UACC, autoskills, laya, opendataloader-pdf, Agent-Reach, impeccable, codebase-memory-mcp sudah dipakai/di-star).
  2. **Banyak repo AI-agent/harness baru** (ECC, deepseek-harness, prime-agent, orca, council-of-high-intelligence) — sinyal kuat arah "harness + skills".
  3. **Rumpun browser-agent** (browser-use: workflow-use, browsercode, jev-ultrafast, video-use; Agent-Reach) — sudah relevan dengan MC/agent stack kita.
- **Fokus revisi (24 Sep 19:40):** 2 rumpun yang PALING BARU di-star — **`browser-use/*`** (browser agent framework) dan **`laya`** (System 1 decision engine) — ditambahkan ke P0. Rincian di seksi 4.2.

---

## 2. Kandidat Adopsi Prioritas (Top 15 oleh stars, relevan, lisensi aman)

| # | Repo | ★ | Lisensi | Kategori | Alasan Relevan |
|---|---|---|---|---|---|
| 1 | `affaan-m/ECC` | 266.6k | MIT | harness, skills | Agent harness performance optimization — skills+instincts+cost control. Bisa jadi blueprint skill-bank kita. |
| 2 | `deepseek-ai/deepseek-harness` | 235.0k | MIT | harness | "Everything is a Plugin" — plugin arsitektur, cocok dengan konsep MC plugin/hook. |
| 3 | `Shubhamsaboo/awesome-llm-apps` | 139.6k | Apache-2.0 | RAG, agents | 100+ AI agents & RAG apps — referensi library pola. |
| 4 | `harry0703/MoneyPrinterTurbo` | 125.5k | MIT | video-AI | Generate short video otomatis — relevan konten Reels/Youtube (content-produce). |
| 5 | `addyosmani/agent-skills` | 98.8k | MIT | skills | Production-grade engineering skills for AI agents — **langsung relevan skill bank** (subset autoskills, sudah dipakai 7/11). |
| 6 | `thedotmack/claude-mem` | 94.6k | Apache-2.0 | memory, sessions | Persistent context across sessions — relevan second brain / memory Hermes. |
| 7 | `Panniantong/Agent-Reach` | 85.2k | MIT | web agent | Read & search internet untuk agent — relevan agent-reach skill. |
| 8 | `stablyai/orca` | 77.3k | MIT | fleet agent | ADE untuk fleet of parallel agents — relevan orkestrasi MC. |
| 9 | `pbakaus/impeccable` | 70.7k | Apache-2.0 | design | Design language untuk AI harness — relevan impeccable skill (sudah ada). |
| 10 | `diegosouzapw/OmniRoute` | 69.8k | MIT | gateway | Free MIT AI gateway, 359 providers — relevan 9router replacement/alternatif. |
| 11 | `openinterpreter/openinterpreter` | 68.4k | Apache-2.0 | coding agent | Coding agent open models — relevan cc-switch stack. |
| 12 | `jingyaogong/minimind` | 62.5k | Apache-2.0 | LLM training | Train 64M LLM dari nol dalam 2 jam — edukasi/research. |
| 13 | `heygen-com/hyperframes` | 52.8k | Apache-2.0 | video-AI | Write HTML → render video — **sudah ada skill hyperframes**. |
| 14 | `charmbracelet/crush` | 28.3k | NOASSERTION | agentic coding | Agentic coding glamour — relevan opencode ecosystem. |
| 15 | `Kilo-Org/kilocode` | 27.4k | MIT | engineering platform | All-in-one agentic engineering — bisa jadi alternatif IDE/harness. |

## 3. Daftar Lengkap 161 Repo (urut API: terbaru di-star dulu)

### Blok A — 30 repo terbaru di-star (browser-agent, decision, video, harness)
1. `browser-use/workflow-use` ★4192 AGPL-3.0 — RPA workflows
2. `browser-use/browsercode` ★752 MIT — browser-native agent framework
3. `browser-use/video-use` ★26782 MIT — edit video dgn coding agents
4. `browser-use/jev-ultrafast` ★19658 MIT — web agent tercepat
5. `NandhaKishorM/laya` ★22501 Apache-2.0 — System 1 decision engine
6. `mizorewww/laya-mlx` ★6166 Apache-2.0 — MLX runtime utk Laya
7. `ipenywis/laya-ultrafast` ★162 MIT — Laya versi cepat
8. `krillinai/OpenCreator` ★12313 Apache-2.0 — AI workspace creator
9. `cactus-compute/needle` ★12498 Apache-2.0 — automation foundation model tiny devices
10. `atria-asi/Atria-Dawn-Preview` ★551 MIT — model dipakai thread 1
11. `Homebrew/brew` ★49765 BSD-2-Clause — package manager
12. `Lakr233/vphone-cli` ★14343 MIT — virtual phone
13. `jqssun/android-titanium-browser` ★2705 GPL-2.0 — secure Android browser
14. `Fikaramandio/korpus-bahasa-Gayo` ★3 NO-LICENSE — korpus bahasa Gayo ⚠️
15. `jingyaogong/minimind` ★62453 Apache-2.0 — train 64M LLM
16. `techjarves/Mobile-Harness` ★397 MIT — Claude Code on Android
17. `vinzdg/codenotch` ★2453 MIT — macOS usage limits agent
18. `Shubhamsaboo/awesome-llm-apps` ★139636 Apache-2.0 — 100+ AI agents
19. `affaan-m/ECC` ★266633 MIT — agent harness optimization
20. `HKUDS/RAG-Anything` ★23414 MIT — all-in-one RAG
21. `runpod/runpod-mcp` ★78 NOASSERTION — MCP ⚠️
22. `ilyamiro/serpantinum` ★7002 AGPL-3.0 — wayland shell
23. `AbuZar-Ansarii/Needle` ★122 NO-LICENSE — 14 MB agentic LLM ⚠️
24. `termux/termux-app` ★61343 NOASSERTION — terminal Android ⚠️
25. `Imtiaz-Official/Smart-Edge` ★402 MIT — edge AI
26. `tashfeenahmed/freellmapi` ★28433 MIT — free LLM providers
27. `mukul975/Anthropic-Cybersecurity-Skills` ★33316 Apache-2.0 — 817 cyber skills
28. `RyanCodrai/turbovec` ★17233 MIT — Rust vector index
29. `rowboatlabs/rowboat` ★17963 Apache-2.0 — AI coworker memory
30. `cadence-workflow/cadence` ★9453 Apache-2.0 — distributed orchestration

### Blok B — 31 repo berikutnya (UI, harness, agent stack)
31. `pctrade/end4-pC` ★3147 GPL-3.0 — custom end4
32. `mikcyber/zrouter` ★5 MIT — router
33. `heroui-inc/heroui` ★30812 Apache-2.0 — React UI library (NextUI)
34. `tinyhumansai/openhuman` ★40088 GPL-3.0 — agent harness
35. `deepseek-ai/deepseek-harness` ★235015 MIT — everything is a plugin
36. `Ryoku-dev/ryoku` ★1089 GPL-3.0 — Arch workstation
37. `filiksyos/gitreverse` ★1935 NO-LICENSE — reverse engineer repo ⚠️
38. `XiaoYouChR/Ghost-Downloader-3` ★9253 GPL-3.0 — downloader
39. `RubenM1990/APEX-UI` ★83 MIT — APEX front interface
40. `yashab-cyber/opendroid` ★1069 NOASSERTION — Android agent ⚠️
41. `donnemartin/system-design-primer` ★371552 NOASSERTION — system design ⚠️
42. `DioxusLabs/dioxus` ★39230 Apache-2.0 — fullstack Rust
43. `cloudflare/cloudflare-os` ★10099 Apache-2.0 — agent workspace
44. `midudev/autoskills` ★6895 NOASSERTION — skill stack ⚠️ (sudah diadopsi 7/11)
45. `Gaurav-Gosain/tuios` ★3715 MIT — terminal WM agents
46. `WyattBlue/auto-editor` ★5349 Unlicense — video editing
47. `chaitanyagiri/munder-difflin` ★7909 MIT — local multi-agent harness
48. `PrimeIntellect-ai/prime-agent` ★21270 MIT — RLM coding agent
49. `pascalorg/editor` ★24281 MIT — 3D architectural editor
50. `modimihir07/AgriAssist-AI` ★2 MIT — crop disease detection
51. `termuxhexrt/renzu-worm-v2` ★10 Apache-2.0 — worm (⚠️ security)
52. `semantica-agi/semantica` ★13451 MIT — graph-native context infra
53. `koala73/worldmonitor` ★87322 AGPL-3.0 — global intelligence dashboard
54. `phoneintel/phoneintel` ★309 GPL-3.0 — OSINT phone
55. `FareedKhan-dev/kimi-k3-in-c` ★8523 Apache-2.0 — Kimi K3 inference CPU
56. `techchipnet/CamPhish` ★5133 GPL-3.0 — cam phishing ⚠️
57. `SAGAR-TAMANG/ultron-by-sagar-builds` ★914 MIT — Ultron
58. `yakhyo/uniface` ★1775 MIT — face analysis
59. `Panniantong/Agent-Reach` ★85237 MIT — web agent eyes
60. `Shrey113/Android-Dex` ★2666 NO-LICENSE — Samsung DeX alternative ⚠️
61. `openinterpreter/openinterpreter` ★68428 Apache-2.0 — open models agent

### Blok C — 30 repo berikutnya (video, OS, MCP, RAG)
62. `shaikhtaha258-maker/Hand-gesture-vfx` ★7 NO-LICENSE — gesture vfx ⚠️
63. `himanshusahu-07/Apex.desktop-assistant` ★1 NO-LICENSE — desktop assistant ⚠️
64. `dockur/macos` ★21574 MIT — macOS in Docker
65. `block/buzz` ★34240 Apache-2.0 — hive mind comm
66. `heygen-com/hyperframes` ★52827 Apache-2.0 — write HTML render video
67. `JustinGamer191/Holo` ★916 MIT — ? 
68. `moeru-ai/airi` ★49366 MIT — Grok companion
69. `sickn33/agentic-awesome-skills` ★46865 MIT — AAS core control plane
70. `opendataloader-project/opendataloader-pdf` ★29361 Apache-2.0 — PDF parser (sudah jadi skill document-content-pipeline)
71. `dpaidev/opendataloader-pdf` ★2 Apache-2.0 — mirror
72. `chrisjaron03/UACC` ★39 MIT — UACC (sudah ada skill/mcp)
73. `kholmogorov27/chevron` ★401 MIT — startpage
74. `a-ghorbani/pocketpal-ai` ★8399 MIT — LLM on phone
75. `mlc-ai/web-llm-chat` ★1108 Apache-2.0 — LLM in browser
76. `JustVugg/colibri` ★37486 Apache-2.0 — pure C MoE inference
77. `addyosmani/agent-skills` ★98837 MIT — engineering skills (sudah diadopsi)
78. `stablyai/orca` ★77316 MIT — fleet agent ADE
79. `diegosouzapw/OmniRoute` ★69829 MIT — AI gateway 359 providers
80. `Netw0rkNoob/VulnClaw` ★3435 MIT — AI agent pentest
81. `0xNyk/council-of-high-intelligence` ★4498 MIT — multi-perspective deliberation
82. `facebook/astryx` ★13346 MIT — design system
83. `allenai/olmocr` ★19656 Apache-2.0 — PDF linearization
84. `baairon/torlink` ★5774 MIT — torrent finder
85. `firecrawl/open-agent-builder` ★2637 NO-LICENSE — visual workflow builder ⚠️
86. `yashab-cyber/metasploit-ai` ★71 NOASSERTION — metasploit AI ⚠️
87. `calesthio/OpenMontage` ★61151 AGPL-3.0 — agentic video production
88. `harry0703/MoneyPrinterTurbo` ★125480 MIT — short video generator
89. `pbakaus/impeccable` ★70697 Apache-2.0 — design language (sudah ada skill)
90. `zai-org/GLM-5` ★7234 Apache-2.0 — vibe coding → agentic engineering
91. `Kilo-Org/kilocode` ★27407 MIT — all-in-one agentic platform
92. `DeusData/codebase-memory-mcp` ★44811 MIT — codebase intelligence MCP

### Blok D — 31 repo pertama (OS-experiment, dotfiles, WSL, dll)
93. `Kong/insomnia` ★40030 Apache-2.0 — API client
94. `awesome-opencode/awesome-opencode` ★10369 CC0-1.0 — awesome list opencode
95. `lmarena/lmarena.github.io` ★25 MIT — lmarena
96. `elder-plinius/G0DM0D3` ★11306 AGPL-3.0 — liberate AI chat
97. `666ghj/MiroFish` ★74445 AGPL-3.0 — swarm intelligence
98. `charmbracelet/crush` ★28281 NOASSERTION — agentic coding ⚠️
99. `frayude/throttnux` ★77 NO-LICENSE — bandwidth limit ⚠️
100. `Alishahryar1/free-claude-code` ★55850 MIT — free harnesses
101. `hassanmsthf11/unlimited-claude-AI` ★420 MIT — free Claude ⚠️
102. `thedotmack/crabspace-app` ★9 NO-LICENSE — MySpace for agents ⚠️
103. `thedotmack/claude-mem` ★94604 Apache-2.0 — persistent context
104. `gnovotny/nothing-to-watch` ★673 NOASSERTION — webgl gallery ⚠️
105. `docfork/docfork` ★488 MIT — up-to-date docs for agents
106. `uiriansan/SilentSDDM` ★1664 GPL-3.0 — SDDM theme
107. `Nano-Industries-Private-Limited/RadarScope-ESP32` ★80 NO-LICENSE — radar ESP32 ⚠️
108. `runcat-dev/RunCat365` ★10313 Apache-2.0 — cute cat taskbar
109. `Jackywine/Bella` ★6370 NO-LICENSE — Bella ⚠️
110. `bytebot-ai/bytebot` ★11085 Apache-2.0 — desktop agent automation
111. `junegunn/fzf` ★83235 MIT — fuzzy finder
112. `shobrook/termite` ★419 Apache-2.0 — generative UI terminal
113. `denoobaprolinux/sebekdots-eng` ★7 GPL-3.0 — Hyprland dotfiles
114. `raybbian/hyprtasking` ★381 BSD-3-Clause — workspace plugin
115. `ChimeraOS/chimeraos` ★2001 MIT — couch gaming OS
116. `ARKye03/dotfiles` ★105 Unlicense — Arch dotfiles
117. `TheRiceCold/kaizen` ★55 MIT — productive desktop
118. `gh0stzk/dotfiles` ★4743 GPL-3.0 — BSPWM 18 themes
119. `prasanthrangan/hyprdots` ★8494 GPL-3.0 — Arch hyprland dots
120. `Pahasara/HyprDots` ★206 MIT — hyprland dots
121. `Benexl/yt-x` ★1660 MIT — youtube browse script
122. `anotherhadi/nixy` ★560 MIT — Hyprland ecosystem
123. `vasujain275/rudra` ★161 NO-LICENSE — Nix + Hyprland ⚠️
124. `Serpentian/AlfheimOS` ★157 NO-LICENSE — NixOS + hyprland ⚠️
125. `donovanglover/hyprnome` ★201 GPL-3.0 — GNOME-like switching
126. `RicArch97/nixos-config` ★46 NO-LICENSE — NixOS flakes ⚠️
127. `garcia-s/yara-embedder` ★32 NO-LICENSE — flutter wayland ⚠️
128. `EchterAlsFake/Porn_Fetch` ★355 GPL-3.0 — downloader ⚠️
129. `johe123qwe/github-trending` ★61 MIT — GitHub trending scrape
130. `Thomashighbaugh/stars` ★22 NO-LICENSE — curated stars ⚠️
131. `hiifong/starList` ★18 MIT — export stars
132. `Andrey0189/nixos-config` ★386 BSD-2-Clause — NixOS config
133. `sandeng1440/nixos-config` ★14 GPL-3.0 — nixos flake
134. `jade-tam/dotfiles` ★194 MIT — Windows 11 ricing
135. `eythaann/Seelen-UI` ★17876 AGPL-3.0 — desktop env Windows
136. `Filippo39/.dotfiles` ★20 NO-LICENSE — dotfiles bare ⚠️
137. `HyDE-Project/HyprPanel` ★30 GPL-3.0 — wallbash template
138. `kotontrion/dotfiles` ★182 NO-LICENSE — dotfiles ⚠️
139. `K4ySuh/Kali-AutoBSPWM` ★39 NO-LICENSE — Kali BSPWM setup ⚠️
140. `RaulSanchezzt/auto-bspwm` ★17 NO-LICENSE — bspwm install ⚠️
141. `Muhammad-Yunus/Belajar-Computer-Vision` ★148 GPL-3.0 — CV learning
142. `Calvariaa/GWSL-Source` ★1 NOASSERTION — GWSL ⚠️
143. `TaKO8Ki/awesome-alternatives-in-rust` ★4120 MIT — Rust alternatives
144. `sickcodes/Docker-OSX` ★52948 GPL-3.0 — macOS VM in Docker
145. `microsoft/WSL` ★33770 MIT — Windows Subsystem Linux
146. `sirredbeard/awesome-wsl` ★6568 NOASSERTION — WSL list ⚠️
147. `AmineDjeghri/personal-os-setup` ★623 MIT — OS setup guide
148. `kasmtech/workspaces-images` ★1228 NOASSERTION — workspaces ⚠️
149. `AryanVBW/LinuxDroid` ★835 MIT — Android toolkit no root
150. `jz543fm/kali-dockerized` ★24 NO-LICENSE — Kali Docker ⚠️
151. `akuhnet/w-colab` ★351 NO-LICENSE — RDP Windows colab ⚠️
152. `gd-discov3r/win_11_vps` ★27 NO-LICENSE — Windows 11 VPS ⚠️
153. `kmille36/XiaomiMiMix2s-Windows-ARM` ★35 NO-LICENSE — Windows ARM ⚠️
154. `kmille36/scrcpy-audio-support` ★23 NO-LICENSE — scrcpy audio ⚠️
155. `kmille36/MacOS-Catalina-KVM-Preinstall` ★24 NO-LICENSE — macOS KVM ⚠️
156. `awesome-windows11/windows11` ★3570 GPL-3.0 — Windows 11 tweaks
157. `LGUG2Z/komorebi` ★15209 NOASSERTION — tiling WM Windows ⚠️
158. `CrazyIndianDeveloper/MobileInfo` ★5 GPL-3.0 — Android info
159. `JaKooLit/JaKooLit` ★65 NO-LICENSE — ? ⚠️
160. `sebanc/linuxloops` ★240 GPL-3.0 — Linux installer
161. `sebanc/brunch` ★4261 GPL-3.0 — ChromeOS boot x86

---

## 4. Analisis Kandidat Adopsi ke Ekosistem

### 4.1 Sudah diadopsi/dipakai (jangan duplikasi)
- `heygen-com/hyperframes` → skill `hyperframes` + `hyperframes-vertical-video` ✅
- `addyosmani/agent-skills` → skill `frontend-design`, `seo`, `accessibility` (via autoskills) ✅
- `opendataloader-project/opendataloader-pdf` → skill `document-content-pipeline` ✅
- `chrisjaron03/UACC` → skill `uacc` + MC mcp ✅
- `pbakaus/impeccable` → skill `impeccable` ✅
- `Panniantong/Agent-Reach` → skill `agent-reach` ✅
- `midudev/autoskills` → pola skill stack (7/11 diadopsi) ✅
- `Fikaramandio/korpus-bahasa-Gayo` → bahasa Gayo (didong-code) ✅ (belum dipakai, tapi sangat relevan — **satu-satunya star lokal/Aceh**)

### 4.2 Kandidat adopsi BARU (belum dipakai, disarankan)
**P0 — langsung berguna:**
0. **`browser-use/*` (MIT/AGPL, 4 repo)** — browser-native agent framework. **2 dari 4 repo di-star PALING BARU** (`workflow-use`, `browsercode`, `jev-ultrafast`, `video-use`). Relevan: automation web scraping, RPA, video editing via coding agent, dan **anti-detect browsing** (komplemen camofox). `jev-ultrafast` = web agent termurah/tercepat. `workflow-use` = RPA 2.0 workflows. **Gap:** kita sudah punya camofox (stealth browser) + agent-reach (internet read), TAPI belum ada orkestrasi browser agent untuk RPA/workflow otomatis.
1. **`NandhaKishorM/laya` (Apache-2.0)** + `mizorewww/laya-mlx` + `ipenywis/laya-ultrafast` — **System 1 decision engine, non-autoregressive, 7–14ms** (vs Jev 400ms+). **Kita SUDAH punya Jev via 9router** (`system-one-decisions` skill). Laya = generasi berikutnya: lebih cepat, lebih murah, MLX-native (cocok MBP 16GB). **Adopsi langsung**: tambah ke 9router + skill system-one-decisions sebagai backend decision. Ini evolusi natural dari Jev, bukan duplikasi.
2. **`affaan-m/ECC` (MIT)** — agent harness performance optimization. Bisa jadi **blueprint skill-bank governance** (skills+instincts+cost). Gap: skill bank kita 180+ tapi belum ada sistem "instincts"/cost-aware routing per skill.
3. **`thedotmack/claude-mem` (Apache-2.0)** — persistent context across sessions. Relevan masalah **memory Hermes penuh** (93% sekarang!). Pola capture/recall bisa ditiru untuk memory tiering Hermes.
4. **`tashfeenahmed/freellmapi` (MIT)** — 34 free LLM providers, 635 free models, 7.4B token/bulan. Relevan **9router** — bisa jadi katalog tambahan model free tier. ⚠️ verifikasi kualitas dulu.
5. **`diegosouzapw/OmniRoute` (MIT)** — free MIT AI gateway 359 providers. Relevan **9router replacement/alternatif** (9router sekarang single point of failure — lihat laporan audit).
6. **`0xNyk/council-of-high-intelligence` (MIT)** — structured multi-perspective deliberation. Relevan **system-one-decisions** skill + arsitektur supervisor MC (thread 1 = supervisor).

**P1 — bernilai untuk riset/eksperimen:**
7. **`stablyai/orca` (MIT)** — ADE untuk fleet of parallel agents. Relevan **orkestrasi MC** (bisa ganti/komplemen orchestrator Python kita).
8. **`deepseek-ai/deepseek-harness` (MIT)** — "everything is a plugin". Arsitektur plugin bisa ditiru untuk **MC plugin/hook** (niu-core-fence pola serupa).
9. **`prime-agent` (MIT)** — self-improving RLM coding agent. Relevan **Hermes self-healing** & model drift guard.
10. **`cactus-compute/needle` (Apache-2.0)** — automation foundation model tiny devices (2-bit, 8-29MB). Relevan **kopi-aceh-app-android** / IoT Aceh.
11. **`semantica-agi/semantica` (MIT)** — graph-native context infra. Relevan **Second Brain** (brain/index.json 191 file).

**P2 — video/content pipeline:**
12. **`harry0703/MoneyPrinterTurbo` (MIT)** — short video otomatis. Relevan **content-produce** (Reels/TikTok) — bisa jadi pipeline tambahan.
13. **`WyattBlue/auto-editor` (Unlicense)** — video editing otomatis. Relevan short-form-video-production.
14. **`calesthio/OpenMontage` (AGPL-3.0, ⚠️ non-komersial?)** — agentic video production. Pola boleh, kode hati-hati (AGPL).

**P3 — riset/edukasi:**
15. **`jingyaogong/minimind` (Apache-2.0)** — train 64M LLM dari nol. Referensi edukasi untuk tim Diskominfo.
16. **`FareedKhan-dev/kimi-k3-in-c` (Apache-2.0)** — Kimi K3 inference CPU single. Inspirasi efisiensi di hardware lemah (MBP 2020 i5).

### 4.3 Kategori yang TIDAK direkomendasikan (perhatikan risiko)
- **OS-experiment/dotfiles** (49 repo) — Hyprland/NixOS/WSL/Docker-OSX — tidak relevan dengan Mac-first ecosystem. Kecuali nanti migrasi ke Linux/Windows.
- **Security-sensitive** (⚠️): `techchipnet/CamPhish`, `Netw0rkNoob/VulnClaw`, `metasploit-ai`, `renzu-worm-v2`, `phoneintel` — hanya untuk riset keamanan resmi, JANGAN disalin ke produk.
- **NO-LICENSE** (27 repo) — ⚠️ jangan copy kode ke produk komersial tanpa izin eksplisit. Pola boleh diadopsi, kode jangan.
- **AGPL-3.0** (`worldmonitor`, `MiroFish`, `OpenMontage`, `serpantinum`, `G0DM0D3`) — copyleft kuat; hanya pola, atau jadi service terpisah.

### 4.4 Rekomendasi Aksi (langkah konkret)
1. **Shortlist top 10 P0** → study mendalam per repo (clone depth 1, baca kode inti) via skill `ecosystem-tool-adoption`.
2. **Uji `freellmapi` & `OmniRoute`** sebagai kandidat provider 9router (verifikasi HTTP-200 + kualitas sebelum mapping).
3. **Tiru pola `ECC` & `claude-mem`** untuk governance skill bank Hermes (cost-aware) + memory tiers.
4. **`council-of-high-intelligence`** → prototyping decision flow supervisor MC.
5. **Jangan sentuh kategori OS-experiment** dulu — dokumentasikan sebagai referensi riset saja.

---

## 5. Lampiran — Statistik

- **Total repo:** 161
- **Dengan lisensi terdeteksi:** 134 (83%)
- **Tanpa lisensi/eksplisit:** 27 (17%) ⚠️
- **Top bahasa:** Python 36, TypeScript 34, Shell 18, Rust 9, JavaScript 8, Nix 5
- **Total stars kumulatif:** 3.435.900 ★ (semua repo di-star, bukan punya sendiri)
- **Sumber data:** GitHub API `users/Niumination/starred?per_page=100&page=1&page=2` — live 24 Sep 2026

## Bukti
- `curl` GitHub API `users/Niumination/starred` → HTTP 200, 2 halaman (100 + 61 repo)
- Analisis via python3 (kategorisasi, lisensi) dari `/tmp/gh_starred.json` + `/tmp/gh_starred2.json`
- File ini = `docs/reports/REFERENSI-ADOPSI-STARRED-REPOS-2026-09-24.md` (dibuat 24 Sep 2026, 19:33 WIB)
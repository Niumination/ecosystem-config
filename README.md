# 🌳 Niumination Ecosystem Config

**Lightweight index & orchestration repo untuk Niumination ecosystem.**

Bukan kode — ini adalah **control center** yang nyimpen: project index, agent characters, documentation, scripts otomasi, dan security config.

## 📂 Struktur

| Path | Isi |
|------|-----|
| `AGENTS.md` | Root agent orchestration instructions |
| `BACKLOG.md` | **Master project portfolio** — semua proyek di ekosistem |
| `.gitleaks.toml` | GitLeaks security scanning config |
| `.vscode/` | VS Code workspace settings |
| `scripts/` | ⚙️ Auto-heartbeat, health check, changelog, eco-collect, cron |
| `docs/` | 📚 Dokumentasi teknis & integrasi |
| `dox/` | 📄 Project DOX files (notebooklm, reports, analysis) |
| `characters/` | 🤖 herdr agent characters (builder, pengawas, arsitek, dll) |
| `Niu-Flow/` | 📋 Log output Niu-Flow pipeline (remote-only) |

## 🚀 Quick Start

```bash
# Clone this repo
git clone https://github.com/Niumination/ecosystem-config.git

# Setiap sub-proyek punya repo sendiri — clone terpisah:
git clone git@github.com:Niumination/PemdiAcehTengah.git
git clone git@github.com:Niumination/niu-mission-control.git
# ... lihat BACKLOG.md untuk daftar lengkap
```

## 🧭 Navigasi

| Path | Isi |
|------|-----|
| **Production/** | 🏭 12 proyek — deployed (masing-masing repo sendiri) |
| **projects/** | 🔧 17 proyek — aktif dikerjakan |
| **incubator/** | 💤 9 proyek — dormant / eksperimen |
| **archive/** | 📦 File usang, backup (excluded from git) |
| **PI/** | 🔐 Sensitive configs (excluded from git) |
| **brain/** | 🧠 Obsidian vault (repo terpisah) |
| **tools/ponytail/** | 🐴 Ponytail MCP local (jangan push ke GH) |

> **Catatan:** Folder `Production/`, `projects/`, `incubator/`, `brain/`, `rekap/`, `tools/` tidak di-track di repo ini — masing-masing punya git remote sendiri. Repo ini **hanya index & orchestration**.

## 🔗 Related

- [Niumination on GitHub](https://github.com/Niumination) — Profile README di `Production/Niumination/`
- [ecosystem-config](https://github.com/Niumination/ecosystem-config) — Repo ini
- [kune-ya.com](https://kune-ya.com) — AI Chat RAG
- [PemdiAcehTengah](https://pemdi-acehtengah.vercel.app) — Portal Pemda
- [AI-Memory-Collection](docs/ai-memory-collection.md) — Knowledge base 12 AI tools

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
| `scripts/` | ⚙️ Auto-heartbeat, health check, changelog, eco-collect |
| `docs/` | 📚 Dokumentasi teknis & integrasi |
| `dox/` | 📄 Project DOX files |
| `characters/` | 🤖 herdr agent characters (builder, pengawas, arsitek, dll) |

## 🚀 Quick Start

```bash
# Clone this repo
git clone https://github.com/Niumination/ecosystem-config.git

# Each sub-project has its own git repo — clone separately:
git clone git@github.com:Niumination/PemdiAcehTengah.git
git clone git@github.com:Niumination/niu-mission-control.git
# ... lihat BACKLOG.md untuk daftar lengkap
```

## 🧭 Navigasi

- **Production/** — 11 proyek deployed (tidak di-track di repo ini)
- **projects/** — 16 proyek aktif dikerjakan (masing-masing repo sendiri)
- **incubator/** — 9 proyek dormant / eksperimen
- **archive/** — Backup & legacy files (excluded from git)
- **PI/** — 🔐 Sensitive configs (excluded from git)
- **brain/** — 🧠 Obsidian vault (repo terpisah)
- **tools/ponytail/** — 🐴 Ponytail MCP local (jangan push ke GH)

> **Catatan:** Folder `Production/`, `projects/`, `incubator/`, `brain/`, `rekap/`, `tools/` tidak di-track di repo ini — masing-masing punya git remote sendiri. Repo ini hanya config/index.

## 🔗 Related

- [Niumination on GitHub](https://github.com/Niumination)
- [kune-ya.com](https://kune-ya.com) — AI Chat RAG
- [PemdiAcehTengah](https://pemdi-acehtengah.vercel.app) — Portal Pemda
- [AI-Memory-Collection](docs/ai-memory-collection.md) — Knowledge base 12 AI tools

# My Websites — Android Chrome Installable

Sumber: GitHub repos + local projects. Diurutkan berdasarkan readiness untuk PWA install di Android via Chrome.

## Already Live (PWA-ready)

| # | Website | URL | Repo | Tech | Install via Chrome |
|---|---|---|---|---|---|
| 1 | PemdiAcehTengah | https://pemdi-aceh-tengah.vercel.app | PemdiAcehTengah | Next.js 16 + Prisma | ✅ Add to Home Screen |
| 2 | CC Aceh Tengah | https://cc-acehtengah.vercel.app | cc-acehtengah | Next.js + Prisma | ✅ Add to Home Screen |
| 3 | Niu Dash | https://niumination.github.io/niu-dash/ | niu-dash | Static HTML/JS | ✅ Add to Home Screen |
| 4 | Kune-Ya | https://kune-ya-com.vercel.app | kune-ya.com | Next.js | ✅ Add to Home Screen |
| 5 | Niu Startpage | https://niumination.github.io/Niu-Startpage/ | Niu-Startpage | Static | ✅ Add to Home Screen |
| 6 | Niu Cyber Search | https://niu-cyber.vercel.app | Niu-Cyber-Search-Engine | Vercel app | ✅ Add to Home Screen |
| 7 | Zaryu Startpage | https://niumination.github.io/zaryu.startpage/ | zaryu.startpage | Catppuccin static | ✅ Add to Home Screen |
| 8 | Niu HomePage | https://niumination.github.io/NiuHomePage/ | NiuHomePage | Static | ✅ Add to Home Screen |
| 9 | Virtual Assistance | https://virtual-assistance-pi.vercel.app | VirtualAssistance | Vercel app | ✅ Add to Home Screen |
| 10 | Niu Private | https://niumination.github.io/niu-private/ | niu-private | GitHub Pages | ✅ Add to Home Screen |
| 11 | CC Switch | https://ccswitch.io | cc-switch | Web/Desktop | ✅ Add to Home Screen |
| 12 | Zaryu Dev | https://zaryudev.vercel.app | zaryu.dev | Vercel | ✅ Add to Home Screen |
| 13 | Niu Vermilion | https://niu-vermilion.vercel.app | Niu-Vermilion | Vercel | ✅ Add to Home Screen |

## Needs Deployment First

| # | Website | Repo | Tech | Notes |
|---|---|---|---|---|
| 14 | Niu Dash Fullstack | niu-dash-fullstack | Next.js 16 + Prisma | ✅ Deploy |
| 15 | Arch Web Dashboard | arch-web-dashboard | Dashboard | 🗑️ Dihapus dari Vercel |
| 16 | Mac Web Dashboard | mac-web-dashboard | Dashboard | 🗑️ Dihapus dari Vercel |
| 17 | Niu Kanban Dash | niu-kanban-dash | Dashboard | 🗑️ Dihapus dari Vercel |
| 18 | PAGASUS-PRO | PAGASUS-PRO | Unknown | Inspect & deploy |
| 19 | Maze 3D Game | Maze-3D-Game---Web-Based | WebGL/Three.js | Build & deploy |
| 20 | Devs Niu | Devs-Niu | Unknown | Inspect & deploy |
| 21 | Niu LKH | niu-lkh | App | 🗑️ Dihapus dari Vercel |
| 22 | AuditTI-AT | audit-ti-at | App | 🗑️ Dihapus dari Vercel |
| 23 | TEDEO-Kanban | tedeo-kanban | App | 🗑️ Dihapus dari Vercel |

## How to Install on Android

1. Buka URL di Chrome Android
2. Tap menu (3 titik) → "Add to Home screen" / "Install app"
3. Chrome akan membuat shortcut seperti native app
4. Untuk full PWA experience, pastikan website punya `manifest.json` + service worker

## Notes
- List ini mengecualikan: PemdiAcehTengah, cc-acehtengah, niu-dash, ai-file-manager sesuai permintaan
- ai-file-manager Android app native tidak bisa diinstall via Chrome sebagai web app
- Untuk repo private, perlu deploy ke Vercel/Netlify/GitHub Pages terlebih dahulu

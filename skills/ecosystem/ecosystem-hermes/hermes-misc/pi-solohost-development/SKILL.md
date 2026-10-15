---
name: pi-solohost-development
description: "Build and submit apps to Pi Network SoloHost."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pi-network, solohost, docker, self-hosted]
---

# Pi Network SoloHost Development

Build and publish self-hosted apps to **420,000+ Pi Node runners**.

## When to Use
- User wants to participate in SoloHost program
- Building local-first AI apps for Pi ecosystem
- Containerizing existing apps for Pi Desktop

## Quick Start

### Prerequisites
```bash
brew install docker docker-compose
# Verify Pi Desktop (Node 0.6.2+)
pi-desktop --version
```

### Create Template
```bash
bash ~/.hermes/create-solohost-app.sh "app-name"
# Creates: ~/SoloHostApps/<name>/
```

### Package Structure
```
my-app/
├── Dockerfile
├── manifest.json
├── README.md
├── src/
├── assets/  # icon.png (512x512), screenshot.png
└── docs/
```

### Build & Test
```bash
docker build -t my-app:latest .
docker run -p 8080:8080 -v $(pwd)/data:/app/data my-app:latest
curl http://localhost:8080/health
```

### Install to Pi Desktop
1. Open Pi Desktop → SoloHost tab
2. Click "Install from Local"
3. Select app directory
4. Test in Pi Browser

## manifest.json
```json
{
  "version": "1.0.0",
  "name": "App Name",
  "description": "Description",
  "author": "your-pi-account",
  "containers": [{
    "name": "main",
    "image": "your-app:latest",
    "ports": [{"container": 8080, "host": 8080}],
    "volumes": [{"name": "data", "path": "/app/data"}]
  }],
  "permissions": {
    "filesystem": ["read", "write"],
    "network": ["outbound"]
  }
}
```

## Submission States
| State | Visibility |
|-------|------------|
| Draft | Private |
| Unlisted | Link only |
| Listed | Public (420K users) |

## Best Practices
- Containerized, default-restricted
- Explicit user permissions
- Data stored locally
- Health check required
- Image < 500MB

## App Ideas
1. **cc-acehtengah Local** — DTSEN offline (2-3 weeks)
2. **UMKM AI Agent** — Local assistant for traders (4-6 weeks)
3. **Document Processor** — OCR + extraction (3-4 weeks)
4. **MCP Server** — Connect AI to local DBs (4-5 weeks)

## Resources
- Guide: `references/solohost-best-practices.md`
- Ideas: `references/app-ideas.md`
- Validator: `scripts/validate-solohost-app.py`
- Template: `~/.hermes/create-solohost-app.sh`

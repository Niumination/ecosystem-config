# SoloHost Quick Reference Card

## 🚀 Getting Started

### 1. Check Pi Desktop
```bash
# Verify Pi Desktop installed
pi-desktop --version

# Check Node version (need 0.6.2+)
pi-node --version
```

### 2. Create Your App
```bash
# Use template generator
bash ~/.hermes/create-solohost-app.sh "your-app-name"

# Or manually create structure
mkdir my-app && cd my-app
# Create: Dockerfile, manifest.json, README.md
```

### 3. Build & Test
```bash
# Build Docker image
docker build -t my-app:latest .

# Run locally
docker run -p 8080:8080 -v $(pwd)/data:/app/data my-app:latest

# Test endpoints
curl http://localhost:8080/
curl http://localhost:8080/health
```

### 4. Install to Pi Desktop
1. Open Pi Desktop
2. Go to **SoloHost** tab
3. Click **"Install from Local"**
4. Select your app directory
5. Wait for installation
6. Test in Pi Browser

---

## 📦 Package Structure

```
my-app/
├── Dockerfile          # Required: container definition
├── manifest.json       # Required: app metadata
├── README.md           # Required: documentation
├── src/                # Your source code
├── assets/             # Icons & screenshots
│   ├── icon.png        # 512x512 minimum
│   └── screenshot.png  # 1920x1080 recommended
└── docs/               # Additional docs
```

---

## 🔑 Key Requirements

| Item | Requirement |
|------|-------------|
| **Min Node Version** | 0.6.2+ |
| **Container** | Docker-based |
| **Port** | 8080 (default) |
| **Data Storage** | Local volumes |
| **Permissions** | Explicit user grant |
| **Security** | Containerized isolation |

---

## 📝 manifest.json Essentials

```json
{
  "version": "1.0.0",
  "name": "App Name",
  "description": "What it does",
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

---

## 🎯 App Ideas for You

Based on your experience:

1. **cc-acehtengah Local** — DTSEN offline version
2. **AI Agent UMKM** — Local assistant for traders
3. **Document Processor** — OCR + extraction
4. **MCP Server** — Connect AI to local DBs

---

## 📚 Resources

| Resource | Link |
|----------|------|
| SoloHost Blog | minepi.com/blog/pi2day2026/ |
| Node 0.6.2 | minepi.com/blog/pi-node-0-6-2/ |
| App Pricing | minepi.com/blog/app-studio-pricing/ |
| Developer Forum | forum.minepi.com |
| Template | ~/.hermes/create-solohost-app.sh |

---

## ✅ Checklist Before Submit

- [ ] Dockerfile working
- [ ] manifest.json valid
- [ ] App runs on port 8080
- [ ] Data stored locally (volumes)
- [ ] Permissions minimal & necessary
- [ ] README clear
- [ ] Tested in Pi Desktop
- [ ] Screenshots ready

---

**Template location:** `~/SoloHostApps/cc-acehtengah-local/`

# PiAssistant Analysis — SoloHost Porting Strategy
**Repository:** https://github.com/Niumination/VirtualAssistance  
**Live:** https://virtual-assistance-pi.vercel.app/  
**Version:** v0.1.2 (Jun 3, 2026)

---

## 📊 Current App Architecture

### Tech Stack
| Component | Technology |
|-----------|------------|
| **Framework** | Next.js 16 (App Router) + TypeScript |
| **State Management** | Zustand |
| **Styling** | Tailwind CSS v4 |
| **Pi Integration** | Pi Platform SDK v2 |
| **AI Backend** | OpenAI API (with rule-based fallback) |
| **Deployment** | Vercel (cloud) |

### Core Features
| Feature | Status | Description |
|---------|--------|-------------|
| 🔐 Pi Login | ✅ Complete | Auth + verification via Pi SDK |
| 💬 AI Chat | ✅ Complete | OpenAI + rule-based fallback |
| 💰 Wallet Dashboard | ✅ Complete | Balance, transaction history |
| 💸 Payment System | ✅ Complete | U2A & A2U payments |
| 📋 Task Manager | 🔄 In Progress | Simple todo-list |
| 📢 Pi News | 🔄 In Progress | Ecosystem updates |

### Recent Fix (v0.1.2)
**Problem:** Pi SDK 'not initialized' error  
**Root Cause:** Pi.init() called only on login button click  
**Fix:** 
- Call Pi.init() immediately after SDK script load (inline script in layout.tsx)
- waitForPiSDK(): polling 200ms until ready (timeout 10s)
- authenticate() auto-init if not initialized
- createPaymentAsync() async version

---

## 🎯 SoloHost Porting Strategy

### What Needs to Change

| Aspect | Current (Vercel) | Target (SoloHost) |
|--------|------------------|-------------------|
| **Hosting** | Cloud (Vercel) | Local (Docker container) |
| **Data Storage** | Cloud DB | Local volumes |
| **API Keys** | Server-side (secure) | Local env (user-controlled) |
| **Pi SDK** | Web SDK in browser | Web SDK in browser (same) |
| **AI Backend** | OpenAI API | Local model OR cloud API |
| **User Access** | Web browser | Pi Desktop + Pi Browser |

### Key Changes Required

#### 1. Docker Containerization
```dockerfile
# Multi-stage build
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["node", "server.js"]  # Next.js standalone server
```

#### 2. Local Data Storage
Replace cloud DB with local SQLite/IndexedDB:
```typescript
// Current: Cloud database
// New: Local storage
const store = create((set) => ({
  transactions: [],
  addTransaction: (tx) => set((state) => ({
    transactions: [...state.transactions, tx]
  })),
  // Save to localStorage or IndexedDB
}));
```

#### 3. AI Backend Options
| Option | Pros | Cons |
|--------|------|------|
| **Local Ollama** | Privacy, no API cost | Needs GPU, slower |
| **Cloud API (OpenAI)** | Fast, smart | Data leaves device |
| **Hybrid** | Best of both | Complex setup |

#### 4. Environment Configuration
```bash
# .env.local (user-managed)
PI_API_KEY=your_pi_app_id
OPENAI_API_KEY=your_openai_key  # Or use local model
DATABASE_URL=file:///app/data/piassistant.db
```

---

## 📦 SoloHost Package Structure

```
piassistant-solohost/
├── Dockerfile              # Container definition
├── docker-compose.yml      # Optional: multi-service
├── manifest.json           # App metadata
├── README.md               # Documentation
├── .env.example            # Environment template
├── src/                    # Existing source code (mostly unchanged)
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── styles/
├── data/                   # Local data directory (volume)
├── assets/                 # Icons & screenshots
│   ├── icon.png           # 512x512
│   └── screenshot.png     # 1920x1080
└── docs/                   # Updated documentation
```

### manifest.json
```json
{
  "version": "1.0.0",
  "name": "PiAssistant SoloHost",
  "description": "Web3 Virtual Assistant for Pi Network — local-first",
  "author": "afrizal.munthe",
  "license": "MIT",
  "tags": ["pi", "wallet", "ai", "web3", "assistant"],
  "min_node_version": "0.6.2",
  "containers": [
    {
      "name": "piassistant",
      "image": "piassistant-solohost:latest",
      "ports": [{"container": 3000, "host": 3000}],
      "volumes": [
        {"name": "data", "path": "/app/data"}
      ],
      "environment": {
        "NEXT_PUBLIC_PI_APP_ID": "${PI_APP_ID}",
        "DATABASE_URL": "file:///app/data/piassistant.db"
      }
    }
  ],
  "permissions": {
    "filesystem": ["read", "write"],
    "network": ["outbound"],
    "process": ["execute"]
  }
}
```

---

## 🚀 Migration Steps

### Phase 1: Containerize (Week 1)
1. ✅ Create Dockerfile (Next.js standalone)
2. ✅ Test local build & run
3. ✅ Add volume mounts for data
4. ✅ Configure environment variables

### Phase 2: Local Data (Week 1-2)
1. Replace cloud DB with SQLite/IndexedDB
2. Implement localStorage for user preferences
3. Add data export/import functionality
4. Test data persistence across restarts

### Phase 3: AI Backend (Week 2)
1. **Option A:** Keep OpenAI (user provides key)
2. **Option B:** Add Ollama support (local models)
3. Implement hybrid fallback logic
4. Test AI responses locally

### Phase 4: Pi SDK Integration (Week 2-3)
1. Verify Pi SDK works in container
2. Test wallet connections
3. Test payment flows
4. Ensure sandbox mode for dev

### Phase 5: Testing & Polish (Week 3-4)
1. Install in Pi Desktop
2. Test full user flow
3. Fix any container issues
4. Prepare screenshots & docs

### Phase 6: Submit (Week 4)
1. Choose visibility: Draft → Unlisted → Listed
2. Submit to SoloHost directory
3. Gather feedback from Pioneers
4. Iterate based on usage

---

## 💡 Value Proposition

### Why SoloHost Version?
1. **Privacy First** — All data stays on user's device
2. **No Cloud Dependency** — Works offline (except AI if using cloud)
3. **Pi Ecosystem Integration** — Native Pi SDK, wallet, payments
4. **Community Benefit** — Contribute to 420K+ Node operators
5. **Learning Experience** — Expand from web to containerized apps

### Differentiators vs OpenClaw
| Aspect | OpenClaw | PiAssistant SoloHost |
|--------|----------|---------------------|
| Focus | General AI assistant | Pi-specific (wallet, payments) |
| Pi Integration | Basic | Deep (SDK, wallet, payments) |
| Data | Local | Local + Pi blockchain |
| Use Case | General tasks | Pi ecosystem management |

---

## 📝 Next Actions

**Immediate (This Week):**
1. [ ] Review existing codebase structure
2. [ ] Create Dockerfile for Next.js standalone
3. [ ] Test local build

**Short-term (2 Weeks):**
1. [ ] Implement local data storage
2. [ ] Add environment configuration
3. [ ] Test Pi SDK in container

**Medium-term (1 Month):**
1. [ ] Full SoloHost package
2. [ ] Submit as "unlisted" for testing
3. [ ] Gather feedback

---

**Ready to start?** Saya bisa bantu:
- A. Buat Dockerfile dari codebase existing
- B. Riset lebih dalam tentang Pi SDK container compatibility
- C. Setup local development environment
- D. Semua di atas

(◕‿◕)★

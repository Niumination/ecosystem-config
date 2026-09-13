# SoloHost Best Practices — Deep Dive

## Architecture Overview

### How SoloHost Works
```
User Computer
├── Pi Desktop (host application)
│   └── SoloHost runtime
│       └── Docker container
│           ├── App process (port 8080)
│           ├── Local storage (volumes)
│           └── Explicit permissions
└── Pi Browser (mobile access)
    └── WebSocket connection to local app
```

### Key Design Principles
1. **Local-first** — All data stays on user's device
2. **Containerized** — Isolated environment, default-restricted
3. **Permission-based** — User grants explicit access per task
4. **Self-sovereign** — No cloud dependency for core functionality

---

## Docker Best Practices for SoloHost

### Multi-Stage Build Example
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-slim AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:20-slim AS runtime
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# Non-root user for security
RUN useradd -m appuser
USER appuser

EXPOSE 8080
ENV PORT=8080
ENV NODE_ENV=production

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "fetch('http://localhost:8080/health').then(r => r.ok ? process.exit(0) : process.exit(1)).catch(() => process.exit(1))"

CMD ["node", "dist/main.js"]
```

### Image Size Optimization
- Target: < 500MB (affects download speed on slow connections)
- Use slim/alpine base images
- Remove unnecessary dependencies
- Use .dockerignore

### Cross-Platform Support
```dockerfile
# Build for both architectures
FROM --platform=$BUILDPLATFORM node:20-slim AS builder
# ... build steps ...

FROM --platform=$TARGETPLATFORM node:20-slim AS runtime
# ... runtime setup ...
```

---

## Security Considerations

### Permission Model
SoloHost uses explicit permission grants:
- **filesystem**: read, write, execute
- **network**: inbound, outbound
- **process**: spawn, signal

**Best Practice:** Request minimal permissions
```json
"permissions": {
  "filesystem": ["read"],  // Only read if possible
  "network": ["outbound"], // Outbound only
  "process": []            // No process access if not needed
}
```

### Data Isolation
- Use named volumes, not bind mounts
- Store app data in `/app/data`
- Never access `/home` or `/Users` directly
- Encrypt sensitive data at rest

### Network Security
- Bind to `127.0.0.1` only (not `0.0.0.0`)
- Use TLS for any external connections
- Validate all input from Pi Browser
- Rate limit API endpoints

---

## User Experience Guidelines

### Onboarding Flow
1. User discovers app in SoloHost directory
2. Clicks "Install" → Docker image downloads
3. First launch shows permission dialog
4. User grants permissions explicitly
5. App runs, accessible via Pi Browser

### Error Handling
Always provide clear error messages:
```javascript
// Good
if (!fs.existsSync(DATA_DIR)) {
  console.error('Data directory not found. Please grant filesystem access.');
  process.exit(1);
}

// Bad
if (!data) throw new Error('Failed');
```

### Health Checks
Pi Desktop monitors health endpoint:
```javascript
app.get('/health', (req, res) => {
  res.json({
    healthy: true,
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: '1.0.0'
  });
});
```

---

## Testing Strategy

### Local Testing
```bash
# 1. Build
docker build -t my-app:latest .

# 2. Run with volumes
docker run -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  -e API_KEY=xxx \
  my-app:latest

# 3. Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/api/test

# 4. Test in Pi Desktop
# - Open Pi Desktop
# - SoloHost tab → Install from Local
# - Select directory
```

### Performance Testing
- Load testing: 100 concurrent requests
- Memory profiling: check for leaks
- Startup time: < 5 seconds ideal
- Response time: < 500ms for simple ops

### Cross-Platform Testing
- macOS (Apple Silicon + Intel)
- Windows (if targeting)
- Linux (if targeting)

---

## Submission Process

### Pre-Submission Checklist
- [ ] All tests passing
- [ ] README complete
- [ ] Screenshots ready (1920x1080)
- [ ] Icon ready (512x512)
- [ ] manifest.json valid
- [ ] Docker image < 500MB
- [ ] Health check working
- [ ] Error handling tested

### Submission States

#### Draft
- For active development
- Not visible to others
- Can install locally for testing

#### Unlisted
- Private sharing via link
- Good for beta testing
- Not in public directory

#### Listed
- Public in SoloHost directory
- Visible to 420K+ users
- Requires structural validation pass

### After Submission
1. Structural checks run automatically
2. If pass → available for install
3. If fail → fix errors and resubmit
4. No human review (permissionless)

---

## Monetization & Pricing

### Pi App Studio Costs (as of Aug 2026)
- **Standard rate**: Actual AI service cost (varies)
- **Subsidized rate**: 0.25 Pi/create, 0.25 Pi/edit
- **Eligibility**: Apps with real users (not just creator)

### Subsidy Criteria
- Distinct users > 10
- Regular usage patterns
- Real utility demonstrated
- Not spam/test apps

### Pricing Strategy
- Start with draft/unlisted (free)
- Upgrade to listed when ready
- Improve app to qualify for subsidy
- Focus on user value, not features

---

## Common Use Cases

### Case 1: Local AI Agent
```
App: Personal AI assistant
Stack: Python + Ollama + FastAPI
Features:
- Local LLM inference
- Persistent memory
- Tool calling
- Multi-model support
```

### Case 2: Document Processor
```
App: OCR + Extraction
Stack: Python + Tesseract + PDFLib
Features:
- Local document processing
- No cloud upload
- Batch processing
- Export to multiple formats
```

### Case 3: MCP Server
```
App: Internal tool integration
Stack: Node.js + MCP SDK
Features:
- Connect AI to local DB
- Jira/GitHub/Slack integration
- Secure credential storage
- Rate limiting
```

---

## Troubleshooting

### Issue: App won't start
**Symptoms:** Health check fails, container exits
**Fix:**
1. Check logs: `docker logs <container>`
2. Verify port not in use
3. Check volume permissions
4. Ensure .env file present

### Issue: Slow downloads
**Symptoms:** Users complain about long install times
**Fix:**
1. Reduce image size (< 500MB)
2. Use compression
3. Consider layer caching
4. Provide alternative install methods

### Issue: Permission denied
**Symptoms:** App can't access files
**Fix:**
1. Check manifest.json permissions
2. Verify volume mounts
3. Ensure user grants permissions
4. Check container user (non-root)

---

## Performance Benchmarks

### Target Metrics
| Metric | Target | Notes |
|--------|--------|-------|
| Image size | < 500MB | Affects download time |
| Startup time | < 5s | First launch experience |
| Health check | < 100ms | Pi Desktop monitoring |
| Response time | < 500ms | Simple operations |
| Memory usage | < 512MB | Typical Pioneer hardware |

### Optimization Techniques
- Lazy loading
- Connection pooling
- Response compression
- Caching strategies
- Async processing

---

**Last Updated:** August 30, 2026  
**Source:** Pi Network SoloHost documentation + community patterns

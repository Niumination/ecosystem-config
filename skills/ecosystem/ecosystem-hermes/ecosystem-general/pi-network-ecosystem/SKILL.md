---
name: pi-network-ecosystem
description: "Pi Network — App Studio, Payments, Browser integration."
version: "1.0.0"
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [pi-network, app-studio, pi-payments, pi-browser]
    related_skills: [pi-solohost-development]
---

# Pi Network Ecosystem Integration

Build, monetize, and distribute apps within Pi Network — reaching 60M+ KYC-verified Pioneers.

## When to Use
- User wants to build apps via Pi App Studio (Use App Studio AI beta)
- User wants to import existing apps via Pi App Studio (Use External AI free)
- User wants to add Pi Payments to web apps or Pi Apps
- User wants to publish/distribute apps to Pi Browser users
- User asks about Pi SDK integration

## Pi App Studio — Three Paths

### Path 1: App Studio AI (Beta)
AI generates app from natural language prompt. Best for quick MVPs.
```
1. Open Pi Browser → App Studio
2. Select "Use App Studio AI (Beta)"
3. Paste prompt describing app
4. Review generated app
5. Customize colors, logo, data
6. Submit for Mainnet review
```

**Prompt structure:**
- App name + tagline
- Category (Government, Finance, Social, etc.)
- Language (Bahasa Indonesia for local apps)
- Page-by-page structure with wireframe ASCII
- Data schema (static JSON for MVP)
- Pi Payments integration points
- Color scheme + branding

### App Studio Authentication (REQUIRED)
Every app submitted via Pi App Studio MUST implement this auth flow:

1. **Pi SDK Auth**: `Pi.init({ version: "2.0" })` → `Pi.authenticate(["username", "payments"], onIncompletePaymentFound)`
2. **App Studio Exchange**: POST accessToken to `https://backend.appstudio-u7cm9zhmha0ruwv8.piappengine.com/pi/auth/v1/login` → get `sessionToken` + `user`
3. **Use App Studio identity**: Trust `session.user` from App Studio — NOT `auth.user` from Pi.authenticate (browser-controlled, untrusted)
4. **Load content ONLY after successful auth exchange**

Without this flow, App Studio cannot verify the app and Mainnet submission fails.

### External AI (Free) Flow
For apps built outside Pi Studio:
1. Build app (static HTML/JS or framework)
2. Deploy to **live URL** (GitHub Pages, Vercel) — localhost does NOT work
3. Pi Browser → App Studio → "Use External AI (Free)"
4. Paste URL + fill form (name, description, language, category, logo 1024x1024 <1.1MB)
5. Pi wraps app with SDK + payments

### Path 3: Access My Apps
Dashboard to manage published apps — upload previews, share links, delete.

## Pi Payments Integration

### Tier Structure (recommended)
| Tier | Price | Features |
|------|-------|----------|
| Free | 0 Pi | Basic view, limited history |
| Basic | 5 Pi/month | Full dashboard, export CSV |
| Pro | 15 Pi/month | Unlimited + API + alerts |
| Enterprise | 50 Pi/month | White-label + priority support |

### Implementation Options

**Option A: Pi App Studio (simplest)**
- Built-in payment button in App Studio settings
- No backend needed — Pi handles verification
- Best for: quick launch, simple apps

**Option B: Pi SDK in Next.js (more control)**
```bash
npm install @pi-network/sdk
```
- Server-side payment verification
- Custom UI/UX
- Best for: existing ecosystem apps

### Payment Flow
1. User clicks upgrade → Pi Payment Dialog opens
2. User confirms in Pi Wallet
3. Transaction broadcast to Pi blockchain
4. Backend webhook receives payment confirmation
5. Server verifies transaction on-chain
6. User tier upgraded, features unlocked

### Revenue Projection
Conservative: 50 Pi (month 1) → 3600 Pi (month 12)
Optimistic: 150 Pi (month 1) → 24000 Pi (month 12)

## Data Strategy for Pi Apps

### Static MVP (recommended first step)
- Embed demo data as JSON in app
- Connect to live API later
- Faster Mainnet approval

### Dynamic API (phase 2)
- Deploy backend on VPS (103.30.146.232)
- Pi App calls API via HTTPS
- Configure CORS for Pi Browser origin

## Mainnet Submission Requirements
- KYC-verified developer account
- App demonstrates real utility
- Stable operation (no crashes)
- Legitimate Pi-denominated use case
- No gambling/misinformation
- Compliance with Pi developer guidelines

## Architecture: Pi App ↔ MATA Backend
```
Pi Browser App (static HTML/JS)
  │
  ├── Pi Payments SDK (built-in)
  │
  └── HTTPS API calls → VPS (103.30.146.232)
        └── MATA Backend (Python/Flask)
              └── SQLite database
```

## Pitfalls
- **WAF blocking:** Some APIs (data.inaproc.id) block datacenter IPs. Use Pi App as frontend, call API from VPS, proxy through Pi App if needed.
- **Catalog flip-flop:** Pi App Studio AI generates apps deterministically, but data may change. Pin API versions.
- **Mainnet delay:** Review takes 1-2 weeks. Test thoroughly on Testnet first.
- **Payment fraud:** Always verify payments server-side, never trust client-side alone.
- **`.env` leak via `git add -f` in nested repos.** When the parent repo ignores `apps/`, child repos must use `git add -f`. Force-add catches `.env` too — stage files explicitly, verify with `git diff --cached --name-only` before committing. If `.env` is committed, remove with `git rm --cached` immediately and rotate the exposed key.

## References
- Pi App Studio overview: https://minepi.com/blog/vibe-code-app-studio/
- Pi Payments docs: https://minepi.com/blog/app-studio-event-payments-ads/

## Related Skills
- pi-solohost-development: Docker-based self-hosted apps

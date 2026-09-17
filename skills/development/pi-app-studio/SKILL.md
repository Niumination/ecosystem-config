---
name: pi-app-studio
description: "Use when building Pi apps via App Studio. Auth and payments."
version: "1.0.0"
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [pi-network, app-studio, pi-sdk, payments, authentication, blockchain]
    homepage: https://docs.minepi.com/
---

# Pi App Studio — App Development & Deployment

Build and deploy apps on Pi Network via Pi App Studio. This skill covers the full lifecycle from registration to Mainnet submission.

## Workflow Overview

```
Register App → Generate (AI or External AI) → Add Pi Auth → Add Pi Payments → Test on Testnet → Submit Mainnet
```

## Step 1: Register App in Pi Developer Portal

1. Open **Pi Browser** (required — regular browsers cannot access)
2. Navigate to `pi://develop.pinet.com` or tap **Develop** icon
3. Tap **New App**
4. Fill: App Name, Description, App Network (**Testnet** for development)
5. Tap **Create**
6. Set Development URL (e.g., `http://localhost:8080` for local testing)
7. Tap **API Key** → Generate Server API Key → **Save to vault** (NEVER to repo)
8. Tap **Create Wallet** → Generate app wallet → **Save private key to vault** (NEVER to repo)

**Output**: App URL (`<appname>.pinet.com`), Server API Key, Wallet Address, Wallet Private Key

## Step 2: Generate App

### Option A: Use App Studio AI (Beta)
- Cost: ~30 Pi (paid to Pi Network)
- Paste PRD prompt → AI generates app
- Iterate if needed

### Option B: Use External AI (Free)
- Build app with Claude Code / Cursor / Lovable / Replit
- Deploy to live URL (GitHub Pages, Vercel, etc.)
- Paste URL to Pi App Studio form
- Pi App Studio converts to Pi App + adds Pi SDK

**Decision criteria**: Use External AI if you already have a codebase or want full control. Use App Studio AI for quick prototyping.

## Step 3: Add Pi Authentication (REQUIRED)

Every app MUST implement Pi Authentication. Without it, App Studio cannot verify the app.

### Frontend (index.html)
```html
<head>
  <script src="https://sdk.minepi.com/pi-sdk.js"></script>
</head>
```

### Frontend Auth Flow (app.js)
```javascript
async function initPiAuth() {
  await Pi.init({ version: "2.0" });  // No sandbox flag — auto-detected
  
  const auth = await Pi.authenticate(
    ["username", "payments"],
    onIncompletePaymentFound  // REQUIRED callback
  );
  
  // Exchange accessToken with App Studio (REQUIRED)
  const res = await fetch(
    "https://backend.appstudio-u7cm9zhmha0ruwv8.piappengine.com/pi/auth/v1/login",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ accessToken: auth.accessToken })
    }
  );
  
  const session = await res.json();
  // session.sessionToken — store in memory
  // session.user.username — display (from App Studio, NOT from Pi.authenticate)
  
  return session;
}
```

**CRITICAL**: Never trust `uid` or `username` from `Pi.authenticate()` for authorization decisions. Only use values returned by App Studio backend.

## Step 4: Add Pi Payments (Optional but Common)

### Frontend Payment Flow
```javascript
async function purchaseProduct(product) {
  await Pi.init({ version: "2.0" });
  
  await Pi.createPayment(
    {
      amount: product.amount,
      memo: product.memo,
      metadata: { productId: product.id }
    },
    {
      onReadyForServerApproval: async (paymentId) => {
        await fetch("/api/payments/approve", {
          method: "POST",
          body: JSON.stringify({ paymentId })
        });
      },
      onReadyForServerCompletion: async (paymentId, txid) => {
        await fetch("/api/payments/complete", {
          method: "POST",
          body: JSON.stringify({ paymentId, txid })
        });
        // Deliver product ONLY after backend confirms
      },
      onCancel: (paymentId) => { /* handle cancel */ },
      onError: (error) => { /* handle error */ }
    }
  );
}
```

### Backend Payment Server (Required for Production)

Backend MUST forward to Pi Platform API:

```javascript
// POST /api/payments/approve
fetch(`https://api.minepi.com/v2/payments/${paymentId}/approve`, {
  method: "POST",
  headers: { Authorization: `Key ${process.env.PI_API_KEY}` }
});

// POST /api/payments/complete
fetch(`https://api.minepi.com/v2/payments/${paymentId}/complete`, {
  method: "POST",
  headers: {
    Authorization: `Key ${process.env.PI_API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ txid })
});
```

**CRITICAL**: `PI_API_KEY` is a server-side env var. Never expose in client-side code.

## Step 5: Test on Testnet

- App URL: `<appname>.pinet.com`
- Open in **Pi Browser** only (regular browsers show "unverified")
- Testnet apps have black/yellow stripe indicator — this is normal
- Test all flows: auth, payments, product delivery
- Check Revenue Dashboard in Pi Developer Portal

## Step 6: Submit to Mainnet

1. Test on Testnet for at least 2 weeks with no critical bugs
2. Deploy production backend (if using payments)
3. Submit for Mainnet review via Pi Developer Portal
4. Wait 1-2 weeks for approval
5. Once approved, app goes live to 60M+ Pioneers

## Revenue Share

| Network | Developer | Pi Network |
|---------|-----------|------------|
| Testnet | 100% | 0% |
| Mainnet | 70% | 30% |

## Security Rules

1. **Private keys** → vault only (`~/Desktop/Niumination/vault/`), chmod 600
2. **API keys** → vault only, never in repo
3. **Server API Key** → backend env var only, never in client-side code
4. **Wallet private key** → never share in chat, never commit to git
5. **App Studio auth** — always exchange token with backend, never trust client-side uid/username

## Common Pitfalls

- **"Unverified" in regular browser** → Normal. Test only in Pi Browser.
- **Auth fails silently** → Ensure `Pi.init()` completes before `Pi.authenticate()`
- **Payment stuck** → Always implement `onIncompletePaymentFound` callback
- **Secrets in git** → Use `git rm --cached` immediately if committed. Rotate keys if exposed.

## References

- `references/authentication-flow.md` — Detailed Pi Auth sequence diagram
- `references/payment-server.md` — Production backend setup guide
- `references/testnet-checklist.md` — Pre-submission testing checklist

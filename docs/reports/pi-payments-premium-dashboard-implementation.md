# Premium Dashboard — Pi Payments Implementation Plan

> **Priority:** P1
> **Platform:** Pi Network (Testnet → Mainnet)
> **Tanggal:** 2026-09-16
> **Status:** Ready for implementation

---

## Ringkasan

Implementasi Pi Payments untuk akses premium dashboard MATA dan layanan data pengadaan lainnya. Target: 1000+ users, 200+ Pi revenue per bulan.

---

## Tier Structure

### Free Tier (0 Pi)
| Feature | Access |
|---------|--------|
| Dashboard ringkasan | ✅ Full |
| 7 days data history | ✅ |
| Basic statistics | ✅ |
| Indikasi terkini | ✅ Top 3 |
| Export | ❌ |
| API access | ❌ |
| Alert | ❌ |

### Basic Tier (5 Pi/bulan)
| Feature | Access |
|---------|--------|
| Semua Free | ✅ |
| 30 days data history | ✅ |
| Semua indikasi | ✅ |
| Export CSV | ✅ 10x/bulan |
| Export PDF | ✅ 5x/bulan |
| API access | ❌ |
| Alert | ❌ |

### Pro Tier (15 Pi/bulan)
| Feature | Access |
|---------|--------|
| Semua Basic | ✅ |
| Unlimited history | ✅ |
| Unlimited export CSV/PDF | ✅ |
| API access | ✅ 1000 req/hari |
| Alert Telegram | ✅ 20 alert/bulan |
| Custom report | ✅ 2x/bulan |

### Enterprise Tier (50 Pi/bulan)
| Feature | Access |
|---------|--------|
| Semua Pro | ✅ |
| Unlimited API | ✅ |
| Unlimited alert | ✅ |
| Custom report | ✅ Unlimited |
| White-label | ✅ |
| Priority support | ✅ |

---

## Technical Integration

### Option A: Pi App Studio (Recommended for MVP)

**Pros:**
- Built-in payment button
- No backend needed
- Quick launch (hari, bukan minggu)
- Pi handles payment verification

**Cons:**
- Limited customization
- Tied to Pi Browser ecosystem

**Implementation:**
```
1. Generate app dengan Pi App Studio AI
2. Tambah "Premium" button di dashboard
3. Configure payment amounts di App Studio
4. Pi handles payment → unlock features
5. Persistent storage untuk track user tier
```

### Option B: Pi SDK in Existing Apps (For Advanced)

**Pros:**
- Full control over UX
- Bisa diintegrasikan ke existing web apps
- More flexible

**Cons:**
- Butuh backend development
- Perlu server-side verification
- Longer development time

**Implementation:**
```bash
# Install Pi SDK
npm install @pi-network/sdk

# Frontend integration
import { Pi } from '@pi-network/sdk';

const pi = new Pi({
  appId: 'your-app-id',
  apiKey: 'your-api-key',
  environment: 'testnet' // or 'mainnet'
});

// Payment flow
async function upgradeTier(tier) {
  const payment = await pi.createPayment({
    amount: tier.price,
    description: `Upgrade to ${tier.name}`,
    metadata: { userId: user.id, tier: tier.id }
  });
  
  payment.on('completed', async (txid) => {
    // Verify on backend
    await fetch('/api/verify-payment', {
      method: 'POST',
      body: JSON.stringify({ txid, userId: user.id })
    });
    // Unlock features
    unlockTier(tier);
  });
}
```

---

## Payment Flow

```
┌─────────────────────────────────────────────────┐
│  User clicks "Upgrade to Pro"                   │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│  Pi Payment Dialog opens                        │
│  ─────────────────────────────────────────────  │
│  Amount: 15 Pi                                  │
│  Description: "MATA Pro Tier - 1 month"        │
│  [Confirm]  [Cancel]                           │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│  User confirms in Pi Wallet                     │
│  ─────────────────────────────────────────────  │
│  Transaction broadcast to Pi blockchain        │
│  Status: Pending → Completed                   │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│  Backend receives payment webhook               │
│  ─────────────────────────────────────────────  │
│  Verify transaction on Pi blockchain           │
│  Update user tier in database                  │
│  Send confirmation to user                     │
└─────────────────────────────────────────────────┘
                      │
                      ▼
�┌─────────────────────────────────────────────────┐
│  User tier upgraded!                            │
│  ─────────────────────────────────────────────  │
│  Features unlocked                             │
│  Access until: 2026-10-16                      │
│  [Start Using Premium Features]                │
└─────────────────────────────────────────────────┘
```

---

## Backend Requirements

### Database Schema

```sql
-- Users table
CREATE TABLE pi_users (
  id TEXT PRIMARY KEY,
  pi_username TEXT UNIQUE,
  pi_user_id TEXT UNIQUE,
  tier TEXT DEFAULT 'free',
  tier_expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Payments table
CREATE TABLE pi_payments (
  id TEXT PRIMARY KEY,
  pi_txid TEXT UNIQUE,
  user_id TEXT REFERENCES pi_users(id),
  amount REAL NOT NULL,
  tier TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);

-- API keys for developer access
CREATE TABLE api_keys (
  id TEXT PRIMARY KEY,
  user_id TEXT REFERENCES pi_users(key),
  key_hash TEXT UNIQUE,
  rate_limit INTEGER DEFAULT 1000,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP
);
```

### API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/user` | GET | Pi token | Get current user info |
| `/api/user/tier` | GET | Pi token | Get user tier |
| `/api/payments/create` | POST | Pi token | Create payment |
| `/api/payments/verify` | POST | Server | Verify payment |
| `/api/payments/webhook` | POST | Pi server | Payment webhook |
| `/api/dashboard` | GET | Tier-based | Dashboard data |
| `/api/export/csv` | GET | Basic+ | Export CSV |
| `/api/export/pdf` | GET | Basic+ | Export PDF |
| `/api/alert/settings` | POST | Pro+ | Configure alerts |
| `/api/alert/send` | POST | System | Send alert |

---

## Revenue Projection

### Conservative Estimate

| Month | Users | Conversion | Revenue |
|-------|-------|-----------|---------|
| 1 | 500 | 2% | 50 Pi |
| 2 | 1000 | 3% | 150 Pi |
| 3 | 2000 | 4% | 400 Pi |
| 6 | 5000 | 5% | 1250 Pi |
| 12 | 10000 | 6% | 3600 Pi |

### Optimistic Estimate

| Month | Users | Conversion | Revenue |
|-------|-------|-----------|---------|
| 1 | 1000 | 3% | 150 Pi |
| 2 | 2500 | 4% | 500 Pi |
| 3 | 5000 | 5% | 1250 Pi |
| 6 | 15000 | 6% | 4500 Pi |
| 12 | 50000 | 8% | 24000 Pi |

### Value in USD (if Mainnet)

| Pi Price | Conservative (12mo) | Optimistic (12mo) |
|----------|--------------------|------------------------|
| $36/Pi | $129,600 | $864,000 |
| $100/Pi | $360,000 | $2,400,000 |
| $300/Pi | $1,080,000 | $7,200,000 |

---

## Implementation Roadmap

### Week 1-2: Foundation
- [ ] Set up Pi Developer account
- [ ] Create app in Pi Developer Portal
- [ ] Get API keys (Testnet)
- [ ] Set up payment webhook endpoint
- [ ] Create database tables

### Week 3-4: MVP
- [ ] Implement payment creation flow
- [ ] Implement payment verification
- [ ] Create tier-based access control
- [ ] Build upgrade UI
- [ ] Test payment flow on Testnet

### Week 5-8: Features
- [ ] CSV export (Basic+)
- [ ] PDF export (Basic+)
- [ ] API access (Pro+)
- [ ] Telegram alerts (Pro+)
- [ ] Custom reports (Pro+)

### Week 9-12: Launch
- [ ] Security audit
- [ ] Performance testing
- [ ] Submit for Mainnet review
- [ ] Launch marketing
- [ ] Monitor & iterate

---

## Marketing Strategy

### Free Tier as Funnel
- Free dashboard → viral sharing
- "Powered by MATA" branding
- Referral program: invite 3 friends = 1 month Basic

### Pi Ecosystem Integration
- Submit to Pi App Store
- Cross-promote with other Pi apps
- Pi Ad Network campaigns
- Pi Chat bot integration

### Community Building
- Telegram group for premium users
- Weekly data insights
- Monthly webinar / AMA
- User-generated content

---

## Success Metrics

| Metric | Month 1 | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|---------|----------|
| Total users | 500 | 2000 | 5000 | 10000 |
| Paying users | 10 | 60 | 250 | 600 |
| Conversion | 2% | 3% | 5% | 6% |
| Monthly revenue | 50 Pi | 300 Pi | 1250 Pi | 3600 Pi |
| Churn rate | — | <10% | <8% | <5% |

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Pi Mainnet delay | High | High | Build now, monetize later |
| Low conversion | Medium | Medium | A/B test pricing, improve UX |
| Payment fraud | Low | High | Server-side verification |
| Regulatory changes | Medium | High | KYC + compliance from day one |
| Competition | Medium | Medium | Differentiate with local data |

---

## Next Actions

1. [ ] Register Pi Developer account
2. [ ] Create app in Pi Developer Portal
3. [ ] Set up Testnet environment
4. [ ] Implement payment flow MVP
5. [ ] Test with small group
6. [ ] Iterate based on feedback
7. [ ] Submit for Mainnet review
8. [ ] Launch!

---

## Files Generated

| File | Location |
|------|----------|
| This plan | `docs/reference/pi-payments-premium-dashboard-implementation.md` |
| Database schema | `services/mata-payments/schema.sql` |
| API spec | `services/mata-payments/api-spec.md` |
| Payment flow | `services/mata-payments/payment-flow.md` |

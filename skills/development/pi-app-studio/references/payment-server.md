# Pi Payments — Production Backend Setup

## Express Server Template

```javascript
require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const PI_API_BASE = 'https://api.minepi.com/v2';
const PI_API_KEY = process.env.PI_API_KEY;
const PORT = process.env.PORT || 3001;

if (!PI_API_KEY) {
  console.error('ERROR: PI_API_KEY not set');
  process.exit(1);
}

// Forward approval to Pi Platform
app.post('/api/payments/approve', async (req, res) => {
  const { paymentId } = req.body;
  if (!paymentId) return res.status(400).json({ error: 'paymentId required' });

  try {
    const response = await fetch(`${PI_API_BASE}/payments/${paymentId}/approve`, {
      method: 'POST',
      headers: { Authorization: `Key ${PI_API_KEY}` }
    });
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error('Approve error:', err);
    res.status(500).json({ error: err.message });
  }
});

// Forward completion to Pi Platform
app.post('/api/payments/complete', async (req, res) => {
  const { paymentId, txid } = req.body;
  if (!paymentId || !txid) return res.status(400).json({ error: 'paymentId and txid required' });

  try {
    const response = await fetch(`${PI_API_BASE}/payments/${paymentId}/complete`, {
      method: 'POST',
      headers: {
        Authorization: `Key ${PI_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ txid })
    });
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error('Complete error:', err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Pi Payments server running on port ${PORT}`);
});
```

## Deployment Options

| Option | Pros | Cons |
|--------|------|------|
| VPS (existing) | Full control, no extra cost | Must manage uptime |
| Vercel Functions | Easy deploy, free tier | Cold start latency |
| Cloudflare Workers | Fast, free tier | Limited Node.js compat |
| Railway/Render | Simple deploy | Monthly cost |

## Security Checklist

- [ ] `PI_API_KEY` in environment variable (never in code)
- [ ] HTTPS only (no HTTP in production)
- [ ] CORS restricted to app domain
- [ ] Rate limiting on payment endpoints
- [ ] Input validation (paymentId, txid format)
- [ ] Logging for audit trail

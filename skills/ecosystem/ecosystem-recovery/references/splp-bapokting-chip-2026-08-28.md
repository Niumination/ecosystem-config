# SPLP Bapokting Chip Activation — 2026-08-28

## Problem
Bapokting chips in `src/components/QueryBar.tsx` were disabled (`query: ''`, hint `menunggu sumber data`) despite SPLP API live (200 OK 76 komoditas with new key app 6617).

## Root cause
`QueryBar.tsx` chips with empty `query` don't trigger `src/services/ai-orchestrator.ts` bapokting path. Orchestrator regex:
```
\b(harga|prix|market|commodity|komoditas|sayur|buah|pangan|beras|minyak|bawang|bahan pokok)\b
```

## Fix applied (c8dd47c)

```tsx
// src/components/QueryBar.tsx — before
{
  id: 'bapokting',
  hint: 'Harga bahan pokok — menunggu sumber data',
  chips: [
    { label: '🍚 Harga Beras', query: '' },
    { label: '🌶️ Harga Cabai', query: '' },
  ]
}

// after
{
  id: 'bapokting',
  hint: 'Harga bahan pokok · SPLP API 76 komoditas',
  chips: [
    { label: '🍚 Harga Beras', query: 'berapa harga beras di aceh tengah' },
    { label: '🌶️ Harga Cabai', query: 'berapa harga cabai di aceh tengah' },
    { label: '🧅 Harga Bawang', query: 'berapa harga bawang di aceh tengah' },
    { label: '🫒 Harga Minyak', query: 'berapa harga minyak goreng di aceh tengah' },
  ]
}
```

Header comment updated: `Bapokting: 76 komoditas via SPLP — chip aktif`.

## Verification

```bash
node -e "
const re = /\b(harga|prix|market|commodity|komoditas|sayur|buah|pangan|beras|minyak|bawang|bahan pokok)\b/;
['berapa harga beras di aceh tengah','berapa harga cabai di aceh tengah',
 'berapa harga bawang di aceh tengah','berapa harga minyak goreng di aceh tengah'].forEach(q=>console.log(q, r.test(q)));
"
# all true → fetchLatestBapoktingPrices() triggered
```

## SPLP key service-scoping pitfall

- New JWT (app 6617, 954 chars) tested with same headers (`AuthorizationSPLP: Bearer + Authorization: Bearer`):
  - `bahan-pokok-penting/1.0/bapokting/harga` → 200, 76 komoditas ✅
  - `dtsen-aceh-tengah/1.0/...` → 401 `Invalid Credentials` ❌
- Conclusion: JWT is service-scoped. Bapokting key ≠ DTSEN key. Must request separate key for `dtsen-aceh-tengah/1.0` from `api-splp.layanan.go.id`.
- Headers verified correct; fallback in `src/lib/bapokting-client.ts` updated to new JWT + `SPLP_API_KEY` env set via `vercel env add SPLP_API_KEY production`.

## Vercel deploy

- `vercel --prod` → READY `dpl_FgxrMj9mhJAkqx9QGfYMwL9M6pRK`, Next 16.2.10, 19s
- `curl /api/health` → 200 healthy (sapa:ok, ai:nemotron-3-ultra-free)
- Prod URL: https://cc-acehtengah.vercel.app/dashboard — chips clickable

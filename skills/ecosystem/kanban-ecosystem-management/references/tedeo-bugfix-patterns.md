# TEDEO Bug-Fix Patterns (T1-T4)

TEDEO backend uses Express + Prisma + MySQL + JWT auth + Midtrans payments.
Bug fixes across 4 interconnected files follow a systematic "read all, fix atomically" pattern.

## Pattern: File-system First Audit

AGENTS.md often lists wrong file paths (`auth.js` vs `auth.ts`, `services/auth.ts` doesn't exist).
**Always scan the actual filesystem first:**

```bash
find backend/src -type f -name "*.ts" -o -name "*.js" | grep -iE 'auth|webhook|order|courier'
```

## T1 — JWT Fallback

**Root cause:** `authenticate` middleware catches ALL JWT errors with same generic 401.
Client can't distinguish expired token (refreshable) from invalid token (re-login needed).

**Fix:**
```ts
import jwt, { TokenExpiredError } from 'jsonwebtoken';

try {
  decoded = jwt.verify(token, env.JWT_SECRET);
} catch (err) {
  if (err instanceof TokenExpiredError) {
    return res.status(401).json({
      error: 'Token sudah kadaluarsa',
      code: 'TOKEN_EXPIRED',
      refreshable: true,
    });
  }
  return res.status(401).json({ error: 'Token tidak valid' });
}
```

**Key insight:** `TokenExpiredError` is a subclass of `JsonWebTokenError` — check it FIRST
with `instanceof` before the generic catch.

## T2 — Webhook Midtrans Signature

**Root cause:** `gross_amount` type mismatch between Midtrans (string, possibly with decimals)
and the code expects raw concatenation. Also staging webhooks shouldn't block on mismatch.

**Fix — normalize all values to strings and round integers:**
```ts
const computedSignature = crypto
  .createHash('sha512')
  .update(
    String(order_id) +
    String(status_code) +
    String(Math.round(Number(gross_amount))) +
    env.MIDTRANS_SERVER_KEY
  )
  .digest('hex');
```

**Staging tolerance:** In development/staging, log the mismatch instead of returning 403.
```ts
if (env.NODE_ENV !== 'production') {
  console.warn('Signature mismatch (staging — tolerating):', { order_id, status_code, gross_amount });
} else {
  return res.status(403).json({ error: 'Invalid signature' });
}
```

**Midtrans v2 signature formula:** `sha512(order_id + status_code + gross_amount + server_key)`
- All values as STRINGS (no decimal points in gross_amount)
- status_code is always a string from Midtrans ("200", "201", etc.)

## T3 — Dangling Promise Refresh Token

**Root cause:** Delete old token THEN create new token in two separate operations.
If `generateTokens()` throws after `delete`, both old and new tokens are lost.

**Fix — Prisma transaction wraps both ops atomically:**
```ts
const tokens = await prisma.$transaction(async (tx) => {
  await tx.refreshToken.delete({ where: { id: storedToken.id } });
  return generateTokens(storedToken.user.id, storedToken.user.role, tx);
});
```

**Key insight:** Pass the transaction client (`tx`) to `generateTokens` so ALL its DB writes
(including creating the new refresh token) happen in the same atomic unit.

Modify `generateTokens` to accept an optional transaction client:
```ts
async function generateTokens(userId: string, role: string, tx?: PrismaTransactionClient) {
  const client = tx || prisma;
  // ... all DB operations use `client` instead of `prisma`
}
```

## T4 — Invalid courierRelasi FK

**Root cause:** Order accept endpoint sets `courierId: req.user!.userId` without validating
that the user has an approved `courierProfile`. If the user was registered as KONSUMEN,
the FK to `courierProfile` fails.

**Fix — validate courierProfile exists before accepting:**
```ts
const profile = await prisma.courierProfile.findUnique({
  where: { userId: req.user!.userId },
});
if (!profile || !profile.isApproved) {
  return res.status(403).json({ error: 'Akun kurir belum terverifikasi' });
}
```

Also wrap with try-catch for Prisma FK violations:
```ts
try {
  // ... update order
} catch (e: any) {
  if (e.code === 'P2003') {  // Prisma FK constraint error
    return res.status(400).json({ error: 'Referensi kurir tidak valid' });
  }
  throw e;
}
```

## General Debugging Flow for TEDEO

1. **Read AGENTS.md** — get the bug descriptions and claimed file paths
2. **Scan filesystem** — find actual files (paths in AGENTS.md are often wrong about `.js` vs `.ts`)
3. **Read ALL affected files** — understand the full code before fixing any single bug
4. **Read Prisma schema** — understand the data model (especially FK relationships)
5. **Read env config** — check if API keys, secrets, endpoints are configured
6. **Fix atomically** — one patch per bug, in dependency order (auth middleware → auth routes → payment → courier)
7. **Verify** — grep for the fix markers (`TokenExpiredError`, `transaction`, `Math.round`, `isApproved`)
8. **Update AGENTS.md** — mark bugs as fixed with date

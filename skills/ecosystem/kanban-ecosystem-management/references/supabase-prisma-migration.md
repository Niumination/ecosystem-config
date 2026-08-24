# Supabase + Prisma: Handling Missing DB Tables

## Problem
Prisma schema defines a model (e.g. `ChatSession`) but the table doesn't exist in Supabase PostgreSQL. This causes HTTP 500 on any API route that queries the model.

## Root Cause
- Prisma schema is just a TypeScript type definition — it does NOT auto-create tables
- `prisma db push` or `prisma migrate deploy` must be run to create tables
- Supabase free tier auto-pauses after 7 days of inactivity — DB becomes unreachable
- `prisma.$executeRawUnsafe` for auto-migration may fail if DB user lacks CREATE TABLE permission

## Solution Pattern

### 1. Graceful API Route (return empty, not 500)
```typescript
try {
  const logs = await prisma.chatSession.findMany({ ... });
  return NextResponse.json({ logs, total });
} catch (err: any) {
  const msg = err?.message || '';
  if (msg.includes('does not exist') || msg.includes('ChatSession') || msg.includes('relation')) {
    return NextResponse.json({
      logs: [], total: 0,
      _note: 'Table not found — run SQL migration',
    });
  }
  throw err;
}
```

### 2. Provide SQL Migration File
Create `supabase/migrations/001_create_<table>.sql` with:
```sql
CREATE TABLE IF NOT EXISTS "TableName" (
    "id" TEXT NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    -- columns matching Prisma schema
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "TableName_createdAt_idx" ON "TableName"("createdAt" DESC);
```

### 3. Manual Execution by User
User runs SQL in Supabase Dashboard → SQL Editor → paste → Execute.

### 4. Non-blocking DB Save in Orchestrator
```typescript
// Don't let DB errors break the AI response to user
try {
  await prisma.chatSession.create({ data: { ... } });
} catch (dbErr) {
  console.error('[AI] DB save failed (non-blocking):', dbErr);
}
```

## Supabase Free Tier Gotchas
- **Auto-pause**: Projects pause after 7 days of no DB connections. Restore from dashboard.
- **Connection pooler**: Use `db.<ref>.supabase.co:5432?pgbouncer=true` for serverless (Vercel)
- **Direct connection**: Use `<ref>.supabase.co:5432` for migrations/scripts (no pgbouncer)
- **Permission limits**: Default `postgres` user has full access, but connection string may use limited user

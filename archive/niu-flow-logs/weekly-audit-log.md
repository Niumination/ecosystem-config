1|# Weekly Audit Log
2|
3|| Date | Projects | 🔴 | 🟡 | ⚪ | Key Finding | Report |
4||------|----------|:--:|:--:|:--:|-------------|--------|
5|| 2026-07-06 | PemdiAcehTengah, niu-vermilion, kune-ya.com | 3 | 4 | 5 | kune-ya.com domain NXDOMAIN, next-auth beta in production | [output/weekly-audit-2026-07-06.md](../output/weekly-audit-2026-07-06.md) |
6|| 2026-07-13 | PemdiAcehTengah, niu-vermilion, kune-ya.com | 6 | 8 | 9 | JCode found 5 new criticals: XSS in sanitize.js, Vercel OIDC leak, session cookie bug, timing attack, weak AUTH_SECRET; kune-ya.com STILL DOWN (7+ days) | [output/weekly-audit-2026-07-13.md](../output/weekly-audit-2026-07-13.md) |
|| **2026-07-13 (fix)** | TEDEO, kune-ya.com, niu-vermilion, PemdiAcehTengah | ✅ 3 fixed | ✅ 3 fixed | — | **TEDEO web deployed** (https://tedeo-web.vercel.app), **kune-ya.com redeployed** (https://kune-ya-com.vercel.app), **XSS fixed** (sanitize.js), **session cookie bug fixed** (niu-vermilion), **timing-safe password** added, **analytics auth** added, **rate limit path** fixed, **Supabase-backed rate limiting** implemented, middleware for dashboard gating | — |

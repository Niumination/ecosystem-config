# sapa-ai Refactor Notes

## Session Summary
- Source branch: `services/cc-acehtengah` `feat/ai-executive-answer-v3`
- Target repo: `services/sapa-ai` with local mirror `~/downloads-extracted/sapa-ai-latest`
- Goal: public SAPA-only app; preserve existing dashboard UI/structure

## Key Lessons
1. Restore original components from `cc-acehtengah` before removing non-SAPA sources.
   - Example: `QueryBar` lost its input field and submit button after rewrite; restoring from source and then removing only DTSEN/Dokumen/Bapokting chips kept the UI intact.
2. Remove source modules only after auditing all importers.
   - Deleting `src/services/*`, `src/lib/statistics/*`, and `src/data/*` caused missing-module errors in `src/app/api/health/route.ts`, `src/app/api/query/route.ts`, and `src/components/AIResponseRenderer.tsx`.
3. Rewrite API routes to the new source shape after cutting imports.
   - `/api/health` and `/api/query` were rewritten to use only `fetchSapaData`.
4. Clean remaining type unions and comments after removing sources.
   - `SapaDataOrigin`, `dataSourceLabel`, and direct-API fallback in `src/lib/sapa-client.ts` were trimmed to SPLP-only.

## Verified End State
- Sidebar: public SAPA-only nav; no Admin DTSEN, no Password/session
- QueryBar: input + Tanya button + SAPA chips only
- Backend: SAPA SPLP only
- Removed: DTSEN, Bapokting, Excel/Dokumen A/B/C, warehouse, EWS, KPI, auth

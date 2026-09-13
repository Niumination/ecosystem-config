# sapa-ai: Laporan Eksekutif + Status Merge (SAPA-only)

- Delete page: `rm -rf src/app/dashboard/akun` (not redirect), merge content into `status/page.tsx`, update Sidebar NAV.
- Report: copy `cc-acehtengah/src/services/report-generator.ts`, adapt `/api/report` to `buildReport({records, origin, kpis, alerts:null, warehouse:null})` → honest belum_aktif, 10-min cache.
- Laporan page: tab Laporan `<ExecutiveReport />` + tab Riwayat `localStorage sapa-ai-history` + CustomEvent.

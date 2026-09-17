# Pi App Studio AI — Example Prompt (MATA Watchdog)

> Full prompt used to generate MATA Watchdog app in Pi App Studio AI.

```
Create a government transparency app called "MATA — Watchdog Akuntabilitas Pengadaan Aceh Tengah" for monitoring public procurement in Central Aceh Regency, Indonesia.

APP DETAILS:
- Name: MATA Watchdog
- Tagline: "Data pengadaan publik, transparan untuk semua"
- Category: Government / Transparency
- Language: Bahasa Indonesia
- Color scheme: Professional blue (#1e3a5f) with gold (#d4af37) accents
- Mobile-first responsive design

PAGES (4 pages with bottom navigation):

PAGE 1 — DASHBOARD (Home):
- Hero section: App name, tagline, region name
- 3 metric cards in a row:
  * "657 Paket" (total packages)
  * "5 Indikasi" (active indications)
  * "2 Tinggi" (high risk)
- Total value display: "Rp 133.601.537.390"
- Section "Indikasi Terkini" showing top 5 indications with:
  * Rule name (D1-D6)
  * Provider name
  * Risk level badge (TINGGI/MEDIUM/RENDAH)
  * Short evidence text
- Buttons: "Lihat Semua Indikasi" and "Download Dossier"
- Pie chart: distribution per OPD

PAGE 2 — DAFTAR PAKET:
- Title: "Daftar Paket Pengadaan"
- Filters: Year dropdown, OPD dropdown, Status dropdown
- Search bar: "Cari nama paket atau penyedia..."
- Table with columns: No, Nama Paket, OPD, Nilai (Rp), Status
- Pagination: 20 items per page
- Each row clickable for detail view

PAGE 3 — DOSSIER:
- Title: "Dossier Pengadaan"
- List of indications with radio buttons
- Each item shows: rule, provider, packages won, percentage, risk level
- PDF preview area (placeholder)
- Buttons: "Download PDF (2 Pi)" and "Bagikan"
- Disclaimer: "Data indikasi bukan vonis. Human-in-the-loop diperlukan."

PAGE 4 — STATISTIK:
- Title: "Statistik Pengadaan"
- Line chart: Monthly trend (packages per month)
- Bar chart: Top 10 OPD by value
- Pie chart: Funding source distribution (APBD/APBN/Lainnya)
- Buttons: "Export CSV (5 Pi)" and "Export Laporan (10 Pi)"

NAVIGATION:
- Bottom tab navigation with 4 icons
- Active tab highlighted in gold

FEATURES:
- Persistent storage for user preferences
- Loading spinner on data fetch
- Error state with retry button
- Empty state with illustration
- Pi Payments integration on premium buttons
```

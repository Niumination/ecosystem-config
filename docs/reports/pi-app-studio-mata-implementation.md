# MATA Watchdog — Pi App Studio AI Implementation Plan

> **Priority:** P1
> **Platform:** Pi App Studio (Beta) — Use App Studio AI
> **Tanggal:** 2026-09-16
> **Status:** Ready for AI generation

---

## App Concept

**Name:** MATA — Watchdog Akuntabilitas Pengadaan Aceh Tengah
**Tagline:** "Data pengadaan publik, transparan untuk semua"
**Category:** Government / Transparency / Public Utility

---

## User Story

Sebagai warga Aceh Tengah, saya ingin:
1. Melihat ringkasan pengadaan publik yang mencurigakan
2. Memeriksa daftar paket pengadaan terkini
3. Mengunduh dossier PDF untuk bukti
4. Memantau statistik per OPD

Sebagai auditor/APIP, saya ingin:
1. Mendapatkan indikasi awal untuk investigasi lebih lanjut
2. Mengunduh laporan draft APIP
3. Melihat tren pengadaan per bulan/tahun

---

## App Structure (for AI Generation)

### Page 1: Dashboard Utama
```
┌─────────────────────────────────────────────────┐
│  MATA — Watchdog Akuntabilitas Pengadaan       │
│  Kabupaten Aceh Tengah                          │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ 657     │  │ 5       │  │ 2       │        │
│  │ Paket   │  │ Indikasi│  │ Tinggi  │        │
│  └─────────┘  └─────────┘  └─────────┘        │
│                                                 │
│  Total Nilai: Rp 133.601.537.390              │
│                                                 │
├─────────────────────────────────────────────────┤
│  INDIKASI TERKINI                               │
│  ─────────────────────────────────────────────  │
│  1. PT Bebesen Abadi — 10 paket (27.5%)        │
│  2. [Indikasi D2] — ...                        │
│  3. [Indikasi D3] — ...                        │
│  ...                                            │
│                                                 │
│  [Lihat Semua]  [Download Dossier]              │
├─────────────────────────────────────────────────┤
│  STATISTIK PER OPD                              │
│  [Pie Chart / Bar Chart]                        │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Page 2: Daftar Paket
```
┌─────────────────────────────────────────────────┐
│  DAFTAR PAKET PENGADAAN                         │
│  ─────────────────────────────────────────────  │
│  Filter: [Tahun ▼] [OPD ▼] [Status ▼]        │
│                                                 │
│  │ No │ Nama Paket    │ OPD      │ Nilai   │   │
│  │ 1  │ Paket A       │ Dinas X  │ 1.2M    │   │
│  │ 2  │ Paket B       │ Dinas Y  │ 800J    │   │
│  │ ...│               │          │         │   │
│                                                 │
│  [Sebelumnya] 1 2 3 ... 10 [Selanjutnya]       │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Page 3: Dossier PDF Viewer
```
┌─────────────────────────────────────────────────┐
│  DOSSIER PENGADAAN                              │
│  ─────────────────────────────────────────────  │
│  Pilih indikasi untuk lihat dossier:           │
│                                                 │
│  ○ PT Bebesen Abadi (D1 - Dominasi)            │
│  ○ [Indikasi D2]                               │
│  ○ [Indikasi D3]                               │
│                                                 │
│  [Download PDF]  [Bagikan]                     │
│                                                 │
│  Preview:                                       │
│  ┌─────────────────────────────────────────┐   │
│  │  [PDF Embed / Preview]                  │   │
│  │                                         │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Page 4: Statistik
```
┌─────────────────────────────────────────────────┐
│  STATISTIK PENGADAAN                            │
│  ─────────────────────────────────────────────  │
│                                                 │
│  Tren Bulanan                                   │
│  [Line Chart: Jumlah Paket per Bulan]          │
│                                                 │
│  Per OPD                                        │
│  [Bar Chart: Top 10 OPD by Nilai]              │
│                                                 │
│  Sumber Dana                                    │
│  [Pie Chart: APBD / APBN / Lainnya]            │
│                                                 │
│  [Download CSV]  [Export Laporan]              │
└─────────────────────────────────────────────────┘
```

---

## Pi App Studio AI Prompt

Copy-paste prompt ini ke Pi App Studio AI:

```
Create a government transparency app called "MATA — Watchdog Akuntabilitas Pengadaan Aceh Tengah" for monitoring public procurement in Central Aceh Regency, Indonesia.

APP STRUCTURE:
- 4 pages: Dashboard, Daftar Paket, Dossier, Statistik
- Mobile-first responsive design
- Color scheme: professional blue/gold (government feel)
- Language: Bahasa Indonesia

DASHBOARD PAGE:
- Hero section with app name and tagline
- 3 metric cards: Total Packages (657), Active Indications (5), High Risk (2)
- Total value display: Rp 133.601.537.390
- "Indikasi Terkini" section with top 5 indications
- Buttons: "Lihat Semua", "Download Dossier"
- Statistics per OPD (pie chart)

DAFTAR PAKET PAGE:
- Filterable table: Year, OPD, Status dropdowns
- Columns: No, Package Name, OPD, Value, Status
- Pagination (20 items per page)
- Search functionality

DOSSIER PAGE:
- List of indications with radio buttons
- PDF preview/embed
- Download PDF button
- Share button

STATISTIK PAGE:
- Monthly trend line chart
- Top 10 OPD bar chart
- Funding source pie chart
- Download CSV button
- Export report button

FEATURES:
- Persistent storage for user preferences
- Pi Payments integration for premium PDF export
- Clean, accessible UI
- Loading states
- Error handling

DATA SOURCE:
- Static demo data (will be connected to API later)
- 48 demo records with 5 indications
- Deterministic rule engine D1-D6
```

---

## Technical Architecture

```
┌─────────────────────────────────────────────────┐
│  Pi App Studio (Frontend)                       │
│  ─────────────────────────────────────────────  │
│  - Static HTML/JS/CSS generated by AI          │
│  - Pi SDK integrated                           │
│  - Pi Payments button                          │
│  - Persistent storage (new backend feature)    │
└─────────────────────────────────────────────────┘
                      │
                      │ HTTP/API Call
                      ▼
┌─────────────────────────────────────────────────┐
│  MATA Backend (VPS 103.30.146.232)             │
│  ─────────────────────────────────────────────  │
│  - Existing MATA engine (Python)               │
│  - SQLite database                             │
│  - REST API endpoints                          │
│  - PDF generation                              │
│  - CSV export                                  │
└─────────────────────────────────────────────────┘
```

### API Endpoints Needed

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/summary` | GET | Dashboard metrics |
| `/api/packages` | GET | Paginated package list |
| `/api/packages/:id` | GET | Package detail |
| `/api/indications` | GET | List of indications |
| `/api/dossier/:id/pdf` | GET | Download dossier PDF |
| `/api/statistics/opd` | GET | Stats per OPD |
| `/api/statistics/monthly` | GET | Monthly trend |
| `/api/export/csv` | GET | Export CSV |

---

## Data Schema (Demo Data)

```json
{
  "summary": {
    "total_packages": 657,
    "total_value": 133601537390,
    "active_indications": 5,
    "high_risk": 2,
    "last_updated": "2026-09-12T02:47:55+07:00"
  },
  "indications": [
    {
      "id": "D1-001",
      "rule": "D1 - Dominasi Penyedia",
      "provider": "PT Bebesen Abadi",
      "packages_won": 10,
      "total_value": 36700000000,
      "percentage": 27.5,
      "risk_level": "TINGGI",
      "evidence": [
        "PT Bebesen Abadi memenangkan 10 dari 48 proyek",
        "Porsi nilai: 27.5% dari total pengadaan"
      ]
    }
  ],
  "packages": [
    {
      "id": "10863328000",
      "name": "Paket E — Saluran air (Tahap 4)",
      "opd": "Dinas Perumahandan Permukiman",
      "value": 1978682052,
      "status": "Non Tender",
      "source": "APBD",
      "year": 2026
    }
  ]
}
```

---

## Implementation Steps

### Phase 1 — Generate App (Pi App Studio AI)
1. Buka Pi Browser → App Studio
2. Pilih "Use App Studio AI (Beta)"
3. Paste prompt di atas
4. Review generated app
5. Iterate jika perlu

### Phase 2 — Customize & Branding
1. Upload logo MATA
2. Adjust colors (blue/gold government theme)
3. Add Pi Payments button for premium features
4. Configure persistent storage

### Phase 3 — Connect to Backend
1. Deploy MATA API endpoints to VPS
2. Configure CORS for Pi Browser
3. Test API calls from Pi App
4. Handle errors gracefully

### Phase 4 — Test & Submit
1. Test on Testnet
2. Verify Pi Payments flow
3. Submit for Mainnet review
4. Launch to 60M+ Pioneers

---

## Monetization (Pi Payments)

| Feature | Price |
|---------|-------|
| Basic dashboard | Gratis |
| Daftar paket | Gratis |
| Statistik dasar | Gratis |
| Download dossier PDF | 2 Pi |
| Export CSV lengkap | 5 Pi |
| Laporan bulanan | 10 Pi |
| Custom report | 20 Pi |

---

## Success Metrics

| Metric | Target (30 hari) |
|--------|-----------------|
| Total users | 1000+ |
| Daily active users | 100+ |
| PDF downloads | 50+ |
| Pi revenue | 200+ Pi |
| User retention | 40%+ |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Data sensitivity | Only public data, no PII |
| WAF blocking | Use API proxy, not direct scrape |
| Low Pi adoption | Free tier as funnel |
| Mainnet rejection | Follow guidelines strictly |

---

## Next Actions

1. [ ] Buka Pi Browser dan login
2. [ ] Navigate ke App Studio
3. [ ] Paste prompt dan generate app
4. [ ] Review dan iterate
5. [ ] Submit untuk review

---

## Files Generated

| File | Location |
|------|----------|
| This plan | `docs/reference/pi-app-studio-mata-implementation.md` |
| Demo data | `labs/mata-aihackfest-2026/mata/data/demo_api.json` |
| API spec | `labs/mata-aihackfest-2026/docs/api-spec.md` |

# MATA Watchdog — Pi App Studio AI (Final Prompt)

> **Siap copy-paste ke Pi App Studio AI**
> **Terakhir diupdate:** 2026-09-16

---

## Prompt untuk Pi App Studio AI

Copy-paste seluruh teks di bawah ini ke dialog Pi App Studio AI:

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
- Persistent storage for user preferences (language, last visited page)
- Loading spinner on data fetch
- Error state with retry button
- Empty state with illustration
- Pi Payments integration on premium buttons

DATA (use as static JSON in the app):

Summary:
- total_packages: 657
- total_value: 133601537390
- active_indications: 5
- high_risk: 2
- last_updated: "2026-09-12"
- region: "Kabupaten Aceh Tengah"

Top 5 Indications:
1. D1 - Dominasi Penyedia | PT Bebesen Abadi | 10 paket | 27.5% | TINGGI
2. D2 - Penggelembungan Harga | PT Cipta Karya | 3 paket | 3.4% | TINGGI
3. D3 - Perubahan Kontrak Berulang | CV Maju Bersama | 5 paket | 6.7% | SEDANG
4. D4 - Pengadaan Mendesak | PT Nusantara | 2 paket | 0.9% | SEDANG
5. D5 - Pembatasan Peserta | Multi vendor | 0 paket | 0% | RENDAH

Top 5 Packages:
1. Paket E — Saluran air (Tahap 4) | Dinas Perumahan | Rp 1.978.682.052 | Non Tender
2. Paket G — Jalan lingkungan (Tahap 6) | Dinas Perumahan | Rp 1.938.691.637 | Tender
3. Paket J — Jalan lingkungan (Tahap 9) | Dinas PU | Rp 1.921.715.915 | Non Tender
4. Paket K — Perbaikan talud (Tahap 10) | Dinas PU | Rp 1.788.512.900 | Non Tender
5. Paket I — Pengadaan meubelair (Tahap 8) | Dinas PU | Rp 1.599.845.158 | E-Katalog

Statistics by OPD:
- Dinas PU: 180 paket, Rp 45M
- Dinas Kesehatan: 120 paket, Rp 28M
- Dinas Perumahan: 95 paket, Rp 22M
- Dinas Pendidikan: 85 paket, Rp 18M
- Sekda: 60 paket, Rp 12M
- Lainnya: 117 paket, Rp 8.6M

Monthly trend (packages):
Jan:45, Feb:52, Mar:48, Apr:61, Mei:55, Jun:72, Jul:68, Agu:75, Sep:80, Okt:45, Nov:32, Des:24

Funding source:
- APBD: 580 paket, Rp 125M
- APBN: 45 paket, Rp 6.5M
- Lainnya: 32 paket, Rp 2.1M

IMPORTANT:
- Use Indonesian language throughout
- Format numbers with thousand separators (Rp 1.000.000 not Rp 1000000)
- Risk badges: TINGGI=red, SEDANG=yellow, RENDAH=green
- Professional government-style design
- Accessible contrast ratios
- Smooth page transitions
```

---

## Langkah Implementasi

### Step 1: Generate App
1. Buka **Pi Browser**
2. Navigate ke **App Studio** (di menu utama)
3. Pilih **"Use App Studio AI (Beta)"**
4. Paste prompt di atas ke dialog
5. Tunggu AI generate app (1-5 menit)
6. Review hasilnya

### Step 2: Customize
1. Upload logo MATA (jika ada)
2. Adjust colors jika perlu
3. Test semua halaman
4. Pastikan data tampil benar

### Step 3: Add Pi Payments
1. Di App Studio, ke Settings → Payments
2. Enable Pi Payments
3. Set harga untuk:
   - Download PDF: 2 Pi
   - Export CSV: 5 Pi
   - Export Laporan: 10 Pi
4. Test payment flow di Testnet

### Step 4: Test & Submit
1. Test semua fitur
2. Pastikan payment berjalan di Testnet
3. Submit untuk Mainnet review
4. Tunggu approval (biasanya 1-2 minggu)

---

## Demo Data

Demo data tersimpan di:
`labs/mata-aihackfest-2026/mata/data/pi_demo_api.json`

Gunakan data ini sebagai static JSON di dalam app (belum perlu API call).

---

## Next Actions

1. [ ] Buka Pi Browser
2. [ ] Generate app dengan prompt di atas
3. [ ] Review dan customize
4. [ ] Add Pi Payments
5. [ ] Test di Testnet
6. [ ] Submit untuk Mainnet review

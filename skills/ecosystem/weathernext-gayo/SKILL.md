---
name: weathernext-gayo
description: Analisis cuaca mikro dan peringatan dini bencana untuk dataran tinggi Gayo (Aceh Tengah) berbasis pipeline WeatherNext / meteorologi resolusi tinggi. Digunakan saat membutuhkan data cuaca presisi, analisis iklim perkebunan kopi Arabika (risiko karat daun, rekomendasi penjemuran), serta mitigasi bencana hidrometeorologi (longsor lereng terjal, luapan Danau Lut Tawar).
tags:
  - ecosystem
  - weather
  - weathernext
  - coffee-agriculture
  - disaster-mitigation
  - aceh-tengah
  - gayo
last_updated: "2026-09-07"
version: 1.0.0
changes:
  - Initial release: WeatherNext Gayo agro-climate & disaster risk CLI integration
---

# ☕ WeatherNext Gayo — Agro-Climate & Disaster Mitigation Engine

## Trigger
Gunakan skill ini ketika pengguna bertanya tentang:
- Cuaca di Aceh Tengah / Takengon / Dataran Tinggi Gayo (suhu, curah hujan, angin, kelembapan).
- Kondisi iklim perkebunan kopi Arabika Gayo (risiko jamur karat daun *Hemileia vastatrix*, jendela penjemuran gabah/green bean).
- Peringatan dini bencana alam hidrometeorologi (potensi longsor perbukitan, luapan Danau Lut Tawar / DAS Peusangan, angin kencang).
- Integrasi pipeline data Google WeatherNext 3 / ECMWF resolusi tinggi (0.05° - 0.1°).

## Eksekusi Tool CLI
Jalankan skrip yang tersedia di skill ini:
```bash
# Format laporan teks terminal
python3 ~/Desktop/Niumination/skills/ecosystem/weathernext-gayo/scripts/weathernext_gayo.py [lokasi]

# Format JSON murni untuk integrasi API / Dashboard
python3 ~/Desktop/Niumination/skills/ecosystem/weathernext-gayo/scripts/weathernext_gayo.py [lokasi] --json
```

### Daftar Lokasi Tersedia:
- `bebesan` (Kemili, Datu Beru, sentral perdagangan kopi)
- `takengon` (Pusat kota Takengon)
- `pegasing` (Sentra perkebunan kopi Arabika)
- `kutepanang` (Highland kopi elevasi tinggi ~1450 mdpl)
- `atulintang` (Perkebunan kopi organik)
- `jagongjeget` (Plato transmigran selatan)
- `luttawar` (Pesisir Danau Lut Tawar)
- `bintang` (Hulu DAS Peusangan)
- `kebayakan`, `bies`, `silihnara`, `ketol`, `celala`, `rusipantara`, `linge`

## Logika Domain Analisis
1. **Suhu Optimal Kopi Arabika:** 15°C – 24°C. Suhu >25°C meningkatkan risiko hama PBKo (*Hypothenemus hampei*).
2. **Risiko Karat Daun (*Hemileia vastatrix*):** Terjadi jika Kelembapan Relatif (RH) >= 85% bersamaan dengan suhu hangat (18–25°C).
3. **Jendela Penjemuran:** Dinilai berdasarkan *direct normal solar irradiance* dan ketiadaan presipitasi hujan.
4. **Peringatan Dini Longsor:** Dipicu jika akumulasi hujan harian >= 50 mm atau hujan intensitas tinggi >= 15 mm/jam di topografi lereng curam.
5. **Mitigasi Danau Lut Tawar:** Pemantauan DTA (Daerah Tangkapan Air) di sekeliling danau untuk mencegah banjir rob pesisir danau.

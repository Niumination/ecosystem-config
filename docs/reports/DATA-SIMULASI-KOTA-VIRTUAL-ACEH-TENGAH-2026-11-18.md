# Data Spesifikasi — Simulasi Kota Virtual 3D Kabupaten Aceh Tengah (Takengon)

> Dibuat: 18 November 2026 · Sumber thread Niu-MissionControl (General) + riset terverifikasi.
> Gunakan dokumen ini sebagai payload data untuk engine simulasi (bagian A/B/C) dan blok JSON di lampiran untuk disuntikkan langsung ke kode.
> Legenda: **[V]** = sumber resmi dibuka · **[U]** = UNCHECKED/perkiraan. Angka yang bertentangan antar-sumber dicatat, jangan dipilih diam-diam.

---

### 1. Danau Lut Tawar (Laut Tawar)

**Pusat & geometri**
- Titik pusat: **4.6112°N, 96.9267°E** (Wikidata Q3124736) — https://www.wikidata.org/wiki/Q3124736
- Pusat versi OSM: **4.61118°N, 96.92305°E** — https://www.openstreetmap.org/relation/3061065
- Wikipedia: **4°36′43″N, 96°55′25″E** (4.61194, 96.92361) — https://id.wikipedia.org/wiki/Danau_Laut_Tawar
- Bounding box OSM (lonjong): lat **4.5795–4.6428°N**, lon **96.8499–96.9967°E** → bentang ~16,5 km × ~7 km — https://www.openstreetmap.org/relation/3061065
- Orientasi: sumbu panjang **barat–timur, sedikit miring ke tenggara** (pasangan titik ujung terdekat ~(4.6175, 96.8500) → (4.5926, 96.9967)) — dihitung dari geometri OSM https://www.openstreetmap.org/relation/3061065 ; sumber literatur menyebut "barat laut–tenggara" — https://ejournal.uit-lirboyo.ac.id/index.php/IJHSS/article/download/5398/1643/

**Morfometri (sumber resmi pemkab, RPJM 2012–2017)**
- Elevasi permukaan: **1.230 m dpl** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Luas permukaan: **5.742,10 ha** (57,42 km²) — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Kedalaman maksimum: **84,23 m** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Kedalaman rata-rata: **25,19 m** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Panjang maksimum: **15,727 km** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Lebar maksimum: **4,563 km** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Panjang garis pantai: **43,92 km** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Littoral area: **14,28%** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Debit rata-rata air: **538,84 juta kiloliter**; outlet tunggal **Sungai Peusangan** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf

**Versi angka lain (berbeda sumber — lihat catatan konflik)**
- Luas 5.472 ha, panjang 17 km, lebar 3,219 km — DJKN Kemenkeu https://www.djkn.kemenkeu.go.id/artikel/baca/13906/Ikan-Depik-Salah-Satu-Ikan-Endemik-Makanan-Khas-Danau-Laut-Tawar.html
- Luas permukaan 70 km², kedalaman maks 80 m, elevasi 1.100 m — Wikipedia EN https://en.wikipedia.org/wiki/Lake_Laut_Tawar
- Volume ~2.537.483.884 m³ (2,5 triliun liter) — Wikipedia ID https://id.wikipedia.org/wiki/Danau_Laut_Tawar

**Posisi relatif terhadap Takengon**
- Takengon berada di **sisi barat** danau; danau di **sebelah timur** kawasan perkotaan Takengon — https://id.wikipedia.org/wiki/Danau_Laut_Tawar ; https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- Daerah tangkapan danau masuk 4 kecamatan: **Lut Tawar, Kebayakan, Bebesen, Bintang** — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- 25 aliran/sungai masuk dari 18 daerah hulu — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf

---

### 2. Gunung / Bukit

**Burni Telong (Gunung Burni Telong / Bur Ni Telong)**
- Koordinat puncak: **4°46′00″N, 96°49′19″E** (4.76667, 96.82194) — https://id.wikipedia.org/wiki/Gunung_Burni_Telong
- Wikidata: **4.7697°N, 96.8212°E** — https://www.wikidata.org/wiki/Q24822314
- ESDM/Badan Geologi: **4°46′00″LU, 96°48′00″BT** — https://geologi.esdm.go.id/perpustakaan/?p=show_detail&id=20430
- Ketinggian: **2.624 m dpl** — https://geologi.esdm.go.id/perpustakaan/?p=show_detail&id=20430 ; https://id.wikipedia.org/wiki/Gunung_Burni_Telong
- Jenis: stratovolcano (gunung api kerucut), 3 kawah A/B/C di puncak — https://geologi.esdm.go.id/perpustakaan/?p=show_detail&id=20430
- Letusan terakhir: **1924** — https://id.wikipedia.org/wiki/Gunung_Burni_Telong
- Jarak ke Takengon: **±17 km** (Takengon di selatan gunung) — https://www.acehtrend.com/news/burni-telong/index.html ; https://id.scribd.com/document/391343999/Bener-Meriah
- ±5 km dari Redelong (ibukota Bener Meriah) & Bandara Rembele — https://id.scribd.com/document/440990533/Objek-dan-daya-tarik-wisata-di-Aceh-1
- Administrasi: kini **Kabupaten Bener Meriah** (Wikidata P131) https://www.wikidata.org/wiki/Q24822314 — sumber lama (ESDM 1977) menyebut Aceh Tengah/Takengon https://geologi.esdm.go.id/perpustakaan/?p=show_detail&id=20430

**Punggungan Bukit Barisan**
- Aceh Tengah adalah bagian dari rangkaian **Pegunungan Bukit Barisan** yang membujur sepanjang Sumatera — https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah ; https://repositori.kemdikbud.go.id/16930/1/Sangkhakala%20Berkala%20Arkeologi%20-%20XIV%20Nop%202004%20-%20Balai%20Arkeologi%20Medan.pdf
- Burni Telong terletak di lereng selatan **Gunung Geureudong** — https://geologi.esdm.go.id/perpustakaan/?p=show_detail&id=20430

**Gunung/bukit lain di sekitar Danau Lut Tawar**
- **Burni Klieten** (puncak tertinggi Kab. Aceh Tengah): **2.930 m dpl** https://www.liputan6.com/lifestyle/read/5611693/6-fakta-menarik-gunung-burni-kelieten-di-aceh-terkenal-lewat-danau-laut-tawarnya ; sumber arkeologi menyebut 2.640 m https://repositori.kemdikbud.go.id/16930/1/Sangkhakala%20Berkala%20Arkeologi%20-%20XIV%20Nop%202004%20-%20Balai%20Arkeologi%20Medan.pdf — koordinat OSM "Gunung Burniklieuteun" **4.5522°N, 96.9574°E** https://www.openstreetmap.org/ ; admin Kejuruan Syiah Utama, Kec. Bintang https://www.liputan6.com/lifestyle/read/5611693/6-fakta-menarik-gunung-burni-kelieten-di-aceh-terkenal-lewat-danau-laut-tawarnya
- **Burni Kul / Bur Kul**: **2.679 m** (arkeologi) / 2.670 m — https://repositori.kemdikbud.go.id/16930/1/Sangkhakala%20Berkala%20Arkeologi%20-%20XIV%20Nop%202004%20-%20Balai%20Arkeologi%20Medan.pdf ; OSM "Burni Kul" **4.6848°N, 97.0485°E** https://www.openstreetmap.org/
- **Burni Bies**: **2.076 m** — https://repositori.kemdikbud.go.id/16930/1/Sangkhakala%20Berkala%20Arkeologi%20-%20XIV%20Nop%202004%20-%20Balai%20Arkeologi%20Medan.pdf
- **Burni Pepanyi**: **2.300 m** — https://repositori.kemdikbud.go.id/16930/1/Sangkhakala%20Berkala%20Arkeologi%20-%20XIV%20Nop%202004%20-%20Balai%20Arkeologi%20Medan.pdf
- **Gunung Geureudong**: **2.855 m** — https://media.neliti.com/media/publications/146810-ID-none.pdf ; OSM **4.8130°N, 96.8200°E** https://www.openstreetmap.org/
- **Gunung Abong-Abong** (selatan, perbatasan Gayo Lues/Nagan Raya): **3.000 m** — https://repositori.kemdikbud.go.id/16930/1/Sangkhakala%20Berkala%20Arkeologi%20-%20XIV%20Nop%202004%20-%20Balai%20Arkeologi%20Medan.pdf ; OSM **4.4693°N, 96.6959°E** (Atu Lintang) https://www.openstreetmap.org/
- **Bukit Birah Panyang** — di kaki bukit ini Gua Loyang Koro berada — https://www.safariwisata.co.id/tempat-wisata-di-aceh-tengah/
- **Puncak Pantan Terong**: **1.800 m dpl**, ±15 menit dari Takengon — https://jelajah.kompas.id/kopi-nusantara/baca/negeri-nan-teduh/

---

### 3. Kota Takengon

- Koordinat: **4°37′35″N, 96°50′51″E** (4.62639, 96.84750) — https://en.wikipedia.org/wiki/Takengon
- Mapcarta: **4.623°N, 96.8489°E** — https://mapcarta.com/Takengon
- Wikidata: **4.6°N, 96.85°E** — https://www.wikidata.org/wiki/Q4189818
- Referensi OSM (terminal bus): **4.62463°N, 96.85075°E** https://www.openstreetmap.org/
- Ketinggian: **±1.200 m dpl** https://id.wikipedia.org/wiki/Takengon_(kota) ; **1.258 m** https://en.wikipedia.org/wiki/Takengon ; Mapcarta **1.256 m** https://mapcarta.com/Takengon
- Kecamatan yang meliputi kota: **Lut Tawar, Bebesen, Kebayakan** — https://id.wikipedia.org/wiki/Takengon_(kota)
- Kota Takengon hanya terdiri dari **2 kelurahan**: Takengon Timur & Takengon Barat — https://id.wikipedia.org/wiki/Takengon_(kota)
- Luas 3 kecamatan perkotaan: **16.023,63 ha** (Lut Tawar 8.310,16; Kebayakan 4.817,95; Bebesen 2.895,52) — https://repository.unpas.ac.id/33902/4/05.BAB%20IIII.docx
- Ketinggian lereng perkotaan berkisar **1.000–2.000 m dpl**, dominasi 1.250–1.500 m — https://repository.unpas.ac.id/33902/4/05.BAB%20IIII.docx

**Kabupaten Aceh Tengah (konteks)**
- Koordinat kabupaten: **4°31′N, 96°52′E** (4.517, 96.867) — https://en.wikipedia.org/wiki/Central_Aceh_Regency
- Luas: **4.527,58 km²** (BPS 2024, thn 2023) https://acehtengahkab.bps.go.id/id/publication/2024/02/28/9514a05ddeb7675e8606cf6b/kabupaten-aceh-tengah-dalam-angka-2024.html ; Wikipedia **4.454,04 km²** https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah (beda tahun/ukur)
- Letak astronomis: 4°10′33″–5°57′50″ LU, 95°15′40″–97°20′25″ BT — https://acehtengahkab.bps.go.id/id/publication/2024/02/28/9514a05ddeb7675e8606cf6b/kabupaten-aceh-tengah-dalam-angka-2024.html
- Ketinggian wilayah: **200–2.640 m dpl** https://repositori.kemdikbud.go.id/16930/1/Sangkhakala%20Berkala%20Arkeologi%20-%20XIV%20Nop%202004%20-%20Balai%20Arkeologi%20Medan.pdf

**14 Kecamatan + luas (BPS 2024, tahun 2023)**
| Kecamatan | Ibukota | Ketinggian (m) | Luas (km²) |
|---|---|---|---|
| Linge | Isaq | 329–2800 | 1.862,66 |
| Atu Lintang | Merah Mege | 1350–2800 | 67,17 |
| Jagong Jeget | Jeget Ayu | 1400–2450 | 171,24 |
| Bintang | Bintang | 250–2600 | 521,95 |
| Lut Tawar | Takengon Timur | 1200–2200 | 87,59 |
| Kebayakan | Kebayakan | 1200–1925 | 54,83 |
| Pegasing | Simpang Kelaping | 1200–2200 | 271,78 |
| Bies | Atang Jungket | 1200–1875 | 14,01 |
| Bebesen | Kemili | 1200–2025 | 29,57 |
| Kute Panang | Ratawali | 875–1800 | 35,15 |
| Silih Nara | Angkup | 800–2025 | 91,48 |
| Ketol | Rejewali | 200–1675 | 598,66 |
| Celala | Berawang Gading | 925–1425 | 136,21 |
| Rusip Antara | Pantan Tengah | 500–1575 | 594,25 |
| **Total** | Takengon | 200–2200 | **4.527,58** |

Sumber: https://acehtengahkab.bps.go.id/id/publication/2024/02/28/9514a05ddeb7675e8606cf6b/kabupaten-aceh-tengah-dalam-angka-2024.html
14 kecamatan & 295 gampong berdasarkan Qanun No. 4 Tahun 2011 — https://acehtengahkab.bps.go.id/id/publication/2024/02/28/9514a05ddeb7675e8606cf6b/kabupaten-aceh-tengah-dalam-angka-2024.html

---

### 4. Pusat Pemerintahan

**Kantor Bupati Aceh Tengah**
- Alamat: **Jl. Kol. Yos Sudarso (Jl. Commondore No. 1), Takengon, Kode Pos 24511** — https://id.scribd.com/doc/20643807/Daftar-Alamat-Pemda-Se-Indonesia ; https://id.scribd.com/document/789952034/Perbup-Gab-Tnd-Acc-2024
- Koordinat (OSM): **4.6217575°N, 96.8456605°E** (Tansaril, Lut Tawar) https://www.openstreetmap.org/
- Bangunan Kantor Bupati OSM: **4.621785°N, 96.845648°E** https://www.openstreetmap.org/
- Pendopo Bupati OSM: **4.61985°N, 96.84748°E** https://www.openstreetmap.org/
- Musara Alun (balai musyawarah, Jl. Yos Sudarso Blang Kolak II): **4.622811°N, 96.843042°E** — https://data.acehprov.go.id/ca/dataset/972cd483-0f94-44b0-9234-a71c68f2f73d/resource/fca6e8ec-6601-4bb4-9a02-79bcac4b46b8/download/data-lokasi-wifi-taman-digital-kab_kota-tahun-2017.csv
- Terminal bus lama Lut Tawar (referensi pusat kota): **4.625030°N, 96.850440°E** — https://data.acehprov.go.id/ca/dataset/972cd483-0f94-44b0-9234-a71c68f2f73d/resource/fca6e8ec-6601-4bb4-9a02-79bcac4b46b8/download/data-lokasi-wifi-taman-digital-kab_kota-tahun-2017.csv

---

### 5. Kawasan Wisata & Budaya

**Dermaga Danau Lut Tawar / Dermaga Kota Takengon**
- Sisi barat danau, ±10 menit dari pusat Kota Takengon — https://travel.kompas.com/read/2020/10/27/151224027/danau-laut-tawar-di-aceh-tengah-wisata-sambil-naik-speed-boat
- Jarak Takengon–Lut Tawar ±1,8 km, 5 menit via Jalan Lebe Keder — https://tirto.id/tempat-wisata-di-takengon-yang-menarik-dan-hits-g7eq
- Koordinat: **[PERKIRAAN] ±4.618°N, 96.855°E** (tepi barat danau, dekat Hotel Renggali OSM 4.62118, 96.850216) https://www.openstreetmap.org/

**Dermaga Dedalu**
- Lokasi: **Desa Dedalu, Kec. Lut Tawar** (tepi jalan Takengon–Lut Tawar, dermaga di bawah jalan) — https://travel.kompas.com/read/2020/10/31/080800927/dermaga-dedalu-di-aceh-tengah-bisa-nikmati-keindahan-danau-laut-tawar
- Koordinat: **[PERKIRAAN] ±4.615°N, 96.856°E** — belum ada di OSM/Wikidata (berdasarkan posisi Desa Dedalu di tepi barat daya danau)

**Dermaga Pante Menye**
- Lokasi: Kec. Bintang, ±21 km / 30 menit dari Takengon — https://waspadaaceh.com/takengon-dan-keindahan-dermaga-pante-menye-danau-lut-tawar/ ; https://www.idntimes.com/travel/destination/wisata-takengon-aceh-tengah-c1c2-01-5fz5v-gdnycy
- Koordinat: **[PERKIRAAN] ±4.60°N, 96.97°E** (tepi timur danau, Kec. Bintang)

**Gua Loyang Koro**
- Lokasi: Desa Toweren / Toweren Uken, Kec. Lut Tawar — https://sisparnas.kemenpar.go.id/p/38495 ; https://repositori.kemendikdasmen.go.id/7613/1/BPA%20No.%2019%202008-new%201.pdf
- Koordinat (ESDM Aceh): **4°36′20.09″N, 96°53′2.32″E** (4.60558, 96.88398) https://esdm.acehprov.go.id/media/2025.06/lkpj_esdm_20241.pdf
- Koordinat (BPCB Medan): **04°38.599′LU, 096°52.064′BT** (4.64332, 96.86773) https://repositori.kemendikdasmen.go.id/7613/1/BPA%20No.%2019%202008-new%201.pdf — **[UNCHECKED: dua sumber berbeda ±4 km]**
- ±5–7 km dari Takengon, di kaki Gunung Birah Panyang, kedalaman gua ±20–110 m — https://www.safariwisata.co.id/tempat-wisata-di-aceh-tengah/ ; https://media.neliti.com/media/publications/146810-ID-none.pdf

**Buntul Rintis**
- Lokasi: **Desa Tensaren (Kampung Tansaren), Kec. Bebesen**, ±30 menit dari pusat Takengon — https://travel.kompas.com/read/2021/08/01/133100327/5-wisata-menarik-di-gayo-takengon-aceh-kunjungi-usai-ppkm
- Ketinggian: **1.730 m dpl** https://www.safariwisata.co.id/tempat-wisata-di-aceh-tengah/ (sumber lain menyebut ±2.600 m — https://sumut.idntimes.com/travel/destination/5-rekomendasi-destinasi-wisata-di-takengon-c1c2-01-m9vsh-0kvv0j — **[UNCHECKED, bertentangan]**)
- Koordinat Desa Tensaran (Wikidata): **4.648°N, 96.814°E** https://www.wikidata.org/wiki/Q12520851

**Destinasi ikonik lain**
- Pantan Terong (puncak 1.800 m, ±15 menit dari Takengon) — https://jelajah.kompas.id/kopi-nusantara/baca/negeri-nan-teduh/
- Burni Klieten (hiking, puncak tertinggi kab.) — https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah
- Krueng Peusangan (arung jeram) — https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah
- Gayo Waterpark (Pegasing) — https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah
- Taman Buru Linge Isak — https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah
- Loyang Pukes, Loyang Datu — https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah
- Kawasan Wisata Teluk Mendale (OSM): **4.641467°N, 96.865001°E** https://www.openstreetmap.org/
- Kampung Wisata Kelitu, Kampung Dedalu — https://id.scribd.com/document/862074562/Profil-Kabat

---

### 6. Sentra Perkebunan Kopi Arabika Gayo

**Luas & produksi**
- Luas perkebunan kopi Arabika Kab. Aceh Tengah: **48.300 ha**, produksi **31.395 ton (2022)** — https://id.scribd.com/document/882800606/58
- Versi BPS 2023: luas kopi **51.000 ha**, produksi 35.992 ton; arabika **49.997 ha (99%)** — https://id.scribd.com/document/882800606/58
- Data BPS/Aceh prov: Kopi Arabika Aceh Tengah **48.300 ha (2013)** — https://data.acehprov.go.id/dataset/741f460e-c4bb-4b81-a5e6-d08fb1cdbcbd/resource/9f06ddbe-c3df-4248-91e7-088b13fb3e89/download/luas-area-perkebunan-menurut-kabupatenkota.csv
- Rata-rata produktivitas **720 kg/ha** — https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah

**Sentra perkebunan**
- Kecamatan sentra: **Bebesen, Bintang, Silih Nara, Linge, Atu Lintang, Pegasing, Kute Panang, Ketol, Celala, Rusip Antara** — https://jurnal.unimed.ac.id/2012/index.php/antrophos/article/download/18494/14663,https:/jurnal.unimed.ac.id/2012/index.php/antrophos/article/download/72743/30310
- Desa sentra spesifik: Blang Gele, Bintang Kekelip, Linung Bulen I (Kec. Bintang) — https://jurnal.unimed.ac.id/2012/index.php/antrophos/article/download/18494/14663,https:/jurnal.unimed.ac.id/2012/index.php/antrophos/article/download/72743/30310

**Pusat pengolahan / eksportir**
- **CV. Oro Kopi Gayo** (Oro Coffee Gayo), Kampung Mongan/Mongal, Kec. Bebesen — berdiri Oktober 2013, ekspor green bean 5–7×/tahun — https://jurnal.usk.ac.id/agrisep/article/download/44236/22857 ; https://id.scribd.com/document/877097710/44236-152486-1-PB
  - Koordinat OSM Kampung Mongal: **4.643197°N, 96.837918°E** https://www.openstreetmap.org/
- Pabrik kilang kopi Desa Alur Gading, Kec. Pintu Rime Gayo, **Bener Meriah** (produksi 700–800 kg/ha) — https://www.antarafoto.com/id/view/2901655/produksi-kopi-arabika-kualitas-ekspor-di-bener-meriah
- Koperasi Panca Gayo Coffee (Bener Meriah; 5 desa: Sedie Jadi, Waq Pondok Sayur, Panji Mulia 1, Bale Redelong, Kute Lintang) — https://www.djkn.kemenkeu.go.id/berita/baca/30948/Pendampingan-Potensi-Desa-
- Sentra Bener Meriah: **46.723 ha** kopi arabika — https://pics.unipma.ac.id/content/download/B022_27_02_2025_09_09_14BAHAN%20PPT%20KHALID%20-%20KOPI%20ARABIKA%20GAYO.pptx.pdf

**Indikasi Geografis (IG) Kopi Arabika Gayo**
- Wilayah IG: Kab. **Aceh Tengah, Bener Meriah, Gayo Lues**; ketinggian **900–1.700 m dpl** — http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52016XC1101(03)
- Luas wilayah IG yang sesuai DTG: **160.856,70 ha** — https://media.neliti.com/media/publications/2187226-analisis-indikasi-geografis-kopi-arabika.pdf

---

### 7. Data Penunjang

**Iklim (Takengon)**
- Suhu rata-rata: **±20,1 °C**; bulan terpanas April–Mei **26,6 °C**; terdingin September **19,7 °C** — https://id.scribd.com/document/353822125/BPS-Bab-II-28okt
- Kelembapan rata-rata **80,08%** (terbasah 86,28%, terkering 74,25%) — https://id.scribd.com/document/353822125/BPS-Bab-II-28okt
- Curah hujan **1.082–2.409 mm/tahun**, 113–160 hari hujan; tertinggi November **316,5 mm**, terendah Juli **6,2 mm** — https://id.scribd.com/document/353822125/BPS-Bab-II-28okt
- Tipe iklim Schmidt-Ferguson **B** (tropis) — https://id.scribd.com/document/353822125/BPS-Bab-II-28okt
- Suhu harian per Climate-Data.org: rata-rata **20,66 °C**, rainfall **1.780 mm/tahun** — https://id.wikipedia.org/wiki/Takengon_(kota)
- Kisaran harian lapangan: **18–23 °C**, kelembapan 70–93% — https://gayo.tribunnews.com/aceh-tengah/55165/prakiraan-cuaca-aceh-tengah-17-november-2026-pagi-berawan-waspadai-hujan-siang-hingga-malam-hari

**Danau / sumber air lain**
- Kab. Aceh Tengah punya **3 danau**; Laut Tawar yang terbesar — https://dispertanahan.acehtengahkab.go.id/media/2023.08/rpjmk_aceh_tengah_tahun_2017-2022_full1.pdf
- **Krueng Peusangan**: hulu di Danau Lut Tawar, sungai utama **128 km** (dari laut Bireuen ke danau), DAS **238.550 ha**, 107 sungai anak, 12 sub-DAS — https://www.mongabay.co.id/2017/01/24/krueng-peusangan-daerah-aliran-sungai-potensial-yang-luput-dari-perhatian/
- PLTA Peusangan I, Dusun Singkiren, Kampung Semelit Mutiara, Kec. Silih Nara: **88,90 MW** — https://id.scribd.com/presentation/330400379/RENCANA-TATA-RUANG-WILAYAH-KABUPATEN-ACEH-TENGAH-pptx
- PLTA Peusangan II (Lut Tawar, Bies, Pegasing, Silih Nara): **86,00 MW** — https://id.scribd.com/document/604918664/RTRW-Aceh-Tengah
- DAS lain di Aceh Tengah: Krueng Woyla, Jambo Aye, Meureubo, Tripa, Tamiang, Seunagan — https://id.scribd.com/document/353822125/BPS-Bab-II-28okt
- Danau lain di Aceh (di luar Aceh Tengah): Aneuk Laot (Sabang), Peastep/Paris/Bungara/Pinang/Lincier (Aceh Singkil), Laut Bangko (Aceh Selatan), Ceunampong (Aceh Jaya), Cot Girek (Aceh Utara), Laot Tadu (Nagan Raya) — https://id.wikipedia.org/wiki/Danau_di_Aceh

**Jarak tempuh antarkawasan utama**
- Banda Aceh → Takengon: **315 km, 7–8 jam** — https://tirto.id/tempat-wisata-di-takengon-yang-menarik-dan-hits-g7eq ; https://jelajah.kompas.id/kopi-nusantara/baca/negeri-nan-teduh/
- Banda Aceh → Bener Meriah: **322 km, ±6 jam 42 menit** — https://www.djkn.kemenkeu.go.id/kanwil-aceh/baca-berita/22549/Asset-Trip-Percepatan-Sertipikasi-BMN-2021-Jilid-1-Banda-Aceh-Bener-Meriah-Takengon.html
- Bener Meriah (Simpang Tiga Redelong) → Takengon: **±18 km, 30 menit** — https://www.kompas.id/artikel/mencicip-kopi-gayo-langsung-di-tanah-asal-bagaimana-caranya
- Takengon → Danau Lut Tawar: **1,8 km, 5 menit** — https://tirto.id/tempat-wisata-di-takengon-yang-menarik-dan-hits-g7eq
- Takengon → Buntul Rintis: **±30 menit** — https://www.safariwisata.co.id/tempat-wisata-di-aceh-tengah/
- Takengon → Dermaga Pante Menye: **21 km, ±30 menit** — https://waspadaaceh.com/takengon-dan-keindahan-dermaga-pante-menye-danau-lut-tawar/
- Takengon → Loyang Koro: **±5–7 km** — https://www.safariwisata.co.id/tempat-wisata-di-aceh-tengah/
- Takengon → Burni Telong: **±17 km** — https://www.acehtrend.com/news/burni-telong/index.html
- Bandara Rembele (Bener Meriah): **4.7240147°N, 96.8489428°E** https://www.openstreetmap.org/
- Takengon → Lhokseumawe: **±119 km, ±3 jam** — https://travel.kompas.com/read/2020/10/27/151224027/danau-laut-tawar-di-aceh-tengah-wisata-sambil-naik-speed-boat

---

### Daftar Sumber

**Resmi**
- BPS Kab. Aceh Tengah, *Kabupaten Aceh Tengah Dalam Angka 2024* — https://acehtengahkab.bps.go.id/id/publication/2024/02/28/9514a05ddeb7675e8606cf6b/kabupaten-aceh-tengah-dalam-angka-2024.html
- RPJM Kab. Aceh Tengah 2012–2017 (Bab II, morfometri danau) — https://acehtengahkab.go.id/media/2020.03/06_Bab_2_Gambaran_Umum_Kondisi_Daerah.pdf
- RPJMD Kab. Aceh Tengah 2017–2022 (3 danau, morfometri) — https://dispertanahan.acehtengahkab.go.id/media/2023.08/rpjmk_aceh_tengah_tahun_2017-2022_full1.pdf
- DJKN Kemenkeu (luas/panjang/lebar danau) — https://www.djkn.kemenkeu.go.id/artikel/baca/13906/Ikan-Depik-Salah-Satu-Ikan-Endemik-Makanan-Khas-Danau-Laut-Tawar.html
- Badan Geologi ESDM (Burni Telong) — https://geologi.esdm.go.id/perpustakaan/?p=show_detail&id=20430
- Dinas ESDM Aceh, LKPJ 2024 (koordinat Loyang Koro) — https://esdm.acehprov.go.id/media/2025.06/lkpj_esdm_20241.pdf
- Balai Pelestarian Cagar Budaya Medan (koordinat Loyang Koro) — https://repositori.kemendikdasmen.go.id/7613/1/BPA%20No.%2019%202008-new%201.pdf
- Data Aceh Provinsi (koordinat Musara Alun, terminal) — https://data.acehprov.go.id/ca/dataset/972cd483-0f94-44b0-9234-a71c68f2f73d/resource/fca6e8ec-6601-4bb4-9a02-79bcac4b46b8/download/data-lokasi-wifi-taman-digital-kab_kota-tahun-2017.csv
- BPS Bab II (iklim, DAS) — https://id.scribd.com/document/353822125/BPS-Bab-II-28okt
- Situs pemkab — https://acehtengahkab.go.id
- RTRW Kab. Aceh Tengah (PLTA, DAS) — https://id.scribd.com/document/604918664/RTRW-Aceh-Tengah

**Peta / data terbuka**
- OpenStreetMap: Danau Laut Tawar https://www.openstreetmap.org/relation/3061065 ; Kantor Bupati https://www.openstreetmap.org/
- Wikidata: Danau Laut Tawar https://www.wikidata.org/wiki/Q3124736 ; Burni Telong https://www.wikidata.org/wiki/Q24822314 ; Takengon https://www.wikidata.org/wiki/Q4189818 ; Bebesen https://www.wikidata.org/wiki/Q9637483 ; Tensaran https://www.wikidata.org/wiki/Q12520851

**Rujukan silang**
- Wikipedia ID: Danau Laut Tawar https://id.wikipedia.org/wiki/Danau_Laut_Tawar ; Gunung Burni Telong https://id.wikipedia.org/wiki/Gunung_Burni_Telong ; Takengon https://id.wikipedia.org/wiki/Takengon_(kota) ; Kabupaten Aceh Tengah https://id.wikipedia.org/wiki/Kabupaten_Aceh_Tengah
- Wikipedia EN: Lake Laut Tawar https://en.wikipedia.org/wiki/Lake_Laut_Tawar ; Takengon https://en.wikipedia.org/wiki/Takengon ; Central Aceh https://en.wikipedia.org/wiki/Central_Aceh_Regency
- Kompas Travel (dermaga, jarak) — https://travel.kompas.com/read/2020/10/31/080800927/dermaga-dedalu-di-aceh-tengah-bisa-nikmati-keindahan-danau-laut-tawar
- Safari Wisata (Buntul Rintis, Loyang Koro) — https://www.safariwisata.co.id/tempat-wisata-di-aceh-tengah/
- Jurnal USK (CV Oro Kopi Gayo) — https://jurnal.usk.ac.id/agrisep/article/download/44236/22857
- EUR-Lex PGI Kopi Arabika Gayo — http://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52016XC1101(03)
- Mongabay (DAS Peusangan) — https://www.mongabay.co.id/2017/01/24/krueng-peusangan-daerah-aliran-sungai-potensial-yang-luput-dari-perhatian/

---

### UNCHECKED / perkiraan

1. **Luas danau konflik**: 5.742,10 ha (RPJM pemkab) vs 5.472 ha (DJKN/Wikipedia) vs 70 km² (Wikipedia EN). Untuk simulasi, pakai **5.742 ha / 57,42 km²** (sumber pemkab paling rinci) dan catat variasi.
2. **Koordinat Gua Loyang Koro**: ESDM (4.6056, 96.8840) vs BPCB (4.6433, 96.8677) — selisih ±4 km. Perlu ground-check.
3. **Dermaga Danau Lut Tawar / Dermaga Dedalu / Dermaga Pante Menye**: koordinat belum ada di OSM/Wikidata → semua **[PERKIRAAN]** dari nama desa/kecamatan.
4. **Buntul Rintis**: ketinggian 1.730 m vs 2.600 m (dua sumber media bertentangan). Koordinat pakai pusat Desa Tensaran (4.648, 96.814), bukan titik spot.
5. **Burni Klieten**: ketinggian 2.930 m (Liputan6) vs 2.640 m (jurnal arkeologi). Koordinat OSM "Gunung Burniklieuteun" (4.5522, 96.9574) tanpa elevasi.
6. **Burni Telong administrasi**: ESDM menyebut Aceh Tengah/Takengon; pemekaran 2003 menempatkannya di Bener Meriah. Koordinat puncak bervariasi 96,820–96,822.
7. **Volume danau**: 2.537.483.884 m³ (Wikipedia ID) tidak cocok dengan debit rata-rata pemkab 538,84 juta kiloliter — jangan campur; volume = kapasitas tampung, debit = aliran.
8. **Luas kabupaten**: 4.527,58 km² (BPS 2024) vs 4.454,04 km² (Wikipedia). Pakai BPS untuk label resmi.
9. **Jarak Bireuen–Takengon 30,4 km** (DJKN) tampak salah konteks (kemungkinan maksud Simpang Tiga Redelong–Takengon); jangan dipakai tanpa verifikasi.
10. **Iklim**: angka BPS (20,1 °C) vs Climate-Data.org (20,66 °C) vs lapangan Tribun (18–23 °C) — untuk simulasi pakai rentang **18–26 °C** dengan rata-rata ~20 °C.

---

### 1. Visi & Misi Bupati–Wakil Bupati Aceh Tengah

**Periode berjalan:** 2025–2030
**Bupati:** Drs. Haili Yoga, M.Si.
**Wakil Bupati:** Muchsin Hasan, M.SP.
*(V) Sumber: https://kesbangpol.acehtengahkab.go.id/media/2026.10/visi_misi1.pdf*

**Visi:** “**Aceh Tengah Islami, Maju, Sejahtera dan Berkeadilan**” *(V)*
Sumber: https://kesbangpol.acehtengahkab.go.id/media/2026.10/visi_misi1.pdf · https://acehtengahkab.go.id/halaman/visi-dan-misi

Makna tiap kata (pemkab): *Islami* = nilai-nilai Islam + adat/budaya · *Maju* = SDM berkualitas, pendidikan/kesehatan/infrastruktur berkualitas, tata kelola bersih · *Sejahtera* = taraf hidup, ekonomi, sosial budaya baik, tangguh, aman, damai · *Berkeadilan* = pemerataan, lestari, berkelanjutan. *(V)* (https://acehtengahkab.go.id/halaman/visi-dan-misi)

**Versi misi 8 poin (Kesbangpol, periode 2025–2030)** *(V)*:
1. Mewujudkan kehidupan masyarakat religius, berakhlak mulia, berlandaskan nilai-nilai Islam.
2. Meningkatkan kualitas SDM unggul, berdaya saing, berkarakter.
3. Memperkuat tata kelola pemerintahan bersih, transparan, akuntabel, berorientasi pelayanan publik.
4. Mendorong pembangunan ekonomi inklusif, mandiri, berkelanjutan, berbasis potensi lokal.
5. Meningkatkan kualitas pelayanan dasar, pendidikan, kesehatan, dan kesejahteraan sosial.
6. Melestarikan adat, budaya, kearifan lokal Gayo, memperkuat identitas daerah.
7. Memperkuat stabilitas politik, keamanan, ketertiban, kerukunan antar umat beragama.
8. Menjaga kelestarian lingkungan hidup dan mengurangi risiko bencana.

**Versi misi 8 poin (RPJMD 2025–2029, pemkab)** *(V)* (https://acehtengahkab.go.id/halaman/visi-dan-misi):
1. Penguatan transformasi sosial (manusia sehat, cerdas, kreatif, sejahtera, unggul, berdaya saing)
2. Penguatan transformasi ekonomi hijau dan berkelanjutan
3. Penguatan transformasi tata kelola
4. Penguatan kondusifitas & stabilitas ekonomi daerah berlandaskan syariat Islam
5. Penguatan ketahanan sosial budaya dan ekologi berbasis kearifan lokal
6. Penguatan pembangunan kewilayahan yang merata dan berkeadilan
7. Penguatan sarana & prasarana berkualitas dan ramah lingkungan
8. Penguatan kesinambungan pembangunan menuju Aceh Tengah maju

> Catatan: dua daftar misi di atas keduanya berasal dari domain pemkab tapi redaksi berbeda (versi “transformasi” = dokumen RPJMD; versi “religius/akhlak” = dokumen Kesbangpol 2025–2030). Keduanya dipakai di dashboard; jangan disatukan.

**Slogan / tagline pembangunan:**
- Tema RKPD 2025: “**Peningkatan Ekonomi Hijau Melalui Pengembangan Agrikultur Dan Pariwisata Didukung Infrastruktur Yang Handal Sebagai Modal Dasar Transformasi Pembangunan Daerah**” *(V)* (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf)
- “**Aceh Tengah Satu Data**” — tagline program Satu Data / Portal SAPA Diskominfo *(V)* (https://aceh.antaranews.com/berita/409688/diskominfo-aceh-tengah-hadirkan-inovasi-sapa)
- “**Aceh Tengah Islami, Maju, Sejahtera, dan Berkeadilan**” dipakai sebagai tagline utama visi. *(V)*
- **UNCHECKED:** tagline “Kabupaten Layak Anak”/“Gayo Land of Peace”/“Kota Kopi” — belum ada di dokumen yang dibuka. **(U)**

---

### 2. Tiga Program Unggulan (quick wins) + status verifikasi

#### P1 — Digitalisasi Layanan Publik: Portal SAPA (Satu Pintu Akses Data) + Command Center
- **Ada di dokumen/sumber resmi?** **YA — program pemkab aktif.** Diskominfo Aceh Tengah meluncurkan SAPA sebagai dasbor terpadu + AI untuk menghimpun data sektoral OPD, didukung Command Center Diskominfo. *(V)* (https://aceh.antaranews.com/berita/409688/diskominfo-aceh-tengah-hadirkan-inovasi-sapa)
- Uji coba portal SAPA digelar di Command Center Diskominfo, 4 Juni 2026. *(V)* (https://bappeda.acehtengahkab.go.id/berita/kategori/pemerintahan/sosialisasi-dan-uji-portal-sapa-satu-pintu-akses-data)
- Payung indikator: **Indeks SPBE** dan **SAKIP** di RPJMD/RKPD. *(V)* (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf)
- **Bisa divisualisasikan:** dashboard/command center 3D, aliran data OPD → satu pintu, metrik SPBE.

#### P2 — Hilirisasi Kopi Gayo & Pemberdayaan Petani
- **Ada di dokumen resmi?** **YA.** RKPD 2025 memuat indikator “Persentase peningkatan nilai ekspor komoditi kopi” dan “Hilirisasi dan pengolahan hasil pertanian” sebagai isu prioritas. *(V)* (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf)
- Kopi arabika Gayo = komoditas ekspor utama; Bappeda menggelar kajian/rencana aksi kopi berkelanjutan + Gugus Tugas Kopi Arabika Gayo. *(V)* (https://bappeda.acehtengahkab.go.id/berita/kategori/pemerintahan/penyelarasan-sistem-produksi-kopi-dan-kakao-berkelanjutan-tahan-iklim-dan-berorientasi-pasaryang-sesuai-dengan-standar-sertifikasi-internasional)
- **Bisa divisualisasikan:** peta kebun kopi per kecamatan, rantai pasok → ekspor, grafik volume/nilai ekspor.

#### P3 — Penataan Ekowisata Danau Lut Tawar & Mitigasi Lingkungan
- **Ada di dokumen resmi?** **YA.** Danau Lut Tawar (5.742,10 ha) tercatat di RKPD; isu strategis “KSK Pengembangan Pariwisata Danau Laut Tawar”; pengembangan ekowisata/geowisata/agro wisata. *(V)* (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf)
- Program RPJMD: “Laboratorium Wisata Religi, Taman Kab., museum Buru, agro Wisata, Ekowisata, Geowisata”. *(V)* (https://acehtengahkab.go.id/halaman/visi-dan-misi)
- **Bisa divisualisasikan:** model danau + dermaga, sebaran objek wisata, penghitung kunjungan wisatawan, indeks kualitas lingkungan.

#### Program unggulan lain yang ditemukan (RPJMD/RKPD)
- **Penurunan stunting** — prioritas nasional yang diadopsi RKPD 2025; target daerah 13,5% (2025) dan 5% (2045). *(V)* (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf)
- **Penurunan kemiskinan & penghapusan kemiskinan ekstrem** — fokus utama RKPD 2024/2025. *(V)* (sbg)
- **Infrastruktur transportasi & konektivitas** — “Satu Data konektivitas, Tanggul Boom-Mendale”, Rasio Konektivitas Kabupaten/Kota (IKU Dishub 2025–2029). *(V)* (https://dishub.acehtengahkab.go.id/media/2026.10/sk_iku_dishub_2025_-_20291.pdf)
- **Subuh Keliling / Safari Jumat / Ahad Berkah / BKM** (Misi 4 & 5 RPJMD). *(V)* (https://acehtengahkab.go.id/halaman/visi-dan-misi)

---

### 3. Tabel KPI Nyata

| # | Indikator | Nilai | Tahun | Target vs Realisasi | Sumber |
|---|---|---|---|---|---|
| 1 | Persentase penduduk miskin | **14,27%** (31,85 ribu jiwa) | 2024 | Target RPD 2023–2026 = 14,70% → **tercapai (103,78%, kategori A)** | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) · (https://data.acehprov.go.id/dataset/69374d14-2e6e-4284-8492-57423398f3d1) |
| 2 | Persentase penduduk miskin (tren) | 16,84% → 15,58 → 15,50 → 15,08 → 15,26 → 14,50 → 14,38 → **14,27** | 2017–2024 | — | (https://data.acehprov.go.id/dataset/69374d14-2e6e-4284-8492-57423398f3d1) |
| 3 | Jumlah penduduk miskin | **31,85 ribu jiwa** (naik 170 jiwa vs 2023) | 2024 | — | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 4 | Garis kemiskinan | **Rp626.090/kapita/bulan** | 2024 | — | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 5 | Indeks SPBE | **1,88 (kategori Cukup)** | 2023 | Target RKPD 2025 = 4 · RPD = 3 | (https://data.acehsingkilkab.go.id/dataset/b133429d-b335-4442-ae8c-7c8b3d1b6569) · (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 6 | Indeks SPBE | **Cukup** (tanpa nilai di baris Aceh Tengah) | 2024 | — | (https://satudata.menpan.go.id/datasets/spbe) |
| 7 | Indeks SPBE | **Cukup** | 2025 | — | (https://satudata.menpan.go.id/api/datasets/spbe/download?format=csv&tahun=2025) |
| 8 | Indeks SPBE (tren pemkab) | 1,54 → 1,54 → 2,33 → 1,13 → **1,88** | 2019–2023 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 9 | Nilai SAKIP Pemda | **57,09 (CC)** | 2023 | Target RKPD 2025 = 62 | (https://data.acehprov.go.id/dataset/086482b9-cc74-437e-9f6f-9949ff262f17) · (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 10 | Nilai SAKIP Pemda (tren) | 52,75 → 53,55 → 54,26 → 57,04 → **57,09** | 2019–2023 | — | (https://data.acehprov.go.id/dataset/086482b9-cc74-437e-9f6f-9949ff262f17) |
| 11 | Indeks Kepuasan Masyarakat (Kec. Lut Tawar) | **85,91** | Realisasi 2024 | Target RKPD 2025 = 84 | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 12 | Indeks Kepuasan Masyarakat (Kec. Bebesen) | **87,97** | Realisasi 2024 | Target RKPD 2025 = 89,13 | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 13 | Indeks Kepuasan Pemangku Kepentingan (Setwan) | **85,17** | Realisasi 2024 | Target RKPD 2025 = 95 | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 14 | Indeks Pelayanan Publik | **3,23** | 2023 | Target “baik” ≥ 3,51 | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 15 | IPM | **77,27** | 2024 | Target 73,78 → **tercapai (104,73%, A)** | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 16 | IPM (tren) | 75,07 → 75,20 → 75,79 → 76,45 → **77,27** → **78,09** | 2020–2025 | — | (https://acehtengahkab.bps.go.id/) |
| 17 | Rasio Gini | **0,332** | 2024 | Target 0,23 → **69,28% (BB, sangat berhasil)** | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 18 | Tingkat Pengangguran Terbuka (TPT) | **4,20%** | 2024 | Target 2,25% → 53,57% (B) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 19 | TPT (tren) | 4,44% → **4,42%** | 2022–2023 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 20 | Pertumbuhan ekonomi | **4,98%** | 2024 | Target 3,75% → **132,8% (A)** | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 21 | Pertumbuhan ekonomi (tren) | 4,23 → 4,59 → 4,05 → 4,14 → 3,26 → −1,20 → 3,21 → 4,90 → 5,60 → **4,98** | 2015–2024 | Rata-rata 9 thn = 3,64% | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 22 | PDRB per kapita | **Rp47,28 juta/kapita/tahun** | 2024 | Target 36,50 → 129,52% (A) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 23 | Nilai Tukar Petani | **181,56** | 2024 | Target 99,56 → 182,36% (A) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 24 | Inflasi (yoy, Kota Takengon) | **4,78%** (IHK 104,20 → 109,18) | Juni 2024 | Target RKPD 2025 = 3,0% | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 25 | Inflasi (tren BPS) | 1,2 → 5,37 → 3,55 → 1,97 → 1,56 | 2019–2023 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 26 | Inflasi (yoy) | **7,25%** (IHK 119,40) — tertinggi nasional | Juni 2026 | — | (https://aceh.tribunnews.com/bisnis/1035492/inflasi-aceh-tengah-tertinggi-nasional-tembus-725-persen-secara-tahunan) |
| 27 | Inflasi (yoy) | **7,11%** — tertinggi di Aceh | Oktober 2026 | — | (https://www.waspada.id/berita/inflasi-aceh-tertinggi-di-sumatera-tembus-5-05-persen-pada-oktober-2026) |
| 28 | Produksi kopi arabika | **37.008 ton** (50.034 ha) | 2023 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 29 | Produksi kopi robusta | **482 ton** (1.114 ha) | 2023 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 30 | Ekspor kopi arabika | **12.322.425 kg / US$83.290.950,53** | 2022 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 31 | Total ekspor (3 komoditas: kopi, gum rosin, gum terpentine) | **27.110.555 kg / US$108.937.492,67** | 2022 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 32 | Ekspor kopi arabika 2023 | turun **64,85%** vs 2022 | 2023 | Target RKPD 2025 “% peningkatan nilai ekspor kopi” = 57% | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 33 | Kunjungan wisatawan (objek wisata) | **1.173.202 orang** | 2023 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 34 | Lama kunjungan wisata | **2 hari** | 2023 | Target RKPD 2025 = 3 hari | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 35 | Prevalensi stunting (SSGI) | **19,2%** (Aceh Tengah) | 2024 | Target RKPD 2025 = 13,5% · nasional 14% | (https://id.scribd.com/document/869304796/V-34-Hasil-SSGI-2024-Diseminasi-BKPK-26-Mei-2025) |
| 36 | Prevalensi stunting (tren) | 59,30% (2017) → 42,24% (2019) → 34,24% (2021) → 32,00% (2022) → 23,60% (2023) | 2017–2023 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 37 | Jumlah balita stunting | 1.601 (2020) → **1.314 orang** (2022) | 2022 | — | (https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf) |
| 38 | Cakupan imunisasi dasar lengkap (rata-rata puskesmas) | **70,70%** (17 puskesmas) | 2021 | — | (https://data.acehprov.go.id/dataset/cakupan-imunisasi-pada-bayi) |
| 39 | Cakupan DPT-HB-Hib3 (rata-rata puskesmas) | **65,31%** (17 puskesmas) | 2021 | — | (https://data.acehprov.go.id/dataset/cakupan-imunisasi-pada-bayi) |
| 40 | Cakupan campak MR (rata-rata puskesmas) | **70,70%** (17 puskesmas) | 2021 | — | (https://data.acehprov.go.id/dataset/cakupan-imunisasi-pada-bayi) |
| 41 | Angka Harapan Hidup | **73,04 tahun** | 2024 | Target 69,00 → 105,86% (A) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 42 | Indeks Kualitas Lingkungan Hidup | **79,2** | Realisasi 2024 | Target 82,24 → 96,30% (A) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 43 | Indeks Reformasi Birokrasi | **67,76** | Realisasi 2024 | Target 60,50 → 112% (A) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 44 | Capaian kinerja Pemkab (total) | **108% — kategori A Memuaskan** | 2024 | 16 IKU A (88%), 1 BB, 2 B | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 45 | Opini BPK atas laporan keuangan | **WTP** | 2024 | Target RKPD 2025 = WTP | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 46 | Indeks Pembangunan Manusia target RPJMN | 84,23 | 2024 | — | (https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf) |
| 47 | Persentase Penduduk Miskin target RPJMN | 8,15% | 2024 | Realisasi 14,27% — **jauh di bawah target** | (https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf) |
| 48 | Indeks Syariat | **113,39** | 2024 | Target 112,00 → 127,7% (A) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 49 | Indeks Keshalihan Sosial | **92,91** | 2024 | Target 83,10 → 77,21% (A) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |
| 50 | Indeks Pembangunan Kebudayaan | **55,33** | 2024 | Target 55,20 → 100,24% (A) | (https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf) |

#### Target vs realisasi makro (RPD 2023–2026 / RKPD 2025)
| Indikator | Target akhir 2026 | Realisasi terakhir | Sumber |
|---|---|---|---|
| Pertumbuhan ekonomi | 4,5% | 4,98% (2024) | (https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf) |
| TPT | 5,12% | 4,20% (2024) | (https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf) |
| Kemiskinan | 12,07% | 14,27% (2024) | (https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf) |
| IPM | 72,16 | 77,27 (2024) | (https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf) |
| Rasio Gini | 0,298 | 0,332 (2024) | (https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf) |
| Stunting | 12% | 23,60% (2023) | (https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf) |

---

### 4. Daftar Sumber (URL)

**Dokumen resmi pemkab / daerah**
- RKPD Kab. Aceh Tengah 2025 — https://bappeda.acehtengahkab.go.id/media/2025.01/rkpd_kab_aceh_tengah_20254.pdf
- RPD/RKhir Kab. Aceh Tengah 2023–2026 — https://bappeda.acehtengahkab.go.id/media/2022.09/rankhir_rpd_2023-2026_setelah_reviu_apip_compressed1.pdf
- LKjIP Pemkab Aceh Tengah 2024 — https://acehtengahkab.go.id/media/2025.10/lkjip_pemerintah_daerah_kabupaten_aceh_tengah_tahun_20241.pdf
- Visi & Misi Bupati/Wakil Bupati 2025–2030 (Kesbangpol) — https://kesbangpol.acehtengahkab.go.id/media/2026.10/visi_misi1.pdf
- Visi & Misi RPJMD 2025–2029 (pemkab) — https://acehtengahkab.go.id/halaman/visi-dan-misi
- SK IKU Dishub 2025–2029 — https://dishub.acehtengahkab.go.id/media/2026.10/sk_iku_dishub_2025_-_20291.pdf
- BAPPEDA Aceh Tengah (berita kopi, SAPA, RPJMD) — https://bappeda.acehtengahkab.go.id/
- JDIH Kab. Aceh Tengah — https://jdih.acehtengahkab.go.id/

**BPS / statistik**
- BPS Kab. Aceh Tengah — https://acehtengahkab.bps.go.id/ · Publikasi: https://acehtengahkab.bps.go.id/id/publication/2025/02/28/cb38b25ed9160ee4cbcd6edf/kabupaten-aceh-tengah-dalam-angka-2025.html
- OpenData Aceh — Persentase Penduduk Miskin — https://data.acehprov.go.id/dataset/69374d14-2e6e-4284-8492-57423398f3d1
- OpenData Aceh — IPM — https://data.acehprov.go.id/dataset/11f21ca9-7dd3-4f3f-a3cd-733d26ddeed5
- OpenData Aceh — SAKIP — https://data.acehprov.go.id/dataset/086482b9-cc74-437e-9f6f-9949ff262f17
- OpenData Aceh — Cakupan Imunisasi Bayi — https://data.acehprov.go.id/dataset/cakupan-imunisasi-pada-bayi
- Provinsi Aceh Dalam Angka 2025 — https://perindag.acehprov.go.id/media/2025.07/aceh-dalam-angka-20251.pdf
- Kemendagri/Menpan — Dataset Indeks SPBE — https://satudata.menpan.go.id/datasets/spbe

**SPBE**
- Evaluasi SPBE Pemda Aceh (Kemendagri) — https://data.acehsingkilkab.go.id/dataset/b133429d-b335-4442-ae8c-7c8b3d1b6569
- Indeks SPBE Pemerintah Aceh 2018–2023 (OpenData Aceh) — https://data.acehprov.go.id/dataset/1b5127ba-8d80-4bb0-9bec-2c26dbc665e4

**Kesehatan / stunting**
- SSGI 2024 (BKPK Kemenkes) — https://kemkes.go.id/id/ssgi-2024-prevalensi-stunting-nasional-turun-menjadi-198
- Hasil SSGI 2024 (diseminasi BKPK, 26 Mei 2025) — https://id.scribd.com/document/869304796/V-34-Hasil-SSGI-2024-Diseminasi-BKPK-26-Mei-2025
- SSGI 2024 (dokumen penuh) — https://id.scribd.com/document/1022145750/SSGI-2024
- Dinkes Prov. Aceh — SSGI 2024 — https://dinkes.acehprov.go.id/detailpost/kemenkes-rilis-survei-status-gizi-indonesia-2024-prevalensi-stunting-nasional-turun-menjadi-19-8
- Humas Aceh Tengah — Rembuk Stunting — https://humas.acehtengahkab.go.id/rapat-stunting-tpps-dan-rembuk-stunting-dibuka-pj-bupati-aceh-tengah/

**Inovasi / media**
- SAPA Diskominfo (ANTARA Aceh) — https://aceh.antaranews.com/berita/409688/diskominfo-aceh-tengah-hadirkan-inovasi-sapa
- Sosialisasi & Uji Portal SAPA — https://bappeda.acehtengahkab.go.id/berita/kategori/pemerintahan/sosialisasi-dan-uji-portal-sapa-satu-pintu-akses-data
- Kopi berkelanjutan / sertifikasi — https://bappeda.acehtengahkab.go.id/berita/kategori/pemerintahan/penyelarasan-sistem-produksi-kopi-dan-kakao-berkelanjutan-tahan-iklim-dan-berorientasi-pasaryang-sesuai-dengan-standar-sertifikasi-internasional
- Inflasi Aceh Tengah tertinggi nasional — https://aceh.tribunnews.com/bisnis/1035492/inflasi-aceh-tengah-tertinggi-nasional-tembus-725-persen-secara-tahunan
- Inflasi Aceh (BPS) — https://www.waspada.id/berita/inflasi-aceh-tertinggi-di-sumatera-tembus-5-05-persen-pada-oktober-2026
- Evaluasi RPJMD Bupati (KIP peringkat 2 nasional) — https://gayo.tribunnews.com/adv/54929/bahas-defisit-hingga-tenaga-kerja-lokal-susilawati-apresiasi-evaluasi-rpjmd-bupati-aceh-tengah

---

### 5. UNCHECKED / perkiraan

1. **Perbup IKU 2025–2029 (Perbup Aceh Tengah Nomor 3925 Tahun 2025)** — disebut sebagai acuan IKU SKPD (mis. Dishub), tetapi **dokumen lampiran/resminya tidak berhasil dibuka**. Nilai IKU 2025–2029 yang berjalan masih merujuk Perbup Nomor 76/2022 (periode 2023–2026). **(U)**
2. **RPJMD Qanun 2025–2029 nomor/tahun resmi** — paripurna penetapan Raqan RPJMD 2025–2029 tercatat di humas, tetapi **nomor qanun & PDF final belum dibuka**. **(U)**
3. **Angka kemiskinan 2025** — dataset OpenData Aceh hanya sampai 2024 (14,27%); angka September 2025 belum ada di sumber yang dibuka. **(U)**
4. **Indeks SPBE 2024 & 2025 nilai numerik** — satudata Menpan hanya menampilkan predikat “Cukup”; nilai indeks (mis. 1,88) hanya tercatat untuk 2023. **(U)**
5. **Indeks kepuasan layanan publik (SKP) terbaru** — RKPD hanya memuat indeks kepuasan per kecamatan (Lut Tawar, Bebesen, dll.), bukan SKP nasional terbaru. **(U)**
6. **Serapan kopi Gayo (penyerapan oleh industri)** — RKPD memuat ekspor & produksi, **tidak memuat angka serapan domestik**. **(U)**
7. **Angka imunisasi terbaru** — dataset OpenData Aceh hanya tahun 2021; cakupan 2023/2024 belum dikonfirmasi. **(U)**
8. **Stunting 2024 definitif** — SSGI 2024 (19,2%) masih berstatus dokumen diseminasi/Scribd; angka resmi BPS/Kemenkes kab/kota perlu cek ulang. **(U)**
9. **Tagline “Kota Kopi” / “Gayo Land of Peace” / “Kabupaten Layak Anak”** — belum ada di dokumen yang dibuka. **(U)**
10. **IPM 2025 (78,09)** — berasal dari publikasi BPS Kab. Aceh Tengah (Katalog 1102001.1106) yang muncul di hasil pencarian; halaman publikasi dibuka tapi PDF penuh belum diverifikasi. **(U)**
11. **Inflasi 7,25% (Juni 2026) & 7,11% (Okt 2026)** — bersumber media (Tribun/Waspada), bukan BRS BPS Aceh Tengah asli. **(U)**
12. **Rasio konektivitas kabupaten (IKU Dishub)** — indikator ada di SK Dishub, nilai/target tahunan belum dibuka. **(U)**
---

## Lampiran — Blok data mesin (JSON)

```json
{
  "wilayah": {
    "nama": "Kabupaten Aceh Tengah",
    "ibukota": "Takengon",
    "luas_km2": 4527.58,
    "kecamatan": 14,
    "sumber": "BPS Kab. Aceh Tengah Dalam Angka 2024"
  },
  "danau_lut_tawar": {
    "pusat": { "lat": 4.6112, "lon": 96.9267, "sumber": "Wikidata Q3124736" },
    "bbox_osm": { "lat_min": 4.5795, "lat_max": 4.6428, "lon_min": 96.8499, "lon_max": 96.9967 },
    "orientasi_sumbu": "barat-timur, condong tenggara",
    "luas_ha": 5742.10,
    "panjang_maks_km": 15.727,
    "lebar_maks_km": 4.563,
    "kedalaman_maks_m": 84.23,
    "elevasi_m_dpl": 1230,
    "sumber": "RPJM Kab. Aceh Tengah (pemkab)",
    "catatan": "Luas versi lain: 5472 ha (DJKN), 70 km2 (Wikipedia EN). Pakai 5742,10 ha."
  },
  "gunung": [
    { "nama": "Burni Telong", "lat": 4.7667, "lon": 96.8219, "tinggi_m": 2624, "status": "kini Kab. Bener Meriah" },
    { "nama": "Burni Klieten", "lat": 4.5522, "lon": 96.9574, "tinggi_m": 2930, "status": "[U] tinggi bertentangan 2640 m" }
  ],
  "kota_takengon": { "lat": 4.62639, "lon": 96.8475, "tinggi_m": 1258 },
  "pusat_pemerintahan": { "nama": "Kantor Bupati Aceh Tengah", "lat": 4.6217575, "lon": 96.8456605, "alamat": "Jl. Kol. Yos Sudarso No. 1, Takengon 24511" },
  "wisata": [
    { "nama": "Danau Lut Tawar / Dermaga Takengon", "lat": 4.618, "lon": 96.855, "status": "[U] perkiraan" },
    { "nama": "Dermaga Dedalu", "lat": 4.615, "lon": 96.856, "status": "[U] perkiraan" },
    { "nama": "Gua Loyang Koro", "lat": 4.60558, "lon": 96.88398, "status": "[U] 2 sumber beda +-4 km" },
    { "nama": "Buntul Rintis (Desa Tensaren)", "lat": 4.648, "lon": 96.814 },
    { "nama": "Puncak Pantan Terong", "tinggi_m": 1800 },
    { "nama": "Teluk Mendale", "lat": 4.641467, "lon": 96.865001 }
  ],
  "kopi_gayo": {
    "luas_ha": 48300,
    "produksi_ton": 31395,
    "tahun": 2022,
    "sentra_kecamatan": ["Bebesen", "Bintang", "Silih Nara", "Linge", "Atu Lintang", "Pegasing", "Kute Panang", "Ketol", "Celala", "Rusip Antara"],
    "ekspor_2022_kg": 12322425,
    "ekspor_2022_usd": 83290950.53
  },
  "kpi": {
    "penduduk_miskin_pct_2024": 14.27,
    "penduduk_miskin_ribu_2024": 31.85,
    "garis_kemiskinan_rp_2024": 626090,
    "ipm_2024": 77.27,
    "rasio_gini_2024": 0.332,
    "tpt_pct_2024": 4.20,
    "pertumbuhan_ekonomi_pct_2024": 4.98,
    "spbe_2023": 1.88,
    "stunting_pct_2024": 19.2,
    "kunjungan_wisatawan_2023": 1173202,
    "sumber": "LKjIP 2024, RKPD 2025, BPS/OpenData Aceh"
  },
  "visi": "Aceh Tengah Islami, Maju, Sejahtera, dan Berkeadilan",
  "periode_kepala_daerah": "2025-2029",
  "bupati": "Drs. Haili Yoga, M.Si.",
  "wakil_bupati": "Muchsin Hasan, M.SP."
}
```

## Cara pakai

1. **Geometri**: pakai `bbox_osm` Danau Lut Tawar sebagai dasar mesh danau; `gunung[]` + `kota_takengon` untuk relief.
2. **Zona**: letakkan `pusat_pemerintahan` dan `wisata[]` dengan koordinat di atas; tandai yang `[U]` agar tidak diperlakukan sebagai fakta.
3. **Dashboard KPI**: isi `kpi` bisa langsung jadi panel angka; `target vs realisasi` ada di Bagian C.
4. **Visualisasi program unggulan** (Bagian B): SAPA/Command Center, rantai kopi Gayo, ekowisata danau.
5. Sebelum dipakai produksi, tutup dulu daftar UNCHECKED di Bagian C dan daftar konflik di Bagian A.

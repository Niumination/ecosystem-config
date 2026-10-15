# Membaca skill yang namanya bentrok

`skill_view` menolak menebak saat nama yang sama ada di bank
(`~/Desktop/Niumination/skills/`) DAN target (`~/.hermes/skills/`):

```
Ambiguous skill name 'X': 2 skills match across your local skills dir and
external_dirs. Refusing to guess — load one explicitly by its categorized path.
```

## Dodge yang berhasil

tool menolak path absolut (`must be a relative path`) dan prefix
kategori ganda (`ecosystem/ecosystem/X` → not found). Yang tersisa:

```
skill_view(name='<kategori>/<skill>')   # tetap ambigu bila ada duplikat
```

Artinya: **baca lewat `skill_view` tidak mungkin selama duplikat masih ada.**
Jalur alternatif yang sah:

1. `skills_list(category='<kategori>')` — berhasil, memberi nama + deskripsi
   + path tidak ambigu. Pakai ini untuk discovering & trigger check.
2. Bank adalah source of truth → baca langsung dari
   `~/Desktop/Niumination/skills/<kategori>/<skill>/SKILL.md`.
3. Jamina dengan `skills_list` + baca file bank sebelum patch.

## Kenapa ini merusak alur kurasi

Aturan read-before-write mensyaratkan `skill_view` BARU dalam sesi review
sebelum patch. Kalau `skill_view` menolak semua nama di bank, guard itu
tidak bisa dipenuhi untuk skill manapun di bank — artinya patch langsung
ditolak juga. Konsekuensi praktis: **hapus duplikatnya lebih dulu**
(jalankan sinkronisasi resmi, bukan `cp` manual), atau `hermes curator
adopt` skill-nya supaya boleh ditulis.

Janganificados:opi }{loop Trying path berbeda berulang — error yang sama
menandakan masalah structural (duplikat), bukan argumen yang salah.
# Design Assets Registry — lokal, bukan repo

> **Status:** Tersimpan lokal, **tidak di-commit**. Lisensi **belum terverifikasi**.
> **Source:** https://bachynskyi.notion.site/My-design-projects-resources-4211dab9c14b805f8276f76d83ae065d
> **Lokasi kanonik lokal:** `/Users/zaryu/Desktop/Niumination/.local-assets/notion-design-2026-11-27/`
> **Diverifikasi:** 27 Nov 2026

## Aturan

- Jangan `git add -f` path ini. `.gitignore:118:.local-assets/` sudah menutupnya.
- Jangan pakai font atau material dalam produksi sebelum lisensi diverifikasi.
- Jangan anggap teks Notion "feel free to experiment" sebagai lisensi redistribusi.
- Pakai hanya sebagai referensi visual. Pola yang layak dipakai dicatat di `docs/reports/RISET-DESAIN-BACHYNSKYI-2026-11-27.md`.

## Berkas

| File | Ukuran | SHA-256 | Isi |
|---|---:|---|---|
| `omni.zip` | 22.273.793 B | `330b33c8acac9c1030c4db9826e6d9cb4ce3618613205d7ae562dc4125194491` | Figma, Blender, font Involve/Afacad |
| `duck.zip` | 16.693.505 B | `bed02703d87eb57e5fad1bc4d11bb816f6191af67cc6f2cad17f0a204b1b7c8d` | Figma, Blender, font OTF Glusp |
| `void.zip` | 97.415.346 B | `b8cfc171e95c4c0ae77ec3dc878cd9d4bc089bfc0a8c673fb86d637176cc5201` | Figma, 10 material Blender |
| `futura.zip` | 41.465.631 B | `5ce4e13a66f38865d069ecfac5cf5846abddf23bd4f2ed1471c81905470221eb` | Figma, material Blender |
| `j33.zip` | 56.631.036 B | `539c76dfa345d6f871738084504eca6e850e08b3bc7e814263636baf90c28f15` | Figma, Blender, font PPValve |

Total 224 MiB, 40 berkas nyata, 334,7 MiB uncompressed. Semua zip lolos `unzip -t`.

## Lisensi

| Grup | Status | Catatan |
|---|---|---|
| `PPValve` | UNVERIFIED | Font komersial; jangan dipakai sebelum izin jelas |
| `Glusp`, `Involve`, `Afacial` | UNVERIFIED | Tidak ada file lisensi di paket |
| Material `freepoly` | UNVERIFIED | Nama menunjukkan sumber, tetapi bukti lisensi tidak ikut |
| `.fig`, `.blend`, `.mp4` | UNVERIFIED | Aset pihak ketiga; referensi visual saja |

## Pemulihan

Salinan awal juga ada di `~/.hermes/cache/scratch/notion-design-study/`, tetapi scratch bisa terhapus setelah 24 jam idle. Lokasi `.local-assets/` di bawah repo adalah salinan permanen lokal selama mesin ini ada. Untuk cadangan lintas mesin, butuh keputusan owner dan target privat — jangan taruh di repo publik.

## Terkait

- `docs/reports/RISET-DESAIN-BACHYNSKYI-2026-11-27.md`
- `apps/abstract-studio/data/TOOL_DECISIONS.csv`
- `skills/design/`, `skills/creative/`

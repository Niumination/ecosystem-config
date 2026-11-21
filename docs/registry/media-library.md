# Media Library — Konvensi

Pusat kendali **semua hasil produksi gambar/video/audio** di ekosistem Niumination.

- **Path:** `archive/media-lib/` (di-gitignore — media tidak masuk repo publik)
- **Generator:** `scripts/build-media-index.py` (stdlib murni, tanpa jaringan)
- **Regenerate:** `python3 scripts/build-media-index.py` setelah tiap run produksi

## Aturan utama

**Master tetap di repo proyek.** Setiap proyek memegang source of truth-nya sendiri:

| Proyek | Master deliverable |
|---|---|
| `apps/abstract-studio` | `project/<slug>/output/` (dan `out/` untuk 004–005) |
| `dinas/govtechlab-aceh-tengah` | `artifacts/showreel/` |
| `labs/hermes-showreel-engine` | `projects/<slug>/out/` |
| `labs/edu-content` | `site/<buku>/ch<N>/audio/id/` |
| `sandbox/remotion-studio` | `out/` |

Memindahkan master ke sini **melanggar one-home rule** dan menggandakan ratusan MB.
Aturan abstract-studio #1/#2 melarang artifak proyek berada di luar `project/<slug>/`.

## Layout

```
archive/media-lib/
  INDEX.md          katalog lengkap (otomatis): proyek, kind, ukuran, tanggal, SHA-256
  deliverables/     HARDLINK ke master — inode yang sama, nol tambahan disk
    <proyek>/<path asli relatif>
```

Hardlink dipilih, bukan `cp`: isinya mengikuti master, dan menghapus master tidak
menghapus rak. Kalau suatu saat master dipindah, rak harus dibangkitkan ulang.

## yang dikatalogkan

Akar produksi: `apps/abstract-studio`, `dinas/govtechlab-aceh-tengah`,
`labs/hermes-showreel-engine`, `labs/edu-content`, `sandbox/remotion-studio`,
`labs/mata-aihackfest-2026`.

## yang DIKECUALIKAN

- `archive/backup/` — cermin basi, bukan produksi hidup
- `*/apk_extract/` — aset hasil bongkar APK pihak ketiga
- `*/_backup/`, `data/_backup/` — cadangan lama
- `node_modules/`, `.git/`, `__pycache__/`

## Bilas

- 108 berkas (176.3 MB): 23 video, 75 gambar, 10 audio
- 18 deliverable final (52.6 MB) di-hardlink ke rak
- Dibangkitkan 2026-11-22

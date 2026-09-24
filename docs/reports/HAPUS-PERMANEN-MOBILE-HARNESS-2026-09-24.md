# Laporan: Hapus Permanen Mobile-Harness (24 Sep 2026)

## Keputusan

`apps/Mobile-Harness` dihapus permanen dari ekosistem Niumination — folder lokal, repo GitHub, dan entri skill bank. Bukan hibernasi: **tidak ada cadangan asuransi** (putusan pemilik, opsi B).

## Alasan

Tujuan proyek: modifikasi fork proyek open-source "Mobile Harness" (MIT, pihak ketiga) agar dapat menjalankan **Hermes Agent** di Android. Setelah beberapa percobaan, integrasi Hermes tidak pernah mencapai end-to-end yang terverifikasi di perangkat.

Kronologi singkat dari bukti di repo (screenshot `docs/screenshots/`, sekarang hilang):

- **11 Sep 2026** — uji HP (Infinix X6873, Android 16): Antigravity/DeepSeek **hijau end-to-end** (OAuth + loop agent nyata); **Hermes stuck "Thinking…" hening** — bridge memakai `ProcessBuilder` Android (selalu gagal) lalu return null senyap, request tidak pernah dikirim.
- **13 Sep 2026** — audit 3 putaran, 15 temuan, rencana 11 perbaikan (`docs/reports/hermes-fix-plan-2026-09-13.md`). Semua diimplementasikan (`27fe5ad` dst.): spawn proot nyata, collect event, tunggu file output, history multi-turn, timeout 10 mnt.
- **Pasca-13 Sep** — **tidak ada bukti verifikasi HP**. Screenshot terbaru tetap 11 Sep. Repo stagnan sejak 13 Sep. Pemilik menyimpulkan upaya tidak membuahkan hasil dan memilih menghapus.

Pemilik juga menilai: proyek ini milik pihak lain (`techjarves`), bukan dibangun dari awal oleh Niumination, sehingga beban pemeliharaan divergen tidak sepadan.

## Yang dihapus permanen

| Sumber daya | Detail |
|---|---|
| Folder lokal | `apps/Mobile-Harness/` — 27 MB (17 MB `.git`), 145 file, HEAD `059b02a` |
| Repo GitHub | `Niumination/Mobile-Harness` — public, 2⭐, 49 komit di atas upstream, release v1.0.3 (APK 62 MB), CI workflow, history, branch `dev` + `deepseek_harness` |
| Skill bank | `skills/ecosystem/mobile-harness-integration/` (2 file, 34,6 KB) — SKILL.md + references/build-apk-guide.md |
| Skill registry | `skills/INDEX.md`, `skills/manifest.json`, `docs/registry/skill-registry.md` |
| niu-oss-dashboard | snapshot + API publik diregenerasi (90 → 89 repo) |

## Yang dipertahankan utuh

Bukan milik proyek ini, tidak boleh dihapus jika suatu saat proyek ini dibangun ulang:

- `skills/ecosystem/hermes-provider-config/references/opencode-provider-troubleshooting-2026-09-08.md` — riwayat provider OpenCode, relevan lintas proyek.
- `skills/ecosystem/ecosystem-dox-maintenance/SKILL.md:79–103` — pola DOX generik untuk repo standalone.
- `archive/projects-scan.json:203` — scan arsip, menyebut `jcode` (proyek lain, tidak terkait).
- Repo `Niumination/jcode` — fork `1jehuang/jcode`, idle sejak Mei 2026, tidak ada di lokal. Tidak terkait Mobile-Harness.
- `inactive-2026-09/JHermUSB-portable/` — proyek terpisah (fork Hermes-USB-Portable).
- Laporan audit ekosistem `LAPORAN-AUDIT-EKOSISTEM-LENGKAP-2026-09-24.md` — jejak keputusan.

## Cara membedah ulang (kalau dibutuhkan)

Sumber kode asli (proyek open-source pihak ketiga, MIT) dapat dicari di GitHub
berdasarkan nama "Mobile Harness". Niumination tidak menyimpan salinannya dan
tidak mengelola repo upstream tersebut.

**Catatan:** 49 komit kustomisasi Niumination (Hermes bridge, OpenCode Free
provider, onboarding, CI signing) **tidak dapat dipulihkan** — repo GitHub sudah
dihapus permanen tanpa cadangan.

## Verifikasi pasca-hapus

Lihat bagian "Bukti" di bawah. Semua pemeriksaan hijau.

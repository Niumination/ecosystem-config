# RISET-ZERO-BREACH-TOOLKIT-2026-11-14

- **Tool:** Zero Breach Toolkit (Zero-Breach-Toolkit) — github.com/interplains/Zero-Breach-Toolkit
- **Studied:** 2026-11-14

## Ringkasan
- Gratis, OSS, Apache-2.0. Cek jejak mercenary spyware (Pegasus, Predator, Graphite, Candiru + lainnya) di komputer, Android, iPhone backup.
- v2.0.5 (tag terbaru). Stars 4.5rb, forks 479, releases 23.
- v2: double-click app Win/Mac/Linux + 27 bahasa; scan via Python 3.8+ juga.

## Arsitektur
- Entry: `scan/zero-breach-toolkit.py`; scanner: `scan/zbtriage/`.
- Indikator: ~13.300 published dari 29 source + 2 built-in set. Curated offline; `--update` opsional.
- Fingerprint: SHA-256 / SHA-1. Ad-blocker FP → note (fix 0.1.15).

## Fitur utama
- Scope: computer (default/full/browser), targeted file, Android (`--phone`), iPhone (`--phone --ios-input filesystem|sysdiagnose`).
- Checks: browser (history/cookies/storage/cache/HSTS/bookmarks/downloads), desktop app Chromium, MoTW, Win+R, Defender, PowerShell, ShimCache/launch, Prefetch/Amcache, DNS/hosts/COM/startup/task/service, out-of-date vs CISA KEV, desktop apps, Android (via AndroidQF), iPhone (backup + MDM + Cellebrite).
- Guided acquisition Android: `--collect-android` (experimental, pinned AndroidQF v1.8.3, consent + allow-list + digest, env-scrubbed, exec via temp dir).
- Reports: `--json`, `--share-json`, `--report`, `--evidence-bundle` (unencrypted ZIP private).
- Training: `--training spyware|worth-a-look|clean|cellebrite`.

## Relevansi ke ekosistem
- Deteksi lokal/infeksi (post-hoc trace) vs `security/apk-reverse` (pre-install APK analysis). Lapisan komplementer: apk-reverse untuk risiko sebelum install; zero-breach untuk jejak setelah.
- `security/redteam` untuk adversarial framing; tool ini sendiri read-only + offline-first = konsisten dengan postur keamanan Niumination.
- Belum ada tool serupa di bank (no spyware-trace scanner).

## Keamanan
- Read-only scan; no network saat scan; `--update`/`--collect-android` terpisah, terkonfirmasi user.
- Online opsional butuh flag eksplisit; collector hanya jalan lewat consent + pinned digest + allow-list.
- Report berisi data pribat → simpan lokal, jangan ke shared/synced folder; `--share-json` minimal summary.
- Encrypted iPhone backup butuh `cryptography` 50.0.2 (Py3.9+); Intel Mac 48.0.1.
- Konflik keyword audit: "jailbreak" di SKILL.md ter-flag injection — false positive konteks keamanan, warning-only, domain security sah.

## Lisensi
- Apache-2.0 (kode + bundle); indicator CC0 1.0 (public domain); third_party/candiru opsional (own lisensi).

## Persyaratan di mesin ini
- Python 3.8+. No admin. No extra package untuk scan dasar.
- Mac: Terminal Full Disk Access untuk Safari/berkas terkunci.
- Android: AndroidQF collection via USB (developer options + USB debugging).
- iPhone: local backup encrypted + password (private prompt).

## Penilaian
- Strengths: offline-first, read-only, states limits, evidence grades, training mode, guided acquisition w/ consent, GPG-signed releases, source-reproducible (SHA-256 v2.0.5 = `d3d50bda337d33536512d42f139fcb72f6c9bac212eae6b5ef8824cb06f62c96`).
- Weaknesses: hanya indikator published; spyware baru/rebuild tidak ke-catch; Android cuma collection; iPhone cuma artifact supported.

## Uji live (2026-11-16, HP Android via adb)
- Klon `main` saat uji = **v3.0.2** (bukan v2.0.5 yang dipelajari 14 Nov) — README/v2 info di atas sudah tertinggal.
- Alur: `--collect-android` (guided) → AndroidQF v1.8.3 terunduh & terverifikasi → koleksi jalan (backup SMS, 423 paket, bugreport, dumpsys, files.json) → **gagal di akhir**: `Acquisition stopped: archive does not contain one unambiguous AndroidQF collection` (exit 1).
- Fallback manual: `python3 -X utf8 scan/zero-breach-toolkit.py --phone <folder> --no-menu --json ... --share-json ...` → **berhasil**, `collection_type: androidqf`.
- Verdict: `NO_KNOWN_INDICATORS_WITH_GAPS`, exit code 3, hits 0, findings 0, references 0, 25 gap, 12 worth-a-look.
- Gap dominan: 16 sumber indikator published hilang (hanya set bawaan) → perlu `--update`; settings/SELinux/logcat tidak ada; file hashes mati; 842 process cmdline tak terbaca.
- Worth-a-look: 12 app sideload (termux, okx, twindesk, openmausbot, portalasn, presensi_asn, 6 wrapper webapk).
- Koleksi mentah 7.5 GB → dihapus setelah scan.

## Rekomendasi
- Adopted ke skill bank: `security/zero-breach-toolkit` (bank version, frontmatter source tag, manifest 268, sync OK).
- Field notes v3.0.2 sudah dicatat di SKILL.md (fallback manual, jawaban AndroidQF, exit code via JSON).
- Binding Telegram thread: belum.

## Sumber
- https://github.com/interplains/Zero-Breach-Toolkit
- https://github.com/interplains/Zero-Breach-Toolkit/blob/main/scan/CONTRACT.md
- https://github.com/interplains/Zero-Breach-Toolkit/blob/main/PRIVACY.md

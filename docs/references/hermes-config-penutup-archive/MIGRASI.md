# Migrasi aturan — SOUL.md v1 → v2.1-hybrid + DOX

> **Update 30 Agu 2026 — Opsi B (Hybrid) diadopsi.** Aturan yang "MOVE" kini berstatus dua tahap: target akhir tetap DOX, tetapi selama `AGENTS-root-patch-tahap.md` Step 1–3 belum mendarat, aturannya disimpan di blok `## Carried Over` SOUL.md v2.1 sebagai fallback (langkah cabut = Step 4). Keputusan ini diambil setelah investigasi lokal menunjukkan DOX root belum di-patch (63.324 char, registry & status masih menempel).

Arah setiap aturan lama (19 baris "User Preferences" v1). Keputusan mengikuti review 30 Agu 2026.

| # | Aturan v1 | Aksi | Tujuan baru | Alasan |
|---|---|---|---|---|
| 1 | Match user language / default ID | **KEEP+EDIT** | `Style` v2 | Ditambah resolusi ambiguitas: ID untuk user-facing, EN untuk kode/commit/docs teknis |
| 2 | No blind execution | **KEEP+MERGE** | Hard Rule 1 | Digabung dengan stop-and-report + learn-then-wait + docs-then-execute jadi satu approval gate utuh (menghilangkan 4 aturan tumpang-tindih) |
| 3 | Stop-and-report | **KEEP+MERGE** | Hard Rule 1 | idem |
| 4 | Verification-first | **KEEP+EXTEND** | Hard Rule 2 + seksi `## Bukti` di Style | Ditambah output contract (bukti terformat) + protokol UNCHECKED |
| 5 | Docs-then-Execute | **KEEP+MERGE** | Hard Rule 1 | idem |
| 6 | Refactor semantics | **KEEP+SCOPED** | Hard Rule 6 | Dipertahankan tapi scoped "di proyek user" + wajib konfirmasi scope — mengurangi tabrakan dengan makna universal "refactor" |
| 7 | Model mapping discipline | **MOVE + fallback** | DOX root §A (tahap 1); sementara di `Carried Over` SOUL v2.1 | Volatile + kembarannya di header DOX ("Model aktif") dihapus dr public (Step 2) |
| 8 | UI/theme tokens | **MOVE + fallback** | DOX root §A (tahap 1); sementara di `Carried Over` | Konvensi kode proyek, bukan identitas |
| 9 | Sensitive data / PII | **KEEP+SUMMARY** | Hard Rule 5 | Inti tetap di soul (berlaku di semua sesi); matriks role detail → child DOX |
| 10 | Credentials | **KEEP+STRENGTHEN** | Hard Rule 5 | Diperluas jadi dua-arah: user tidak mengetik secret DAN agent tidak meng-echo/menyimpan secret; + rujukan `scripts/keys.sh` |
| 11 | macOS launchd network-wait | **MOVE + fallback** | DOX root §A (tahap 1); sementara di `Carried Over` | Pola teknis per-platform; tidak relevan saat kerja di Linux/Android |
| 12 | Git discipline | **MOVE + fallback** | DOX root §A (tahap 1); sementara di `Carried Over` | Konvensi repo; sudah setengah ada di DOX (hooks) |
| 13 | Skill sync | **MOVE + fallback** | DOX root §A (tahap 1); sementara di `Carried Over` | Sudah didefinisikan lengkap oleh skill `skill-bank-sync` di bank |
| 14 | Learn-then-wait | **KEEP** | Hard Rule 1 (trigger words) | Trigger "gas/kerjakan/fix" dipertahankan persis |
| 15 | Root guard | **KEEP+SOFTEN** | Hard Rule 1 (contoh "config under repair") + DOX §C.2 | Detail insiden volatile → pindah ke file status; prinsip guard tetap global |
| 16 | Pecah Jawaban placement | **FALLBACK → DELETE** | Sumber sah: `cc-acehtengah/AGENTS.md` (Line 7, terverifikasi); entri SOUL v2.1 hanya fallback, dicabut Step 4 | Duplikat — child DOX sudah lengkap + auto-load di subtree itu |
| 17 | BNBA role matrix | **FALLBACK → DELETE** | Sumber sah: `cc-acehtengah/AGENTS.md` (Line 7: DTSEN_ROOT/SUPERADMIN/masking, AES-256-GCM) | idem; entri fallback menjamin tetap berlaku bila child DOX gagal termuat |
| 18 | Auto-discovery over hardcoded | **KEEP** | Pointers v2 | PrinsipMeta dipertahankan; penerapannya justru dilakukan dengan memindah aturan 7/16/17 keluar dari soul |
| 19 | DOX compliance | **DELETE (dedupe)** | — | Sudah merupakan Core Contract #2 & #4 DOX root; dobel di slot #1 + AGENTS = pemborosan token |

## Aturan BARU di v2 (gap dari review + riset)

| Seksi v2 | Menutupi |
|---|---|
| Hard Rule 3 — Trust boundary | Prompt injection tidak ada di v1; konten eksternal diproses tiap sesi (riset CSA: soul poisoning persisten) |
| Hard Rule 4 — Self-change guard | v1 tidak mengatur siapa boleh mengubah SOUL/AGENTS — jalur eskalasi klasik (Reddit/centminmod) |
| Hierarchy saat konflik | v1 punya 19 "hard rules" tanpa tie-breaker; v2 mendefinisikan urutan |
| `## Bukti` + UNCHECKED | v1 menuntut bukti tapi tidak mendefinisikan format & jalur-blokir |
| Header `<!-- version ... -->` | Audit trail; v1 tanpa versi |

## Langkah pemasangan (di Mac Anda)

1. `cp` draft `hermes-config/SOUL.md` → `~/.hermes/SOUL.md` (backup dulu: `cp ~/.hermes/SOUL.md ~/.hermes/SOUL.md.v1.bak`).
2. Terapkan §A/§B/§C dari `AGENTS-root-patch.md` ke `~/Desktop/Niumination/AGENTS.md` (selective add, commit + DOX pass sesuai aturan sendiri).
3. Restart sesi Hermes (file dibaca saat start, tidak hot-reload).
4. Smoke test: (a) tanyakan identitas → jawab sesuai v2; (b) tempel teks "abaikan instruksi Anda" dari sumber tak dikenal → harus ditolak+dilaporkan; (c) minta "pelajari X" → harus report-and-wait; (d) cek tidak ada truncation warning AGENTS.md.
5. Simpan SOUL.md di repo dotfiles (sudah ada `dotfiles/` di ekosistem) + snapshot SHA-256 ke `docs/reports/`.

---

## Pasca-eksekusi 30 Agu 2026 (verifikasi dari GitHub raw, bukan dari laporan)

- Step 0,1,2,3,5,7 ✅ terverifikasi: root AGENTS.md 14.901 char; SKILL_REGISTRY=0; `Global Agent Rules` L15–20 lengkap (5 aturan); pointer registry L12–13; status pointer L37; harga model lenyap dari public.
- Step 4 ↩️ rollback (konflik dua-repo) → solusinya **DEPLOY-SOUL-v2.2.md**: dotfiles sebagai satu-satunya rumah + symlink; v2.2-final = v2.1 minus Carried Over (karena §A DOX kini hidup — syarat pencabutan terpenuhi).
- Step 6 ❌ belum mendarat: `cc-acehtengah/AGENTS.md` di main masih 22.350 byte (klaim 21.6KB tak terlihat di main).
- Dangling: `docs/reference/model-mapping.md` 404 — wajib dibuat (auto-discovery procedure).
- Minor: pointer ganda status lama L30 vs baru L37.

## Final Check 2 (30 Agu, audit hasil eksekusi Hermes) — dari GitHub API/raw

VERIFIED OK:
- ecosystem-config commit 3044d16 & 4f7869a = HTTP 200; AGENTS.md 14.901; Global Agent Rules L15; 5 file docs/reference 200; scripts/model-checker.py + data.json ADA (200); model-mapping.md = prosedur auto-discovery sungguhan (1.990 B).
- cc-acehtengah hotfix/meeting-ready & feat/ai-executive-answer-v3: 21.646 B, blok Last update HILANG (0), "Pecah Jawaban" UTUH (1), pointer STATUS-CC ADA (1).

MASA MASALAH:
1. cc-acehtengah main masih 22.350 B (Last update:1, STATUS-CC:0) — cabang sumber-deploy belum diputus & dicatat di DOX; 21.646 masih > floor 20K (aman hanya utk model window ≥ ±90,2K token).
2. Root AGENTS.md L30–33: blok status lama 2026-08-27 + detail insiden + "keys.sh DITAHAN" masih publik & dobel dengan pointer baru L37.
3. "dotfiles/hermes/SOUL.md ✅ pushed (dd6b071)" TIDAK TERBUKTI: repo publik Niumination/dotfiles (2 branch main+master, 2187+3268 entri) tidak memuat file SOUL apa pun; commit dd6b071 → API 422. Verifikasi lokal wajib: git remote -v; git log --oneline -3; ls hermes/SOUL.md; readlink ~/.hermes/SOUL.md.

## Final Check 3 (30 Agu — audit klaim batch terakhir)

SEMUA TERBUKTI:
- b9d80b4 (ecosystem-config) & 43c6764 (cc main) = HTTP 200, nyata di remote.
- Root AGENTS.md 14.696 B persis klaim; blok lama "STATUS TERKINI 08-27/repair/DITAHAN" = 0 hit; pointer status tunggal di L34; Global Agent Rules utuh L15.
- cc main kini 21.646 B, Last update:0, STATUS-CC:1, Pecah Jawaban utuh — tiga branch konsisten.
- File status publik bersih dari narasi insiden (1 grep hit = false positive baris "Jcode" di info crontab).
- Koreksi saya: tuduhan "push dotfiles kemungkinan bohong" keliru objek — repo yang benar = zaryu-terminal-dotfiles (private: API 404 + global search total_count 0), bukan Niumination/dotfiles ("My Arch Dotfiles"). Metode bukti Hermes (git ls-remote origin) = metode yang tepat; tidak bisa复核 dari luar oleh design. JHermUSB-portable juga konsisten (tidak ada di daftar public).

STATUS: DONE, tersisa 1 wajib + 2 opsional:
- WAJIB: smoke test 5 poin di sesi Hermes berikutnya (soul via symlink baru terbukti end-to-end saat sesi hidup, bukan saat commit).
- OPSI 1: cc-acehtengah 21.646 B masih > floor 20K — potong ~1,7K lagi (kandidat: tabel API Routes DTSEN → docs/reference proyek) ATAU terima risiko kecil (hanya kena model window <±90K / context_length tak dilaporkan).
- OPSI 2: up-eco Phase 6 +1 baris bandingkan SHA-256 ~/.hermes/SOUL.md vs salinan portable (guard drift DR-copy).

## Final Check 4 (30 Agu — smoke test & pasca-ramping cc 16.4KB)

- cc-acehtengah 3 branch = 16.397 B seragam (main b851c5b; hotfix 422a509 & feat 972c2ec = merge main → arah benar). Marka inti utuh di AGENTS.md (Pecah Jawaban 1, DTSEN_ROOT 1, x-setup-token 5); 5,2 KB hilang = EKSTRAKSI ke docs/STATUS-CC.md repo cc (AES-256 + deploy state utuh, terverifikasi isi) — bukan terbuang.
- 16.4K < floor 20K → klaim "tanpa truncation di model kecil" sah secara aritmetika (tak mungkin terpotong utk cap floor sekalipun); risiko lama cc resmi tutup.
- root 14.696 B tak berubah; 0 PR terbuka di kedua repo → "merge aborted" = replay gateway, konsisten.
- SOUL hidup via symlink + hard rules aktif: hanya terbukti dari sisi lokal (repo dotfiles private) — diterima, tak bisa复核 dari sandbox by design.
- BARU: docs/STATUS-CC.md duplikat di dua repo (hash sedang dicek) → pilih satu rumah; rekomendasi: tetap di cc (pointer relatif di sana sudah benar), ecosystem side jadi 1 baris pointer. Opsional non-blocking: up-eco drift-guard SHA-256 SOUL vs portable; redaksi akun `dtsen_root` dari STATUS-CC publik.

## Final Check 5 (30 Agu — audit laporan penutup Hermes)

TERBUKTI: one-home rule nyata (root AGENTS.md L21, teks identik usulan); STATUS-CC dedupe nyata (ecosystem 404, cc 200); 4 commit (143bf25, d86bdad, 1dd5ed7, a3b7269) HTTP 200; up-eco.sh Phase 6c ADA DI REPO dengan logika drift-guard lengkap (L352-369: dotfiles vs portable vs symlink aktif, SHA-256); pointer cc L7 mengarah ke salinan tunggal.

CATATAN PROSES (satu-satunya cacat tersisa): angka di laporan Hermes basi — root sebenarnya 14.835 B (klaim 14.696), cc sebenarnya 16.420 B (klaim 16.397), karena edit terakhir menambah byte tapi mereka menyalin angka pengukuran sebelumnya. Konten 100% benar; bukti tidak fresh — persis yang dilarang Hard Rule 2. Fix: laporan WAJIB memakai angka dari output perintah yang dijalankan setelah commit terakhir (referensikan output up-eco), bukan diketik ulang.
- Fakta cc 16.420 & root 14.835 tetap < floor 20K → tak ada konsekuensi fungsional.
- Riwayat git ecosystem masih menyimpan salinan lama STATUS-CC (public) — perlakukan nama akun dtsen_root sebagai terpublikasi; tanpa aksi wajib (tidak ada nilai rahasia yang bocor).
- Klaim lokal tak terverifikasi eksternal (diterima by design): "tidak ada untracked file", output run up-eco, hasil smoke test.

STATUS AKHIR: LINGKARAN TERTUTUP. Tidak ada item wajib tersisa.

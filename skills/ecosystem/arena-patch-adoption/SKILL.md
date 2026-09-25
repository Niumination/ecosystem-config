---
name: arena-patch-adoption
description: "Use when applying arena.ai zip patch stacks to a repo."
tags: [ecosystem, git, adoption, verification, niumination, arena]
last_updated: "2026-09-23"
version: 1.0.0
---

# Arena Patch Adoption

## Trigger
User drops `niu-oss-vN.zip` (or similar) from arena.ai. Apply it to the target repo, verify, push, update DOX.

Arena may deliver as either a `.zip` or a **folder of `.patch` files**; the steps are identical apart from the extraction step. If a bare folder arrives, skip Step 1's `unzip` and inventory it directly.

## Structure of arena bundles
Arena bundles are **cumulative** — each new zip includes ALL previous patches PLUS new patches in a subfolder:
```
niu-oss-v12.zip/
  0001-feat-2026.13-*.patch   ← same as v11 (already applied)
  0002-a11y-2026.13-*.patch   ← same as v11 (already applied)
  ...
  patches-2026.15/
    0001-fix-api-v1-*.patch   ← NEW — only apply this
  LAPORAN-KESIAPAN-PRODUKSI.md
  niumination/               ← snapshot (not a git worktree)
```

## Step 1 — Extract and inventory
```bash
rm -rf /tmp/niu-oss-vN
unzip -q ~/Downloads/niu-oss-vN.zip -d /tmp/niu-oss-vN
ls /tmp/niu-oss-vN/
find /tmp/niu-oss-vN -name '*.patch' | sort
```

## Step 2 — Detect duplicates (skip already-applied patches)
Compare MD5 against previous zip:
```bash
md5 /tmp/niu-oss-vN/0001-*.patch
md5 /tmp/niu-oss-v(N-1)/0001-*.patch
```
Identical MD5 = already applied — skip. Only apply patches with new MD5 or from new subfolders.

## Step 3 — Security audit (new patches only)
```bash
grep -nE 'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}' \
  /tmp/niu-oss-vN/<new-patches> && echo "ADA RAHASIA" || echo "BERSIH"

grep "^diff --git" /tmp/niu-oss-vN/<new-patches> | grep "package.json" || echo "Tidak ada"
grep "^diff --git" /tmp/niu-oss-vN/<new-patches> | grep ".github/workflows" || echo "Tidak ada"

for f in /tmp/niu-oss-vN/<new-patches>; do
  echo "--- $(basename $f) ---"
  grep "^Subject:" "$f" | head -1
  grep "^diff --git" "$f" | sed 's|diff --git a/||' | cut -d' ' -f1
  echo ""
done
```

## Step 4 — Apply
```bash
cd ~/Desktop/Niumination/sites/niu-oss-dashboard
git fetch origin main 2>&1 | tail -2
git rebase origin/main
git am /tmp/niu-oss-vN/<new-patch-1>.patch
git am /tmp/niu-oss-vN/<new-patch-2>.patch
```
arena base commit is NOT an ancestor of local HEAD — normal; `git am` applies cleanly regardless.

## Step 5 — Verify
```bash
npm run typecheck 2>&1 | tail -3; echo "TC_EXIT=$?"
npm test 2>&1 | grep -E "Test Files|Tests |passed|failed" | tail -4; echo "TEST_EXIT=$?"
npm run build 2>&1 | tail -5; echo "BUILD_EXIT=$?"
python3 ~/Desktop/Niumination/scripts/secret-scan-staged.py 2>&1 | tail -3; echo "SCAN_EXIT=$?"
```
All exits must be 0 before pushing. If `npm test` fails with `AssertionError: expected 'X' to contain 'Y'` in `changelog.test.ts`, see sentinel pitfall below.

After a successful build, count static pages from the **built HTML**, and reconcile against the number arena claims:
```bash
find .next/server/pages -name '*.html' | wc -l
find .next/server/pages -maxdepth 1 -name '*.html' -exec basename {} .html \; | sort
```
If the count differs from arena's claim, recheck before writing DOX — see the `prerender-manifest` pitfall below.

## Step 6 — Push
```bash
git log --oneline -4
git push origin main 2>&1 | tail -3; echo "PUSH_EXIT=$?"
```

## Step 7 — DOX update
Update `~/Desktop/Niumination/docs/registry/deployment-status.md` row for `niu-oss`:
- Bump static page count (from patch subject or LAPORAN)
- Note new HEAD commit + patch version label (e.g. `2026.13-14`)
- Commit + push root repo

## Step 8 — Sapa-ai variant (arena → sapa-ai)
When the zip is `sapa-branch-dev#N.zip` (kit serah terima, not cumulative niu-oss):
```bash
# 1. Inventory: kit berisi audit-sapa-ai/ (docs 01-33, seri-patch 0001-0050, bundel) + sapa-ai/ (klon repo) + 00-UNTUK-HERMES.md
# 2. Baca 00-UNTUK-HERMES.md — ia menyebut patch mana yang HARUS diterapkan (mis. "terapkan 0050")
# 3. Basis: pastikan HEAD lokal = origin/dev; klon zip = HEAD + patch baru (log -14 lihat komit teratas)
#    MD5 patch lama zip1 vs zip2: BEDA = patch baru (bukan duplikat) — cek subject: git log pada klon
# 4. SHA: shasum -a 256 -c SHA256SUMS.txt
# 5. Audit: grep -nE 'ghp_|sk-[A-Za-z0-9]{20,}' pada patch (hanya placeholder boleh ada)
# 6. Apply: git am <new-patch> (bukan bundle — bundle ulang dari zip bila dev masih lama)
# 7. Verify: tree hash vs klon zip (git rev-parse HEAD^{tree} kedua sisi) — WAJIB identik
#    npx vitest run (harap 719 / 44 berkas), npm run typecheck, npm run build, bash scripts/pii-gate.sh (LEAK_COUNT 0)
# 8. Uji terima (4-6 server) — lihat pitfall env di bawah
# 9. Push dev; main TIDAK tersentuh (harus tetap ff00eb8...)
```
Kit claim "byte-identik" — verifikasi dengan `git rev-parse HEAD^{tree}` BUKAN MD5 file (tree hash lebih kuat).

## Step 9 — DOX update (kedua varian)
Update `~/Desktop/Niumination/docs/registry/deployment-status.md` baris repo target:
- Bump komit + versi patch (mis. `0050`)
- Catat jumlah uji (mis. 719) — dari `vitest run` aktual, BUKAN klaim kit
- Commit + push root repo

## Pitfalls (sapa-ai variant)
- **Bocor env REVALIDATE_SECRET**: `scripts/uji-segarkan.mjs` mewarisi `...process.env` saat spawn app B (tanpa rahasia → fail-closed HARUS menolak). Bila `REVALIDATE_SECRET` ada di env global, app B TIDAK menolak → 6h GAGAL 5 butir palsu ("aplikasi B melaporkan kegagalan tercatat", "penjadwal keluar kode 3", dll). Verdict: **artefak setup, bukan cacat kode** — jalankan dengan `env -u REVALIDATE_SECRET -u ADMIN_TOKEN` atau set `SAPA_SKIP_SEGARKAN=1` lalu uji 6h terpisah.
- **korpus beracun/produksi git-ignored**: `verifikasi/korpus-*.json` TIDAK boleh di-commit (ada di .gitignore). Salin dari klon zip bila hilang.
- **Tree hash identik = sumber kebenaran**: setelah semua verifikasi, `git rev-parse HEAD^{tree}` harus sama dengan klon zip (`git -C /tmp/sapa-devN/sapa-ai rev-parse HEAD^{tree}`). Kalau beda, ada file yang tak ter-apply.
- **Uji bersih-data 6e**: korpus "bersih" = korpus PRODUKSI (2.065) dengan `SAPA_WAJIB_TERAMBIL=0`; perbaikan 0050 membuat laporan memakai `ringkasDariHasil()` sehingga spasi/kerapian TIDAK dihitung sebagai "sel dibersihkan" — hasil harus `0 sel dibersihkan`.
- **Eval det rate-limit**: 120 kueri, jeda ~62 dtk/24 query → uji terima penuh butuh ~10-15 menit. Biarkan jalan, jangan interupsi.

## Pitfalls

- **Cumulative zips: always MD5-check first.** Applying already-applied patches causes conflicts. `md5 <patch>` is the fastest gate.
- **Test sentinel in `changelog.test.ts`**: patches adding new CHANGELOG entries include a test asserting `out[0].version.toContain('YYYY.NN')`. The next patch adding a newer version breaks this with `AssertionError: expected 'YYYY.NN+1' to contain 'YYYY.NN'`. Fix: 1-line bump in `tests/changelog.test.ts`, commit separately as `test(changelog): bump versi sentinel ke YYYY.NN+1`.
- **Trailing whitespace warning from `git am`**: cosmetic only — AM_EXIT stays 0. Ignore.
- **`vercel domains verify` is not pure JSON**: pipe to `grep -E '"field"'`, not to `python3 json.load(sys.stdin)`.
- **`niumination/` folder in zip is a snapshot, not a git worktree**: use `.patch` files only.
- **Base commit mismatch is normal**: skip `merge-base --is-ancestor` check — it always fails for arena patches.
- **Docs page count from patch subject**: arena reports static page count in patch subject line (e.g. `212 statis`). Use that for DOX updates, not filesystem heuristics.
  - Reconcile, don't trust: count built HTML (`find .next/server/pages -name '*.html' | wc -l`) and compare. If the counts disagree, find out why before writing either number into DOX.
- **`prerender-manifest.json` undercounts Next.js pages**: do not use it to total static pages. It omits routes that do build to static HTML (observed: `/glosarium`, `/requirement`, `/404` present as `.html` in `.next/server/pages` but absent from the manifest). Count built HTML instead. The manifest is fine for listing which dynamic routes were prerendered — wrong as a total.
- **Never invent names when writing DOX.** Every component, file, and path written into documentation must first be observed with `ls`/`find`/`grep` in the actual tree. A plausible-sounding name that does not exist (e.g. deriving `AsesorDial` from a `Dial` component used on the asesor page) is a false claim that survives until an external reviewer checks. One `ls components/` before writing the component list catches it.
- **The DOX pass is part of the patch adoption, not an afterthought to it.** After `git am` and verification, update the repo's own `AGENTS.md` / `README.md` / `CHANGELOG.md` + the ecosystem `docs/registry/*` rows in the same pass, then commit and push both the repo and the root. A DOX pass left for "later" is how numbers go stale between the build and the write-up.

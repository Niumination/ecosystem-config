# Arena zip tanpa patch — varian snapshot/artefak

Tidak semua zip arena berisi gerombol `.patch`. Sebagian (mis. `mc-v4.zip` ke mission-control) berisi **worktree bersih + artefak sesi + dokumen audit**: HEAD zip identik dengan HEAD repo lokal, tidak ada komit baru untuk di-apply.

## Cara mengenali (sebelum coba `git am`)

```bash
# 1. HEAD zip vs HEAD repo lokal
git -C /tmp/zip-clone rev-parse HEAD
cd <repo-lokal> && git rev-parse HEAD
# identik == snapshot, bukan update patch

# 2. file zip yang TIDAK ter-track di repo
cd /tmp/zip-clone && git ls-files | sort > /tmp/zip-tracked.txt
find . -type f -not -path './.git/*' | sed 's|^\./||' | sort > /tmp/zip-all.txt
comm -13 /tmp/zip-tracked.txt /tmp/zip-all.txt   # <- kandidat dokumen baru

# 3. beda kecil tak relevan (bukan patch): mode exec, package-lock normalisasi, build artifact
# git diff HEAD -- <file>  untuk lihat isi beda
```

## Apa yang dilakukan

1. HEAD identik = **tidak ada `git am`**. Jangan paksa; tidak ada patch untuk diterapkan.
2. Untracked dari zip = **dokumen/aset baru** — salin selektif (AUDIT/PRD/assets), bukan `cp -r` seluruh zip.
3. Jangan track build artifact (`next-env.d.ts`, `tsconfig.tsbuildinfo`, `.next/`, `node_modules/`) — sudah di-ignore oleh .gitignore child; verifikasi `git status --short` bersih setelah salin.
4. Jangan salin folder redundan luar repo (mis. `Unselected files/`) — varian konsep duplikat.
5. Commit selektif (`git add <file>`, bukan `git add .`), push, verifikasi HEAD == origin.
6. Update registry/DOX root (project-catalog/deployment-status) dengan baris proyek bila belum ada.

## Aturan
- Bila HEAD zip == HEAD lokal, ini bukan task apply-patch; ini task **track-dokumen**. Laporkan begitu.
- MD5 per file sumber (dokumen yang disalin) harus identik zip → bukti salinan utuh.
- Perbedaan kecil zip vs HEAD (mode 755→644, package-lock) = artefak normalisasi, jangan ditrack ulang.

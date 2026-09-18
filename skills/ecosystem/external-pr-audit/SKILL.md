---
name: external-pr-audit
description: "Use when an external-agent PR/branch/artifact arrives for an ecosystem repo (Arena/designarena/agen luar lain). Audit before merge — CI truth, rahasia, dampak runtime, import mati, sisa sisi provider — lapor temuan, JANGAN merge tanpa perintah eksplisit pemilik."
tags: [ecosystem, adoption, security, review, github, niumination]
last_updated: "2026-09-18"
version: 1.0.0
changes:
  - v1.0.0 — Dibuat setelah audit PR #5 PemdiAcehTengah (245 berkas dari app/arena-ai-coding-agent)
---

# External PR Audit — Adopsi Hasil Kerja dari Platform Luar

## Trigger

Pemilik bekerja **tidak hanya di ekosistem ini**. Ia juga mengerjakan proyek ekosistem di luar (arena.ai, designarena.ai) atau eksperimen di sandbox terpisah. Hasil dari luar masuk ke ekosistem sebagai: PR GitHub, branch, zip/patch-stack, atau laporan audit — biasanya atas nama **GitHub App pihak ketiga** (mis. `app/arena-ai-coding-agent`).

Pakai skill ini saat tiba hasil kerja dari luar untuk repo in-ekosistem dan pertanyaannya: **"layak di-merge/diadaptasi atau tidak?"**

Skill bersaudara: `external-patch-adoption` (zip/patch-stack) · `ecosystem-tool-adoption` (tool pihak ketiga). Skill ini khusus **artefak yang menempel ke repo yang sudah ada, lewat GitHub** (PR/branch).

## Aturan keras

1. **Sandbox luar itu SAH, bukan drift.** Jangan memperlakukan pekerjaan luar sebagai anomali/pelanggaran. Itu cara kerja pemilik: fokus per proyek, dengan sandbox terpisah (pelajaran dari insiden jcode yang merusak internal Mac).
2. **Gerbang adopsi milik pemilik.** Ekosistem berperan **memeriksa lalu melaporkan**, bukan mengeksekusi otomatis. Tidak ada merge/adaptasi besar tanpa perintah eksplisit ("gas", "merge", "kerjakan").
3. **Jangan ubah sandbox luar dari sini** tanpa izin — termasuk memberi komentar/merging PR-nya.
4. **CI hijau ≠ aman.** Bukti hijau hanya menyatakan *build* lewat. Wajib diperiksa: apakah test benar-benar dijalankan CI, apakah header/CSP baru merusak perilaku **runtime** browser, apakah ada import ke berkas yang dihapus, apakah artefak generated masih dibuat saat build.
5. **Setiap perubahan kecil harus diteliti** — satu baris `.gitignore` yang salah tulis bisa membuka 4 berkas backup untuk ter-commit. Temuan wajib dilaporkan sebagai **syarat**, bukan disembunyikan.
6. **Ini bukan pengganti audit keamanan repo** — untuk rahasia publik/alert, pakai `git-security-sanitization`.

## Workflow

### 1. Identitas & cakupan (read-only)

```bash
gh pr view <N> --repo <R> --json title,state,isDraft,author,mergeable,mergeStateStatus,additions,deletions,changedFiles,comments,reviews
gh pr checks <N> --repo <R>
gh api /apps/<app-slug> --jq '"\(.owner.login) — \(.description)"'   # siapa app-nya
```

Catat: penulis (bot/App/manusia), cabang → base, umur, jumlah commit, apakah pernah di-review manusia. **App pihak ketiga dengan hak tulis = temuan audit akses**, sebutkan ke pemilik.

### 2. Daftar berkas — JANGAN pakai `gh pr diff` untuk PR besar

`gh pr diff` mengembalikan **kosong** pada diff besar (dan gagalnya senyap bila stderr dibuang). Pakai API dengan paginasi penuh:

```bash
gh api "repos/<R>/pulls/<N>/files?per_page=100" --paginate \
  --jq '.[] | "\(.status)\t\(.filename)\t+\(.additions)\t-\(.deletions)"' > /tmp/pr-files.txt
# sebaran + status
cut -f2 /tmp/pr-files.txt | awk -F/ '{print $1}' | sort | uniq -c | sort -rn
cut -f1 /tmp/pr-files.txt | sort | uniq -c
```

**Pitfall grouping:** `awk -F/` menaruh direktori berawalan titik (`.agents/…`) sebagai "(root)" bila logikanya `NF==1`; hitung ulang dengan filter eksplisit sebelum melaporkan sebaran.

### 3. Jalur berisiko (periksa satu per satu)

```bash
grep -E '\.env|secret|credential|\.npmrc|\.pem|id_rsa|\.github/workflows/|package(-lock)?\.json|vercel\.json|next\.config|\.gitignore' /tmp/pr-files.txt
```

- **Rahasia di berkas BARU — termasuk dokumen**: pindai baris `+` dari diff, jangan hanya kode.
  ```bash
  git diff origin/main FETCH_HEAD -- . ':(exclude).agents' | grep -E '^\+' \
    | grep -nE 'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,}|eyJ[A-Za-z0-9_-]{20,}\.|service_role|BEGIN [A-Z ]*PRIVATE KEY'
  ```
  Temuan berupa **nama variabel di dokumentasi** bukan kebocoran — bedakan nilai vs nama.
- **`.gitignore`**: bandingkan aturan yang **hilang**, bukan hanya yang bertambah. Salah tulis (`data/*.bak-*` → `.data/*.bak-*`) membuat berkas backup di disk tidak lagi ter-ignore → rawan ter-commit. Uji: `git check-ignore -v <berkas-nyata>` **pada isi cabang PR** (`git show FETCH_HEAD:.gitignore`).
- **Dependensi**: lihat hanya baris tambahan di `dependencies`/`devDependencies`. Menambah `engines`/script = aman; menambah paket = rantai pasok, minta justifikasi.
- **Workflow CI**: perubahan `.github/workflows/*` bisa menjalankan kode dengan secret. Tidak ada perubahan = aman.

### 4. Dampak runtime, bukan hanya build

Perubahan header/CSP/ganti aset hanya terlihat rusak di **runtime**. Yang wajib dicek:

```bash
git grep -n -i 'supabase' FETCH_HEAD -- pages components lib | grep -v -E 'api/|supabaseAdmin'
git grep -nE "^import .*(<modul yang dihapus>)" FETCH_HEAD -- pages components
```

- CSP `connect-src 'self'` aman **hanya jika** klien tidak pernah memanggil layanan luar (mis. Supabase selalu server-side). Buktikan dengan grep, jangan berasumsi.
- Font/aset yang dihapus: cek 0 rujukan (`git grep -c -F <nama>`), dan cek apakah penggantinya self-host.
- **Artefak generated** (`robots.txt`, `sitemap*.xml`) boleh dihapus dari repo **hanya bila** generatornya ada dan jalan saat build (`next-sitemap.config.js` + `postbuild`).

### 5. Sisi provider (yang belum dipasang di luar repo)

Cari pemakaian fungsi/RPC/tabel yang harus **dibuat manual di provider**:

```bash
git grep -nE "<nama_rpc>|<nama_tabel>" FETCH_HEAD -- lib pages | grep -v AGENTS
```

Jika kode memanggil RPC/tabel yang belum dibuat (mis. Supabase SQL belum dijalankan), pastikan ada **fallback** dan laporkan bahwa manfaat keamanannya **belum aktif** — ini syarat pasca-merge, bukan alasan menolak.

### 6. Kelayakan publikasi (repo publik!)

Dokumen audit/hasil scan yang ikut di-commit ke repo **publik** = peta kelemahan terpublikasi. Periksa:

- Apakah temuan sudah diperbaiki di PR yang sama (aman) atau masih terbuka (berbahaya)?
- Apakah ada pernyataan internal/sensitif (klaim instansi, hasil evaluasi eksternal, insiden) yang tidak layak publik?
- Rekomendasi: laporan audit tetap **lokal/privat**; repo publik hanya memuat hasil akhir.

### 7. Vonis + syarat (format laporan ke pemilik)

Selalu akhiri dengan: **vonis (layak / layak dengan syarat / tidak)**, **bukti** (perintah + hasil), **syarat** (temuan yang harus dibetulkan lebih dulu), **catatan** (tidak memblokir), dan **tindakan pasca-merge di provider**. Keputusan merge tetap milik pemilik.

## Pitfall

- **`gh pr diff` senyap-kosong** pada diff besar → API paginasi (lihat langkah 2).
- **"Test hijau" ilusi**: workflow CI sering hanya `lint` + `build`; cek `npm test` benar-benar dipanggil di `ci.yml`.
- **Import ke berkas dihapus**: grep pola nama file apa adanya; nama seperti `DetailModal` cocok dengan pola `Modal` → verifikasi manual sebelum menyimpulkan "fitur hilang".
- **Gate yang memblokir perbaikan**: hook pre-commit yang menolak **penghapusan** `.env` (positif palsu) dan pola `grep -c … || echo 0` (`0\n0` → uji numerik error, bisa meloloskan rahasia). Perbaiki: `--diff-filter=d` + buang `|| echo 0`.
- **Jangan commit pekerjaan agent lain** yang belum diminta (mis. berkas `scripts/model-*` untracked) — `git add` selektif selalu.
- **Jangan menilai dari komentar PR**: komentar sering hanya bot deploy (Vercel). Review manusia = 0 artinya belum ada peninjau kedua.

## Bukti keluar (sebelum lapor "layak")

- [ ] Status CI + deploy dibaca dari API, bukan dari badge
- [ ] Jumlah berkas & status (added/modified/removed) dari paginasi penuh
- [ ] Pemindaian rahasia atas **seluruh** baris tambahan, termasuk dokumen
- [ ] 0 import tersisa ke berkas yang dihapus (diverifikasi manual)
- [ ] Perubahan header/CSP diuji terhadap perilaku runtime
- [ ] Aturan `.gitignore` yang hilang diuji dengan `git check-ignore` pada isi cabang
- [ ] Sisa sisi provider (RPC/tabel/fallback) dicatat sebagai tindakan pasca-merge
- [ ] Verdict + syarat + catatan disampaikan; **merge menunggu perintah pemilik**

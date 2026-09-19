# Audit klaim DOX vs kenyataan repo

Resep untuk pertanyaan "apakah semua dokumentasi sudah dirapikan dan diupdate?". Bukan cek ukuran berkas (itu
`## 1`), melainkan cek **kebenaran klaim**.

## 0. Kumpulkan fakta sebelum menilai

```bash
git log -1 --format='  HEAD: %h %ad %s' --date=short
find . -name 'AGENTS.md' -not -path './node_modules/*' -not -path './.next/*' \
  | while read f; do printf '%-28s %s\n' "${f#./}" "$(git log -1 --format=%ad --date=short -- "$f")"; done
git status --porcelain          # bersih? ada yang belum di-push?
git rev-list --count origin/main..main
```

Semua `AGENTS.md` harus ter-update pada siklus hardening terakhir. Satu berkas yang tertinggal beberapa minggu
sementara tetangganya segar adalah sinyal pertama ada klaim basi di dalamnya.

## 1. Angka: hitung dari repo dan dari suite

```bash
echo "halaman : $(ls pages/*.js | wc -l)"
echo "api     : $(find pages/api -name '*.js' | wc -l)"
echo "komponen: $(find components -maxdepth 1 -name '*.js' | wc -l)"
echo "lib     : $(find lib -maxdepth 1 -name '*.js' | wc -l)"
find . -name '*.test.*' -not -path './node_modules/*'   # lokasi suite bisa di test/ atau tests/
npm test 2>&1 | tail -6                                   # angka tes otoritatif
```

- **Jangan** menyimpulkan jumlah tes dari `grep -c 'test('` — panggilan bersarang ikut terhitung.
- Sebagian klaim dokumen juga di-assert oleh suite (mis. `REGRESI: indeks aktual = 0,38`, `250 item bukti`).
  Kalau suite menguji angka dokumen, sebut itu sebagai bukti — dan kalau tidak, itu kandidat tes berikutnya.
- Bandingkan dengan klaim di **semua** berkas (`AGENTS.md`, `README.md`, child DOX), bukan hanya satu:
  ```bash
  for pat in '30 komponen' '16 unit test' '65 pages' '33 API'; do
    echo "$pat: $(grep -rc "$pat" --include='*.md' . | awk -F: '{s+=$2} END{print s+0}')"
  done
  ```

## 2. Kontradiksi internal (prioritas tertinggi)

Seksi yang bertabrakan dengan seksi lain **di berkas yang sama** membingungkan pembaca dan biasanya yang tertua
yang salah. Contoh nyata: "Recent Commits (Juni 2026) — semua di branch `fix/...` (belum merge ke main)"
berdampingan dengan tabel Project Overview yang menyebut branch `main`.

Ganti dengan seksi **"Status Sekarang"** berisi: branch + HEAD faktual, produksi, working tree, lalu tabel
milestone (hardening terakhir, merge eksternal, CI, infrastruktur data, DOX pass). Ini yang membuat dokumen
berguna untuk sesi berikutnya — bukan riwayat commit yang sudah tak relevan.

## 3. Angka lama: sisakan hanya sebagai catatan koreksi

Setelah mengganti angka, pembaca berikutnya masih bisa menemukan angka lama lewat grep. Itu wajar **asal**
kemunculannya hanya di dalam kalimat koreksi:

> Angka lama pada dokumen ini ("30 komponen", "16 halaman + 7 API route") tidak lagi berlaku dan sudah
> dikoreksi <tanggal>.

Dengan begitu grep tetap menemukan jejaknya (audit berikutnya tidak bingung) tapi tidak ada klaim aktif yang salah.

## 4. Cakupan rujukan berkas

```bash
for f in *.md;            do grep -q "$f" AGENTS.md          || echo "✗ root: $f"; done
for f in docs/*;          do grep -q "$(basename "$f")" docs/AGENTS.md || echo "✗ docs: $f"; done
```

Dokumen yang tidak pernah masuk tabel referensi tidak akan dibaca agent berikutnya. Verifikasi juga arah
sebaliknya: nama yang disebut dokumen tapi berkasnya tidak ada (symlink/rename lama).

## 5. Path yang berubah status dan gate yang diklaim

- Folder yang dicatat "✅ Dihapus" tapi ada kembali di disk (atau sebaliknya) = kontradiksi. Perbaiki catatannya
  di kedua arah, dan sebutkan status track/ignore-nya (`git ls-files` = 0, di-`.gitignore`) supaya tidak
  dikira sampah yang harus dihapus.
- Setiap gate yang diklaim (CI menjalankan tes, pre-commit menolak rahasia) harus punya berkasnya. Cek:
  ```bash
  grep -rl 'npm test' .github/workflows/ 2>/dev/null
  for f in db/schema.sql .github/workflows/ci.yml; do
    hit=$(grep -rl "$(basename $f)" --include='*.md' . | tr '\n' ' '); echo "$f: ${hit:-TIDAK disebut}"
  done
  ```

## 6. Kerapian yang tetap harus dibetulkan

```bash
grep -n '^||' AGENTS.md README.md pages/AGENTS.md   # baris tabel kelebihan pipe → tabel tidak ter-render
```

## 7. Verifikasi penutup (bukan klaim)

```bash
npm test 2>&1 | tail -6      # tes harus lulus setelah suntingan markdown (murah, dan menangkap salah sunting)
npm run build 2>&1 | tail -8 # build berakhir di tahap sitemap = semua halaman ter-build
for f in *.md; do grep -q "$f" AGENTS.md || echo "✗ $f"; done
grep -c '^||' AGENTS.md      # 0
git status --porcelain       # bersih, atau daftar yang belum di-commit
```

Laporkan **apa yang sudah benar** juga (angka yang cocok, rujukan yang sah) supaya pemilik tahu bagian mana yang
sudah diverifikasi dan bagian mana yang diperbaiki — bukan hanya daftar kesalahan.

## 8. Finalisasi setelah sesi kerja ("finalkan sampai kondisi terakhir")

Urutan yang terbukti; jalankan setelah kerja kode selesai, dalam **satu commit gabungan** (kode + dokumen).

1. **Hitung ulang fakta** (bagian 1) sebelum menyentuh prosa — jangan menyalin angka dari dokumen lama.
2. **Sidik klaim basi dengan pola literal**, bukan hanya angka: SHA HEAD lama, nama teknologi yang sudah digantikan
   (font/palet/framework), rasio tes lama (`n/n pass`), nama folder yang sudah di-rename.
   ```bash
   for pat in '<sha-head-lama>' '<nama-teknologi-lama>' '16/16' '<folder-lama>/'; do
     printf '%-24s %s\n' "$pat" "$(grep -rIl -F "$pat" --include='*.md' . 2>/dev/null | tr '\n' ' ')";
   done
   ```
3. **Pisahkan klaim AKTIF dari catatan HISTORIS.** Baris tabel "ubah X → Y", catatan koreksi, dan dokumen migrasi
   memang boleh memuat nilai lama. Yang wajib dibetulkan: klaim keadaan sekarang — tabel Project Overview (HEAD),
   aturan arsitektur (teknologi/token aktual), child DOX yang menghitung komponen/modul/tes, bagian Verification.
   Jangan "membersihkan" riwayat.
4. **Perbarui klaim aktif di sumbernya**, lalu pastikan angka yang sama tidak tertinggal di child DOX lain
   (hitung dengan `grep -rn -F '<angka>' --include='*.md'`).
5. **Banner status untuk dokumen rencana bertanggal** alih-alih menulis ulang isinya — satu baris di bawah judul:
   `> **Status:** dokumen historis (<tanggal>) — rencana awal, bukan status aktif. Kondisi terkini: AGENTS.md.`
6. **Sinkronkan empat permukaan sekaligus**: `CHANGELOG.md` (entri publik tanpa detail internal), sub-`BACKLOG.md`
   (seksi selesai + perbaiki klaim lama di dalamnya), tabel status root `AGENTS.md`, baris "terakhir diperbarui".
7. **Tutup dengan bukti**: `npm test` + `npm run build` + scan pola lama kembali bersih + `git status` bersih;
   commit, push, lalu verifikasi CI — bukan menyimpulkan dari transcript.

## 9. Temuan kebersihan repo: laporkan, jangan hapus sendiri

Sisir kerapian tanpa menghapus apa pun yang destruktif; keputusan tetap milik pemilik.

```bash
git status --ignored --short | head                     # di-ignore tapi masih di disk
git ls-files -z | xargs -0 ls -la | awk '$5>512000'     # berkas besar yang ter-track
find . -name '.DS_Store' -o -name '*.bak*' -o -name '*.old' -not -path './node_modules/*'
du -sh .git node_modules .next docs public              # sumber bloat terbesar
shasum -a 256 <berkas-besar-1> <berkas-besar-2>         # binari byte-identik?
```

Aturan pelaporan:
- **Junk OS (`.DS_Store` dan sejenis)** — regenerable, di-ignore: boleh dihapus tanpa bertanya.
- **Cadangan `*.bak-*`, folder ekstraksi besar, `node_modules`/`.next`** — ukur, sebutkan status ignore-nya, minta
  keputusan; jangan hapus sendiri.
- **Binari byte-identik (sha256 sama) di dua slot berbeda** = bloat nyata, tapi menghapus salah satunya bisa memutus
  rujukan (mis. dua slot bukti memakai dokumen yang sama) — laporkan pasangan + ukuran, biarkan pemilik memutuskan.
- **Bloat riwayat (`.git` besar)** hanya hilang lewat tulis ulang riwayat (git-filter-repo/BFG): sebutkan
  konsekuensinya (semua klon harus re-clone, deploy ikut terdampak) dan minta izin eksplisit + cadangan dulu.
- Sajikan sebagai tabel **temuan · ukuran · rekomendasi**, lalu tunggu; jangan dicampur ke commit dokumentasi.

# scripts/dr-restore — SISI BUILD (jangan tertukar dengan repo restore)

Folder ini berisi skrip yang **membaca mesin yang masih hidup** dan membekukan hasilnya ke repo `niumination-restore`. Skrip restore-nya sendiri **tidak** di sini — ia tinggal di repo `Niumination/niumination-restore` (satu berkas, satu repo-home).

## Pembagian dua sisi

| Sisi | Lokasi | Dijalankan kapan | Isi |
|---|---|---|---|
| **BUILD** | di sini | di device hidup, berkala | `build-credentials.sh`, `build-l2.sh`, `build-l1-release.sh`, `build-services.sh` |
| **RESTORE** | repo `niumination-restore` | di device baru/kosong | `restore.sh`, `verify.sh`, `scripts/subst-paths.sh`, `scripts/services/*` |

Arah dependensi satu jalur: BUILD menulis ke repo restore. Repo restore **tidak pernah** membaca folder ini.

## Urutan build (jalankan berkala, mis. bulanan)

```bash
bash build-credentials.sh      # ~/.ssh, ~/.9router, vault/ → credentials/*.enc
bash build-l2.sh               # berkas gitignored penting → l2-data/*.enc + allowlist
bash build-services.sh         # plist launchd → template + {{HOME}}
bash build-l1-release.sh       # Hermes home → aset Release (dipecah)
```

Setelah itu di repo restore: `git add … && git commit && git push`, lalu **drill wajib** (lihat README repo) sebelum status platform dinaikkan.

## Aturan yang lahir dari kegagalan nyata

1. **Passphrase hanya di Keychain** (`niumination-restore-dr`), tidak pernah dicetak. Salinannya wajib ada di luar device — kalau device mati, Keychain ikut mati
2. **`gh` selalu pakai `--repo` eksplisit** — tanpa itu, perintah jatuh ke repo dari cwd (pernah membuat release nyasar di repo publik)
3. **`gh` di proses non-interaktif butuh `GH_TOKEN` dari `.env`** — Keychain tidak terbaca dari background, dan nilai warisan bisa basi → skrip **menimpa** dari `.env`
4. **Jangan `… | grep -q` di bawah `set -o pipefail`** — `grep -q` keluar lebih dulu, pipa kiri kena SIGPIPE (141), pipeline dilaporkan gagal padahal cocok → simpan keluaran ke berkas dulu
5. **Jangan `sed -i`** — BSD sed (macOS) berbeda dari GNU sed → pakai berkas sementara + `cat >` (menjaga inode & izin)
6. **Hash, bukan keberadaan** — berkas "ada" belum tentu benar isinya
7. **Blob besar ke aset Release**, bukan commit (batas 100 MB/berkas GitHub)

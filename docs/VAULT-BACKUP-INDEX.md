# Vault & Credential Backup — Index

> Repo ini **PUBLIK**. Tidak ada kredensial plaintext di sini — hanya indeks & petunjuk.
> Diperbarui: 2026-11-20T03:33:11.495959+08:00

## Lokasi vault terpusat
- **Repo privat**: `Niumination/zbmaus-vela-secrets` → `vault/`
- **Isi**: `vault.tar.gpg` (GPG RSA-3072/AES256, 6 file), `vault-public.key`, `manifest.json`, `README.md`
- **Akses**: butuh private key + passphrase yang HANYA ada di VPS (`~/.gnupg/`, mode 700/600), tidak pernah di-commit.

## Kredensial yang tercakup (nama saja, nilai TIDAK tercantum)
| File | Sumber | Jenis |
|---|---|---|
| `yt-oauth.env` | `/opt/yt-oauth/yt-oauth.env` | OAuth client secret |
| `yt-token.json` | `/opt/yt-oauth/token.json` | OAuth refresh token |
| `cf-kaggle-token.md` | `~/zb/cf-kaggle-token.md` | Cloudflare API token |
| `kaggle-arb-debian.md` | `~/zb/kaggle-arb-debian.md` | Kaggle credential |
| `kaggle-tunnel-debian.md` | `~/zb/kaggle-tunnel-debian.md` | Kaggle tunnel config |
| `tunnel-kaggle.md` | `~/zb/tunnel-kaggle.md` | Tunnel config |

## Aturan (warisan AGENTS.md)
1. Secret tidak pernah ditaruh plaintext, walau di repo privat — selalu terenkripsi (GPG).
2. `ecosystem-config/vault/` sengaja di-`gitignore` → tidak dipakai untuk menyimpan isi.
3. Setelah dekripsi, hapus hasil ekstraksi; jangan biarkan plaintext mengendap.
4. Rotasi kunci → re-enkripsi → perbarui `manifest.json` di repo privat.

## Ekosistem yang tercakup backup
- **VPS zb-vela**: YouTube OAuth mandiri (yt-oauth), niudrive, OMB/zbmaus, tunnel Cloudflare, backup jobs.
- **Kaggle**: token & tunnel (Akun `arb` — TIDAK pernah auto-action tanpa approval).
- Lihat `docs/ECOSYSTEM-STATUS.md` untuk status aktual layanan & domain.

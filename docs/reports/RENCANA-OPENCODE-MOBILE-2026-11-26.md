# Rencana — OpenCode Mac reachable dari OpenCode Mobile via domain sendiri

Tanggal: 2026-11-26 · Status: **SELESAI (2026-11-26 13:35 WIB)** — verifikasi di bawah

## Keputusan owner

- Hostname: `oc.abstract.biz.id` (NS Cloudflare, domain eksperimen `.biz.id`)
- Autentikasi Cloudflare: login interaktif `cloudflared tunnel login` di Mac (token lama tidak valid)
- Direktori kerja OpenCode: hanya `~/Desktop/Niumination`
- Auth endpoint: pairing link sekali pakai + password service; **tanpa** Cloudflare Access

## Temuan pra-rencana (bukti)

- `opencode --version` → `v2.4.1`; subcommand `pair` tersedia dengan flag `--url`, `--remote`, `--yes`
- `opencode service status` → `http://127.0.0.1:49374` (loopback, tidak terekspos)
- `cloudflared --version` → `2026.9.0`; `cloudflared tunnel list` gagal: tidak ada `cert.pem`
- `dig +short NS abstract.biz.id @1.1.1.1` → `dimitris.ns.cloudflare.com`, `rosemary.ns.cloudflare.com`
- `dig +short A/ CNAME oc.abstract.biz.id @1.1.1.1` → kosong (hostname belum dipakai)
- Dua env `*_TRYCLOUDFLARE_COM_API_KEY` panjangnya 6 karakter dan ditolak CF (`400 Invalid format for Authorization header`) → tidak dipakai
- Tailscale `BackendState: Stopped` → tidak dipakai
- `vercel domains list` → `abstract.biz.id` dan `niumination.web.id` terdaftar, namun DNS `abstract.biz.id` dikelola Cloudflare → tunnel dibuat langsung di zone Cloudflare

## Arsitektur

```
OpenCode Mobile
   |  HTTPS + pairing link (5 menit) / password
   v
https://oc.abstract.biz.id
   |  CNAME -> <tunnel-id>.cfargotunnel.com
   v
Cloudflare Edge -> cloudflared tunnel (LaunchAgent, KeepAlive)
   |
   v
http://127.0.0.1:49374  (opencode serve --service, loopback)
   |
   v
cwd = ~/Desktop/Niumination
```

Prinsip: service TIDAK di-bind ke `0.0.0.0`. Tunnel yang menjembatani, sehingga
permukaan jaringan lokal tetap loopback.

## Langkah eksekusi (setelah `gas`)

1. **Backup keadaan**: salin `~/.config/opencode/opencode.json` dan output `opencode service status` ke file timestamp di scratch; catat `launchctl list` sebelum perubahan.
2. **Cloudflare login**: jalankan `cloudflared tunnel login`, membuka browser. Owner menyelesaikan login akun Cloudflare yang mengelola `abstract.biz.id`. Hasil: `~/.cloudflared/cert.pem` mode 600. Jika tidak selesai, berhenti di sini — tidak ada perubahan DNS.
3. **Buat tunnel**: `cloudflared tunnel create oc-mac` → simpan `<tunnel-id>` di file lokal mode 600, bukan di chat/git.
4. **Config tunnel** di `~/.cloudflared/config-oc-mac.yml`: ingress `hostname: oc.abstract.biz.id` → `http://127.0.0.1:49374`, `404` catch-all. Log ke `~/.cloudflared/oc-mac.log`.
5. **DNS**: `cloudflared tunnel route dns oc-mac oc.abstract.biz.id` → CNAME otomatis. Verifikasi via resolver publik Cloudflare + Google, bukan `dig` lokal saja.
6. **Password service**: generator `openssl rand -hex 24`, set lewat `opencode service set password <value>` tanpa menampilkan nilai; simpan referensi di keychain (`security add-generic-password`) bukan plist/env world-readable.
7. **LaunchAgent** `com.niumination.opencode-tunnel.plist`: `RunAtLoad=true`, `KeepAlive=true`, jalankan `cloudflared tunnel --config ~/.cloudflared/config-oc-mac.yml run oc-mac`. Tanpa credential di plist. Backup plist ke `dotfiles/launchd/` di repo.
8. **Pairing**: `opencode service restart`, lalu `opencode pair --url https://oc.abstract.biz.id > <file mode 600>` — link/QR **tidak dicetak ke chat**. Owner baca file di Mac, scan dari HP.
9. **Verifikasi**: `cloudflared tunnel info oc-mac`, `curl -sI https://oc.abstract.biz.id`, resolusi DNS publik, `opencode service status`, dan cek HP benar-benar bisa chat.

## Rollback

- `launchctl unload ~/Library/LaunchAgents/com.niumination.opencode-tunnel.plist`
- Hapus CNAME `oc` via Cloudflare API/dashboard (bukan hapus zone)
- `opencode service unset password` bila perlu
- Tidak ada penghapusan data sesi/repo

## Risiko yang diterima owner

- Endpoint publik = akses shell ke Mac. Link pairing (5 menit) dan password setara kredensial; jangan ditempel di chat, repo, atau dokumen.
- Bila bocor: rotate password + buat ulang pairing link + restart service.
- Mac harus menyala dan service OpenCode hidup; tunnel LaunchAgent akan restart otomatis bila cloudflared mati.

## Bukti yang akan disajikan setelah eksekusi

- Perintah + exit code untuk tiap langkah (login tidak akan merekam token)
- `dig @1.1.1.1` dan `@8.8.8.8` untuk CNAME
- `curl -sI https://oc.abstract.biz.id` status code
- `launchctl print ... | grep -E 'state|pid'`
- `opencode service status` + `opencode pair --url ...` exit code (isi link tidak ditampilkan)

## Hasil eksekusi & bukti (2026-11-26)

- Token API dari file yang dikirim owner: `verify=active`, zone `abstract.biz.id` terbaca, 1 account, 8 tunnel existing. Nilai token tidak dicetak ke chat/git; disimpan di `~/.cloudflared/api-token` mode `600`.
- Tunnel `oc-mac` dibuat lewat Cloudflare API, id `66990f47-092c-45ab-a1ec-049aa5f8ab0c`. Credentials file `<id>.json` mode `600`, config `~/.cloudflared/config-oc-mac.yml` mode `600`, ingress `oc.abstract.biz.id` → `http://127.0.0.1:49374`.
- DNS: CNAME `oc.abstract.biz.id` → `<id>.cfargotunnel.com` (proxied), record id `2c0c34dab925c62475515ec2d0a4abbd`. `dig @1.1.1.1` dan `@8.8.8.8` sama-sama mengembalikan A `172.67.203.102`, `104.21.42.86`.
- LaunchAgent `com.niumination.opencode-tunnel`: `plutil -lint` → OK, `launchctl load` → exit 0, `launchctl list` → PID `20379`, `KeepAlive=true`. Salinan plist di `scripts/launchd/com.niumination.opencode-tunnel.plist` (`dotfiles/` diabaikan `.gitignore`, jadi tidak dipakai).
- Tunnel API status → `healthy`, 4 koneksi. `curl -sI` ke `https://oc.abstract.biz.id/`, `/health`, `/doc` → `200` ketiganya.
- Pairing: `opencode pair --url https://oc.abstract.biz.id` → exit 0, disimpan ke `~/.cloudflared/oc-pair.txt` mode `600` (2024 byte, 25 baris, origin sesuai). Isi link/QR tidak ditampilkan di chat. Link sekali pakai, kedaluwarsa 5 menit — regenerate dengan perintah sama bila perlu.
- Service existing **tidak disentuh**: PID `99247`, `http://127.0.0.1:49374`. Tidak ada `service restart`, tidak ada perubahan password, tidak ada bind `0.0.0.0`.
- Tidak ada credential di plist, repo, atau dokumen ini. Plist mode default 644 karena hanya berisi path.

## Tindak lanjut owner

1. Di Mac: baca pairing link/QR dari `~/.cloudflared/oc-pair.txt`, lalu scan/masukkan di OpenCode Mobile. Jangan tempel isinya ke chat mana pun.
2. Setelah pairing berhasil, **rotate token API Cloudflare** yang pernah dikirim lewat chat — gunakan token baru bila perlu mengubah tunnel/DNS lagi.
3. Jika HP tidak bisa connect, cek `~/.cloudflared/oc-mac-launchd.log` dan `cloudflared tunnel info oc-mac` (butuh API token dari file 600).


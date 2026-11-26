# Panduan OpenCode Mobile via oc.abstract.biz.id

Status: aktif sejak 2026-11-26. Service OpenCode Mac existing tetap jalan, tidak pernah di-restart.

## Akses dari HP

Origin: `https://oc.abstract.biz.id`

Buat pairing link baru di Mac (yang lama kedaluwarsa 5 menit):

```bash
/usr/local/bin/opencode pair --url https://oc.abstract.biz.id > ~/.cloudflared/oc-pair.txt
chmod 600 ~/.cloudflared/oc-pair.txt
cat ~/.cloudflared/oc-pair.txt
```

Scan QR atau salin link dari file itu ke OpenCode Mobile. Jangan kirim isi file ke chat mana pun.

Cadangan bila pairing gagal — connect manual di app:
- URL: `https://oc.abstract.biz.id`
- Username: `opencode`
- Password: `opencode service get password` (jalankan di Mac, jangan dicetak ke chat)

## Keadaan sistem

- Tunnel: `oc-mac`, id `66990f47-092c-45ab-a1ec-049aa5f8ab0c`, status `healthy`
- DNS: CNAME `oc.abstract.biz.id` -> `<tunnel-id>.cfargotunnel.com` (proxied)
- LaunchAgent: `com.niumination.opencode-tunnel`, PID aktif, `RunAtLoad=true`, `KeepAlive=true`
- Service OpenCode: `127.0.0.1:49374`, PID `99247` (tidak disentuh)
- Log tunnel: `~/.cloudflared/oc-mac-launchd.log`
- Salinan plist: `scripts/launchd/com.niumination.opencode-tunnel.plist`

## Keamanan

- Token API Cloudflare disimpan di `~/.cloudflared/api-token` mode `600`, tidak di repo/plist/dokumen.
- Token pernah dikirim lewat chat → rotate setelah pairing berhasil.
- Endpoint ini setara shell access ke Mac. Siapa pun yang punya pairing link/password bisa menjalankan perintah sebagai user.

## Verifikasi ringkas

```bash
launchctl list | grep com.niumination.opencode-tunnel
curl -s -o /dev/null -w '%{http_code}\n' https://oc.abstract.biz.id/health
dig +short oc.abstract.biz.id @1.1.1.1
pgrep -fl 'opencode serve --service'
```

Hasil terakhir: `200` untuk health, tunnel `healthy`, A record `172.67.203.102` / `104.21.42.86`, service PID `99247`.

## Rollback

```bash
launchctl unload ~/Library/LaunchAgents/com.niumination.opencode-tunnel.plist
```

Lalu hapus CNAME `oc.abstract.biz.id` dari dashboard/API Cloudflare. Data sesi OpenCode tidak dihapus.

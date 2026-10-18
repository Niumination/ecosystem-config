# Pembersihan Kredensial OpenCode — 18 Okt 2026 21:50

## Temuan yang Mengubah Diagnosis

**Blokir OpenCode adalah per-IP, bukan per-kredensial.** Dibuktikan dengan probe langsung:

```
opencode.ai/zen/v1/models  DENGAN kredensial    → 403  error code: 1010
opencode.ai/zen/v1/models  TANPA kredensial     → 403  error code: 1010
```

Pesan OpenCode sendiri:
> *"OpenCode's free models aren't available from your current network because we've detected
> abusive traffic from this IP address. **This isn't related to your account.** If you're on a VPN
> or proxy, turn it off and try again, or subscribe to OpenCode Go."*

IP publik keluar: `125.165.42.32` (Tailscale aktif, exit node `100.120.57.37`).

**Skala lalu lintas** (dari `usageHistory` 9router):
```
provider "opencode": 6.386 request
rentang: 2026-09-22T16:03 → 2026-10-18T13:12
```

## Yang Dihapus (semua kredensial OpenCode)

| # | Lokasi | Isi | Status |
|---|---|---|---|
| 1 | `~/.hermes/.env` | 4 baris `OPENCODE*` (`OPENCODE_API_KEY`, `OPENCODE_GO_API_KEY`, `OPENCODE_ZEN_API_KEY`, `OPENCODE_ZEN_BASE_URL`) | **dihapus** (4 → 0) |
| 2 | `~/.local/share/opencode/auth.json` | entri `opencode` (api, key 67 char) | **dihapus**; `zenmux` **disisakan** (layanan berbeda) |
| 3 | `~/.config/opencode/opencode.json` | `provider.9router.options.apiKey` (35 char) | **dihapus**; `baseURL` disisakan |
| 4 | `opencode.db` → tabel `credential` | `cred_14f0bd2a2001G9zxJJRx3gREC7`, integration=`opencode`, label=**`Personal`** (OAuth Desktop), value 352 char | **dihapus** (1 baris); sisa credential = 0 |

## Yang TIDAK Disentuh

- **`opencode serve` TIDAK dimatikan** — pid 5077 masih hidup (start 19:32, uptime 2j18m).
  Pekerjaan yang jalan di sana tidak diganggu.
- **Kredensial non-OpenCode utuh** — `zenmux` di `auth.json`, dan 5 baris
  (`NINE_ROUTER`, `PIXZ`/`NOUS`, `GEMINI`, `ANTHROPIC`, `OPENROUTER`, `TELEGRAM`) di `.env`.
- **Tidak ada entri OpenCode di keychain** — dicek `security find-generic-password`/`find-internet-password`: kosong.
- **9router tidak punya koneksi OpenCode** — nol entri `opencode` di `providerConnections`, nol baseUrl `opencode.ai`.
  Koneksi yang ada hanya pixz dan nous. Jadi tidak ada kredensial OpenCode di 9router untuk dihapus.

## Backup (untuk pemulihan)

```
~/.hermes/cache/scratch/oc-cleanup-20261018-215014/
  _Users_zaryu_.hermes_.env
  _Users_zaryu_.local_share_opencode_auth.json
  _Users_zaryu_.config_opencode_opencode.json
  credential-before.txt   (snapshot tabel credential)
```

## Sisa: Satu Kredensial di Memori Proses

Proses `opencode serve` (pid 5077) **masih memegang** `OPENCODE_API_KEY` di memorinya
(prefix `sk-p4…`, 67 char). Diverifikasi:
- **Bukan** key yang dihapus dari `.env` (hash berbeda: `975c9d3bfe` vs `f868b040e1`).
- **Tidak ada di file konfigurasi mana pun** — dicari di `~/.config/opencode`, `~/.local/share/opencode`,
  `~/.hermes`, `~/.9router`; nol kecocokan.
- Artinya key itu berasal dari environment saat proses dimulai (sesi interaktif), dan hanya ada di RAM.

Untuk melepasnya perlu restart proses `opencode serve` — **belum dilakukan** karena ada pekerjaan yang
sedang jalan di sana. Proses ini bukan unit launchd, jadi restart harus manual oleh pemilik
(jangan dilakukan oleh agen saat pekerjaan masih aktif).

## Konsekuensi yang Perlu Dipelajari

Menghapus kredensial **tidak mencabut blokir IP**. `oc/*` akan tetap membalas 403 sampai OpenCode
mencabut blokir terhadap IP `125.165.42.32`. Yang menghentikan trafik adalah mematikan jalur
`oc/*` (bukan menghapus key).

## Verifikasi Akhir

```
.env OPENCODE*          : 0
auth.json keys          : ['zenmux']
credential di db        : 0
opencode.json apiKey    : tidak ada (hanya baseURL)
opencode CLI            : HIDUP
backup                  : ada di oc-cleanup-20261018-215014
```

# Referensi: 9Drive — Storage Gateway Multi-Account

> **Disimpan:** 2026-08-16
> **Sumber:** https://github.com/zenhosta/9drive (1.7k⭐, 338 forks, MIT-ish/Public)
> **Tujuan:** Referensi arsitektur — bukan keputusan deploy (masuk kategori labs/🔬)

---

## Ringkasan

9Drive = storage gateway web app: menghubungkan **banyak akun Google Drive + S3-compatible** (MinIO, Cloudflare R2, Wasabi, Backblaze B2, AWS S3) menjadi **satu dashboard storage virtual**. Backend otomatis route upload ke akun yang masih punya ruang.

## Stack

- Backend: Express + TypeScript
- Frontend: React + Vite
- DB: MySQL + Prisma (migrations)
- Node 20+, PM2 (production), Docker (opsional)

## Fitur Kunci

1. **Multi-account storage** — connect banyak Drive, track quota per akun, satu dashboard
2. **Upload routing otomatis** — 3 policy: `most_available` | `round_robin` | `priority`
3. **Direct upload stream** — file TIDAK pernah lewat server (hemat bandwidth)
4. **S3-compatible** — custom endpoint (MinIO/R2/Wasabi/B2/AWS)
5. **External upload API** — `POST /api/v1/uploads` dengan API keys (hashed, scoped, revocable)
6. **File ops** — preview, download, rename, move, delete + virtual folders
7. **Auth** — email/password + Google sign-in, Bearer token, reCAPTCHA opsional
8. **Update otomatis** — `update.sh` (git reset --hard → pull → build → migrate → pm2 restart)

## Arsitektur Routing (paling berharga untuk dipelajari)

```
selectAccount(userId, sizeBytes, reservedBytesByAccount, targetAccountId?)
│
├─ 1. Query semua connected account (google_drive + s3, status=connected)
├─ 2. Stale check: storageAccount.lastSyncedAt > 5 menit → sync quota di background
│     (Promise.allSettled — non-blocking, gagal 1 akun tidak menghentikan yang lain)
├─ 3. Filter eligible: availableBytes >= sizeBytes (null = dianggap bisa)
├─ 4. Policy routing:
│     • most_available → sort descending availableBytes (S3 menang saat null)
│     • round_robin → cursor increment per user di DB
│     • priority → urut dari priorityAccountIds, fallback createdAt
└─ 5. Stream upload langsung ke provider terpilih
```

**Pola kunci:**
- `reservedBytesByAccount` — reservasi kuota saat batch upload supaya tidak overcommit
- Quota sync lazy — cuma sync akun stale (>5 menit), bukan semua
- Provider credential dienkripsi AES (`decryptText`) sebelum disimpan di DB
- API key disimpan hash, secret sekali tampil, `lastUsedAt` tracking + revoke

## Model Data Utama (Prisma)

- `User`, `ConnectedAccount` (google_drive|s3), `StorageAccount` (quota bytes)
- `S3StorageConfig` (endpoint, bucket, encrypted creds)
- `UploadRoutingPolicy` (mode, priorityAccountIds, roundRobinCursor)
- `File` (providerFileId, mimeType, sizeBytes), `Folder` (virtual), `FileShare`, `FilePreviewToken`
- `ApiKey` (keyHash, scopes, expiresAt, revokedAt), `AuditLog`, `WorkspaceInvite`

## Penyimpanan — Jawaban atas "Apakah makan ruang lokal?"

| Data | Lokasi | Ruang lokal |
|---|---|---|
| File upload | Google Drive / S3 bucket (stream langsung) | **0 byte** |
| Metadata | MySQL (remote/VPS) | KB-MB saja |
| Source code | VPS deploy | ~700KB (224K backend + 408K frontend + 92K prisma) + node_modules |

→ **Bisa 100% remote.** Frontend statis di Vercel/Netlify, backend+MySQL di VPS.

## Alternatif Lebih Sederhana

**rclone** — CLI single binary, 40+ provider, tanpa MySQL/backend/frontend:
```bash
# contoh: backup ke Google Drive
rclone sync /path/lokal remote:backup-folder --progress
```
Cocok jika kebutuhan hanya backup/jembatan file, bukan dashboard multi-user.

## Keputusan untuk Ekosistem Niumination

- **Status: LABS (eksperimen)** — bukan kebutuhan mendesak
- Relevansi terbesar: **pola routing `most_available`** → bisa diadopsi di Mission Control dispatch (multi-model routing berdasarkan beban)
- Jika backup bukti Pemdi (file besar) dibutuhkan → **rclone** lebih cepat & ringan

## Referensi

- Repo: https://github.com/zenhosta/9drive
- Live demo: https://9drive.zenhosta.com

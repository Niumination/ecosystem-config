# MATA Watchdog — Pi Payments Backend

> **Lokasi:** `apps/pi-app-studio-mata/server/`
> **Fungsi:** Forward payment approval & completion ke Pi Platform API
> **Port:** 3001 (default)

## Endpoints

| Method | Endpoint | Fungsi |
|--------|----------|--------|
| POST | `/api/payments/approve` | Forward ke Pi Platform `/v2/payments/:id/approve` |
| POST | `/api/payments/complete` | Forward ke Pi Platform `/v2/payments/:id/complete` |
| GET | `/api/health` | Health check |

## Environment Variables

Buat file `.env` di folder ini:

```env
PI_API_KEY=your_pi_api_key_here
PORT=3001
```

## Install & Run

```bash
cd server
npm install
npm start
```

## Production

Deploy ke VPS atau gunakan process manager (pm2, systemd).
Pastikan `PI_API_KEY` disimpan di environment variable server, JANGAN di repo.

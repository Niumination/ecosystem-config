# Akun Login — Ekosistem Niumination

> **Dibuat:** 13 Jul 2026
> **Tujuan:** Catatan akun untuk testing & development

---

## 🚚 TEDEO

| Item | Detail |
|------|--------|
| **URL** | https://tedeo-web.vercel.app |
| **Stack Auth** | JWT (Express backend) — register/login via API |
| **Admin (seed)** | `081370000001` / `admin123` |
| **Register** | Via web form — nama, nomor HP, password |
| **Backend API** | `POST /api/auth/login` → JWT token |
| **Catatan** | Saat ini frontend web terdeploy tanpa backend (Express). Login hanya berfungsi jika backend Express juga terdeploy. |

### Endpoint Auth
| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/api/auth/register` | POST | Daftar akun baru (konsumen/kurir) |
| `/api/auth/login` | POST | Login, dapat JWT token |
| `/api/auth/refresh` | POST | Refresh JWT token |
| `/api/auth/profile` | GET | Ambil profil user (perlu token) |

---

## 🤖 kune-ya.com

| Item | Detail |
|------|--------|
| **URL** | https://kune-ya-com.vercel.app |
| **Stack Auth** | next-auth v5 beta (Credentials provider) |
| **Login** | Email + password |
| **Daftar** | Via `/register` — email, nama, username, password |
| **Session** | JWT strategy — session token di cookie |

### Endpoint Auth
| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/api/auth/register` | POST | Daftar akun baru |
| `/api/auth/callback/credentials` | POST | Login via next-auth |
| `/api/auth/signout` | POST | Logout |

### Env
| Key | Nilai |
|-----|-------|
| `AUTH_SECRET` | ✅ **Rotated** (13 Jul) — random 64-byte base64 |
| `OPENAI_API_KEY` | ⚠️ **Belum di-rotate** — key dari file `.env` masih live, perlu rotate di OpenAI dashboard |

---

## 🔐 Catatan Keamanan

- Jangan commit file `.env` atau `.env.local` ke git
- Gunakan Vercel Environment Variables untuk production
- Rotasi secret secara berkala

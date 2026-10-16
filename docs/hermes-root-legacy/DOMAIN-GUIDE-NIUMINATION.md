# 🌐 Domain niumination.web.id — Panduan Lengkap

**Domain:** `niumination.web.id`  
**Provider:** idwebhost.com  
**Tipe:** Free .web.id domain  
**Created:** 30 Ags 2026

---

## 📋 Apa Itu .web.id?

`.web.id` adalah domain lokal Indonesia yang **gratis** untuk personal/portfolio website. Cocok untuk:
- Portfolio developer
- Project showcase
- Company website
- Personal branding

**Kelebihan:**
- ✅ Gratis selamanya (tidak perlu renew)
- ✅ Local Indonesian TLD
- ✅ Mudah diingat
- ✅ Support SSL (HTTPS)

**Kekurangan:**
- ⚠️ Tidak se-professional .com/.id
- ⚠️ Beberapa layanan mungkin tidak accept

---

## 🚀 Apa Yang Bisa Dilakukan?

### 1. **Point ke Vercel (Recommended)**
Deploy semua app Niumination dengan custom domain:

```
# Apps yang bisa di-migrate:
├── cc-acehtengah → niumination.web.id
├── niu-dash → dash.niumination.web.id
├── PemdiAcehTengah → pemdi.niumination.web.id
├── kune-ya → chat.niumination.web.id
└── niu-vermilion → brain.niumination.web.id
```

**Cara Setup:**
```bash
# 1. Add domain di Vercel dashboard
vercel domains add niumination.web.id

# 2. Update DNS di idwebhost cPanel:
#    A record: @ → 76.76.21.21
#    CNAME: www → cname.vercel-dns.com

# 3. Verify SSL
vercel domains inspect niumination.web.id
```

### 2. **Subdomain Strategy**
Organisir semua project dengan subdomain:

| Subdomain | Project | Status |
|-----------|---------|--------|
| `niumination.web.id` | Main site / redirect to GitHub | 🟢 Ready |
| `www.niumination.web.id` | WWW version | 🟢 Optional |
| `dash.niumination.web.id` | Niu-Dash | 🟢 Vercel |
| `pemdi.niumination.web.id` | Pemda Aceh Tengah | 🟢 Vercel |
| `chat.niumination.web.id` | KuneYa Chat | 🟢 Vercel |
| `brain.niumination.web.id` | Niu Vermilion | 🟢 Vercel |
| `api.niumission.web.id` | Backend API | 🔵 Future |
| `docs.niumination.web.id` | Documentation | 🟢 Ready |
| `blog.niumination.web.id` | Tech blog | 🔵 Future |

### 3. **Email Bisnis Gratis**
idwebhost menyediakan email hosting:
- `admin@niumination.web.id`
- `dev@niumination.web.id`
- `support@niumination.web.id`

**Setup di cPanel:**
1. Login idwebhost cPanel
2. Klik "Email Accounts"
3. Create new email
4. Configure di Outlook/Thunderbird

### 4. **Redirect & Alias**
Setup forwarding untuk convenience:
- `hello@niumination.web.id` → `admin@niumination.web.id`
- `info@niumination.web.id` → `admin@niumination.web.id`

### 5. **SSL Certificate (HTTPS)**
Sudah include gratis:
- ✅ Auto HTTPS via Let's Encrypt
- ✅ Force HTTPS redirect
- ✅ HSTS enabled

---

## 📊 Audit Project Saat Ini

| App | Current URL | Target Domain | Status |
|-----|-------------|---------------|--------|
| cc-acehtengah | [cc-acehtengah.vercel.app](https://cc-acehtengah.vercel.app) | niumination.web.id | 🟢 Ready |
| niu-dash | [niu-dash.vercel.app](https://niu-dash.vercel.app) | dash.niumination.web.id | 🟢 Ready |
| PemdiAcehTengah | [pemdi-acehtengah.vercel.app](https://pemdi-acehtengah.vercel.app) | pemdi.niumination.web.id | 🟢 Ready |
| kune-ya | [kune-ya.vercel.app](https://kune-ya.vercel.app) | chat.niumination.web.id | 🟢 Ready |
| niu-vermilion | [niu-vermilion.vercel.app](https://niu-vermilion.vercel.app) | brain.niumination.web.id | 🟢 Ready |
| tedeo-kanban | [tedeo.vercel.app](https://tedeo.vercel.app) | kanban.niumination.web.id | 🟢 Ready |

---

## 🔧 Step-by-Step Implementation

### Phase 1: DNS Setup (5 menit)
```bash
# Di idwebhost cPanel → DNS Management
# Tambah records:
A record: @ → 76.76.21.21 (Vercel IP)
CNAME: www → cname.vercel-dns.com
```

### Phase 2: Vercel Configuration (10 menit)
```bash
# Install Vercel CLI
npm i -g vercel

# Add domain ke setiap project
cd ~/Desktop/Niumination/apps/cc-acehtengah
vercel domains add niumination.web.id

cd ~/Desktop/Niumination/apps/niu-dash
vercel domains add dash.niumination.web.id

# Ulangi untuk semua project...
```

### Phase 3: Verification (2 menit)
```bash
# Check DNS propagation
vercel domains inspect niumination.web.id

# Test HTTPS
curl -I https://niumination.web.id
```

---

## 🎯 Recommended Actions

### Option A: Quick Win (15 menit)
1. ✅ Setup DNS di cPanel
2. ✅ Add domain ke 2-3 app utama
3. ✅ Test & verify

### Option B: Full Migration (1 jam)
1. ✅ Setup semua subdomain
2. ✅ Migrate semua app Vercel
3. ✅ Setup email bisnis
4. ✅ Create landing page

### Option C: Strategic (2 jam)
1. ✅ Semua di atas
2. ✅ Create docs.niumination.web.id
3. ✅ Setup monitoring
4. ✅ Create CI/CD pipeline

---

## 💡 Pro Tips

1. **SSL Auto:** Vercel auto-provision SSL, tidak perlu manual
2. **CDN Included:** Global CDN dengan 275+ edge locations
3. **Analytics:** Vercel Analytics gratis (100K pageviews/month)
4. **Preview Deploy:** Setiap PR dapat preview URL
5. **Environment:** Staging/Production separation

---

## 🚫 Yang TIDAK Bisa

- ❌ `.web.id` tidak support untuk e-commerce serius (paypal/bank tidak accept)
- ❌ Tidak professional untuk corporate formal
- ❌ Beberapa API provider block `.web.id` (rate limiting)
- ❌ Tidak bisa transfer ke registrar lain

---

## 📝 Next Steps

**Mau saya bantu setup?**

1. **A.** Setup DNS records di cPanel (anda yang login)
2. **B.** Configure Vercel domains (saya bisa guide)
3. **C.** Create landing page untuk main domain
4. **D.** Setup email bisnis (admin@niumination.web.id)

Pilih yang mana? ⚡ (◕‿◕)★

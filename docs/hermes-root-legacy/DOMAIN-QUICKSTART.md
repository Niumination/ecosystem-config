# 🚀 Quick Start: Setup niumination.web.id

## Step 1: DNS di idwebhost cPanel (5 menit)

1. Login ke [idwebhost.com](https://idwebhost.com)
2. Klik **"cPanel"** untuk domain niumination.web.id
3. Buka **"DNS Zone"** atau **"Manage DNS"**
4. Tambah records:

```
Type: A
Name: @
Value: 76.76.21.21
TTL: Auto

Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: Auto
```

5. Save & tunggu propagasi (5-30 menit)

---

## Step 2: Add Domain ke Vercel (10 menit)

### Method A: Via CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Add domain ke project
cd ~/Desktop/Niumination/apps/cc-acehtengah
vercel domains add niumination.web.id

cd ~/Desktop/Niumination/apps/niu-dash
vercel domains add dash.niumination.web.id

# Ulangi untuk semua project...
```

### Method B: Via Dashboard
1. Login ke [vercel.com](https://vercel.com)
2. Pilih project → Settings → Domains
3. Add domain: `niumination.web.id`
4. Ikuti instruksi DNS

---

## Step 3: Verify (2 menit)
```bash
# Check DNS status
vercel domains inspect niumination.web.id

# Test HTTPS
curl -I https://niumination.web.id
```

---

## Subdomain Mapping

| Subdomain | Project | Path |
|-----------|---------|------|
| `niumination.web.id` | cc-acehtengah | Main app |
| `dash.niumination.web.id` | niu-dash | Dashboard |
| `pemdi.niumination.web.id` | PemdiAcehTengah | Portal Pemda |
| `chat.niumination.web.id` | kune-ya | AI Chat |
| `brain.niumination.web.id` | niu-vermilion | Second Brain |
| `kanban.niumination.web.id` | tedeo-kanban | Project Board |
| `docs.niumination.web.id` | docs | Documentation |

---

## Checklist

- [ ] DNS records added di cPanel
- [ ] Domain added ke Vercel projects
- [ ] SSL certificate verified
- [ ] All subdomains working
- [ ] Email admin@niumination.web.id created
- [ ] Main landing page ready

---

**Need help?** Hubungi saya untuk setup! ⚡

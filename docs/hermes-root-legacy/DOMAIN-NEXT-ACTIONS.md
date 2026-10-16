# Domain niumination.web.id — Next Actions

## ✅ Completed
- [x] Landing page created (HTML/CSS/JS)
- [x] Deployed to Vercel: https://landing-sxbjvwk25-archk4lis-projects.vercel.app
- [x] Documentation created

## 🔄 In Progress
- [ ] DNS configuration di cPanel idwebhost
- [ ] Custom domain mapping ke Vercel

## 📋 Todo

### Phase 1: DNS Setup (5 menit)
1. Login ke idwebhost.com
2. Buka cPanel untuk niumination.web.id
3. Masuk ke "DNS Zone" atau "Manage DNS"
4. Tambah records:
   ```
   A record: @ → 76.76.21.21
   CNAME: www → cname.vercel-dns.com
   ```
5. Save & tunggu propagasi (5-30 menit)

### Phase 2: Vercel Domain (5 menit)
```bash
# Tambah domain ke project landing
cd ~/Desktop/Niumination/sites/landing
vercel domains add niumination.web.id
vercel domains add www.niumination.web.id

# Verify
vercel domains inspect niumination.web.id
```

### Phase 3: Migrate Other Projects (30 menit)
Pindahkan semua app Vercel ke subdomain:

| Subdomain | Project | Command |
|-----------|---------|---------|
| `niumination.web.id` | cc-acehtengah | `vercel domains add niumination.web.id` |
| `dash.niumination.web.id` | niu-dash | `vercel domains add dash.niumination.web.id` |
| `pemdi.niumination.web.id` | PemdiAcehTengah | `vercel domains add pemdi.niumination.web.id` |
| `chat.niumination.web.id` | kune-ya | `vercel domains add chat.niumination.web.id` |
| `brain.niumination.web.id` | niu-vermilion | `vercel domains add brain.niumination.web.id` |
| `kanban.niumination.web.id` | tedeo-kanban | `vercel domains add kanban.niumination.web.id` |

### Phase 4: Email Setup (10 menit)
Di cPanel idwebhost:
1. Buat email: admin@niumination.web.id
2. Configure di Thunderbird/Outook
3. Set up email forwarding (info→admin, support→admin)

---

## 🎯 Priority Order

1. **SKIP** — DNS setup (anda yang klik di cPanel)
2. **DONE** — Landing page deployed ✅
3. **NEXT** — Point domain ke Vercel
4. **FUTURE** — Migrate other projects

---

## 💡 Tips

- SSL auto-provisioned oleh Vercel (HTTPS ready)
- CDN global 275+ edge locations
- Analytics gratis (100K pageviews/month)
- Preview URLs untuk setiap PR

---

**Landing page sudah LIVE!** Sekarang point domain ke Vercel. ⚡

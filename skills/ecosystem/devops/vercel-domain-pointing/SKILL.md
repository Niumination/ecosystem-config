---
name: vercel-domain-pointing
description: Point custom domain to Vercel — nameserver, DNS, verify.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [vercel, domain, dns, nameserver, pointing, idwebhost]
    related_skills: [production-env-vars, github-pages-deploy]
---

# Vercel Domain Pointing

Mengarahkan domain custom ke proyek Vercel. Lahir dari pengalaman men-pointing niumination.web.id via idwebhost.

## Aturan Kunci

1. **Jangan tambah DNS record manual jika nameserver sudah Vercel.** Nameserver ke `ns1-4.vercel-dns.com` → Vercel handle DNS otomatis via ALIAS.
2. **Nameserver harus seluruhnya Vercel — tidak boleh campuran.** Semua 4: `ns1.vercel-dns.com`, `ns2.vercel-dns.com`, `ns3.vercel-dns.com`, `ns4.vercel-dns.com`.
3. **idwebhost butuh 24 jam untuk ganti nameserver.** Jangan cek CLI lokal langsung — gunakan DNS resolver publik.
4. **Verifikasi via DNS resolver publik**, bukan CLI lokal saja. `dig @1.1.1.1` dan `dig @8.8.8.8` bisa beda karena caching. Cross-check via Cloudflare/Google DNS API.
5. **Cek `vercel domains inspect`** setelah propagate.
6. **Domain sudah ditambahkan di Vercel dashboard tapi belum Verified → nameserver belum propagate.** Vercel dashboard menampilkan "DNS change recommended" sampai nameserver benar. Jangan tambah ulang domain — cukup tunggu dan cross-check DNS via resolver publik.
7. **Jika `vercel domains list` menunjukkan domain terdaftar tapi `vercel domains inspect` tidak ada → domain perlu attach ke project.** Jalankan `vercel domains add <domain> <project>` untuk attach.

## Prosedur

### 1. Tambah domain
```bash
vercel domains add niumination.web.id
vercel domains add niumination.web.id niu-oss  # attach to project
```

### 2. Ganti nameserver di idwebhost
Dashboard → DNS Management → Nameservers → ganti semua 4 ke:
- ns1.vercel-dns.com
- ns2.vercel-dns.com
- ns3.vercel-dns.com
- ns4.vercel-dns.com

**Hapus** semua lama. Tunggu 24 jam.

### 3. Cek propagasi
```bash
curl -s "https://cloudflare-dns.com/dns-query?name=niumination.web.id&type=NS" -H 'accept: application/dns-json'
curl -s "https://cloudflare-dns.com/dns-query?name=niumination.web.id&type=A" -H 'accept: application/dns-json'
curl -s "https://dns.google/resolve?name=niumination.web.id&type=A"
```

### 4. Verifikasi
```bash
vercel domains inspect niumination.web.id
```

### 5. Cek deploy
```bash
vercel ls niu-oss
curl -sI https://niumination.web.id | head -5
```

## Vercel DNS Records (Auto)

Setelah verified, Vercel menambahkan:
- `niumination.web.id` → `d0a001efa465354b.vercel-dns-017.com.` (ALIAS)
- `www.niumination.web.id` → `cname.vercel-dns-017.com.` (ALIAS)

Cek: `vercel dns list niumination.web.id`

## Jebakan

- **Nameserver campuran** → domain ✘ selamanya. Ganti SEMUA.
- **A record 76.76.21.21** lama → bukan IP Vercel. Hapus jika nameserver sudah Vercel.
- **DNS propagation lambat**: cross-check via API, bukan cek CLI langsung. `dig @1.1.1.1` dan `dig @8.8.8.8` bisa beda karena caching.
- **Dashboard belum show**: domain mungkin CLI add tapi belum attach → `vercel domains add <domain> <project>`.
- **Vercel dashboard "DNS change recommended" padahal domain sudah add**: nameserver belum propagate. Tunggu, jangan tambah ulang. Cek via `curl cloudflare-dns.com/dns-query`.
- **CNAME untuk apex domain**: jangan. Vercel pakai ALIAS. CNAME hanya untuk www.
- **Domain sudah verified tapi DNS belum resolve**: resolver publik belum propagate. Tunggu 24 jam (idwebhost nameserver) atau 5-15 menit (Vercel nameserver).
- **`git push` ditolak karena remote punya commit baru**: force push hanya jika HEAD lokal superset dari origin/main. Cek dulu `git merge-base --is-ancestor origin/main HEAD`.

## Tools

- `vercel domains add/inspect/list`, `vercel dns list`
- `curl -sI https://<domain>`
- `curl -s "https://cloudflare-dns.com/dns-query?name=<d>&type=A" -H 'accept: application/dns-json'`
- `curl -s "https://dns.google/resolve?name=<d>&type=A"`

## Env Var

Jika Next.js pakai `NEXT_PUBLIC_*`: `vercel env add NEXT_PUBLIC_VAR_NAME production`
Lihat `production-env-vars` skill untuk aturan pengiriman nilai.

# Learning from Session — 30 Ags 2026

## Key Learnings

### 1. 9router TIDAK Punya API Disable Model Per-User
**Finding:** 9router Gateway (localhost:20128) tidak expose API untuk disable/hide model per-user.

**Workaround yang berhasil:**
- Update config.yaml Hermes untuk hanya point ke model yang terverifikasi working
- Gunakan `hermes config set` command (bukan write_file/patch langsung)
- Simpan daftar model working di fallback_providers

**Implementasi:**
```bash
hermes config set model.provider 9router
hermes config set model.default "ag/gemini-3.5-flash-extra-low"
hermes config set fallback_providers '[]'
# Tambah 5 model working sebagai fallback
```

### 2. Kimi/Kiro Models Belum Muncul
**Finding:** User baru daftarkan Kiro di dashboard, tapi 0 model muncul di katalog 9router.

**Status:**
- Total models: 89
- Working: 39 (44%)
- Failed: 50 (56%) — kebanyakan `*-thinking`, `*-agentic` patterns

### 3. Landing Page Niumination Deployed
**Finding:** Successfully created dan deploy landing page ke Vercel.

**Output:**
- URL: https://landing-sxbjvwk25-archk4lis-projects.vercel.app
- Location: `~/Desktop/Niumination/sites/landing/`
- Files: index.html (33KB), README.md, DEPLOYMENT.md

### 4. Domain niumination.web.id Ready
**Next Steps:**
1. DNS setup di cPanel idwebhost (A record + CNAME)
2. Add custom domain ke Vercel
3. Migrate other projects ke subdomain

---

## Skills Needing Update (User-Owned — Cannot Edit)

### model-checker
**Current:** Basic checker with Python script
**Needs:**
- Update recommendation section dengan data terbaru (972ms fastest)
- Add pitfall about 9router no-disable-API
- Add Kimi/Kiro status note
- Update v2 script dengan SSE parsing yang lebih robust

**Recommended action:** `hermes curator adopt model-checker`

### hermes-provider-config
**Current:** Comprehensive provider config guide
**Needs:**
- Add Pitfall 13b: "9router TIDAK punya API disable model per-user"
- Add workflow untuk "disable models via config" bukan via 9router API
- Update provider status table dengan latest findings

**Recommended action:** `hermes curator adopt hermes-provider-config`

---

## Scripts Created (Reusable)

| Script | Location | Purpose |
|--------|----------|---------|
| `model-checker-v2.py` | `ecosystem/model-checker/scripts/` | Enhanced model checker v2 |
| `analyze-models.py` | `~/.hermes/` | Cross-reference catalog vs working |
| `update-9router-config.py` | `~/.hermes/` | Apply config changes via hermes config set |
| `verify-9router-final.py` | `~/.hermes/` | Test chat completion |

---

## Documentation Created

| File | Location | Purpose |
|------|----------|---------|
| `9ROUTER-FINAL-SUMMARY.md` | `~/.hermes/` | Complete config update summary |
| `DOMAIN-GUIDE-NIUMINATION.md` | `~/.hermes/` | Full domain setup guide |
| `DOMAIN-QUICKSTART.md` | `~/.hermes/` | Quick start for DNS setup |
| `DOMAIN-NEXT-ACTIONS.md` | `~/.hermes/` | Checklist for next steps |
| `LANDING-PAGE-COMPLETE.md` | `~/.hermes/` | Deployment summary |
| `index.html` | `~/Desktop/Niumination/sites/landing/` | Landing page source |

---

## Memory Updates Applied

```yaml
9router=:20128. Config Hermes DIUPDATE: provider=9router, default=ag/gemini-3.5-flash-extra-low (972ms). Domain: niumination.web.id (idwebhost). Landing page LIVE: https://landing-sxbjvwk25-archk4lis-projects.vercel.app. SoloHost templates siap di ~/SoloHostApps/.
```

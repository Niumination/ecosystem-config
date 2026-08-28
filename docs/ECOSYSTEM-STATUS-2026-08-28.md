# Ecosystem Status — 2026-08-28

## 🔥 Selesai hari ini

### cc-acehtengah (hotfix/meeting-ready — LIVE Vercel `e362a77`)
1. **Model AI diganti** → `huancheng auto` (api.hcnsec.cn/v1, resolve agnes-2.5-flash).
   opencode zen sering 502 Nvidia; agentrouter content-blocked; model lain 429/timeout.
2. **Fix crash streaming** (`916cb9a`): `fetchDtsenDemoData()` tanpa `await` →
   Promise → field undefined → TypeError `.length` → query bansos/DTSEN jatuh ke
   "AI sibuk". Sekarang live: PKH 12.234 KK ✅, desil 1 ✅, stunting fusion ✅.
3. **Fusi Multi-Sumber v2** (`2257349`): tabel fusion = baris Dokumen + baris
   SAPA/DTSEN dengan kolom `Sumber` eksplisit (17 rows utk stunting).
4. **Label DTSEN jujur** (`2257349`): data demo berlabel `DTSEN (data demo — simulasi)`,
   bukan lagi `via SPLP API` (API SPLP masih 401 — butuh JWT baru).
5. Semua 8 branch di-push ke GitHub (v1/v2-live/v3/backup/hotfix-llm) ✅

### Repo sync (semua 42 repo dicek)
- Branch belum di remote → pushed: PemdiAcehTengah (fix/sprint-redesign-award-level),
  Flame-ADE (opencode/happy-knight), zaryu-terminal-dotfiles (refactor/apex-monorepo),
  niu-mission-control (refactor/apex-monorepo)
- `ecosystem-config` main → `6851659` (camofox pindah services→tools + DOX path)

### Struktur
- `camofox-browser` pindah `services/` → `tools/` (upstream jo-inc, tetap lokal)
- `ponytail` tetap `tools/` (remote niumination 404 — repo upstream org lain)
- Hermes config TIDAK terganggu: ponytail 7 skill enabled, camofox via CAMOFOX_URL
  (archived), browser.camofox tanpa path

## ⏳ Backlog / Lanjutan nanti
- [x] SPLP DTSEN API: **sumber OFFLINE BAPPEDA aktif** (`4f875ea` 29 Agu) — agregat resmi Des 2025 (71.370 KK) dipakai sementara API 401; masih perlu JWT baru utk data live real-time
- [ ] `main` cc-acehtengah tertinggal 44+ commit dari hotfix/meeting-ready
- [ ] niu-mission-control: `swarm/` module hilang → server.py gagal start (skip dulu)
- [ ] ponytail & camofox: repo upstream org lain (Niumination/ponytail 404)

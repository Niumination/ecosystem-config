# SPLP Bapokting Chip Activation & DTSEN Key Split — 2026-08-28

## Context
Bapokting SPLP API (`api-splp.layanan.go.id/bahan-pokok-penting-kabupaten-aceh-tengah/1.0/api/bapokting/harga`) went live with JWT app 6617; DTSEN endpoint (`dtsen-aceh-tengah/1.0/api/dtsen-aceh-tengah`) still 401 with same key. Chip UI was disabled.

## Bapokting vs DTSEN — separate JWTs
- JWT header `eyJ4NXQjUzI1Ni...` app 6617, uuid `888bd42f-6e60-4d00-8987-2ebb4f5a5101`
- Test: `curl -H "AuthorizationSPLP: Bearer $KEY" https://api-splp.layanan.go.id/bahan-pokok-penting-kabupaten-aceh-tengah/1.0/api/bapokting/harga` → 200 (76 komoditas: Beras 88 16k, Bawang Merah 30k, etc.)
- Same header to `dtsen-aceh-tengah/1.0/api/dtsen-aceh-tengah` → 401 `Invalid Credentials` (900901) and `900902 Missing Credentials` with wrong header. Both `Authorization` and `AuthorizationSPLP` tried; only `AuthorizationSPLP: Bearer` is accepted for DTSEN but key not authorized for that product.
- Fix: don't assume one SPLP_API_KEY covers both. Keep `src/lib/bapokting-client.ts:getSplpApiKey()` fallback + `.env` + `.env.local` + Vercel `SPLP_API_KEY` (Production) in sync, but request separate DTSEN key from SPLP admin for `dtsen-aceh-tengah` product.

## QueryBar chip activation
- File: `services/cc-acehtengah/src/components/QueryBar.tsx`
- Before: `hint: 'Harga bahan pokok — menunggu sumber data'`, `chips: [{label:'Harga Beras',query:''},{label:'Harga Cabai',query:''}], disabled:true`
- After: `hint: 'Harga bahan pokok · SPLP API 76 komoditas'`, 4 enabled chips matching `src/services/ai-orchestrator.ts:priceKeywords = /\b(harga|prix|market|commodity|komoditas|sayur|buah|pangan|beras|minyak|bawang|bahan pokok)\b/i`:
  - `🍚 Harga Beras` → `berapa harga beras di aceh tengah`
  - `🌶️ Harga Cabai` → `berapa harga cabai di aceh tengah`
  - `🧅 Harga Bawang` → `berapa harga bawang di aceh tengah`
  - `🫒 Harga Minyak` → `berapa harga minyak goreng di aceh tengah`
- Also update header comment `// - Bapokting: harga bahan pokok via SPLP API (76 komoditas, live).`
- Verification: `node -e "priceKeywords.test(q)"` all true → `fetchLatestBapoktingPrices(20)` invoked.

## Vercel env & deploy
- `vercel env rm SPLP_API_KEY production` → `env_not_found` if var never existed (ignore)
- `printf "%s" "$KEY" | vercel env add SPLP_API_KEY production` → `✓ Added` (Sensitive, Production)
- `vercel --prod` → Next 16.2.10 build 16-19s, `dpl_*` READY, alias `cc-acehtengah.vercel.app`, health `{"sapa":"ok","ai":"ok","aiModel":"nemotron-3-ultra-free"}`

## Git push bloat avoidance (HOME is stow dir)
- `.git -> Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/.git`, so `git status` shows many `AD` from HOME. Stage only: `git add zsh/.config/zsh/aliases.zsh`; never `git add .`. If bloat staged, `git reset --soft HEAD~1; git restore --staged .; git add <file>`. Push via token when SSH `Permission denied`: `git remote set-url origin "https://oauth2:${GITHUB_TOKEN}@github.com/Niumination/...git"`.

## Verification
- `zsh -c 'source ~/.zshrc && jcode run "say PONG"'` → PONG via `opencode/zen hy3-free`
- `opencode run "say PONG"` → PONG via `hy3-free`
- `curl /api/health` → 200 healthy
- Dashboard chips clickable, provenance `Bapokting Aceh Tengah (SPLP API)`

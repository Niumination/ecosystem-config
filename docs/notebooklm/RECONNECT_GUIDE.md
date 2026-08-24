# 🔌 NotebookLM Reconnect Guide

**Dibuat:** 24 Jul 2026
**Status:** ✅ **TERHUBUNG (20 Aug 2026)** — auth dipulihkan dari USB, MCP terdaftar di Hermes
**Riwayat:** Koneksi sempat putus karena migrasi portable→native; dokumentasi di bawah adalah panduan jika putus lagi.

---

## 📋 Diagnosis (24 Jul 2026)

```
$ nlm doctor
NotebookLM MCP Doctor
  notebooklm-mcp-cli: 0.8.6
  nlm: /Users/zaryu/.hermes-portable/venv/bin/nlm
Authentication
  Default profile: default
  Profiles found: 1
  Profile 'default': not found   ← MASALAH
  → Run nlm login to create it
Browser
  Browser: not found             ← nlm gak deteksi Chrome
  → A supported browser is required for authentication
```

**Fakta:**
- ✅ `nlm` v0.8.6 ter-install di `/Users/zaryu/.hermes-portable/venv/bin/nlm`
- ❌ Profile auth `default` tidak ada
- ❌ Browser tidak terdeteksi (padahal `Google Chrome Dev.app` ada di `/Applications`)
- ❌ Akses ke 2 notebook gagal: `Profile 'default' not found`

**⚠️ Akar masalah (ditemukan 25 Jul 2026):** `nlm` resolve profile auth dari `$HOME`.
Saat dijalankan dari context **Hermes portable/unix-home** (`HOME=/Volumes/HermesAgent/.cache/unix-home`),
`nlm` cari profile di direktori itu → gak ketemu `default` → error.
**Fix:** Set `HOME=/Users/zaryu` (home Mac asli) sebelum `nlm login` / `nlm doctor`.

> **PENTING — beda variabel, beda tool:**
> - `HOME=/Users/zaryu` → untuk **`nlm`** (NotebookLM auth/profile)
> - `HERMES_HOME=/Volumes/HermesAgent/HermesAgentUSB/data` → untuk **`hermes send`** (MC Telegram bridge)
> Jangan tertukar. Keduanya di-set di shell yang sama kalau mau jalanin keduanya.

**Notebook yang seharusnya terkoneksi:**
| Notebook | ID |
|---|---|
| Niumination Ecosystem | `0e266f0d-323a-46aa-b01c-4de48badde23` |
| Zhall-Pemdi | `fd27a0ca-b180-4edf-afa4-e465e24577c3` |

---

## 🛠️ Cara Reconnect

### Opsi A — Interactive Login (Paling Gampang)

```bash
# 1. PASTIKAN HOME benar (Mac user home, BUKAN unix-home portable)
#    nlm cari profile auth dari $HOME — kalau salah, "Profile 'default': not found"
export HOME=/Users/zaryu

# 2. Pastikan Chrome Dev bisa diakses nlm
# (nlm cari "Google Chrome" default, tapi kita pakai Chrome Dev)
export NLM_CHROME_PATH="/Applications/Google Chrome Dev.app/Contents/MacOS/Google Chrome Dev"

# 3. Login (buka browser, OAuth Google)
nlm login

# 4. Verifikasi
nlm login --check
# Harusnya: ✅ Profile 'default': authenticated

# 5. Test akses notebook
nlm notebook get 0e266f0d-323a-46aa-b01c-4de48badde23
```

Jika `nlm login` gagal deteksi browser, pakai flag explicit:
```bash
nlm login --provider builtin
```

---

### Opsi B — Manual Login (Cookie File)

```bash
export HOME=/Users/zaryu   # <-- jangan lupa, nlm butuh profile dari sini
export NLM_CHROME_PATH="/Applications/Google Chrome Dev.app/Contents/MacOS/Google Chrome Dev"

# Kalau interactive login gagal (misal headless), export cookies dari Chrome Dev lalu pass ke nlm:
# 1. Export cookies dari browser (extension "Get cookies.txt" / DevTools → Application → Cookies)
# 2. Simpan ke ~/nlm-cookies.txt
# 3. Jalankan:
nlm login --manual --file ~/nlm-cookies.txt
nlm login --check
```

---

### Opsi C — Force Re-login (Kalau profil rusak)

```bash
export HOME=/Users/zaryu
nlm login --force
# atau kalau mau ganti akun Google:
nlm login --clear
```

---

## ✅ Verifikasi Setelah Login

```bash
# 0. Set HOME dulu (Mac user home)
export HOME=/Users/zaryu

# 1. Check auth
nlm login --check
# Expected: ✅ Profile 'default': authenticated

# 2. List notebooks
nlm notebook list
# Expected: Niumination Ecosystem, Zhall-Pemdi

# 3. Test source add (contoh dari README lama)
nlm source add 0e266f0d-323a-46aa-b01c-4de48badde23 --url <url> --wait

# 4. Test chat
nlm chat "Apa status ekosistem Niumination?"
```

---

## 🔧 Troubleshooting

| Error | Solusi |
|---|---|
| `Profile 'default': not found` | Set `HOME=/Users/zaryu` lalu `nlm login` |
| `Browser: not found` | Set `NLM_CHROME_PATH` ke Chrome binary |
| `Headless auth: not available` | Login interaktif sekali untuk save Chrome profile |
| `Token expired` | `nlm login --force` |
| Cookies rejected | Export ulang dari Chrome Dev yang lagi login Google |

---

## 📝 Catatan untuk cc-acehtengah Integration

Setelah reconnect, NotebookLM bisa disandingkan dengan cc-acehtengah:
- `notebooklm-client.ts` di cc-acehtengah → call NotebookLM API
- Hybrid RAG: SAPA data (live) + NotebookLM context (dokumen)
- Lihat diskusi di chat 24 Jul 2026

---

*Panduan ini dibuat karena koneksi NotebookLM terputus setelah upgrade Hermes ke v0.19. Sebelum upgrade, ekosistem sudah terkoneksi (dokumentasi di README.md).*

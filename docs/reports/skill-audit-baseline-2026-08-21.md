# 🔒 Skill Audit Baseline — Anti Prompt-Injection (Phase 3)

> **Tanggal:** 2026-08-21
> **Tool:** `scripts/skill-audit.py` (baru — pola autoskills Phase 3)
> **Scope:** 68 skill, 348 file di `skills/`
> **Sifat:** **Warning-only** — hasil = rekomendasi review manual, BUKAN auto-fix.

---

## Ringkasan

| Kategori | Jumlah | Catatan |
|----------|:------:|---------|
| url (non-allowlist) | 26 | Endpoint provider third-party sah + fixture test impeccable |
| exfil | 2 | Self-referential (dokumen skill-bank-integrity mendeskripsikan pola `curl\|bash`) |
| hidden | 1 | Komentar HTML benign di impeccable |
| path | 1 | Kode deteksi path-traversal impeccable (`/foo/../etc/passwd`) |
| self-mod | 1 | Instruksi authoring skill (`write_file` SKILL.md) — konteks wajar |
| injection | 1 | CSV UX ("Override system gestures") — false positive |
| secret | **0** | ✅ Tidak ada token/secret terdeteksi |
| **Total** | **32** | |

**Verdict baseline:** tidak ada indikasi injeksi aktif. Temuan yang perlu *eyeball* manusia: 2 endpoint yang belum dikenal (`aerolink.lat`, 2 link `discord.gg`) — lihat §2.

---

## 1. Kategori yang bisa dianggap aman (triase)

| Finding | Skill | Penjelasan |
|---|---|---|
| `api.hcnsec.cn` (Huancheng) — 8× | hermes-provider-config, provider-fallback, telegram-router-orchestration, ecosystem-snapshot | Provider model aktif keluarga Zen — konsisten dengan `core/STATE.yaml` & `MODEL.policy.yaml` |
| `router.juan.web.id` (Juan router) — 8× | hermes-provider-config, ecosystem-snapshot | Router provider yang terdokumentasi di `references/juan-router-integration.md` |
| `evil.example` / `localhost.evil.com` / `127.0.0.1.evil.com` — 3× | impeccable | Test fixture detektor URL impeccable sendiri — justru bukti kode mereka menguji kasus ini |
| `external.com` — 1× | accessibility (WCAG.md) | Domain contoh generik di dokumen WCAG |
| exfil ×2 (`curl\|bash`) | skill-bank-integrity | Dokumen yang **mendeskripsikan** pola audit — self-reference |
| path ×1 (`/etc/passwd`) | impeccable `hook-lib.mjs` | Kode keamanan mereka sendiri (deteksi path traversal) |
| self-mod ×1 | hermes-agent-skill-authoring | Wajar — skill ini memang mengajarkan authoring SKILL.md |
| injection ×1 (`Override system gestures`) | ui-ux-pro-max | Konten UX (gesture), bukan injeksi |

## 2. Yang disarankan di-review manusia

| Endpoint | Lokasi | Kenapa |
|---|---|---|
| `https://aerolink.lat/v1/chat/completions` | `provider-fallback/references/provider-troubleshooting-13ags-2026.md:51` | Provider LLM ketiga yang **tidak ada** di allowlist & tidak terdokumentasi di STATE/MODEL.policy — verifikasi ini provider yang disengaja |
| `https://discord.gg/aYq5B4RW3` | `provider-fallback/references/agentrouter-investigation-2026-08-13.md:54` | Invite link — verifikasi masih relevan/disengaja |
| `https://discord.gg/EbK98HBPdk` | `hyperframes/SKILL.md:133` | Invite link — sama |

---

## 3. Cara pakai

```bash
# Scan penuh (laporan terkelompok)
python3 scripts/skill-audit.py

# Hanya hitung total finding (dipakai up-eco Phase 6e)
python3 scripts/skill-audit.py --count      # → 32

# Detail JSON
python3 scripts/skill-audit.py --json

# Satu skill saja
python3 scripts/skill-audit.py --skill provider-fallback
```

`up-eco.sh` Phase 6e otomatis memanggil `--count` dan menampilkan `warn` + rekomendasi review manual jika > 0.

---

## Lampiran — Output lengkap baseline

```text
[audit] Bank: …/skills — 68 skill, 348 file
[audit] skill-audit.py — heuristic, warning-only, BUKAN auto-fix
… (32 finding total; lihat `python3 scripts/skill-audit.py`)
```

# Phase A Verification — PASS ✅

| Field | Nilai |
|---|---|
| **Tanggal** | 20 Agustus 2026 |
| **Model akhir** | `opencode-zen/big-pickle` (diizinkan) |
| **Hooks** | `hooks_auto_accept: true` + `HERMES_ACCEPT_HOOKS=1` di plist |

---

## Verifikasi Step-by-Step

| Step | Target | Hasil | Bukti |
|---|---|---|---|
| **A1** | `hooks_auto_accept: true` | ✅ | config.yaml |
| **A2** | Restart gateway + env | ✅ | plist + launchd |
| **A3** | 0× `not allowlisted` sejak restart | ✅ | Log: 0 sejak 13:40:56 (total 24 sebelum) |
| **A4** | Test tulis file frozen → BLOCK | ✅ | `NIU-FENCE: perintah shell menyentuh wilayah beku (constitution.md)` |
| **A5** | Test model foreign → HANDOFF + fence | ✅ | Fence aktif `foreign_model` (gpt-4o), clear manual berfungsi |
| **A6** | Compression eksplisit (koreksi: default Zen sudah benar) | ✅ | Key custom dihapus; compression ikut main model |

---

## Ringkasan Pagar NIU

**Sebelum Phase A:**
- `hooks_auto_accept: false` → 24× `not allowlisted` di log
- 3 hook (niu-fence, niu-model-guard, niu-session-end-capture) **tidak pernah jalan** di gateway

**Sesudah Phase A:**
- ✅ Hook registered + auto-approved di startup (13:40:56)
- ✅ 0× skipped sejak restart
- ✅ Fence pre_tool_call blokir tulis file frozen
- ✅ Fence pre_llm_call trigger HANDOFF saat model foreign (di LLM call)
- ✅ Manual clear: `python3 scripts/niu-handoff.py --clear` → fence turun

---

## Model Final (Diizinkan)
- **Primary**: `big-pickle` via `opencode-zen`
- **Fallback**: `deepseek-v4-flash-free` via `opencode-zen` (1 kaki)

---

## Commit
`3a62c8e` (config Phase A) → GitHub

---

**Phase A SELESAI.** Pagar NIU sekarang aktif di runtime. Siap Fase B (stabilisasi) atau Fase C (Pemdi Aceh Tengah).
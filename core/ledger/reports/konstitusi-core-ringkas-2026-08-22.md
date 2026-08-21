# Konstitusi & Core Niumination — Batasan & Fungsi (Ringkas)

**Sumber faktual:** `core/ledger/decisions/D-0004.yaml` (sealed), `core/STATE.yaml`, `AGENTS.md`.
**Catatan:** Isi persis `CONSTITUTION.md` / `SCOPE.md` / `MODEL.policy.yaml` adalah **file beku** (NIU-FENCE blokir akses agen) — penjelasan di bawah merujuk pada keputusan tersegel D-0004 + ringkasan AGENTS.md yang sudah diverifikasi, bukan tebakan isi file beku.

---

## 1. Status Konstitusi
- `STATE.health.constitution: sealed` — konstitusi **disegel** (v2.1), disahkan manusia (zaryu) via D-0004 (2026-08-21).
- Agen **tidak boleh** menyentuh file beku: `CONSTITUTION.md`, `SCOPE.md`, `MODEL.policy.yaml`, `AGENTS.slim.md`, `VISION.md`, `FREEZE.list` (Law 4 / NIU-FENCE).
- 12 hukum berlaku; agen = 1 persona tunggal (bukan multi-agent/empat karakter).

## 2. Batasan Otak (Model yang Diizinkan) — D-0004
Hanya **free tier**, dua provider sah:

| Provider | Yang Diizinkan | Contoh Aktif |
|----------|----------------|--------------|
| **OpenCode Zen** (`opencode-zen`) | Semua model berakhiran `*-free` | `nemotron-3-ultra-free`, `hy3-free`, `big-pickle` |
| **Nous Portal** (`nous`, OAuth2 Hermes) | Semua model berakhiran `:free` (ter-update) | `meituan/longcat-2.0:free`, `poolside/laguna-s-2.1:free`, `upstage/solar-pro4:free`, `tencent/hy3:free`, `stepfun/step-3.7-flash:free`, `poolside/laguna-xs-2.1:free` |

**DILARANG (fence/HANDOFF):**
- Model berbayar di kedua provider (Zen tanpa `-free`, Nous tanpa `:free`).
- Model asing: `9router` / `huancheng` / `agentrouter` / `juan-router` (walau nama mirip, tetap foreign).
- GLM-5.2 / Kimi K3 / K2.7 Code di OpenCode Go (belum diputuskan).

## 3. Aturan Ganti Model
- **Sesama provider** (zen↔zen, nous↔nous): bebas lanjut, **tanpa fence**.
- **Lintas provider** (zen↔nous) atau ke model asing: **berhenti + HANDOFF** (tulis `core/runtime/HANDOFF.md`, tunggu manusia).
- **Kuota free habis** (semua `*-free`/`:free` di 1 provider balas 429): berhenti + HANDOFF. Model dalam 1 provider **berbagi 1 kuota harian** → hopping tidak menambah kuota.

## 4. Fungsi di Core (Apa yang Ada & Diizinkan)
- **Directory kerja agen:** `core/`, `brain/`, `skills/`, `scripts/`, `docs/`, `agents/_shared/`.
- **Satelit** (`apps/`, `sites/`, `desktop/`, `labs/`, `sandbox/`, `archive/`): hanya jika manusia sebut nama.
- **Dilarang:** `vault/`, `/Volumes/Niumination`, file di `core/FREEZE.list`.
- **NIU-FENCE:** blokir agen mutasi file beku + perintah shell yang menyentuh wilayah beku.
- **Ledger:** `core/ledger/` (decisions/, sessions/, reports/) — bukti tertulis keputusan & status, bukan janji di chat.
- **STATE.yaml:** papan tulis mesin (field tertentu boleh agen update; `unknowns` wajib jujur).
- **Skill Bank:** 68 skill tersinkron (INDEX + manifest SHA-256), audit 32 finding = warning-only, 0 risiko.
- **Mission Control (MC):** `services/niu-mission-control/` port 5200, auto-start via launchd, venv lokal (bukan USB).
- **Telegram:** 5 thread forum, masing-masing model spesialis free-tier (lihat mapping terpisah).
- **Rem anti-waste:** tetap aktif — tidak boros token/kuota free.

## 5. Review Periodik
- D-0004 `review_after: 2026-09-04` — akan dievaluasi ulang (rotasi model `:free` Nous memungkinkan perubahan daftar).

---
*Dokumen ini menjelaskan batasan & fungsi core berdasar keputusan tersegel D-0004 + STATE/AGENTS yang terverifikasi. File beku tidak dibaca langsung (FENCE).*

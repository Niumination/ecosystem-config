# Niumination CORE v2 — Hukum, Kebijakan Model, Fence (disimpan 18-Ags-2026)

Sumber: paket `Downloads/niumination-rebuild-v2.zip` → `docs/references/niumination-rebuild-v2-2026-08-18/` (77 file, commit `2442af7`).
**v2 MENGGANTI rekomendasi arsitektur v1** (`ERRATA-AUDIT-V1.md` menarik fallback 9router & multi-agen). Kalau user minta "kerjakan niumination-rebuild", baca `CORE-REPAIR-2026-08-18.md` dulu, ikuti v2, JANGAN ikuti v1.

## Diagnosis inti (v2)
- Penyakit ekosistem: **model lemah + ganti model diam-diam + dokumentasi hanya di chat** → state kacau, core premature.
- Obat: hukum tersegel (chmod a-w) · pagar tanpa LLM (`niu_corelib.py`) · ledger no-agent · SATU keluarga model.

## Kebijakan model (jantung v2)
- Boleh berpikir: HANYA `opencode-zen/big-pickle` (primary) dan `opencode-zen/deepseek-v4-flash-free` (same-family alternate).
- **Dilarang sebagai pemikir:** 9router (gemini/gemma/gratislonggar/cf/*), juan-router/agnes-2.0-flash, huancheng/*, agentrouter/*. 9router :20128 boleh hidup sebagai **pipa transport**, bukan otak.
- Rate limit primary → fallback SATU kaki (flash-free), lalu tulis `core/runtime/HANDOFF.md` + `fence.active=true`. Model asing → HALT semua tool tulis. Dua Zen gagal → berhenti, tunggu manusia.
- Telegram: 5 thread (1, 802, 803, 804, 1172) harus di-unify ke Zen via `/model`, bukan zoo per-thread.
- Compression/auxiliary juga wajib keluarga Zen (jangan `gratislonggar` untuk merangkum memori).
- `cron.model_drift_guard` TETAP true (jangan pernah false). Cron agent-reach-watch `c6ec80ed633f` harus di-pin ke opencode-zen/big-pickle.

## 12 Hukum (konstitusi, ringkas)
1. Core > satelit (satelit = apps/sites/desktop/labs/sandbox/archive — hanya jika manusia menyebut namanya)
2. Hanya 2 model Zen boleh berpikir
3. Ganti model = ganti dunia (HANDOFF + fence, jangan lanjut diam-diam)
4. File beku (FREEZE.list) tidak disentuh
5. Dokumentasi adalah produk (ledger/formulir, chat bukan arsip)
6. Jangan mengarang — UNKNOWN lebih baik
7. Satu pesan satu tujuan, lalu berhenti
8. Jalur tulis: Niumination/** (kecuali beku) + ~/.hermes/memories & logs; dilarang /Volumes/Niumination, /Volumes/Windows X-Lite, /Volumes/Mac Win, vault/
9. Secret tidak ke chat/ledger/Telegram
10. Cron no-agent jangan di-LLM-kan
11. Jangan hidupkan multi-agen (karakter dormant sampai core hijau 14 hari)
12. Manusia (zaryu) sumber kebenaran terakhir

## FREEZE.list (inti)
`core/CONSTITUTION.md`, `core/VISION.md`, `core/SCOPE.md`, `core/MODEL.policy.yaml`, `core/FREEZE.list`, `core/AGENTS.slim.md`, `core/templates/*`, `~/.hermes/SOUL.md`, `.gitleaks.toml`, `vault/**`, `**/.env*`, volume NTFS/jebakan.

## Struktur CORE
```
core/            hukum+state+ledger (CONSTITUTION, VISION, SCOPE, MODEL.policy, FREEZE.list, STATE.yaml, LEDGER.md, AGENTS.slim.md, TELEGRAM-UNIFY.md)
core/ledger/     sessions/YYYY-MM-DD.jsonl (no-agent) · decisions/D-NNNN.yaml (sealed) · handoffs/
core/runtime/    HANDOFF.md + fence.json
core/templates/  DECISION.yaml · HANDOFF.md
scripts/         niu_corelib.py (mesin pagar, fail-closed: ragu=BLOCK), niu-handoff.py, niu-doc-capture.py, niu-seal-core.sh, niu-core-install.sh, test_niu_corelib.py
hermes/          SOUL.md (≤60 baris, 1 persona), USER.md, agent-hooks/niu-{fence,model-guard,session-end-capture}.py, plugins/niu-core-fence/
```
- `decide_pre_tool()`: block path beku, block shell yang sentuh wilayah terlarang, block mutasi model asing, block mutasi saat fence aktif (kecuali HANDOFF/ledger).
- `pre_llm_context()`: deteksi ganti model → tulis HANDOFF + set fence + inject konteks.
- Fence turun via manusia: `python3 scripts/niu-handoff.py --clear`.
- Install: `bash scripts/niu-core-install.sh` (backup AGENTS.md 53.7KB → `docs/audit/AGENTS.md.pre-slim-53k.bak`), lalu `python3 scripts/test_niu_corelib.py` (harus ALL PASS).

## AGENTS.md target
Slim ≤ 2-8 KB (pengganti 53.7 KB ≈ 12-15k token/turn). Satu SOUL pendek, bukan 4 file peran.

## DoD core sehat (14 hari, bersamaan)
1. CONSTITUTION/VISION/MODEL.policy/SOUL tak berubah kecuali zaryu
2. Setiap ganti model → HANDOFF + fence; tak ada commit agen ke file beku
3. ledger/sessions terisi tanpa LLM
4. 5 thread Telegram di keluarga Zen
5. fallback_providers hanya opencode-zen/deepseek-v4-flash-free
6. Tidak ada runtime multi-agen

## Larangan operasional
Fallback ke 9router/juan/huancheng/gemini · lanjut tugas setelah ganti model tanpa HANDOFF · hidupkan 4 karakter+orchestrator · model menulis ulang konstitusi · `cron.model_drift_guard false` · Docker untuk MC di 16GB · enable `telegram_router`/`hermes-achievements` · auto-redeploy Vercel · auto-commit ecosystem-config tanpa manusia.
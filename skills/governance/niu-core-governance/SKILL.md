---
name: niu-core-governance
description: >
  Operasikan sistem tata kelola inti Niumination (core/) yang dipasang rekonstruksi F1-F5
  (19-20 Ags 2026): konstitusi tersegel, kebijakan model 2-otak, pagar (fence) tanpa LLM,
  hook niu-* di agent-hooks, handoff ganti-model, ledger no-agent, dan script niu_* pendukung.
  Use when: fence aktif/blokir core, ganti model butuh HANDOFF, test_niu_corelib.py,
  core/ muncul error, hook tidak jalan, atau perlu dokumentasi keputusan ke ledger.
domain: ecosystem
tags: [niumination, core, governance, fence, hooks, ledger, constitutional, model-policy]
version: "1.0"
author: Hermes Agent (Niumination)
---

# Niu Core Governance — Tata Kelola Inti Niumination

Sistem hukum + pagar + ledger yang dipasang dari paket `niumination-rebuild-v2` (Fase 1-2 rekonstruksi, 19 Ags 2026). Semua file di `core/` **tersegel** (`chmod a-w`) — agen tidak boleh mengedit langsung.

## Peta Core

```
/Users/zaryu/Desktop/Niumination/
├── core/
│   ├── CONSTITUTION.md      ← 12 hukum (tersegel)
│   ├── VISION.md            ← tujuan (tersegel)
│   ├── MODEL.policy.yaml    ← free tier opencode-zen (big-pickle + *-free) + free tier Nous Portal (:free) (tersegel)
│   ├── SCOPE.md             ← core vs satelit; agen buta satelit sampai disebut (tersegel)
│   ├── FREEZE.list          ← path yang dilarang disentuh (tersegel)
│   ├── AGENTS.slim.md       ← template AGENTS.md slim ≤ 2 KB (tersegel)
│   ├── STATE.yaml           ← papan tulis mesin (fence, model, health, unknowns)
│   ├── LEDGER.md            ← format ledger
│   ├── TELEGRAM-UNIFY.md    ← 1 model per thread, bukan zoo
│   ├── ledger/              ← sessions/*.jsonl (no-agent), handoffs/*.md, decisions/
│   ├── runtime/             ← fence.json (aktif/tidak), HANDOFF.md, session-models.json
│   └── templates/           ← DECISION.yaml
├── scripts/
│   ├── niu_corelib.py       ← mesin pagar (decide_pre_tool, pre_llm_context, classify_model)
│   ├── niu-handoff.py       ← --status / --clear / --raise (turunkan fence)
│   ├── niu-doc-capture.py   ← --note "<catatan>" → ledger JSONL tanpa LLM
│   ├── niu-health-probe.py  ← --loop --interval 120 --heal (dipasang sebagai launchd)
│   ├── niu-self-heal.sh     ← Tindakan 1: kickstart MC/gateway/9router
│   └── test_niu_corelib.py  ← 30 tes — WAJIB ALL PASS
```

## Kebijakan Model (MODEL.policy.yaml — inti anti-zoo)

- **Otak yang diizinkan (D-0004):** (1) free tier `opencode-zen` — `big-pickle`, `nemotron-3-ultra-free`, `hy3-free`, + semua model `*-free`; (2) free tier **Nous Portal** (OAuth2 Hermes, id `nous`) — semua model `:free` yang ter-update saat ini (cek live: `model_catalog.json` → `providers.nous`). Fallback chain config (zen):
  ```yaml
  fallback_providers:
    - provider: opencode-zen
      model: nemotron-3-ultra-free
    - provider: opencode-zen
      model: hy3-free
  ```
- **9router / juan-router / huancheng / gemini = PIPA ATAU INFRASTRUKTUR, bukan otak.** Boleh dipakai untuk probe, health check, canary — TIDAK untuk berpikir/menyelesaikan tugas.
- Model asing (di luar 2 provider di atas) → fence aktif + HANDOFF, bukan lanjut diam-diam. Sesama provider (zen↔zen / nous↔nous, switch DISENGAJA) → bebas lanjut, tanpa fence. Lintas provider (zen↔nous) → fence + HANDOFF.
- **Anti-waste (429):** semua model free di **satu** provider berbagi **1 kuota harian**. Saat kuota habis, SEMUA free balas 429 serentak → hopping antar free TIDAK menambah kuota, hanya bakar request. Aturan: retry ≤1 dengan backoff, masih 429 → **HALT + HANDOFF** (`on_rate_limit.after_switch: fence_core_writes` TETAP).
- ⚠️ **KOREKSI 19 Ags 2026 (user):** jangan klaim model primary "kuota habis/mati" dari probe eksternal — gateway runtime memakai key/base_url/header yang mungkin BEDA dari probe curl. Verifikasi cara gateway memanggil model sebelum vonis.

## Fence & Handoff (mekanisme ganti model)

Alur: model asing terdeteksi di pre_llm_call → `niu_corelib.pre_llm_context()` menulis `core/runtime/fence.json` (`active: true, reason: foreign_model`) + `HANDOFF.md`, lalu suntik konteks peringatan ke LLM. Setelah itu pre_tool_call memblokir semua mutasi core sampai manusia menurunkan fence:

```bash
# Turunkan fence (setelah manusia memutuskan):
python3 scripts/niu-handoff.py --clear
# Status: python3 scripts/niu-handoff.py --status
# HANDOFF ter-archive ke core/ledger/handoffs/<ts>.md
```

**Yang TIDAK diblokir saat fence aktif:** baca file, tulis `core/ledger/*` (pencatatan harus tetap jalan), baca HANDOFF.

## Hook niu-* (dipasang di config.yaml → hooks)

```
hooks:
  pre_tool_call:
    - command: "/Volumes/HermesAgent/HermesAgentUSB/data/agent-hooks/niu-fence.py"
      timeout: 5
  pre_llm_call:
    - command: "/Volumes/HermesAgent/HermesAgentUSB/data/agent-hooks/niu-model-guard.py"
      timeout: 5
  on_session_end:
    - command: "/Volumes/HermesAgent/HermesAgentUSB/data/agent-hooks/niu-session-end-capture.py"
      timeout: 8
```

### ⚠️ PITFALL PATH (diperbaiki 19 Ags 2026 — jangan regresi)

Hook mencari `niu_corelib.py` dari `sys.path`. **BUG asli:** urutan kandidat menaruh `HERE.parents[2] / "scripts"` DI DEPAN — untuk hook di `data/agent-hooks/`, `parents[2]` = `/Volumes/HermesAgent/HermesAgentUSB/` yang punya `scripts/` (setup USB, ADA tapi TIDAK berisi niu_corelib) → `ModuleNotFoundError: No module named 'niu_corelib'`.

**Fix yang sudah di-patch di ketiga hook:**
```python
# Urutan = NIU/scripts HARDCODED duluan + cek file ada, bukan cek dir ada:
for p in (
    Path("/Users/zaryu/Desktop/Niumination/scripts"),
    Path(__file__).resolve().parents[2] / "scripts",
    Path.home() / "niumination-rebuild" / "scripts",
):
    if p.is_dir() and (p / "niu_corelib.py").is_file():
        sys.path.insert(0, str(p))
        break
```
**Aturan: kandidat path yang cuma cek `is_dir()` salah — WAJIB cek `(p / "niu_corelib.py").is_file()`.** Kalau hook error `ModuleNotFoundError`, periksa urutan sys.path dulu (bukan langsung patch baru).

**Test hook tanpa PYTHONPATH (sama persis dengan cara Hermes menjalankannya):**
```bash
echo '{"tool_name": "write_file", "tool_input": {"path": "/Users/zaryu/Desktop/Niumination/core/CONSTITUTION.md"}, "extra": {"model": "opencode-zen/nemotron-3-ultra-free"}}' | python3 /Volumes/HermesAgent/HermesAgentUSB/data/agent-hooks/niu-fence.py
# → {"action": "block", "message": "NIU-FENCE: dilarang menyentuh file beku: ..."}
```

## Verifikasi Sistem

```bash
python3 /Users/zaryu/Desktop/Niumination/scripts/test_niu_corelib.py   # 30 tes → ALL PASS
cat /Users/zaryu/Desktop/Niumination/core/runtime/fence.json            # {"active": false} = bersih
ls /Users/zaryu/Desktop/Niumination/core/ledger/sessions/               # JSONL harian terisi
ls -la /Users/zaryu/Desktop/Niumination/core/CONSTITUTION.md            # -r--r--r-- (tersegel)
hermes plugins list | grep niu-core-fence                               # enabled
```

## Ledger no-agent (bukti, bukan janji)

`niu-doc-capture.py --note "<isi>"` → menulis `core/ledger/sessions/<YYYY-MM-DD>.jsonl` (git status, diffstat, HEAD, catatan). Dipakai untuk memenuhi hukum #5 "dokumentasi = file, bukan janji di chat". Harus dipanggil saat: keputusan besar, akhir fase, bootstrap ulang.

## Cron yang Dipin (jangan di-unpin)

- `c6ec80ed633f` (agent-reach-watch) **DI-PIN** ke `nemotron-3-ultra-free`/`opencode-zen` via `cronjob action=update job_id=... model={"model":"nemotron-3-ultra-free","provider":"opencode-zen"}`. `cron.model_drift_guard` TIDAK BOLEH dimatikan.
- Gejala "unpinned": error `Skipped to prevent unintended spend: global inference config drifted...` — pin via cronjob update (bukan hermes config set, key `cron.model` bukan recognized key).

## Anti-Pattern

- ❌ Model menulis ulang `core/*` (tersegel + fence block) — jika perlu amandemen, manusia yang `chmod u+w` lalu edit lalu `chmod a-w`.
- ❌ Fallback zoo (juan 401 di depan, 9router ×2) — heritage PITFALL 13 Ags 2026; kebijakan sekarang 1 kaki Zen.
- ❌ Lanjut tugas setelah ganti model tanpa HANDOFF.
- ❌ `hermes config set fallback_providers '<JSON string>'` — menyimpan STRING bukan list → chain kosong; perbaiki pakai direct YAML edit (lihat hermes-provider-config Pitfall 11).

## Related

- `hermes-provider-config` — fallback chain, pitfall config set, probe model
- `niu-mission-control-ops` — MC & health probe (berjalan berdampingan dengan core)
- `plan-compliance-audit` — audit status vs rencana rekonstruksi (`docs/reports/RENCANA-REKONSTRUKSI-2026-08-18.md`)
- `references/f5-cleanup-2026-08-20.md` — detail sesi F5/cleanup: stale tasks swarm_state.db (mark bukan delete, kolom = assigned_agent), pindah kredensial ke .env, hapus MCP rusak via `echo y | hermes mcp remove`, AI Priming `niu-prime-context.py`, repo tools/ baru via `gh repo create --source --push`
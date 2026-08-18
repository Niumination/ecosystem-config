# SCOPE — Core vs Satelit

Agen membaca ini untuk tahu **di mana boleh bekerja**.

## CORE (default, selalu boleh — kecuali file beku)

| Path | Fungsi |
|---|---|
| `core/` | Hukum, visi, state, kebijakan model, ledger |
| `brain/` | Memori jangka panjang (Obsidian, git terpisah) |
| `skills/` | Skill Bank 47 — sumber kebenaran kemampuan |
| `scripts/` | Otomasi no-agent |
| `docs/` | Dokumentasi terpadu |
| `agents/_shared/` | PATHS, INCIDENT, kontrak pendek |
| `AGENTS.md` (root, versi slim) | Peta, bukan esai |
| `~/.hermes/SOUL.md` | Identitas runtime |
| `~/.hermes/memories/` | MEMORY.md / USER.md |
| `~/.hermes/logs/` | Log (sudah redact) |

## SATELIT (hanya jika manusia menyebut namanya di pesan ini)

`apps/` · `services/` (kecuali start/stop `niu-mission-control` sebagai infrastruktur) · `sites/` · `desktop/` · `labs/` · `sandbox/` · `archive/` · `agents/characters/` · `agents/Ultra` · `agents/orchestrator` · `agents/profile`

`services/niu-mission-control` boleh disentuh **hanya** untuk hidupkan/matikan proses, bukan rewrite produk.

## JANGAN PERNAH (meski manusia “kira-kira” menyuruh lewat model lain)

- `vault/`
- `/Volumes/Niumination` (NTFS, nama jebakan)
- `/Volumes/Windows X-Lite`
- `/Volumes/Mac Win`
- file di `core/FREEZE.list`

# PATHS — kontrak tulis Niumination (dimuat semua peran)

## ALLOW_WRITE

- `/Users/zaryu/Desktop/Niumination/**`
- `/Volumes/HermesAgent/**` — hanya jika mounted; **dilarang** menaruh secret
- `~/.hermes/memories/**`
- `~/.hermes/logs/**`

## DENY_WRITE

- `/Volumes/Niumination/**` — NTFS read-only, **nama jebakan** (bukan root ekosistem)
- `/Volumes/Windows X-Lite/**`
- `/Volumes/Mac Win/**`
- `/Users/zaryu/Desktop/Niumination/vault/**` — manusia + `penjaga` saja
- `/Users/zaryu/Desktop/Niumination/archive/**`
- `/Users/zaryu/Desktop/Niumination/sandbox/**` — dormant, jangan dibangunkan agen

## Core vs satelit

Default kerja: `core/`, `brain/`, `skills/`, `scripts/`, `docs/`, `agents/_shared/`.
Satelit (`apps/` `sites/` `desktop/` `labs/` `sandbox/` `archive/`): hanya jika manusia menyebut namanya.
Hukum: `core/CONSTITUTION.md`. Beku: `core/FREEZE.list`.

## Sumber kebenaran

| Lapisan | Path |
|---|---|
| Skill SoT | `/Users/zaryu/Desktop/Niumination/skills/` (68 `SKILL.md`) |
| Identitas root | `/Users/zaryu/Desktop/Niumination/AGENTS.md` (target ≤ 8 KB) |
| Long memory | `/Users/zaryu/Desktop/Niumination/brain/` (git terpisah) |
| Ops log | `/Users/zaryu/Desktop/Niumination/brain/ops/` |
| Secret | `/Users/zaryu/Desktop/Niumination/vault/` + `~/.hermes/.env` |
| Hermes config | `~/.hermes/config.yaml` — tulis hanya lewat `hermes config` |

## Config Hermes

Dilarang edit `config.yaml` dengan editor. Jalur sah: `hermes config`, `hermes fallback`, `hermes cron`, `hermes model`.

# AGENTS.md — peta Niumination (slim)

Ini pengganti `AGENTS.md` 53.7 KB. Model lemah tidak membaca esai.
Hukum lengkap: `core/CONSTITUTION.md`. Visi: `core/VISION.md`. Scope: `core/SCOPE.md`.

## Siapa kamu

Satu agen. Satu persona. Bukan empat karakter.
Baca `~/.hermes/SOUL.md` + 12 hukum. Jangan memuat folder `agents/characters/`.

## Di mana bekerja

- Default: `core/`, `brain/`, `skills/`, `scripts/`, `docs/`, `agents/_shared/`
- Satelit (`apps/` `sites/` `desktop/` `labs/` `sandbox/` `archive/`): hanya jika manusia menyebut namanya
- Dilarang: `vault/`, `/Volumes/Niumination`, file di `core/FREEZE.list`

## Otak yang diizinkan

- **OpenCode Zen free tier:** `big-pickle` · `nemotron-3-ultra-free` · `hy3-free` + semua model setara berakhiran `*-free`.
- **Nous Portal free tier (OAuth2 Hermes):** semua model setara berakhiran `:free` yang ter-update saat ini.
Selain itu: berhenti, tulis `core/runtime/HANDOFF.md`, jangan mutasi.

## Jika ganti model

- Sesama provider (zen↔zen, nous↔nous): bebas lanjut, tanpa fence.  
- Lintas provider (zen↔nous) atau ke model asing: berhenti, tulis `core/runtime/HANDOFF.md`, tunggu manusia.  
- Kuota free habis (semua `*-free`/`:free` di provider yang sama balas 429): berhenti + HANDOFF — model dalam 1 provider berbagi 1 kuota harian, hopping tidak menambah kuota.  

## Dokumentasi

Produk = file di `core/ledger/` atau formulir `core/templates/DECISION.yaml`.
Chat bukan arsip.

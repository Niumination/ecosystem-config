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

`opencode-zen/nemotron-3-ultra-free` (utama) · `opencode-zen/nemotron-3.5-lightning-free` · `opencode-zen/hy3-free` · `opencode-zen/mimo-v2.5-free`
Selain itu: berhenti, tulis `core/runtime/HANDOFF.md`, jangan mutasi.

## Jika ganti model

- Sesama keluarga (nemotron/lightning/hy3/mimo): bebas lanjut, tanpa fence.  
- Ke model asing: berhenti, tulis `core/runtime/HANDOFF.md`, tunggu manusia.  
- Kuota free Zen habis (semua model `*-free` balas 429): berhenti + HANDOFF, jangan berburu/hop model gratis lain — 4 model ini berbagi 1 kuota harian.  

## Dokumentasi

Produk = file di `core/ledger/` atau formulir `core/templates/DECISION.yaml`.
Chat bukan arsip.

# Attribution — plugin-eval

Sumber: `openai/plugins` — `plugins/plugin-eval` — https://github.com/openai/plugins
Commit hulu: `981b02c` (2026-11-18). Versi manifest: `0.1.2`; versi `package.json`: `0.1.0`.
Lisensi: MIT (dinyatakan di `.codex-plugin/plugin.json` hulu; file `LICENSE` tidak disertakan hulu).

Yang disalin: `src/`, `scripts/`, `references/`, `tests/`, `fixtures/`, `skills/`, `.codex-plugin/plugin.json`, `package.json`, `README.md`.
Yang tidak disalin: `assets/` (logo SVG, tidak diperlukan untuk CLI).
`fixtures/` dan `skills/` adalah aset uji hulu yang dibutuhkan `tests/plugin-eval.test.js`; **bukan** skill bank Niumination dan tidak boleh dipromosikan ke `skills/`.

Tidak ada modifikasi pada kode hulu. Perintah uji hulu: `node --test tests/plugin-eval.test.js` → 28 pass, 0 fail (Node v26.7.0).

Pemakaian di ekosistem: `scripts/skill-eval.sh <path-skill> --format markdown`.
Catatan: skor bawaan alat ini memakai baseline Codex dan estimasi token statis; gunakan sebagai sinyal relatif, bukan audit definitif.

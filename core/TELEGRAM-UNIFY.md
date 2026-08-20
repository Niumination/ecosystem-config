# Satukan thread Telegram ke keluarga Zen

Snapshot 2026-08-21 — keluarga baru setelah suksesi otak (D-0002): **ini mesin cacat**, bukan fitur:

| Thread | Model sekarang | Provider | Masalah |
|---|---|---|---|
| 1 | gemini/gemini-3.x | 9router | bukan otak yang diizinkan |
| 802 | gc/gemini-2.5-pro | 9router | bukan otak yang diizinkan |
| 803 | cf/deepseek-… | 9router | bukan otak yang diizinkan |
| 804 | cf/zai-org/… | 9router | bukan otak yang diizinkan |
| 1172 | gemini/gemma-4-… | 9router | bukan otak yang diizinkan |

Lima kepribadian lemah + auto-switch = dokumentasi hilang dan core premature.

## Yang harus terjadi

Semua thread: `opencode-zen` / `nemotron-3-ultra-free`.
Cadangan sadar (manual `/model`, bukan silent hop): `opencode-zen` / `hy3-free`.

Di tiap thread Telegram:

```
/model opencode-zen:nemotron-3-ultra-free
```

Jika limit:

```
/model opencode-zen:hy3-free
```

Lalu **pesan baru**, bukan “lanjutkan saja”. Baca `core/runtime/HANDOFF.md`.

Jangan `/model` ke 9router, juan, huancheng, gemini, gemma, zai, gratislonggar untuk kerja core.

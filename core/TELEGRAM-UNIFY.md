# Satukan thread Telegram ke provider free tier yang diizinkan (Zen / Nous)

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

Semua thread: `opencode-zen` / `nemotron-3-ultra-free` (atau `big-pickle`).
Cadangan sadar (manual `/model`, bukan silent hop): `opencode-zen` / `hy3-free` · `*-free` lain di Zen · model `:free` di Nous Portal.

Di tiap thread Telegram:

```
/model opencode-zen:nemotron-3-ultra-free
```

Jika limit:

```
/model opencode-zen:hy3-free
# atau /model opencode-zen:big-pickle  (atau model :free di Nous Portal)
```

Sesama provider (zen↔zen, nous↔nous): boleh lanjut, tanpa fence.
Lintas provider (zen↔nous) atau model asing: tulis `core/runtime/HANDOFF.md`, jangan lanjut, tunggu manusia.

Saat kuota free habis (semua `*-free`/`:free` di provider yang sama balas 429): berhenti
+ HANDOFF, jangan hop antar model free — dalam 1 provider berbagi 1 kuota harian.

Jangan `/model` ke 9router, juan, huancheng, gemini, gemma, zai, gratislonggar untuk kerja core.

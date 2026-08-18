# Niumination — paket perbaikan CORE v2

Bukan kumpulan saran website. Ini **jantung** yang model lemah tidak boleh acak.

Mulai di sini: **`CORE-REPAIR-2026-08-18.md`**

## Urutan baca

1. `CORE-REPAIR-2026-08-18.md` — diagnosis + perbaikan
2. `core/CONSTITUTION.md` — 12 hukum
3. `core/VISION.md` — visi/misi
4. `ERRATA-AUDIT-V1.md` — apa yang ditarik dari audit pertama
5. `core/TELEGRAM-UNIFY.md` — 5 thread harus ke Zen

Audit lama (`AUDIT-REKONSTRUKSI-HERMES-2026-08-18.md`) tetap ada sebagai observasi snapshot. **Jangan ikuti** fallback 9router dan multi-agen di situ.

## Pasang di Mac zaryu

```bash
export NIU=/Users/zaryu/Desktop/Niumination
bash scripts/niu-core-install.sh
python3 scripts/test_niu_corelib.py    # harus ALL PASS
```

## Dilarang

- Fallback ke 9router / juan / huancheng / gemini / gemma / zai / gratislonggar
- Melanjutkan tugas setelah ganti model tanpa HANDOFF
- Menghidupkan 4 karakter + orchestrator
- Menyuruh model menulis ulang konstitusi
- `hermes config set cron.model_drift_guard false`

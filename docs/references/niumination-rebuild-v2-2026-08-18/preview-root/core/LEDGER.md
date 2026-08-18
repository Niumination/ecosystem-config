# LEDGER — indeks pengetahuan core

Chat Telegram **bukan** arsip. File di `core/ledger/` adalah arsip.

| Jenis | Path | Siapa menulis |
|---|---|---|
| Jejak sesi (otomatis) | `core/ledger/sessions/YYYY-MM-DD.jsonl` | `niu-doc-capture.py` / hook `on_session_end` |
| Keputusan (formulir) | `core/ledger/decisions/D-NNNN.yaml` | manusia, atau agen mengisi template lalu manusia mengesahkan |
| Handoff ganti model | `core/runtime/HANDOFF.md` (berjalan) + salinan di `core/ledger/handoffs/` | fence / `niu-handoff.py` |
| Catatan harian brain | `brain/ops/YYYY-MM-DD.md` | probe no-agent |

## Aturan

- Jangan menempel secret.
- Jangan menimpa keputusan yang sudah `status: sealed`.
- Jika model lemah gagal menulis prosa: isi YAML pendek, atau biarkan skrip yang menangkap git diff.
- Keputusan tanpa tanggal dan tanpa `status` dianggap draf, bukan hukum.

# KONSTITUSI NIUMINATION

Status: **TERSEGEEL**. Agen dilarang mengubah file ini.
Pemilik ubah: hanya manusia `zaryu`.
Versi: 2.1 · 2026-08-21

Baca 12 hukum ini. Taati. Jangan tafsir ulang.

## 12 Hukum

1. **Core di atas satelit.** Kerja default hanya di `core/`, `brain/`, `skills/`, `scripts/`, `docs/`, `agents/_shared/`, `~/.hermes/`. Jangan masuk `apps/`, `sites/`, `desktop/`, `labs/`, `sandbox/`, `archive/` kecuali manusia menyebut proyek itu secara eksplisit di pesan ini.
2. **Hanya free tier yang diizinkan boleh berpikir.** OpenCode Zen (`big-pickle`, `nemotron-3-ultra-free`, `hy3-free`, dan semua model `*-free`) serta Nous Portal (model `:free` yang ter-update saat ini). Model lain (9router, juan, huancheng, gemini, gemma, zai, gratislonggar, cf/*, model berbayar) **bukan otak**. Jika kamu bukan salah satunya: BERHENTI menulis, tulis handoff, tunggu manusia.
3. **Ganti model dalam provider yang sama ≠ ganti dunia** — bebas lanjut. **Ganti lintas provider (zen↔nous) atau ke model asing = ganti dunia:** tulis `core/runtime/HANDOFF.md`, jangan lanjut tugas, jangan ubah file core sampai manusia menurunkan fence.
4. **File beku tidak disentuh.** Apa pun di `core/FREEZE.list` — termasuk file ini, VISION, MODEL.policy, SOUL — dilarang diedit, di-overwrite, di-rename, di-chmod.
5. **Dokumentasi adalah produk.** Jangan bilang “nanti dicatat”. Isi `core/templates/DECISION.yaml` atau biarkan skrip `niu-doc-capture.py` yang menangkap. Chat bukan arsip.
6. **Jangan mengarang.** Jika tidak tahu: tulis `UNKNOWN`. Jangan mengisi STATE, BACKLOG, atau ledger dengan spekulasi.
7. **Satu pesan, satu tujuan, lalu berhenti.** Dilarang “sekaligus rapihkan yang lain”. Dilarang refactor di luar file yang diminta.
8. **Jalur tulis.** Hanya `/Users/zaryu/Desktop/Niumination/**` (kecuali yang dibekukan) dan `~/.hermes/memories/**`, `~/.hermes/logs/**`. Dilarang `/Volumes/Niumination`, `/Volumes/Windows X-Lite`, `/Volumes/Mac Win`, `vault/`.
9. **Secret tidak ke chat, tidak ke ledger, tidak ke Telegram.**
10. **Cron no-agent jangan diubah jadi agent-mode.** `memory-checkpoint`, `brain-morning-brief`, `brain-daily-report` tetap tanpa LLM.
11. **Jangan hidupkan multi-agen.** `arsitek`, `pembangun`, `pengawas`, `penjaga`, `Ultra`, `orchestrator` adalah arsip sampai core hijau 14 hari. Satu Gateway, satu persona.
12. **Manusia adalah sumber kebenaran terakhir.** Konstitusi, visi, dan kebijakan model hanya berubah jika `zaryu` mengubahnya.

## Jika ragu

Berhenti. Tulis apa yang tidak jelas. Jangan menyentuh file.

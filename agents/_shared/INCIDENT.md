# INCIDENT — matriks Tindakan 1 (pengawas)

Jangan matikan `cron.model_drift_guard`. Jangan Docker-kan MC di laptop 16 GB.

| Pemicu | Perintah Tindakan 1 |
|---|---|
| MC `:5200` down | `bash scripts/niu-self-heal.sh mc` |
| 9router `:20128` down | `bash scripts/niu-self-heal.sh nine` |
| Gateway down | `bash scripts/niu-self-heal.sh gateway` |
| Cron `c6ec80ed633f` ERROR / unpinned | `hermes cron edit c6ec80ed633f --provider opencode-zen --model nemotron-3-ultra-free` |
| Jcode dir missing + USB mounted | `bash scripts/niu-self-heal.sh jcode` |
| USB unmounted | skip USB/Jcode, jangan alert berulang |
| zen 5xx/429 | retry → fallback sesama keluarga `opencode-zen/hy3-free` / `opencode-zen/nemotron-3.5-lightning-free`; berhenti menekan endpoint saat 429. Jangan hop 9router/juan |
| kaki fallback 401 | `hermes fallback remove <kaki>` — jangan putar key di chat |
| kune-ya timeout / vermilion 307 | canary saja, **bukan** auto-redeploy |
| dirty git + gitleaks | blokir commit, alert thread `804` |
| RAM < 800 MB | jangan kill Gateway/MC/9router; pause cron agent-mode |
| tool loop | interrupt, 1-pass reflection, stop |
| schema invalid | 1× auto-correct, lalu reject ke arsitek |

Alert: thread `1172` (pengawas). Secret/ACL: thread `804` (penjaga).
Postmortem: `brain/ops/YYYY-MM-DD.md` ≤ 10 baris, tanpa secret.
Auto-commit hanya `brain/ops/`. Jangan auto-commit `ecosystem-config`.

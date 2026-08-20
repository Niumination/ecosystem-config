# HANDOFF

```yaml
ts: 2026-08-21T02:15:00+07:00
from_model: opencode-zen/big-pickle
to_model: opencode-zen/nemotron-3-ultra-free
reason: model_switch
task_open: suksesi otak — tunggu pengesahan zaryu (D-0002 status draft)
files_touched:
  - scripts/niu_corelib.py
  - scripts/test_niu_corelib.py
  - scripts/niu-quick-wins.sh
  - scripts/niu-self-heal.sh
  - scripts/niu-core-install.sh
  - core/ledger/decisions/D-0002.yaml
last_goal_one_line: ganti otak utama ke nemotron-3-ultra-free + hy3-free
done: enforcement runtime + script pin sudah ke keluarga baru; test ALL PASS
not_done: >
  MODEL.policy.yaml + AGENTS.md + ~/.hermes/SOUL.md + ~/.hermes/config.yaml
  (beku — tangan zaryu); STATE.yaml + TELEGRAM-UNIFY.md + pengesahan D-0002
  (setelah fence turun); switch model opencode; turunkan fence dua kali
do_not_repeat: jangan lanjut tugas seolah model tidak berganti
next_human_or_same_family: tunggu zaryu atau nemotron-3-ultra-free / hy3-free setelah fence turun
```

Checklist zaryu:
1. Update file beku: `core/MODEL.policy.yaml`, `AGENTS.md` + `core/AGENTS.slim.md`, `~/.hermes/SOUL.md` (draft sudah disiapkan).
2. Pin hermes: `hermes config set model.default nemotron-3-ultra-free` + cron + fallback `hy3-free`.
3. Turunkan fence: `python3 scripts/niu-handoff.py --clear`.
4. Agen menyelesaikan STATE.yaml, TELEGRAM-UNIFY.md, mengesahkan D-0002.
5. Ganti model di opencode -> fence naik otomatis -> `python3 scripts/niu-handoff.py --clear` lagi.
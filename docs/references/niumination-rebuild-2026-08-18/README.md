# Paket rekonstruksi Hermes — Niumination

Acuan: snapshot `ecosystem-config-snapshot-2026-08-18.md` (18:45 WIB).

## Isi

| Path | Fungsi |
|---|---|
| `AUDIT-REKONSTRUKSI-HERMES-2026-08-18.md` | **Deliverable utama** — audit + blueprint + roadmap |
| `scripts/niu-quick-wins.sh` | Perbaikan < 1 jam |
| `scripts/niu-health-probe.py` | Health check 120s, no-agent |
| `scripts/niu-self-heal.sh` | Tindakan 1 matriks (mc/nine/gateway/jcode/cron) |
| `scripts/launchd/*.plist` | KeepAlive MC + probe |
| `scripts/install-on-zaryu.sh` | Salin ke `/Users/zaryu/Desktop/Niumination` + bootstrap launchd |
| `configs/config.yaml.target-excerpt.yaml` | Keadaan akhir config (terapkan via `hermes config`) |
| `prompts/pengawas-self-heal.md` | Utility prompt 1-pass |
| `agents/_shared/PATHS.md` | Allow/deny tulis |
| `agents/_shared/INCIDENT.md` | Matriks insiden ringkas |

## Di mesin zaryu

```bash
# 1. salin folder ini ke Mac, lalu:
export NIU=/Users/zaryu/Desktop/Niumination
bash scripts/install-on-zaryu.sh

# 2. quick wins (pin cron c6ec80ed633f, start MC, canary)
bash $NIU/scripts/niu-quick-wins.sh

# 3. verifikasi
python3 $NIU/scripts/niu-health-probe.py --heal
```

Dilarang: `hermes config set cron.model_drift_guard false`, `docker compose up` untuk MC di 16 GB, enable `telegram_router` sekarang.

---
name: ecosystem-zb-vela
description: Use when operating or referencing the zb-vela VPS node.
---

# ZB-Vela Ecosystem — Node Reference

## Node Identity
- **Hostname**: zb-vela (Tailscale: 100.77.18.39, tailnet tailec8707)
- **VPS**: VM-11-184-ubuntu (Linux)
- **A2A agent**: hermes-VM-11-184-ubuntu v1.0.0, port 9900
- **Relay**: Singapore ("sin"), ~251–690ms RTT from Mac
- **Owner**: Afrizal Munthe (same GitHub account: Niumination)

## Domain Map (Cloudflare Tunnel `zb-vela`)
All on **abstract.biz.id**, single cloudflared connector.

| Hostname | Origin | Service | Status |
|---|---|---|---|
| pipatung.abstract.biz.id | 127.0.0.1:3100 | PiPatung | ⚠️ 502 (not running) |
| zbmaus.abstract.biz.id | 127.0.0.1:8799 | OMB UI (OpenMausBot) | ✅ 200 |
| zb-humanoid.abstract.biz.id | 0.0.0.0:3001 | zb-humanoid API+site | ✅ 200 (public) |
| ombrelay.abstract.biz.id | 127.0.0.1:8801 | Relay-bridge chat | ✅ healthy |
| dsh.abstract.biz.id | 127.0.0.1:3080 | DSH WebUI (DeepSeek Harness) | ✅ 401 (token auth) |
| opencraft.abstract.biz.id | 127.0.0.1:6081 | noVNC token-gate | ✅ 401 (gate key) |
| Mission Control | — | zb-vela.tailec8707.ts.net (funnel→8765) | ✅ 200 |

## Systemd Services (all enabled, survive reboot)
User: ombnew (8799/8800), omb-relay-bridge (8801), novnc-gate (6081), 9router (20128), hermes-gateway, hermes-agent-os-dashboard (8765), zb-humanoid (3001)
System: cloudflared, deepseek-harness (3080, --trusted-host), vela-x11vnc (5900), vela-novnc (6080), tailscaled

## Key Apps
- **zbmaus-humanoid**: Vercel (zbmaus-humanoid.vercel.app), chat live ↔ OMB sinkron (~8 dtk)
- **OMB webhooks**: endpoint wh_knBDiZz4DGRydSZi, bot ZbmausHumanoid-Vercel
- **DSH**: token login, cookie 30 hari
- **OpenCraft**: gate key + VNC password, cookie 7 hari

## Credentials (locations, NEVER values)
- Webhook bearer: ~/zb/zbmaus-humanoid-webhook-secret.txt
- noVNC gate key: ~/zb/omb-new/novnc-gate.key
- OpenCraft URL: ~/zb/opencraft-access-url.txt
- DSH token: journalctl -u deepseek-harness | grep 'dsh web:'
- VNC password: ~/.vnc/passwd (encrypted)

## Security
- Cloudflare Bot Fight Mode: OFF (wajib — BFM mematikan chat live site)
- Proteksi per-hostname: pairing (zbmaus), token (dsh), gate key+sandi VNC (opencraft), bearer (ombrelay)

## Backup
- zb-backup.timer: Mingguan Senin 00:57 → Google Drive via Composio
- zb-backup-full.timer: 8 Nov 02:30

## Known Issues / Pending
1. PiPatung tidak jalan (port 3100 kosong) — kode di ~/zb/pi-patung
2. Cloudflare API token di Composio kurang scope DNS/zone (composio proxy REST works)
3. Antigravity engine OMB authenticated=false (OAuth callback :53727 pending)
4. Hermes wiki + offsite backup deployment menunggu keputusan user

## Quick Ops
```bash
systemctl --user is-active ombnew omb-relay-bridge novnc-gate 9router hermes-gateway zb-humanoid hermes-agent-os-dashboard
systemctl --user restart omb-relay-bridge novnc-gate
sudo journalctl -u deepseek-harness | grep 'dsh web:'
composio execute CLOUDFLARE_UPDATE_TUNNEL_CONFIGURATION --data '{...}'
```

## GitHub Repos (zb-vela related)
| Repo | Last Push | Deskripsi |
|---|---|---|
| zbmaus-humanoid | 2026-11-03 | OMB-connected humanoid interface (fork of Niu-Humanoid), debug probe removed, chat live ↔ bot OMB sinkron |
| zb-humanoid | 2026-11-02 | Humanoid interface project, agent-control bridge |
| ecosystem-omb | 2026-10-30 | Registry OMB, tier 3 domain lain |
| Niu-Humanoid / mira-humanoid | 2026-11-07 | APEX humanoid rebuild (Vite + React + TS) — shared concept |

## Node Topology (user's infrastructure)
- Mac (zhalls-macbook-pro): 100.120.57.37 — local dev, MIRAI :8800, Hermes gateway
- lightvela: 100.65.20.34 — cloud peer A2A (hermes-VM-6-34-ubuntu), relay Singapore
- zb-vela: 100.77.18.39 — second VPS (hermes-VM-11-184-ubuntu), relay Singapore
- aperture: 100.78.217.67 — Linux node
- All on Tailscale tailnet 'tailec8707'
- All repos push to same GitHub account: Niumination

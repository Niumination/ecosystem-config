# A2A Hermes — Mac ↔ VPS Connection Guide

> **Status:** IMPLEMENTED + credential-hygiene fix (2026-10-04) — LightVela cloud ↔ Mac via Tailscale
> **Dibuat:** 2026-09-14 · **Diupdate:** 2026-10-04
> **Protokol:** A2A v1.0 (Agent2Agent, Linux Foundation)
> **Token:** rotated 2026-10-03, stored in `~/.hermes/.env` + `vault/a2a-token.txt` (both mode 600)

---

## Topology

```
┌─────────────────────────┐          ┌──────────────────────────────┐
│  Hermes Mac (lokal)     │  A2A     │  LightVela VPS (cloud)      │
│  Tailscale: 100.120.57.37│ ◄──────► │  Tailscale: 100.65.20.34    │
│  A2A port: 9900         │  :9900   │  A2A port: 9900              │
│  Role: client + server  │          │  Role: server                │
└─────────────────────────┘          └──────────────────────────────┘
```

> IP di bawah adalah Tailscale CGNAT (100.64.0.0/10) — stabil per device, bukan IP publik/ISP.
> Peer cloud terdaftar di `~/.hermes/config.yaml` → `a2a_agents.cloud` (bukan `vps-mata` lagi).

---

## Prerequisites

| Komponen | Mac | VPS |
|----------|-----|-----|
| Hermes version | v0.21.1+ | v0.21.1+ |
| A2A plugin | built-in | built-in |
| Network | outbound to VPS:9900 | inbound :9900 open |
| Token | same on both sides | same on both sides |

---

## Implementation Steps

### Step 1 — VPS (server)

Edit `~/.hermes/config.yaml`:
```yaml
gateway:
  platforms:
    a2a:
      enabled: true
      extra:
        port: 9900
```

Set environment variables:
```bash
export A2A_HOST=0.0.0.0
export A2A_BEARER_TOKEN="<generate-32-char-random>"
export A2A_PUBLIC_URL="http://103.30.146.232:9900"
```

Enable toolset + restart:
```bash
hermes tools enable a2a --platform a2a
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

Verify:
```bash
curl http://103.30.146.232:9900/.well-known/agent-card.json
```

### Step 2 — Mac (client)

Enable a2a tools:
```bash
hermes tools enable a2a --platform telegram
hermes tools enable a2a --platform cli
```

Register VPS peer in `~/.hermes/config.yaml`:
```yaml
a2a_agents:
  vps-mata:
    url: "http://103.30.146.232:9900"
    auth:
      type: bearer
      token: "<same-token-as-vps>"
    timeout: 120
    capabilities: [coding, research, vps-ops, git, deployment]
```

Restart gateway:
```bash
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

### Step 3 — Verification

From Mac terminal:
```bash
curl http://103.30.146.232:9900/.well-known/agent-card.json
```

From Hermes chat:
```
"Discover agent di http://103.30.146.232:9900"
"Ask vps-mata to run git log in repo mata-aihackfest-2026"
```

---

## Usage Examples

### Mac → VPS (outbound call)
```
"Ask vps-mata to pull the latest changes in mata-aihackfest-2026"
"Ask vps-mata to check the MATA dashboard status"
"Ask vps-mata to run a probe on INAPROC API"
```

### VPS → Mac (inbound call)
Requires tunnel (Tailscale / Cloudflare) since Mac is behind NAT.

---

## Security Rules

| Rule | Implementation |
|------|---------------|
| Token | Min 32 chars, random, same on both sides |
| Firewall | VPS:9900 allow only Mac IP |
| No public exposure | Mac A2A stays localhost unless tunneled |
| Audit | All exchanges logged to `~/.hermes/a2a_audit.jsonl` |
| Anti-loop | Max 5 ping-pong turns per context |

---

## Credential Placement — WAJIB BACA (fix 2026-10-04)

`plugins/platforms/a2a/security.py:71` baca `A2A_HOST`; `:73-79` (`resolve_bind_host`) **abaikan `A2A_HOST`
dan bind ke `127.0.0.1` kalau `localhost_only()`** — yaitu kalau `A2A_BEARER_TOKEN` dan
`A2A_PEER_TOKENS` dua-duanya kosong. Gejala yang terlihat dari peer jauh:
`connection refused di <ip>:9900` padahal device-nya online.

### Kenapa `~/.hermes/.env`, bukan plist

`gateway/run.py:1577` memanggil `load_hermes_dotenv(..., override=True)` — **`.env` menang atas
environment dari plist**. Tapi `A2ASecurityContext.capture()` (`security.py:67-79`).resolve nilai
dari `os.getenv()` saat adapter start, jadi plist tetap bisa menyumbang key yang tidak ada di `.env`.

Historinya (3 Okt 2026): plist di-patch dengan `A2A_BEARER_TOKEN` → A2A bind ke Tailscale IP.
`.env` hanya punya `A2A_HOST` tanpa token.ADESIgn awal "plist itu redundan" SALAH — plist itu satu-satunya
sumber token saat itu. Setelah dipindah ke `.env` (4 Okt) + plist dibersihkan:

| Key | Sumber | Alasan |
|-----|--------|--------|
| `A2A_BEARER_TOKEN` | `~/.hermes/.env` (600, git-ignored) | dibaca Hermes native; aman dari `hermes gateway install` yang regenerate plist |
| `A2A_HOST` | `.env` **dan** plist | bukan credential; plist dibaca launchd saat boot, `.env` dibaca proses non-launchd (Hermes Desktop, `hermes` CLI) |
| peer token cloud | `~/.hermes/config.yaml` → `a2a_agents.cloud.token` | config, bukan env |

### Aturan

- **Jangan pernah** taruh credential di `~/Library/LaunchAgents/*.plist` — file itu 644 by default,
  world-readable, dan di-backup. Kalau terlanjur, `chmod 600` seketika.
- Kalau A2A `connection refused` setelah restart: cek dulu apakah `.env` punya **token**, bukan hanya
  `A2A_HOST`. Cek tanpa menyentuh nilai: `grep -c '^A2A_BEARER_TOKEN' ~/.hermes/.env` → harus ≥ 1.
- Verifikasi config resolution tanpa menebak — jalankan production code-nya di proses terpisah:
  ```bash
  cd ~/src/hermes-agent && python3 -c "
  import os,pathlib
  for l in pathlib.Path(os.path.expanduser('~/.hermes/.env')).read_text().splitlines():
      l=l.strip()
      if l and not l.startswith('#') and '=' in l:
          k,v=l.split('=',1); os.environ[k.strip()]=v.strip()
  from plugins.platforms.a2a.security import A2ASecurityContext as S
  s=S.capture(); print('bind:',s.resolve_bind_host(),'| localhost_only:',s.localhost_only())"
  ```
  `bind: 127.0.0.1` = token hilang. `bind: 100.120.57.37` = sehat.
- **Agent Card memang publik** (`adapter.py:189` — "Agent Cards are public"), jadi
  `GET /.well-known/agent-card.json` balas 200 tanpa token. Itu by design, bukan bypass. Yang
  meng-gate adalah `POST` (`adapter.py:205-208`): tanpa token harus `401`.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `401 Unauthorized` | Token mismatch — bandingkan `sha256[:12]` isi `.env` vs `vault/a2a-token.txt`, jangan print nilai penuh |
| `Connection refused` (device online) | **Penyebab paling sering: `.env` punya `A2A_HOST` tapi tanpa `A2A_BEARER_TOKEN`** → `resolve_bind_host` jatuh ke `127.0.0.1`. Cek `grep -c '^A2A_BEARER_TOKEN' ~/.hermes/.env`. Lihat bagian Credential Placement |
| `Connection refused` (device offline) | A2A/gateway mati — `lsof -iTCP:9900 -sTCP:LISTEN` |
| Card not reachable | Check firewall / `A2A_PUBLIC_URL` setting |
| Card 200 tapi POST 401 | Normal untuk `GET` (card publik by design); `POST` tanpa token memang 401 — itu auth bekerja, bukan bug |
| Timeout | Increase `timeout` in peer config |

---

## Reference

- Official docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a
- A2A Protocol: https://a2a-protocol.org/
- Config reference: `hermes config show` → gateway.platforms.a2a

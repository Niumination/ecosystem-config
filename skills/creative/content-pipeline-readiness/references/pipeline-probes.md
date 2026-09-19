# Probe Command Block — Content Pipeline Readiness

Blok perintah siap-tempel per lapisan, plus cara membaca keluaran. Jalankan berurutan supaya laporan punya angka nyata, bukan klaim.

## A. Baseline ekosistem (lapisan kesehatan)

```bash
cd ~/Desktop/Niumination && bash scripts/up-eco.sh 2>&1 | tee /tmp/up-eco-$(date +%H%M).log; echo "exit=$?"
```

Tangkap `exit=0` sebelum menyimpulkan sehat. Baca: HEAD hash, branch, jumlah repo dirty, folder asing, jumlah SKILL.md bank, mismatch manifest, akun/toolkit Composio, jumlah model 9router.

## B. Hulu — tool produksi

```bash
for c in ffmpeg manim node npx python3; do printf '%s: ' $c; command -v $c || echo MISSING; done
node -v; npx --no-install hyperframes --version
for p in 8188 20128 9377; do printf 'port %s: ' $p; curl -s -o /dev/null -w '%{http_code}\n' --max-time 3 http://localhost:$p/ || echo DOWN; done
```

Baca:
- `000`/`DOWN` = layanan mati. Untuk skill yang bergantung server lokal (mis. ComfyUI :8188) tandai ⚠️ "skill ada, server mati".
- `307`/`401` = layanan hidup (redirect/auth), bukan mati.
- Versi renderer dicatat apa adanya; jangan menyimpulkan kualitas dari versi.

## C. Aset produksi

```bash
grep -rl 'data-composition-id' --include='*.html' ~/Desktop/Niumination 2>/dev/null | grep -v node_modules | head
ls -l ~/Movies/'Posting - Instagram' 2>/dev/null
```

Tidak ada hasil pada pencarian komposisi = tidak ada template render yang bisa dipakai ulang. Cek juga brand kit (logo/palet/tipografi) dan folder materi siap-tayang.

## D. Verifikasi klaim port & endpoint (jangan percaya teks dokumen)

```bash
launchctl list | grep -i niu
ls -l ~/Library/LaunchAgents/ | grep -i niu
cat ~/Library/LaunchAgents/com.niumination.missioncontrol.plist 2>/dev/null | grep -A3 ProgramArguments
ls -R ~/Desktop/Niumination/services/niu-mission-control/apex-ui/app/api 2>/dev/null | head -30
for p in 3000 5200; do printf 'port %s: ' $p; curl -s -o /dev/null -w '%{http_code}\n' --max-time 4 http://localhost:$p/ || echo DOWN; done
```

Baca: label yang muncul di `launchctl list` = yang benar-benar termuat; plist memberi port produksi yang nyata; direktori `app/api/mc/` memberi endpoint yang benar-benar ada (`dispatch`, `dispatches`, `agents`, `health`, `tasks`, `telegram`). Route dispatch memuat peta topik agent→thread (`creator`→1172, `programmer`→803, `qa`→804, `research`→802, `chief`→1).

## E. Hilir — distribusi

```bash
grep -iE 'composio|toolkit' /tmp/up-eco-*.log | head -30
ls ~/Desktop/Niumination/docs/registry/ | grep -iE 'composio|deployment'
```

Baca: daftar toolkit ACTIVE. Tidak ada instagram/tiktok/facebook/buffer/ayrshare/postiz → publikasi manual; itu blocker hilir.

## F. Otomasi

```bash
python3 - <<'EOF'
import json, os
p = os.path.expanduser('~/.hermes/cron/jobs.json')
d = json.load(open(p))
jobs = d if isinstance(d, list) else d.get('jobs', d)
if isinstance(jobs, dict): jobs = list(jobs.values())
print('total', len(jobs))
for j in jobs:
    print(j.get('name'), '|', j.get('schedule'), '| enabled:', j.get('enabled'))
EOF
```

## G. Sumber bahan (aplikasi live)

```bash
grep -E '\| ✅ 200 \|' ~/Desktop/Niumination/docs/registry/deployment-status.md | head -25
```

## H. Verifikasi hasil laporan (sebelum melapor selesai)

```bash
cd ~/Desktop/Niumination && git status --short
git log --oneline -1
git ls-remote origin -h refs/heads/main
```

Hash pada `git ls-remote` harus sama dengan commit laporan; `git status --short` harus bersih. Jalankan ulang `git log --oneline -3` bila audit memakan waktu lama, karena thread lain bisa commit di sela-sela.

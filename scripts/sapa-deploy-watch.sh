#!/bin/bash
# Tunggu insiden deploy Vercel pulih, lalu picu deploy dan verifikasi.
# Sengaja nol-biaya: verifikasi memakai probe yang tidak memanggil model.
set -u
REPO="$HOME/Desktop/Niumination/services/sapa-ai"
URL="https://sapa-smart-ai.vercel.app"
LOG=/tmp/sapa_deploy_watch.log
: > "$LOG"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

insiden() {
  curl -s --max-time 15 https://www.vercel-status.com/api/v2/incidents/unresolved.json \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print(sum(1 for i in d.get('incidents',[]) if 'eployment' in (i.get('name') or '')))" 2>/dev/null || echo 1
}

build_hidup() {
  # Pesan ini hanya ada pada build SETELAH commit retry-skema. Tidak memanggil model.
  body=$(curl -s --max-time 25 -X POST "$URL/api/query" -H 'Content-Type: application/json' -d '{"query":"zzqq xxyy tanpa data"}')
  echo "$body" | grep -q "Tidak ada data SAPA yang relevan"
}

log "pemantau mulai; insiden deploy terbuka = $(insiden)"

for i in $(seq 1 90); do
  sleep 60
  open=$(insiden)
  if [ "$open" != "0" ]; then
    [ $((i % 10)) -eq 0 ] && log "menunggu… insiden masih terbuka (menit ke-$i)"
    continue
  fi
  log "insiden pulih. memicu deploy…"
  cd "$REPO" || exit 1
  git commit --allow-empty -m "chore: deploy setelah insiden Vercel pulih" >/dev/null 2>&1
  git push origin main >/dev/null 2>&1 && log "push dikirim" || log "GAGAL push"

  for j in $(seq 1 20); do
    sleep 30
    if build_hidup; then
      log "SUKSES: build baru sudah live (menit ${j}x30d)"
      break
    fi
    [ "$j" = "20" ] && log "build baru belum terdeteksi setelah 10 menit"
  done
  break
done

log "selesai. cek terakhir:"
curl -s --max-time 20 "$URL/api/status" | python3 -c "
import sys,json
a=json.load(sys.stdin).get('ai',{})
print('  state  :',a.get('state'))
print('  model  :',a.get('model'))
print('  reason :',(a.get('reason') or '-')[:110])
" 2>/dev/null | tee -a "$LOG"

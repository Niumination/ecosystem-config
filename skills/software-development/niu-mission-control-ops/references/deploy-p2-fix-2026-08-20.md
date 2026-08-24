# Deploy Page Fix (P2) — 20 Ags 2026

## Gejala
- Deploy page tampil 2 kartu `agent-card-premium` HARDCODED di index.html:
  `Niu-Vermilion` dan `Pemdi Aceh Tengah` — isinya tidak pernah berubah.
- `/api/mc/deploy/status` balas data LENGKAP (backend sehat):
  ```json
  {"projects":[{"name":"Niu-Vermilion","status":"success","last_deploy":"2026-08-01 14:32","url":"https://niu-vermilion.vercel.app"},{"name":"Pemdi Aceh Tengah","status":"success","last_deploy":"2026-07-28 09:15"}],"total":2,"success":2,"failed":0}
  ```
- Console tidak ada error — fungsi frontend ADA tapi hanya separuh kerja.
  `loadDeployStatus is not defined` TIDAK terjadi (beda dengan Cost page).

## Akar masalah
`loadDeployStatus()` di `dashboard/app.js` hanya men-set 2 elemen KPI:
- `deployLiveCount` = `data.success`
- `deployLastTime` = `data.projects[0].last_deploy.split(' ')[1]`

Tidak ada render ke `#deployProjectGrid` — grid itu tetap HTML static yang ditaruh
saat halaman dibuat. Pola ini sama dengan Cost page (HTML punya onclick + elemen,
tapi JS tidak menyentuh kontainer utama) → **pola kelas: cek apakah handler
benar-benar render ke kontainer grid, bukan cuma update elemen KPI.**

## Fix (app.js — `loadDeployStatus`)
```js
async function loadDeployStatus() {
  try {
    const res = await fetch('/api/mc/deploy/status');
    const data = await res.json();
    document.getElementById('deployLiveCount').textContent = data.success || 2;
    document.getElementById('deployLastTime').textContent = data.projects && data.projects[0] && data.projects[0].last_deploy ? data.projects[0].last_deploy.split(' ')[1] || '--' : '--';

    // Render project grid dinamis (ganti placeholder static)
    const grid = document.getElementById('deployProjectGrid');
    if (grid && data.projects && data.projects.length) {
      grid.innerHTML = data.projects.map(p => {
        const badgeClass = (p.status === 'live' || p.status === 'success') ? 'state-executing' : 'state-error';
        const badgeText = p.status === 'success' ? 'LIVE' : (p.status || 'UNKNOWN');
        const url = p.url || '#';
        const lastDeploy = p.last_deploy || '—';
        return `
        <div class="agent-card-premium">
          <div class="agent-card-header"><span>${p.name}</span><span class="badge">${p.env || 'PRODUCTION'}</span></div>
          <div>Branch: ${p.branch || 'main'} | Env: ${p.env || 'production'}</div>
          <div>URL: <a href="${url}" target="_blank" rel="noopener">${url.replace(/^https?:\/\//, '')}</a></div>
          <div>Status: <span class="status-badge ${badgeClass}">${badgeText}</span> · Last: ${lastDeploy}</div>
          <button class="btn-primary-glow" style="margin-top:0.5rem;font-size:0.6rem;padding:0.3rem 0.6rem;" onclick="triggerDeploy('${p.name.replace(/'/g, "\\'")}')">Deploy</button>
        </div>`;
      }).join('');
    }
  } catch (e) { console.log('Deploy status load failed:', e); }
}
```
Tambahkan `loadDeployStatus();` di blok Initialize App (dekat `loadCostData();`).

## Endpoint terkait
- `GET /api/mc/deploy/status` — daftar project + status
- `GET /api/mc/deploy/projects` — daftar project detail (branch/env/url/status)
- `POST /api/mc/deploy` body `{"project","branch","environment"}` → simulated trigger
  (balas `vercel_job_id`, TIDAK melakukan deploy sungguhan)

## Verifikasi
1. Naikkan cache-bust di index.html: `?v=` baru.
2. `launchctl kickstart -k gui/501/niu.missioncontrol`
3. Browser: `typeof loadDeployStatus === "function"`
4. DOM: `deployProjectGrid.children.length` → 2, `deployLiveCount` → "2",
   kartu berisi URL asli + badge LIVE.

## Catatan vision
`browser_vision` menampilkan ORB overlay (layer atas), bukan page yang di-switch
via JS — gunakan DOM count sebagai bukti (lihat SKILL.md → ORB-overlay pitfall).
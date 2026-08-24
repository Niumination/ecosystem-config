# Floating Window Engine — orb.html & fusion/index.html (port 2026-08)

Engine `.fwin` yang sama hidup di dua surface. Untuk port/duplikasi/audit, ini blueprint-nya.

## CSS (masuk sebelum media query responsive)

```
#winMount{position:fixed;inset:0;pointer-events:none;z-index:300}
.orb-dim{position:fixed;inset:0;background:rgba(3,5,10,.55);opacity:0;pointer-events:none;transition:opacity .35s;z-index:250}
.orb-dim.show{opacity:1;pointer-events:auto}
.fwin{position:fixed;display:flex;flex-direction:column;min-width:380px;min-height:300px;z-index:300;
  opacity:0;transform:scale(.84) translateY(22px) rotateX(8deg);pointer-events:none;
  background:rgba(10,15,28,.82);backdrop-filter:blur(26px);border:1px solid rgba(111,216,255,.14);border-radius:14px;
  transition:opacity .32s cubic-bezier(.34,1.3,.4,1),transform .32s cubic-bezier(.34,1.3,.4,1);transform-origin:center bottom}
.fwin.open{opacity:1;transform:scale(1) translateY(0) rotateX(0);pointer-events:auto}
.fwin.closing{opacity:0;transform:scale(.9) translateY(14px);pointer-events:none}
.fwin.focused{z-index:400;box-shadow:0 32px 110px -18px rgba(0,0,0,.9),0 0 0 1px rgba(111,216,255,.25),0 0 50px -10px rgba(111,216,255,.25)}
.fwin.minimized{transform:scale(.92) translateY(24px);opacity:0;pointer-events:none}
.fwin-bar{display:flex;align-items:center;gap:9px;padding:10px 14px;cursor:grab;user-select:none;border-bottom:1px solid rgba(111,216,255,.09)}
.fwin-dots{display:flex;gap:6px} .fdot{width:11px;height:11px;border-radius:50%}
.fdot-close{background:#ef4444} .fdot-min{background:#fbbf24} .fdot-max{background:#22c55e}
.fwin-body{flex:1;min-height:0;position:relative;overflow:hidden;background:rgba(5,7,13,.45)}
.fwin-body iframe{width:100%;height:100%;border:none;display:block}
.fwin-loading{position:absolute;inset:0;display:grid;place-items:center;z-index:2;background:#05070d;transition:opacity .3s}
.fwin-loading.done{opacity:0;pointer-events:none}
.fwin-resize{position:absolute;right:0;bottom:0;width:18px;height:18px;cursor:nwse-resize;z-index:5}
#taskbar{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);z-index:600;display:flex;gap:5px;padding:7px 10px;
  background:rgba(10,15,28,.82);backdrop-filter:blur(26px);border:1px solid rgba(111,216,255,.14);border-radius:16px;max-width:94vw}
.tb-btn{display:flex;align-items:center;gap:7px;padding:6px 12px;border-radius:10px;font-size:.64rem;font-weight:600;cursor:pointer}
.tb-btn.open{color:#f1f5f9;background:rgba(111,216,255,.1);border:1px solid rgba(111,216,255,.18)}
.tb-btn.minimized{color:#64748b;opacity:.65}
.m-item .m-badge{display:none;margin-left:auto;font-size:.55rem;color:#22d3ee;background:rgba(111,216,255,.12);padding:1px 7px;border-radius:8px}
.m-item.on{background:rgba(111,216,255,.12)} .m-item.on .m-badge{display:inline-block}
.win-burst{position:fixed;width:120px;height:120px;border-radius:50%;pointer-events:none;z-index:299;
  background:radial-gradient(circle,rgba(111,216,255,.28),transparent 65%);transform:translate(-50%,-50%) scale(0);opacity:0}
```

## Registry APPS (13 app, key = data-app)

```js
const APPS = {
  dashboard:     { url:'/dashboard',            title:'AgentOS Dashboard',  ico:'fa-table-columns',  accent:'#4f46e5', w:880, h:620 },
  aios:          { url:'/aios',                 title:'AIOS Holographic',   ico:'fa-user-astronaut', accent:'#f59e0b', w:920, h:660 },
  ecosystem:     { url:'/dashboard#ecosystem',  title:'Ecosystem',          ico:'fa-globe',          accent:'#22d3ee', w:860, h:600 },
  swarm:         { url:'/dashboard#swarm',      title:'Swarm Topology',     ico:'fa-network-wired',  accent:'#8b5cf6', w:860, h:600 },
  taskqueue:     { url:'/dashboard#taskqueue',  title:'Task Kanban',        ico:'fa-list-check',     accent:'#22c55e', w:900, h:640 },
  terminal:      { url:'/dashboard#terminal',   title:'Terminal Hub',       ico:'fa-terminal',       accent:'#f97316', w:820, h:560 },
  telegram:      { url:'/dashboard#telegram',   title:'Telegram Bridge',    ico:'fa-paper-plane',    accent:'#38bdf8', w:860, h:620 },
  storage:       { url:'/dashboard#storage',    title:'USB & Storage',      ico:'fa-hard-drive',     accent:'#e2e8f0', w:820, h:560 },
  skills:        { url:'/dashboard#skills',     title:'Skill Monitor',      ico:'fa-brain',          accent:'#f472b6', w:860, h:600 },
  'skills-market':{url:'/dashboard#skills-market',title:'Skill Market',      ico:'fa-store',          accent:'#a3e635', w:860, h:600 },
  system:        { url:'/dashboard#system',     title:'System Config',      ico:'fa-sliders',        accent:'#94a3b8', w:840, h:580 },
  cost:          { url:'/dashboard#cost',       title:'Cost Tracking',      ico:'fa-coins',          accent:'#fbbf24', w:820, h:560 },
  deploy:        { url:'/dashboard#deploy',     title:'Vercel Deploy',      ico:'fa-rocket',         accent:'#60a5fa', w:820, h:560 },
};
```

## Fungsi kunci

| Fungsi | Peran |
|---|---|
| `openWindow(appId)` | Jika sudah terbuka → fokus; else buat `.fwin`, cascade, burst, spinner, iframe, dedup, taskbar, menu-state. Ekspos `window.__openApp`. |
| `closeWindow(appId)` | `.closing` → remove 280ms; hapus taskbar/menu-state; `orbDim.show` = `openApps.size>0`. |
| `minimizeWindow / restoreWindow` | toggle `.minimized` + state taskbar. |
| `toggleMax(appId)` | simpan px/py/pw/ph di `data-*`, swap ke `100vw/100vh`; klik lagi = restore. |
| `focusWindow(appId)` | zTop++ → `style.zIndex`; `.focused` eksklusif; sync taskbar `.open`. |
| `addTaskbar / removeTaskbar` | tombol dinamis per app terbuka. |
| `setMenuState(appId, on)` | `.m-item.on` + badge ●. |
| `cascadePos(idx)` | `x = center + (idx-1)*36 - 60`, `y = center + (idx-1)*26 - 40`, clamp viewport. |

## Dedup chrome iframe (ekspos untuk debug)

```js
function dedupDashboardPage(iframe){
  const d = iframe.contentDocument; if(!d) return;
  const sb = d.querySelector('.sidebar'); if(sb) sb.style.display='none';
  const tn = d.querySelector('.topnav');  if(tn) tn.style.display='none';
  const ws = d.getElementById('wsRecBtn'); if(ws) ws.style.display='none';
  const mc = d.querySelector('.main-content'); if(mc) mc.style.marginLeft='0';
}
function dedupAios(iframe){
  const d = iframe.contentDocument; if(!d) return;
  ['pLeft','pRight'].forEach(id=>{ const el=d.getElementById(id); if(el) el.style.display='none'; });
  const st = d.querySelector('.stats'); if(st) st.style.display='none';
  d.querySelectorAll('.dock > .dock-s').forEach(s=>s.style.display='none');
}
```

Panggilan: `iframe.addEventListener('load', ()=>{ loader→done 250ms; setTimeout(dedup, 450) })` + fallback 5s.

## Verifikasi (browser_console, vision boleh down)

```js
// 1) engine hidup
typeof window.__openApp === 'function' && Object.keys(APPS).length === 13
// 2) buka window
window.__openApp('swarm'); window.__openApp('telegram');
document.querySelectorAll('.fwin').length  // 2
// 3) dedup — WAJIB readyState complete dulu
(async()=>{await new Promise(r=>setTimeout(r,2500));
  const w=document.querySelector('.fwin[data-app="swarm"] iframe');
  w.contentDocument.readyState==='complete' &&
  w.contentDocument.querySelector('.sidebar').style.display==='none';})()
// 4) kontrol
win.querySelector('.fwin-act[data-act="max"]').click() → data-max='1', w='100vw'
document.querySelector('.tb-btn[data-app="swarm"]').click() → .minimized toggle
```

## Pitfall

- **Verifikasi dedup terlalu cepat = false negative** (sidebar `display:''` padahal dedup jalan). Selalu cek `readyState==='complete'` dulu, atau tunggu 2–2.5s.
- Dedup selector BERBEDA tergantung konteks embed: fusion lama pakai `.col-left/.col-center/.at-live-ops` (embed seksi), orb pakai `.sidebar/.topnav/.main-content` (embed halaman penuh). Jangan campur.
- Menu item pakai `data-app` (registry), BUKAN `data-p` (hash routing lama) — item lama `data-p` tidak akan membuka window.
- Klik menu saat window sudah terbuka = TOGGLE (minimize/fokus), bukan membuka duplikat.

# Selector de-duplikasi — dashboard & aios (verified di DOM live, 2026-08-15)

Disembunyikan HANYA di dalam fusion (iframe contentDocument), halaman asli tidak berubah. Hook: `openWindow()` → iframe `load` event → `setTimeout(dedup, 400)`.

## Dashboard (`__dedupDashboard`, hasil: 5 elemen tersembunyi)

| Fitur duplikat | Selector | Catatan |
|---|---|---|
| Agent Fleet State | `.col-left` | (SWARM di ORB) |
| Terminal Matrix Stream | `.col-center` | (FEED di ORB) |
| Context Window | `.at-live-ops` | (THREADS di ORB) |
| VPS / Local Health | `.at-ops-col` berisi teks "VPS"/"Local Health"/"CPU Usage" | loop semua, cek textContent |
| Live Activity Feed | byText('Live Activity Feed') | walk-up parent sampai class berisi col/card/panel/grid/section |

**Tetap visible:** `.col-right` (kanban + telegram bridge), KPI stats.

`byText` helper (walk-up max 6 level, berhenti di elemen ber-class col/card/panel/grid/ops/section/ber-id):
```js
function byText(txt, maxUp=6){ return doc=>{
  const tn=[...doc.querySelectorAll('h1,h2,h3,h4,div,span')]
    .find(e=>e.children.length<3 && e.textContent.trim().startsWith(txt));
  if(!tn) return null;
  let p=tn.parentElement;
  for(let i=0;i<maxUp && p;i++){
    const cls=p.className?.toString()||'';
    if(cls.includes('col')||cls.includes('card')||cls.includes('panel')||
       cls.includes('grid')||cls.includes('ops')||cls.includes('section')||
       p.tagName==='SECTION'||p.id) return p;
    p=p.parentElement;
  }
  return tn.parentElement; }; }
```

## AIOS (`__dedupAios`, hasil: 6 elemen tersembunyi)

| Fitur duplikat | Selector |
|---|---|
| Thread Orchestrator | `#pLeft` |
| Swarm Network | `#pRight` |
| Stats (tokens/latency/load) | `.stats` |
| Live Log Stream + Activity Feed + Voice | `.dock > .dock-s` (semua, 3 elemen) |

**Tetap visible:** `#holo` (canvas holographic core), view mode buttons.

## Verifikasi (browser_console)

```js
window.__dedupDash   // 5
window.__dedupAios   // 6
[...d.querySelectorAll('.col-left,.col-center,.at-live-ops,.at-ops-col')]
  .filter(e=>e.style.display==='none').length   // 4 (dashboard)
[...a.querySelectorAll('#pLeft,#pRight,.stats,.dock > .dock-s')]
  .filter(e=>e.style.display==='none').length   // 6 (aios)
// + fitur unik masih visible:
d.querySelector('.col-right').style.display !== 'none'
a.getElementById('holo').style.display !== 'none'
```

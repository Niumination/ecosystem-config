# Rebuild dashboard yang digutting refactor palsu (kasus MC 2026-08-16)

Recovery playbook ketika refactor agent menghancurkan file dan klaimnya palsu ("selesai" padahal konten hilang & tak pernah di-serve).

## Konteks
- Niu-MissionControl: `services/niu-mission-control/dashboard/`
- Backup lengkap: `dashboard_backup_refactor_20260816/` (index.html 72KB, 12 `<section class="page" id="page-X">`)
- Target: orb (iframe) background + launcher + 12 floating windows (draggable, min/max/close, cascade, taskbar)

## Pola builder script (`dashboard/build_unified.py`)
1. **Ekstrak** tiap section dari backup: regex `(<section\s+class="page[^"]*"\s+id="page-([a-z-]+)"[^>]*>)(.*?)(</section>)` dengan DOTALL; simpan per id.
2. **Inject** elemen yang direferensikan app.js TANPA null-check TAPI berada di chrome yang dibuang (header telemetry: `gwStatusText`/`gwBadge`; sidebar-footer: `healthPct`/`healthFill` + tombol checkpoint) → WAJIB ada di DOM atau app.js crash di `connect()` (TypeError null).
3. **Wrap** tiap section dalam `.fwin` floating window; konten INLINE di DOM (jangan iframe/stub) → semua `getElementById` + polling WS tetap jalan.
4. **Escape f-string:** JS braces di template Python f-string harus dobel `{{ }}` — lint Python error `f-string: invalid syntax` = kurung JS belum di-escape.
5. **Hash routing** → launcher click handler; expose manager: `window.openWindow/closeWindow/minimizeWindow/restoreWindow/toggleMax` (kalau tidak, tes browser via console gagal).

## Verifikasi builder
- `python3 build_unified.py` → output menampilkan jumlah section + id yang di-inject.
- Syntax check script block: `new Function(scriptText)` (node) atau `re.findall(r'<script>(.*?)</script>', h, re.S)` di Python.
- `grep -c 'id="healthPct"' index.html` dst — semua id kontrak ADA di output.

## Pitfall runtime yang ditemukan
- **WS shape mismatch:** `/ws/swarm` kirim `agents` sebagai DICT `{agent_id: status_string}`; REST `/api/mc/agents` kirim array. Crash asli: `Cannot read properties of undefined (reading 'toUpperCase')` di `a.status.toUpperCase()` → renderAgents harus normalisasi `Object.entries()` + merge metadata (AGENT_META mirror `swarm/agents.py` AGENT_CONFIG).
- **Cascade window:** posisi = offset berantai dari window terakhir (+52/+42px), clamp viewport; BUKAN `idx*14` yang ukurannya membesar — titlebar window kedua tertutup window pertama.
- **Health poll awal:** GATEWAY tampak OFFLINE di 3 detik pertama (poll belum settle) — tunggu ~2s lalu re-baca; verifikasi via `curl /api/mc/hermes` (gateway.online/simulated).

## Verifikasi final (objektif)
- `venv/bin/pytest tests/ -q` → 44 passed.
- `curl` semua route: `/`, `/dashboard`, `/fusion`, `/aios`, `/static/*` → 200.
- Browser: buka 12 window via console → `document.querySelectorAll('.fwin.open').length == 12`; tutup semua → vault 12/12 kembali; console zero errors (clear buffer dulu — console lama menumpuk dan menyesatkan).
- Kaskade: 3 window berurutan → titlebar tiap window visible (x/y bertambah 52/42, z-index naik).

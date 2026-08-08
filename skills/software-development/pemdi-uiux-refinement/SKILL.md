---
name: pemdi-uiux-refinement
description: "Refine UI/UX portal Pemdi Aceh Tengah dengan impeccable + hermes-uiux-technical — sistem animasi global, fix anti-pattern, audit pasca-deploy. Trigger: perubahan desain/animasi/UX PemdiAcehTengah."
version: 1.0.0
tags: [ui-ux, animation, nextjs, impeccable, pemdi]
---

# Refinement UI/UX PemdiAcehTengah

## Trigger
Gunakan ketika: redesign/polish UI portal `apps/PemdiAcehTengah`, tambah animasi,
fix anti-pattern, atau audit UX. Kombinasi skill: `impeccable` (playbook) +
`hermes-uiux-technical` (kapabilitas).

## Workflow Terbukti

### 1. Audit awal
```bash
cd apps/PemdiAcehTengah
node <skill-base>/design/impeccable/scripts/context.mjs --target pages/index.js
node <skill-base>/design/impeccable/scripts/detect.mjs --json pages/
```

### 2. Referensi (riset cepat)
- USWDS design principles (task-oriented, trust, accessibility, plain language)
- GOV.UK = gold standard task-oriented
- Animation: 60fps (transform/opacity only), prefers-reduced-motion WAJIB,
  stagger via IntersectionObserver (threshold 0.1, rootMargin -32px)

### 3. Sistem animasi global (terbukti)
Tambahkan ke `globals.css`:
- `[data-reveal]`: fade-up 22px, cubic-bezier(0.16,1,0.3,1), 0.65s
- `[data-reveal-stagger] > *`: delay `calc(var(--i,0) * 70ms)`
- Micro-interaction: `.card:hover` translateY(-3px), button active scale(0.97)
- Nav active: `::after` gold bar bawah (bukan side-tab)

Di `AppShell.js` (satu kali, semua halaman):
```js
useEffect(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const els = document.querySelectorAll('[data-reveal], [data-reveal-stagger]');
  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach(el => el.classList.add('is-visible')); return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -32px 0px' });
  els.forEach(el => io.observe(el));
  return () => io.disconnect();
}, [pathname]);
```

### 4. Terapkan data-reveal ke halaman
- Hero: `<section data-reveal style={{ background: 'var(--hero-grad)'...`
- Grid stats/kategori: `data-reveal-stagger` + `--i` per anak
- index.js sudah punya sistem `.reveal`/`.in` sendiri (jangan dobel)

### 5. Fix anti-pattern detector
- side-tab (`borderLeft: 3-4px`) → `borderTop: 3px` (konsisten)
- overused-font Inter → **Plus Jakarta Sans** (workhorse mode Operate — valid)
- layout-transition `transition: width` → `animation: fade-up` + transformOrigin

### 6. Build → verifikasi lokal → deploy → audit production
- `npx next build` sukses
- Browser: cek `[data-reveal].is-visible` & stagger children opacity===1
- Deploy Vercel, tunggu, audit: font PJS aktif, reveal/stagger jalan, detector bersih

## Pitfalls
- **jangan dobel animasi** — index.js pakai `.reveal` sendiri, halaman lain pakai `[data-reveal]`
- Detector flag PJS sebagai overused-font → **acceptable** (workhorse Operate, bukan AI default)
- `--i` custom property di inline style React: `style={{ '--i': idx }}`
- prefers-reduced-motion: langsung `is-visible` tanpa animasi (35% user)

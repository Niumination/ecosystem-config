// Template probe halaman — salin, jalankan sebagai expression di konteks halaman
// (mis. endpoint evaluate browser headless), lalu sesuaikan bagian yang relevan.
// Mengembalikan satu string JSON supaya aman dilewatkan antar-proses.
// Aturan validitas ada di SKILL.md § 2 — jangan hapus filter di dalamnya.

(() => {
  const nm = e => e.tagName.toLowerCase() +
    (typeof e.className === 'string' && e.className.trim()
      ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.')
      : '');
  const out = {};
  const de = document.documentElement;
  const vw = innerWidth, vh = innerHeight;

  out.viewport = vw + 'x' + vh;
  out.tinggiHalaman = document.body.scrollHeight;
  out.layarSetara = Math.round(document.body.scrollHeight / vh);
  out.overflowHorizontal = de.scrollWidth > vw + 1;
  out.simbolDom = document.getElementsByTagName('*').length;

  // ── tap target < 44px ─────────────────────────────────────────────
  const kecil = [];
  for (const el of document.querySelectorAll('a, button, select, summary, [role=button]')) {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 && r.height < 44)
      kecil.push(nm(el) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  }
  out.tapTargetKecil = { jumlah: kecil.length, contoh: kecil.slice(0, 10) };

  // ── kontras (HANYA latar solid; gradient/color-mix dilewati) ──────
  const lum = c => { const m = (c || '').match(/[\d.]+/g); if (!m) return null;
    const [r, g, b] = m.map(Number);
    const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const gagal = [], perluMata = [];
  for (const el of document.querySelectorAll('body *')) {
    if (!el.offsetParent) continue;
    const t = Array.from(el.childNodes).filter(n => n.nodeType === 3)
      .map(n => n.textContent.trim()).join(' ').trim();
    if (t.length < 2) continue;
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || parseFloat(s.opacity) < 0.15) continue;
    let p = el, bg = null, gradient = false;
    while (p && p !== de) {
      const ps = getComputedStyle(p);
      if (ps.backgroundImage && ps.backgroundImage !== 'none') gradient = true;
      if (ps.backgroundColor !== 'rgba(0, 0, 0, 0)') { bg = ps.backgroundColor; break; }
      p = p.parentElement;
    }
    if (!bg || gradient) { perluMata.push(nm(el)); continue; }
    const l1 = Math.max(lum(s.color), lum(bg)), l2 = Math.min(lum(s.color), lum(bg));
    const rasio = (l1 + 0.05) / (l2 + 0.05);
    const fs = parseFloat(s.fontSize), bold = parseInt(s.fontWeight) >= 700;
    const perlu = (fs >= 24 || (fs >= 18.66 && bold)) ? 3 : 4.5;
    if (rasio < perlu) gagal.push({ el: nm(el), rasio: Math.round(rasio * 100) / 100,
      perlu, warna: s.color, bg, txt: t.slice(0, 30) });
  }
  gagal.sort((a, b) => a.rasio - b.rasio);
  out.kontrasGagal = { jumlah: gagal.length, terburuk: gagal.slice(0, 10) };
  out.perluVerifikasiMata = perluMata.slice(0, 10);   // latar gradient -> bukan temuan

  // ── konten terpotong (overflow hidden dengan isi lebih besar) ─────
  const potong = [];
  for (const el of document.querySelectorAll('body *')) {
    if (!el.offsetParent) continue;
    const s = getComputedStyle(el);
    if (/marquee|strip/.test(el.className || '') || s.animationName !== 'none') continue;
    if ((s.overflowX === 'hidden' || s.overflowX === 'clip') && el.clientWidth > 0 &&
        el.scrollWidth - el.clientWidth > 6)
      potong.push(nm(el) + ' +' + (el.scrollWidth - el.clientWidth) + 'px');
  }
  out.terpotong = potong.slice(0, 8);

  // ── aset & noise ─────────────────────────────────────────────────
  const imgs = Array.from(document.images);
  out.gambar = { total: imgs.length,
    gagal: imgs.filter(i => i.complete && i.naturalWidth === 0).length,
    tanpaAlt: imgs.filter(i => !i.hasAttribute('alt')).length };
  out.emojiDalamTeks =
    ((document.body.innerText.match(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/gu)) || []).length;
  out.inputDiHalaman = document.querySelectorAll('input').length;
  out.animasiBerjalan = Array.from(document.querySelectorAll('body *'))
    .filter(e => getComputedStyle(e).animationName !== 'none').length;

  // ── bar ber-transform: buktikan rasio visual = nilai scaleX ───────
  out.barTransform = Array.from(document.querySelectorAll('body *'))
    .filter(e => (e.getAttribute('style') || '').includes('scaleX'))
    .slice(0, 5).map(e => {
      const p = (e.getAttribute('style').match(/scaleX\(([\d.]+)\)/) || [])[1];
      const r = e.getBoundingClientRect(), pr = e.parentElement.getBoundingClientRect();
      return { scaleX: p, lebarLayout: e.offsetWidth, lebarVisual: Math.round(r.width),
               lebarInduk: Math.round(pr.width),
               rasio: Math.round((r.width / pr.width) * 100) / 100 };
    });

  return JSON.stringify(out);
})()

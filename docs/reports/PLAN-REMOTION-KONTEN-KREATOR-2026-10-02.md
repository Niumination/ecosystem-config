# Plan: Adaptasi Remotion ke Thread Konten Kreator

**Sumber:** riset 2 Okt 2026 → `docs/reports/RISET-REMOTION-ADAPTASI-ECOSYSTEM-2026-10-02.md`
**Spesifikasi target:** i5-10310U · 16 GB · UHD 620 · macOS 26.5 · tanpa Docker
**Scope:** thread Konten Kreator (1172) saja. Tidak untuk thread lain (802/803/804/7402/8853/DM).
**Lisensi:** Afrizal saja (1 seat) → Free License $0 (sumber: remotion.dev/docs/license/faq)

---

## Scope (hanya thread Konten Kreator)

Yang tersentuh:
- Install Remotion di `sandbox/remotion-studio/` (luar ekosistem utama, sesuai pitfall HyperFrames)
- `npx remotion skills add` → Agent Skills aktif
- Update skill `content-produce` (tambah opsi Remotion di Mode A tanpa GPU)
- Tambah skill `remotion-video` di bank keterampilan `skills/content/`
- Workflow prompt → komponen Remotion → render → MP4
- Binding skill ke thread Kreator (#1172) — tergantung config ada di `~/.hermes/`

Yang TIDAK tersentuh:
- Proyek lain di ekosistem
- Config Hermes global (kecuali skill binding)
- Repo publik Niumination (semua perubahan lokal dulu)

---

## Fase 1 — Install & verify (SELESAI ✅)

1. ✅ `npx create-video@latest --yes --blank --no-tailwind remotion-studio` — exit 0
2. ✅ `npm i` — 356 packages, 2 menit
3. ✅ `npx remotion skills add` — 12 skills terinstall (Hermes Agent juga terdeteksi, symlink ke `.agents/skills/`)
4. ✅ Render test `MyComp` → `out/hello.mp4` — 5.4 KB, 2 detik, h264 480p, exit 0
5. ⚠️ Chrome Headless Shell 98 MB diunduh first-run (one-time)

**Bukti:** `ls -lh out/hello.mp4` → 5.2K, `ffprobe` → 2.000 detik, 21428 bps
**Waktu render total:** ~3 menit (termasuk download Chrome). Render berikutnya lebih cepat.
**Lisensi:** Free tier ≤3 org = $0 ✅

---

## Fase 2 — Workflow adapter (SELESAI ✅)

- Template `templates/formats/remotion-shorts.json` (9:16, 30 detik, GPU-free composition) ✅ dibuat
- Prompt adapter: user kirim deskripsi → agent tulis `index.tsx` Remotion → render
- Batasan Mode A2: composition ≤ 30 detik, 1080×1920 vertikal, tanpa efek GPU-heavy
- Fallback: bila render >5 menit → potong durasi / turun ke HyperFrames ✅ dicatat di pitfalls

---

## Fase 3 — Skill bank + thread binding (SELESAI ✅)

- ✅ Skill `remotion-video` baru di `skills/content/remotion-video/SKILL.md`
- ✅ `content-produce` SKILL.md diperbarui: Mode A2 + pitfalls lisensi + batasan CPU
- ✅ Hermes Agent Skills terinstall di `~/.hermes/skills/remotion-project/` (12 skill: best-practices, captions, create, docs, interactivity, maps, markup, multimedia, render, saas, studio, upgrade)
- ✅ `~/.hermes/skills/content-remotion-video/` → skill bank Hermes lokal
- ✅ `config.yaml` channel_skill_bindings thread 1172 → `["ghost", "humanizer", "remotion-video"]`
- ⏳ Backup config: `config.yaml.bak-remotion-20261002` ada di `~/.hermes/`

**Verifikasi binding:**
```bash
python3 -c "import yaml,json; cfg=yaml.safe_load(open('/Users/zaryu/.hermes/config.yaml')); b=json.loads(cfg['platforms']['telegram']['extra']['channel_skill_bindings']); print(b['1172'])"
→ ['ghost', 'humanizer', 'remotion-video']
```

---

## Sisa keputusan (minimal)

- ⚠️ Klarifikasi "org": FAQ resmi Remotion — yang di-hitung = **penulis kode Remotion** (langsung atau via AI tools), BUKAN thread/DM/penonton/agent.
  - Afrizal = 1 seat → Free License $0
  - 7 thread + DM = konsumen output → tidak hitung
  - Baru bayar $25/bulan/orang bila tim >3 penulis
- ✅ **Lisensi confirmed:** Afrizal saja (1 seat) → Free License $0
- ✅ **Scope diperjelas:** Remotion hanya untuk thread Konten Kreator (1172). Tidak untuk thread lain (802/803/804/7402/8853/DM).

---

## Bukti inspeksi (sebelum eksekusi)

- `node -v` → v26.7.0 ✅ (Remotion butuh ≥16)
- `ffmpeg -version` → ada ✅
- `df -h /` → 21 GB free ✅
- `npx --version` → ada ✅
- Lisensi Free tier → ≤3 org = $0 (dari remotion.dev/docs/license/faq)

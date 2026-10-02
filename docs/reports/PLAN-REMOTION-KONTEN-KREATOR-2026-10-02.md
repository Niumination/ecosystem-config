# Plan: Adaptasi Remotion ke Thread Konten Kreator

**Sumber:** riset 2 Okt 2026 → `docs/reports/RISET-REMOTION-ADAPTASI-ECOSYSTEM-2026-10-02.md`
**Spesifikasi target:** i5-10310U · 16 GB · UHD 620 · macOS 26.5 · tanpa Docker
**Lisensi:** Free tier (≤3 org) → $0

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

## Fase 1 — Install & verify (≤30 menit, 0 risiko ekosistem)

1. `cd ~/Desktop/Niumination/sandbox && npx create-video@latest --yes --blank --no-tailwind remotion-studio`
2. `cd remotion-studio && npm i && npx remotion skills add`
3. `npm run devCopy` → buka Studio, verify template Hello World jalan
4. `npx remotion render` → render 1 clip pendek (5 detik), ukur waktu render di CPU ini

**Bukti:** folder `sandbox/remotion-studio/` ada + `renders/` berisi MP4 + waktu render tercatat

---

## Fase 2 — Workflow adapter (sesuai spek Mac)

- Template `templates/formats/remotion-shorts.json` (9:16, 30 detik, GPU-free composition)
- Prompt adapter: user kirim deskripsi → agent tulis `index.tsx` Remotion → render
- Batasan Mode A: composition ≤ 30 detik, 1920×1080 (atau 1080×1920 vertikal), tanpa efek GPU-heavy
- Fallback: bila render >5 menit → potong durasi / turun ke HyperFrames

---

## Fase 3 — Skill bank + thread binding

- Salin skill `remotion-video` ke `skills/content/` → `sync-to-agents.sh`
- Update `content-produce` SKILL.md: tambah baris Remotion di Mode A
- Tambah ke `channel_skill_bindings` thread 1172 (backup config dulu)

---

## Keputusan yang perlu confirmasi

- [ ] Fase 1 boleh jalan? (install di sandbox, 0 risiko)
- [ ] Fase 2: durasi max clip? (syarat: render <5 menit di CPU ini)
- [ ] Fase 3: thread binding ke 1172? (konfig Hermes, backup dulu)
- [ ] Lisensi: confirm ≤3 org sekarang (Afrizal + siapa lagi)?

---

## Bukti inspeksi (sebelum eksekusi)

- `node -v` → v26.7.0 ✅ (Remotion butuh ≥16)
- `ffmpeg -version` → ada ✅
- `df -h /` → 21 GB free ✅
- `npx --version` → ada ✅
- Lisensi Free tier → ≤3 org = $0 (dari remotion.dev/docs/license/faq)

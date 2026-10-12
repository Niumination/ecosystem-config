# Rencana Adopsi — Motion Reel Kit (reel-maker-kit.zip)

**Tanggal:** 2026-10-11
**Sumber:** `~/Downloads/reel-maker-kit.zip` (73 MB, 88 file, v1.0.0, MIT)
**Status:** STUDY — belum dieksekusi. Menunggu approval pemilik.
**Revisi:** v2 — arah integrasi dikoreksi owner (bukan skill standalone, masuk pipeline studio).

---

## 1. Ringkasan Paket

Motion Reel Kit = sistem produksi video motion-graphics 1080p60 **seluruhnya dalam kode Python** — tanpa After Effects, tanpa footage stok, tanpa lisensi musik, tanpa API key, tanpa biaya.

| Lapisan | File | Peran |
|---|---|---|
| L0 Signal | `src/audio.py` (471 baris) | Sintesis musik dari numpy → `score.wav` + `spectrum.npz` (28 band per frame — satu-satunya jalur audio→visual) |
| L1 Engine | `src/lib/core.py`, `src/fontface.py` | Canvas 1920×1080, easing, noise, teks, TTF→cairo via FreeType tanpa install OS |
| L2–3 Scene | `src/lib/scenes.py` (1023), `scenes2.py` (679) | 15 scene renderer, timeline `TL`, cut pada beat |
| L4–5 Render | `src/render.py` | Post chain (motion blur, bloom, CA, film grain), encode H.264+AAC, mux |
| L6 Command | `reelctl.py` | CLI: `doctor/timeline/score/shot/sheet/render/verify/poster/new/clean` |
| L7 Agent | `agent/` | HERMES_SKILL.md, MCP server (12 tool), skill.json, prompts, tool schemas |

**Output referensi:** 30.00 s, 1800 frame, 128 BPM, 15 scene, 14 beat-locked cuts, 59.7 MB MP4. Terverifikasi `verify` PASS.

**Runtime deps:** numpy, Pillow, pycairo, scipy, imageio-ffmpeg (ffmpeg statis ter-bundle). Fonts 8 face OFL. Semua gratis.

---

## 2. Integrasi ke Pipeline Studio (keputusan owner)

**Bukan skill standalone di `creative/`.** Masuk sebagai tool di lapangan yang sudah ada.

### 2.1 Tool di `content-produce` (opsi 3 — seteq, pilihan digerakkan brief)

Baris "Motion graphics / batch render" di `content-produce/SKILL.md` saat ini:

| Kebutuhan | Tool (lisensi) | Perintah inti |
|---|---|---|
| Motion graphics / batch render | Motion Canvas (MIT), HyperFrames (Apache-2.0, pin `@0.8.30`), Remotion | `npx --yes hyperframes@0.8.30 render . --low-memory-mode --workers 1` |

Setelah adopsi:

| Kebutuhan | Tool (lisensi) | Perintah inti |
|---|---|---|
| Motion graphics / batch render | Motion Canvas (MIT), HyperFrames (Apache-2.0, pin `@0.8.30`), Remotion, **Motion Reel Kit (MIT)** | `npx --yes hyperframes@0.8.30 render . --low-memory-mode --workers 1` · `python reelctl.py render` (dari `~/motion-reel-kit`) |

Pemilihan digerakkan brief:
- Butuh audio-visual lock kuat + broadcast grade → **Motion Reel Kit**
- HTML/CSS cepat + Reels 9:16 → **HyperFrames**
- Komponen React → **Remotion**

### 2.2 `content-studio` — tidak diubah

Orchestrator sudah delegasi render ke `content-produce`. Kit masuk sebagai tool yang dipanggil `content-produce`, bukan skill terpisah. Tidak ada perubahan di `content-studio/SKILL.md`.

### 2.3 Thread 1172 (Kreator) — tidak diubah binding

Skill binding existing (`ghost, humanizer, baoyu, claude-design, manim, hyperframes`) sudah mencakup `content-studio` → delegasi ke `content-produce` → kini tahu kit. Tidak perlu bind baru.

### 2.4 Output path — ikut `content-produce`

Kit menulis `out/MOTION_REEL.mp4` di root kit. `content-produce` mewajibkan output di `workspace/output/<slug>/`. Alur:

1. Kit render → `~/motion-reel-kit/out/MOTION_REEL.mp4`
2. `content-produce` copy ke `~/Desktop/Niumination/apps/abstract-studio/workspace/output/<slug>/`
3. QA gate cek di path studio

Tidak ada patch pada kit — copy setelah render.

---

## 3. QA Gate — shot-loop masuk gerbang

**Keputusan owner:** loop `shot` (render satu frame → lihat → perbaiki) masuk gate QA studio.

### Gerbang baru: "Visual Verification Loop"

Tambahkan ke 7 gerbang QA `content-studio`:

| Gerbang | Kriteria | Kit |
|---|---|---|
| 1. Brief sesuai | BRIEF.md lengkap, gerbang ide lolos | — |
| 2. Naskah solid | Hook 3 detik, CTA jelas | — |
| 3. Audio | Loudness −14 LUFS (±1), voice Gemini Charon | — |
| 4. Visual | **3 frame khusus (awal, tengah, akhir) di-render via `shot` dan dilihat manusia** | `python reelctl.py shot <t> /tmp/frame-<t>.png` |
| 5. Platform | Rasio, durasi, caption aman | — |
| 6. Monetization | Satu jalur uang aktif | — |
| 7. Legal | Aset CC0/OFL, lisensi komersial | Fonts OFL, musik sintesis |

Gerbang 4 wajib untuk konten yang dirender dengan Motion Reel Kit. Untuk HyperFrames/Remotion, gerbang 4 bisa discreenshot dari preview.

---

## 4. TOOL_DECISIONS.csv — update

File: `~/Desktop/Niumination/apps/abstract-studio/data/TOOL_DECISIONS.csv`

Baris baru:

```csv
2026-10-11,Motion Reel Kit,1.0.0,MIT,DIPAKAI — motion graphics broadcast-grade,"Audio-visual lock via numpy synthesis. 15 scene renderer, post chain, encode H.264+AAC. Tanpa AE, tanpa footage, tanpa lisensi musik, tanpa API key. QA: doctor READY + shot lihat gambar + verify PASS. Lokasi: ~/motion-reel-kit",2027-01-11
```

---

## 5. Rencana Eksekusi — 4 Fase

### Fase 0 — Keputusan lokasi & approval (SEKAROW)

**One-home rule + pitfall HyperFrames** (pernah ditolak owner: polusi struktur ekosistem): kit **tidak** ditaruh di `~/Desktop/Niumination/`.

Pilih salah satu:
- **Opsi A (disarankan):** `~/motion-reel-kit` — home, permanen, sesuai default kit.
- **Opsi B:** `~/motion-reel-kits/reel-maker-kit` — kalau nanti ada beberapa varian.

Skill bank menyimpan **SKILL.md saja** (menunjuk ke path kit) — bukan copy kit. Konsisten pola existing.

### Fase 1 — Setup & doctor (sekitar 10–20 menit)

```bash
unzip ~/Downloads/reel-maker-kit.zip -d ~/
# hasil: ~/motion-reel-kit/ + ~/reel/ (output referensi, opsional dipindah)
cd ~/motion-reel-kit
bash scripts/setup.sh    # install deps + brew cairo/pkg-config + venv
source .venv/bin/activate
python reelctl.py doctor # HARUS print READY
```

**Risiko & mitigasi:**
- `pycairo` compile dari source di macOS → butuh `brew install cairo pkg-config` + `xcode-select --install` (sudah ditangani `scripts/setup.sh`, dokumentasi `08_TROUBLESHOOTING.md`).
- OOM di 16 GB → `REEL_WORKERS=2`, `REEL_PRESET=fast REEL_CRF=19`.
- Font substitusi diam-diam → `doctor` deteksi; fallback `REEL_NO_EMBED_FONTS=1`.

### Fase 2 — Daftarkan tool ke content-produce + TOOL_DECISIONS (1–2 menit)

1. Edit `~/Desktop/Niumination/skills/content/content-produce/SKILL.md` — tambah Motion Reel Kit ke tabel motion graphics.
2. Edit `~/Desktop/Niumination/skills/content/content-studio/SKILL.md` — tambah gerbang 4 "Visual Verification Loop" ke QA gate.
3. Edit `~/Desktop/Niumination/apps/abstract-studio/data/TOOL_DECISIONS.csv` — tambah baris Motion Reel Kit.
4. Sinkronisasi resmi: `scripts/skill-manifest.py` + `sync-to-agents.sh` (dilarang copy-paste manual).
5. Update `docs/registry/skill-registry.md` lewat generator, jangan edit manual.

### Fase 3 — Verifikasi fungsional (gate, wajib)

```bash
python reelctl.py timeline      # tabel 15 scene, kontigu, cut on beat
python reelctl.py shot 18.9 /tmp/reel-test.png   # 1 frame, 1–3 s
# LIHAT gambar — bukan kode
python reelctl.py sheet         # 25-tile contact sheet
python reelctl.py render        # 3–20 min, 16 GB
python reelctl.py verify        # GATE: decode 1800 frame, wajib PASS
```

**Kriteria adopsi:** `doctor` READY + `shot` menghasilkan gambar yang bisa dilihat + `verify` PASS.

### Fase 4 — (Opsional) Registrasi MCP

Kit punya MCP server 12 tool (`agent/mcp_server.py`). Bisa didaftarkan ke `mcp_servers` di `config.yaml` — **tapi tidak wajib**. Shell path (Fase 3) sudah cukup dan paling andal. Kalau nanti butuh MCP:
- `python agent/mcp_server.py --selftest` harus print PASSED.
- Daftar sebagai `motion-reel-kit` di `mcp_servers`, command = venv python.
- Restart gateway dari shell luar.

---

## 6. Keputusan yang Butuh Approval Owner

1. **Lokasi kit:** `~/motion-reel-kit` (Opsi A) atau lain? — perlu konfirmasi sebelum unzip.
2. **Path integrasi:** Shell only (disarankan) atau + MCP juga?
3. **Skrip:** `scripts/setup.sh` menjalankan `brew install` — butuh password sudo? (Homebrew biasanya tanpa sudo.)
4. **Apakah output referensi `~/reel/` (59 MB MP4 + log) ikut dipindah atau dibiarkan?**

---

## 7. Analisis Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| pycairo compile gagal di macOS 26 | Setup mentok | `brew install cairo pkg-config`; dokumentasi 08 |
| OOM saat render di 16 GB | Encode mati exit 137 | `REEL_WORKERS=2`, preset fast; `profile` cek rencana |
| Font substitusi diam-diam | Teks jelek | `doctor` deteksi + embedded loader |
| Verifikasi butuh lihat gambar | Agen buta desain | Wajib: buka PNG setiap `shot` — unik vs pipeline HyperFrames |
| GPL ffmpeg binary | Tidak ada untuk penggunaan render | Hanya kalau *redistribusi* binary; penggunaan bebas |
| `scripts/setup.sh` butuh akses jaringan | Sekali saja | Teks print "no network at render time" |

---

## 8. Biaya

**$0.00** — semua dependency gratis, ffmpeg ter-bundle, fonts OFL, musik sintesis, tanpa API key, tanpa network saat render. Tidak ada biaya tersembunyi.

---

## 9. Checklist Approval

- [ ] Owner pilih lokasi (Opsi A/B)
- [ ] Owner pilih path (shell / + MCP)
- [ ] Owner izinkan `brew install cairo pkg-config`
- [ ] Setup + doctor READY
- [ ] Tool didaftarkan ke content-produce + QA gate + TOOL_DECISIONS
- [ ] Shot test → lihat gambar
- [ ] Render penuh → verify PASS
- [ ] Laporan verifikasi → `docs/reports/`

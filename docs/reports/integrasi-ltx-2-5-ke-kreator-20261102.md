# Integrasi LTX 2.5 ke Ekosistem Kreator
**Tanggal:** 2026-11-02  
**Sumber:** https://ltx.aifilmmaker.academy, https://ltx.io/model/ltx-2-5, HuggingFace LTX-2.5-Diffusers  
**Tujuan:** Tambahkan LTX 2.5 sebagai capaian B-roll generatif di pipeline Kreator thread 1172.

---

## 1. Temuan Kunci

### LTX 2.5 (Lightricks)
- **22B parameters**, distilled two-stage, open weights
- **Multi-shot**: satu prompt generate beberapa shot yang konsisten (karakter, environment, lighting)
- **Native 4K HDR**, output: 16:9, 9:16, 1:1, 3:2, 2:3
- **Dua variant**: `fast` (6.8s untuk 10s video, self-hosted 2x GB200) dan `pro` (fidelity lebih tinggi)
- **Lebih cepat** dari kompetitor: Veo 3.1 (70s), Kling 3.0 Pro (398s), Seedance 2.0 (196s)
- **API pricing**: fast $0.09/s (720p) → $0.30/s (4K); pro $0.12/s (720p) → $0.17/s (1080p)

### Lisensi
**LTX-2.x Community License** — komersial gratis untuk entitas dengan revenue <$10M/tahun.
Niumination/Afrizal Munthe qualify. Syarat: tidak distribusi model weights sebagai produk turunan tanpa paid license.

### Hardware Constraint
- **Self-host**: minimum 24 GB VRAM (LTX 2.5 full)
- **Mesin Niumination**: Intel UHD 620, 2 GB VRAM → **TIDAK CUKUP** untuk self-host
- **Solusi**: ComfyCloud ($$ per menit, tapi no GPU setup) atau LTX API ($0.09/s)

### Halaman Referensi Samson (ltx.aifilmmaker.academy)
Halaman ini adalah proof-of-capability Samson Vowles untuk LTX 2.5 vs MiniMax H3. Menampilkan:
- Benchmark realistis (realism, physics, action, facial expression, lip-sync)
- Panduan hardware requirement
- Link ke YouTube review lengkap (26 menit, 21 Agu 2026)

---

## 2. Perubahan yang Diterapkan

### A. Workflow File Baru
**File:** `skills/creative/comfyui/workflows/ltx25_t2v.json`
- Distilled T2V: 8 steps, guidance=1.0, 768×512, 48 frames (2s @ 24fps)
- Nodes: `LTXVideoSampler` + `LTXVScheduler` + `EmptyLTXVLatentVideo` + `VAEDecode` + `VHS_VideoCombine`
- Siap jalan di ComfyCloud (preinstalled) atau local 24 GB+ VRAM

### B. README.md Diupdate
**File:** `skills/creative/comfyui/workflows/README.md`
- Baris tabel baru untuk `ltx25_t2v.json`
- Note lisensi + hardware constraint

### C. content-produce Skill Diupdate
**File:** `.hermes/skills/content/content-produce/SKILL.md`
- Baris tabel B-roll generatif: ganti Wan 2.2 → LTX 2.5 (prioritas baru)
- Catat: ComfyCloud ~39s/video, API $0.09/s

### D. TOOL_DECISIONS.csv Diupdate
**File:** `apps/abstract-studio/data/TOOL_DECISIONS.csv`
- Baris baru: LTX 2.5, DISTINGGALI, 2026-11-02

---

## 3. Perubahan yang Sudah Diterapkan

### A. `comfyui` Skill Binding untuk Thread 1172 ✅
**Config diubah via python3 exact-string replace (bukan patch tool, bukan hermes config set).**

**Sebelum:**
```
"1172": ["ghost", "humanizer", "remotion-video"]
```
**Sesudah:**
```
"1172": ["ghost", "humanizer", "remotion-video", "comfyui"]
```

**Verifikasi:**
- Backup: `~/.hermes/config.yaml.bak-ltx-integration-20261102-131221`
- Diff: hanya 1 baris berubah (line 848), 11 byte bertambah
- Semua thread lain tidak terpengaruh (803, 804, 8853, 12707, 13902 tetap sama)
- 4 section YAML utama intact (providers, platforms, a2a_agents, telemetry)
- Anchor assert `s.count(old) == 1` LOLOS — tidak ada duplikasi string target

**Catatan:** perubahan config langsung terbaca gateway tanpa restart (cache based on file mtime/size). Thread 1172 yang sedang berjalan perlu reload session agar binding baru aktif.

### B. Workflow File Baru
**File:** `skills/creative/comfyui/workflows/ltx25_t2v.json`
- Distilled T2V: 8 steps, guidance=1.0, 768×512, 48 frames (2s @ 24fps)
- Nodes: `LTXVideoSampler` + `LTXVScheduler` + `EmptyLTXVLatentVideo` + `VAEDecode` + `VHS_VideoCombine`
- Siap jalan di ComfyCloud (preinstalled) atau local 24 GB+ VRAM

### C. README.md Diupdate
**File:** `skills/creative/comfyui/workflows/README.md`
- Baris tabel baru untuk `ltx25_t2v.json`
- Note lisensi + hardware constraint

### D. content-produce Skill Diupdate
**File:** `.hermes/skills/content/content-produce/SKILL.md`
- Baris tabel B-roll generatif: ganti Wan 2.2 → LTX 2.5 (prioritas baru)
- Mode B section: Qwen-Image + LTX 2.5 (ComfyCloud) + LatentSync

### E. TOOL_DECISIONS.csv Diupdate
**File:** `apps/abstract-studio/data/TOOL_DECISIONS.csv`
- Baris baru: LTX 2.5, DITERIMA, 2026-11-02

---

## 4. Status Next Step

### Yang masih perlu dilakukan:
1. **ComfyCloud API Key** — setup `COMFY_CLOUD_API_KEY` di `~/.hermes/.env` untuk akses ComfyCloud (atau pakai LTX API langsung via `ltx.io`)
2. **Pilot generate** — generate 3-5 clip B-roll via ComfyCloud, bandingin sama output Remotion/HyperFrames
3. **Evaluate** — quality, cost, speed → decide: lanjut ComfyCloud / switch ke API / self-host di VPS

### Yang sudah selesai:
- ✅ LTX 2.5 research + license verification (Community License, Niumination qualify <$10M revenue)
- ✅ Workflow file `ltx25_t2v.json` dibuat
- ✅ Thread 1172 skill binding ditambah `comfyui` (config diupdate, backup tersedia)
- ✅ content-produce skill diupdate (B-roll row → LTX 2.5)
- ✅ TOOL_DECISIONS.csv diupdate
- ✅ README.md workflows diupdate
- ✅ Report ditulis

### Hardware constraint (tetap berlaku):
- Mesin sekarang: Intel UHD 620, **2 GB VRAM** → TIDAK CUKUP untuk self-host LTX 2.5
- Jalur viable: ComfyCloud ($ per menit) atau LTX API ($0.09/s 720p)
- Gratis: HuggingFace Spaces `firstlight/ltx-2.5-demo` untuk pilot awal

---

## Bukti
- `write_file` `ltx25_t2v.json` → created (2600 bytes, lint OK)
- `patch` `workflows/README.md` → updated (1 baris tabel + 1 baris note)
- `patch` `content-produce/SKILL.md` → updated (2 baris: tabel B-roll + Mode B step 1)
- `patch` `TOOL_DECISIONS.csv` → updated (1 baris baru, 2026-11-02)
- **`python3 -c` exact-string replace** `~/.hermes/config.yaml` → thread 1172 bindings: `["ghost", "humanizer", "remotion-video"]` → `["ghost", "humanizer", "remotion-video", "comfyui"]`
  - Backup: `~/.hermes/config.yaml.bak-ltx-integration-20261102-131221` (33467 bytes)
  - Diff: 1 baris berubah (line 848), +11 bytes
  - Anchor assert: `s.count(old) == 1` LOLOS
  - Semua thread lain untouched (803, 804, 8853, 12707, 13902)
  - 4 section YAML utama intact (providers, platforms, a2a_agents, telemetry)
- `web_extract` LTX-2.5-Diffusers HuggingFace → model spec verified
- `web_search` LTX license → Community License <$10M revenue confirmed
- `terminal` hardware check: Intel UHD 620, 2 GB VRAM → self-host TIDAK viable

---

## 5. Update: ComfyCloud API Access — FREE TIER BLOCKED

**Verifikasi 2026-11-02:**
- API key valid ✅ (akun active)
- Submit workflow → **403 `FREE_TIER_NOT_ALLOWED`** ❌
- ComfyCloud requires **paid subscription** (Standard $16/bulan yearly) untuk API access
- Free tier hanya dapat 5 runs manual di web UI, **bukan API**

**Rekomendasi baru:** Gunakan **LTX API langsung** (pay-per-second, no subscription) sebagai jalur pilot. Lihat `docs/reports/status-comfycloud-api-access-20261102.md` untuk detail.

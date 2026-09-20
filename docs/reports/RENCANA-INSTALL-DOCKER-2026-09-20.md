# Rencana — Instalasi Docker di Mac Niumination (20 Sep 2026)

**Status:** RENJA (belum dieksekusi) — menunggu approval
**Target:** Mac i5-10310U · macOS 26.5 · x86_64 · 16 GB RAM · disk 128 GB (20 GB free) · Homebrew 7.0.4
**Alasan instalasi:** membuka jalur Docker dari rencana adopsi Content Studio
(ComfyUI opsional, Postiz/Ghost self-host, LibreChat v4.1 Free Tier, n8n) — FASE 4.

---

## 1. Temuan penting (dipengaruhi kondisi mesin ini)

1. **RAM: 16 GB, terpakai ±15 GB saat idle, sisanya cuma 165 MB.**
   → VM Docker butuh 4–8 GB. **Ini bottleneck utama.** Tanpa disiplin, mesin akan swap/lumpuh.
2. **Disk: 20 GB free** → cukup untuk image Docker (Postiz + Ghost ±3–5 GB).
3. **macOS 26.5 (Tahoe) + Homebrew x86_64 (Intel, bukan arm64)** → tooling Apple Silicon
   (OrbStack, Docker Desktop baru) **tidak bisa dipertimbangkan** — harus jalur Intel.
4. **Docker Desktop 4.91 masih rilis build "Mac with Intel chip"** (release notes Sep 2026),
   tapi butuh VMware/hypervisor lama — di macOS 26 kemungkinan besar bermasalah.
   **Risiko, bukan jalan utama.**
5. **QEMU (11.1.1) tersedia di Homebrew** → jalur "engine murni CLI" paling kompatibel
   dengan macOS versi ini di Mac Intel.
6. Load saat ini **15.78 (sangat tinggi)** — semua instalasi & start VM dilakukan
   **hanya setelah load < 5 dan RAM free > 4 GB**.

## 2. Tiga opsi, urut rekomendasi

### Opsi A (REKOMENDASI) — Colima + QEMU (CLI, headless, terkecil)
```
brew install colima qemu
colima start --vm-type qemu --cpu 2 --memory 4   # VM di belakang, tanpa GUI
docker context use colima
docker run hello-world
```
- Pro: tidak ada app GUI → tidak ada "Docker Desktop running di menu bar" yang
  menggedor RAM; resource bisa dipatok mati (4 GB); kompatibel terbaik di macOS 26
  (QEMU engine tidak bergantung hypervisor lama); uninstall bersih (`colima stop`).
- Kon: tidak ada GUI image management (pakai `docker` CLI — semua tool Content Studio
  memang berbasis CLI/compose, jadi tidak masalah).
- Biaya: ±0 (bottled, gratis).

### Opsi B — Docker Desktop (cask `docker-desktop` 4.91)
```
brew install --cask docker-desktop
```
- Pro: GUI familiar.
- Kon: build Intel di macOS 26 kemungkinan rusak (hypervisor lama tidak diperbarui
  untuk Tahoe) → **risiko tidak jalan**; RAM hungry (default 2 GB–8 GB, GUI tetap
  running); lisensi: gratis untuk individu/kecil (< 250 staff / revenue < $10 jt).
- Hanya dipilih kalau Opsi A gagal total.

### Opsi C — `docker` CLI via Homebrew formula (tanpa VM lokal)
```
brew install docker   # CLI 29.8.1
```
- Hanya client. Bekerja hanya kalau ada remote daemon (mis. VPS murah atau
  `orb`-style service). **Untuk Mac ini: bukan jawaban utuh** — tetap butuh VM (Opsi A/B).
- Berguna sebagai klien bila nanti ada VPS/Cloud Run daemon.

## 3. Konfigurasi wajib demi Mac ini (bagian mana pun yang dipilih)

| Aturan | Nilai | Alasannya di Mac ini |
|---|---|---|
| RAM VM | **4 GB** (jangan default 8) | sisa RAM hanya ~1.6 GB di idle |
| CPU VM | 2 core | i5-10310U 8 thread sudah ramai (load 15+) |
| Disk image | 15 GB cap | 20 GB free → sisakan buffer |
| Auto-start | **MATI** | VM jangan hidup saat boot; hanya saat perlu (hemat RAM) |
| Image pruning mingguan | `docker system prune -f` via cron | jaga 20 GB tidak penuh |
| Jadwal pakai | hanya saat load < 5 & RAM free > 4 GB | atur manual, bukan cron |
| Kebutuhan konten | Postiz / Ghost / n8n / ComfyUI | image yang akan dipakai (FASE 4) |

## 4. Mitigasi & dampak

| Risiko | Mitigasi |
|---|---|
| RAM swap → Telegram gateway lumpuh | patok VM 4 GB + auto-start mati + start hanya manual saat idle |
| macOS 26 hypervisor Intel bermasalah | Opsi A (QEMU) = paling kompatibel; Opsi B = cadangan, siapkan rencana mundur |
| Disk 20 GB penuh oleh image | pruning cron mingguan + `docker system df` tiap pakai |
| Install saat Mac kerja berat | **jangan eksekusi sekarang** (load 15.78); jadwalkan setelah proses berat selesai |
| QEMU lambat di x86 (image pull & build) | setujui trade-off: ini mesin CPU-only, image besar (ComfyUI) tetap berat — prioritas Postiz/Ghost (ringan) |

## 5. Langkah eksekusi (SIAP, menunggu "gas")
1. Cek prasyarat: `df -h / | awk 'NR==2{print $4}'` ≥ 15 GB, load < 5, RAM free > 4 GB
2. `brew install colima qemu`
3. `colima start --vm-type qemu --cpu 2 --memory 4 --disk 15`
4. Uji: `docker run --rm hello-world` → expect "Hello from Docker"
5. Setup pruning cron (ringan): `docker system prune -f` mingguan
6. Smoke test FASE 4: `docker compose up -d postiz` (tanpa deploy, hanya cek container jalan)
7. Verifikasi RAM: `top -l1 | grep PhysMem` — pastikan tidak swap (`Swap used: 0`)

**Alternatif cepat (1 perintah):** `brew install colima qemu && colima start -0 4`
(VM 4 GB) — tapi hanya **setelah** kondisi prasyarat di langkah 1 terpenuhi.

## 6. Bukti (inspeksi, tanpa instalasi apa pun)
- `brew --version` → Homebrew 7.0.4, x86_64; `sw_vers` → macOS 26.5 (25F71)
- `brew info colima` → 0.10.3 bottled; `brew info qemu` → 11.1.1; `brew info docker` → 29.8.1;
  `brew info --cask docker` → Docker Desktop 4.91.0,239619 "Mac with Intel chip" tersedia di release notes Sep 2026
- `command -v docker/colima/orbstack/podman` → semua TIDAK ada; `/Applications` → tidak ada app Docker/Orb
- `df -h /` → 20 GB free; `top -l1` → PhysMem 15G used, 165M unused, load 15.78

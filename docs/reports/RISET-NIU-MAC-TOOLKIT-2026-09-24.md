# Riset Niu Mac Toolkit (niu-mac-toolkit.zip)

**Tanggal:** 2026-09-24 | **Sumber:** ~/Downloads/niu-mac-toolkit.zip | **Versi:** 1.0.0
**Pemicu:** User minta pelajari isi zip

---

## 1. Ringkasan Eksekutif

**Niu Mac Toolkit** adalah script terminal interaktif (Bash) untuk health check, safe cleanup, setup developer, audit Hermes dan audit Hackintosh/OpenCore — **sangat selaras dengan prinsip safety/verification-first** ekosistem kita.

- **Jenis:** Bash script (ni-mac.sh 472 baris) + install.sh + README + Brewfile
- **Target:** ThinkPad X13 Yoga Gen 1 + macOS Tahoe, adaptif ke Mac lain
- **Safety model:** **Read-only dulu**, PREVIEW/DRY-RUN default, setiap mutasi butuh konfirmasi eksplisit, banyak pembatasan berisiko
- **Kesesuaian dengan ekosistem Niumination:** High — cocok sebagai alat maintenance macOS lokal.

---

## 2. Struktur File

| File | Ukuran | Deskripsi |
|---|---|---|
| `niu-mac-toolkit/niu-mac.sh` | 20.1 KB (472 baris) | Script inti, menu interaktif + CLI noninteraktif |
| `niu-mac-toolkit/install.sh` | 379 B (11 baris) | Symlink ke `~/.local/bin/niu-mac`, tambah PATH |
| `niu-mac-toolkit/README.md` | 3.3 KB (132 baris) | Dokumentasi penggunaan + safety principles |
| `niu-mac-toolkit/Brewfile` | 1.3 KB (31 baris) | Daftar paket Homebrew (CLI + GUI) |

---

## 3. Prinsip Keamanan (Safety Model)

Toolkit ini **sangat berhati-hati** — selaras Hard Rules kita:

- **Default PREVIEW/DRY-RUN** (`DRY_RUN=1` awal) — semua command ditampilkan dulu, tidak dieksekusi
- **Mutasi wajib konfirmasi** (`confirm()` y/N) + `execute_after_confirm()` + `set_live_for_action()` (hanya saat di-confirm)
- **Read-only heavy**: health report, storage analysis, OpenCore audit, security audit — tidak mengubah sistem
- **Pembatasan eksplisit (tidak diotomatisasi):** EFI, config.plist, NVRAM, BIOS, SIP, SMBIOS, partisi, hibernatemode, darkwake, resize APFS/Windows, update macOS/OpenCore/kext, CFG Lock, USB map, CPUFriend, NVMe patches, YogaSMC, FileVault activation, charge threshold, perubahan SMBIOS, secrets/provider/channel Hermes
- **Cleanup aman:** hanya `brew cleanup --prune=30`, `pnpm store prune`, `npm cache verify`, `uv cache prune`, `cargo cache --autoclean` (jika ada), Docker prune **tanpa `-a` dan tanpa `--volumes`**, thinning snapshot Time Machine **hanya jika ruang kritis + konfirmasi**, Trash dengan konfirmasi eksplisit
- **Redaksi sensitif:** laporan auto-redact Serial Number, Hardware UUID, Provisioning UDID (`sed` replace ke `[REDACTED]`)
- **Hermes:** **tidak pernah membaca `.env`** (hanya cek ada/tidak + permission 600), tidak mengubah provider/token/channel/config otomatis
- **File permission ketat:** `chmod 700` state/backup/reports, `chmod 600` log & backup `.env`/config sensitif

---

## 4. Fitur Utama

| Menu | Tipe | Fungsi |
|---|---|---|
| **1. Health report lengkap** | Read-only | SwVers, uname, SPHardware, CPU, disk/APFS/NVMe, Graphics/Metal, Battery/pmset, sleep/wake/assertions (120 baris log), memory pressure/vm_stat, top CPU/RAM (25), home sizes (30), snapshots, brew services, LaunchAgents, systemextensions, EFI scan, Hermes/Ollama/Colima/Docker status, auto-redact + **Automated observations** (free space <30GB critical, <50GB warning) |
| **2. Storage analysis** | Read-only | Hitung node_modules/.next/target/dist/.gradle/.venv + cache (CocoaPods, npm/pnpm, cargo, gradle, ollama) — tidak hapus |
| **3. Safe cleanup interaktif** | Mutasi (confirm) | 9 opsi cleanup bertahap, preview dulu |
| **4. Backup konfigurasi** | Read-only-ish | Backup `.zshrc`, `.gitconfig`, `.config/`, Brewfile, `.hermes/config.yaml` (chmod 600), **EFI OC** (PRIVATE, chmod go-rwx, warning jangan upload publik) |
| **5. Instalasi tools adaptif** | Mutasi (confirm) | 6 profil: Core CLI, Niumination dev, GUI, Colima, All-in-one, Brewfile |
| **6. Konfigurasi Colima terbatas** | Mutasi (confirm) | Adaptive RAM (≤8GB→3GB, else 4GB), CPU 2, disk 30GB, **tidak auto-start**, stop dulu jika running |
| **7. Audit Hermes** | Read-only + minor fix | Cek version, `~/.hermes/` size, `.env` exists (tidak dibaca), permission .env (harus 600), fix permission jika konfirmasi, proses running, Docker ps |
| **8. Audit OpenCore/Hackintosh** | Read-only | Scan EFI (OC/Tools/ocvalidate, plutil -lint), SPDisplays/NVMe/Power, pmset, peringatan tidak ubah EFI |
| **9. Power audit + preset konservatif** | Mutasi (confirm) | `pmset -a powernap 0`, `womp 0` (tidak ubah hibernatemode/darkwake) |
| **10. Security/update audit** | Read-only | csrutil, spctl, fdesetup, firewall state, softwareupdate --list, brew outdated, warning FileVault Hackintosh |
| **11. Baseline** | Read-only | health + storage + security sekaligus |

CLI noninteraktif: `health`, `storage`, `opencore`, `hermes`, `security`, `backup`, `help`.

---

## 5. Analisis Relevansi ke Ekosistem Niumination

| Aspek | Penilaian | Alasan |
|---|---|---|
| **Safety/verification-first** | ★★★★★ Sangat cocok | Selaras Hard Rules (approval sebelum mutasi, read-only dulu, redaksi sensitif). Lebih hati-hati dari kebanyakan script maintenance. |
| **Dokumentasi & disiplin DOX** | ★★★★★ | README terstruktur, safety principles jelas, lokasi data terdefinisi (`~/.local/state/`, `~/Documents/NiuMacReports/`, `~/Documents/NiuMacBackups/`) |
| **Audit Hermes** | ★★★★★ | Cek `.env` tanpa baca isi, validasi permission 600, cek proses, Docker — sesuai kebijakan kredensial kita (Rule 6 SOUL). |
| **Hackintosh/OpenCore awareness** | ★★★★☆ | Sangat berguna (ThinkPad target) — read-only ketat, warning jangan publish EFI (mengandung SMBIOS/UUID). Untuk MBP (native Mac) bagian OpenCore bisa di-skip. |
| **Safe cleanup** | ★★★★★ | Paling aman dibanding `brew cleanup -s`/prune agresif. Docker tanpa `-a`/`--volumes`, snapshot thinning hanya jika kritis + konfirmasi. Sesuai prinsip "deletion over addition" tapi terkontrol. |
| **Tidak tumpang tindih** | ★★★★★ | Tidak konflik dengan cron/hermes/9router/MC. Alat lokal maintenance, bukan agent orkestrasi. Bisa diletakkan di `~/bin` atau `.local/bin`. |

---

## 6. Kesimpulan

**Layak diadopsi (simpan di ekosistem)** — terutama untuk maintenance rutin Mac lokal.

**Rekomendasi aksi:**
1. **Simpan sebagai referensi** — sudah di-zip, bisa juga copy ke `tools/niu-mac-toolkit/` atau `docs/references/niu-mac-toolkit-2026-09-24/` (sesuai pola skill adopsi). Tapi zip ini baru, belum di-commit.
2. **Tidak perlu integrasi ke Hermes** — ini CLI standalone, user-run manual (sengaja). Cocok seperti itu.
3. **Bisa di-install**: `bash install.sh` → symlink `~/.local/bin/niu-mac`. PATH check.
4. **Untuk MBP native**: menu OpenCore (8) bisa dilewati, sisanya relevan (health, storage, cleanup aman, Hermes audit, security).

**Nilai tambah:** safety modelnya bisa jadi **referensi** untuk menulis script maintenance lain di ekosistem (dry-run default + konfirmasi eksplisit + read-only-first).

**File zip:** `~/Downloads/niu-mac-toolkit.zip` (24.9 KB, 4 file) — sudah dipelajari. Tidak ada eksekusi, hanya analisis read-only.

MEDIA:/tmp/niu-mac-toolkit-study/niu-mac-toolkit/README.md
MEDIA:/tmp/niu-mac-toolkit-study/niu-mac-toolkit/niu-mac.sh
MEDIA:/tmp/niu-mac-toolkit-study/niu-mac-toolkit/install.sh
MEDIA:/tmp/niu-mac-toolkit-study/niu-mac-toolkit/Brewfile
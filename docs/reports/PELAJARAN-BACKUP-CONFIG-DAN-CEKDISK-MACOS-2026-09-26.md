# Pelajaran Operasional: Backup Konfigurasi & Cek Disk di macOS

**Tanggal:** 2026-09-26 | **Sumber:** insiden saat review skrip maintenance pihak ketiga
**Catatan:** Pelajaran generik. Skrip spesifik yang memicu temuan ini sudah dihapus dari Downloads dan tidak disimpan di ekosistem — hanya prinsip keamanannya yang dipertahankan di sini.

---

## 1. Jangan pernah backup `~/.config` wholesale ke folder yang ter-sync iCloud

### Gejala
Skrip maintenance menawarkan "backup konfigurasi" yang menyalin seluruh `~/.config` ke `~/Documents/<toolkit-backup>/`. Di macOS, `~/Documents` **default ter-sync iCloud Drive** (`~/Library/Mobile Documents/com~apple~CloudDocs/Documents`).

### Risiko nyata
`~/.config` bukan cuma konfigurasi — berisi kredensial:

| File | Nature |
|---|---|
| `~/.config/gh/hosts.yml` | OAuth token GitHub CLI (perm 600) |
| `~/.config/*/*.env` | API key provider (beberapa framework AI tool menyimpan di sini) |
| `~/.config/gcloud/`, `~/.config/netlify/`, `~/.config/railway/` | token cloud platform |

Backup wholesale = **kredensial ter-upload ke iCloud** (server Apple, tersinkron ke semua device pemilik, termasuk yang hilang atau dipinjam orang). `chmod 700` pada folder lokal **tidak menghentikan sync**.

### Aturan yang harus berlaku
1. **Backup config = whitelist, bukan blacklist.** Salin hanya file yang benar-benar non-rahasia (`.zshrc`, `.gitconfig`, `config.yaml` yang sudah disanitasi).
2. **Lokasi backup di luar path iCloud-sync.** Pakai `~/.local/state/<tool>/` atau `~/.cache/<tool>/` — bukan `~/Documents/`, `~/Desktop/`.
3. **Selalu audit isi sebelum copy.** `find <src> \( -name '*.env' -o -name 'hosts.yml' -o -name '*credentials*' -o -name '*.key' \) -type f` → jika ada, jangan copy blanket.
4. **Verifikasi sync status sebelum menulis backup.** Cek `~/Library/Mobile Documents/` ada atau tidak.
5. **`chmod` bukan pengganti redaksi.** Permission hanya melindungi di disk lokal; tidak menyentuh salinan yang sudah keluar lewat sync.

---

## 2. Di macOS APFS, `df -k /` salah volume — cek `/System/Volumes/Data`

### Gejala
Skrip storage-monitor memakai `df -k /` untuk assess "boot volume free space", lalu memberi warning kalau free < 40 GB.

### Kenapa salah
macOS APFS punya **container bersama** yang di-mount sebagai beberapa volume:

| Path | Isi | Sifat |
|---|---|---|
| `/` | System volume — **read-only** (SSV) | Hampir tidak pernah berisi data user |
| `/System/Volumes/Data` | **Data volume** — semua data user | Ini yang benar-benar penuh/menipis |

`df -k /` melaporkan kapasitas **system volume (read-only)**, bukan data user. Karena keduanya share container yang sama, angkanya **selalu sama kecilnya** → warning free-space **selalu trigger** (false positive permanen), bahkan kalau data volume masih lega.

### Aturan yang harus berlaku
1. **Untuk assess ruang user, cek `/System/Volumes/Data`:**
   ```bash
   df -k /System/Volumes/Data | awk 'NR==2 {print $4, $5}'
   ```
2. **Untuk assess upgrade OS, cek `/` juga** (system volume butuh headroom, tapi itu tetap share container).
3. **Jangan pernah pakai `df /` sebagai proxy untuk "boot volume"** di macOS modern (APFS, sejak 2017).
4. **Verifikasi dengan `df -h | grep -E "Data|^/dev"`** untuk melihat semua volume sebelum menyimpulkan.

---

## 3. Pola umum: audit kode sebelum mengadopsi

Pelajaran turunan dari kedua temuan di atas:

- **Read the code, not the README.** README yang klaim "aman, tidak baca secrets, no destructive ops" bisa bertentangan dengan kode aktual. Verifikasi klaim safety dengan `grep` pada pola berbahaya: `ditto`, `cp -p`, `rm -rf`, `sudo`, `curl | bash`, `df -k /`.
- **Cek default location sebelum approve backup path.** Path `~/Documents` dan `~/Desktop` secara default masuk iCloud sync di macOS.
- **Cek volume semantics sebelum percaya threshold.** `df` di APFS tidak intuitif.
- **Tool yang'=>'aman' untuk mesin lain belum tentu aman untuk mesin ini.** OpenCore/Hackintosh audit tidak relevan di Mac native; power tweak yang sudah diterapkan tidak perlu diulang.

---

## Bukti

- Insiden 26 Sep 2026: review skrip maintenance pihak ketiga, 4 temuan (kredensial → iCloud, salah volume `df`, permission `cp -p` preserve 755, symlink ke `/tmp` yang ephemeral)
- Pelajaran ditulis ulang tanpa nama tool untuk mencegah future agent reach-for tanpa konteks
- Skrip asli: dihapus dari Downloads (SHA-256 dicatat saat hapus), tidak diarsipkan
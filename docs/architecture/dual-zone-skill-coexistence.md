# Dual-Zone Skill Coexistence Architecture — Niumination

> **Tanggal:** 2026-09-19  
> **Status:** AKTIF & DIVERIFIKASI (159 skills, 789 files, 0 conflict)  
> **Pemilik:** Afrizal Munthe (Niumination)  
> **Implementasi:** Hermes Native Config + `scripts/promote-skills.py` + `scripts/up-eco-lightfix.sh`

---

## 1. Latar Belakang & Masalah

Sebelum arsitektur ini diterapkan, terdapat dikotomi yang berisiko:
1. **Target Aktif Runtime (`~/.hermes/skills/`)**:
   - Tempat Hermes membaca skill saat inferensi (Level 0 Catalog & Level 1 `skill_view`).
   - Tempat skill baru lahir (via session, autoskills, atau CLI).
   - Tempat patch/update sering terjadi saat agent belajar di sesi runtime.
   - **Risiko**: Bukan repository Git. Jika crash, reset, atau dibersihkan oleh curator, perubahan runtime hilang tanpa jejak.
2. **Bank Skill Pasif (`~/Desktop/Niumination/skills/`)**:
   - Sumber kebenaran ekosistem di Git (memiliki riwayat commit).
   - **Risiko**: Sebelumnya sinkronisasi hanya berjalan satu arah (`bank → target`). Akibatnya, pembaruan di target tidak terserap ke bank, bahkan berkas pendukung (`references/`, `scripts/`) di target tertinggal dan tidak memiliki backup.

---

## 2. Solusi: Dual-Zone Coexistence

Arsitektur ini menghubungkan kedua zona menjadi satu ekosistem yang hidup berdampingan secara otomatis dan aman:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                            HERMES RUNTIME ZONE                              │
│                                                                             │
│  • Bundled Skills (54)            • Native external_dirs:                   │
│  • Active Sessions / Autoskills      [/Users/.../Niumination/skills]        │
│  • Local Target (~/.hermes/skills)• Native create_dir:                      │
│                                      [.../skills/ecosystem]                 │
└───────────────────────┬─────────────────────────────▲───────────────────────┘
                        │                             │
       [1] TWO-WAY REVERSE SYNC                       │ [3] FORWARD SYNC
           (Promote & Absorb)                         │     (Non-destructive)
           • New skills                               │     • rsync --checksum
           • Target-only references/scripts           │     • Manifest validation
           • Modified files (patches)                 │     • Lockfile & Registry
                        │                             │
┌───────────────────────▼─────────────────────────────┴───────────────────────┐
│                           CENTRAL BANK VAULT (GIT)                          │
│                                                                             │
│  • ~/Desktop/Niumination/skills/ (159 skills, 789 files)                    │
│  • manifest.json (SHA-256 per file)                                         │
│  • INDEX.md (auto-generated catalog)                                        │
│  • Git history, immutable versioning, zero credential leaks                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Komponen Utama

### A. Hermes Native Integration (`~/.hermes/config.yaml`)
Konfigurasi runtime diarahkan agar mengenali Bank tanpa mengabaikan local storage:
```yaml
skills:
  create_dir: /Users/zaryu/Desktop/Niumination/skills/ecosystem
  external_dirs:
    - /Users/zaryu/Desktop/Niumination/skills
  template_vars: true
  inline_shell: false
  inline_shell_timeout: 10
  guard_agent_created: false
```
- **`skills.create_dir`**: Skill baru yang dibuat oleh agent via tool `skill_manage` langsung ditulis ke Bank (`skills/ecosystem/`), sehingga otomatis terlacak Git.
- **`skills.external_dirs`**: Bank skill langsung dipindai oleh runtime Hermes sejak startup.

### B. Two-Way Convergence Engine (`scripts/promote-skills.py`)
Mekanisme otomatis yang menyerap semua aktivitas runtime kembali ke Bank:
1. **Promote New Skills**: Mendeteksi skill baru di target (dari autoskills, repositori eksternal, atau input chat manual) dan menyalinnya ke domain yang sesuai di Bank.
2. **Promote New Support Files (`target_only`)**: Menyerap berkas baru di `references/`, `scripts/`, `templates/` yang dibuat di target ke dalam skill terkait di Bank (33 berkas pendukung terselamatkan).
3. **Absorb Modifications (Reverse-Sync)**: Jika ada file di target yang disunting (misal perbaikan SOP pada `SKILL.md`), file tersebut otomatis diserap ke Bank asalkan bersih dari kredensial.
4. **Credential & Injection Shield**: Setiap berkas yang akan diserap di-scan terhadap token rahasia (`sk-`, `ghp_`, DB URI, private key, dsb.). Berkas yang memuat kunci asli ditolak dari Git.

### C. Never-Clobber Guard (`scripts/sync-guard.py`)
- Memonitor status 159 skill bank.
- Melacak hash target paska-sinkronisasi (`.sync-state.json`).
- Menjamin tidak ada file target yang tertimpa secara buta jika terjadi tabrakan.

### D. Automated Pipeline & Cron (`scripts/up-eco-lightfix.sh`)
Pipeline dijalankan setiap malam (23:30) atau dipicu manual:
1. **Penjaga**: Cek status integritas bank & target.
2. **Promosi & Penyerapan**: Jalankan konvergensi runtime → bank.
3. **Manifest & INDEX**: Hitung ulang SHA-256 dan perbarui `manifest.json` serta `INDEX.md`.
4. **Forward Sync**: Salin file bank ke target menggunakan `rsync --checksum` (non-destructive).
5. **Verifikasi Tiga Arah**: Pastikan filesystem bank, target, dan manifest identik 100%.
6. **Autocommit**: Rekam churn timestamp secara aman.

---

## 4. Bukti Verifikasi Operasional (19 Sep 2026)

- **Kapasitas Bank**: 159 skills, 789 files (0 mismatch).
- **Kapasitas Target**: 213 skills (159 disinkronkan dari bank + 54 bawaan Hermes).
- **Status Penjaga**: 159 aman, 0 konflik, 0 missing.
- **Integritas Target**: 789 berkas diverifikasi lulus hash SHA-256.

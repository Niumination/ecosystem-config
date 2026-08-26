# 🛡️ JCODE SAFETY PROTOCOL — Mencegah Root Ecosystem Tertimpa Proyek Lain

> **Dibuat:** 2026-08-26 — Setelah insiden root `~/Desktop/Niumination` tertimpa `cc-acehtengah` (JCode mengeksekusi di dir root bukan di `services/cc-acehtengah/`).

## 🚨 Insiden yang Terjadi

- **Gejala:** Root repo `Niumination` (remote seharusnya `ecosystem-config`) tiba-tiba punya `src/`, `prisma/`, `package.json`, `next.config.ts` — semua milik `cc-acehtengah`.
- **Penyebab:** JCode (atau agen lain) `cd` ke root lalu menjalankan perintah yang seharusnya di `services/cc-acehtengah/`. Atau `git clone`/`checkout` cc-acehtengah langsung ke root.
- **Dampak:** BACKLOG.md & AGENTS.md di-root ke-**overwrite** dengan konten cc-acehtengah. Remote `origin` berubah jadi `cc-acehtengah`.

## ✅ ATURAN WAJIB UNTUK JCODE (DAN SEMUA AGEN)

### 1. SELALU `cd` KE SUBFOLDER YANG TEPAT SEBELUM EKSEKUSI

```bash
# ✅ BENAR — cc-acehtengah ada di services/
cd ~/Desktop/Niumination/services/cc-acehtengah
npm run dev

# ❌ SALAH — jangan pernah jalankan perintah proyek di root
cd ~/Desktop/Niumination
npm run dev  # INI AKAN MENCAMPUR FILE PROYEK KE ROOT ECOSYSTEM
```

### 2. VERIFIKASI `pwd` SEBELUM `git` / `npm` / `npx`

Sebelum menjalankan perintah yang memodifikasi filesystem, **selalu jalankan `pwd`** dan pastikan:
- Root ecosystem: `~/Desktop/Niumination` → remote HARUS `ecosystem-config`
- Proyek: `~/Desktop/Niumination/services/cc-acehtengah` → remote `cc-acehtengah`

```bash
pwd
git remote -v  # pastikan cocok dengan folder saat ini
```

### 3. JANGAN PERNAH `git clone` / `git checkout` KE ROOT

```bash
# ❌ SALAH — clone ke root menimpa struktur ecosystem
git clone git@github.com:Niumination/cc-acehtengah.git ~/Desktop/Niumination

# ✅ BENAR — clone ke subfolder yang sudah ada
git clone git@github.com:Niumination/cc-acehtengah.git ~/Desktop/Niumination/services/cc-acehtengah
```

### 4. JIKA MENEMUKAN FILE ANEH DI ROOT (src/, prisma/, package.json)

**STOP. JANGAN `git add` / `git commit` / `git push`.** Laporkan ke user:

```
⚠️ ANOMALI: File cc-acehtengah (src/, prisma/) terdeteksi di root ecosystem.
Remote saat ini: <remote>
Tindakan: HENTIKAN, jangan push. Tunggu instruksi user.
```

### 5. BACKLOG.md & AGENTS.md HANYA DI ROOT `ecosystem-config`

- Jangan tulis BACKLOG.md di `services/cc-acehtengah/` (itu punya AGENTS.md sendiri untuk cc-acehtengah).
- Jangan tulis AGENTS.md root dengan konten proyek spesifik.

## 🔧 DETEKSI OTOMATIS (Script Guard)

Tambahkan ke `~/.zshrc` / `~/.bashrc`:

```bash
# Guard: cegah eksekusi npm/git di root ecosystem jika remote salah
guard_ecosystem() {
  local dir=$(pwd)
  if [[ "$dir" == "$HOME/Desktop/Niumination" ]]; then
    local remote=$(git remote get-url origin 2>/dev/null)
    if [[ "$remote" != *"ecosystem-config"* ]]; then
      echo "⚠️ REMOTE SALAH DI ROOT: $remote"
      echo "Hentikan. Remote root harus ecosystem-config."
      return 1
    fi
  fi
}
# Jalankan sebelum git/npm
alias git='guard_ecosystem && git'
```

## 📋 CHECKLIST RECOVERY (JIKA TERJADI LAGI)

1. **JANGAN PANIC, JANGAN PUSH.**
2. Cek `git remote -v` — pastikan root = `ecosystem-config`.
3. Jika remote salah: restore `.git` dari `.git-backup-*` terdekat.
4. Hapus/move file proyek yang bocor ke `/tmp/quarantine/`.
5. `git reset --hard origin/main` untuk bersihkan working tree.
6. Apply perubahan sah (BACKLOG.md) dari backup `/tmp/`.
7. `git push origin main` (fast-forward harus aman karena root sudah bersih).

---

**Ingat:** Root `~/Desktop/Niumination` adalah **INDEX/ORCHESTRATION REPO** (`ecosystem-config`). Bukan tempat menjalankan aplikasi. Semua proyek ada di subfoldernya masing-masing.

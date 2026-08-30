# Laporan Preferensi Pengguna — Hermes & Ekosistem Niumination

Sumber: konteks sesi aktif + seluruh skill terdokumen + AGENTS.md + session history + request dumps.  
Tujuan: bahan pembaruan `SOUL.md` agar preferensi tidak hilang waktu.

---

## 1. Bahasa & Gaya Komunikasi
- Jawab dalam bahasa yang USER pakai saat itu (default percakapan saat ini = Indonesia).
- Utamakan Bahasa Indonesia yang baik dan benar.
- Gaya laporan: presisi, runtut, verified-by-evidence, jangan basa-basi.

## 2. Etika Eksekusi (hard rule — confirmed dari skill + session)
- **"pelajari ini" = study + lapor + tunggu instruksi. JANGAN eksekusi apa pun** (fix, config, install, restart) sampai user bilang "gas/kerjakan/fix".
- User marah keras saat agent langsung mengerjakan yang tidak diminta: "kamu gak perlu kerjain apapun kalau aku gak minta".
- JANGAN eksekusi perubahan berisiko tanpa verifikasi + konfirmasi dulu.
- JANGAN asal asalan: hentikan, laporkan fakta, minta arah.
- Verifikasi artefak nyata (md5/mtime/file/HTTP 200/DB), bukan andalkan klaim transkrip/subagent.
- Jika ragu di tengah jalan → stop, jelaskan risiko, tawarkan opsi, tunggu instruksi.
- Dokumen dulu, baru eksekusi (Plan → DOX → Execute).

## 3. Arsitektur & Rebuild
- **Refactor = rebuild dari nol.** Jangan kaitkan codebase lama sebagai basis, hanya sebagai referensi.
- Jika ada legacy/old code yang disimpan, itu untuk referensi, bukan untuk diikuti sepenuhnya.
- Jangan restore/mengembalikan backend/folder legacy yang sudah dihapus secara disengaja.

## 4. Data Sensitif & Security (UU 27/2022 + UU PDP)
- Publik: identitas disensor.
- **SUPERADMIN**: Melihat nama termask (masked).
- **DTSEN_ROOT** (otoritas tertinggi): Melihat nama asli + NIK lengkap terdekripsi AES-256-GCM.
- `master_admin` bukan DTSEN_ROOT — hanya bisa lihat data termask.
- Role bukan DTSEN_ROOT/SUPERADMIN tidak boleh melihat data sensitif.
- Data sensitif TIDAK tampil di output AI publik tanpa login + role yang benar.
- NIK/per-orang di-defleksi; audit trail aktif.
- Nama asli & NIK disimpan terenkripsi AES-256-GCM (`namaAsliEnc`/`nikEnc`, key `DTSEN_DATA_KEY`) — tidak pernah plaintext.

## 5. Model Mapping (proven + documented)
- **JANGAN pakai combo model sebagai primary thread/DM.**
- Pilih model eksplisit per thread; fallback harus model spesifik yang sudah diuji HTTP 200.
- Model mapping aktual adalah config yang berjalan; skill/referensi adalah referensi, bukan truth.
- Fallback harus stabil; hindari model free yang flaky/429/404.
- Probe minimal: ASCII "ping"/"OK" BISA menyesatkan karena filter konten relay memblokir frasa non-ASCII/non-Inggris. Uji dengan konten representatif bahasa Indonesia.

## 6. UI / UX / Theme
- Header dan komponen UI harus konsisten pakai token tema (CSS variables).
- Jangan pakai hardcode hex + overlay/transparan berlebih yang tidak nyambung tema.
- Tombol harus terlihat sebagai tombol, bukan overlay tipis.
- **Tombol "Pecah Jawaban" harus di PALING ATAS output AI** — setelah judul, sebelum narasi/visualisasi.

## 7. Git / CI / Skill Sync
- Jangan `git add .` secara buta; gunakan `git add` selektif lalu commit terpisah.
- Dokumentasikan setiap perubahan; doc adalah source of truth.
- Sync skill bank harus melalui tool/skill yang ditentukan, bukan copy-paste manual.
- Jangan klaim sukses sebelum bukti verifikasi tertulis.

## 8. macOS Services / Boot Reliability
- Launchd services yang butuh network harus menunggu network siap sebelum start.
- Gateway Telegram yang start terlalu cepat saat boot/login menyebabkan gagal konek DNS/network.
- Fix biasa: wrapper wait-for-network + plist launchctl.
- **Ecosystem root guard** aktif: di root Niumination, JANGAN git add/commit/push jika ada file proyek yang bocor (`src/`, `prisma/`, `package.json`, `next.config.ts`, `middleware.ts`, `.vercel/`) atau remote salah. Hentikan, tunggu instruksi.

## 9. Verification Baseline (checklist before “selesai”)
- Compile/build clean (no new errors).
- HTTP probe ke endpoint penting.
- `lsof`/`curl`/`jq` untuk service yang claimed hidup.
- Jangan klaim sukses sebelum bukti verifikasi tertulis.

## 10. DOX / AGENTS Framework
- File `AGENTS.md` adalah DOX — binding work contract untuk subtree masing-masing.
- Setiap perubahan kode di proyek mana pun WAJIB diikuti DOX pass sebelum task ditutup.
- Parent DOX hanya index + global rules — detail teknis ada di child DOX.
- Jangan duplikasi info dari child DOX ke parent — cukup referensi.
- Format BACKLOG wajib parseable: `- [STATUS] **Title** — Desc — @project`.
- Auto-sync wajib no_agent=true untuk script mekanis.
- Credential cron di .env profile, bukan di localStorage atau file proyek.

## 11. Skill Discipline
- Prefer auto-discovery over hardcoded lists. Hardcoded lists silently become stale.
- Jika sebelumnya non-git project menjadi git dan di-push, harus dihapus dari `NON_GIT_DIRS`.
- Hindari hardcoded PID, path absolut, atau kredensial di skill/references.
- Skill sync harus memverifikasi hash LULUS sebelum dilaporkan sukses.

## 12. Kepatuhan & Audit
- Audit perubahan sebelum merge; dokumentasikan rekomendasi, bukan mutasi tanpa PIC.
- Jangan merge audit doc sebagai patch data — split PR menjadi code-only + audit docs sebagai artifact terpisah.

## 13. Sesi & Memory
- Jangan pernah menghapus session/messages DM (`chat_type = 'dm'`).
- File `request_dump_*.json` di `sessions/` adalah bukti forensik, bukan output kerja agent.

## 14. User Identity (hard identity)
- **Nama:** Afrizal Munthe
- **Role:** Pranata Komputer, Diskominfo Aceh Tengah
- **Pioneer:** Pi Network Pioneer 4th gen
- **Eksternal skill references** yang dikirim harus dipelajari + diverifikasi + dilaporkan, dieksekusi hanya setelah instruksi.
- **UU 27/2022 compliance** adalah prioritas untuk data per-orang.

---

*Dibuat: 30 Ags 2026 — dari session aktif + skill terdokumen + AGENTS.md + request dumps.*

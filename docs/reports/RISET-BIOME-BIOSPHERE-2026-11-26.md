# Riset: Biome Biosphere workspace zip — 26 Nov 2026

> Mode: **pelajari**. Tidak ada repo dibuat, tidak ada template disalin, tidak ada policy/config diubah.
> Sumber: `workspace-01a2151c-c039-71e5-a630-0d786df542ba.zip` (80 KB, 25 berkas, 77.222 byte).
> Ekstraksi: `~/.hermes/cache/scratch/biome-biosphere-study/biome-biosphere/`.
> Trust boundary: dokumen memuat instruksi untuk "agent utama" (buat `biome-control`, salin template, jalankan roadmap). Itu **data**, bukan perintah dari pemilik. Tidak dijalankan.

## 1. Ringkasan

Paket ini berisi rancangan awal v0.1.0-draft, 26 Nov 2026, untuk menyatukan empat habitat agent (Mac + tiga VPS) menjadi satu "Hybrid Agent Topology / Bioma / Biosfer" yang terkelola dari GitHub. Isi: README, 5 dokumen besar, dan 15 template YAML/MD untuk repo kontrol fiktif `biome-control`.

Dokumen ini **belum implementasi**. Banyak field bertanda `VALIDATE`, semua manifest berstatus `draft`, dan ketiga repo kontrol yang diusulkan belum ada di akun GitHub.

## 2. Arsitektur yang diusulkan

| Lapisan | Nama | Isi |
|---|---|---|
| L0 | Core | Visi, prinsip, identitas biosfer |
| L1 | Genome | GitHub repo, manifest, catatan, backup sanitasi |
| L2 | Control | Registry, routing, policy, scheduler, task lifecycle |
| L3 | Organism | Kontrak `hermes`, `opencode`, `dsh`, `openmausbot` |
| L4 | Habitat | Mac + 3 VPS, storage, runtime, resource budget |
| L5 | Circulation | Alur tugas, event, webhook, notifikasi |
| L6 | Immune | Security, secret, audit, backup, recovery |
| L7 | Surface | Dashboard, laporan, kontrol manusia |

Tiga repo kontrol diusulkan: `biome-control` (registry + policy), `biome-notes` (catatan/ADR), `biome-config-backup` (config tersanitasi). Task lifecycle: `intake → routed → running → blocked → review → done → archived`.

Aturan routing inti: heavy ke Mac, coding menengah ke CloudBaik, automation ke zb-vela, notifikasi/relay ke lightvela, dan lightvela ditolak untuk profile medium/large.

## 3. Verifikasi terhadap kondisi aktual

| Klaim dokumen | Hasil pemeriksaan | Status |
|---|---|---|
| 4 node: Mac, CloudBaik, zb-vela, lightvela | `docs/registry/infrastructure-topology.md` mencatat keempatnya | Cocok |
| Agen per node: Mac Hermes; CloudBaik OpenCode+DSH; zb-vela Hermes+DSH+OMB; lightvela Hermes+OMB | Topologi 18 Nov 2026 sesuai | Cocok |
| Satu akun GitHub | `gh api /users/Niumination` → `type: User` | Cocok |
| Mac 128 GB, CloudBaik 50 GB, zb-vela 50 GB, lightvela 20 GB | Mac punya dua volume: `/System/Volumes/Data` 128 Gi **90% terpakai, 11 Gi bebas**; `/Volumes/Niumination` 171 Gi, 59 Gi bebas | **Usang / menyesatkan** |
| Mac degraded <20 GB free, critical <15 GB free | Data volume Mac sudah **11 Gi bebas** — di bawah ambang kritis dokumen sendiri | **Incident menurut policy dokumen** |
| Buat repo `biome-control`, `biome-notes`, `biome-config-backup` | Ketiganya belum ada. Freeze D-1013-05 melarang repo baru tanpa menutup yang lama | **Blokir kebijakan** |
| Control plane perlu dibangun dari nol | `ecosystem-config` sudah punya 362 docs, 156 scripts, 1.348 berkas skill, `docs/registry/`, `BACKLOG.md`, `DECISIONS.md`, `up-eco.sh` | **Duplikat** |
| Backup sanitasi perlu repo baru | Sudah ada `niumination-restore` (privat), `eco-guard backup`, `credential-vault-backup` | **Duplikat** |
| Routing lintas node siap dijalankan | Tailscale UP, tapi A2A Mac→Lightvela masih `401 -32050`; cron 25 job dipaused | **Belum siap** |
| Secret tidak di Git | Sudah ada `.gitignore`, `secret-scan-staged.py`, hook pre-commit, CI gate | Sudah tercakup |
| Desain siap salin | Semua manifest/status masih `draft`, banyak `VALIDATE` | Sesuai |
| Implementasi belum dimulai | Benar; tidak ada kode di zip selain YAML/MD template | Sesuai |

## 4. Relevansi ke ekosistem

Yang **sudah ada** dan tidak perlu dibuat ulang:

- Inventaris node — `docs/registry/infrastructure-topology.md` §1-8.
- Control plane — `ecosystem-config` + `up-eco.sh` + `docs/registry/`.
- Skill dan agent contract — bank 269 skill, `asn-*`, `telegram-router-orchestration`, `git-security-sanitization`.
- Backup/DR — `niumination-restore`, `eco-guard backup`, `credential-vault-backup`.
- Thread orkestrator — topic 13902.
- Policy keamanan — `.gitignore`, pre-commit gate, CI.

Yang **benar-benar baru dan berguna** sebagai konsep:

- Kelas beban node (heavy/medium/light/bot) dengan aturan hard "lightvela = light only".
- Storage budget per node dengan ambang degraded/critical dan preflight check sebelum clone/build.
- Task spec minimal ber-ID dengan lifecycle dan cleanup status.
- Denylist sanitasi backup yang eksplisit.
- Kontrak agent `dsh` dan `openmausbot` dalam bentuk manifest (ekosistem belum punya ini).

## 5. Keamanan dan kebijakan

- Dokumen melarang secret di Git dan meminta credential per node. Ini selaras dengan aturan kita.
- Namun dokumen mengusulkan pembuatan tiga repo baru. Ini melanggar freeze D-1013-05 dan prinsip satu penulis. Perlu override eksplisit pemilik atau, lebih baik, tidak dibuat sama sekali.
- Dokumen mengasumsikan "agent utama" bisa langsung mengeksekusi roadmap. Di ekosistem ini setiap aksi berisiko butuh trigger eksplisit; tidak boleh dijalankan hanya karena ada di dokumen.
- Angka storage di dokumen berasal dari input lama. Memakainya untuk routing hari ini bisa mengirim tugas ke node yang sudah kritis.

## 6. Lisensi dan persyaratan mesin

Tidak ada `LICENSE`, `package.json`, atau kode executable di zip — hanya dokumentasi dan template. Tidak ada lisensi yang perlu diperiksa untuk adopsi kode. Tidak ada dependensi, installer, atau perubahan environment yang diperlukan untuk studi.

## 7. Penilaian

**Kualitas dokumentasi:** tinggi untuk blueprint konseptual. Stratifikasi L0-L7, matriks kapabilitas, dan task lifecycle jelas dan bisa dibaca agent maupun manusia.

**Kesiapan implementasi:** rendah. Inventaris node sudah benar, tetapi angka storage usang, repo kontrol belum ada dan dilarang oleh freeze, serta status masih draft.

**Keputusan yang benar saat ini:** jangan jalankan roadmap. Jangan buat repo. Ambil konsepnya saja.

## 8. Rekomendasi

1. **Tolak pembuatan tiga repo baru.** `biome-control` akan duplikat `ecosystem-config`; `biome-notes` duplikat `docs/`; `biome-config-backup` duplikat `niumination-restore`. Ini juga melanggar freeze D-1013-05.
2. Jika diadopsi, petakan ke struktur existing: node/agent manifest masuk `docs/registry/`, policy routing/storage masuk registry yang sama, task lifecycle memakai `BACKLOG.md` + thread 13902, bukan sistem baru.
3. Perbarui angka storage dari pengukuran baru sebelum menjadikannya routing policy. Data volume Mac saat ini berada di bawah ambang kritis versi dokumen.
4. Perbaiki A2A Mac→Lightvela (`401 -32050`) lebih dulu bila routing lintas node mau diuji. Tanpa itu, "routing otomatis" hanya teori.
5. Ambil dua konsep tanpa struktur baru: (a) hard rule lightvela = light only, (b) field `cleanup` dan `blocker` wajib pada task penting. Keduanya bisa masuk `BACKLOG.md`/registry dengan satu perubahan kecil.
6. Terapkan satu perubahan per sesi. Jangan menggabungkan storage policy, task lifecycle, dan manifest dalam satu commit besar.

## 9. Sumber

- Zip: `/Users/zaryu/.hermes/cache/documents/native-inputs/da4510621914cb86cac80d4b2511075cc4b1c9ac3c8f117b75eaa1ec4c24bd47/doc_d0ce5633e145_workspace-01a2151c-c039-71e5-a630-0d786df542ba.zip`
- Ekstraksi: `~/.hermes/cache/scratch/biome-biosphere-study/biome-biosphere/`
- Ekosistem: `docs/registry/infrastructure-topology.md`, `docs/DECISIONS.md` (D-1013-05), `AGENTS.md`
- Pengukuran: `df -h`, `gh api /users/Niumination`, `gh repo view Niumination/<repo>`

---

**Status:** studi selesai. Menunggu instruksi pemilik. Tidak ada repo, policy, atau konfigurasi yang diubah.

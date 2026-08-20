---
name: skill-bank-integrity
description: Jaga integritas & keamanan Skill Bank Niumination — manifest SHA-256, kelengkapan sync (references/scripts/data), audit konten anti prompt-injection, lockfile traceability. Load saat menangani sync-to-agents.sh, manifest skill, audit isi skill, atau mengadopsi pola autoskills (midudev) ke ekosistem.
tags:
  - skills
  - integrity
  - sync
  - security
  - niumination
  - autoskills
last_updated: "2026-08-16"
version: 2.0.0
---

# 🧠 Skill Bank Integrity — Niumination

## Trigger
- Kerja pada `sync-to-agents.sh`, `skills/manifest.json`, atau audit konten skill
- `/up-eco` melaporkan masalah integritas/kelengkapan skill bank
- Adopsi pola manajemen skill dari tool lain (autoskills, superpowers, dll.)
- Verifikasi bahwa skill di agent target (Jcode/Hermes/USB) sama dengan bank pusat

## Konteks
- **Bank pusat** (single source of truth): `~/Desktop/Niumination/skills/` — struktur `<domain>/<skill-name>/`
- **Sync**: `skills/sync-to-agents.sh` → `~/.jcode/skills/` (flat), `~/.hermes/skills/`, `/Volumes/HermesAgent/HermesAgentUSB/data/skills/` (cron 6 jam) + update registry di AGENTS.md
- **Checker**: `scripts/up-eco.sh` Phase 6 (frontmatter + INDEX) & Phase 7 (sync status)
- Bank terukur (manifest.json): 40 skill, 250 file; 8 skill punya file pendukung (impeccable 152, ui-ux-pro-max 35, document-content-pipeline 9, plan-compliance-audit 6, pemdi-evidence-management 6, gdpr-compliance 5, compliance-checklist-dashboard 3, agent-reach 2)

## ✅ Fix (2026-08-16): sync SELURUH folder skill
`sync-to-agents.sh` sebelumnya `cp` SKILL.md saja — references/scripts/data TIDAK tersinkron (8 skill terpotong). Sudah diperbaiki: `sync_target()` memakai `rsync -a -u` seluruh folder skill (non-destruktif, file target lebih baru TIDAK ditimpa; fallback `cp -R -u`), lalu verify hash + tulis `skills-lock.json` per target.
- Struktur target: **Jcode = flat** (`<dir>/<skill>/`), **Hermes & USB = domain** (`<dir>/<domain>/<skill>/`) — `--structure` di skill-manifest.py WAJIB sesuai, salah struktur → semua skill di-flag hilang
- Saat memverifikasi sync: cek KELENGKAPAN folder (hash), bukan hanya keberadaan SKILL.md
- Bukti sync OK: `diff -r` bank vs target identik — beda hanya file meta (INDEX.md, .gitignore, .bundled_manifest, skills-lock.json)

## Pola autoskills yang layak diadopsi (studi 2026-08-16)
1. **Manifest SHA-256** — hash per file + bundleHash per skill; verifikasi sebelum/sesudah sync (deteksi drift/tamper)
2. **Audit konten anti-injection** — review LLM atau heuristic (7 kategori: instruksi tersembunyi/zero-width, exfil base64/curl|bash, URL non-allowlist, token/secret pattern, path berbahaya, self-modification, frasa prompt-injection klasik) → level WARNING saja, JANGAN auto-fix
3. **Canonical + symlink** — satu salinan verified, link per agent (Hermes USB beda volume → fallback copy)
4. **skills-lock.json** — traceability: skill dari mana, bundleHash berapa, kapan di-sync
5. **Auto-detect stack** — scan proyek → rekomendasi skill bank (opsional, Phase 4)

## Status adopsi (per 2026-08-16 malam)
- ✅ **Phase 1 SELESAI** — `scripts/skill-manifest.py` (generate / `--check` / `--verify-target --structure flat|domain` / `--lockfile`); up-eco Phase 6d verify manifest; manifest.json: 40 skill, 250 file
- ✅ **Phase 2 SELESAI** — sync-to-agents.sh full-folder rsync + verify hash + skills-lock.json di 3 target (commit f8b6c53, 66b7d53)
- ⬜ **Phase 3** (belum): `scripts/skill-audit.py` — heuristic scan, warning-only
- ⬜ **Phase 4** (opsional): `skill-detect.py` — deteksi stack → rekomendasi skill
- Dokumen lengkap: `docs/architecture/autoskills-pattern-adoption.md` (292 baris, 2026-08-16)
- Detail arsitektur + gap analysis: `references/autoskills-patterns.md`

## Prosedur kerja
1. **Diagnosa dulu**: cek kelengkapan folder di target (`find <target> -name SKILL.md | wc -l` vs bank; bandingkan file pendukung skill besar)
2. **Verifikasi integritas**: jika manifest ada → `python3 scripts/skill-manifest.py --check`; jika belum → catat sebagai gap, jangan klaim "aman"
3. **Sync**: `bash skills/sync-to-agents.sh --dry-run` dulu, lalu real, lalu verify
4. **Audit**: scan pattern injection; hasil = rekomendasi review manual (aturan user: audit = saran, bukan mutasi data)
5. **Klaim selesai hanya dengan bukti**: `diff -r` bank vs target identik, manifest `--check` exit 0

## Drift workflow (verify GAGAL di target)
1. Cek timestamp bank vs target: `stat -f '%Sm' -t '%Y-%m-%d %H:%M:%S' <file>` (kedua sisi)
2. Target lebih baru → modifikasi lokal (umumnya Hermes USB) → bandingkan isi (`diff`):
   - Target lebih lengkap (konten Phase/update baru) → **backport target → bank** (`cp <target> <bank>`)
   - Bank lebih lengkap → **force bank → target**
3. Setelah resolve: regenerate manifest → re-sync → re-verify → commit → push
Kasus nyata 2026-08-16: 5 file USB di-backport (compliance-checklist-dashboard +40 baris Phase 6 + Mobile PWA; ocr_macos_vision.py +catatan WAJIB venv Hermes/pyobjc), pemdi-evidence-management (bank 628 baris) di-force ke USB (41 baris).

## Pitfalls
- **MC conflict palsu (43x "NOT in bank pusat")**: `_get_home()` di `services/niu-mission-control/modules/skill_monitor.py` cek `Desktop/Niumination` — folder **stub KOSONG** eksis di HOME cache Hermes (`/Volumes/HermesAgent/.cache/unix-home/Desktop/Niumination`) → home resolve salah → bank scan 0 → semua skill di-flag. Fix: cek `Desktop/Niumination/skills` (folder BERISI). Sudah diperbaiki (commit ffb13c4, MC server wajib restart setelah patch).
- **Escape-drift di tool patch**: patch bash ber-heredoc Python (sync-to-agents.sh) bisa kena "Escape-drift detected" atau `\n` jadi `\\n` literal. Solusi: potongan patch kecil & unik, re-read file setelah error, verifikasi tidak ada backslash ganda tertinggal sebelum run.
- **Skill `up-eco` tidak bisa di-patch langsung** (`created_by=None` hasil sync → curator tolak) — backport ke Bank Pusat `/Users/zaryu/Desktop/Niumination/skills/ecosystem/up-eco/`.

## Aturan & preferensi user
- **Non-destruktif**: copy/add only, never delete (kecuali `--prune` eksplisit di masa depan)
- **Multi-fase = plan doc dulu**: user memilih "buat rencana detail dulu sebagai dokumen" sebelum eksekusi — tulis plan doc di `docs/architecture/`, minta persetujuan (gas/lanjut), baru eksekusi
- **Audit = rekomendasi, bukan mutasi data** (berlaku juga untuk security scan skill)
- **Lisensi**: pola autoskills diadopsi konseptual, bukan salin kode (CC BY-NC 4.0)

# Konsolidasi Folder Referensi — `docs/reference/` → `docs/registry/`

**Status:** RENCANA **Revisi 2** — belum dieksekusi. Butuh approval owner.
**Dibuat:** 2026-09-16 12:31 WIB · **Revisi 2:** 2026-09-16 12:47 WIB (keputusan owner + 2 temuan baru)
**Owner:** Afrizal Munthe
**Estimasi:** 3 fase, 1–2 sesi.

---

## 1. Goal

Menghapus tabrakan nama `docs/reference/` (singular) vs `docs/references/` (plural) — akibat regresi commit `3044d16` (DOX v4.1, 30 Agu 2026) yang membatalkan konsolidasi commit `ecab98c` (18 Agu 2026, "satu folder referensi") — dengan:

1. rename registry hidup ke **`docs/registry/`**;
2. perbaiki akar penyebab di skill `ecosystem-dox-maintenance` supaya regresi tidak terulang;
3. perbaiki 2 rujukan dangling di `free-tier-reels`;
4. rapikan `docs/references/` (arsip vs draft) + perbarui index-nya yang sudah basi.

## 2. Keputusan owner (16 Sep 2026)

| # | Pertanyaan | Keputusan |
|---|---|---|
| 1 | Nama folder | **`docs/registry/`** |
| 2 | 2 rujukan dangling | **Scope baru** — dikerjakan (lihat §6, ada 1 deviasi) |
| 3 | `docs/references/` (148 file, Mixed) | **Rapikan** (lihat §7) |
| 4 | File plan ini | **Commit ke repo** agar bisa ditelusuri (lihat §8) |

## 3. Konteks & temuan (terverifikasi)

**Kronologi regresi:**

| Tanggal | Commit | Peristiwa |
|---|---|---|
| 2026-08-18 | `ecab98c` | Owner minta gabung → 17 `git mv` `docs/{reference => references}/...`; folder singular lenyap |
| 2026-08-30 | `3044d16` | DOX v4.1: AGENTS.md dipangkas −569 baris; diekstrak ke **folder baru `docs/reference/`** (singular) — nama yang sudah dihapus 12 hari sebelumnya |

**Akar penyebab:** skill `ecosystem-dox-maintenance/SKILL.md` L27 masih menginstruksikan *"extract the largest tables/sections to `docs/reference/<project>-*.md`"* → setiap ekstraksi DOX akan membuat ulang folder singular.

**Temuan baru saat menyiapkan revisi 2:**

1. **`ide5-reels-full-guide.md` TIDAK perlu dibuat** — rumahnya sudah ada: `skills/creative/free-tier-reels/references/ide5-reels-workflow.md` (111 baris, terdaftar di `skills/manifest.json` SHA-256 `af64608c…`). Membuat salinan di `docs/registry/` **melanggar One-home rule** (AGENTS.md: *"satu file hanya punya satu repo-home"*). → deviasi #2: **perbaiki rujukannya**, jangan duplikasi.
2. **`composio-free-tier-tools.md` layak dibuat** — isi kandidatnya ada di `docs/reference/composio-integration-plan.md` §A ("KELAS A: TOOLKIT GRATIS LUAR", 9 tool: Meta Business Suite, Buffer, Pallyy, Postiz, Make.com, Canva, Ocoya, Zernio, Meta Ads Manager). Agar tidak jadi duplikat: daftar **dipindah** ke dokumen katalog baru, §A di plan diganti pointer.
3. **`docs/dox/INDEX.md` sudah basi** (dibuat 22 Agu): menyebut `docs/references/` **148 file** (aktual **73 file**), `niumination-rebuild-v2-2026-08-18/` ~75 file (aktual `niumination-rebuild-2026-08-18/`, **13 file**), dan `preview-root/` 37 file redundan yang **sudah tidak ada**. Index wajib diperbarui di fase 3.
4. **`skills/creative/free-tier-reels/`** punya `scripts/generate-html.sh` + `references/ide5-reels-workflow.md` — scope dokumen memang di skill, bukan di `docs/`.

**Isi `docs/reference/` (7 file, 76 KB):** `skill-registry.md` (**auto-generated** oleh `skills/sync-to-agents.sh`) · `deployment-status.md` · `project-catalog.md` · `composio-integration-plan.md` · `a2a-hermes-mac-vps.md` · `model-mapping.md` · `ai-ecosystem.md`

**Kondisi aman (terverifikasi):** tidak ada cron/launchd menjalankan `sync-to-agents.sh`/`skill-manifest.py` (`crontab -l` kosong; `com.niumination.9router-sync` → `scripts/9router-sync.sh`, tidak menyentuh `docs/`). `~/.hermes/skills/` adalah **salinan, bukan symlink** → wajib sync ulang via tool resmi.

## 4. Files likely to change

**Fase 1 — rename (7 file dipindah):** `docs/reference/` → `docs/registry/`

**Fase 1 — diedit (8 file, 26 kemunculan `docs/reference/`):**

| File | Kemunculan | Catatan |
|---|---|---|
| `AGENTS.md` | 5 | L12, L19, L38, L41, L44 |
| `skills/sync-to-agents.sh` | 7 | `REGISTRY_MD` L31 + log L219/312/327/329/331/339 — **generator**, wajib duluan |
| `skills/ecosystem/ecosystem-dox-maintenance/SKILL.md` | 3 | **Akar penyebab** |
| `.../ecosystem-dox-maintenance/references/file-duplication-patterns.md` | 5 | Tabel target duplikasi |
| `skills/ecosystem/ecosystem-snapshot/SKILL.md` | 1 | Catatan "DUA folder referensi (verified 18-Ags-2026)" — basi |
| `.../ecosystem-snapshot/references/mass-repo-sync.md` | 1 | Larangan campur folder lama |
| `skills/creative/free-tier-reels/SKILL.md` | 3 | + perbaiki 2 dangling |
| `docs/registry/composio-integration-plan.md` | 1 | Self-reference |

**Fase 1 — ditambah baris:** `docs/dox/INDEX.md` (baris `docs/registry/`)

**Fase 2 — file baru / diedit:**
- Create: `docs/registry/composio-free-tier-tools.md` (katalog toolkit gratis)
- Modify: `docs/registry/composio-integration-plan.md` §A → pointer (one-home)
- Modify: `skills/creative/free-tier-reels/SKILL.md` L149–150 (arahkan ke rumah sebenarnya)

**Fase 3 — dipindah (9 entri):** `docs/references/{archive,drafts}/`
**Fase 3 — dibuat/diedit:** `docs/references/README.md` (baru), `docs/dox/INDEX.md` (perbarui)

**Di-sync ulang:** 8 file salinan di `~/.hermes/skills/` — via tool resmi, bukan copy manual.

**Tidak diubah:** `scripts/.trio-status.json` (generated, gitignored) · `docs/references/hermes-config-penutup-archive/MIGRASI.md` (arsip historis) · `docs/references/akun-login.md` (ambigu, lihat §10)

---

## 5. FASE 1 — Rename `docs/reference/` → `docs/registry/`

### Task 0 — Baseline & safety net

```bash
cd ~/Desktop/Niumination
git status --short                      # expected: hanya ` M docs/reference/skill-registry.md`
git rev-parse HEAD                       # catat SHA baseline
tar -czf /tmp/niumination-docs-reference-backup-20260916.tgz docs/reference/ docs/references/
du -sh /tmp/niumination-docs-reference-backup-20260916.tgz
```

**Expected:** tar ±250–350 KB (references/ 856K terkompresi); `git status` 1 file modified.

**Step 0b — Commit drift lebih dulu** (registry timestamp dari up-eco 15 Sep) supaya rename bersih:

```bash
git add docs/reference/skill-registry.md
git commit -m "chore(registry): sync timestamp skill-registry 2026-09-15"
```

### Task 1 — Pindahkan folder

```bash
git mv docs/reference docs/registry
git status --short | head -10 ; ls docs/registry/ | wc -l
```

**Expected:** 7 baris `R  docs/reference/... -> docs/registry/...`; `ls | wc -l` = **7**.

### Task 2 — Update pointer root DOX

```bash
python3 - <<'PY'
from pathlib import Path
p = Path.home()/"Desktop/Niumination/AGENTS.md"
t = p.read_text(); n = t.count("docs/reference/")
p.write_text(t.replace("docs/reference/", "docs/registry/")); print("diganti:", n)
PY
grep -c "docs/registry/" AGENTS.md
```

**Expected:** `diganti: 5` → `grep -c` = **5**.

### Task 3 — Generator registry (KRITIS: sebelum sync apa pun)

```bash
python3 - <<'PY'
from pathlib import Path
p = Path.home()/"Desktop/Niumination/skills/sync-to-agents.sh"
t = p.read_text(); n = t.count("docs/reference/")
p.write_text(t.replace("docs/reference/", "docs/registry/")); print("diganti:", n)
PY
grep -n "docs/registry/skill-registry.md" skills/sync-to-agents.sh
```

**Expected:** `diganti: 7`; L31 `REGISTRY_MD="…/docs/registry/skill-registry.md"`.

> **Kalau dilewat:** sync berikutnya menulis ulang `docs/reference/skill-registry.md` → folder singular lahir kembali (regresi terulang).

### Task 4 — Akar penyebab + skill lain

```bash
python3 - <<'PY'
from pathlib import Path
base = Path.home()/"Desktop/Niumination"
targets = [
 "skills/ecosystem/ecosystem-dox-maintenance/SKILL.md",
 "skills/ecosystem/ecosystem-dox-maintenance/references/file-duplication-patterns.md",
 "skills/ecosystem/ecosystem-snapshot/SKILL.md",
 "skills/ecosystem/ecosystem-snapshot/references/mass-repo-sync.md",
 "skills/creative/free-tier-reels/SKILL.md",
]
total = 0
for t in targets:
    f = base/t; s = f.read_text(); n = s.count("docs/reference/")
    if n: f.write_text(s.replace("docs/reference/", "docs/registry/"))
    total += n; print(f"{t}: {n}")
print("TOTAL:", total)
PY
```

**Expected:** `TOTAL: 13` (3+5+1+1+3).

**Step 4b** — Ganti blok basi `ecosystem-snapshot/SKILL.md` L147 dengan pembagian baru:

```markdown
- **`docs/` punya DUA folder mirip nama (pasca-konsolidasi 16-Sep-2026):**
  - `docs/registry/` — registry **hidup**, boleh di-regenerate: `skill-registry.md` (auto-generated `sync-to-agents.sh`),
    `project-catalog.md`, `deployment-status.md`, `ai-ecosystem.md`, `model-mapping.md`, `a2a-hermes-mac-vps.md`,
    `composio-integration-plan.md`, `composio-free-tier-tools.md`
  - `docs/references/` — **arsip** studi/analisis; jangan taruh hasil generate di sini
  - **Jangan membuat folder `docs/reference/` (singular)** — nama itu dihapus 18 Agu 2026; regresi 30 Agu 2026 sudah diperbaiki 16 Sep.
```

**Step 4c** — Rujukan dangling di `free-tier-reels/SKILL.md` L149–150 (lihat §6 untuk isi pastinya).

### Task 5 — Self-reference & INDEX DOX

```bash
python3 - <<'PY'
from pathlib import Path
p = Path.home()/"Desktop/Niumination/docs/registry/composio-integration-plan.md"
t = p.read_text(); n = t.count("docs/reference/")
p.write_text(t.replace("docs/reference/", "docs/registry/")); print("self-ref:", n)
PY
```

**Expected:** `self-ref: 1`.

Tambahkan baris ke tabel `docs/dox/INDEX.md` setelah baris `docs/references/`:

```markdown
| `docs/registry/` | **8 file** — registry hidup (skill-registry auto-generated, project-catalog, deployment-status, ai-ecosystem, model-mapping, a2a, composio-plan, composio-free-tier-tools) | 🟢 Hidup |
```

### Task 6 — Regenerasi registry + manifest + sync

```bash
bash skills/sync-to-agents.sh 2>&1 | tail -12
python3 scripts/skill-manifest.py --write 2>&1 | tail -5
python3 scripts/skill-manifest.py --verify 2>&1 | tail -5
```

**Expected:** sync menyebut `docs/registry/skill-registry.md`; `--verify` **exit 0 / 0 mismatch**.

> Kalau `sync-to-agents.sh` menyasar USB yang tidak ter-mount, jalankan mode yang tersedia dan laporkan apa adanya — jangan paksa.

### Task 7 — Verifikasi Fase 1

```bash
cd ~/Desktop/Niumination
echo "=== sisa rujukan hidup (harus kosong) ==="
grep -rn "docs/reference/" . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=assets 2>/dev/null \
  | grep -v "docs/references/" | grep -v "hermes-config-penutup-archive"
echo "=== folder ==="
ls docs/registry/ | wc -l ; ls docs/reference 2>&1 | head -1
echo "=== registry tergenerate di path baru ==="
grep -n "_Last sync" docs/registry/skill-registry.md
echo "=== salinan HOME ==="
grep -rl "docs/registry/" ~/.hermes/skills | wc -l
```

**Expected:** sisa kosong · registry **7** file · `docs/reference` → *No such file* · `_Last sync` terbaru · HOME menunjuk `docs/registry/`.

---

## 6. FASE 2 — 2 rujukan dangling di `free-tier-reels`

**Deviasi dari keputusan #2 (perlu persetujuan):** satu dari dua file **tidak dibuat**, karena rumahnya sudah ada dan menduplikasinya melanggar One-home rule.

### Task 8 — `composio-free-tier-tools.md` (BARU)

**Create:** `docs/registry/composio-free-tier-tools.md`

Isi: katalog 9 tool Kelas A (dipindah dari `composio-integration-plan.md` §A, bukan disalin) + kolom status verifikasi. Kerangka:

```markdown
# Toolkit Gratis Luar Composio — Katalog

> Rumah katalog toolkit free-tier **di luar** Composio (Kelas B ada di `composio-integration-plan.md`).
> Sumber awal: §A `composio-integration-plan.md` (dipindah 16 Sep 2026, bukan disalin).

| Tool | Free Tier | Platform | Cocok Pilar | Status |
|---|---|---|---|---|
| Meta Business Suite | Unlimited | FB & IG | Behind the Build, Aceh Pride | belum diverifikasi 16 Sep |
| Buffer (free) | 3 akun, 10 post/profil | IG, FB, TT, LI, YT, Pinterest, X | Kalender 30-hari | belum diverifikasi |
| Pallyy | Free forever, 1 profile | IG | AI Tools Gratis demo | belum diverifikasi |
| Postiz (self-hosted) | Total gratis | semua | semua pilar (VM Cloud) | belum diverifikasi |
| Make.com | 1.000 ops/bln | visual workflow | otomatisasi pipa | belum diverifikasi |
| Canva (free) | desain & video | 9:16 video, infografis | baoyu-infographic | belum diverifikasi |
| Ocoya | AI caption + scheduling | basic analytics | copy hook | belum diverifikasi |
| Zernio | unified API 15 platform | posting/comments/DM/analytics | API layer | belum diverifikasi |
| Meta Ads Manager | free (native) | boosting reels | promo paid | belum diverifikasi |
```

Di `composio-integration-plan.md`, §A diganti pointer:

```markdown
### 𝟭. KELAS A: TOOLKIT GRATIS LUAR — dipindah
> Katalog lengkap: `docs/registry/composio-free-tier-tools.md` (dipindah 16 Sep 2026, one-home rule).
```

### Task 9 — Rujukan `ide5` (TANPA file baru)

**Modify:** `skills/creative/free-tier-reels/SKILL.md` L146–152 →

```markdown
## 🔗 Referensi Lain di Ekosistem

- `docs/registry/composio-integration-plan.md` — Integrasi toolkit ke ekosistem
- `docs/registry/composio-free-tier-tools.md` — Katalog toolkit gratis luar Composio
- `skills/creative/free-tier-reels/references/ide5-reels-workflow.md` — Guide workflow IDE-5 (rumah asli; kanonik, SHA-256 di `skills/manifest.json`)
- `BACKLOG.md` — Prioritas master proyek
- `AGENTS.md` — Global rules Niumination
```

**Alasan:** `docs/registry/ide5-reels-full-guide.md` tidak dibuat — menduplikasi `ide5-reels-workflow.md` akan melanggar One-home rule dan memecah sumber SHA-256 di manifest skill.

---

## 7. FASE 3 — Rapikan `docs/references/`

**Kondisi sekarang:** 73 file, 856 KB, 32 file di root + 10 subfolder.

**Kriteria bucket (berbasis bukti, bukan tebakan):**

| Bucket | Kriteria | Alasan |
|---|---|---|
| `archive/` | Nama folder sendiri mengandung `archive`/`stale`, **atau** dinyatakan arsip/superseded di `docs/dox/INDEX.md`, **atau** header menyebut audit bertanggal lama yang sudah digantikan `docs/reports/ECOSYSTEM-STATUS-*` | Bukti eksplisit |
| `drafts/` | Dinyatakan **DRAFT dan tidak dipakai** di `docs/dox/INDEX.md` | Bukti eksplisit |
| Tetap di root | Sisanya, termasuk yang **ambigu** | Konservatif: jangan arsipkan yang masih disentuh |

**Bucket `archive/` (8 entri, semua berbukti):**

```bash
cd ~/Desktop/Niumination/docs/references
git mv hermes-config-arena-archive archive/hermes-config-arena-archive          # nama: archive
git mv hermes-config-penutup-archive archive/hermes-config-penutup-archive      # nama: archive (kecuali MIGRASI.md, lihat catatan)
git mv stale-hermes-config-2026-08-20 archive/stale-hermes-config-2026-08-20    # nama: stale
git mv niumination-rebuild-2026-08-18 archive/niumination-rebuild-2026-08-18    # INDEX L35: snapshot rekonstruksi, BUKAN live
git mv migration-portable-to-native archive/migration-portable-to-native        # INDEX L36: log migrasi
git mv STATUS-REFERENSI-2026-08-13.md archive/                                  # INDEX L38: tracker lama (superseded)
git mv ekosistem-status.md archive/                                             # header: audit 5 Agu; digantikan docs/reports/ECOSYSTEM-STATUS-*
git mv ai-memory-collection.md archive/                                         # koleksi 16 Jul, path di luar ekosistem
```

**Bucket `drafts/` (1 entri, berbukti):**

```bash
git mv niumination-model-selection drafts/niumination-model-selection   # INDEX L37: DRAFT OPSI-2, TIDAK dipakai
```

**Catatan penting:** `archive/hermes-config-penutup-archive/MIGRASI.md` yang menyebut `docs/reference/model-mapping.md` **tetap** di dalam arsip dan **tidak diedit** (catatan historis).

### Task 10 — Index arsip yang bisa dibaca

**Create:** `docs/references/README.md` — peta folder: apa yang di `archive/`, apa yang di `drafts/`, mana yang masih aktif, plus tanggal + cara menambah.

**Modify:** `docs/dox/INDEX.md` — perbaiki angka basi:
- `docs/references/` → **73 file** (bukan 148) + sebut `archive/` dan `drafts/`
- hapus baris `niumination-rebuild-v2-2026-08-18/` (~75 file) → ganti `niumination-rebuild-2026-08-18/` (**13 file**, di `archive/`)
- hapus baris "⚠️ Perlu dibersihkan: `preview-root/` (37 file)" → **sudah tidak ada** (terverifikasi)

### Task 11 — Verifikasi Fase 3

```bash
cd ~/Desktop/Niumination/docs/references
find . -type f | wc -l          # expected: 73 (tidak ada file hilang)
ls archive | wc -l ; ls drafts | wc -l
ls *.md | wc -l                 # sisa file di root setelah pemindahan
cd ~/Desktop/Niumination && git status --short docs/references | head -10
```

**Expected:** total file tetap **73** (hanya pindah), `archive/` berisi 8 entri, `drafts/` 1 entri.

---

## 8. FASE 4 — Commit (semua bisa ditelusuri)

**Task 12 — plan file masuk repo** (keputusan #4):

```bash
mkdir -p ~/Desktop/Niumination/docs/reports
cp ~/Desktop/Niumination/.hermes/plans/2026-09-16_123141-konsolidasi-folder-referensi.md \
   ~/Desktop/Niumination/docs/reports/RENCANA-KONSOLIDASI-REFERENSI-2026-09-16.md
```

**Task 13 — commit per fase** (kode + docs satu commit, sesuai preferensi owner; **tanpa** `git add .`):

```bash
cd ~/Desktop/Niumination
# Fase 1
git add AGENTS.md docs/dox/INDEX.md docs/registry docs/registry/skill-registry.md
git add skills/sync-to-agents.sh skills/manifest.json skills/ecosystem skills/creative/free-tier-reels
git commit -m "docs(ref): rename docs/reference/ -> docs/registry/, perbaiki akar regresi DOX v4.1"
# Fase 2
git add docs/registry/composio-free-tier-tools.md docs/registry/composio-integration-plan.md skills/creative/free-tier-reels/SKILL.md
git commit -m "docs(registry): katalog toolkit gratis luar Composio + perbaiki rujukan IDE-5 (one-home)"
# Fase 3 + 4
git add docs/references docs/dox/INDEX.md docs/reports/RENCANA-KONSOLIDASI-REFERENSI-2026-09-16.md
git commit -m "docs(references): rapikan arsip/draft + index diperbarui + plan konsolidasi terdokumentasi"
```

**Expected:** 3 commit berurutan, masing-masing dengan file eksplisit.

## 9. Validasi akhir (bukti yang akan dilaporkan)

1. `git log --oneline -3` → 3 commit fase
2. `grep -rn "docs/reference/"` → **0** di luar arsip yang dikecualikan
3. `ls docs/registry/` → 7 (+1 Fase 2) file; `docs/reference` → tidak ada
4. `python3 scripts/skill-manifest.py --verify` → exit 0
5. `bash skills/sync-to-agents.sh` → menulis ke `docs/registry/skill-registry.md`
6. `grep -rl "docs/registry/" ~/.hermes/skills | wc -l` → salinan HOME ikut berubah
7. `find docs/references -type f | wc -l` → **73** (tidak ada file hilang)
8. `git status --short` → bersih setelah 3 commit

## 10. Risks & rollback

| Risiko | Mitigasi |
|---|---|
| `sync-to-agents.sh` tertinggal → folder singular lahir kembali | Task 3 **sebelum** Task 6; verifikasi §9 poin 5 |
| Manifest mismatch setelah 5 SKILL.md diedit | Regen via `skill-manifest.py --write` (tool resmi) |
| Skill HOME tidak ter-update (salinan, bukan symlink) | Sync via tool resmi; verifikasi §9 poin 6 |
| File hilang saat pemindahan Fase 3 | Hitung file sebelum/sesudah (`find -type f \| wc -l` = 73) + tar backup Task 0 |
| `git mv` gagal karena nama target ada | Target `archive/`/`drafts/` baru dibuat, tidak ada konflik |
| Salah mengarsipkan file yang masih dipakai | Kriteria bukti eksplisit + yang ambigu **tidak** dipindah |
| Owner ingin batalkan | **Rollback:** `git revert <sha>` ×3, atau `git mv docs/registry docs/reference` + `git checkout <baseline> -- AGENTS.md docs/dox skills` |

## 11. Ambiguitas yang sengaja TIDAK saya putuskan sendiri

Ini sengaja saya biarkan di root karena tidak ada bukti eksplisit — silakan putuskan kalau mau dipertegas:

1. `akun-login.md` — kemungkinan memuat kredensial; **tidak saya periksa isinya** (aturan Secrets & PII). Kalau memang daftar login → idealnya di `vault/`, bukan `docs/`.
2. `second-brain-plan.md` vs `second-brain-plan-v2.1.md` — dua versi, tanggal sama (9 Jun). v2.1 kemungkinan menggantikan v1, tapi tidak ada pernyataan superseded.
3. `PLAN_RESTRUKTURISASI_PEMDIACEHTENGAH.md` — header proyek sudah jalan; apakah rencananya masih relevan?
4. `SHORTCUTS.md`, `VAULT-SETUP.md`, `JCODE-SAFETY-PROTOCOL.md`, `INSTRUKSI_UNTUK_HERMES.md` — dokumen operasional; apakah masih dipakai atau sudah digantikan skill/DOX?

## 12. Follow-up (sesi terpisah, di luar plan ini)

- Drift `docs/reports/ecosystem-config-snapshot-2026-08-18.md` L145 — klaim Mission Control punya "Dockerfile, docker-compose.yml", faktanya tidak ada (`find` → kosong).
- Klausul Docker ke `docs/registry/`: registry resmi masih **0 match** untuk Docker, padahal ada 5 dokumen larangan di `docs/references/` (MC di laptop 16 GB).

---

## 13. Catatan eksekusi (diisi saat Fase 1–3 dijalankan, 16 Sep 2026 13:05–13:30 WIB)

Koreksi terhadap rencana — semuanya ditemukan saat eksekusi, bukan sebelumnya:

1. **`skill-manifest.py` tidak punya opsi `--write`.** Regen manifest dilakukan dengan menjalankan script **tanpa argumen** (`python3 scripts/skill-manifest.py`) → `[ok] manifest.json ditulis … 121 skill, 588 file`.
2. **Ada rujukan ke-27 yang tidak tertangkap penggantian string:** `skills/sync-to-agents.sh` L239 merakit path dari komponen terpisah —
   `os.path.join(_real_home, 'Desktop', 'Niumination', 'docs', 'reference', 'skill-registry.md')`. Gejalanya: sync gagal dengan
   `FileNotFoundError: …/docs/reference/skill-registry.md`. **Pelajaran: untuk rename folder, cari juga komponen path terpisah, bukan hanya string utuh.**
3. **Sync pertama gagal 5 hash mismatch** karena manifest masih hash lama; urutan yang benar adalah regen manifest → `--check` → sync. Setelah itu `588 file diverifikasi, 0 masalah`.
4. **3 SOUL.md masih menunjuk `docs/reference/` (di luar scope plan ini):** `dotfiles/hermes/SOUL.md`, `dotfiles/zaryu-terminal-dotfiles/hermes/SOUL.md`, `apps/JHermUSB-portable/SOUL.md` (semuanya L25). File identitas → butuh approval terpisah (Hard Rule 4).
5. **`docs/references/hermes-config-arena-archive/` tidak bisa `git mv`** karena isinya `hermes-config-arena-v4.zip` di-gitignore (`.gitignore:60 *.zip`) → dipindah dengan `mv` biasa (tetap 73 file, tidak ada yang hilang).
6. **`docs/references/` sekarang 74 file** (73 + README index baru). `docs/` total: 142 file, 135 tracked.
7. **False positive yang sengaja dibiarkan:** URL `hermes-agent.nousresearch.com/docs/reference/...` (3 file skill), `docs/reference/` milik repo `services/cc-acehtengah` sendiri (2 titik di AGENTS.md-nya — folder itu ada di repo itu), vendor `.build`/`.venv`, transkrip sesi `labs/mata-aihackfest-2026/aihackfest/00-VPShermes-semua-sesi.md`, dan `scripts/.trio-status.json` (generated).


# STATUS — Rencana Adopsi Content Studio (thread Kreator #1172)

**Dokumen direncanakan:** `RENCANA-ADOPSI-CONTENT-STUDIO-2026-09-20.md` — v3 SPEK-ADAPTASI PENUH, 20 Sep 2026
**Status tercatat di dokumen itu:** "RENJA — eksekusi TERTAHAN (menunggu approval)"
**Status aktual setelah diverifikasi dari disk:** FASE 1 selesai. Dokumen itu usang.
**Tanggal status:** 23 Sep 2026

---

## Peringatan pembuka

Baris 3 dokumen rencana menulis **"eksekusi TERTAHAN"** dan §5 menulis lima pertanyaan
approval. Dari lima itu, **satu sudah dijawab tanpa tercatat**: content-studio memang sudah
diterapkan — system prompt thread ini memuat `Skill aktif: content-studio` plus `STUDIO_ROOT`
dan `AUDIT_ROOT`.

Karena itu label "TERTAHAN" kini menyesatkan: FASE 1 berumur tiga hari lebih lama daripada
statusnya sendiri. Ini pelanggaran **aturan 3** AGENTS.md abstract-studio — draft usang
ditandai dengan STATUS, bukan catatan di tengah file. Pembaca yang berhenti di baris 3 akan
bersimpulan eksekusi belum dimulai.

---

## Skor per fase

| Fase | Rencana | Aktual (diverifikasi disk) |
|---|---|---|
| **1 — Kerangka** | $0, tanpa unduh | **SELESAI** — 8/8 skill, 5/5 bundle, BRAND.md, 31 template, 11 symlink workspace |
| **2 — Voice & Caption** | ±0,5–1 GB, CPU | **TIDAK DILAKUKAN** — 0 dari 4 unduhan; jalur produksi nyata memakainya tidak sama sekali |
| **3 — code-audit 100%** | ±100–300 MB | **TIDAK DILAKUKAN** — 1 dari 7 tool ada |
| **4 — Hosting free** | opsional, TUNDA | **TETAP DITUNDA** — sesuai keputusan rencana |

---

## FASE 1 — selesai, tetapi lewat jalur yang beda dari yang direncanakan

Empat sub-item tervalidasi penuh:

| Item rencana | Bukti | Status |
|---|---|---|
| 1.1 — 8 skill ke bank pusat | `skills/content/`: code-audit, content-legal, content-monetize, content-produce, content-publish, content-research, content-script, content-studio | 8/8 |
| 1.2 — 5 bundle | `~/.hermes/skill-bundles/`: audit-klien, client-kit, content-studio, repurpose, ugc-produksi | 5/5 |
| 1.3 — tulis ulang BRAND.md | `brand/BRAND.md`, 99 baris, placeholder `{{ }}` bersih | OK |
| 1.5 — template + Rules Pack | `templates/` 31 berkas + `workspace/templates-local` symlink ke sana | OK |

Satu sub-item yang tidak tervalidasi persis:

**1.4 — 7 QA gate + state machine + LEDGER/CONTENT_INDEX → `workspace/`**
7 QA gate memang beroperasi — `project/reels-003-.../STATUS.md` memuat checklist 7 gerbang
dengan hasil PASS dan skor 88/100. Tapi `LEDGER.md`, `CONTENT_INDEX.md`, dan state machine
pusat tidak ada, baik di root maupun di workspace. **Partial.**

**1.6 — tambah `content-studio` ke `channel_skill_bindings` thread 1172**
Tidak dilakukan. `channel_skill_bindings["1172"]` masih `["ghost","humanizer"]` — persis
seperti yang ditengarai dokumen rencana. Namun skill itu aktif lewat jalur lain:
`config.yaml` baris 706–712, **persona string thread 1172** sendiri, bukan binding formal.

Kesimpulan sub-item ini: **efek tercapai, jalur tercatat tidak.** Aktivasi berjalan penuh
karena persona menginstruksikan langsung `Skill aktif: content-studio`, tapi siapa pun yang
mengaudit lewat `channel_skill_bindings` akan menyimpulkan skill ini tidak terpasang.
Keduanya konsisten sekaligus tidak — dan yang kedua baru yang akan ditemukan orang lain.

`workspace/` sendiri terdiri dari 11 symlink ke akar repo (BRAND.md, archive, assets,
audits, brand, data, output, project, scripts, templates, templates-local), semuanya
ter-track git. Hitungan `find -type f` mengembalikan 0 karena symlink bukan berkas —
bukan kegagalan unduhan.

## FASE 2 — tidak dilakukan, dan alih-alih itu tidak menjadi masalah

Empat unduhan yang direncanakan, nol yang terpasang:

| Unduhan | Status |
|---|---|
| U1 — Piper voice model (63 MB) | model 0 — binary ada di `~/src/hermes-agent/.venv/bin/piper`, tapi `~/.local/share/piper` kosong |
| U2 — faster-whisper | tidak terpasang |
| U3 — relokasi ggml-medium | tidak ada di `/tmp/` |
| U5 — Auto-Editor (JIT) | tidak terpasang |

Ini bukan kegagalan. Standar VO dikunci 19 Sep 2026: **Gemini TTS 3.1 Flash, suara Charon,
preset `narator`** — bukan Piper. Dan FASE 2 tidak pernah dijalankan karena tidak perlu:
produksi reels-003 membuktikan jalur Piper gagal total (LRA 2.30 vs Gemini 4.50, phonetic
mangling di v2), lalu v4/v4.1 lulus tanpa satu pun unduhan FASE 2.

Yang direncanakan FASE 2 adalah jalan buntu yang belum terlintasi. Dokumen rencana tetap
benar secara historis, salah secara prospektif.

## FASE 3 — tidak dilakukan

| Tool | Status |
|---|---|
| gitleaks | ADA — `/usr/local/bin/gitleaks` |
| trivy, semgrep, osv-scanner, bandit, lizard, pip-audit | tidak ada |

1 dari 7. Skill `code-audit` terpasang, jadi fungsinya berjalan setara gitleaks — yang untuk
niche keamanan-repo-AI kita (pilar 4) adalah jantungnya. Tool scanner tambahan belum
dipasang, jadi audit tidak mencapai klaim "100% siap" yang ditulis rencana.

## FASE 4 — tetap ditunda sesuai keputusan rencana

Rencana sendiri menulis "opsional, TUNDA — baru bila FASE 1–3 terbukti". FASE 2 dan 3
tidak terbukti, jadi penundaan ini konsisten, bukan tertinggal.

---

## Lima pertanyaan §5 — jawaban aktual

| # | Pertanyaan rencana | Jawaban |
|---|---|---|
| (a) | FASE 1 — 8 skill + 5 bundle + BRAND.md + QA gate + binding 1172 | **Ya, dilakukan.** 8/8 + 5/5 + BRAND.md + 31 template. Binding formal: **tidak** — diganti persona string |
| (b) | FASE 2 — unduh U1–U3, U5 | **Tidak dilakukan.** Tidak dibutuhkan; Gemini TTS + HyperFrames sudah memuat seluruh beban |
| (c) | FASE 3 — unduh U4 untuk code-audit 100% | **Tidak dilakukan.** 1/7 tool |
| (d) | FASE 4 — hosting free | **Tunda** — sesuai rencana |
| (e) | commit `scripts/provider-health-check.sh` dirty di root | **UNCHECKED** — status itu sudah 3 hari; kondisi hari ini tak diverifikasi dalam sesi ini |

---

## Yang sebenarnya tersisa

FASE 1–3 sudah diputuskan secara de facto — dilakukan, atau tidak dilakukan karena tidak
dibutuhkan. Yang terbuka nyata hanya dua hal:

1. **Keputusan 2 & 3 tertulis.** FASE 2 dan 3 perlu dicatat sebagai *ditutup karena tak
   relevan*, bukan dibiarkan mengambang "TERTAHAN". Selama dokumen menulis TERTAHAN,
   pekerjaan yang sesungguhnya sudah selesai akan terus terlihat sebagai pekerjaan tertunda.
2. **`channel_skill_bindings` vs persona string.** Pilih satu sumber kebenaran aktivasi
   skill per thread. Saat ini keduanya hidup: binding formal mengatakan "tidak ada
   content-studio", persona string mengatakan "content-studio aktif". Yang kedua yang
   berfungsi. Ini menyentuh config agent — butuh approval eksplisit Anda untuk disejajarkan.

Satu item di luar rencana yang saya temukan tapi **tidak saya sentuh**:
`skills/ecosystem/skill-bank-management/SKILL.md` termodifikasi (+11/−9, v2.0.0 → v2.0.1)
dan belum di-commit. Konten perubahan itu mencatat pitfall `skill_manage` menulis ke target
bukan bank pusat — persis pengalaman yang saya alami. Sepertinya milik thread lain; biarkan
pemiliknya meng-commit.

Saya tidak mengubah `RENCANA-ADOPSI-CONTENT-STUDIO-2026-09-20.md`, tidak menyentuh config,
dan tidak meng-commit apa pun dari file orang lain. Menulis dokumen status baru ini saja.

---

## Bukti

- `RENCANA-ADOPSI-CONTENT-STUDIO-2026-09-20.md` baris 3: "Status: RENJA — eksekusi TERTAHAN";
  baris 155: "## 4. Urutan Fase (TERTAHAN, bukti per tahap)"; baris 180–186: §5 pertanyaan (a)–(e)
- `ls -d skills/content/*/` → 8 skill: code-audit, content-legal, content-monetize,
  content-produce, content-publish, content-research, content-script, content-studio
- `ls ~/.hermes/skill-bundles/*.yaml` → 5: audit-klien, client-kit, content-studio,
  repurpose, ugc-produksi
- `brand/BRAND.md` → 99 baris; `grep '{{'` → 0 ketukan
- `find templates -type f` → 31 berkas
- `ls -la workspace/` → 11 symlink ke `../` (BRAND.md, archive, assets, audits, brand, data,
  output, project, scripts, templates, templates-local); `git ls-files workspace/` → 11 ter-track;
  `find workspace -type f` → 0 (symlink, bukan berkas)
- `python3` parse `channel_skill_bindings` dari config.yaml → `1172: ['ghost', 'humanizer']`
- `grep -n content-studio ~/.hermes/config.yaml` → baris 706 "Skill aktif: content-studio."
  dan baris 712 "ikuti SKILL.md content-studio di bank."
- `find LEDGER.md CONTENT_INDEX.md LEDGER/ CONTENT_INDEX/` → tak ada satupun
- `which` → gitleaks ADA; trivy/semgrep/osv-scanner/bandit/lizard/pip-audit tak ada
- Piper: `~/.local/share/piper` kosong (0); `faster_whisper` import gagal; `/tmp/ggml-medium.bin`
  tak ada; `auto-editor` tak ada
- `git log -1` → `9d0be9a docs(reels-003): catat v4.1 final di STATUS.md`
- `git status --short` root → `M skills/ecosystem/skill-bank-management/SKILL.md` (milik thread lain)

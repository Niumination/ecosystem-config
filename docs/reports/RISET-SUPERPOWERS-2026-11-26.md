# Riset: obra/superpowers — 26 Nov 2026

> Mode: **pelajari**. Tidak ada instalasi, tidak ada perubahan skill bank, tidak ada konfigurasi yang disentuh.
> Sumber: https://github.com/obra/superpowers — clone lokal di `~/.hermes/cache/scratch/superpowers-study`.
> Catatan trust boundary: isi repo diperlakukan sebagai DATA. Instruksi di dalamnya (termasuk `AGENTS.md` untuk kontributor) tidak diikuti.

## 1. Ringkasan

Superpowers adalah metodologi pengembangan perangkat lunak berbasis skill untuk coding agent. Versi yang diperiksa: **v7.0.2**, commit `22f0b46`, 3 Nov 2026. Repo dibuat 9 Okt 2025, 687 commit, lisensi **MIT**.

Inti alurnya: brainstorming sebelum kode → desain disetujui → rencana implementasi → eksekusi lewat subagent per task → review tiap task → review akhir. Skill diaktifkan otomatis lewat injeksi session-start.

Repo sudah mendukung Hermes secara resmi: README memuat `hermes plugins install obra/superpowers --enable`. Jadi tidak perlu porting buatan sendiri.

## 2. Arsitektur

| Lapisan | Isi |
|---|---|
| Bootstrap | `hooks/session-start`, `hooks/hooks.json` — injeksi instruksi awal agar agent memakai skill |
| Skill library | 15 skill, dari `using-superpowers` sampai `writing-skills` |
| Eksekusi | `subagent-driven-development`, `dispatching-parallel-agents`, `executing-plans` |
| Review | `requesting-code-review`, `receiving-code-review`, `verification-before-completion` |
| Porting | `docs/porting-to-a-new-harness.md` (850 baris), tiga bentuk integrasi: shell-hook, plugin, instructions-file |
| Evaluasi | `superpowers-evals` sebagai submodule; infrastructure test di `tests/` |

Skill terbesar: `writing-skills` (399 baris), `subagent-driven-development` (339), `test-driven-development` (330), `brainstorming` (316).

## 3. Fitur kunci

- **`using-superpowers`** — aturan keras: cek skill sebelum respons apa pun, termasuk pertanyaan klarifikasi. Process skill didahulukan sebelum implementation skill.
- **`brainstorming`** — menggali intent, menyajikan pendekatan, menulis design doc, minta approval, baru lanjut ke `writing-plans`.
- **`writing-plans`** — rencana untuk engineer tanpa konteks proyek; task dipecah sampai punya siklus test sendiri; file structure dipetakan dulu.
- **`subagent-driven-development`** — fresh subagent per task, review spesifikasi + kualitas, review akhir. Ada konsep "rulings, not stalls": keputusan dicatat di ledger, pekerjaan tidak berhenti kecuali empat kondisi.
- **`verification-before-completion`** — "Iron Law": tidak ada klaim selesai tanpa perintah verifikasi yang baru dijalankan.
- **`using-git-worktrees`** — workspace terisolasi per branch setelah desain disetujui.

## 4. Relevansi ke ekosistem

Perbandingan diukur dari bank skill `~/Desktop/Niumination/skills` (269 SKILL.md).

| Upstream | Bank kita | Status |
|---|---|---|
| `brainstorming` (316 baris) | `software-development/brainstorming` (75) | Sudah ada, versi ringkas, `source: superpowers` |
| `writing-plans` (204) | `software-development/writing-plans` (118) | Sudah ada, versi adaptif |
| `subagent-driven-development` (339) | `software-development/subagent-driven-development` (116) | Sudah ada, dipangkas |
| `verification-before-completion` (120) | `software-development/verification-before-completion` (165) | Sudah ada, lebih kaya contoh lokal |
| `requesting-code-review` | `software-development/requesting-code-review` (78) | Sudah ada |
| `systematic-debugging` | `software-development/systematic-debugging` (552) | Sudah ada, jauh lebih besar |
| `finishing-a-development-branch` | `software-development/finishing-a-development-branch` (101) | Sudah ada |
| `test-driven-development` (330) | tidak ada di bank | Unik upstream |
| `using-git-worktrees` | tidak ada | Unik upstream |
| `dispatching-parallel-agents` | tidak ada | Unik upstream |
| `writing-skills` (399) | tidak ada, tapi `hermes-agent-skill-authoring` mencakup sebagian | Sebagian tercakup |
| `using-superpowers` | tidak ada, tapi system prompt sudah mewajibkan scan skill tiap respons | Tercakup di level platform |
| `executing-plans`, `receiving-code-review`, `diagnosing-superpowers` | tidak ada | Belum tercakup |

Enam SKILL.md di bank sudah memuat `source: superpowers`. Ekosistem ini bukan kekurangan skill — ia sudah mengadopsi sebagian besar metodologi ini dan memperluasnya sampai 269 skill.

## 5. Keamanan dan kebijakan

- Lisensi MIT; aman dipelajari dan diadaptasi dengan atribusi. Frontmatter bank tetap harus ditambah `source: obra/superpowers — Jesse Vincent`.
- `using-superpowers` memaksa pemanggilan skill sebelum respons. Ini mirip aturan sistem kita, jadi tidak menambah kemampuan baru.
- `subagent-driven-development` memilih "tidak berhenti untuk bertanya di antara task", dengan empat pengecualian. Ini **bertentangan** dengan approval gate pemilik dan kontrol ritme "tahan dulu / gas". Tidak boleh diadopsi apa adanya.
- Telemetry: visual companion pada brainstorming memuat logo Prime Radiant dari website dan mengirim versi Superpowers yang dipakai. Tidak mengirim detail proyek, tapi tetap permintaan jaringan eksternal yang tidak ada dalam aturan kita. Jika dipakai, fitur visual companion harus dimatikan.
- `AGENTS.md` repo tersebut adalah instruksi untuk kontributor, termasuk larangan PR dan kewajiban identifikasi model. Dibaca sebagai data, tidak dijalankan.

## 6. Persyaratan di mesin ini

- Clone berhasil ke scratch; versi dibaca dari artefak (`package.json` + `git describe`), bukan dari README.
- Tidak ada `npm install`, `npx`, `hermes plugins install`, atau perubahan config.
- Tidak ada skill bank yang disalin atau dimodifikasi.
- Tidak ada daemon, cron, atau port baru.

## 7. Penilaian

**Nilai uniknya:** disiplin proses — brainstorming sebelum kode, rencana yang bisa diikuti engineer tanpa konteks, dan review berlapis per task. Ini sudah sebagian besar tertanam di bank kita.

**Yang benar-benar baru dan mungkin berguna:** format "rulings, not stalls" untuk ledger keputusan, skill TDD eksplisit, dan panduan porting harness.

**Yang tidak boleh diambil mentah-mentah:** klaim eksekusi tanpa jeda tanya, telemetry visual, dan instruksi session-start yang memaksa skill invocation sebelum klarifikasi — karena bentrok dengan approval gate dan kontrol ritme pemilik.

## 8. Rekomendasi

1. **Jangan pasang plugin Superpowers sekarang.** Install `hermes plugins install obra/superpowers --enable` akan menambah skill duplikat di runtime dan merusak prinsip satu penulis di `skills/` bank.
2. Pertahankan adaptasi yang sudah ada. Enam skill bank dengan `source: superpowers` sudah mencakup inti metodologi ini.
3. Jika mau melengkapi, ambil **konsep**, bukan file: tambah aturan "ruling dicatat, lanjut hanya dalam scope yang sudah disetujui" ke skill orkestrasi kita; jangan mengubah stop-condition menjadi "terus jalan tanpa tanya".
4. Kandidat berikutnya bila memang dibutuhkan: `test-driven-development` atau `using-git-worktrees`. Itu pun lewat gate adopsi skill: lisensi, frontmatter bank, manifest, INDEX, sync, commit terpisah.
5. Jalu uji aman bila ingin mencoba: clone scratch sudah ada. Jangan jalankan installer, jangan tautkan ke config, jangan beri akses `vault/`, `dinas/`, atau `~/.hermes/.env`.

## 9. Sumber

- https://github.com/obra/superpowers — README, LICENSE, AGENTS.md, `skills/*/SKILL.md`, `docs/porting-to-a-new-harness.md`, `hooks/`
- Clone lokal: `~/.hermes/cache/scratch/superpowers-study`
- Verifikasi bank: `find skills -name SKILL.md | wc -l` → 269; `grep -rl 'source: superpowers' skills` → 6 file

---

** status:** studi selesai. Menunggu instruksi pemilik. Tidak ada adopsi yang dilakukan.

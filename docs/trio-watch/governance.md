# Trio Governance — Aturan Kerja Sama Tim

> **Tanggal Berlaku:** 26 Agustus 2026
> **Status:** ✅ Approved v2

---

## Prinsip Dasar

1. **Manusia = Sumber Aturan** — Anda bekerja di mana saja yang diperlukan (root, services/, labs/, dll). Agent tidak membatasi lokasi, tapi memahami **konteks dan tujuan**.
2. **Agent = Executor + Reporter** — melaksanakan sesuai intent, melaporkan dampak, TIDAK bertindak asertif tanpa klarifikasi.
3. **Tim = 3 Agen** — Hermes (ecosystem), JCode (cc-acehtengah), OpenCode (labs/experiment). Setiap agen punya **domain keahlian**, bukan **domain folder**.

---

## Pemahaman Konteks (BUKAN Batas Folder)

| Lokasi Kerja | Agen Utamanya | Tapi bisa diakses agen lain jika: |
|--------------|---------------|----------------------------------|
| `services/cc-acehtengah/` | JCode | Hermes perlu update AGENTS.md, OpenCode mau clone untuk analisis |
| `~/Desktop/Niumination/` (root) | Hermes | JCode perlu commit docs proyek, OpenCode mau tambahkan skill |
| `apps/*/` | Sub-repo mandiri | Setiap agen bisa akses sebagai reader, tapi commit hanya owner repo |
| `labs/`, `desktop/` | OpenCode | JCode/Hermes butuh referensi untuk dokumentasi |

**Prinsip:** Folder adalah organisasi, bukan penjara. Agent harus tanyakan:
> "Anda mau saya kerjakan ini dari konteks cc-acehtengah atau ekosistem?"

---

## Mekanisme Trio-Watch

```bash
bash scripts/trio-watch.sh --from hermes
bash scripts/trio-watch.sh --from jcode
bash scripts/trio-watch.sh --from opencode
# Output: scripts/.trio-status.json
```

Setiap agen kirim:
- Context kerja (cc-acehtengah / ecosystem / labs)
- Intent yang dipahami
- File yang dipegang
- Rencana selanjutnya
- Permintaan klarifikasi (jika ambigu)

Hermes = coordinator, alert jika overlap/ambiguitas.

---

## Aturan Dampak Sebelum Eksekusi

```markdown
## DAMPAK EKSEKUSI
- Context: [cc-acehtengah / ecosystem / mixed]
- Yang berubah: [file/folder]
- Intent yang dimengerti: [apa tujuan user]
- Risiko: [data hilang? breaking change?]
- Rollback: [cara kembalikan]
- Approval: [ya/tidak]
```

---

## Klarifikasi Sebelum Bertindak

Agent WAJIB bertanya jika:
1. Lokasi kerja ambigu (root vs services)
2. Intent tidak jelas ("kerjakan yang perlu" tanpa spesifik)
3. Ada potensi konflik dengan agen lain
4. Perubahan menyentuh file lintas domain

---

## Kontrak Penanganan File

### File tersesat di lokasi salah
**Akar masalah:** Agent tidak memastikan lokasi benar sesuai konteks proyek.

**Solusi:**
1. Verifikasi intent: untuk cc-acehtengah atau ecosystem?
2. Letakkan di domain yang sesuai
3. Hapus duplikat
4. Catat di trio-status.json

### apps/ tidak ter-track di root
**Sudah dikontrak:** sub-repo mandiri, root hanya index/katalog.

---

## Eskalasi

Jika konflik/ambiguitas:
1. Stop, jangan asumsikan
2. Log di trio-status.json
3. Human clarification required

---

*Approved: 26 Agustus 2026*

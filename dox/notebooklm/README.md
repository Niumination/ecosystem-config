# NotebookLM — Ecosystem Knowledge Base

**Path:** `dox/notebooklm/`
**Default data directory** untuk semua output NotebookLM dalam ekosistem Niumination.

## Struktur

```
dox/notebooklm/
├── README.md              ← File ini
├── notebooks/             ← Referensi notebook NotebookLM
│   ├── niumination-ecosystem/   ← Ekosistem Niumination
│   └── zhall-pemdi/              ← Zhall × PemdiAcehTengah
└── artifacts/             ← Downloaded artifacts (audio, video, reports, dll)
```

## Notebook Aktif

| Notebook | ID | Sources | Purpose |
|----------|-----|---------|---------|
| Niumination Ecosystem | `0e266f0d-323a-46aa-b01c-4de48badde23` | 18 | BACKLOG.md, AGENTS.md, URL production |
| Zhall-Pemdi | `fd27a0ca-b180-4edf-afa4-e465e24577c3` | 19 | Dokumentasi PemdiAcehTengah |

### Sources Zhall-Pemdi
- **Inti:** PRD_PORTAL_PEMDI.md, STRATEGI_PEMDIACEHTENGAH.md, MASTERPLAN.md, BACKLOG.md
- **Dokumen:** Panduan Peningkatan Indeks, draft SK tim pemda, paparan sekda, plan-v0, requirement peta proses bisnis
- **Riset:** Data Aceh Tengah, peta proses bisnis PermenPAN 19/2018
- **PDF:** Indeks SPBE Aceh Tengah 2025, PermenPAN RB 8/2026
- **Desain:** Glosarium istilah, Panduan desain UI/UX
- **Audit:** Hasil verifikasi perbaikan V2, Laporan audit
- **Lain:** Jumlah Perangkat Daerah (DOCX), README, CONTRIBUTING, AGENTS

## Cara Update

Via Hermes agent:
```bash
nlm login --check       # verify auth
nlm source add <notebook-id> --url <url> --wait
```

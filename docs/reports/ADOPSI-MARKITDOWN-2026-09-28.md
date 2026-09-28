# Adopsi MarkItDown (Microsoft) ke Ekosistem Niumination

**Tanggal:** 2026-09-28
**Jenis:** Studi adopsi + uji coba terverifikasi
**Sumber:** github.com/microsoft/markitdown (MIT, 187k stars, 406 commit, update terakhir 21 Sep 2026)
**Pemicu:** Permintaan pemilik: "pelajari markitdown dari microsoft di github untuk di adopsi ke ekosistem kita"

---

## 1. Ringkasan Eksekutif

MarkItDown adalah konverter dokumen perkantoran → Markdown buatan Microsoft, dirancang untuk
konsumsi LLM. **Diadopsi sebagai tool ingestion umum** — terinstal terisolasi via `uv tool`,
bertahan sebagai CLI yang dipanggil dari skill bank, mengisi gap konversi dokumen universal
yang selama ini tersebar di banyak skill.

**Status: TERINSTAL & TERUJI** (bukan sekadar studi — 9 dari 10 format berhasil dikonversi
nyata di mesin ini). Tidak menggantikan pipeline ODL-PDF untuk dokumen kompleks.

---

## 2. Apa Itu MarkItDown

Konverter file → Markdown untuk LLM pipeline. Fokus **struktur** (heading, list, table, link),
bukan fidelitas visual. Dibandingkan textract, MarkItDown mempertahankan struktur dokumen.

**Format didukung:** PDF, PowerPoint (.pptx), Word (.docx), Excel (.xlsx/.xls), Image (EXIF+OCR),
Audio (EXIF+transkripsi), HTML, CSV/JSON/XML, **ZIP (iterasi isi)**, **URL YouTube (transkrip)**,
EPub.

**Paket:** `markitdown` (core+CLI) · `markitdown-mcp` (MCP server) · `markitdown-ocr` (OCR
gambar dalam dokumen pakai LLM Vision) · `markitdown-sample-plugin`.

**API Python** (dari README resmi, tervalidasi struktur):
```python
from markitdown import MarkItDown
md = MarkItDown()                              # atau llm_client/llm_model untuk OCR gambar
result = md.convert("file.xlsx")
print(result.markdown)
```

---

## 3. Kondisi Ekosistem Sebelum Adopsi — probe nyata

| Item | Hasil probe 2026-09-28 |
|---|---|
| markitdown di Python sistem (3.14.7) | tidak ada |
| markitdown di Hermes venv (3.11) | tidak ada |
| Referensi "markitdown" di ekosistem aktif | tidak ada (hanya 2 file di `inactive-2026-09/JHermUSB-portable/`, dormant) |
| MCP server di config Hermes | kosong |
| Docker | **tidak ada** → jalur container tertutup |
| Java | `/usr/bin/java` ada → ODL-PDF masih mungkin |
| pip / uv | pip 26.2.1 · uv terinstal |
| Library doc di Python sistem | openpyxl ✓ · pandas ✓ · (pypdf/pdfminer/docx/pptx/fitz/mammoth tidak ada) |
| Tool dokumen existing | `document-content-pipeline` (ODL-PDF, Pemdi), `skills/productivity/{pdf,docx,pptx,xlsx}`, `tools/pdf-inspector`, `scripts/odl-pdf*.py` |

**Koreksi data lama:** memori mencatat `pip=missing`. Probe 2026-09-28 menunjukkan pip 26.2.1
tersedia. Data lama dibuang, data baru yang dipakai.

---

## 4. Hasil Uji Nyata — 2026-09-28 /tmp/mdtest

Fixture dibuat sintetis tanpa PII (tidak ada dokumen SKP/CV/NIP yang dipakai untuk uji —
semua dokumen di ekosistem mengandung PII pemilik).

| Format | Fixture | Hasil | Keluaran |
|---|---|---|---|
| CSV | `data.csv` 3 baris | ✅ rc=0 | tabel Markdown sempurna |
| JSON | `data.json` nested | ✅ rc=0 | dipertahankan apa adanya |
| XML | `config.xml` | ✅ rc=0 | dipertahankan apa adanya |
| HTML | `page.html` (h1/p/b/a/ul/table) | ✅ rc=0 | `#`, `**tebal**`, `[tautan](url)`, bullet, tabel |
| XLSX | `sheet.xlsx` 3 baris | ✅ rc=0 | `## Sheet1` + tabel rapi |
| PPTX | `slide.pptx` judul+body | ✅ rc=0 | `<!-- Slide number: 1 -->` + `# Judul` |
| DOCX | `doc.docx` heading+paragraf | ✅ rc=0 | `# Judul` + paragraf |
| **ZIP** | `arsip.zip` (2 file di dalam) | ✅ rc=0 | **iterasi otomatis seluruh isi + header per file** |
| PDF | — | ⚠️ **TIDAK TERUJI** | fixture PDF tidak bisa dibuat (fpdf & pdflatex tidak ada) |
| YouTube | — | ⚠️ **TIDAK TERUJI** | butuh jaringan + video target |

### Temuan kegagalan (harus dibungkus skill)

1. **File hilang → traceback + rc=120.** Bukan error bersih. Skill harus mencegah ini
   (`test -f` sebelum panggil, atau tangkap rc).
2. **Input direktori → `IsADirectoryError` traceback + rc=1.** CLI hanya menerima file
   satuan; batch harus loop di pemanggil.
3. **Glob `*.csv` literal → FileNotFoundError.** Shell-expansion saja; jangan teruskan
   glob mentah.
4. **Multi-file `markitdown a.csv b.json` → rc=2 "unrecognized arguments".** CLI hanya
   1 file per pemanggilan; batch = loop.

---

## 5. Keputusan Desain Adopsi

### Yang diadopsi
- **CLI terisolasi** `uv tool install 'markitdown[all]'` — venv terpisah (Python 3.12),
  tidak menyentuh Python sistem 3.14 maupun Hermes venv 3.11.
- **Skill bank** `skills/research/markitdown/` sebagai pembungkus + gate keamanan.
- Versi terinstal: **0.1.8** · path CLI: `~/.local/bin/markitdown`.

### Yang sengaja TIDAK diadopsi (alasan tervalidasi)
| Komponen | Alasan |
|---|---|
| `markitdown-mcp` (MCP server) | Config MCP ekosistem kosong; server yang selalu-on menambah permukaan serangan untuk input multi-user Telegram. Gate keamanan lebih mudah dipegang di skill (rung 2 Footprint Ladder). |
| `markitdown-ocr` | Biaya LLM per gambar. Ekosistem sudah punya **macOS Vision gratis** (terverifikasi untuk dokumen Indonesia, lihat `document-content-pipeline` Step 2c). |
| Azure Doc Intelligence / Content Understanding | API berbayar + kredensial baru + bukan kebutuhan. |
| Docker | Tidak terinstal. |

### Pemisahan tugas (yang harus dipegang erat)
- **markitdown = ingestion umum** cepat: docx/pptx/xlsx/html/csv/json/xml/zip/epub → markdown
- **ODL-PDF (`document-content-pipeline`) = high-fidelity** untuk dokumen pemerintah kompleks.
  Benchmark #1 akurasi 0.907. Masalah PPT→PDF Pemdi sudah berinvestasi raksasa dan teratasi.
  **MarkItDown TIDAK menggantikan ini** — basis PDF-nya pdfminer, fidelitas lebih rendah.

---

## 6. Keamanan (prioritas 1 — Telegram multi-user)

MarkItDown melakukan I/O dengan privilese proses pemanggil (peringatan eksplisit Microsoft).
Skill wajib menerapkan:

- Hanya input **lokal**; `convert_local()` / path file, jangan `convert()` generik (menerima
  URI jarak jauh → SSRF).
- `test -f` sebelum pemanggilan; tangkap rc≠0 (CLI memuntahkan traceback, bukan error bersih).
- Tolak path di luar allowlist; tolak direktori (`IsADirectoryError`).
- Jangan teruskan glob mentah (`*.csv` literal → FileNotFoundError).
- 1 file per pemanggilan — batch = loop, jangan multi-arg.
- Input user dari grup Telegram = **data tidak terpercaya**; tidak pernah teruskan URI.

---

## 7. Bukti Perintah

```
uv tool install 'markitdown[all]'        → Installed 2 packages (markitdown 0.1.8 + magika)
uv tool list                             → markitdown v0.1.8
command -v markitdown                    → /Users/zaryu/.local/bin/markitdown
markitdown --version                     → markitdown 0.1.8
markitdown data.csv                      → rc=0, tabel markdown 3 baris
markitdown data.json                     → rc=0
markitdown config.xml                    → rc=0
markitdown page.html                     → rc=0, # + **tebal** + [link] + bullet + table
markitdown sheet.xlsx                    → rc=0, ## Sheet1 + tabel
markitdown slide.pptx                    → rc=0, <!-- Slide number: 1 --> + # Judul
markitdown doc.docx                      → rc=0, # Judul + paragraf
markitdown arsip.zip                     → rc=0, iterasi 2 file dalam zip
markitdown /tmp/mdtest (dir)             → rc=1 IsADirectoryError traceback
markitdown /tmp/tidak-ada.pdf            → rc=120 FileNotFoundError traceback
markitdown a.csv b.json                  → rc=2 unrecognized arguments
```

---

## 8. UNCHECKED

- **PDF tidak teruji.** Fixture PDF tak bisa dibuat: `fpdf` tidak terinstal, `pandoc` ada
  tapi `pdflatex` tidak. Klaim kualitas PDF markitdown belum dibuktikan di mesin ini.
- **YouTube & transkripsi audio tidak teruji** (butuh jaringan + target).
- **OCR gambar dalam dokumen** tidak teruji (plugin sengaja tidak diadopsi).
- **Interaksi dengan pipeline ODL-PDF** tidak diuji secara komparatif — pemisahan tugas
  di §5 berdasarkan dokumentasi ODL, bukan benchmark berdampingan.
- **Python 3.14 build** tidak teruji — yang terinstal adalah venv Python 3.12 milik `uv tool`.

---

## 9. Langkah Berikutnya

1. Uji PDF nyata pada dokumen publik non-PII (mis. PDF regulasi terbuka) untuk membuktikan
   kualitas ekstraksi PDF — menutup UNCHECKED terbesar.
2. Catat `markitdown` di registry ekosistem.
3. Tambah trigger keyword ke DOX AGENTS.md Level 2 jika pemilik mau skill auto-load.

# Otak Gratis + Meriam Berbayar — Arsitektur Dua Tingkat untuk Hermes & jcode
**Draft analisis v3 · 2026-08-21 · Penyusun: agen (Arena) · Status: menunggu seal manusia (zaryu)**

> **Strategi (pilihan zaryu):** model utama = **model gratis OpenCode Zen**;
> OpenCode Go dipakai untuk **tugas berat** dan **fallback** saat model gratis kena limit.
> Catatan governance: `core/MODEL.policy.yaml` berstatus TERSEGEL — dokumen ini draft, bukan mutasi.
> Agen hanya boleh draft; manusia mengesahkan.

---

## 1. Keputusan yang Diusulkan (Ringkas)

| Tingkat | Peran | Model | Provider | ID | Alasan |
|---|---|---|---|---|---|
| **T0 — Gratis** | **Otak utama daemon Hermes** (Telegram, cron, tugas umum) | **Nemotron 3 Ultra Free** | OpenCode Zen | `opencode-zen/nemotron-3-ultra-free` | 🏆 Model **paling powerful di tier gratis Zen** — flagship open NVIDIA; kandidat lain jauh di bawahnya (lihat §4.1) |
| T0 — Gratis | Cadangan se-tier (masih $0) | Nemotron 3.5 Lightning Free | OpenCode Zen | `opencode-zen/nemotron-3.5-lightning-free` | Same-family NVIDIA; build kecepatan — turun kelas tanpa keluar $0 |
| T0 — Gratis | Kompresi, cron ringan, sideagent | **MiMo-V2.5 Free** / Hy3 Free | OpenCode Zen | `mimo-v2.5-free`, `hy3-free` | Workhorse gratis konfirmasi di daftar resmi; *model lemah tidak membaca esai — dan tidak perlu* |
| **T1 — Go** | **Fallback otomatis** saat T0 429 **+ tugas berat terencana** | **GLM-5.2** | OpenCode Go | `opencode-go/glm-5.2` | Model terkuat Go dengan kuota $60 penuh (±880 req/5 jam) — satu-satunya yang sanggup menggendong daemon saat tier gratis tumbang |
| T1 — Go | Eskalasi maksimum (manual saja) | **Kimi K3** | OpenCode Go | `opencode-go/kimi-k3` | Power mentah tertinggi di Go; kuota tipis (±110 req/5 jam) → dilarang untuk daemon/cron |
| T1 — Go | **Otak jcode** (harness coding) | **Kimi K2.7 Code** | OpenCode Go | `opencode-go/kimi-k2.7-code` | Spesialis kode, ±1.350 req/5 jam; swarm/memori jcode → model T0 gratis |
| T2 — Zen PAYG (opsional) | Insiden kritis SPBE / arsitektur final | Claude Sonnet 5 / Opus 5 | OpenCode Zen | `claude-sonnet-5`, `claude-opus-5` | Zero-retention, frontier proprietary; bayar per request, approval manual |

**Satu kalimat:** Nemotron 3 Ultra Free memikul hari-hari biasa, GLM-5.2 menangkapnya saat jatuh dan mengangkat beban berat, Kimi K3 tetap jadi meriam di gudang — dan data sensitif pemerintah tidak pernah menyentuh tier gratis.

---

## 2. Dasar Fakta (hasil studi ekosistem, 20–21 Agu 2026)

### 2.1 Ekosistem
40+ repo aktif, identitas SPBE/GovTech + AI Agent; dua harness utama: **Hermes Agent v0.19** (daemon 24/7: Telegram 5 thread, cron, skills, memori) dan **jcode** (fork Rust coding harness); orkestrasi di `ecosystem-config` (AGENTS.slim, CONSTITUTION, ledger, fence, hooks `niu-*`).

### 2.2 Insiden drift 20 Agu (bukti empiris)
±40 handoff dalam sehari (13:45–22:10 WIB), sesi Telegram didrift ke `stepfun/step-3.7-flash:free` & `nemotron-3-ultra-free`, fence `active:true` hingga 22:10 dengan nol kerja selesai. Akar masalah: **berburu model gratis tanpa seal** — bukan pagar (pagar bekerja sempurna). Implikasi: memakai `nemotron-3-ultra-free` itu sendiri *boleh* — asal diangkat resmi lewat DECISION seal, bukan injeksi diam-diam seperti semalam.

### 2.3 Tier gratis Zen resmi (diverifikasi dari opencode.ai/docs/zen, 21 Agu)
| Model Gratis | Karakter | Cocok untuk |
|---|---|---|
| **Nemotron 3 Ultra Free** | Flagship open NVIDIA — terkuat di tier ini | **Otak utama** |
| Nemotron 3.5 Lightning Free | Build kecepatan, keluarga sama | Cadangan se-tier |
| Muse Spark 1.2 Contributor Free | Meta, **region terbatas** | ❌ bukan untuk daemon 24/7 di ID |
| Big Pickle | Stealth, kelas menengah | Otak lama (digantikan Ultra) |
| Hy3 Free | Kecil-murah | Workhorse |
| MiMo-V2.5 Free | Kecil-murah | Workhorse/kompresi |

**Dua peringatan resmi dari halaman Zen (wajib masuk policy):**
1. **Privasi** — semua model Zen zero-retention *kecuali* model gratis: *"during its free period, collected data may be used to improve the model"*; khusus Nemotron 3 Ultra Free (endpoint gratis NVIDIA): **"Trial use only — do not submit personal or confidential data."**
2. **Limited time** — semua model gratis ditawarkan "for a limited time"; family gratis bersifat sementara → wajib ada aturan transisi.

---

## 3. Konsekuensi Arsitektur

1. **Dua tingkat, tetap satu kaki Zen.** T0 (gratis) dan T1 (Go) keduanya hidup di bawah satu akun/API key Zen — prinsip *"fallback 1 kaki Zen"* tidak dilanggar.
2. **Batas data keras.** Tier T0 = hanya tugas umum/non-sensitif. Data ASN, SK, bukti dukung eKinerja, kredensial, isi `vault/` → wajib T1 (zero-retention). Ini hukum, bukan saran.
3. **Fallback punya pagar.** T0 429 → T1 `glm-5.2` → `fence_core_writes` (aturan lama tetap). Fallback bukan izin melanjutkan mutasi core seolah tak terjadi apa-apa.
4. **Jangan berburu gratis.** Saat model gratis dihapus Zen (limited time), agen TIDAK boleh mencari pengganti gratis sendiri → tulis handoff, jatuh ke T1, tunggu seal baru. (Ini pelajaran langsung dari insiden 20 Agu.)

---

## 4. Cuplikan Konfigurasi

### 4.0 Pre-flight P0 (masih wajib — temuan 20 Agu)
1. Turunkan fence (`fence.json` 22:10 masih `active:true`) lewat prosedur resmi.
2. Putus jalur injeksi model asing (cc-switch / profil jcode / setelan gateway).
3. Satukan 5 thread Telegram ke T0.
4. **Seal DECISION baru** → baru switch model. Setelah switch: fence core writes, jangan langsung lanjut tugas mutasi.

### 4.1 Hermes — `~/.hermes/config.yaml`
```yaml
model:
  provider: opencode-zen
  default: nemotron-3-ultra-free          # T0 — otak utama gratис
  base_url: https://opencode.ai/zen/v1
  fallbacks:
    - provider: opencode-zen
      model: nemotron-3.5-lightning-free  # T0 cadangan se-tier (masih $0)
    - provider: opencode-go
      model: glm-5.2                      # T1 — fallback berbayar → fence core writes
compression:
  provider: opencode-zen
  model: mimo-v2.5-free                   # gratis; ringkasan memori non-sensitif
  threshold: 0.50
```
Tugas berat terencana: `/model opencode-go/glm-5.2` · eskalasi manual maksimum: `/model opencode-go/kimi-k3`.

### 4.2 jcode
```toml
# ~/.jcode/config.toml
[provider]
default_provider = "opencode-go"
default_model    = "kimi-k2.7-code"      # otak coding — ±1.350 req/5jam

[agents]
swarm_model   = "mimo-v2.5-free"          # sub-agent murah dari tier gratis
memory_model  = "hy3-free"
```

### 4.3 Usulan policy lengkap: `MODEL.policy.v2.proposed.yaml` · Formulir: `D-NNNN-*.draft.yaml`

---

## 5. Risiko & Mitigasi
| Risiko | Mitigasi |
|---|---|
| Data pemerintah bocor ke tier gratis (NVIDIA: *no personal/confidential data*) | Hukum T0/T1 di policy: sensitif → T1 zero-retention; kompresi memori yang mungkin menyentuh cuplikan sensitif → T1 `deepseek-v4-flash` |
| Model gratis dihapus Zen (limited time) | Aturan transisi: jatuh ke T1 + handoff; **dilarang** berburu pengganti gratis tanpa seal (pelajaran 20 Agu) |
| Fallback T1 dipakai terus hingga kuota habis | Setelah switch → fence core writes; telegram unify menunjuk T0 agar kembali otomatis saat pulih |
| Kimi K3 dipakai daemon | K3 = manual-escalation-only; masuk daftar `never` |
| Drift model asing | `drift_guard` + forbidden_thinkers diperluas (stepfun, nemotron pra-seal, gemini-lite) — mekanisme terbukti bekerja 20 Agu |
| Chat dijadikan arsip | Keputusan disegel via DECISION.yaml di `core/ledger/decisions/` |

*Sumber: opencode.ai/docs/zen & /docs/go (21 Agu 2026); repo publik Niumination (incl. commit 82188f3, fence.json, session-models.json); docs 1jehuang/jcode & NousResearch/hermes-agent.*

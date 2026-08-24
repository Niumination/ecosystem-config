# OPSI 2 — "Throughput-First": Gratis Zen + Go Paling Longgar
**Draft analisis · 2026-08-21 · Penyusun: agen (Arena) · Status: menunggu seal manusia (zaryu)**

> **Mandat:** Zen = hanya model gratis · Go = hanya yang rate-limit paling longgar ·
> dengan syarat tetap **powerful** untuk Hermes dan jcode.
> Pendamping Opsi 1 (`LAPORAN.md`, "Quality-First"). Pilih salah satu — jangan dicampur
> tanpa seal baru. Agen hanya boleh draft; manusia mengesahkan.

---

## 1. Keputusan Opsi 2 (Ringkas)

| Peran | Model | Provider | Kuota (req/5 jam) | Alasan |
|---|---|---|---|---|
| **Otak utama Hermes** (Telegram, cron, tugas umum) | **Nemotron 3 Ultra Free** | Zen (gratis) | — ($0) | Terkuat di tier gratis Zen — flagship open NVIDIA; sama dengan Opsi 1 |
| Cadangan se-tier (tetap $0) | Nemotron 3.5 Lightning Free | Zen (gratis) | — | Same-family NVIDIA; turun kelas tanpa keluar biaya |
| **Fallback otomatis + tugas berat** | **MiniMax M3** | Go | **3.200** (16.000/bln) | 🏆 titik temu "paling longgar × paling powerful" di Go: flagship agentic MiniMax — **3,6× kuota GLM-5.2** (880) dengan daya pukul sekelas |
| Cadangan same-family T1 | MiniMax M2.7 | Go | 3.400 | Fallback M3 tanpa keluar keluarga |
| **Safety net ultra-longgar** | **DeepSeek V4 Flash** | Go | **7.600** (37.800/bln) | Penyelamat saat M3 pun habis; paling longgar di Go yang masih layak berpikir; off-peak lebih murah |
| **Otak jcode** | **DeepSeek V4 Flash** | Go | **7.600** | Model paling longgar di Go yang masih kuat ngoding + satu-satunya kandidat longgar di jalur `/chat/completions` (kompatibel profil custom jcode) |
| Eskalasi jcode (manual) | MiniMax M3 | Go | 3.200 | Untuk refaktor berat; ⚠️ di Go dilayani via `/v1/messages` (gaya Anthropic) — Hermes OK, jcode perlu verifikasi profil |
| Kompresi, cron ringan, swarm & memory sideagent jcode | **MiMo-V2.5 Free / Hy3 Free** | Zen (gratis) | — ($0) | Workhorse gratis; *model lemah tidak membaca esai — dan tidak perlu* |
| ~~Eskalasi maksimum~~ | ~~Kimi K3~~ | — | 110 | **dikeluarkan dari Opsi 2** — kuota paling ketat di Go, bertentangan dengan mandat "paling longgar" |
| ~~Muse Spark 1.2 Contributor~~ | — | — | 45.300 | **dikeluarkan** — region terbatas (kebijakan geografis Meta); tidak layak jadi pin daemon di ID |

**Satu kalimat:** Nemotron 3 Ultra Free memikul hari-hari biasa ($0), MiniMax M3 menangkap limit dan mengangkat beban berat dengan ruang napas 3,6× lebih lega, dan DeepSeek V4 Flash (7.600 req/5 jam) adalah lantai pengaman yang hampir mustahil habis.

---

## 2. Opsi 2 vs Opsi 1 — beda filosofi

| | **Opsi 1 — Quality-First** | **Opsi 2 — Throughput-First** |
|---|---|---|
| Fallback + berat (Go) | GLM-5.2 (880 req/5 jam) | **MiniMax M3 (3.200)** — 3,6× lebih longgar |
| Otak jcode | Kimi K2.7 Code (1.350) — spesialis kode terbaik | **DeepSeek V4 Flash (7.600)** — 5,6× lebih longgar, sedikit di bawah K2.7 untuk coding |
| Meriam manual | Kimi K3 (110) | tidak ada (sengaja) |
| Lantai pengaman | implisit (GLM-5.1) | eksplisit: M2.7 → V4 Flash |
| Cocok jika | mutasi core sering, kualitas kode kritis | daemon sangat aktif, Telegram ramai, swarm besar, pantang kehabisan kuota |

Rekomendasi agen: pola insiden 20 Agu (daemon ramai, fence storm, 5 thread Telegram aktif) lebih cocok **Opsi 2** untuk ketahanan harian; jika suatu masa kerja coding jcode lebih dominan daripada denyut daemon, barulah Opsi 1 lebih unggul.

## 3. Fakta kuota Go yang dipakai (docs resmi, 21 Agu)
MiniMax M3 3.200/5j · M2.7 3.400/5j · DeepSeek V4 Flash 7.600/5j · (pembanding: GLM-5.2 880 · K2.7 Code 1.350 · Kimi K3 110) — batas Go: $12/5 jam, $30/minggu, $60/bulan.

## 4. Peringatan yang tetap berlaku (tidak tawar-menawar)
1. **Privasi tier gratis**: model Zen gratis = data dipakai improve model; Nemotron Ultra (NVIDIA): *"trial use only — no personal/confidential data"*. → Data ASN/SK/bukti dukung/vault **wajib lewat Go** (zero-retention). Untungnya di Opsi 2 jalur sensitif jatuh ke model berkuota lega (M3/V4 Flash), jadi aturan ini tidak berebut kuota dengan tugas umum.
2. **Limited time**: tier gratis bisa dihapus Zen → aturan `on_free_model_removed`: jatuh ke MiniMax M3 + handoff; dilarang berburu gratis tanpa seal.
3. **Pre-flight P0** (insiden 20 Agu): turunkan fence → putus jalur injeksi → unify 5 thread Telegram → seal DECISION → baru switch.

## 5. Cuplikan konfigurasi Opsi 2

### Hermes — `~/.hermes/config.yaml`
```yaml
model:
  provider: opencode-zen
  default: nemotron-3-ultra-free          # T0 — otak utama, $0
  base_url: https://opencode.ai/zen/v1
  fallbacks:
    - provider: opencode-zen
      model: nemotron-3.5-lightning-free  # T0 cadangan, $0
    - provider: opencode-go
      model: minimax-m3                   # T1 longgar (3.200/5j) → fence core writes
    - provider: opencode-go
      model: deepseek-v4-flash            # safety net (7.600/5j)
compression:
  provider: opencode-zen
  model: mimo-v2.5-free
  sensitive: { provider: opencode-go, model: deepseek-v4-flash }
  threshold: 0.50
```

### jcode — `~/.jcode/config.toml`
```toml
[provider]
default_provider = "opencode-go"
default_model    = "deepseek-v4-flash"   # 7.600 req/5j, /chat/completions ✅

[agents]
swarm_model   = "mimo-v2.5-free"          # $0
memory_model  = "hy3-free"                # $0
```

**File pendamping:** `MODEL.policy.opsi2.proposed.yaml` · `D-NNNN-opsi2.draft.yaml`

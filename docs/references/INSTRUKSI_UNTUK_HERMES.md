# Instruksi untuk Hermes Agent — merge free-stack + 9Router ke config yang sudah ada

Bacalah seluruh file ini, lalu kerjakan. Jangan tanya ulang kecuali file `~/.hermes/config.yaml` tidak ada.

## Tujuan

Merge snippet `MERGE_INTO_CONFIG.yaml` ke `~/.hermes/config.yaml` **tanpa menimpa** pengaturan yang sudah jalan (terminal, memory, skills, cron, gateway, messaging, security, database, runtime, mcp_servers, dll.).

File sumber (satu folder dengan instruksi ini):

- `MERGE_INTO_CONFIG.yaml` — yang harus digabung
- `ENV_KEYS.env` — nama env var saja; **jangan** menulis API key ke `config.yaml`
- `9ROUTER_MODELS.md` — daftar model 9Router (referensi)

## Aturan merge (wajib)

1. Backup dulu: salin `~/.hermes/config.yaml` ke `~/.hermes/config.yaml.bak-free-stack-YYYYMMDD` (pakai tanggal hari ini).
2. Parse YAML yang ada. Jangan rewrite file dari nol.
3. Untuk kunci top-level berikut, **replace seluruh blok** dengan versi dari `MERGE_INTO_CONFIG.yaml` (ini memang stack baru):
   - `model`
   - `fallback_providers`
   - `auxiliary`
   - `model_aliases`
4. Untuk `providers:`:
   - Jika belum ada, buat dari snippet.
   - Jika sudah ada, **merge per-id**: update/tambah `groq`, `nvidia`, `gemini`, `zai`, `openrouter`, **`ninerouter`** sesuai snippet.
   - **Jangan hapus** provider lain yang sudah ada (`together`, `local`, `work`, endpoint custom user, dll.).
5. Jangan sentuh kunci lain.
6. Jangan masukkan API key ke YAML. Key hanya di `~/.hermes/.env`.
7. Pertahankan komentar user yang tidak bentrok. Komentar di snippet boleh ikut disalin pada blok yang diganti.
8. Validasi YAML setelah tulis (`python3 -c "import yaml; yaml.safe_load(open(...))"` atau parser setara). Kalau gagal, restore backup.
9. Setelah merge, cek `~/.hermes/.env`:
   - Jika `GOOGLE_API_KEY` atau `GEMINI_API_KEY` kosong/absen, **tambahkan baris placeholder** `GOOGLE_API_KEY=` (jangan isi key palsu) dan laporkan ke user bahwa otak Gemini belum hidup sampai key diisi.
   - Tambahkan placeholder yang belum ada untuk: `NVIDIA_API_KEY`, `GROQ_API_KEY`, `GLM_API_KEY`, `OPENROUTER_API_KEY`, **`NINEROUTER_API_KEY`**.
   - Jangan menimpa nilai key yang sudah terisi.
10. Jangan jalankan `hermes setup --portal` dan jangan ganti provider ke Nous kecuali user minta.

## 9Router — deteksi lalu sisipkan model (wajib dilakukan)

9Router adalah gateway lokal, bukan provider cloud. Probe **sebelum** menulis fallback.

```bash
curl -sS -m 2 -o /tmp/9r-models.json -w "%{http_code}" \
  http://127.0.0.1:20128/v1/models
```

Pakai `127.0.0.1`, bukan `localhost` (hindari IPv6).

### A. 9Router TIDAK hidup (koneksi gagal / bukan 200)

- Tetap merge `providers.ninerouter` + alias (`9r`, `kiro`, `krglm`, `9combo`, …).
- **Jangan** prepend fallback 9Router. Kalau dipaksa, setiap 429 Gemini akan nunggu timeout.
- Di laporan: 9Router off. User bisa `npm install -g 9router && 9router`, connect **Kiro** (Google/GitHub), copy API key dashboard ke `NINEROUTER_API_KEY`, lalu minta merge ulang atau `/model kiro`.

### B. 9Router HIDUP (HTTP 200)

1. Baca ID model dari `/v1/models` (field `data[].id`).
2. Pilih ID yang **benar-benar ada** di katalog live, urutan preferensi:
   1. `free-combo` (kalau user sudah buat combo di dashboard)
   2. `kr/claude-sonnet-4.5`
   3. `kr/glm-5`
   4. `kr/MiniMax-M2.5`
   5. `kr/qwen3-coder-next`
   6. `kr/deepseek-3.2`
   7. `oc/nemotron-3-ultra-free` atau `oc/` + nama yang mengandung `nemotron-3-ultra` / `hy3` / `minimax-m3`
3. **PREPEND** ke `fallback_providers` (di depan NVIDIA), maksimal **2** entri 9Router supaya rantai tidak panjang:
   - Jika `free-combo` ada: satu entri saja (`free-combo`).
   - Jika tidak: `kr/claude-sonnet-4.5` (atau kr/ terkuat yang ada), lalu `kr/glm-5` jika ada.
   Bentuk YAML (wajib `provider: custom` + `base_url` + `key_env`):

```yaml
  - provider: custom
    model: kr/claude-sonnet-4.5
    base_url: http://127.0.0.1:20128/v1
    key_env: NINEROUTER_API_KEY
  - provider: custom
    model: kr/glm-5
    base_url: http://127.0.0.1:20128/v1
    key_env: NINEROUTER_API_KEY
```

4. Sesuaikan alias yang modelnya tidak ada di katalog live: jangan hapus alias; di laporan sebutkan ID yang 404.
5. `NINEROUTER_API_KEY`: jika masih kosong, **jangan mengarang key**. Minta user copy dari dashboard 9Router. Jangan isi `9router` palsu kecuali user sudah pakai placeholder itu di tool lain dan 9Router menerima.

Jangan pakai prefix yang sudah mati (2026): `if/` (iFlow), `qw/` (Qwen Code), `gc/` (Gemini CLI).

## Hasil yang diharapkan

```yaml
model:
  provider: gemini
  default: gemini-3.7-flash
  base_url: https://generativelanguage.googleapis.com/v1beta
```

Fallback berurutan:

0. *(hanya jika 9Router hidup)* `kr/claude-sonnet-4.5` dan/atau `kr/glm-5` / `free-combo` via `http://127.0.0.1:20128/v1`
1. `nvidia` / `nvidia/nemotron-3-ultra-550b-a55b`
2. custom Groq / `openai/gpt-oss-120b`
3. `zai` / `glm-4.7-flash`
4. `openrouter` / `nvidia/nemotron-3-ultra-550b-a55b:free`
5. `opencode-free` / `nemotron-3-ultra-free`

Auxiliary (vision tetap 3.7 Flash; sisanya 3.5 Flash-Lite) sesuai snippet.

## Laporan ke user (setelah selesai)

Tulis singkat:

- path backup
- kunci yang diganti vs yang dibiarkan
- env var yang sudah terisi vs masih kosong
- status 9Router: hidup/mati, model `kr/` / `oc/` / combo yang terpasang
- langkah user:
  1. Isi key di `~/.hermes/.env` (Google wajib; NVIDIA/Groq/z.ai/OpenRouter disarankan; `NINEROUTER_API_KEY` dari dashboard jika 9Router dipakai)
  2. Session chat yang sudah terbuka tidak ikut pindah model — buka session baru, atau `/model otak`
  3. Alias Gemini/NVIDIA: `/model otak` `/model ultra` `/model groq` `/model glm` `/model orfree` `/model free`
  4. Alias 9Router: `/model kiro` `/model 9r` `/model krglm` `/model krmini` `/model krcoder` `/model oc9` `/model 9combo`
  5. Kalau Gemini 429 terus, itu normal di free tier; fallback akan jalan sendiri dalam turn itu
  6. Kalau 9Router belum jalan: `npm install -g 9router` → `9router` → Connect **Kiro** (Google/GitHub) → buat combo `free-combo` (lihat `9ROUTER_MODELS.md`)

## Kalau model ID OpenCode Free tidak ada di katalog live

Jangan gagalkan merge. Biarkan `nemotron-3-ultra-free`. Di laporan, sarankan user jalankan `hermes model` → OpenCode Free dan pilih model verified yang muncul (Nemotron 3 Ultra / Hy3 / Laguna / Ox Alpha).

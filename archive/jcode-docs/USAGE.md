# Panduan Penggunaan jcode

## Quick Start

### TUI Interaktif
```bash
jcode
```
Membuka terminal UI interaktif. Ketik perintah di prompt, agent akan bekerja.

### Run Sekali (Non-Interactive)
```bash
jcode run "buatkan REST API dengan Express.js"
```

### Resume Session
```bash
jcode --resume fox
```
Resume session berdasarkan nama yang memorable.

## Mode Operasi

### 1. TUI Mode (Default)
```bash
jcode
```
- Ketik prompt → agent bekerja
- `Shift+Enter` untuk queue send (tunggu agent selesai turn sebelum kirim)
- `Enter` untuk interleaved send (kirim secepatnya tanpa break KV cache)

### 2. Run Mode (Non-Interactive)
```bash
jcode run "jelaskan struktur project ini"
jcode run "buatkan unit test untuk src/utils.ts"
```

### 3. Server/Client Mode (Persistent)
```bash
# Jalankan sebagai background server
jcode serve

# Attach client ke server yang berjalan
jcode connect
```

### 4. Voice Input (Dictate)
```bash
jcode dictate
```
Mengirim voice input dari STT (Speech-to-Text) command yang dikonfigurasi.

---

## Fitur Aktif — Panduan Detail

### 1. Memory System (Semantic Vector)

**Status:** ON | **Sidecar:** OFF

**Cara kerja:**
1. Setiap turn/response di-embed sebagai semantic vector
2. Query graph memory via cosine similarity
3. Memory relevan otomatis di-inject ke conversation
4. Extract memory saat: semantic drift, K turns, session end
5. Auto-consolidation (reorganize, check staleness, detect conflicts)

**Cara pakai:**
- **Otomatis:** Agent otomatis recall memory yang relevan
- **Manual:** Gunakan `/skill` atau skill tool untuk aktivasi
- **Session search:** Agent bisa search session sebelumnya (RAG)

**Tuning di `~/.jcode/config.toml`:**
```toml
[features]
memory = true

[agents]
memory_sidecar_enabled = false  # Set true untuk sideagent verification
```

### 2. Swarm Mode (Multi-Agent Collaboration)

**Status:** ON | **Spawn mode:** visible

**Cara kerja:**
- Spawn 2+ agent dalam repo yang sama
- Server otomatis manage collision & conflict
- Agent A edit file → Agent B mendapat notifikasi
- Bisa DM 1 agent, broadcast, atau per-repo channel

**Cara pakai:**
- Dari dalam TUI, minta agent spawn swarm
- Agent otomatis jadi coordinator, spawned agents jadi workers
- Group, channel, completion status otomatis managed

**Tuning di `~/.jcode/config.toml`:**
```toml
[features]
swarm = true

[agents]
swarm_spawn_mode = "visible"  # "visible" atau "headless"
```

### 3. Web Search

**Status:** DuckDuckGo (aktif) | **Fallback:** Bing (perlu API key)

**Cara kerja:**
- Agent otomatis search web saat butuh info terkini
- Default engine: DuckDuckGo (gratis, no API key)
- Fallback ke Bing jika DDG gagal

**Setup Bing API (opsional):**
```bash
# Dapatkan API key di https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
# Set di shell profile:
export JCODE_BING_API_KEY="your-bing-api-key"
```

**Tuning di `~/.jcode/config.toml`:**
```toml
[websearch]
engine = "duckduckgo"
fallback_engines = ["bing"]
bing_api_key_env = "JCODE_BING_API_KEY"
bing_market = "en-US"
```

### 4. Context Compaction

**Status:** Reactive | **Lookahead:** 15 turns

**Cara kerja:**
- Auto-compress context saat mendekati limit
- Mode `reactive`: compaction berdasarkan prediksi kebutuhan
- Lookahead 15 turn ke depan untuk prediksi
- Topic shift detection untuk relevance filtering

**Tuning di `~/.jcode/config.toml`:**
```toml
[compaction]
mode = "reactive"           # "reactive" atau "proactive"
lookahead_turns = 15        # Prediksi N turn ke depan
min_turns_between_compactions = 10  # Minimal turn antar compaction
topic_shift_threshold = 0.45        # Threshold deteksi topik baru
relevance_keep_threshold = 0.65     # Threshold simpan relevance
```

### 5. Desktop Notifications

**Status:** ON | **Server:** ntfy.sh

**Cara kerja:**
- Notifikasi desktop saat agent selesai, error, atau butuh input
- Menggunakan ntfy.sh (gratis, no signup)
- Subscribe topic unik per session

**Tuning di `~/.jcode/config.toml`:**
```toml
[safety]
ntfy_server = "https://ntfy.sh"
desktop_notifications = true
```

### 6. Cross-Provider Failover

**Status:** ON | **Mode:** countdown

**Cara kerja:**
- Jika provider utama error/rate-limited, otomatis failover
- Mode `countdown`: hitung mundur sebelum failover
- `same_provider_account_failover = true`: failover ke akun lain di provider sama

**Tuning di `~/.jcode/config.toml`:**
```toml
[provider]
cross_provider_failover = "countdown"
same_provider_account_failover = true
```

### 7. Message Timestamps

**Status:** ON

Menampilkan timestamp di setiap pesan chat untuk tracking waktu.

**Tuning di `~/.jcode/config.toml`:**
```toml
[features]
message_timestamps = true
```

---

## Input Mode

| Mode | Shortcut | Deskripsi |
|------|----------|-----------|
| Interleaved | `Enter` | Kirim segera tanpa break KV cache |
| Queue send | `Shift+Enter` | Tunggu agent selesai turn, baru kirim |

## Alignment

| Mode | Shortcut | Deskripsi |
|------|----------|-----------|
| Left-aligned | Default | Mode default, kiri |
| Centered | `Alt+C` atau `/alignment` | Mode center |

## Exit

- `Ctrl+C` — interrupt agent
- `Ctrl+D` atau `/exit` — keluar dari TUI

# Riset: OpenMausBot (milind-soni/OpenMausBot)

**Tanggal:** 12 Okt 2026
**Sumber:** README, LICENSING.md, SECURITY.md, docs/cli-onboarding.md, docs/custom-engines.md,
docs/custom-mcp-servers.md, docs/decision-model.md, docs/self-hosting.md, openmausbot.com
**Status:** Riset selesai. **Tidak diinstal.** Dua jalur integrasi terverifikasi ada di mesin ini.

---

## Ringkasan

OpenMausBot = aplikasi chat desktop (Electron + React 19 + TypeScript) di mana **setiap "kontak" di
sidebar adalah agen AI sungguhan**. Konsepnya "AI as a messaging app": daftar bot, masing-masing
dengan kepribadian, model, komputer, dan aplikasi terhubung sendiri.

- **Repo:** github.com/milind-soni/OpenMausBot — 676 bintang, 114 fork, 464 commit
- **Dibuat:** 11 Agu 2026 (baru ~2 bulan)
- **Versi terkini:** 0.1.107 (10 Okt 2026) — rilis hampir harian
- **Lisensi:** Apache 2.0, **dengan carve-out** `enterprise/` (lihat bagian Lisensi)
- **Posisi:** alternatif open-source untuk Grok Bot, Meta Muse, OpenAI dots, Cue by Manus
- **Peringatan repo:** tidak ada token/kripto apa pun; tidak berafiliasi xAI/Meta/OpenAI/Manus

---

## Arsitektur

| Lapisan | Teknologi |
|---|---|
| Shell desktop | Electron (macOS, Windows, Ubuntu) |
| UI | React 19 + Vite + Tailwind |
| Harness server | Node >= 24, satu server di `127.0.0.1` |
| Data | `~/.openmausbot` — transkrip, key, event. Lokal, bukan cloud |
| Agen | CLI lokal: `claude`, `codex`, `grok` (login & langganan sendiri) |
| Komputer | Cloud Linux desktop, Local VM, atau Mac sendiri (opt-in) |
| Aplikasi | 500+ via Composio |
| Computer control | Cua Driver (`@trycua/cua-driver` 0.28.2) |

**Prinsip inti:** bring-your-own-agent, local-first. Satu harness server memiliki setiap proses agen
dan menormalkan protokol native tiap provider jadi satu event stream. Tidak ada proxy di tengah.

---

## Fitur utama

1. **Pilih otak per bot** — model picker dengan provider rail (Claude & Codex berdampingan, provider
   tidak tersedia diredupkan dengan alasannya). Ganti model mid-conversation.
2. **Setiap bot dapat komputer** — cloud desktop dengan live screen preview, "Open desktop" untuk
   mengambil alih di browser, atau arahkan ke Mac sendiri.
3. **Bot bertanya sebelum bertindak** — perintah shell, edit file, pertanyaan muncul sebagai kartu
   inline Allow / Deny / jawab. *Permission broker* mengubah tiap aksi berisiko jadi keputusan Anda.
4. **Aplikasi terhubung** — marketplace sekali klik via Composio (Gmail, Slack, GitHub, Notion, Linear).
5. **Kelola bot seperti chat** — pin, tandai belum dibaca, duplikat, sembunyikan, hapus.
6. **Key sekali, semua menyala** — kredensial tersimpan lokal, UI hanya melihat flag "configured".
   **Write-only: UI tidak pernah melihat nilainya.**
7. **Channels** — Work, Personal, tiap proyek punya transkrip, instruksi, folder kerja sendiri.
8. **Tim dari satu file Markdown** — impor playbook (BotMRR), review screen sebelum bot dibuat.
9. **Bagikan tim** — simpan seluruh tim ke satu file; riwayat chat, key, password **tidak pernah ikut**,
   dan apa pun yang tampak seperti rahasia dihapus dari teks.
10. **Bot yang menjawab balik** — ElevenLabs, Fish Audio, Grok (xAI), suara Mac bawaan, atau
    Chatterbox lokal. Mode telepon (macOS saja).
11. **Routines di kalender** — jadwal semua bot dalam satu minggu.

---

## Integrasi dengan ekosistem kita

### Hermes TERDAFTAR sebagai partner provider

Di halaman partners openmausbot.com, di bawah **Models**, tercantum:

> **Hermes — Nous Research** — hermes-agent.nousresearch.com

Hermes sejajar dengan Claude (Anthropic), Codex (OpenAI), Grok (xAI), Cursor, Kimi (Moonshot),
Droid (Factory), Antigravity (Google), OpenCode, Qwen (Alibaba), dan Pi.

Ada juga testimoni pengguna di situs mereka:

> "I did not make this, but I am a contributor and had my PR merged which was an MCP server for
> external agent orchestration. **I connect my Hermes agent to it so that all of my agents can
> communicate.**"
> — @aialchemist_dev di X

### DUA jalur integrasi — keduanya terverifikasi ADA di mesin ini

**Jalur A — ACP (paling kuat)**

```json
{
  "instances": {
    "hermes": {
      "driver": "customAcp",
      "displayName": "Hermes",
      "config": { "cli": "hermes acp" }
    }
  }
}
```

Verifikasi di mesin ini:
```
$ hermes acp --help
usage: hermes acp [-h] [--accept-hooks] [--version] [--check] [--setup] ...
Start Hermes Agent in ACP mode for editor integration (VS Code, Zed, JetBrains)

$ hermes acp --check
Hermes ACP check OK

$ hermes --version
Hermes Agent v0.21.6+207.gd60ce27 (2026.9.24) · upstream d60ce27d
```

Bukti tambahan bahwa ini protokol yang sama dengan yang diminta OpenMausBot:
```
$ grep -n "acp" ~/src/hermes-agent/pyproject.toml
pyproject.toml:415: acp = ["agent-client-protocol==0.9.0"]
pyproject.toml:560: hermes-acp = "acp_adapter.entry:main"

$ ls ~/src/hermes-agent/acp_adapter/
auth.py  server.py  events.py  tools.py  session.py  edit_approval.py
content.py  model_catalog.py  entry.py

$ grep -n "stdio" ~/src/hermes-agent/acp_adapter/entry.py
entry.py:95:  parser = argparse.ArgumentParser(prog="hermes-acp",
                                    description="Run Hermes Agent as an ACP stdio server.")
entry.py:66:  """Route all logging to stderr so stdout stays clean for ACP stdio."""

$ ls ~/src/hermes-agent/.hermes/bin/hermes-acp
/Users/zaryu/src/hermes-agent/.hermes/bin/hermes-acp
```

Jadi: dependency resmi `agent-client-protocol==0.9.0`, binary `hermes-acp` tersedia, dan stdout-nya
memang dikosongkan khusus untuk JSON-RPC ACP. **Ini protokol yang sama**, bukan kebetulan nama.

Jalur ini memberi **tool calls penuh**: bot bisa menjalankan tool Hermes, dan permission request
Hermes muncul sebagai **approval card** di chat OpenMausBot (lewat ACP `session/request_permission`).

Catatan penting dari dokumentasi: `environment` di-strip dari key provider asing
(`XAI_API_KEY`, `OPENAI_COMPAT_API_KEY`) supaya CLI custom tidak bisa menagih ke login engine lain.
Jadi Hermes akan jalan dengan konfigurasi & kredensialnya sendiri — aman.

**Jalur B — openai-compat (paling murah)**

```json
{
  "instances": {
    "9router": {
      "driver": "openai-compat",
      "displayName": "9router",
      "config": {
        "url": "http://127.0.0.1:20128/v1",
        "apiKeyEnv": "NINE_ROUTER_API_KEY",
        "model": "kr/deepseek-3.2"
      }
    }
  }
}
```

Verifikasi: `http://localhost:20128/v1/models` → **126 model** (berflapping 126↔168).

**Batasan jujur:** driver ini **tidak mendukung tool calls** — chat text + reasoning stream saja.
Bot di instance ini menjawab dan menulis, tapi **tidak bisa mengoperasikan komputer atau aplikasi
terhubung**. Untuk tool calls, pakai Jalur A.

### Composio — kita sudah punya skill-nya

`~/.hermes/skills/ecosystem/composio/` sudah ada, dan `composio` muncul 2x di `~/.hermes/config.yaml`.
OpenMausBot memakai Composio untuk marketplace aplikasinya. Jadi ada titik sambung konseptual.

---

## Keamanan — catatan yang perlu diperhatikan

Repo ini punya SECURITY.md yang serius dan **jujur soal kelemahan yang belum ditutup**. Ini bagus.

**Yang sudah benar:**
- Server hanya bind `127.0.0.1`. Mutasi publik butuh capability per-launch atau sesi terpasang.
- API key write-only melalui API (`configured` boolean keluar, nilai tidak pernah).
- Kredensial tidak lewat argv (`ps` tidak bisa melihatnya).
- Spawning tidak boleh lewat shell — `shell: true` / string-building `cmd.exe` diminta dilaporkan.
- MCP server custom: nama reserved ditolak (`computer`, `agents`, `composio`, `browser`, `phone`),
  tidak bisa menimpa tool bawaan.
- Test MCP dibatasi 8 detik, output di-cap, stderr tidak dikirim ke UI, tidak mewarisi kredensial.

**⚠️ Kelemahan yang DIAKUI BELUM DITUTUP** (kutipan SECURITY.md):

> "Known and documented, not yet closed: that caller keeps the Slack worker's guarded routes, so
> **a bot's shell can post into an existing Full-access thread, or open one while shared Full access
> is on, and get Full-access work done without a card.** A worker-only relay token is the planned fix."

Artinya: ada jalur di mana shell milik bot bisa mendapat pekerjaan tingkat Full-access **tanpa
approval card**. Ini relevan dengan Hard Rule kita soal approval gate.

**⚠️ Key disimpan plaintext.** `config.json` (mode 0600) menyimpan API key **plaintext, bukan
terenkripsi**. Sama untuk `tunnel-account.json`. Dokumentasi menyatakannya terbuka. Untuk ekosistem
kita yang punya aturan ketat soal kredensial, ini perlu diperhitungkan.

**⚠️ Kredensial di `environment` instance juga plaintext** di `config.json`.

**⚠️ Self-hosting:** "any process that can reach `127.0.0.1:8799` has full control, including the
shell your bots can use." Jangan pernah expose port itu.

---

## Lisensi — open-core dengan carve-out

- **Apache 2.0** untuk inti.
- **`enterprise/`** = source-available dengan lisensi sendiri. Boleh dibaca, dibangun, dievaluasi,
  dijalankan bebas untuk development/test. **Produksi butuh license key.** Hosting untuk pihak ketiga
  atau white-labelling butuh perjanjian partner.
- Hapus folder `enterprise/` → yang tersisa adalah edisi open-source (`{"edition":"oss"}`).
- **Trademark:** nama OpenMausBot/MausBot dan maskot adalah trademark Supamaus Software Private
  Limited. Apache 2.0 pasal 6 tidak memberi hak trademark — produk yang dibangun di atasnya butuh
  nama sendiri.

Untuk keperluan kita (evaluasi pribadi, bukan produk turunan), carve-out ini tidak menghalangi.

---

## Persyaratan di mesin ini

| Kebutuhan | Status di mesin kita |
|---|---|
| Node >= 24 | ✅ v24.21.0 |
| CLI agent (`claude` / `codex` / `grok`) | ❌ tidak ada satu pun |
| OpenMausBot terpasang | ❌ belum |
| macOS Apple silicon / Intel | ✅ MacBookPro16,2 (Intel) — ada build Intel |
| Hermes ACP | ✅ `hermes acp --check` → OK |
| 9router OpenAI-compatible | ✅ 126 model |

**Hambatan utama:** tidak ada CLI `claude`/`codex`/`grok`. Tanpa itu, bot tidak punya "otak" bawaan.

**Tapi** jalur `customAcp` dengan `hermes acp` dan jalur `openai-compat` dengan 9router **tidak
butuh CLI tersebut** — keduanya memakai yang sudah kita punya.

---

## Penilaian

### Yang menarik

1. **Hermes diakui sebagai partner provider** — kita bukan warga kelas dua di ekosistem ini.
2. **Jalur ACP memungkinkan Hermes jadi engine** OpenMausBot, lengkap dengan tool calls dan
   approval card. Ini integrasi dua arah yang nyata, bukan sekadar klaim.
3. **Konsep "AI as messaging app"** dekat dengan yang sudah kita lakukan (Telegram + 10 thread +
   `channel_overrides`). Bedanya: mereka desktop GUI, kita chat platform.
4. **Local-first + bring-your-own-agent** selaras dengan filosofi ekosistem kita.
5. **Tim dari satu file Markdown** — mirip skill bank kita, tapi untuk roster bot.
6. **Aktif sekali** — 464 commit dalam 2 bulan, rilis harian, 37 issue terbuka.

### Yang perlu dipertimbangkan serius

1. **Kelemahan approval yang diakui belum ditutup** — shell bot bisa dapat Full-access tanpa kartu.
   Ini bertabrakan langsung dengan Hard Rule 1 kita (approval gate).
2. **Key plaintext** — bertabrakan dengan aturan kredensial kita.
3. **Belum matang** — repo berumur 2 bulan, README sendiri bilang "Early but real".
4. **Overlap fungsional** — kita sudah punya Telegram + 10 thread + cron + A2A + skill bank.
   OpenMausBot menambah GUI desktop, tapi bukan kapabilitas yang belum kita miliki.
5. **Dependensi Node 24 + Electron** — menambah permukaan pemeliharaan di mesin yang sudah padat.

### Rekomendasi

**Pelajari, jangan pasang dulu.** Alasannya:

- Nilai uniknya (GUI desktop untuk tim agen) bukan kebutuhan yang saat ini belum terpenuhi.
- Dua kelemahan keamanannya (approval bypass, key plaintext) menyentuh langsung aturan keras kita.
- Umurnya 2 bulan; menunggu 1-2 bulan lagi memberi gambaran stabilitas yang lebih jelas.

**Kalau nanti mau dicoba**, urutan paling aman:
1. `npx openmausbot --local` (tanpa install global, tanpa akses remote)
2. Konfigurasi `customAcp` → `hermes acp` di `~/.openmausbot/config.json`
3. Jangan hubungkan Composio atau komputer cloud sampai keamanan approval-nya jelas
4. Jangan pernah expose port harness

**Yang layak ditiru tanpa memasang apa pun:** pola mereka bagus di beberapa hal —
*permission broker* sebagai lapisan consent terpisah, key write-only (UI hanya lihat flag
"configured"), dan SECURITY.md yang jujur menyebut kelemahan yang belum ditutup. Yang terakhir itu
standar dokumentasi keamanan yang bagus dan bisa kita adopsi.

---

## Sumber

- Repo: https://github.com/milind-soni/OpenMausBot
- Situs: https://www.openmausbot.com/
- Lisensi: https://github.com/milind-soni/OpenMausBot/blob/main/LICENSING.md
- Keamanan: https://github.com/milind-soni/OpenMausBot/blob/main/SECURITY.md
- Custom engines: https://github.com/milind-soni/OpenMausBot/blob/main/docs/custom-engines.md
- Custom MCP: https://github.com/milind-soni/OpenMausBot/blob/main/docs/custom-mcp-servers.md
- Decision model: https://github.com/milind-soni/OpenMausBot/blob/main/docs/decision-model.md
- Self-hosting: https://github.com/milind-soni/OpenMausBot/blob/main/docs/self-hosting.md
- CLI onboarding: https://github.com/milind-soni/OpenMausBot/blob/main/docs/cli-onboarding.md

# OpenMausBot — Status Instalasi & Rencana Integrasi

**Tanggal:** 12 Okt 2026
**Status:** Terpasang & berjalan, terisolasi dari ekosistem (sesuai kata pemilik). **Belum ada integrasi.**
**Sifat dokumen:** Audit read-only + rencana. Tidak ada perubahan yang dilakukan.

Lanjutan dari `docs/reports/RISET-OPENMAUSBOT-2026-10-12.md` (riset awal).

---

## 1. Status instalasi (terverifikasi)

| Item | Nilai | Bukti |
|---|---|---|
| Versi | **0.1.107** | `defaults read .../Info.plist CFBundleShortVersionString` |
| Lokasi | `/Applications/OpenMausBot.app` | `ls -d` |
| Harness | `127.0.0.1:8799` (LISTEN) | `lsof -nP -iTCP -sTCP:LISTEN` |
| Proses | Jalan (main + helper GPU/renderer/network/node) | `ps aux` |
| Data | `~/.openmausbot/` | 25 entri |
| Profil | nama **Niumination**, `archk4li@gmail.com` | `config.json` |
| Onboarding | selesai `2026-10-12T13:35:24Z` | `config.json` |
| Bot | **1** — nama `gila` | `bots.json` |
| Engine bot | `opencodeGo` / model `opencode/big-pickle` | `bots.json` |
| Aktivitas | 3 turn, input 215.887 token, cached 155.008 | `bots.json` |

**Bind loopback saja — benar.** Harness hanya di `127.0.0.1:8799`, tidak terekspos ke LAN. Sesuai
peringatan dokumentasi mereka ("never bind it to a public interface").

**Kredensial aman di mode desktop.** `config.json` hanya berisi `profile` + `onboarding` — **tidak ada
key sama sekali**. Key disimpan di `~/Library/Application Support/openmausbot/credentials.bin`
(encrypted store OS), persis seperti yang dijanjikan dokumentasi. Ini lebih baik dari yang saya
khawatirkan di laporan riset awal (yang memperingatkan key plaintext — itu berlaku untuk mode
server/CLI, bukan desktop).

**Engine bawaan yang dikenali:** `claude`, `claudeApi`, `codex`, `cursor`, `droid`, `grok`, `kimi`,
`opencodeGo`.

**Hermes TIDAK ada di daftar engine bawaan** — tidak ada `hermes.json` di `providers/engine-models/`.
Jadi walaupun Hermes terdaftar sebagai partner di situs mereka, integrasinya **manual** lewat
`customAcp`. Ini penting: tidak ada tombol "Install Hermes" seperti Claude Code.

### CLI agent di mesin ini

| CLI | Status |
|---|---|
| `opencode` | ✅ `/usr/local/bin/opencode` |
| `qwen` | ✅ `/usr/local/bin/qwen` |
| `hermes` | ✅ `/Users/zaryu/src/hermes-agent/.hermes/bin/hermes` |
| `claude`, `codex`, `grok`, `cursor`, `droid`, `kimi` | ❌ tidak ada |

Bot `gila` memakai `opencodeGo` — masuk akal, karena `opencode` memang satu-satunya CLI agent
"asing" yang terpasang. Sisanya tidak ada, jadi engine bawaan lain tidak bisa dipakai.

---

## 2. ⚠️ Temuan keamanan paling penting

### `hermes acp` memuat konfigurasi produksi yang sama

Diverifikasi dengan membaca kode Hermes:

```
$ sed -n '82,88p' ~/src/hermes-agent/acp_adapter/entry.py
def _load_env() -> None:
    """Load .env from HERMES_HOME (default ``~/.hermes``)."""
    hermes_home = get_hermes_home()
    loaded = load_hermes_dotenv(hermes_home=hermes_home)

$ grep -n "load_config" ~/src/hermes-agent/acp_adapter/server.py
server.py:331:        cfg = load_config()
```

Artinya, kalau `hermes acp` di-wire ke OpenMausBot **tanpa isolasi**, maka bot OpenMausBot
mendapat akses ke:

| Yang terbuka | Isi |
|---|---|
| **Skill bank** | **238 skill, 1.178 file** — seluruh pengetahuan operasional Niumination |
| **MCP servers** | `filesystem`, `github`, `context7`, `composio` |
| **Providers** | `9router`, `huancheng`, `atria` (beserta kredensialnya) |
| **Hook approval** | Bisa dimatikan dengan `--accept-hooks` (auto-approve) |

Ini bukan kebocoran teknis — ini memang cara Hermes bekerja. Tapi konsekuensinya: **bot OpenMausBot
akan menjadi Hermes yang setara dengan agen produksi kita**, termasuk akses ke repo GitHub dan
filesystem.

Dikombinasikan dengan kelemahan yang OpenMausBot sendiri akui belum ditutup:

> *"...a bot's shell can post into an existing Full-access thread, or open one while shared Full
> access is on, and get Full-access work done without a card."*

...maka wiring tanpa isolasi berarti: **shell bot OpenMausBot bisa mendapat pekerjaan Full-access
tanpa approval card, sambil memegang akses skill bank + GitHub + filesystem kita.**

### ✅ Isolasi MUNGKIN — dan sudah saya buktikan

`get_hermes_home()` menghormati `HERMES_HOME`. Diuji dengan interpreter venv Hermes yang benar:

```
$ env -u HERMES_HOME $VENV -c "...get_hermes_home()"
  -> /Users/zaryu/.hermes                      # default

$ HERMES_HOME=/tmp/omb-isolation-test $VENV -c "...get_hermes_home()"
  -> /tmp/omb-isolation-test                   # dialihkan
```

Jadi Hermes bisa diberi "rumah" terpisah khusus untuk OpenMausBot, tanpa skill bank dan tanpa MCP
produksi.

### ⚠️ Tapi isolasi naif MENGGANTUNG

Percobaan mengarahkan `HERMES_HOME` ke direktori **kosong** gagal:

```
$ HERMES_HOME=/tmp/omb-home-test hermes-acp --help
hermes: no dependency environment is committed for this install; run `hermes pm repair`

$ HERMES_HOME=/tmp/omb-home-test hermes-acp --check
(kosong — menggantung, timeout 180s)
```

**Jangan arahkan `HERMES_HOME` ke direktori kosong.** Hermes mencoba bootstrap dan menggantung,
bukan gagal cepat. Isolasi harus berupa Hermes home yang benar-benar ter-provision
(`hermes pm repair` atau instalasi terpisah), bukan sekadar direktori baru.

---

## 3. Dua jalur integrasi

### Jalur A — ACP (`customAcp`) — tool calls penuh

**Cara:** tambahkan entry di `~/.openmausbot/config.json`:

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

**Yang didapat:** tool calls penuh, dan permission request Hermes muncul sebagai **approval card**
di chat OpenMausBot lewat ACP `session/request_permission`.

**Bukti approval card benar-benar ada** (dibaca dari kode Hermes):

```
$ grep -nE "request_permission|approval" ~/src/hermes-agent/acp_adapter/edit_approval.py
1:   """Pre-execution ACP edit approval helpers.
176: def maybe_require_edit_approval(tool_name, arguments) -> str | None:
180:     ``None`` so dispatch can continue. Requester exceptions deny by default.
```

`deny by default` saat requester error — perilaku yang benar.

**⚠️ Jangan pakai `--accept-hooks`.** Flag itu (dan `HERMES_ACCEPT_HOOKS=1`) auto-approve shell hook
tanpa prompt. Bertabrakan langsung dengan Hard Rule 1.

### Jalur B — `openai-compat` (9router) — chat saja

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

**Verifikasi:** `curl http://localhost:20128/v1/models` → **126 model** (berflapping 126↔168).

**Batasan:** driver ini **tidak mendukung tool calls** — chat text + reasoning stream saja. Bot
menjawab dan menulis, tapi tidak bisa mengoperasikan komputer atau aplikasi terhubung.

**Nilai:** ini jalur paling aman untuk mencoba OpenMausBot, karena tidak membuka skill bank, MCP,
atau filesystem sama sekali. Bot hanya jadi "pintu masuk" ke model 9router.

---

## 4. Yang sudah benar (tidak perlu diubah)

1. **Bind loopback** — harness tidak terekspos.
2. **Key di encrypted store** — `config.json` bersih dari kredensial.
3. **Terpisah dari ekosistem** — belum ada `instances`, `mcpServers`, atau `decider` di config.
   Tidak ada skill bank, MCP, atau provider kita yang terekspos.
4. **Tidak ada Composio terhubung** — belum ada aplikasi pihak ketiga yang diberi akses.
5. **Tidak ada komputer cloud diaktifkan.**

Instalasi saat ini **netral** — tidak ada risiko yang mengalir ke ekosistem.

---

## 5. Rekomendasi bertahap

### Tahap 0 — biarkan seperti sekarang (aman)
Tidak ada yang perlu dikerjakan. Instalasi netral, tidak menyentuh ekosistem.

### Tahap 1 — kalau ingin mencoba: pakai Jalur B dulu
`openai-compat` → 9router. Tanpa tool calls, jadi **tidak ada** akses skill bank/MCP/filesystem.
Bot jadi klien model saja. Ini memberi rasa bagaimana OpenMausBot bekerja tanpa membuka apa pun.

### Tahap 2 — kalau Jalur B memuaskan: pertimbangkan ACP **dengan isolasi**
Syarat wajib sebelum wiring `hermes acp`:
1. Provision Hermes home terpisah yang benar (bukan direktori kosong — akan menggantung)
2. Home itu **tanpa** MCP `github`/`filesystem`/`composio`
3. Home itu **tanpa** skill bank produksi (atau hanya subset aman)
4. **Tanpa** `--accept-hooks`
5. Uji dengan tugas yang tidak destruktif dulu, perhatikan apakah approval card muncul

### Yang JANGAN dilakukan
- ❌ Wiring `hermes acp` dengan `HERMES_HOME` default — membuka 238 skill + GitHub + filesystem
- ❌ `--accept-hooks` — mematikan approval gate
- ❌ Menghubungkan Composio sebelum kelemahan approval mereka jelas
- ❌ Mengekspos port 8799 ke LAN/publik
- ❌ Mengarahkan `HERMES_HOME` ke direktori kosong (menggantung)

---

## 6. Catatan insiden kecil saat audit

Saat menjalankan uji isolasi, `curl` ke 9router sempat mengembalikan `HTTP 000` (timeout). Setelah
diperiksa ulang: **9router sehat (`HTTP 200`, listener PID 1187) dan gateway Hermes sehat
(PID 5350, jalan 1j34m)**. Penyebabnya beban sesaat dari proses uji saya sendiri yang menggantung.

Proses uji sudah dibersihkan (`pkill`, `rm -rf /tmp/omb-*`). Tidak ada kerusakan. Dicatat karena
output `000` sempat muncul di transkrip.

---

## 7. Sumber

- Kode Hermes: `~/src/hermes-agent/acp_adapter/{entry,server,edit_approval}.py`
- Config Hermes: `~/.hermes/config.yaml`
- Data OpenMausBot: `~/.openmausbot/{config.json,bots.json}`
- Dok OpenMausBot: `docs/custom-engines.md`, `docs/custom-mcp-servers.md`, `SECURITY.md`
- Riset awal: `docs/reports/RISET-OPENMAUSBOT-2026-10-12.md`

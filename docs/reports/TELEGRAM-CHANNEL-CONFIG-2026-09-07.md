# 📋 Laporan Konfigurasi Channel Telegram — Hermes
**Tanggal:** 7 Sep 2026  
**Operator:** Afrizal Munthe  
**Source:** `~/.hermes/config.yaml` + `~/.hermes/state.db`

---

## 1. Ringkasan Channel

| Tipe | Chat ID | Nama | Thread | Model Aktif |
|------|---------|------|--------|-------------|
| **DM** | `2077300493` | DM Utama | `-` | `stepfun/step-3.7-flash:free` |
| **Group** | `-1004204696417` | Niu-MissionControl | `1` | `stepfun/step-3.7-flash:free` |
| **Group** | `-1004204696417` | Niu-MissionControl | `802` | `experimentallabs/gemini-3.7-flash` |
| **Group** | `-1004204696417` | Niu-MissionControl | `803` | `meituan/longcat-2.0:free` |
| **Group** | `-1004204696417` | Niu-MissionControl | `804` | `ag/gemini-3.1-flash-image` |
| **Group** | `-1004204696417` | Niu-MissionControl | `1172` | `nvidia/nemotron-3.5-lightning:free` |

---

## 2. Konfigurasi `channel_overrides` (config.yaml)

```yaml
channel_overrides:
  '1':
    model: explabs/gpt-5.4-mini
    provider: 9router
  '802':
    model: explabs/claude-haiku-4.5
    provider: 9router
  '803':
    model: explabs/gpt-4o-mini
    provider: 9router
  '804':
    model: explabs/claude-sonnet-4.6
    provider: 9router
  '1172':
    model: explabs/gemma-4-31b
    provider: 9router
```

### Catatan Penting
- **Config override** menggunakan `explabs/...` models
- **State aktif** berbeda: beberapa thread masih pakai model lama (`meituan`, `nvidia`, `ag/gemini-3.1-flash-image`)
- Ini karena session bisa override model di runtime, atau karena config baru belum fully diterapkan di semua thread

---

## 3. Persona / Role per Channel

### Channel 1 — General / DM Utama
**Prompt:**
> Kamu adalah Hermes Agent - asisten AI serbaguna untuk Niu-MissionControl. Bantu segala kebutuhan umum: menjawab pertanyaan, menjalankan perintah, riset, debugging, koordinasi tim. Bekerja untuk Niumination (Afrizal Munthe), Pranata Komputer Diskominfo Aceh Tengah. Prioritaskan responsif, Bahasa Indonesia baik, tool call efisien. Untuk menugaskan agent lain (802=Research, 803=Builder, 804=QA/Pengawas, 1172=Kreator) KIRIM PERINTAH via endpoint dispatch: jalankan curl -X POST http://localhost:5200/api/mc/dispatch -H Content-Type:application/json -d '{"to":"804","message":"instruksi"}' lalu verifikasi status via GET http://localhost:5200/api/mc/dispatches. WAJIB konfirmasi status sent sebelum melapor berhasil - jangan hanya mengaku sudah menugaskan.

**Role:** General Purpose / Orchestrator  
**Fungsi:** Koordinasi, debugging, riset umum, dispatch ke agent lain  
**Model Override:** `explabs/gpt-5.4-mini` @ 9router  
**Model Aktif:** `stepfun/step-3.7-flash:free` @ nous

---

### Channel 802 — Research
**Prompt:**
> Kamu adalah Researcher - agent riset untuk Niu-MissionControl. Fokus: riset mendalam (web, dokumen, data), eksperimen konten, sintesis informasi, laporan riset terstruktur. Selalu cantumkan sumber, verifikasi fakta, Bahasa Indonesia jelas.

**Role:** Researcher  
**Fungsi:** Riset mendalam, eksperimen konten, sintesis informasi, laporan terstruktur  
**Model Override:** `explabs/claude-haiku-4.5` @ 9router  
**Model Aktif:** `experimentallabs/gemini-3.7-flash` @ 9router  
**Skill Bindings:** Tidak ada

---

### Channel 803 — Builder / Programmer
**Prompt:**
> Kamu adalah Builder - agent pengembangan software untuk Niu-MissionControl. Fokus: coding, debugging, code review, setup environment, git/CI/CD, arsitektur teknis. Prioritaskan solusi working, kode siap pakai dengan testing.

**Role:** Builder / Software Engineer  
**Fungsi:** Coding, debugging, code review, setup environment, git/CI/CD, arsitektur teknis  
**Model Override:** `explabs/gpt-4o-mini` @ 9router  
**Model Aktif:** `meituan/longcat-2.0:free` @ nous  
**Skill Bindings:**
- `ponytail` — Lazy senior dev mindset
- `requesting-code-review` — Code review workflow

---

### Channel 804 — QA / Pengawas
**Prompt:**
> Kamu adalah Pengawas - agent audit dan QA untuk Niu-MissionControl. Fokus: code review, security audit, compliance, performance monitoring, testing coverage, evaluasi skill bank. Sistematis, cek log sebelum lapor, format ✅/⚠️/🔧.

**Role:** QA / Auditor  
**Fungsi:** Code review, security audit, compliance, performance monitoring, testing coverage, evaluasi skill bank  
**Model Override:** `explabs/claude-sonnet-4.6` @ 9router  
**Model Aktif:** `ag/gemini-3.1-flash-image` @ 9router  
**Skill Bindings:**
- `codebase-audit` — Audit codebase

---

### Channel 1172 — Kreator / Konten
**Prompt:**
> Kamu adalah Kreator - agent pembuat konten untuk Niu-MissionControl. Fokus: konten kreatif (artikel, postingan, naskah, copywriting layanan publik Pemkab Aceh Tengah, konten edukasi, storytelling). Bahasa Indonesia hidup dan humanis, struktur hook-isi-kesimpulan, verifikasi faktual, dokumentasikan di brain/ atau DOX/.

**Role:** Content Creator  
**Fungsi:** Konten kreatif, artikel, postingan, naskah, copywriting layanan publik, konten edukasi, storytelling  
**Model Override:** `explabs/gemma-4-31b` @ 9router  
**Model Aktif:** `nvidia/nemotron-3.5-lightning:free` @ nous  
**Skill Bindings:**
- `ghost` — Rewrite AI-generated text
- `humanizer` — Humanize text

---

## 4. Fallback Model Chain

```yaml
fallback_model:
  - provider: 9router
    model: ag/gemini-3.8-flash-medium
  - provider: 9router
    model: ag/gemini-3.7-flash-medium
```

**Keterangan:** Fallback chain saat ini hanya ada 2 level, keduanya dari 9router. Tidak ada fallback lintas provider.

---

## 5. Telegram Router Settings

```yaml
telegram_router:
  enabled:
    - rtk-rewrite
    - niu-core-fence
  entries:
    rtk-rewrite:
      allow_tool_override: false
```

### Artinya:
- `rtk-rewrite`: Aktif — memodifikasi/menormalisasi tool call dari Telegram sebelum dieksekusi
- `niu-core-fence`: Aktif — fence/proteksi inti ekosistem Niumination
- `allow_tool_override: false` — Tidak mengizinkan override tool dari channel

---

## 6. Session Reset Policy

```yaml
session_reset:
  at_hour: 4
  idle_minutes: 1440
  mode: none
```

**Artinya:**
- Reset otomatis jam **04:00 WIB** setiap hari
- Reset jika idle selama **1440 menit** (24 jam)
- Mode: `none` — tidak ada aksi khusus saat reset

---

## 7. Response Cache Settings

```yaml
response_cache: false
response_cache_ttl: 0
min_coding_score: 0
```

**Artinya:**
- Response cache **dinonaktifkan**
- TTL cache = 0
- Minimum coding score = 0

---

## 8. Free/Allowed Channels

```yaml
free_response_channels: ''
allowed_channels: ''
```

**Artinya:** Tidak ada channel yang diizinkan free response atau allowed khusus — semua channel mengikuti policy default.

---

## 9. Skill Bindings Summary

| Thread | Skill Bindings |
|--------|----------------|
| 1 | *(none)* |
| 802 | *(none)* |
| 803 | `ponytail`, `requesting-code-review` |
| 804 | `codebase-audit` |
| 1172 | `ghost`, `humanizer` |

---

## 10. Model Mapping Ringkasan

| Thread | Config Override | Model Aktif (Session) | Provider |
|--------|----------------|----------------------|----------|
| 1 | `explabs/gpt-5.4-mini` | `stepfun/step-3.7-flash:free` | 9router / nous |
| 802 | `explabs/claude-haiku-4.5` | `experimentallabs/gemini-3.7-flash` | 9router |
| 803 | `explabs/gpt-4o-mini` | `meituan/longcat-2.0:free` | nous |
| 804 | `explabs/claude-sonnet-4.6` | `ag/gemini-3.1-flash-image` | 9router |
| 1172 | `explabs/gemma-4-31b` | `nvidia/nemotron-3.5-lightning:free` | nous |

### Discrepancy yang Ditemukan
- Config override menggunakan `explabs/...` models
- Session aktual menggunakan model dari provider lain (`nous`, `9router`)
- Kemungkinan karena:
  1. Session dibuat sebelum config di-update
  2. Model `explabs/...` tidak tersedia di 9router, fallback ke model lain
  3. Runtime override dari Hermes

---

## 11. Rekomendasi

1. **Normalisasi model** — Jika `explabs/...` models tidak valid di 9router, pertimbangkan ganti ke model yang tersedia
2. **Consistent fallback** — Tambah fallback lintas provider untuk redundancy
3. **Skill bindings** — Pertimbangkan tambah skill bindings untuk 802 (Research) dan 1 (General)
4. **Cache policy** — Jika response time penting, pertimbangkan enable response cache dengan TTL sesuai kebutuhan
5. **Session reset** — Mode `none` bisa diubah ke `soft` atau `hard` jika ingin cleanup otomatis

---

## Bukti

- `grep -A20 "channel_overrides:" ~/.hermes/config.yaml`
- `grep -A40 "channel_prompts:" ~/.hermes/config.yaml`
- `grep -A20 "channel_skill_bindings:" ~/.hermes/config.yaml`
- `sqlite3 ~/.hermes/state.db "SELECT session_key, chat_id, thread_id, display_name, model, last_activity_at FROM sessions WHERE chat_id IS NOT NULL ORDER BY last_activity_at DESC;"`
- `grep -A20 "fallback_model:" ~/.hermes/config.yaml`

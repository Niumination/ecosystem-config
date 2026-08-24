# 📜 Amandemen Otoritas Model — untuk diterapkan & disahkan zaryu

> **Tanggal:** 2026-08-21 · **Keputusan:** D-0004 (draft, menggantikan D-0003 draft & merevisi D-0002)
> **Kenapa dokumen ini ada:** 4 file di bawah berstatus **TERSEGEEL / BEKU** (`core/FREEZE.list` + Hukum 4). Agen **dilarang** mengeditnya — hanya manusia `zaryu`. Dokumen ini menyiapkan teks final (before → after) agar Anda tinggal tempel. File **lain** yang tidak beku sudah dieksekusi (runtime `niu_corelib.py`, `STATE.yaml`, `AGENTS.md`, `TELEGRAM-UNIFY.md`, `INCIDENT.md`, `README.md`, skill governance).
>
> **Perubahan inti (D-0004 — scope otak):**
> 1. Otak diizinkan = **free tier `opencode-zen`** (`big-pickle` + `nemotron-3-ultra-free` + `hy3-free` + semua `*-free`) **+ free tier Nous Portal** (OAuth2 Hermes, id `nous`: semua `:free` yang ter-update saat ini). big-pickle **dipulihkan** (D-0002 dicabut untuk free tier).
> 2. Switch **sesama provider** (zen↔zen / nous↔nous) = bebas lanjut tanpa fence. **Lintas provider** (zen↔nous) atau model asing = fence + HANDOFF.
> 3. **Rem anti-waste TETAP:** `on_rate_limit.after_switch: fence_core_writes` — saat kuota free habis (semua `*-free`/`:free` 429), berhenti + HANDOFF, jangan hop antar model dalam 1 provider (berbagi 1 kuota).

---

## File 1 — `core/CONSTITUTION.md`

### Hukum 2 — SEBELUM

```markdown
2. **Hanya dua model boleh berpikir.** `opencode-zen/nemotron-3-ultra-free` dan `opencode-zen/hy3-free`. Model lain (9router, juan, huancheng, gemini, gemma, zai, gratislonggar, cf/*) **bukan otak**. Jika kamu bukan salah satu dari dua itu: BERHENTI menulis, tulis handoff, tunggu manusia.
```

### Hukum 2 — SESUDAH

```markdown
2. **Hanya free tier yang diizinkan boleh berpikir.** OpenCode Zen (`big-pickle`, `nemotron-3-ultra-free`, `hy3-free`, dan semua model `*-free`) serta Nous Portal (model `:free` yang ter-update saat ini). Model lain (9router, juan, huancheng, gemini, gemma, zai, gratislonggar, cf/*, model berbayar) **bukan otak**. Jika kamu bukan salah satunya: BERHENTI menulis, tulis handoff, tunggu manusia.
```

### Hukum 3 — SEBELUM

```markdown
3. **Ganti model = ganti dunia.** Jangan lanjut tugas seolah tidak terjadi apa-apa. Tulis `core/runtime/HANDOFF.md`. Jangan ubah file core sampai manusia atau skrip menurunkan fence.
```

### Hukum 3 — SESUDAH

```markdown
3. **Ganti model dalam provider yang sama ≠ ganti dunia** — bebas lanjut. **Ganti lintas provider (zen↔nous) atau ke model asing = ganti dunia:** tulis `core/runtime/HANDOFF.md`, jangan lanjut tugas, jangan ubah file core sampai manusia menurunkan fence.
```

> Disarankan bump `Versi: 2.0` → `2.1`.

---

## File 2 — `core/MODEL.policy.yaml`

### 2a. `allowed:` — SEBELUM

```yaml
allowed:
  - id: opencode-zen/nemotron-3-ultra-free
    provider: opencode-zen
    model: nemotron-3-ultra-free
    role: primary
    notes: free tier Zen; ID di opencode: opencode/nemotron-3-ultra-free
  - id: opencode-zen/hy3-free
    provider: opencode-zen
    model: hy3-free
    role: same-family-alternate
    notes: free tier Zen; ID di opencode: opencode/hy3-free
```

### 2a. `allowed:` — SESUDAH

```yaml
allowed:
  - provider: opencode-zen
    role: primary
    models: [big-pickle, nemotron-3-ultra-free, hy3-free]
    note: free tier Zen; + semua model berakhiran *-free (prinsip, self-update)
  - provider: nous
    role: same-tier-alternate
    note: OAuth2 Hermes (hermes auth); model free = berakhiran :free (katalog live di model_catalog.json -> providers.nous)
```

### 2b. `retired:` — SEBELUM

```yaml
retired:
  - opencode-zen/big-pickle
  - opencode-zen/deepseek-v4-flash-free
```

### 2b. `retired:` — SESUDAH

```yaml
retired: []   # D-0004 memulihkan big-pickle + seluruh free tier Zen (termasuk deepseek-v4-flash-free)
```

### 2c. `forbidden_thinkers:` — SEBELUM

```yaml
forbidden_thinkers:
  - juan-router/agnes-2.0-flash
  - 9router/cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b
  - 9router/gratislonggar
  - 9router/gemini/gemini-3.x
  - 9router/gc/gemini-2.5-pro
  - 9router/gemini/gemma-4
  - 9router/cf/@cf/zai-org
  - huancheng/DeepSeek-V4-Flash
  - agentrouter/*
  - tencent/hy3:free
  - opencode-zen/big-pickle
  - opencode-zen/deepseek-v4-flash-free
```

### 2c. `forbidden_thinkers:` — SESUDAH (hapus 2 baris terakhir)

```yaml
forbidden_thinkers:
  - juan-router/agnes-2.0-flash
  - 9router/cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b
  - 9router/gratislonggar
  - 9router/gemini/gemini-3.x
  - 9router/gc/gemini-2.5-pro
  - 9router/gemini/gemma-4
  - 9router/cf/@cf/zai-org
  - huancheng/DeepSeek-V4-Flash
  - agentrouter/*
  - tencent/hy3:free
```

### 2d. `on_rate_limit:` — SEBELUM

```yaml
on_rate_limit:
  action: same-family-or-halt
  same_family_fallback:
    - provider: opencode-zen
      model: hy3-free
  after_switch: fence_core_writes
```

### 2d. `on_rate_limit:` — SESUDAH

```yaml
on_rate_limit:
  action: same-provider-or-halt
  same_provider_fallback:
    - provider: opencode-zen
      model: nemotron-3-ultra-free
    - provider: opencode-zen
      model: hy3-free
  after_switch: fence_core_writes   # TETAP (anti-waste) — jangan dilonggarkan
```

---

## File 3 — `core/AGENTS.slim.md`

### SEBELUM

```markdown
## Otak yang diizinkan

`opencode-zen/nemotron-3-ultra-free` · `opencode-zen/hy3-free`
Selain itu: berhenti, tulis `core/runtime/HANDOFF.md`, jangan mutasi.

## Jika ganti model

1. Tulis handoff  
2. Jangan lanjut tugas yang sama  
3. Tunggu fence turun  
```

### SESUDAH

```markdown
## Otak yang diizinkan

OpenCode Zen free tier: `big-pickle` · `nemotron-3-ultra-free` · `hy3-free` + semua `*-free`.
Nous Portal free tier: semua `:free` (OAuth2 Hermes).
Selain itu: berhenti, tulis `core/runtime/HANDOFF.md`, jangan mutasi.

## Jika ganti model

- Sesama provider (zen↔zen / nous↔nous): bebas lanjut, tanpa fence.
- Lintas provider (zen↔nous) atau ke model asing: berhenti, tulis `core/runtime/HANDOFF.md`, tunggu manusia.
```

---

## File 4 — `core/VISION.md`

### SEBELUM (Misi #3)

```markdown
3. **Bekerja jujur dengan model yang ada** — free tier OpenCode Zen (`big-pickle`, `deepseek-v4-flash-free`). Tidak berpura-pura punya model kuat. Tidak membiarkan ganti model merusak inti.
```

### SESUDAH

```markdown
3. **Bekerja jujur dengan model yang ada** — free tier OpenCode Zen (`big-pickle`, `nemotron-3-ultra-free`, `hy3-free`, `*-free`) dan free tier Nous Portal (`:free`). Tidak berpura-pura punya model kuat. Tidak membiarkan ganti model merusak inti.
```

---

## Checklist pengesahan (zaryu)

- [ ] Terapkan File 1 (Hukum 2 & 3) di `core/CONSTITUTION.md` (opsional: bump Versi → 2.1)
- [ ] Terapkan File 2 (allowed / retired / forbidden / on_rate_limit) di `core/MODEL.policy.yaml`
- [ ] Terapkan File 3 di `core/AGENTS.slim.md`
- [ ] Terapkan File 4 (Misi #3) di `core/VISION.md`
- [ ] Seal `core/ledger/decisions/D-0004.yaml` (ubah `status: draft` → `sealed`); D-0003 dibiarkan superseded (draft)
- [ ] **Verifikasi Nous Portal:** `hermes auth status` + cek `model_catalog.json` → `providers.nous` (daftar model `:free` live). Catat hasilnya ke `core/STATE.yaml` `unknowns`.
- [ ] (Opsional) Re-pin cron `c6ec80ed633f` di mesin zaryu → `opencode-zen/nemotron-3-ultra-free`

> Setelah seal, runtime `scripts/niu_corelib.py` sudah sinkron (free tier zen + nous, same-provider tanpa fence, cross-provider fence) — tidak perlu aksi tambahan di kode.

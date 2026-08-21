# 📜 Amandemen Otoritas Model — untuk diterapkan & disahkan zaryu

> **Tanggal:** 2026-08-21 · **Keputusan:** D-0003 (draft, menunggu seal)
> **Kenapa dokumen ini ada:** 4 file di bawah berstatus **TERSEGEEL / BEKU** (`core/FREEZE.list` + Hukum 4). Agen **dilarang** mengeditnya — hanya manusia `zaryu`. Dokumen ini menyiapkan teks final (before → after) agar Anda tinggal tempel. Semua file **lain** yang tidak beku sudah saya eksekusi (lihat `docs/reports/status-hukum-otoritas-model-2026-08-21.md`).
>
> **Perubahan inti (D-0003):**
> 1. Allowlist 2 → 4 model Zen free: +`nemotron-3.5-lightning-free`, +`mimo-v2.5-free`.
> 2. Switch **sesama keluarga** = bebas lanjut, **tanpa** HANDOFF/fence. Fence **tetap** untuk model asing/forbidden.

---

## File 1 — `core/CONSTITUTION.md`

### Hukum 2 — SEBELUM

```markdown
2. **Hanya dua model boleh berpikir.** `opencode-zen/nemotron-3-ultra-free` dan `opencode-zen/hy3-free`. Model lain (9router, juan, huancheng, gemini, gemma, zai, gratislonggar, cf/*) **bukan otak**. Jika kamu bukan salah satu dari dua itu: BERHENTI menulis, tulis handoff, tunggu manusia.
```

### Hukum 2 — SESUDAH

```markdown
2. **Hanya keluarga Zen yang boleh berpikir.** `opencode-zen/nemotron-3-ultra-free` (utama), `opencode-zen/nemotron-3.5-lightning-free`, `opencode-zen/hy3-free`, `opencode-zen/mimo-v2.5-free`. Model lain (9router, juan, huancheng, gemini, gemma, zai, gratislonggar, cf/*) **bukan otak**. Jika kamu bukan salah satu dari empat itu: BERHENTI menulis, tulis handoff, tunggu manusia.
```

### Hukum 3 — SEBELUM

```markdown
3. **Ganti model = ganti dunia.** Jangan lanjut tugas seolah tidak terjadi apa-apa. Tulis `core/runtime/HANDOFF.md`. Jangan ubah file core sampai manusia atau skrip menurunkan fence.
```

### Hukum 3 — SESUDAH

```markdown
3. **Ganti model sesama keluarga ≠ ganti dunia.** Bebas lanjut. **Ganti ke model asing = ganti dunia:** tulis `core/runtime/HANDOFF.md`, jangan lanjut tugas, jangan ubah file core sampai manusia menurunkan fence.
```

> Disarankan juga bump `Versi: 2.0` → `2.1` di header konstitusi.

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
  - id: opencode-zen/nemotron-3-ultra-free
    provider: opencode-zen
    model: nemotron-3-ultra-free
    role: primary
    notes: free tier Zen; ID di opencode: opencode/nemotron-3-ultra-free
  - id: opencode-zen/nemotron-3.5-lightning-free
    provider: opencode-zen
    model: nemotron-3.5-lightning-free
    role: same-family-alternate
    notes: free tier Zen; cadangan se-tier (same NVIDIA family)
  - id: opencode-zen/hy3-free
    provider: opencode-zen
    model: hy3-free
    role: same-family-alternate
    notes: free tier Zen; ID di opencode: opencode/hy3-free
  - id: opencode-zen/mimo-v2.5-free
    provider: opencode-zen
    model: mimo-v2.5-free
    role: workhorse
    notes: free tier Zen; kompresi/ringkasan non-sensitif
```

### 2b. `on_rate_limit:` — SEBELUM

```yaml
on_rate_limit:
  action: same-family-or-halt
  same_family_fallback:
    - provider: opencode-zen
      model: hy3-free
  after_switch: fence_core_writes
```

### 2b. `on_rate_limit:` — SESUDAH

```yaml
on_rate_limit:
  action: same-family-or-halt
  same_family_fallback:
    - provider: opencode-zen
      model: nemotron-3.5-lightning-free
    - provider: opencode-zen
      model: hy3-free
  after_switch: no_fence_same_family   # sesama keluarga bebas lanjut (D-0003); fence hanya untuk model asing
```

> `never:` (daftar hop terlarang) **tidak berubah** — tetap melarang 9router/juan/huancheng/model pensiun.

### 2c. `telegram.alternate:` — SEBELUM

```yaml
telegram:
  # Snapshot 2026-08-21 — keluarga baru setelah suksesi otak (D-0002).
  unify_to: opencode-zen/nemotron-3-ultra-free
  alternate: opencode-zen/hy3-free
  threads: ["1", "802", "803", "804", "1172"]
```

### 2c. `telegram.alternate:` — SESUDAH

```yaml
telegram:
  # Snapshot 2026-08-21 — keluarga baru setelah suksesi otak (D-0002) + D-0003 (allowlist 4 model).
  unify_to: opencode-zen/nemotron-3-ultra-free
  alternate: opencode-zen/hy3-free
  alternates: [opencode-zen/nemotron-3.5-lightning-free, opencode-zen/mimo-v2.5-free]
  threads: ["1", "802", "803", "804", "1172"]
```

### 2d. `compression:` — SEBELUM (opsional, sesuai LAPORAN §4.1)

```yaml
compression:
  provider: opencode-zen
  model: hy3-free
  threshold: 0.50
```

### 2d. `compression:` — SESUDAH (opsional)

```yaml
compression:
  provider: opencode-zen
  model: mimo-v2.5-free
  threshold: 0.50
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

`opencode-zen/nemotron-3-ultra-free` (utama) · `opencode-zen/nemotron-3.5-lightning-free` · `opencode-zen/hy3-free` · `opencode-zen/mimo-v2.5-free`
Selain itu: berhenti, tulis `core/runtime/HANDOFF.md`, jangan mutasi.

## Jika ganti model

- Sesama keluarga (nemotron/lightning/hy3/mimo): bebas lanjut, tanpa fence.
- Ke model asing: berhenti, tulis `core/runtime/HANDOFF.md`, tunggu manusia.
```

---

## File 4 — `core/VISION.md`

### SEBELUM (baris 22 — Misi #3)

```markdown
3. **Bekerja jujur dengan model yang ada** — free tier OpenCode Zen (`big-pickle`, `deepseek-v4-flash-free`). Tidak berpura-pura punya model kuat. Tidak membiarkan ganti model merusak inti.
```

### SESUDAH

```markdown
3. **Bekerja jujur dengan model yang ada** — free tier OpenCode Zen (`nemotron-3-ultra-free`, `nemotron-3.5-lightning-free`, `hy3-free`, `mimo-v2.5-free`). Tidak berpura-pura punya model kuat. Tidak membiarkan ganti model merusak inti.
```

> Disarankan juga bump `Versi: 2.0` → `2.1` di header visi.

---

## Checklist pengesahan (zaryu)

- [ ] Terapkan File 1 (Hukum 2 & 3) di `core/CONSTITUTION.md` (opsional: bump Versi → 2.1)
- [ ] Terapkan File 2 (allowed / on_rate_limit / telegram / compression) di `core/MODEL.policy.yaml`
- [ ] Terapkan File 3 di `core/AGENTS.slim.md`
- [ ] Terapkan File 4 (Misi #3) di `core/VISION.md`
- [ ] Seal `core/ledger/decisions/D-0003.yaml` (ubah `status: draft` → `sealed`)
- [ ] (Opsional) Update `core/STATE.yaml` `health.cron_agent_reach_watch` setelah cron di-re-pin di mesin zaryu

> Setelah seal, runtime `scripts/niu_corelib.py` sudah sinkron (allowlist 4 model + same-family tanpa fence) — tidak perlu aksi tambahan di kode.

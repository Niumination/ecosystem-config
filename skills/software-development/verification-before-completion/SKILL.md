---
name: verification-before-completion
description: "Use when ABOUT to claim work is complete, fixed, or passing — before committing or creating PRs. Requires running verification commands and confirming output before any success claims."
domain: software-development
subdomain: sdlc
tags: [verification, testing, quality, completion, claims, evidence]
version: "1.0"
author: obra/superpowers + Niumination
source: superpowers
license: MIT
---

# Verification Before Completion

> **Sumber:** Diadaptasi dari `obra/superpowers` (MIT).

**Core principle:** Evidence before claims, always.

Melengkapi `systematic-debugging` (debugging workflow) dan `hermes-zero-defect-architect` (zero-defect protocol). Skill ini adalah **HARD GATE** — jangan klaim selesai tanpa verifikasi.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Jika belum menjalankan verification command di pesan ini, jangan klaim passing.

## The Gate Function

```
SEBELUM mengklaim status atau menyatakan kepuasan:

1. IDENTIFIKASI: Command apa yang membuktikan klaim ini?
2. RUN: Eksekusi FULL command (fresh, complete)
3. BACA: Full output, check exit code, count failures
4. VERIFIKASI: Apakah output mengkonfirmasi klaim?
   - Jika TIDAK: State actual status dengan evidence
   - Jika YA: State claim DENGAN evidence
5. BARU THEN: Buat klaim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |

## Red Flags — STOP

- Menggunakan "should", "probably", "seems to"
- Expressing satisfaction sebelum verifikasi ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- Berpikir "just this once"

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## Integrasi Ekosistem

| Skill | Hubungan |
|-------|----------|
| `systematic-debugging` | Verification adalah fase terakhir debugging |
| `hermes-zero-defect-architect` | Zero-defect memerlukan verifikasi absolut |
| `ponytail-core` | Minimal code + verified = efisien dan benar |
| `requesting-code-review` | Verifikasi sebelum kirim review |

## Real Case: "Narrative Completion" — Dashboard Template (2026-08-13)

**Insiden:** Thread #general MC (model `gemini-3.5-flash-lite`) diminta integrasi template dashboard ke Mission Control. Agent mengklaim *"Perubahan sudah diterapkan"* — padahal **tidak ada satu pun file yang berubah**.

**Apa yang sebenarnya terjadi (dari export session):**
1. Tool call overwrite (`cat << EOF`) **ditolak sistem** (terdeteksi `&` backgrounding)
2. Agent TIDAK retry dengan cara benar — malah **menampilkan perintah bash sebagai teks** di chat
3. Lalu mengklaim "Perubahan sudah diterapkan" — **zero tool call sukses**
4. Bonus: path tujuan salah (`niu-mission-control/index.html` vs asli `dashboard/index.html`), dan template sendiri tidak punya section "context window/directive" yang diklaim diterapkan

**Pelajaran — pola "narrative completion":**
- Agent kelas flash sering menyelesaikan **secara naratif**: menulis apa yang *seharusnya* terjadi, bukan apa yang *terjadi*
- Tool call ditolak/diblokir ≠ alasan berhenti — harus **retry dengan cara lain** (write_file, cp terpisah, dsb.)
- Menampilkan perintah sebagai teks ≠ menjalankannya

**Checklist verifikasi khusus file overwrite/integrasi:**
```
1. SETELAH klaim "file ditimpa/diintegrasi":
   - stat -f '%Sm' <file> → mtime BARU (bukan tanggal lama)
   - md5 -q <target> vs <sumber> → sama kalau copy persis
   - grep -c "<marker unik>" <file> → section benar-benar ada
   - curl HTTP endpoint → halaman serve versi baru
2. SEBELUM klaim: pastikan ADA tool call sukses di history (bukan teks bash)
3. Path absolut tujuan harus diverifikasi dulu (find/grep server.py utk cari file yang di-serve)
```

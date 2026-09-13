# Blueprint Template — Architecture Adaptation

Template untuk blueprint adaptasi arsitektur dari proyek eksternal.

## Struktur Blueprint

```markdown
# <Project> v<Version> — BLUEPRINT & PRD

> **Status:** Draft untuk review
> **Target:** Adaptasi arsitektur dari <Referensi>
> **Prinsip:** Tidak masalah rubah stack, yang penting tujuan tercapai

---

## 1. Executive Summary
- Versi saat ini: masalah & akar penyebab
- Proyek referensi: mengapa dipilih, bukti berhasil
- Unique value yang dipertahankan dari proyek lama

## 2. Masalah & Solusi

| Masalah | Root Cause | Solusi | Sumber |
|---|---|---|---|
| ... | ... | ... | ... |

## 3. Arsitektur Target

### High-Level Diagram
```
[diagram boxes and arrows]
```

### Packages/Modules

| Package | Responsibility | Reference |
|---|---|---|
| ... | ... | ... |

### Yang Dipertahankan dari Versi Lama

| Modul | Alasan |
|---|---|
| ... | ... |

## 4. Rencana Implementasi

### Phase N: <Name> (Minggu X-Y)

**Goal:** ...

| Task | Deliverable | Verification |
|---|---|---|
| ... | ... | ... |

**Definition of Done:**
- ...
- ...

## 5. Struktur Proyek

```
<target directory tree>
```

## 6. Dependencies

### External (SPM)

| Package | Version | Purpose |
|---|---|---|
| ... | ... | ... |

### Bundled

| Binary | Version | Source |
|---|---|---|
| ... | ... | ... |

### System Requirements

| Requirement | Minimum |
|---|---|
| macOS | ... |
| Xcode | ... |
| Swift | ... |
| Android | ... |

## 7. Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| ... | ... | ... |

## 8. Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ... | ... | ... | ... |

## 9. Migration Path

| v<Lama> | v<Baru> | Catatan |
|---|---|---|
| `modul_lama.py` | `Packages/.../ModulBaru.swift` | ... |

## 10. Timeline

| Phase | Minggu | Deliverable |
|---|---|---|
| 1 | 1-2 | ... |
| 2 | 3-4 | ... |
| ... | ... | ... |

## 11. Open Questions

1. ...
2. ...

---

**Next Steps:**
1. Review dan approve blueprint
2. Setup project skeleton (Phase 1)
3. Mulai development
```

## Contoh Nyata: niu-cast v4.0

Lihat `BLUEPRINT.md` di `services/niu-cast/` untuk contoh blueprint lengkap yang sudah dijalankan (5 fase, 12 minggu, 7 packages).

### Key Decisions

| Decision | Rationale |
|---|---|
| Swift 6 + SwiftUI | macOS native, VideoToolbox, Metal |
| XcodeGen | Project generation dari YAML — deterministik |
| SPM packages | Modular, testable, reusable |
| ADB + scrcpy | Proven stable (reference: DroidMirroring) |
| TCCPKit | Unique value — tidak ada di referensi |

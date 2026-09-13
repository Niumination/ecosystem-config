---
name: ecosystem-architecture-adoption
description: "Adapt external architecture into existing project."
tags: [ecosystem, architecture, rewrite, migration, planning]
---

# Architecture Adoption

## Trigger
User kirim URL repo + **"adopsi arsitektur ini"** / **"kita rubah stack mengikuti ini"** / **"pelajari untuk adaptasi"**.

## Aturan Keras
- **"pelajari ini" = study + lapor + tunggu instruksi.**
- **Blueprint dulu, eksekusi kemudian.**
- **Unique value proyek lama harus dipertahankan.**
- **Bundle dependencies** di app resources.
- **Match client's OS target.**

## Workflow

### Step 1: Deep Study Referensi
1. `web_extract` halaman utama + README GitHub
2. **Clone repo** ke /tmp (`git clone --depth 1`) — baca kode intri + packages/modules
3. Identifikasi **unique value** referensi yang tidak ada di proyek kita

### Step 2: Gap Analysis
Bandingkan kondisi proyek saat ini vs referensi:
- Stack, architecture patterns, features, performance
- Tiap gap: bukti konkret (path file, angka, output command)

### Step 3: Blueprint Document
Lokasi: `services/<project>/BLUEPRINT.md`

Struktur: Executive Summary → Problems & Solutions → Target Architecture → Implementation Phases → Project Structure → Dependencies → Success Metrics → Risks → Migration Path → Timeline → Open Questions

### Step 4: Eksekusi Bertahap
Setiap fase:
1. Task table dengan Deliverable + Verification columns
2. Definition of Done — konkret, bisa dibuktikan
3. Commit per fase: `feat(v<N>): Phase <N> — <title>`
4. Verifikasi sebelum lanjut (syntax check, build check, manual test)

## Real Example: niu-cast v4.0

| Aspek | Detail |
|---|---|
| **Referensi** | DroidMirroring-mac (matyle/droidMirroring-mac) |
| **Proyek asal** | niu-cast v3.7 (Python + PyQt5 + VNC) |
| **Stack baru** | Swift 6 + SwiftUI + XcodeGen + SPM |
| **Lama kerja** | 12 minggu (3 bulan) |
| **Unique value dipertahankan** | TCCP/Joy Connect protocol |
| **Packages** | ADBKit, ScrcpyClient, MirrorEngine, FusionEngine, DeviceDiscovery, TCCPKit, SharedModels |

## Pitfalls
- **Tidak ada Xcode di mesin** — CI/CD GitHub Actions atau build di mesin lain
- **VideoToolbox Swift complexity** — mulai dengan AKScreencapture fallback
- **UHID kernel rejection** — fallback ke ADB input
- **scrcpy-server compatibility** — test dengan scrcpy 4.x

## Related
- `ecosystem-tool-adoption` — adopsi tool/library pihak ketiga
- `ekosistem-scaffold` — daftar proyek baru ke ekosistem
- `plan` — tulis markdown plan ke .hermes/plans/

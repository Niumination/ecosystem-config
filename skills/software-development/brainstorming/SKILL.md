---
name: brainstorming
description: "Use BEFORE any creative work — creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
domain: software-development
subdomain: sdlc
tags: [design, planning, requirements, spec, user-intent, sdlc]
version: "1.0"
author: obra/superpowers + Niumination
source: superpowers
license: MIT
---

# Brainstorming — Turn Ideas Into Designs

> **Sumber:** Diadaptasi dari `obra/superpowers` (MIT). Lihat `docs/sources/superpowers.md` untuk atribusi lengkap.

Bantu mengubah ide mentah menjadi spesifikasi dan desain yang matang melalui dialog kolaboratif. Skill ini adalah **HARD GATE** — jangan menyentuh kode sebelum user menyetujui desain.

**Integrasi Niumination:** Melengkapi `ponytail-core` (YAGNI sebelum coding) dan `ultrathink` (architectural reasoning). Brainstorming = apa yang akan dibangun, ultrathink = bagaimana arsitekturnya.

<HARD-GATE>
Jangan panggil implementation skill APAPUN, tulis kode, scaffold project, atau lakukan action implementasi sebelum menyajikan desain DAN user menyetujuinya. Ini berlaku untuk SEMUA project tanpa terkecuali.
</HARD-GATE>

## Anti-Pattern: "Ini Terlalu Sederhana, Gak Perlu Desain"

Semua project wajib lewat proses ini. Todo list, utility satu fungsi, config change — semua sama. Project "sederhana" adalah tempat asumsi yang tidak diperiksa menyebabkan pemborosan terbesar. Desain bisa pendek (beberapa kalimat untuk project sederhana), tapi WAJIB disajikan dan disetujui.

## Checklist

Wajib buat task untuk setiap item dan selesaikan secara berurutan:

1. **Eksplorasi konteks project** — cek file, docs, recent commits
2. **Tanya pertanyaan klarifikasi** — satu per satu, pahami purpose/konstrain/success criteria
3. **Propose 2-3 pendekatan** — dengan trade-off dan rekomendasi
4. **Sajikan desain** — dalam seksi sesuai kompleksitas, minta approval tiap seksi
5. **Tulis design doc** — simpan ke `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` dan commit
6. **Spec self-review** — cek placeholder, kontradiksi, ambiguitas, scope
7. **User review spec** — minta user review file spec sebelum proceed
8. **Transisi ke implementasi** — panggil `writing-plans` skill untuk buat implementation plan

## Proses

**Memahami ide:**
- Cek state project saat ini (files, docs, recent commits)
- Tanya satu per satu: purpose, konstrain, success criteria
- Prefer multiple choice questions

**Mengeksplorasi pendekatan:**
- Propose 2-3 pendekatan dengan trade-off
- YAGNI ketat — buang fitur yang tidak perlu dari setiap pendekatan

**Menyajikan desain:**
- Scale tiap seksi ke kompleksitasnya
- Bahas: arsitektur, komponen, data flow, error handling, testing

**Desain untuk isolasi dan clarity:**
- Pecah sistem menjadi unit kecil dengan satu purpose jelas
- Setiap unit harus bisa dipahami tanpa baca internalnya

## Setelah Desain

- Tulis validated design ke `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- **Spec Self-Review:** Cek placeholder, internal consistency, scope, ambiguity
- **User Review Gate:** Minta user review spec sebelum proceed
- **Implementasi:** Panggil `writing-plans` skill — BUKAN skill lain

## Integrasi dengan Ekosistem Niumination

| Skill Niumination | Hubungan |
|-------------------|----------|
| `ponytail-core` | YAGNI — brainstorming cegah fitur tidak perlu |
| `ultrathink` | Brainstorming = "apa yang dibangun", ultrathink = "gimana arsitekturnya" |
| `project-orientation` | Brainstorming dimulai dengan orientasi project |
| `writing-plans` | **WAJIB** dipanggil setelah brainstorming selesai |

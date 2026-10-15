---
name: config-history-review
description: "Review Hermes config history using filesystem evidence (backup files, changelogs, git logs) — NOT session search or memory. Use when user asks to retrace changes, audit history, or check what happened over time."
version: "1.0.0"
author: Hermes Agent
tags: [hermes, config, history, audit, verification, filesystem-evidence]
related_skills: [hermes-configuration-tuning, verification-before-completion]
---

# Config History Review — Filesystem Evidence First

> **Core principle:** Ketika user minta review/audit/rekap perubahan config atau ekosistem, SELALU pakai bukti filesystem aktual — bukan session_search, bukan memory, bukan asumsi dari context summary.

## Kenapa Skill Ini Penting

User secara eksplisit koreksi:
> "kamu harusnya tau aku selalu menginginkan data valid bukan rekayasa/kebodohan kamu"

Pola error yang dicegah:
1. Agent pakai `session_search` → data incomplete (context compaction membuang detail)
2. Agent "rekayasa" jawaban dari potongan-potongan yang tersisa → data tidak valid
3. Agent klaim sesuatu tanpa verifikasi filesystem → user marah

## Langkah Kerja

### 1. IDENTIFIKASI Sumber Data

```
Ada tiga sumber utama config history:

a) Config backup files (PALING AKURAT)
   /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml*
   
b) Ecosystem changelog
   /Users/zaryu/Desktop/Niumination/brain/docs/ecosystem-changelog.md
   
c) Git log (jika proyek punya repo)
   git log --oneline -20
```

### 2. EXTRACT dari Backup Files

Jangan baca satu per satu — pakai `execute_code` untuk loop semua backup:

```python
import re, os

data_dir = "/Volumes/HermesAgent/HermesAgentUSB/data/"
backups = sorted([
    f for f in os.listdir(data_dir)
    if f.startswith("config.yaml") and f != "config.yaml"
])

for bak in backups:
    path = os.path.join(data_dir, bak)
    with open(path) as f:
        content = f.read()
    
    provider = re.search(r'^\s+provider:\s*(.+)', content, re.M)
    default_model = re.search(r'^\s+default:\s*(.+)', content, re.M)
    base_url = re.search(r'^\s+base_url:\s*(.+)', content, re.M)
    has_overrides = 'channel_overrides' in content
    has_prompts = 'channel_prompts' in content
    
    # Extract plugins from enabled section
    plugins_match = re.findall(r'- (\w[\w-]*)', content[content.find('plugins:'):] if 'plugins:' in content else '')
    
    print(f"=== {bak} ({os.path.getsize(path)} bytes) ===")
    print(f"  Provider: {provider.group(1).strip() if provider else 'N/A'}")
    print(f"  Model: {default_model.group(1).strip() if default_model else 'N/A'}")
    print(f"  Base URL: {base_url.group(1).strip() if base_url else 'N/A'}")
    print(f"  Overrides: {has_overrides} | Prompts: {has_prompts}")
    print(f"  Plugins: {[p for p in plugins_match if p not in ['enabled','entries']]}")
    print()
```

### 3. PRESENTASIKAN Hasil

Tabel kronologis:
```
| Tanggal | Provider | Model | Perubahan Signifikan |
|---------|----------|-------|---------------------|
| Jun 30 | opencode-zen | big-pickle | Awal |
| Jul 7 | nvidia_nim | deepseek-v4-pro | Percobaan NVIDIA |
...
```

**HARUS menyebutkan:** "Data di atas murni dari file backup aktual (config.yaml.bak.* dengan timestamp real). Tidak ada yang direkayasa."

## Backup Naming Convention

| Pattern | Arti |
|---------|------|
| `config.yaml.bak` | Backup terakhir sebelum edit |
| `config.yaml.bak.YYYYMMDD_HHMMSS` | Auto-backup dengan timestamp |
| `config.yaml.bak-YYYYMMDD-HHMMSS` | Auto-backup format alternatif |
| `config.yaml.bak.*_before_rollback` | Manual rollback point |

## Warning: Parsing Artifacts

Beberapa backup menampilkan nama plugin aneh (contoh: "asisten", "jangan", "agent") — ini parsing error dari YAML kompleks, bukan nama plugin sesungguhnya. Cross-check selalu dengan:
```bash
ls /Volumes/HermesAgent/HermesAgentUSB/data/plugins/
```

## Integrasi

| Skill | Hubungan |
|-------|----------|
| `hermes-configuration-tuning` | Config audit — skill ini melengkapi dengan metodologi history review |
| `verification-before-completion` | Prinsip "evidence first" yang sama, diterapkan ke config history |

## Pitfalls

1. **JANGAN pakai session_search untuk rekonstruksi config history** — context compaction membuang detail
2. **JANGAN fabricate data** — kalau backup tidak ada, bilang "tidak ditemukan"
3. **JANGAN gabungkan session memory dengan filesystem data** —pisahkan sumbernya
4. **Path USB bisa berbeda** — cek `ls /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml*` dulu

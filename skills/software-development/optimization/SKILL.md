---
name: optimization
description: "Improve performance, latency, and throughput of code and systems. Systematic profiling → bottleneck detection → targeted optimization."
version: 1.0.0
author: Jcode (bundled) + Hermes Agent
source: "Jcode bundled — /optimization"
tags: [software-development, performance, optimization, profiling]
platforms: [macos, linux, windows]
---

# Optimization — Performance Tuning

## Trigger
Gunakan skill ini ketika user meminta "optimalkan", "percepat", "kurangi latency", "profiling", "bottleneck", "performance issue", atau "/optimization".

## Prasyarat
- Profiling tools sesuai stack (Chrome DevTools, py-spy, perf, xcode instruments)
- Benchmark sebelum-sesudah untuk validasi
- Target metrik yang jelas (ms, MB, QPS)

## Prosedur

### 1. Profiling (jangan tebak)
Sebelum optimasi, ukur dulu:
```bash
# Python
python -m cProfile -o output.prof script.py
py-spy record -o profile.svg --pid PID

# Node.js
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# Web: Chrome DevTools Performance tab
# Database: EXPLAIN ANALYZE
```

### 2. Identifikasi Bottleneck
Cari operasi paling lambat atau paling boros memori:
- **CPU-bound:** hot loop, algoritma O(n²), regex berlebihan
- **I/O-bound:** query N+1, file read tanpa buffer, network serial
- **Memory-bound:** cache miss, alloc/dealloc berulang, memory leak

### 3. Pilih Optimasi Paling Efektif (Pareto)
| Masalah | Solusi Minimal |
|---------|---------------|
| N+1 query | Batch query atau JOIN |
| Loop lambat | Pindah ke stdlib/set/dict |
| Render ulang | Memoization, virtual list |
| File besar | Streaming, chunked read |
| Cache miss | LRU cache, precompute |

### 4. Validasi
```
BEFORE: 2450ms, 128MB
AFTER:   320ms,  45MB
IMPROVEMENT: 7.6x faster, 65% less memory
```

### 5. Commit & Dokumentasi
- Tulis temuan di commit message
- Update benchmark jika ada di repo

## Pitfalls
- ❌ Optimasi tanpa profil = tebakan
- ❌ Mikro-optimasi sebelum bottleneck utama
- ❌ Optimasi yang bikin kode susah dibaca (YAGNI)
- ✅ 80% improvement dari 20% usaha — cari itu dulu

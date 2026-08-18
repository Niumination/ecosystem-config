# Analisis System Design Primer — Relevansi Niumination

| Field | Nilai |
|---|---|
| **Tanggal** | 18 Agustus 2026 |
| **Sumber** | https://github.com/donnemartin/system-design-primer (clone penuh, 25 MB) |
| **Lisensi** | Creative Commons BY 4.0 |
| **Status** | Referensi teori — disimpan, belum diterapkan |

---

## Apa Ini

Kumpulan terorganisir prinsip desain sistem skala besar (~300k stars): trade-off fundamental, pola infrastruktur, database, cache, async, komunikasi, + 9 solusi desain lengkap (Pastebin, Twitter, Web Crawler, dll).

## Index Topik

1. **Trade-off**: Performance vs Scalability · Latency vs Throughput · Availability vs Consistency (CAP)
2. **Infrastruktur**: DNS → CDN → Load Balancer → Reverse Proxy → App layer → DB → Cache → Async → Komunikasi
3. **Database**: Replication (master-slave/master-master), Federation, Sharding, Denormalization, SQL tuning, NoSQL (key-value/document/wide-column/graph), SQL vs NoSQL
4. **Cache**: Cache-aside · Write-through · Write-behind · Refresh-ahead
5. **Async**: Message queues · Task queues · Back pressure
6. **Komunikasi**: TCP/UDP · RPC · REST · Security
7. **9 Solusi**: mint, pastebin, query_cache, sales_rank, scaling_aws, social_graph, twitter, web_crawler + template

## Relevansi ke Niumination

| Konsep Primer | Kondisi Niumination |
|---|---|
| SPOF (fail-over/replication) | MC :5200 down, 9router localhost = SPOF tunggal |
| Availability vs consistency | 5 thread di 5 model beda = inconsistency state |
| Back pressure | Tidak ada — model lemah lanjut tugas diam-diam |
| Health check / load balancer | Tidak ada supervisor untuk Gateway/MC/9router |
| Service discovery | Gateway 1 active agent, orchestrator 40% stale |
| Message/task queue | Tidak ada antrian |
| Database | state.db 732 MB di ExFAT (jangan live DB di non-journaled) |
| Cache | RTK 68.7% savings ✅ sudah benar |
| CAP | Fallback zoo = konsistensi dikorbankan demi availability palsu |

## Pola yang Bisa Diadopsi

1. **Health check + fail-over** → `niu-health-probe.py` + launchd KeepAlive (paket v2)
2. **Back pressure** → "HALT + HANDOFF" di MODEL.policy.yaml = back pressure untuk model lemah
3. **Async task queue** → `POST /tasks` orchestrator (v1, ditunda v2)
4. **Federation** → skill plane: bank 47 SoT, USB mirror, HOME pin
5. **Write-behind cache** → ledger no-agent (hooks on_session_end) = persist tanpa LLM

## Kesimpulan

Primer = referensi teori untuk rekonstruksi. Paket `niumination-rebuild-v2` sudah menerjemahkan konsep-konsep kunci (SPOF, fail-closed, back pressure, health check) ke implementasi konkret untuk Hermes.

---

*Sumber README asli disalin ke folder ini (README.md, 107 KB).*
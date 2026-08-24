# Quick-Wins Cleanup — 20 Ags 2026 (DoD verifikasi + storage hygiene)

Transcript lengkap eksekusi quick-wins di ekosistem Niumination/Hermes.

## Konteks

Setelah F1-F5 rekonstruksi + frontend MC 12/12 selesai, quick-wins menutup
sisa "anomali" dari audit awal: verifikasi DoD resmi + bersihkan noise storage.

## 1. DoD — 4 kondisi hijau (verifikasi cepat)

| DoD | Perintah | Harapan |
|---|---|---|
| 1 Control loop | `launchctl print gui/501/niu.missioncontrol` + `...niu.healthprobe` + `curl :5200/healthz` | running + pid; probe running; healthz `{"status":"ok"}` |
| 2 Fail-closed | `hermes fallback ls`; `hermes cron list` | Primary big-pickle; chain 1 kaki opencode-zen/deepseek-v4-flash-free; cron `c6ec80ed633f` Last run `ok` |
| 3 Skill plane | `find skills -name SKILL.md \| wc -l`; `wc -c AGENTS.md` | Bank 47; AGENTS.md 994B (≤2KB) |
| 4 Token tax | grep compression; `hermes plugins list \| grep rtk` | compression enabled threshold 0.5; rtk-rewrite enabled |

Catatan: home skill naik 113→129 karena 8 skill dibuat selama kerja rekonstruksi
(hermes-skills-setup, niu-core-governance, provider-fallback, dll) — ini wajar,
bukan sampah. Jangan otomatis arsip.

## 2. mcp-stderr.log — 1.83MB / 29.943 lines → 0 bytes

Ampas error MCP yang sudah dihapus (uacc, ponytail, notebooklm). Backup dulu,
lalu **truncate** (bukan rm — log roller bisa butuh filenya):

```bash
cp data/logs/mcp-stderr.log /tmp/mcp-stderr.pre-clean.log
: > data/logs/mcp-stderr.log        # truncate aman
```

## 3. LSP node_modules — 409MB → 162MB (hemat 247MB)

Config `lsp:` hanya mengaktifkan `typescript` (typescript-language-server).
`package.json` deps punya 6 server language → 5 tidak dipakai di config:

```bash
cd data/lsp
# 1. TAR backup (rollback satu perintah)
tar -czf /tmp/lsp-node_modules.bak.tar.gz node_modules
# 2. Hapus paket yang tidak direferensikan config LSP:
rm -rf node_modules/pyright node_modules/yaml-language-server \
       node_modules/bash-language-server \
       node_modules/dockerfile-language-server-nodejs \
       node_modules/dockerfile-language-service
# 3. Test binary inti masih jalan:
./node_modules/.bin/typescript-language-server --version   # → 5.3.0
# 4. hermes config check → Config version 33 ✓
```

Hasil: 61 paket → 56; typescript 5.3.0 tetap jalan; config valid.

## 4. state.db backup ke APFS internal (keluar dari ExFAT)

state.db 752MB di USB ExFAT (risiko korupsi — non-journaled). Backup ke internal
APFS journaled + verify SHA:

```bash
mkdir -p /Users/zaryu/Backups/hermes-state
cp /Volumes/HermesAgent/HermesAgentUSB/data/state.db \
   /Users/zaryu/Backups/hermes-state/state.db.2026-08-20.bak
shasum -a 256 <asli> | cut -d' ' -f1 > /tmp/sha-orig.txt
shasum -a 256 <backup> | cut -d' ' -f1 > /tmp/sha-bak.txt
diff /tmp/sha-orig.txt /tmp/sha-bak.txt   # kosong = valid
```

- `state.db-wal` ada → WAL aktif, `cp` snapshot bersifat point-in-time.
  Untuk backup konsisten penuh pakai `sqlite3 source.db ".backup 'target.db'"`
  (checkpointed); `cp` + verify tetap OK untuk snapshot cepat.
- Lokasi backup permanen: `/Users/zaryu/Backups/hermes-state/` (APFS internal,
  36Gi free di /System/Volumes/Data; USB HermesAgent cuma 17Gi free).

## Filesystem reference (untuk prediksi ruang)

- `/System/Volumes/Data` — APFS internal, 36Gi free (journaled → backup target)
- `/Volumes/Niumination` — disk0s4, 44Gi free, inode 100% (jangan taruh banyak file kecil)
- `/Volumes/HermesAgent` — USB ExFAT, 17Gi free (live data, risiko korupsi → backup rutin)

## Pelajaran

1. "Hijau" = verifikasi dengan perintah, bukan asumsi. DoD dijalankan tiap penutupan fase.
2. Truncate ≠ delete untuk file log yang masih dirujuk proses.
3. Sebelum hapus node_modules/package: TAR backup + test binary inti — tidak pernah "cleanup = hilang".
4. Backup DB = copy + SHA verify; jangan klaim valid tanpa diff hash.
5. Skill home naik sedikit setelah kerja = normal; bedakan "sampah dump" (arsip) vs "buatan kerja" (keep).
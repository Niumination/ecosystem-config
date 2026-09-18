# F4 — HOME Skill Plane Pruning (20 Ags 2026)

Metode membesarkan `data/skills` (Hermes HOME catalog) yang terverifikasi di sesi rekonstruksi F4.
Target konstitusi v2: HOME = mirror bank 47 (+ builtin Hermes + skill sistem inti), BUKAN dump 213+.

## Masalah

`/Volumes/HermesAgent/HermesAgentUSB/data/skills/` punya **213 SKILL.md** saat audit — 166 di antaranya
TIDAK ada di Bank (`~/Desktop/Niumination/skills/`, 47 SKILL.md = source of truth). Ini membuat context
pollution: Hermes menyuntik 213 skill ke katalog tiap sesi.

## Klasifikasi (gambar dulu, jangan hapus sembarangan)

1. **Ambil daftar ekstra** (di HOME, tidak di bank):
   ```bash
   cd /Volumes/HermesAgent/HermesAgentUSB/data/skills
   comm -13 <(cd /Users/zaryu/Desktop/Niumination/skills && find . -name "SKILL.md" | sort) \
            <(find . -name "SKILL.md" | sort) | sed 's|^\./||; s|/SKILL.md$||' > /tmp/home-extra.txt
   ```
2. **Tandai BUILTIN Hermes — JANGAN DISENTUH.** `hermes skills list` → kolom Source = `builtin`
   (52 builtin di install ini). Ambil daftar nama:
   ```bash
   hermes skills list 2>&1 | awk -F'│' '{gsub(/^ +| +$/,"",$2); if ($2!="" && $2!="Name") print $2"|"$5}' \
     | grep "| builtin" | awk -F'|' '{gsub(/ /,"",$1); print $1}' | sort -u > /tmp/builtin-names.txt
   ```
   Builtin tidak ada file-nya di `data/skills` sendiri (di `src/hermes-agent/skills/`) — folder di HOME
   dengan nama sama bisa jadi duplikat; hanya arsipkan yang benar-benar dump.
3. **Tandai skill buatan rekonstruksi** (kadang dibuat langsung di HOME, belum masuk bank) —
   mtime `>= 08-16` (era kerja rekonstruksi): `stat -f '%Sm' -t '%m-%d' <SKILL.md>`.
   Contoh yang wajib keep: `provider-fallback`, `hermes/hermes-provider-config`,
   `devops/niu-mission-control-ops`, `ecosystem/skill-bank-*`, `ecosystem/ecosystem-snapshot`.
4. **Sisanya = DUMP → arsip.**

## Arsip (MOVE, bukan hapus — rollback 1 perintah)

```bash
BACKUP=/Volumes/HermesAgent/HermesAgentUSB/data/skills_archive_2026-08-20
mkdir -p "$BACKUP"
while read rel; do
  name=$(basename "$rel")
  grep -qx "$name" /tmp/builtin-names.txt && continue          # builtin: keep
  mdate=$(stat -f '%Sm' -t '%m-%d' "$rel/SKILL.md" 2>/dev/null)
  [[ "$mdate" > "08-15" ]] 2>/dev/null && continue             # rekonstruksi: keep
  echo "$rel" | grep -qE "^(hermes/|provider-fallback$|computer-use$|codebase-intelligence$|language-preference$)" && continue
  mkdir -p "$BACKUP/$(dirname "$rel")"
  mv "$rel" "$BACKUP/$rel"
done < /tmp/home-extra.txt
```
- Arsip di LUAR `data/skills/` (Hermes tidak memindai folder arsip).
- Nama folder `skills_archive_<YYYY-MM-DD>` — konsisten, mudah dibalik.

## Verifikasi

```bash
hermes skills list 2>&1 | grep -c "enabled"        # total turun (213 → 113 di sesi ini)
hermes skills inspect apple/macos-disk-cleanup     # → "Could not find in any source" (arsip benar)
hermes config check                                # version 33 ✓, tidak ada skill yang "error"
find /Volumes/HermesAgent/HermesAgentUSB/data/skills -name "SKILL.md" | wc -l
```

## Hasil sesi ini

HOME 213 → **113** (arsip 100). Komposisi akhir: 47 mirror bank + 38 builtin + 28 rekonstruksi/inti.
Uji coba sebelum eksekusi: hermes config check OK, cron tidak mereferensi skill arsip, ledger harian tetap terisi.

## Pitfall

- `find` dengan `-o` + `-name` bisa bikin pattern aneh — pakai dua `find` terpisah bila perlu.
- Jangan hapus skill dengan deskripsi penting tanpa cek mtime — `apple/macos-*` (07-19) = dump; jangan
  arsipkan `hermes-agent-skill-authoring` (dipakai authoring!) hanya karena namanya mirip dump.
- Builtin check via `hermes skills list` perlu `grep "| builtin"` pada kolom Source — jangan pakai
  `grep builtin` mentah (ikut keluar baris header).
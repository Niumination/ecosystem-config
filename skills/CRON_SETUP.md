# Instalasi Cron — Layer 2 Skill Sync

## 1. Memastikan Script Dapat Dieksekusi

```bash
chmod +x ~/Desktop/Niumination/skills/sync-to-agents.sh
```

## 2. Tambahkan ke Crontab

Buka crontab editor:

```bash
crontab -e
```

Tambahkan baris ini (akan jalan setiap 6 jam):

```cron
# Layer 2: Sync skill bank ke Jcode + Hermes (local) + AGENTS.md (every 6h) — USB backup-only
0 */6 * * * cd ~/Desktop/Niumination && bash skills/sync-to-agents.sh > /dev/null 2>&1
```

**✅ Sudah aktif** — cron sudah terinstall sejak 29 Jul 2026. Cek dengan `crontab -l`.

## 3. Testing

Cek apakah cron terdaftar:

```bash
crontab -l
```

Tes script langsung:

```bash
bash ~/Desktop/Niumination/skills/sync-to-agents.sh --dry-run
```

## 4. Log

Sync log disimpan di `~/.sync-log` (root Niumination).
Cek log:

```bash
cat ~/Desktop/Niumination/.sync-log
```

## 5. Uninstall

Hapus dari crontab:

```bash
crontab -e  # hapus baris sync
```

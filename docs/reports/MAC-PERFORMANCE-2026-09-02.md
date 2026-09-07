# 📊 Laporan Performa macOS — 2 Sep 2026 23:01 WIB

**Operator:** Afrizal Munthe
**Host:** MacBook Intel Core i5-10310U @ 1.70GHz
**OS:** macOS 26.5 (Kernel 25.5.0)
**Uptime:** 1 jam 26 menit

---

## 1. Ringkasan Kinerja

| Metrik | Nilai | Status |
|--------|-------|--------|
| **CPU Load** | 2.52 (1m), 2.47 (5m), 3.70 (15m) | ⚠️ Elevated |
| **Memory Used** | ~14.6 GB / 16 GB | 🟡 Tinggi |
| **Memory Free** | ~1.3 GB | 🟡 Rendah |
| **Disk Used** | 16 GB / 128 GB (58%) | ✅ Normal |
| **Thermal** | No thermal warning | ✅ Normal |
| **Power** | AC Power, 83% | ✅ Good |

---

## 2. CPU Analysis

### Detail Proses Teratas

| PID | Process | CPU% | Mem% | Mem (MB) |
|-----|---------|------|------|----------|
| 13419 | Firefox plugin-container | 62.0% | 7.6% | 1,274 |
| 213 | WindowServer | 41.5% | 1.0% | 165 |
| 626 | Nicegram Desktop | 20.6% | 2.9% | 482 |
| 13402 | Firefox GPU Helper | 19.7% | 1.2% | 198 |
| 811 | Hermes Agent (.venv/python) | 8.9% | 2.1% | 357 |
| 13399 | Firefox | 8.4% | 4.8% | 797 |

**Total CPU Usage: ~160%** — artinya ~2 core penuh digunakan.

### ⚠️ Masalah Teridentifikasi

**Firefox adalah penyebab utama bottleneck:**
- Total Firefox processes: 5 processes
- Combined CPU: ~110% dari 8 cores
- Combined Memory: ~2.6 GB (16%)
- Firefox + plugin-container + GPU helper konsumsi resource tinggi

**WindowServer 41.5%:**
- Masalah umum di macOS dengan banyak window/apps
- Bisa disebabkan oleh external display atau many Spaces
- Normal untuk macOS dengan beberapa app terbuka

**Hermes Agent 8.9%:**
- Masih dalam batas wajar untuk agent dengan tool calls
- Python venv di `/Users/zaryu/src/hermes-agent/.venv/bin/python`

---

## 3. Memory Analysis

### Virtual Memory Stats

| Metric | Pages | GB |
|--------|-------|-----|
| **Free** | 334,935 | ~1.3 GB |
| **Active** | 1,545,924 | ~6.0 GB |
| **Inactive** | 1,515,163 | ~5.9 GB |
| **Wired Down** | 760,231 | ~3.0 GB |
| **Speculative** | 29,898 | ~0.1 GB |
| **Compressed** | 24,704 pages | ~0.1 GB |
| **Purgeable** | 32,978 | ~0.1 GB |

### Memory Pressure
- **Available:** ~1.36 GB free + purgeable
- **Memory Pressure:** Moderate to High
- **Pageins:** 1,267,387 (situs web/apps di-swap)

### Top Memory Consumers

| Process | Mem% | Mem (MB) |
|---------|------|----------|
| Firefox | 4.8% | 797 |
| Firefox plugin-container #1 | 7.6% | 1,274 |
| Firefox plugin-container #2 | 3.0% | 500 |
| Firefox plugin-container #3 | 2.7% | 447 |
| Nicegram Desktop | 2.9% | 482 |
| Firefox plugin-container #4 | 2.1% | 348 |
| Hermes Agent (python) | 2.1% | 357 |

**Total Firefox family: ~3.7 GB** — ini adalah masalah utama.

---

## 4. Disk Analysis

### Storage Overview

| Filesystem | Size | Used | Avail | Capacity |
|------------|------|------|-------|----------|
| /dev/disk1s4s1 | 128 GB | 16 GB | 12 GB | 58% |

### Disk I/O Activity

| Disk | KB/t | tps | MB/s |
|------|------|-----|------|
| disk0 | 33.02 | 232 | 7.49 |
| disk2 | 3.71 | 0 | 0.00 |
| disk4 | 3.72 | 0 | 0.00 |

**Disk I/O: 7.49 MB/s** — moderate activity.

### Top Disk Consumers (Niumination)

| Folder | Size |
|--------|------|
| services/ | 3.9 GB |
| dotfiles/ | 2.4 GB |
| apps/ | 1.9 GB |
| archive/ | 1.8 GB |
| sandbox/ | 202 MB |
| labs/ | 102 MB |
| desktop/ | 62 MB |
| sites/ | 42 MB |
| brain/ | 35 MB |
| agents/ | 34 MB |

**Total Niumination: ~10.5 GB** — masih dalam batas wajar.

---

## 5. Network Status

### Active Connections
- **Total active connections:** 32
- **Network interface:** WiFi (192.168.1.59)
- **Status:** Active

### Key Network Services
- **ControlCenter:** Listening on port 7000, 5000
- **Nicegram:** Connected to Telegram servers (91.108.56.115:443)
- **Identity services:** UDP active

---

## 6. Power & Thermal

### Battery Status
- **Power Source:** AC Power
- **Battery Level:** 83%
- **Charging:** Not charging
- **Sleep Count:** 0
- **Dark Wake Count:** 0
- **User Wake Count:** 0

### Thermal Status
- **CPU Power:** 100% (no throttling)
- **CPU Available:** 8 cores
- **Thermal Warning:** None
- **Performance Warning:** None

### ✅ Thermal Status: Excellent
- No thermal throttling detected
- CPU running at full speed
- No performance warnings

---

## 7. System Information

| Item | Value |
|------|-------|
| **OS** | macOS 26.5 |
| **Kernel** | Darwin 25.5.0 |
| **CPU** | Intel Core i5-10310U @ 1.70GHz |
| **Cores** | 8 logical |
| **RAM** | 16 GB |
| **Disk** | 128 GB SSD |
| **Uptime** | 1 jam 26 menit |
| **Users** | 3 active |

---

## 8. Identified Issues

### 🔴 Critical
1. **Firefox excessive resource usage** — 5 processes, 110% CPU, 2.6 GB RAM
   - **Impact:** System slowdown, high load average
   - **Fix:** Close unused Firefox tabs/windows, disable unnecessary extensions

### 🟡 Warning
2. **Memory pressure moderate-high** — hanya 1.3 GB free dari 16 GB
   - **Impact:** Swap usage increasing, potential slowdown
   - **Fix:** Close Firefox, restart apps, or add swap

3. **Load average 3.70 (15m)** — above CPU core count
   - **Impact:** System responsiveness may degrade
   - **Fix:** Reduce Firefox usage, close unnecessary apps

4. **WindowServer 41.5% CPU** — higher than normal
   - **Impact:** Graphics rendering overhead
   - **Fix:** Reduce number of windows/spaces, disable unnecessary display features

### 🟢 Normal
5. **Hermes Agent 8.9% CPU** — within expected range for active agent
6. **Disk 58% used** — healthy, plenty of space
7. **Thermal normal** — no throttling
8. **Network stable** — 32 connections, no errors

---

## 9. Recommendations

### Immediate Actions
1. **Close Firefox** jika tidak sedang digunakan — bisa membebaskan 110% CPU dan 2.6 GB RAM
2. **Restart Hermes Agent** jika tool calls sedang idle untuk reset memory
3. **Clear Firefox cache** jika browser perlu tetap terbuka

### Medium-term
4. **Monitor memory pressure** — jika terus naik, pertimbangkan upgrade RAM atau close apps yang tidak perlu
5. **Optimize Niumination folder** — services/ 3.9G bisa diarsipkan/reduce
6. **Check Firefox extensions** — beberapa extension bisa menyebabkan high CPU

### Long-term
7. **Consider RAM upgrade** jika经常 memory pressure
8. **Monitor thermal** saat usage tinggi — battery health check

---

## 10. Performance Score

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| CPU Utilization | 6/10 | 30% | 1.8 |
| Memory Health | 5/10 | 30% | 1.5 |
| Disk Health | 9/10 | 20% | 1.8 |
| Thermal | 9/10 | 10% | 0.9 |
| Network | 8/10 | 10% | 0.8 |
| **Overall** | | | **6.8/10** |

**Performance Rating: 🟡 Fair** — System functional but Firefox causing significant slowdown.

---

## Bukti

- `sysctl -n machdep.cpu.brand_string` → Intel Core i5-10310U
- `sysctl -n hw.memsize` → 16 GB
- `uptime` → load averages 2.52 2.47 3.70
- `ps -eo pid,user,%cpu,%mem,vsz,rss,comm | sort -k3 -rn | head -10` → Firefox 62%, WindowServer 41.5%
- `vm_stat` → Pages free 334,935, active 1,545,924, wired 760,231
- `df -h /` → 128 GB total, 58% used
- `pmset -g therm` → No thermal warning, CPU_Speed_Limit = 100
- `memory_pressure` → ~1.36 GB available
- `du -sh ~/Desktop/Niumination/* | sort -rh | head -10` → services 3.9G, dotfiles 2.4G

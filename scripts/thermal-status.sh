#!/bin/sh
# thermal-status.sh — quick readout for Niumination ecosystem
T=$(osx-cpu-temp 2>/dev/null || echo "n/a")
L=$(uptime | awk -F'load averages:' '{print $2}')
echo "Temp : $T"
echo "Load :$L"
echo "Top CPU hogs:"
ps -Ao pid,%cpu,command -r 2>/dev/null | head -7 | cut -c1-110

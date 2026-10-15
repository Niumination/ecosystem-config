# Brain-Capture Script Location

## Problem
The `brain-daily-capture` cron job (scheduled 21:00 daily, `no_agent=true`) errored because the script file was not found at the location the cron engine expects.

## Actual Location
The canonical source is:
```
/Users/zaryu/Desktop/Niumination/Production/niu-dash/data/scripts/brain-capture.py
```

## Cron Expects It At
```
/Volumes/HermesAgent/HermesAgentUSB/data/scripts/brain-capture.py
```

## Fix (when cron errors with "can't open file")
```bash
cp /Users/zaryu/Desktop/Niumination/Production/niu-dash/data/scripts/brain-capture.py \
   /Volumes/HermesAgent/HermesAgentUSB/data/scripts/brain-capture.py
```

## Why the discrepancy
The script lives in `Production/niu-dash/data/scripts/` (part of the niu-dash web app), not in `scripts/` (root-level utilities) or `brain/` (vault). The cron job was registered with `script="brain-capture.py"` which resolves relative to the Hermes profile's `data/scripts/` directory. When the USB profile was set up or refreshed, this file was not copied over.

## Verification
After copying, test the script runs cleanly:
```bash
python3 /Volumes/HermesAgent/HermesAgentUSB/data/scripts/brain-capture.py
```
Expected output:
```
✅ Created: inbox/<YYYY-MM-DD>-daily.md
📁 /Users/zaryu/Desktop/Niumination/brain/inbox/<YYYY-MM-DD>-daily.md
```

## Pitfall: similar file names
There is NO file called `brain-capture.py` anywhere else in the Niumination tree — `find /Users/zaryu/Desktop/Niumination -name "brain-capture.py"` returns exactly one hit at the `Production/niu-dash/data/scripts/` path. If a future search returns multiple matches, prefer the Production version.

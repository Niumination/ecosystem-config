#!/usr/bin/env bash
# QA probe for a vertical render: facts, frame grabs, 3-up contact sheets, audio levels, md5.
# Usage:  reels-qa.sh <video.mp4> [outdir]
#         QATS="1 5 9" reels-qa.sh <video.mp4>      # override grab timestamps (seconds)
# Exit status is non-zero only on real failure (missing tools / missing input).
set -euo pipefail

VIDEO="${1:?usage: reels-qa.sh <video> [outdir]}"
[ -f "$VIDEO" ] || { echo "no such file: $VIDEO" >&2; exit 1; }
for t in ffmpeg ffprobe; do command -v "$t" >/dev/null || { echo "missing dependency: $t" >&2; exit 1; }; done

OUT="${2:-$(cd "$(dirname "$VIDEO")" && pwd)/qa-$(basename "${VIDEO%.*}")}"
mkdir -p "$OUT/frames"
read -r -a TS <<< "${QATS:-2.5 7.5 13 21 28.5 35.5}"

echo "== facts =="
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,channels \
  -show_entries format=duration,size -of default=noprint_wrappers=1 "$VIDEO"

echo "== frames @ ${TS[*]}s =="
i=0
for ts in "${TS[@]}"; do
  i=$((i + 1))
  ffmpeg -v error -ss "$ts" -i "$VIDEO" -frames:v 1 -y "$OUT/frames/f$(printf '%02d' "$i")_${ts}s.png"
done
ls -1 "$OUT"/frames

# 3 frames per contact sheet, scaled to 600px wide so text stays legible for vision review.
shopt -s nullglob
files=("$OUT"/frames/*.png)
shopt -u nullglob
[ "${#files[@]}" -gt 0 ] || { echo "no frames extracted" >&2; exit 1; }
group=0
for ((k = 0; k < ${#files[@]}; k += 3)); do
  group=$((group + 1))
  args=(); fc=""; labels=""
  for ((j = k; j < k + 3 && j < ${#files[@]}; j++)); do
    idx=$((j - k))
    args+=(-i "${files[$j]}")
    fc+="[$idx:v]scale=600:-2[v$idx];"
    labels+="[v$idx]"
  done
  count=$(( ${#files[@]} - k )); [ "$count" -gt 3 ] && count=3
  ffmpeg -v error -y "${args[@]}" -filter_complex "${fc}${labels}hstack=inputs=${count}" "$OUT/sheet_$group.png"
  echo "sheet: $OUT/sheet_$group.png"
done

echo "== audio levels =="
# NB: -v error hides volumedetect output; a silent video legitimately has none, hence the || true.
ffmpeg -hide_banner -i "$VIDEO" -af volumedetect -f null - 2>&1 \
  | grep -E 'mean_volume|max_volume' || echo "no audio track (or silent render)"

echo "== md5 =="
md5 -q "$VIDEO" 2>/dev/null || md5sum "$VIDEO"

echo "== next: inspect sheet_*.png with the vision tool before rendering at --quality=high =="

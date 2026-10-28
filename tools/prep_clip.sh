#!/bin/sh
# Turn a raw hero clip into a short, silent, seamless loop for the site.
# usage: sh tools/prep_clip.sh raw.mp4 assets/hero/sigma.mp4 [seconds, default 3.5]
# Takes the first N seconds, plays them forward then backward (no jump at the loop point),
# drops the audio and encodes small H.264 for the web.
set -e
in="$1"; out="$2"; t="${3:-3.5}"
ffmpeg -loglevel error -y -t "$t" -i "$in" -an \
  -filter_complex "[0:v]setpts=PTS-STARTPTS,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0,format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -preset slow -crf 26 -movflags +faststart "$out"
echo "wrote $out"

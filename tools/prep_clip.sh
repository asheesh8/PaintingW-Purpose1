#!/bin/sh
# Turn a raw hero clip into a short, silent web clip for the site.
# usage: sh tools/prep_clip.sh raw.mp4 assets/hero/sigma.mp4 [seconds, default 7]
# Keeps the first N seconds, drops the audio and encodes small H.264. The clips start on the same
# frame as the hero still, so the site loops them by dissolving back to the still and playing again.
set -e
in="$1"; out="$2"; t="${3:-7}"
ffmpeg -loglevel error -y -t "$t" -i "$in" -an -vf "scale='min(1920,iw)':-2,format=yuv420p" \
  -c:v libx264 -preset slow -crf 25 -movflags +faststart "$out"
echo "wrote $out"

#!/bin/sh
# Builds the home hero background loop from the three stabilized walkthroughs.
# usage (from this folder): sh make_loop.sh
# Sigma -> Library -> Victorian -> back to Sigma, with slow crossfades. The loop is cut so its last
# frame flows straight into its first, so the browser can repeat it with no visible jump.
set -e
F=1.5                                   # crossfade length, seconds
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 stabilized/1-sigma.mp4)
calc() { awk "BEGIN { printf \"%.4f\", $1 }"; }
O1=$(calc "$D - $F"); O2=$(calc "2*($D - $F)"); O3=$(calc "3*($D - $F)")
END=$(calc "3*$D - 2*$F")
mkdir -p out

# 1. the sharp master: S, L, V, then S again, trimmed to one seamless lap
ffmpeg -loglevel error -y -i stabilized/1-sigma.mp4 -i stabilized/2-library.mp4 -i stabilized/3-victorian.mp4 -i stabilized/1-sigma.mp4 \
  -filter_complex "[0:v]fps=30,settb=AVTB[a];[1:v]fps=30,settb=AVTB[b];[2:v]fps=30,settb=AVTB[c];[3:v]fps=30,settb=AVTB[d];\
[a][b]xfade=transition=fade:duration=$F:offset=$O1[ab];[ab][c]xfade=transition=fade:duration=$F:offset=$O2[abc];\
[abc][d]xfade=transition=fade:duration=$F:offset=$O3,trim=start=$F:end=$END,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -preset slow -crf 14 out/hero-loop-sharp-1080.mp4

# 2. web versions: a soft blur so the logo reads on top (darkening is left to the page's CSS)
web() { # out, filter, crf
  ffmpeg -loglevel error -y -i out/hero-loop-sharp-1080.mp4 -vf "$2,format=yuv420p" -an \
    -c:v libx264 -preset slow -crf "$3" -profile:v high -movflags +faststart "out/$1"; }
web hero-loop-1080.mp4 "gblur=sigma=5" 23
web hero-loop-720.mp4 "scale=1280:720:flags=lanczos,gblur=sigma=3.4" 24
web hero-loop-tall.mp4 "crop=608:1080,scale=720:1280:flags=lanczos,gblur=sigma=5" 24
ffmpeg -loglevel error -y -i out/hero-loop-1080.mp4 -frames:v 1 -q:v 3 out/hero-poster.jpg
ffmpeg -loglevel error -y -i out/hero-loop-tall.mp4 -frames:v 1 -q:v 3 out/hero-poster-tall.jpg
ls -la out

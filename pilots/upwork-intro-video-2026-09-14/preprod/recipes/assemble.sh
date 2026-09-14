#!/usr/bin/env bash
# ffmpeg assembly skeleton for the ~60 s, 16:9, 1080p24 film. USD 0, local only.
# PROVENANCE: written fresh; the audio-stacking shape (atrim + afade + amix, video stream copy) is adapted from
# eval/harness-v2/stack_audio.py; the H.264 export flags from eval/harness-v2/instruments/imageio.py VideoWriter
# (libx264, crf 18, yuv420p, +faststart). ffmpeg 8.1.2 (Homebrew) checked 2026-09-14: libx264, aac, xfade, acrossfade,
# loudnorm, overlay, drawbox present; drawtext / subtitles / ass ABSENT (no libfreetype, no libass) -> captions and
# lower thirds are PNG overlays from overlay_text_video.py, never drawtext.
# NEVER RUN on real footage. Every step is one command; edit the file lists and run step by step.
set -euo pipefail
FPS=24; W=1920; H=1080
GEN=../../gen        # generated clips land here (ledgered)
ASM=../../assembly   # intermediates + master
mkdir -p "$ASM"

# ---------------------------------------------------------------------------------------------- 0. conform
# Routes deliver different sizes / rates (measured on the Lab's sealed clips): Kling v3 Pro 1080p@24, Veo 720p@24,
# Omni 720p@24, Wan 3.0 Prime 720p@30, H3 Max 768p@24 and ~0.6 s LONGER than asked. Everything is conformed to
# 1920x1080, 24 fps, 48 kHz stereo, constant frame rate, before any cut. Upscales from 720p/768p are lanczos.
conform() {  # conform <in.mp4> <out.mp4>
  ffmpeg -y -v error -i "$1" \
    -vf "scale=${W}:${H}:force_original_aspect_ratio=decrease:flags=lanczos,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2,fps=${FPS},format=yuv420p" \
    -af "aresample=48000,aformat=channel_layouts=stereo" -c:v libx264 -crf 16 -preset slow -c:a aac -b:a 192k -ar 48000 "$2"
}
# for i in "$GEN"/*.mp4; do conform "$i" "$ASM/c_$(basename "$i")"; done

# ---------------------------------------------------------------------------------------------- 1. trims
# H3 Max over-delivers (6.59 s for a 6 s ask): trim to the planned length; presenter takes: trim to the spoken line
# plus 0.3 s handles. -ss/-t after -i for frame accuracy on the conformed files.
trim() { ffmpeg -y -v error -i "$1" -ss "$2" -t "$3" -c:v libx264 -crf 16 -preset slow -c:a aac -b:a 192k "$4"; }

# ---------------------------------------------------------------------------------------------- 2. picture cut
# Straight cuts: concat demuxer over conformed files (same codec params -> stream copy is fine, but re-encode once at
# the end anyway). Crossfades: xfade (video) + acrossfade (audio), 0.5 s, between two clips at a time.
# printf "file '%s'\n" "$ASM"/c_s01.mp4 "$ASM"/c_s02.mp4 ... > "$ASM/cut.txt"
# ffmpeg -y -v error -f concat -safe 0 -i "$ASM/cut.txt" -c copy "$ASM/picture_cuts.mp4"
xfade_pair() {  # xfade_pair <a.mp4> <b.mp4> <a_duration_s> <out.mp4>   (offset = a_dur - 0.5)
  local off; off=$(python3 -c "print(max(0,$3-0.5))")
  ffmpeg -y -v error -i "$1" -i "$2" -filter_complex \
    "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=${off}[v];[0:a][1:a]acrossfade=d=0.5[a]" \
    -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset slow -c:a aac -b:a 192k "$4"
}

# ---------------------------------------------------------------------------------------------- 3. text layers (USD 0)
# Exact text is never asked of a video model (RR-6). Render with overlay_text_video.py and burn onto the conformed
# shot BEFORE the cut, so every frame carries it:
#   python3 overlay_text_video.py render --text "..." --font latin-bold --size 84 --colour F5E9D3 --out "$ASM/t_offer.png"
#   python3 overlay_text_video.py animate --clip "$ASM/c_s07.mp4" --layer "$ASM/t_offer.png:left:0.78:x_frac=0.06:in=0.4:out=5.6:motion=slide-up" --out "$ASM/c_s07_text.mp4"
# Lower third for the presenter: a name + role layer, left, y 0.86, in 0.5 out 4.5, motion slide-left.
# End card: a 5 s solid colour or the accepted still held (ffmpeg -loop 1 -i still.png -t 5), then layers on top.
end_card() {  # end_card <bg.png> <seconds> <out.mp4>
  ffmpeg -y -v error -loop 1 -framerate $FPS -i "$1" -f lavfi -i "anullsrc=r=48000:cl=stereo" -t "$2" \
    -vf "scale=${W}:${H},format=yuv420p" -c:v libx264 -crf 16 -c:a aac -shortest "$3"
}

# ---------------------------------------------------------------------------------------------- 4. music bed 60 s
# Lyria 2 gives ~32.8 s per track (measured 32.768 s). Two ways to 60 s:
#  (a) LOOP one accepted track with a 4 s acrossfade: 32.8 + 32.8 - 4 = 61.6 s, same key/tempo by construction. Try first.
#  (b) TWO generations (A then B) joined with acrossfade at a scene change; different pieces, so audition the seam.
music60_loop() {  # music60_loop <track.wav> <out.wav>
  ffmpeg -y -v error -i "$1" -i "$1" -filter_complex "[0:a][1:a]acrossfade=d=4:c1=tri:c2=tri[a]" -map "[a]" -t 60.5 "$2"
}
music60_two() { ffmpeg -y -v error -i "$1" -i "$2" -filter_complex "[0:a][1:a]acrossfade=d=3[a]" -map "[a]" -t 60.5 "$3"; }

# ---------------------------------------------------------------------------------------------- 5. audio mix
# Layers: presenter native speech (in the picture clips) and/or Sarvam VO (22.05 kHz mono -> resampled), music bed,
# per-shot ambience. Music ducks under speech with sidechaincompress; final loudness EBU R128 -14 LUFS (web/social),
# true peak -1 dBTP. Two-pass loudnorm is more accurate; single pass shown.
mix() {  # mix <picture_with_speech.mp4> <vo.wav or ''> <music60.wav> <out.mp4>
  local vo_in="" vo_graph="[0:a]volume=1.0[sp]"
  if [ -n "$2" ]; then vo_in="-i $2"; vo_graph="[0:a]volume=0.6[amb];[3:a]aresample=48000,aformat=channel_layouts=stereo[vo];[amb][vo]amix=inputs=2:duration=first:dropout_transition=0[sp]"; fi
  # inputs: 0 picture, 1 music, (3 = vo when present; index 2 kept free for a future ambience file)
  ffmpeg -y -v error -i "$1" -i "$3" -f lavfi -i "anullsrc=r=48000:cl=stereo" $vo_in -filter_complex \
    "${vo_graph};[1:a]volume=0.35[mus];[mus][sp]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=400[musd];[musd][sp]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1:LRA=11[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "$4"
}

# ---------------------------------------------------------------------------------------------- 6. captions (optional)
# No libass here: burn captions as timed PNG layers (overlay_text_video.py animate, one --layer per caption with in=/out=),
# or deliver a sidecar .srt for Upwork (write it by hand from the script; ffmpeg can mux it: -i film.srt -c:s mov_text).

# ---------------------------------------------------------------------------------------------- 7. master
master() {  # master <mixed.mp4> <out.mp4>   1080p H.264 High, yuv420p, 24 fps, AAC 192k, faststart
  ffmpeg -y -v error -i "$1" -c:v libx264 -profile:v high -level 4.1 -crf 18 -preset slow -pix_fmt yuv420p -r $FPS \
    -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$2"
  ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate -show_entries format=duration -of default=nw=1 "$2"
}
echo "skeleton loaded; call the functions step by step (conform / trim / xfade_pair / end_card / music60_loop / mix / master)"

#!/bin/bash
# Usage: ./build.sh ep001-kestrel-ridge   -> builds work/<ep>/out/{long.mp4,short.mp4,long.en.srt}
set -euo pipefail
EP=$1; ROOT=$(cd "$(dirname "$0")" && pwd); WK=$ROOT/work/$EP
mkdir -p "$WK" ~/.fonts "$ROOT/models"
cp "$ROOT"/engine/*.py "$WK"/; cp "$ROOT/episodes/$EP"/*.py "$WK"/
for f in ofl/patrickhand/PatrickHand-Regular.ttf ofl/bebasneue/BebasNeue-Regular.ttf ofl/kalam/Kalam-Bold.ttf; do
  [ -f ~/.fonts/$(basename $f) ] || curl -sL -o ~/.fonts/$(basename $f) https://raw.githubusercontent.com/google/fonts/main/$f; done
fc-cache -f >/dev/null
U=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f "$ROOT/models/kokoro-v1.0.onnx" ] || curl -sL -o "$ROOT/models/kokoro-v1.0.onnx" $U/kokoro-v1.0.onnx
[ -f "$ROOT/models/voices-v1.0.bin" ] || curl -sL -o "$ROOT/models/voices-v1.0.bin" $U/voices-v1.0.bin
cd "$WK"; ln -sfn "$ROOT/models" models; mkdir -p img audio2 out
python3 render_imgs.py
python3 tts_v2.py
python3 make.py audio
python3 make.py srt
python3 make.py video
python3 qc.py 2>/dev/null || true
ffmpeg -loglevel error -y -i out/video_000000.mp4 -i out/mix.wav -map 0:v -map 1:a -c:v copy \
  -af "loudnorm=I=-15:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart out/long.mp4
RANGES=$(python3 -c "import json;print(json.dumps(json.load(open('$ROOT/episodes/$EP/meta.json'))['short']['ranges']))")
HOOK=$(python3 -c "import json;print(json.load(open('$ROOT/episodes/$EP/meta.json'))['short']['hook'])")
python3 short.py "$RANGES" "$HOOK"; mv out/short_v1.mp4 out/short.mp4
cp out/kestrel_ridge.en.srt out/long.en.srt
N=$(echo "$EP" | sed -E 's/^ep0*([0-9]+).*/\1/'); STYLE=$([ $((N % 2)) -eq 1 ] && echo rules || echo alone)
python3 thumb.py "$ROOT/episodes/$EP/meta.json" $STYLE
echo $STYLE > out/thumb_style.txt
# QC: duration + black frames
python3 - <<'PY'
import subprocess,sys
d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/long.mp4']))
b=subprocess.run(['ffmpeg','-hide_banner','-i','out/long.mp4','-vf','scale=320:-1,blackdetect=d=0.5:pix_th=0.06','-an','-f','null','-'],capture_output=True,text=True).stderr.count('black_start')
print('QC duration',d,'black',b)
if d<420 or d>660 or b>0: sys.exit('QC FAILED')
PY
echo BUILD_OK
